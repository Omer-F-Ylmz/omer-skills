#!/usr/bin/env bash
# Kurulum turu 3c — tur-3 KUR/KUR-duzeltmeli + anahtarsız kurulabilen HESAP yazılımı + elle-19'dan otomatikleşenler.
# Girdi: docs/kurulumlar/tur3-sonuc-*.tsv, kurulum-sirasi.md B. Tetikleyici/hesap listeleri: tetikleyici.md, hesaplar.md.
# Kullanım: bash tools/kurulum-turu-3.sh [--kuru]   (--kuru: yalnız komutları yazdır, yan etki yok)
# Her adım: kuruluysa atla → kur → doğrula → hata ise yalnız o aracı geri al + logla → sonrakine geç.
# MCP env'i ${AD} başvurusudur (değer yazılmaz). Anahtarsız sağlık düşerse "ANAHTAR-BEKLER", geri ALINMAZ.
set -euo pipefail
export MSYS_NO_PATHCONV=1

KOK="$(cd "$(dirname "$0")/.." && pwd)"
LOGD="$KOK/.kos/kurulum-3"; mkdir -p "$LOGD"
LOG="$LOGD/kurulum-turu-3.log"
GERI="$LOGD/geri-al.sh"
KLON="${KLON:-$KOK/.kos/kurulum-tarama/klon}"
SKD="$HOME/.claude/skills"
AGD="$HOME/.claude/agents"
PMD="$HOME/.claude/plugins/marketplaces"
APD="C:/Projeler/uygulamalar"
MOD="${1:-kur}"
TAMAM=0; HATA=0; BEKLE=0

log() { printf '%s\t%s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }
calis() { if [ "$MOD" = "--kuru" ]; then echo "+ $*"; else "$@"; fi; }
geri() { [ "$MOD" = "--kuru" ] || echo "$*" >> "$GERI"; }
mkonum() { cygpath -m "$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['installLocation'])" "$(cygpath -m "$HOME/.claude/plugins/known_marketplaces.json")" "$1")"; }

plugin_var() { grep -qF "$1" <<<"$(claude plugin list 2>&1)"; }
market_var() { grep -qE "❯ $1\$" <<<"$(claude plugin marketplace list 2>&1)"; }
mcp_var() { grep -qF "$1:" <<<"$(claude mcp list 2>&1)"; }
mcp_saglik() { grep -F "$1:" <<<"$(claude mcp list 2>&1)" | grep -q "Connected"; }
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

# S|repo|sha   → SKILL.md klasörleri ~/.claude/skills/<ad>
kur_skill() {
  local repo=$1 sha=$2 f s ad h
  klonla "$repo" "$sha" || return 1
  [ "$MOD" = "--kuru" ] && { echo "+ kopya $repo SKILL.md klasörleri → $SKD/"; return 0; }
  while IFS= read -r f; do
    s=$(dirname "$f"); ad=$(basename "$s"); [ "$s" = "$KD" ] && ad=${repo#*/}
    if [ -e "$SKD/$ad" ]; then log "ATLA/CAKISMA skill $ad ($repo)"; continue; fi
    h=$(supheli "$s"); [ -n "$h" ] && { log "SUPHELI-ATLA skill $ad: $h"; continue; }
    cp -r "$s" "$SKD/$ad" && rm -rf "$SKD/$ad/.git"
    [ -f "$SKD/$ad/SKILL.md" ] || { rm -rf "${SKD:?}/$ad"; log "HATA kopya $ad"; return 1; }
    geri "rm -rf \"$SKD/$ad\"  # $repo"
  done < <(find "$KD" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/.git/*')
  log "OK skill-kopya $repo"
}

# A|repo|sha|bölümler   → yalnız o üst klasörlerdeki *.md ajan dosyaları ~/.claude/agents/
kur_agents() {
  local repo=$1 sha=$2 dirs=$3 d f ad n=0
  klonla "$repo" "$sha" || return 1
  [ "$MOD" = "--kuru" ] && { echo "+ kopya $repo/{${dirs// /,}}/*.md → $AGD/"; return 0; }
  mkdir -p "$AGD"
  for d in $dirs; do
    while IFS= read -r f; do
      ad=$(basename "$f")
      [ -e "$AGD/$ad" ] && { log "ATLA/CAKISMA agent $ad"; continue; }
      grep -q '^name:' "$f" || continue
      cp "$f" "$AGD/$ad"; geri "rm -f \"$AGD/$ad\"  # $repo"; n=$((n+1))
    done < <(find "$KD/$d" -maxdepth 2 -name '*.md' -not -iname 'README*' 2>/dev/null)
  done
  if [ "$n" -gt 0 ]; then log "OK agents $repo ($n dosya)"; else log "HATA agents $repo 0 dosya"; return 1; fi
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

# I|ad@market   (tanımlı resmi marketten tek plugin)
kur_id() {
  plugin_var "$1" && { log "ATLA plugin $1"; return 0; }
  calis claude plugin install -y --scope user "$1" </dev/null || return 1
  [ "$MOD" = "--kuru" ] || plugin_var "$1" || return 1
  geri "claude plugin uninstall $1"; log "OK plugin $1"
}

# N|paket@sürüm|bayrak
kur_npm() {
  local spec=$1 bayrak=${2:-} ad=${1%@*}
  if npm ls -g --depth=0 "$ad" >/dev/null 2>&1; then log "ATLA npm $ad"; return 0; fi
  # shellcheck disable=SC2086
  calis npm i -g "$spec" $bayrak || return 1
  [ "$MOD" = "--kuru" ] || npm ls -g --depth=0 "$ad" >/dev/null 2>&1 || { npm uninstall -g "$ad" || true; return 1; }
  geri "npm uninstall -g $ad"; log "OK npm $spec"
}

# U|spec|ad
kur_uv() {
  local spec=$1 ad=$2
  if grep -qE "^$ad " <<<"$(uv tool list 2>/dev/null)"; then log "ATLA uv $ad"; return 0; fi
  calis uv tool install "$spec" || return 1
  [ "$MOD" = "--kuru" ] || grep -qE "^$ad " <<<"$(uv tool list 2>/dev/null)" || { uv tool uninstall "$ad" || true; return 1; }
  geri "uv tool uninstall $ad"; log "OK uv $spec"
}

# M|ad|ENV listesi|komut   ENV: ADI → -e ADI=${ADI}; ADI=değer → olduğu gibi (değer yine ${AD} başvurusu ya da anahtar olmayan sabit)
kur_mcp() {
  local ad=$1 es=$2 cmdline=$3 e a=() C E
  mcp_var "$ad" && { log "ATLA mcp $ad"; return 0; }
  IFS=, read -ra E <<<"$es"
  for e in "${E[@]}"; do [ -z "$e" ] && continue; if [[ $e == *=* ]]; then a+=(-e "$e"); else a+=(-e "$e=\${$e}"); fi; done
  read -ra C <<<"$cmdline"
  calis claude mcp add --scope user "$ad" "${a[@]}" -- "${C[@]}" || return 1
  geri "claude mcp remove --scope user $ad"
  [ "$MOD" = "--kuru" ] && return 0
  if mcp_saglik "$ad"; then log "OK mcp $ad"; else log "ANAHTAR-BEKLER mcp $ad"; BEKLE=$((BEKLE+1)); fi
}

# H|ad|url   (uzak http MCP, OAuth)
kur_http() {
  mcp_var "$1" && { log "ATLA mcp $1"; return 0; }
  calis claude mcp add --scope user --transport http "$1" "$2" || return 1
  geri "claude mcp remove --scope user $1"
  [ "$MOD" = "--kuru" ] && return 0
  if mcp_saglik "$1"; then log "OK mcp $1"; else log "ANAHTAR-BEKLER mcp $1 (OAuth)"; BEKLE=$((BEKLE+1)); fi
}

# K|ad|repo|sha|tür   → C:\Projeler\uygulamalar\<ad> (global değil). tür: klon | py-req | py-pyproject | node
kur_app() {
  local n=$1 repo=$2 sha=$3 kind=$4 d="$APD/$1" arg
  sha_ok "$sha" || { log "HATA sha-gecersiz $repo"; return 1; }
  [ -d "$d/.git" ] && { log "ATLA app $n"; return 0; }
  calis mkdir -p "$(dirname "$d")"
  calis git clone -q --filter=blob:none --no-checkout "https://github.com/$repo" "$d" || return 1
  calis git -C "$d" checkout -q "$sha" || { [ "$MOD" = "--kuru" ] || rm -rf "$d"; return 1; }
  [ "$MOD" = "--kuru" ] && { echo "+ ($kind) venv/bağımlılık $d"; return 0; }
  geri "rm -rf \"$d\""
  case $kind in
    py-req|py-pyproject)
      arg="-e ."; [ "$kind" = "py-req" ] && arg="-r requirements.txt"
      # shellcheck disable=SC2086
      (cd "$d" && uv venv -q .venv && timeout 900 uv pip install -q --python .venv/Scripts/python.exe $arg) || log "DEP-BEKLER $n (klon+venv tamam, bağımlılık elle)" ;;
    node)
      (cd "$d" && { timeout 600 npm ci --ignore-scripts || timeout 600 npm install --ignore-scripts; }) || log "DEP-BEKLER $n" ;;
  esac
  log "OK app $n"
}

VERI=$(cat <<'EOF'
# E
E|TESTSPRITE_NO_UPDATE_NOTIFIER|1
# S: skill kopyası (tur-3 KUR + KUR-duzeltmeli)
S|get-convex/agent-skills|2cfe645c87f971242cfc8ef3eb53662cbec26a53
S|penglonghuang/chinese-novelist-skill|6a64a04651036aa519c6354a93d6e01d68a9c22a
S|supabase/agent-skills|c9be0e931b7930f7d02126d04774d904c381e7d7
S|tt-a1i/archify|7f483b61e8f68d0d5c3219d2c943c5381c8db0b1
S|anthropics/claude-code-playground|569c5283d9a0a7ee7938df85bb32e4f48cbb8c86
S|jev-chat/jev-chat-jarvis|fdf8d28c811b0b67016d815df674cc61603c33c8
# A: agency-agents yalnız engineering/design/security
A|msitarzewski/agency-agents|f99f6aa910a442b0197b768ce0ea7751e35e2060|engineering design security
# P: plugin marketplace
P|AgriciDaniel/claude-ads|ac21644933910419529bcf81efb95a9ca71edf81|ai-marketing-hub-claude-ads
P|microsoft/azure-skills|0727d81638d64b6888f796287ee00baecfb08ced|azure-skills
P|AgriciDaniel/banana-claude|6a2b1b51fdcc35932184f06e513646a6f6f4f7d8|banana-claude-marketplace
P|openai/codex-plugin-cc|db52e28f4d9ded852ab3942cea316258ae4ef346|openai-codex
I|adobe-for-creativity@claude-plugins-official
# N: npm (tdd-guard: yalnız CLI, hook bağlanmaz = kapalı/opt-in; agent-browser: Playwright MCP ile örtüşür, tarayıcı indirme betiği çalıştırılmaz)
N|tdd-guard@1.7.0|--ignore-scripts
N|agent-browser@0.39.0|--ignore-scripts
N|@alibaba-group/open-code-review@1.12.13|--ignore-scripts
N|netlify-cli@27.12.0|--ignore-scripts
N|vercel@63.1.2|--ignore-scripts
N|@testsprite/testsprite-cli@0.14.0|--ignore-scripts
# U: uv
U|mcp-clickhouse==0.7.0|mcp-clickhouse
# M: MCP (env ${AD} başvurusu)
M|airtable|AIRTABLE_API_KEY|cmd /c npx -y airtable-mcp-server@1.14.0
M|netlify|NETLIFY_PERSONAL_ACCESS_TOKEN=${NETLIFY_AUTH_TOKEN}|cmd /c npx -y @netlify/mcp@1.18.0
M|apify|APIFY_TOKEN|cmd /c npx -y @apify/actors-mcp-server@0.17.4
M|n8n-mcp|N8N_API_KEY,N8N_API_URL,MCP_MODE=stdio|cmd /c npx -y n8n-mcp@2.92.1
M|hostinger|API_TOKEN=${HOSTINGER_API_TOKEN}|cmd /c npx -y hostinger-api-mcp@2.11.0
M|clickhouse|CLICKHOUSE_HOST,CLICKHOUSE_USER,CLICKHOUSE_PASSWORD|mcp-clickhouse
M|auth0||cmd /c npx -y @auth0/auth0-mcp-server@0.1.0-beta.19 run
H|canva|https://mcp.canva.com/mcp
# K: kendi ortamında uygulamalar (function-hook mod'ları yalnız klon = KAPALI; CLAUDE_CODE_ENABLE_FUNCTION_HOOKS açılmaz)
K|fn-hook-mods/claude-toons|achimala/claude-toons|0fac2edc29d06493597d486cae3799441ecef7d8|klon
K|fn-hook-mods/davekiss-env|davekiss/env|609ff7a2be08c880e3a47e3edaface8a7aa95362|klon
K|fn-hook-mods/cache-tax|karanb192/cache-tax|06cac47ec125a41a4aeeb78a6b006bec8cc6d6ed|klon
K|mcp-gsc|aminforou/mcp-gsc|d49eea9e5efb5eb645b722249303179b2c150b49|py-req
K|colibri|justvugg/colibri|bf2442915d6e3dd4cdfd2eb9c2a3d2aa44a25850|py-pyproject
K|thinking-orbs|jakubantalik/thinking-orbs|de85557ca220332586d070d8788c0e1d6e877a0d|node
K|omnivoice|k2-fsa/omnivoice|08be0b4ccbac3e13e374e86fbfead4b4cac343e2|py-pyproject
K|openmontage|calesthio/openmontage|9327439db69021ab4b0e2776729bf3b58fdb5a87|py-req
M|gsc|GSC_OAUTH_CLIENT_SECRETS_FILE|C:/Projeler/uygulamalar/mcp-gsc/.venv/Scripts/python.exe C:/Projeler/uygulamalar/mcp-gsc/gsc_server.py
EOF
)

log "=== kurulum-turu-3 basla ($MOD) ==="
while IFS='|' read -r tur a b c d; do
  [ -z "$tur" ] || [ "${tur:0:1}" = "#" ] && continue
  case $tur in
    E) f=(calis setx.exe "$a" "$b") ;;
    S) f=(kur_skill "$a" "$b") ;;
    A) f=(kur_agents "$a" "$b" "$c") ;;
    P) f=(kur_plugin "$a" "$b" "$c") ;;
    I) f=(kur_id "$a") ;;
    N) f=(kur_npm "$a" "$b") ;;
    U) f=(kur_uv "$a" "$b") ;;
    M) f=(kur_mcp "$a" "$b" "$c") ;;
    H) f=(kur_http "$a" "$b") ;;
    K) f=(kur_app "$a" "$b" "$c" "$d") ;;
    *) log "BILINMEYEN $tur"; continue ;;
  esac
  if "${f[@]}"; then TAMAM=$((TAMAM+1)); else HATA=$((HATA+1)); log "ATLANDI-HATA $tur $a"; fi
done <<<"$VERI"

if [ "$MOD" != "--kuru" ]; then
  log "--- son doğrulama ---"
  claude plugin list >> "$LOG" 2>&1 || true
  claude mcp list >> "$LOG" 2>&1 || true
fi
log "=== bitti: adım-ok $TAMAM · anahtar-bekler $BEKLE · hata $HATA · geri-al: $GERI ==="
