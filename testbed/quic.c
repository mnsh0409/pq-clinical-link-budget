/* quic.c -- X4: one QUIC (RFC 9000/9001) connection + one 1,000-B stream message per run, OpenSSL 3.5 QUIC
 * client and server, timed on CLOCK_MONOTONIC. Tests whether the server's first flight exceeds QUIC's 3x
 * anti-amplification allowance (an extra round trip) and what address validation (Retry) adds.
 *
 * server: quic s PORT CERT KEY CHAIN|- CAFILE GROUPS MUTUAL VALIDATE(0/1) NRUNS
 *         prints "S <t_accept> <t_first_record> <group>"
 * client: quic c HOST PORT CAFILE GROUPS CERT|- KEY|- CHAIN|- NRUNS GAP_MS
 *         prints "C <t_start> <t_hs_done> <t_sent>"
 */
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/quic.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec + t.tv_nsec / 1e9; }
static void die(const char *m) { fprintf(stderr, "%s\n", m); ERR_print_errors_fp(stderr); exit(1); }
static const unsigned char ALPN[] = { 2, 'x', '4' };
static int alpn_cb(SSL *s, const unsigned char **out, unsigned char *outlen, const unsigned char *in, unsigned int inlen, void *arg) {
    (void)s; (void)arg;
    if (SSL_select_next_proto((unsigned char **)out, outlen, ALPN, sizeof ALPN, in, inlen) != OPENSSL_NPN_NEGOTIATED) return SSL_TLSEXT_ERR_ALERT_FATAL;
    return SSL_TLSEXT_ERR_OK;
}

int main(int argc, char **argv) {
    unsigned char buf[1000];
    if (argc < 2) die("usage");
    if (argv[1][0] == 's') {
        int port = atoi(argv[2]); const char *cert = argv[3], *key = argv[4], *chain = argv[5], *ca = argv[6], *groups = argv[7];
        int mutual = atoi(argv[8]), validate = atoi(argv[9]), n = atoi(argv[10]);
        SSL_CTX *ctx = SSL_CTX_new(OSSL_QUIC_server_method());
        if (!ctx) die("ctx");
        SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);
        if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("chain"); }
        else if (SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("cert");
        if (SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("key");
        if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
        SSL_CTX_set_alpn_select_cb(ctx, alpn_cb, NULL);
        SSL_CTX_set_num_tickets(ctx, 0);
        if (mutual) { SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL); }
        int fd = socket(AF_INET, SOCK_DGRAM, 0);
        struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); a.sin_addr.s_addr = INADDR_ANY;
        if (bind(fd, (void *)&a, sizeof a)) die("bind");
        SSL *ls = SSL_new_listener(ctx, validate ? 0 : SSL_LISTENER_FLAG_NO_VALIDATE);
        if (!ls || !SSL_set_fd(ls, fd) || !SSL_listen(ls)) die("listen");
        fprintf(stderr, "ready\n");
        for (int i = 0; i < n; i++) {
            SSL *c = SSL_accept_connection(ls, 0); double t0 = now();
            if (!c) die("accept_connection");
            SSL *st = SSL_accept_stream(c, 0);
            if (!st) die("accept_stream");
            int got = 0;
            while (got < (int)sizeof buf) { int r = SSL_read(st, buf + got, sizeof buf - got); if (r <= 0) die("read"); got += r; }
            double t1 = now();
            printf("S %.6f %.6f %s\n", t0, t1, SSL_get0_group_name(c)); fflush(stdout);
            SSL_write(st, "k", 1); SSL_stream_conclude(st, 0);
            SSL_free(st);
            while (SSL_shutdown(c) == 0) ;
            SSL_free(c);
        }
        SSL_free(ls);
    } else {
        const char *host = argv[2]; int port = atoi(argv[3]); const char *ca = argv[4], *groups = argv[5], *cert = argv[6], *key = argv[7], *chain = argv[8];
        int n = atoi(argv[9]); double gap = atof(argv[10]) / 1e3;
        SSL_CTX *ctx = SSL_CTX_new(OSSL_QUIC_client_method());
        SSL_CTX_set_mode(ctx, SSL_MODE_NO_AUTO_CHAIN);
        SSL_CTX_load_verify_locations(ctx, ca, NULL); SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, NULL);
        if (SSL_CTX_set1_groups_list(ctx, groups) != 1) die("groups");
        if (strcmp(chain, "-")) { if (SSL_CTX_use_certificate_chain_file(ctx, chain) != 1) die("cchain"); }
        else if (strcmp(cert, "-") && SSL_CTX_use_certificate_file(ctx, cert, SSL_FILETYPE_PEM) != 1) die("ccert");
        if (strcmp(key, "-") && SSL_CTX_use_PrivateKey_file(ctx, key, SSL_FILETYPE_PEM) != 1) die("ckey");
        memset(buf, 'x', sizeof buf);
        for (int i = 0; i < n; i++) {
            usleep((useconds_t)(gap * 1e6));
            int fd = socket(AF_INET, SOCK_DGRAM, 0);
            struct sockaddr_in a = {0}; a.sin_family = AF_INET; a.sin_port = htons(port); inet_pton(AF_INET, host, &a.sin_addr);
            if (connect(fd, (void *)&a, sizeof a)) die("udp connect");
            SSL *ssl = SSL_new(ctx);
            if (!ssl || !SSL_set_fd(ssl, fd)) die("ssl");
            BIO_ADDR *peer = BIO_ADDR_new();
            BIO_ADDR_rawmake(peer, AF_INET, &a.sin_addr, sizeof a.sin_addr, a.sin_port);
            if (!SSL_set1_initial_peer_addr(ssl, peer)) die("peer");
            BIO_ADDR_free(peer);
            if (SSL_set_alpn_protos(ssl, ALPN, sizeof ALPN)) die("alpn");
            double t0 = now();
            if (SSL_connect(ssl) != 1) die("quic connect");
            double t1 = now();
            if (SSL_write(ssl, buf, sizeof buf) != (int)sizeof buf) die("write");
            SSL_stream_conclude(ssl, 0);
            double t2 = now();
            printf("C %.6f %.6f %.6f\n", t0, t1, t2); fflush(stdout);
            char k; SSL_read(ssl, &k, 1);
            SSL_shutdown(ssl);
            SSL_free(ssl); close(fd);
        }
    }
    return 0;
}
