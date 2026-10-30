#!/bin/bash
# WSL (root): yerel Postiz yöneticisini bir kez açar, API anahtarını .env'e (chmod 600) yazar. Sır yazdırmaz.
set -e
cd /opt/postiz
if grep -q '^POSTIZ_API_KEY=.\+' .env; then echo "api anahtarı zaten var"; exit 0; fi
for i in $(seq 1 40); do curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:4007/api/auth/can-register | grep -q 200 && break; sleep 5; done
PW=$(openssl rand -hex 12)
curl -s -o /dev/null -w 'register %{http_code}\n' -X POST http://127.0.0.1:4007/api/auth/register \
  -H 'Content-Type: application/json' \
  -d "{\"provider\":\"LOCAL\",\"email\":\"sosyal-oto@localhost.local\",\"password\":\"${PW}Aa1!\",\"company\":\"sosyal-oto\"}"
printf 'sosyal-oto@localhost.local\n%sAa1!\n' "$PW" > admin.txt && chmod 600 admin.txt
KEY=$(docker exec postiz-postgres psql -U postiz-user -d postiz-db-local -tA -c 'select "apiKey" from "Organization" limit 1')
[ -n "$KEY" ] && echo "POSTIZ_API_KEY=$KEY" >> .env && echo "api anahtarı yazıldı (uzunluk ${#KEY})"
