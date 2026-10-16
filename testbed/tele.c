/* tele.c -- X3: a 1,000-B telemetry message every PERIOD ms over TLS 1.3 (OpenSSL 3.5), through link
 * outages taken from measured handover interruptions, under three session policies:
 *   keep      the TLS session and TCP connection survive the outage (TCP retransmits)
 *   reconnect at each outage the session state is lost; after it the client does a full handshake
 *   resume    as reconnect, but the new connection resumes with the last ticket (psk_dhe_ke: fresh key share, no certs)
 * Every message carries its sequence number and generation time (CLOCK_MONOTONIC, shared by all namespaces).
 *
 * server: tele s PORT CERT KEY CHAIN|- CAFILE GROUPS MUTUAL
 *         prints "R seq t_gen t_recv conn" per message and "H conn t_hs_done resumed" per connection
 * client: tele c HOST PORT CAFILE GROUPS CERT|- KEY|- CHAIN|- DURATION_S PERIOD_MS POLICY OUTAGE_FILE
 *         OUTAGE_FILE: lines "t_start t_end" in absolute CLOCK_MONOTONIC seconds (the emulator reads the same file)
 *         prints "K conn t_connect_start t_hs_done resumed" per connection
 */
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <signal.h>

#define MSG 1000
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
static void die(const char *m) { fprintf(stderr, "%s\n", m); ERR_print_errors_fp(stderr); exit(1); }
static SSL_SESSION *last_sess = NULL;
static int new_sess_cb(SSL *ssl, SSL_SESSION *s) { (void)ssl; if (last_sess) SSL_SESSION_free(last_sess); last_sess = s; return 1; }

static void server(char **a) {
    int port = atoi(a[2]); const char *cert = a[3], *key = a[4], *chain = a[5], *ca = a[6], *groups = a[7]; int mutual = atoi(a[8]);
    SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
    SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);
    if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("chain"); }
    else if (SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("cert");
    if (SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("key");
    if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
    SSL_CTX_set_num_tickets(ctx, 1);
    /* required for resumption when client certificates are verified; without it OpenSSL aborts resumed handshakes */
    SSL_CTX_set_session_id_context(ctx, (const unsigned char *)"x3tele", 6);
    if (mutual) { SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL); }
    int ls = socket(AF_INET, SOCK_STREAM, 0), one = 1;
    setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
    struct sockaddr_in sa = {0}; sa.sin_family = AF_INET; sa.sin_port = htons(port); sa.sin_addr.s_addr = INADDR_ANY;
    if (bind(ls, (void *)&sa, sizeof sa) || listen(ls, 16)) die("listen");
    fprintf(stderr, "ready\n");
    unsigned char buf[MSG];
    for (int conn = 0;; conn++) {
        int s = accept(ls, NULL, NULL);
        setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
        SSL *ssl = SSL_new(ctx); SSL_set_fd(ssl, s);
        if (SSL_accept(ssl) != 1) { SSL_free(ssl); close(s); continue; }
        printf("H %d %.6f %d\n", conn, now(), SSL_session_reused(ssl)); fflush(stdout);
        for (;;) {
            int got = 0, r = 0, newconn = 0;
            while (got < MSG) {
                if (!SSL_pending(ssl)) {   /* a new connection means the client lost this session: abandon it */
                    struct pollfd pf[2] = { { s, POLLIN, 0 }, { ls, POLLIN, 0 } };
                    poll(pf, 2, -1);
                    if ((pf[1].revents & POLLIN) && !(pf[0].revents & POLLIN)) { newconn = 1; break; }
                }
                r = SSL_read(ssl, buf + got, MSG - got); if (r <= 0) break; got += r;
            }
            (void)newconn;
            if (got < MSG) break;
            double t = now(); unsigned int seq; double tg;
            memcpy(&seq, buf, 4); memcpy(&tg, buf + 4, 8);
            if (seq == 0xFFFFFFFFu) { printf("END\n"); fflush(stdout); exit(0); }
            printf("R %u %.6f %.6f %d\n", seq, tg, t, conn);
        }
        fflush(stdout);
        SSL_free(ssl); close(s);
    }
}

typedef struct { double a, b; } win;
static volatile int dbg_qh, dbg_qt, dbg_down, dbg_wi, dbg_conn, dbg_stage; static double dbg_t0;
static void on_alarm(int sig) { (void)sig; fprintf(stderr, "WATCHDOG t=%.3f stage=%d qh=%d qtail=%d down=%d wi=%d conn=%d\n", now() - dbg_t0, dbg_stage, dbg_qh, dbg_qt, dbg_down, dbg_wi, dbg_conn); _exit(3); }

int main(int argc, char **argv) {
    if (argc < 2) die("usage");
    if (argv[1][0] == 's') { server(argv); return 0; }
    const char *host = argv[2]; int port = atoi(argv[3]); const char *ca = argv[4], *groups = argv[5], *cert = argv[6], *key = argv[7], *chain = argv[8];
    double dur = atof(argv[9]), period = atof(argv[10]) / 1e3; const char *policy = argv[11];
    win W[256]; int nw = 0;
    FILE *f = fopen(argv[12], "r"); if (!f) die("outages");
    while (nw < 256 && fscanf(f, "%lf %lf", &W[nw].a, &W[nw].b) == 2) nw++;
    fclose(f);
    int keep = !strcmp(policy, "keep"), resume = !strcmp(policy, "resume");
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
    SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);
    SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
    if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
    SSL_CTX_set_session_cache_mode(ctx, SSL_SESS_CACHE_CLIENT | SSL_SESS_CACHE_NO_INTERNAL_STORE);
    SSL_CTX_sess_set_new_cb(ctx, new_sess_cb);
    if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("cchain"); }
    else if (strcmp(cert, "-") && SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("ccert");
    if (strcmp(key, "-") && SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("ckey");

    double t0 = now(), next = t0; unsigned int seq = 0;
    dbg_t0 = t0; signal(SIGALRM, on_alarm); alarm((unsigned)(dur + 40));
    /* queue of generated, unsent messages */
    static double qt[1 << 16]; static unsigned int qs[1 << 16]; int qh = 0, qtail = 0;
    SSL *ssl = NULL; int s = -1, conn = 0, wi = 0, down = 0;
    unsigned char msg[MSG]; memset(msg, 'x', MSG);
    for (;;) {
        double t = now();
        dbg_qh = qh; dbg_qt = qtail; dbg_down = down; dbg_wi = wi; dbg_conn = conn; dbg_stage = 1;
        if (t >= t0 + dur && qh == qtail) break;
        while (next <= t && next < t0 + dur) { qt[qtail & 0xFFFF] = next; qs[qtail & 0xFFFF] = seq++; qtail++; next += period; }
        if (!keep) {  /* session state is lost at an outage start; reconnect at its end */
            if (!down && wi < nw && t >= W[wi].a) { if (ssl) { SSL_set_shutdown(ssl, SSL_SENT_SHUTDOWN | SSL_RECEIVED_SHUTDOWN); SSL_free(ssl); close(s); ssl = NULL; } down = 1; }  /* nothing is sent; the flag only keeps the ticket resumable */
            if (down && t >= W[wi].b) { down = 0; wi++; }
        }
        if (!ssl && !down) {
            s = socket(AF_INET, SOCK_STREAM, 0); int one = 1;
            setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
            struct sockaddr_in sa = {0}; sa.sin_family = AF_INET; sa.sin_port = htons(port); inet_pton(AF_INET, host, &sa.sin_addr);
            double tc = now();
            if (connect(s, (void *)&sa, sizeof sa)) die("connect");
            ssl = SSL_new(ctx); SSL_set_fd(ssl, s);
            if (resume && last_sess) SSL_set_session(ssl, last_sess);
            dbg_stage = 2;
            if (SSL_connect(ssl) != 1) die("tls");
            dbg_stage = 3;
            printf("K %d %.6f %.6f %d\n", conn++, tc, now(), SSL_session_reused(ssl)); fflush(stdout);
            fcntl(s, F_SETFL, fcntl(s, F_GETFL) | O_NONBLOCK);
        }
        if (ssl) {
            unsigned char rb[256]; int r = SSL_read(ssl, rb, sizeof rb); (void)r;  /* processes NewSessionTicket */
            ERR_clear_error();
            while (qh < qtail) {
                memcpy(msg, &qs[qh & 0xFFFF], 4); memcpy(msg + 4, &qt[qh & 0xFFFF], 8);
                int w = SSL_write(ssl, msg, MSG);
                if (w == MSG) { qh++; continue; }
                int e = SSL_get_error(ssl, w);
                if (e == SSL_ERROR_WANT_WRITE || e == SSL_ERROR_WANT_READ) break;
                die("write");
            }
        }
        double wake = next < t0 + dur ? next : t + 0.001;
        if (!keep && wi < nw) { double ev = down ? W[wi].b : W[wi].a; if (ev < wake) wake = ev; }
        double dt = wake - now();
        struct pollfd pf = { s, POLLOUT, 0 };
        if (ssl && qh < qtail) poll(&pf, 1, dt > 0 ? (int)(dt * 1e3) + 1 : 0);
        else if (dt > 0) usleep((useconds_t)(dt * 1e6));
    }
    dbg_stage = 4;
    /* end marker on a blocking socket */
    fcntl(s, F_SETFL, fcntl(s, F_GETFL) & ~O_NONBLOCK);
    unsigned int endm = 0xFFFFFFFFu; memcpy(msg, &endm, 4);
    SSL_write(ssl, msg, MSG);
    usleep(300000);
    return 0;
}
