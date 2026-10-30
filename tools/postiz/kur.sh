#!/bin/bash
# WSL (root) içinde koşar: /opt/postiz kurar, .env yoksa rastgele sırlarla üretir, yığını kaldırır.
# Sır değeri yazdırılmaz.
set -e
SRC="$(cd "$(dirname "$0")" && pwd)"
DST=/opt/postiz
mkdir -p "$DST/dynamicconfig"
cp "$SRC/docker-compose.yml" "$DST/docker-compose.yml"
cp "$SRC"/dynamicconfig/* "$DST/dynamicconfig/"
if [ ! -f "$DST/.env" ]; then
  PG=$(openssl rand -hex 16)
  cat > "$DST/.env" <<EOF
MAIN_URL=http://localhost:4007
FRONTEND_URL=http://localhost:4007
NEXT_PUBLIC_BACKEND_URL=http://localhost:4007/api
JWT_SECRET=$(openssl rand -hex 32)
POSTGRES_USER=postiz-user
POSTGRES_PASSWORD=$PG
POSTGRES_DB=postiz-db-local
DATABASE_URL=postgresql://postiz-user:$PG@postiz-postgres:5432/postiz-db-local
REDIS_URL=redis://postiz-redis:6379
DISABLE_REGISTRATION=false
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=
TIKTOK_CLIENT_ID=
TIKTOK_CLIENT_SECRET=
EOF
  chmod 600 "$DST/.env"
fi
cd "$DST"
docker compose pull -q
docker compose up -d
docker compose ps --format '{{.Name}} {{.Status}}'
