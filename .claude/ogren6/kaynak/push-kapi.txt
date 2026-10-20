#!/usr/bin/env bash
# VİDEO-GÖZ-1b-1R R0: push kapısı — gitleaks git temiz (çıkış 0) değilse push yok. Push yalnız bu betikle; boru yok (çıkış kodu maskelenmez).
gitleaks git --exit-code 1
rc=$?
if [ "$rc" -ne 0 ]; then
  echo "push-kapi: gitleaks çıkış $rc — push yapılmadı" >&2
  exit "$rc"
fi
exec git push "$@"
