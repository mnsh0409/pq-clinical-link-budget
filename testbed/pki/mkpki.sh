#!/bin/bash
# Root -> intermediate -> leaf, for two algorithm families: ec (P-256/ECDSA-SHA256) and mldsa (ML-DSA-65).
# Leaves: server (CN=srv, SAN IP 10.9.0.2) and client (CN=device-01). Minimal X.509 extensions.
set -e
export LD_LIBRARY_PATH=/opt/ossl35/lib; O=/opt/ossl35/bin/openssl
key(){ case $1 in ec) $O genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out $2 2>/dev/null;; mldsa) $O genpkey -algorithm ML-DSA-65 -out $2;; falcon) $O genpkey -algorithm falcon512 -out $2;; esac; }
FAMS=${FAMS:-"ec mldsa"}   # FAMS=falcon needs OPENSSL_CONF pointing at a config that loads oqsprovider (testbed/oqs.cnf)
for f in $FAMS; do
  mkdir -p $f; cd $f
  printf "basicConstraints=critical,CA:TRUE\nkeyUsage=critical,keyCertSign\n" > ca.ext
  printf "basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\nsubjectAltName=IP:10.9.0.2\n" > srv.ext
  printf "basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\n" > cli.ext
  key $f root.key; $O req -new -x509 -key root.key -subj "/CN=root-$f" -days 3650 -out root.crt -addext basicConstraints=critical,CA:TRUE -addext keyUsage=critical,keyCertSign
  key $f int.key; $O req -new -key int.key -subj "/CN=int-$f" -out int.csr; $O x509 -req -in int.csr -CA root.crt -CAkey root.key -CAcreateserial -days 3650 -extfile ca.ext -out int.crt 2>/dev/null
  for who in srv cli; do
    key $f $who.key; $O req -new -key $who.key -subj "/CN=$who" -out $who.csr
    # leaf signed directly by root (chain of 2, root not sent) ...
    $O x509 -req -in $who.csr -CA root.crt -CAkey root.key -CAcreateserial -days 3650 -extfile $who.ext -out $who.byroot.crt 2>/dev/null
    # ... and by the intermediate (chain of 3, intermediate sent)
    $O x509 -req -in $who.csr -CA int.crt -CAkey int.key -CAcreateserial -days 3650 -extfile $who.ext -out $who.byint.crt 2>/dev/null
  done
  cd ..
done
for f in $FAMS; do for c in root int srv.byroot srv.byint; do printf "%s %s DER bytes: " $f $c; $O x509 -in $f/$c.crt -outform DER | wc -c; done; done
