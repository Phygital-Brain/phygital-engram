#!/bin/sh
# Starts Phygital Engram as the unprivileged user "app" (uid 10001).
# A volume is often created owned by root. This makes /data belong to that user first, then drops root.
# Your notes at /notes are mounted read-only and are never changed.
set -eu
if [ "$(id -u)" = "0" ]; then
  mkdir -p /data
  [ "$(stat -c %u /data)" = "10001" ] || chown -R 10001:10001 /data
  exec setpriv --reuid=10001 --regid=10001 --init-groups "$@"
fi
exec "$@"
