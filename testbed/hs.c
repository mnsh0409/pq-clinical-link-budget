/* hs.c -- one TLS 1.3 handshake + one 1,000-B application record, timed on CLOCK_MONOTONIC
 * (shared by all network namespaces of this machine, so client and server times are comparable).
 *
 * server: hs s PORT CERT KEY CHAIN|- CAFILE GROUPS MUTUAL(0/1) NRUNS
 *         prints per connection: "S <t_accept_start> <t_hs_done> <t_first_record>"
 * client: hs c HOST PORT CAFILE GROUPS CERT|- KEY|- CHAIN|- NRUNS GAP_MS
 *         prints per connection: "C <t_connect_start> <t_tcp_up> <t_hs_done> <t_record_sent>"
 * No session tickets, no resumption: every connection is a cold full handshake.
 */
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
static void die(const char *m) { fprintf(stderr, "%s\n", m); ERR_print_errors_fp(stderr); exit(1); }
static unsigned char buf[1000];

int main(int argc, char **argv) {
    if (argc < 2) die("usage");
    if (argv[1][0] == 's') {
        int port = atoi(argv[2]); const char *cert = argv[3], *key = argv[4], *chain = argv[5], *ca = argv[6], *groups = argv[7];
        int mutual = atoi(argv[8]), n = atoi(argv[9]);
        SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
        SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
        if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("chain"); }
        else if (SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("cert");
        if (SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("key");
        if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
        SSL_CTX_set_num_tickets(ctx, 0);
        if (!getenv("AUTOCHAIN")) SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);  /* send only the configured chain, never the root */
        SSL_CTX_set_options(ctx, SSL_OP_NO_TICKET);
        if (mutual) { SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL); }
        int ls = socket(AF_INET, SOCK_STREAM, 0), one = 1;
        setsockopt(ls, SOL_SOCKET, SO_REUSEADDR, &one, sizeof one);
        struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = INADDR_ANY;
        if (bind(ls, (void *)&a, sizeof a) || listen(ls, 16)) die("listen");
        fprintf(stderr, "ready\n");
        for (int i = 0; i < n; i++) {
            int s = accept(ls, NULL, NULL); double t0 = now();
            setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
            SSL *ssl = SSL_new(ctx); SSL_set_fd(ssl, s);
            if (SSL_accept(ssl) != 1) die("accept");
            double t1 = now(); int got = 0;
            while (got < (int)sizeof buf) { int r = SSL_read(ssl, buf + got, sizeof buf - got); if (r <= 0) die("read"); got += r; }
            double t2 = now();
            printf("S %.6f %.6f %.6f %s\n", t0, t1, t2, SSL_get0_group_name(ssl)); fflush(stdout);
            SSL_shutdown(ssl); SSL_free(ssl); close(s);
        }
    } else {
        const char *host = argv[2]; int port = atoi(argv[3]); const char *ca = argv[4], *groups = argv[5], *cert = argv[6], *key = argv[7], *chain = argv[8];
        int n = atoi(argv[9]); double gap = atof(argv[10]) / 1e3;
        SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
        SSL_CTX_set_min_proto_version(ctx, TLS1_3_VERSION);
        SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
        if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
        SSL_CTX_set_session_cache_mode(ctx, SSL_SESS_CACHE_OFF);
        if (!getenv("AUTOCHAIN")) SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);
        if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("cchain"); }
        else if (strcmp(cert, "-") && SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("ccert");
        if (strcmp(key, "-") && SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("ckey");
        memset(buf, 'x', sizeof buf);
        for (int i = 0; i < n; i++) {
            usleep((useconds_t)(gap * 1e6));
            int s = socket(AF_INET, SOCK_STREAM, 0), one = 1;
            setsockopt(s, IPPROTO_TCP, TCP_NODELAY, &one, sizeof one);
            struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); inet_pton(AF_INET, host, &a.sin_addr);
            double t0 = now();
            if (connect(s, (void *)&a, sizeof a)) die("connect");
            double t1 = now();
            SSL *ssl = SSL_new(ctx); SSL_set_fd(ssl, s); SSL_set1_host(ssl, NULL);
            if (SSL_connect(ssl) != 1) die("connect tls");
            double t2 = now();
            if (SSL_write(ssl, buf, sizeof buf) != (int)sizeof buf) die("write");
            double t3 = now();
            printf("C %.6f %.6f %.6f %.6f\n", t0, t1, t2, t3); fflush(stdout);
            char tmp[64]; SSL_read(ssl, tmp, sizeof tmp);  /* wait for server close_notify */
            SSL_free(ssl); close(s);
        }
    }
    return 0;
}
