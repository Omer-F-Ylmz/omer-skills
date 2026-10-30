#!/bin/bash
# POSTIZ-KUR-1: DB + .env yedegi -> Windows tarafi (WSL disina). Sir yazdirilmaz. Kullanim: wsl -d Ubuntu -u root -e bash /mnt/c/Projeler/omer-skills/tools/postiz/yedek.sh
set -e
H=/mnt/c/Users/pc/postiz-yedek; mkdir -p "$H/_arsiv"; T=$(date +%Y%m%d-%H%M)
docker exec postiz-postgres sh -c 'pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB"' | gzip > "$H/db-$T.sql.gz"
cp /opt/postiz/.env "$H/env-$T"; chmod 600 "$H/env-$T"
ls -t "$H"/db-* | tail -n +8 | xargs -r mv -t "$H/_arsiv/" 2>/dev/null || true
echo "yedek tamam: $H/db-$T.sql.gz $(stat -c %s "$H/db-$T.sql.gz") bayt"
