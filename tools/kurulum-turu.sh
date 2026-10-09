#!/usr/bin/env bash
# Kurulum turu 2 — A grubu (etkileşimsiz) kurulumları sırayla kurar.
# Tarif: docs/kurulumlar/kurulum-sirasi.md. Pinler aşağıdaki VERI bloğunda.
# Kullanım: bash tools/kurulum-turu.sh            # kur
#           bash tools/kurulum-turu.sh --kuru     # yalnız komutları yazdır
#           bash tools/kurulum-turu.sh --blok     # skillOverrides bloğunu yazdır (settings.json'a dokunmaz)
# Her adım: zaten kuruluysa atla → kur → doğrula → hata ise geri al + logla + sonrakine geç.
set -euo pipefail
export MSYS_NO_PATHCONV=1

KOK="$(cd "$(dirname "$0")/.." && pwd)"
LOGD="$KOK/.kos/kurulum-2"; mkdir -p "$LOGD"
LOG="$LOGD/kurulum-turu.log"
GERI="$LOGD/geri-al.sh"          # başarılı her kurulumun uninstall komutu buraya eklenir
KLON="${KLON:-$KOK/.kos/kurulum-tarama/klon}"   # tur-1 klonları (pinli SHA'da); yoksa klonlanır
SKD="$HOME/.claude/skills"
PMD="$HOME/.claude/plugins/marketplaces"
MOD="${1:-kur}"
TAMAM=0; HATA=0

log() { printf '%s\t%s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }
calis() { if [ "$MOD" = "--kuru" ]; then echo "+ $*"; else "$@"; fi; }
geri() { echo "$*" >> "$GERI"; }

# --- doğrulayıcılar (pipefail + grep -q SIGPIPE tuzağına düşmemek için here-string) ---
plugin_var() { grep -qF "$1" <<<"$(claude plugin list 2>&1)"; }
market_var() { grep -qE "❯ $1\$" <<<"$(claude plugin marketplace list 2>&1)"; }
mcp_saglik() { grep -F "$1:" <<<"$(claude mcp list 2>&1)" | grep -q "Connected"; }

# P|owner/repo|sha|market-adi   → marketplace'teki TÜM plugin'ler kurulur
kur_plugin() {
  local repo=$1 sha=$2 m=$3 eklendi=0 p
  if ! market_var "$m"; then
    calis claude plugin marketplace add "$repo" || return 1
    eklendi=1; geri "claude plugin marketplace remove $m"
  fi
  [ "$MOD" = "--kuru" ] && { echo "+ git -C $PMD/$m checkout $sha; claude plugin install <hepsi>@$m"; return 0; }
  # pin: katalog klonunu SHA'ya sabitle, sonra kur
  git -C "$PMD/$m" fetch -q origin "$sha" 2>/dev/null || true
  git -C "$PMD/$m" checkout -q "$sha" || { log "PIN-HATA $m $sha"; return 1; }
  for p in $(python -I -c "import json,sys;print(' '.join(x['name'] for x in json.load(open(sys.argv[1],encoding='utf-8'))['plugins']))" "$PMD/$m/.claude-plugin/marketplace.json"); do
    if plugin_var "$p@$m"; then log "ATLA plugin $p@$m"; continue; fi
    claude plugin install -y --scope user "$p@$m" </dev/null || { log "HATA install $p@$m"; return 1; }
    plugin_var "$p@$m" || { log "HATA dogrula $p@$m"; claude plugin uninstall "$p@$m" || true; return 1; }
    geri "claude plugin uninstall $p@$m"; log "OK plugin $p@$m"
  done
}

# S|owner/repo|sha   → SKILL.md içeren her klasör ~/.claude/skills/<ad> olarak kopyalanır
kur_skill() {
  local repo=$1 sha=$2 d="$KLON/${1/\//__}" f s ad
  if [ "$(git -C "$d" rev-parse HEAD 2>/dev/null)" != "$sha" ]; then
    d="$LOGD/klon/${repo/\//__}"; rm -rf "$d"
    calis git clone -q --filter=blob:none --no-checkout "https://github.com/$repo" "$d" || return 1
    calis git -C "$d" checkout -q "$sha" || return 1
  fi
  [ "$MOD" = "--kuru" ] && { echo "+ kopya $repo SKILL.md klasörleri → $SKD/"; return 0; }
  while IFS= read -r f; do
    s=$(dirname "$f"); ad=$(basename "$s"); [ "$s" = "$d" ] && ad=${repo#*/}
    if [ -e "$SKD/$ad" ]; then log "ATLA/CAKISMA skill $ad ($repo)"; continue; fi
    cp -r "$s" "$SKD/$ad" && rm -rf "$SKD/$ad/.git"
    [ -f "$SKD/$ad/SKILL.md" ] || { rm -rf "${SKD:?}/$ad"; log "HATA kopya $ad"; return 1; }
    geri "rm -rf \"$SKD/$ad\"  # $repo"; echo "$repo	$ad" >> "$LOGD/skill-kopya.tsv"
  done < <(find "$d" -name SKILL.md -not -path '*/node_modules/*' -not -path '*/.git/*')
  log "OK skill-kopya $repo"
}

# N|paket@sürüm|ek-bayrak   (npm global)
kur_npm() {
  local spec=$1 bayrak=${2:-} ad=${1%@*}
  if npm ls -g --depth=0 "$ad" >/dev/null 2>&1; then log "ATLA npm $ad"; return 0; fi
  # shellcheck disable=SC2086
  calis npm i -g "$spec" $bayrak || return 1
  [ "$MOD" = "--kuru" ] || npm ls -g --depth=0 "$ad" >/dev/null 2>&1 || { npm uninstall -g "$ad" || true; return 1; }
  geri "npm uninstall -g $ad"; log "OK npm $spec"
}

# U|uv-spec|araç-adı
kur_uv() {
  local spec=$1 ad=$2
  if grep -qE "^$ad " <<<"$(uv tool list 2>/dev/null)"; then log "ATLA uv $ad"; return 0; fi
  calis uv tool install "$spec" || return 1
  [ "$MOD" = "--kuru" ] || grep -qE "^$ad " <<<"$(uv tool list 2>/dev/null)" || { uv tool uninstall "$ad" || true; return 1; }
  geri "uv tool uninstall $ad"; log "OK uv $spec"
}

# M|ad|komut...   (stdio MCP, user scope)
kur_mcp() {
  local ad=$1; shift
  if grep -qF "$ad:" <<<"$(claude mcp list 2>&1)"; then log "ATLA mcp $ad"; return 0; fi
  calis claude mcp add --scope user "$ad" -- "$@" || return 1
  [ "$MOD" = "--kuru" ] || mcp_saglik "$ad" || { log "HATA saglik mcp $ad"; claude mcp remove --scope user "$ad" || true; return 1; }
  geri "claude mcp remove --scope user $ad"; log "OK mcp $ad"
}

# E|AD|DEĞER   (telemetri kapatma; kurulumdan ÖNCE, kullanıcı ortamına setx)
kur_env() { calis setx.exe "$1" "$2" >/dev/null && log "OK env $1"; }

# --blok: dev paketlerin skill'leri için "user-invocable-only" bloğu (model listesinden çıkar, /çağrı ile yüklenir)
if [ "$MOD" = "--blok" ]; then
  python -I - "$HOME/.claude/plugins/cache" "$LOGD/skill-kopya.tsv" <<'PY'
import json, os, re, sys
cache, kopya = sys.argv[1], sys.argv[2]
DEV_MARKET = ["ecc", "open-design", "daymade-skills", "designer-skills", "marketingskills",
              "hyperframes", "android-skills", "mattpocock"]
DEV_KOPYA = ["mengto/skills"]
o = {}
for m in DEV_MARKET:
    for root, dirs, files in os.walk(os.path.join(cache, m)):
        if "SKILL.md" in files:
            plugin = os.path.relpath(root, os.path.join(cache, m)).split(os.sep)[0]
            t = open(os.path.join(root, "SKILL.md"), encoding="utf-8", errors="ignore").read(2000)
            n = re.search(r"^name:\s*['\"]?([^'\"\n]+)", t, re.M)
            o[f"{plugin}:{(n.group(1) if n else os.path.basename(root)).strip()}"] = "user-invocable-only"
if os.path.isfile(kopya):
    for ln in open(kopya, encoding="utf-8"):
        repo, ad = ln.rstrip("\n").split("\t")
        if repo in DEV_KOPYA:
            o[ad] = "user-invocable-only"
print(json.dumps({"skillOverrides": dict(sorted(o.items()))}, ensure_ascii=False, indent=2))
print(f"# {len(o)} skill", file=sys.stderr)
PY
  exit 0
fi

VERI=$(cat <<'EOF'
# E: telemetri kapatma (önce)
E|DO_NOT_TRACK|1
E|HYPERFRAMES_NO_TELEMETRY|1
E|CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS|1
E|CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS|1
E|OMNIVOICE_ANALYTICS_DISABLED|1
E|PHONE_HARNESS_TELEMETRY|0
E|ECC_HOOK_PROFILE|minimal
# P: plugin marketplace (TAM)
P|agentrhq/webcmd|9d8ea440fd3d86ddadf53e66b6f27db6134b0312|webcmd
P|codeswithroh/tastemaker|e39b4bf6586f303761dca996337e16a0354305b7|codeswithroh
P|conardli/garden-skills|aaf9a82f5efd73e87cc0998edc398e75bfc35901|garden-skills
P|dannymac180/fable-advisor|9df042b27f50a525d78844498597aa06817cda24|fable-advisor
P|data-goblin/claude-code-filetree|da1da65724c54541f4a0ec5ddd26641b1a0d672a|claude-code-filetree
P|dgreenheck/webgpu-claude-skill|af2319bd01bb7cc881267a9ef42cafdaf5e9029d|webgpu-threejs-tsl
P|greensock/gsap-skills|aed9cfd3277740755f6bfc1155c7aa645403b760|gsap-skills
P|jakeschincariol/linkedin-agent-skill|add2c23882fe79180737d242ff80a5da205eda6a|linkedin-agent-skill
P|jakubkrehel/skills|d574cc8a576dc24256ad38268b8d03d86724a1b3|interfaces
P|kepano/obsidian-skills|3ccff5338ea700537839b21900aa5358a0402c98|obsidian-skills
P|mattpocock/skills|49dd158d1076134a641b33efb035946536778336|mattpocock
P|nanako0129/sepia|d94121b59125cf42a9f7ce4a069a8beb7a401d61|sepia
P|nyldn/plugins|e3e5a26db35eea0322265fb9a50981214dc64fa2|nyldn-plugins
P|pablo-mano/obsidian-cli-skill|d7782314eadfa12483434fd0c28f8743fe24b060|obsidian-cli-skill
P|scasella/claude-flightdeck|f31daca523d36c501cd0df23a737a44c7dc56ad6|claude-flightdeck
P|sezaakgun/cc-arcade|0baff06d31295850283c2eebe052f39bbc35473f|cc-arcade
P|affaan-m/ecc|ef648e01899ba3e8dc6371642deaaf64b4477775|ecc
P|android/skills|42dc2270e96032bd860bb94511e440aa00a43125|android-skills
P|chromedevtools/chrome-devtools-mcp|f08dbe152502d66e75fa07fb2588dc0feb42bc20|chrome-devtools-plugins
P|coreyhaines31/marketingskills|1efedbc5148b54b2f0f6c6c9fe0be62e151c7fff|marketingskills
P|daymade/claude-code-skills|a9d357310d803b66c4a0d5a52c466dbb6661f396|daymade-skills
P|halluton/mindful-claude|411c9c4f4f1c3d128159be7315823341ae7d9e2d|mindful-claude
P|heygen-com/hyperframes|46f6cb356785bed79e1ce7b79d7e7accc697786a|hyperframes
P|kaankiziltug/logo-design-skill|0ecf52e9a4b3ac92b714f7cc6e3148ab8c774134|logo-design-skill
P|mksglu/context-mode|d573d8e1a0db87da3d72bbd7b5cdc88569f4c734|context-mode
P|mvanhorn/last30days-skill|a3b73fc5f3fb3a464d6dfb7660eec7ef1dc6d366|last30days-skill
P|nexu-io/open-design|802708f6c9f294347ef777b1fda49b9cbe26ef72|open-design
P|owl-listener/designer-skills|9a6930cf84a822eb458624bd11c61aac5bbdf224|designer-skills
# S: skill kopyası
S|behisecc/vibesec-skill|0590993b35ad51961f65a4d01cf1196dfead05bb
S|cloudflare/security-audit-skill|c1c8a8c1471069fb0e188eeaff69b8e8db6564a8
S|coleam00/excalidraw-diagram-skill|8646fcc9f74f38539c6cdb4c969723336a96ddcd
S|elayadesign/ai-design-skills|1c1e97cb9878e236552c772092dda7adcdddbcb2
S|emilkowalski/skills|e8a175de22ae1e49370fc144c1f3bb9aeedf988d
S|eyaprak/skills|ac16e8a7bbbd5bc2be00f2eeb279b933bab28d94
S|ggml-org/llama.cpp|6184e92c57dcd34de8a3e381d7641a5e75250d5f
S|hardikpandya/stop-slop|8da1f030185bdfe8471220585162991eaeb970e9
S|herdrdev/herdr|2563803dca97c040beaf3dc3acdcb5a3221b4238
S|ibelick/ui-skills|587ea305b948ad34f0c2d5c2ea4211d428f66ed8
S|jsmastery-pro/skills|43b69e44c9ca905fe3a3418ccdf4102255e20d40
S|lexmount/moli|fb8b9b7a8c5dca641680298a81bb0c73c516f6f8
S|magnitudedev/magnitude|b2f79f00f4aa8d4ca6ad97f37a8c457ddba4e8a9
S|mengto/skills|83a47fee32f0b6349bff1fede99257a5ef03dc93
S|nidhinjs/prompt-master|2bd92518e26bf659e21e3d9ab90573fcf3ddeccb
S|robonuggets/excalidraw-skill|86a9ff1d3f9266e558a3efad8e8f2b5c724140d8
S|thanhthuduc99/video-to-website|c303b6f1347821f8fc9907d0fd36ae9897cbb565
S|auriti-labs/geo-optimizer-skill|0e1ffc88aa2300c81a4596283c061df8bb0c5f56
S|d4vinci/scrapling|aa814a77d942678f1a44f68198a0c88550382d28
S|leonxlnx/unlazy|16671491f6679ad9378f52604d3bc2415b4120c7
S|remotion-dev/skills|32b241b97f4e0e4ab61fe9a41b05e6e64503f8c5
S|poyrazavsever/life-kernel|b2f7e4efcf5bef3c715457f476b7305815038f71
S|debpalash/voicestudio|06c6e077f0fc35149efefc3561e9be5ae835d916
# N: npm
N|rea-agents@6.1.0|--ignore-scripts
N|codeburn@0.9.25|
# U: uv
U|markitdown[all]==0.1.8|markitdown
U|phone-harness==0.3.0|phone-harness
U|mimic-client==0.1.0|mimic-client
U|droidasc==0.1.1.post3|droidasc
U|git+https://github.com/phuryn/claude-usage@3eea154474e93761f774ed38beeaf45baf838a45|claude-usage
# M: MCP (stdio)
M|drizzle-docs|cmd /c npx -y drizzle-docs-mcp@3.0.2
M|godot|cmd /c npx -y @coding-solo/godot-mcp@0.1.1
M|unity|cmd /c npx -y anklebreaker-unity-mcp@2.36.0
EOF
)

log "=== kurulum-turu basla ($MOD) ==="
grep -qF "everything-claude-code@everything-claude-code" <<<"$(claude plugin list 2>&1)" \
  && log "UYARI eski everything-claude-code kurulu; ecc ile skill'ler çift sayılır (tarif B-0)"
while IFS='|' read -r tur a b c; do
  [ -z "$tur" ] || [ "${tur:0:1}" = "#" ] && continue
  case $tur in
    E) f=(kur_env "$a" "$b") ;;
    P) f=(kur_plugin "$a" "$b" "$c") ;;
    S) f=(kur_skill "$a" "$b") ;;
    N) f=(kur_npm "$a" "$b") ;;
    U) f=(kur_uv "$a" "$b") ;;
    M) read -ra arg <<<"$b"; f=(kur_mcp "$a" "${arg[@]}") ;;
    *) log "BILINMEYEN $tur"; continue ;;
  esac
  if "${f[@]}"; then TAMAM=$((TAMAM+1)); else HATA=$((HATA+1)); log "ATLANDI-HATA $tur $a"; fi
done <<<"$VERI"

if [ "$MOD" != "--kuru" ]; then
  log "--- son doğrulama ---"
  claude plugin list >> "$LOG" 2>&1 || true
  claude mcp list >> "$LOG" 2>&1 || true
  timeout 90 claude doctor </dev/null >> "$LOG" 2>&1 || log "UYARI claude doctor sıfır dışı/zaman aşımı"
fi
log "=== bitti: adım-ok $TAMAM · hata $HATA · geri-al: $GERI ==="
