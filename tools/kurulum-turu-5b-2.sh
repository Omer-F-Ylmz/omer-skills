#!/usr/bin/env bash
# Kurulum turu 5b-2 — tur-5b-2 KUR (claude-reel-skills, 2 skill). Girdi: docs/kurulumlar/tur5b-2-sonuc.tsv.
# Kullanım: bash tools/kurulum-turu-5b-2.sh [--kuru]   (--kuru: yalnız komutları yazdır, yan etki yok)
# Her adım: kuruluysa atla → kur → doğrula → hata ise yalnız o aracı geri al + logla → sonrakine geç. Silme yok (kendi kopyası hariç).
set -euo pipefail
export MSYS_NO_PATHCONV=1

KOK="$(cd "$(dirname "$0")/.." && pwd)"
LOGD="$KOK/.kos/kurulum-5b-2"; mkdir -p "$LOGD"
LOG="$LOGD/kurulum-turu-5b-2.log"
GERI="$LOGD/geri-al.sh"
KLON="${KLON:-$KOK/.kos/kurulum-tarama/klon}"
SKD="$HOME/.claude/skills"
PMD="$HOME/.claude/plugins/marketplaces"
MOD="${1:-kur}"
TAMAM=0; HATA=0

log() { printf '%s\t%s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }
calis() { if [ "$MOD" = "--kuru" ]; then echo "+ $*"; else "$@"; fi; }
geri() { [ "$MOD" = "--kuru" ] || echo "$*" >> "$GERI"; }
mkonum() { cygpath -m "$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['installLocation'])" "$(cygpath -m "$HOME/.claude/plugins/known_marketplaces.json")" "$1")"; }
plugin_var() { grep -qF "$1" <<<"$(claude plugin list 2>&1)"; }
market_var() { grep -qE "❯ $1\$" <<<"$(claude plugin marketplace list 2>&1)"; }
sha_ok() { [[ $1 =~ ^[0-9a-f]{40}$ ]]; }

# klonla repo sha → KD (pinli SHA'da klon)
klonla() {
  local repo=$1 sha=$2
  sha_ok "$sha" || { log "HATA sha-gecersiz $repo"; return 1; }
  KD="$(cygpath -m "$KLON")/${repo/\//__}"
  if [ "$(git -C "$KD" rev-parse HEAD 2>/dev/null)" != "$sha" ]; then
    KD="$(cygpath -m "$LOGD")/klon/${repo/\//__}"; [ "$MOD" = "--kuru" ] || rm -rf "$KD"
    calis git clone -q --filter=blob:none --no-checkout "https://github.com/$repo" "$KD" || return 1
    calis git -C "$KD" checkout -q "$sha" || return 1
  fi
}
# uzaktan betik çeken/çalıştıran dosya (md hariç) varsa şüpheli
supheli() { grep -rEIl 'curl[^|]*\|[ ]*(ba)?sh|Invoke-Expression|base64 (-d|--decode)[^|]*\|[ ]*(ba)?sh' "$1" 2>/dev/null | grep -v '\.md$' | head -3 || true; }

# S|repo|sha|alt-yol|atlanacak-adlar   → alt-yol altındaki SKILL.md klasörleri ~/.claude/skills/<ad> ("." = tüm repo)
kur_skill() {
  local repo=$1 sha=$2 sub=$3 atla=" ${4:-} " f s ad h
  klonla "$repo" "$sha" || return 1
  [ "$MOD" = "--kuru" ] && { echo "+ kopya $repo/$sub SKILL.md klasörleri (atla:$atla) → $SKD/"; return 0; }
  while IFS= read -r f; do
    s=$(dirname "$f"); ad=$(basename "$s")
    [[ $atla == *" $ad "* ]] && { log "ATLA/KAPSAM-DISI skill $ad ($repo)"; continue; }
    if [ -e "$SKD/$ad" ]; then log "ATLA/CAKISMA skill $ad ($repo)"; continue; fi
    h=$(supheli "$s"); [ -n "$h" ] && { log "SUPHELI-ATLA skill $ad: $h"; continue; }
    cp -r "$s" "$SKD/$ad" && rm -rf "$SKD/$ad/.git"
    [ -f "$SKD/$ad/SKILL.md" ] || { rm -rf "${SKD:?}/$ad"; log "HATA kopya $ad"; return 1; }
    geri "rm -rf \"$SKD/$ad\"  # $repo"; log "OK skill $ad"
  done < <(find "$KD/$sub" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.claude/*')
}

# P|repo|sha|market   → marketplace'teki TÜM plugin'ler (pinli)
kur_plugin() {
  local repo=$1 sha=$2 m=$3 p ml
  if ! market_var "$m"; then
    calis claude plugin marketplace add "$repo" || return 1
    geri "claude plugin marketplace remove $m"
  fi
  [ "$MOD" = "--kuru" ] && { echo "+ git -C $PMD/$m checkout $sha; claude plugin install <hepsi>@$m"; return 0; }
  ml=$(mkonum "$m") || { log "PIN-HATA $m konum yok"; return 1; }
  git -C "$ml" fetch -q origin "$sha" 2>/dev/null || true
  git -C "$ml" checkout -q "$sha" || { log "PIN-HATA $m $sha"; return 1; }
  for p in $(python -I -c "import json,sys;print(' '.join(x['name'] for x in json.load(open(sys.argv[1],encoding='utf-8'))['plugins']))" "$ml/.claude-plugin/marketplace.json"); do
    if plugin_var "$p@$m"; then log "ATLA plugin $p@$m"; continue; fi
    claude plugin install -y --scope user "$p@$m" </dev/null || { log "HATA install $p@$m"; return 1; }
    plugin_var "$p@$m" || { log "HATA dogrula $p@$m"; claude plugin uninstall "$p@$m" || true; return 1; }
    geri "claude plugin uninstall $p@$m"; log "OK plugin $p@$m"
  done
}

VERI=$(cat <<'EOF'
S|witcharon/claude-reel-skills|69edd7dd6b717bdd8a389e07ea6625deabd65e24|skills|
EOF
)

log "=== kurulum-turu-5b-2 basla ($MOD) ==="
while IFS='|' read -r tur a b c d; do
  [ -z "$tur" ] || [ "${tur:0:1}" = "#" ] && continue
  case $tur in
    S) f=(kur_skill "$a" "$b" "$c" "$d") ;;
    P) f=(kur_plugin "$a" "$b" "$c") ;;
    *) log "BILINMEYEN $tur"; continue ;;
  esac
  if "${f[@]}"; then TAMAM=$((TAMAM+1)); else HATA=$((HATA+1)); log "ATLANDI-HATA $tur $a"; fi
done <<<"$VERI"

if [ "$MOD" != "--kuru" ]; then
  log "--- son doğrulama ---"
  claude plugin list >> "$LOG" 2>&1 || true
fi
log "=== bitti: adım-ok $TAMAM · hata $HATA · geri-al: $GERI ==="
