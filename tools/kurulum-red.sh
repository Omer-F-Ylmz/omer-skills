#!/usr/bin/env bash
# RED-KUR — RED-İNCELE-1/2 güvenli KUR-adayları: markitdown(+mcp), motion-os, universal-modder. Pinli.
# Kullanım: bash tools/kurulum-red.sh [--kuru]   (--kuru: yalnız komutları yazdır, yan etki yok)
# Her adım: kuruluysa atla → kur → doğrula → hata ise yalnız o aracı geri al + logla → sonrakine geç. Silme yok (kendi kopyası hariç).
set -euo pipefail
export MSYS_NO_PATHCONV=1

KOK="$(cd "$(dirname "$0")/.." && pwd)"
LOGD="$KOK/.kos/kurulum-red"; mkdir -p "$LOGD"
LOG="$LOGD/kurulum-red.log"
GERI="$LOGD/geri-al.sh"
SKD="$HOME/.claude/skills"
MOD="${1:-kur}"
TAMAM=0; HATA=0

MD_SUR=0.1.8          # PyPI markitdown (2026-10-10 doğrulandı)
MCP_SUR=0.0.1a7       # PyPI markitdown-mcp (en yeni; kararlı sürüm yok, alfa)
MO_SHA=15dc59eb33a1bca4de3436975078a65b9c8e2e95   # jasonlee-breadcrumb/motion-os
UM_SHA=550651675153070cce68066e07c3c8f95df86d08   # rehan-remade/universal-modder

log() { printf '%s\t%s\n' "$(date +%H:%M:%S)" "$*" | tee -a "$LOG"; }
calis() { if [ "$MOD" = "--kuru" ]; then echo "+ $*"; else "$@"; fi; }
geri() { [ "$MOD" = "--kuru" ] || echo "$*" >> "$GERI"; }
plugin_var() { grep -qF "$1" <<<"$(claude plugin list 2>&1)"; }
market_var() { grep -qE "❯ $1\$" <<<"$(claude plugin marketplace list 2>&1)"; }
mkonum() { cygpath -m "$(python -I -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['installLocation'])" "$(cygpath -m "$HOME/.claude/plugins/known_marketplaces.json")" "$1")"; }
supheli() { grep -rEIl 'curl[^|]*\|[ ]*(ba)?sh|Invoke-Expression|base64 (-d|--decode)[^|]*\|[ ]*(ba)?sh' "$1" 2>/dev/null | grep -v '\.md$' | head -3 || true; }

# 1) markitdown CLI + markitdown-mcp (uv tool, pinli) + MCP kaydı
kur_markitdown() {
  local t
  t=$(uv tool list 2>/dev/null || true)
  grep -q "^markitdown v" <<<"$t" || { calis uv tool install "markitdown[all]==$MD_SUR" || return 1; geri "uv tool uninstall markitdown"; }
  grep -q "^markitdown-mcp v" <<<"$t" || { calis uv tool install "markitdown-mcp==$MCP_SUR" || return 1; geri "uv tool uninstall markitdown-mcp"; }
  if ! grep -q "^markitdown:" <<<"$(claude mcp list 2>&1)"; then
    calis claude mcp add --scope user markitdown -- markitdown-mcp || return 1
    geri "claude mcp remove --scope user markitdown"
  fi
  [ "$MOD" = "--kuru" ] || { uv tool list | grep -E "^markitdown" | tee -a "$LOG"; log "OK markitdown $MD_SUR + mcp $MCP_SUR"; }
}

# 2) motion-os: repo kökü = skill; pinli klon → ~/.claude/skills/motion-os
kur_motionos() {
  local KD; KD="$(cygpath -m "$LOGD")/klon/motion-os"
  if [ -e "$SKD/motion-os" ]; then log "ATLA/CAKISMA skill motion-os"; return 0; fi
  [ "$MOD" = "--kuru" ] || rm -rf "$KD"
  calis git clone -q --filter=blob:none --no-checkout https://github.com/jasonlee-breadcrumb/motion-os "$KD" || return 1
  calis git -C "$KD" checkout -q "$MO_SHA" || return 1
  [ "$MOD" = "--kuru" ] && { echo "+ cp $KD → $SKD/motion-os"; return 0; }
  local h; h=$(supheli "$KD"); [ -n "$h" ] && { log "SUPHELI-ATLA motion-os: $h"; return 1; }
  cp -r "$KD" "$SKD/motion-os" && rm -rf "$SKD/motion-os/.git"
  [ -f "$SKD/motion-os/SKILL.md" ] || { rm -rf "${SKD:?}/motion-os"; log "HATA kopya motion-os"; return 1; }
  geri "rm -rf \"$SKD/motion-os\""; log "OK skill motion-os"
}

# 3) universal-modder: marketplace + plugin (pinli)
kur_modder() {
  local m=universal-modder ml
  if plugin_var "$m@$m"; then log "ATLA plugin $m@$m"; return 0; fi
  if ! market_var "$m"; then
    calis claude plugin marketplace add rehan-remade/universal-modder || return 1
    geri "claude plugin marketplace remove $m"
  fi
  [ "$MOD" = "--kuru" ] && { echo "+ git -C <market> checkout $UM_SHA; claude plugin install $m@$m"; return 0; }
  ml=$(mkonum "$m") || { log "PIN-HATA $m konum yok"; return 1; }
  git -C "$ml" fetch -q origin "$UM_SHA" 2>/dev/null || true
  git -C "$ml" checkout -q "$UM_SHA" || { log "PIN-HATA $m $UM_SHA"; return 1; }
  claude plugin install -y --scope user "$m@$m" </dev/null || { log "HATA install $m@$m"; return 1; }
  plugin_var "$m@$m" || { log "HATA dogrula $m@$m"; claude plugin uninstall "$m@$m" || true; return 1; }
  geri "claude plugin uninstall $m@$m"; log "OK plugin $m@$m"
}

log "=== kurulum-red basla ($MOD) ==="
for f in kur_markitdown kur_motionos kur_modder; do
  if "$f"; then TAMAM=$((TAMAM+1)); else HATA=$((HATA+1)); log "ATLANDI-HATA $f"; fi
done
log "=== bitti: adım-ok $TAMAM · hata $HATA · geri-al: $GERI ==="
