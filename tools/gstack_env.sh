# gstack-core/bin/gstack-env -- source edilir, idempotent, sessiz.
# claude.ai kullanici skill dosyalarini 644 yazar ve kabuk durumu bash cagrilari
# arasinda korunmaz: her blok bu dosyayi source eder, ilk cagri +x'li bir ayna kurar.
GS_RO="${GSTACK_CORE_RO:-$(ls -d /mnt/skills/*/gstack-core 2>/dev/null | head -1)}"
GS="$HOME/.gstack/core"
if [ ! -x "$GS/bin/browse" ] && [ -n "$GS_RO" ]; then
  mkdir -p "$GS" 2>/dev/null
  cp -r "$GS_RO/." "$GS/" 2>/dev/null
  chmod -R +x "$GS/bin" 2>/dev/null
fi
B="python3 $GS/bin/browse"
D=""
export GS B D
