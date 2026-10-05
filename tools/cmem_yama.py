"""TOKEN-2: claude-mem worker yaması — tek atımlık compress çağrısı (runStandaloneObserverPrompt, maxTurns:1) önbelleksiz.
Neden: bu çağrıda sistem istemi boş, yük her seferinde benzersiz → abonelikte CLI varsayılanı 1h yazma (2×) hiç okunmuyor
(14 günde 678 istek, 46.2 M ağırlıklı). DISABLE_PROMPT_CACHING ile girdi 1×. Ana observer oturumuna dokunulmaz.
settings.json'daki promptCacheTtl'e dokunulmaz (alt süreç settingSources:[] ile onu zaten yüklemiyor).
Idempotent: yamasız → yedek + uygular + node --check (kırıksa geri alır, DUR) | yamalı → dokunmaz | çapa 0/>1 → DUR.
claude-mem güncellenince yeni sürüm dizini yamasız gelir: betiği yeniden koş (token_olc UYARI verir).

Kullanım:
  python tools/cmem_yama.py            # en yeni sürüme uygula
  python tools/cmem_yama.py --kontrol  # yalnız durum
  python tools/cmem_yama.py --geri     # yedekten bayt-eşit geri al
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path.home() / ".claude" / "plugins" / "cache" / "thedotmack" / "claude-mem"
EK = 'DISABLE_PROMPT_CACHING:"1"'
# ...vg({source:"Observer",…,env:i,…}),maxTurns:1} — minified adlar sürümle değişir, yapı aynı kalır
CAPA = re.compile(r'(\.\.\.[\w$]+\(\{source:"Observer",[^{}]*?env:)([\w$]+)(,[^{}]*\}\),maxTurns:1\})')
YAMALI = re.compile(r'\.\.\.[\w$]+\(\{source:"Observer",[^{}]*?env:\{\.\.\.[\w$]+,' + re.escape(EK) + r'\},[^{}]*\}\),maxTurns:1\}')


def bul(kok=KOK):
    s = sorted(Path(kok).glob("*/scripts/worker-service.cjs"),
               key=lambda p: [int(x) for x in re.findall(r"\d+", p.parts[-3])])
    if not s:
        raise SystemExit(f"DUR: {kok} altında worker-service.cjs yok")
    return s[-1]


def durum(metin):
    c, y = len(CAPA.findall(metin)), len(YAMALI.findall(metin))
    return {(1, 0): "yamasız", (0, 1): "yamalı"}.get((c, y), f"çapa {c} + yamalı {y}")


def node_check(yol):
    return subprocess.run(["node", "--check", str(yol)], capture_output=True).returncode == 0


def _yedek(yol):
    return yol.with_name(yol.name + ".token2-yedek")


def uygula(yol, denetle=None):
    b = yol.read_bytes()
    d = durum(b.decode("utf-8"))
    if d == "yamalı":
        return "yamalı: dokunulmadı"
    if d != "yamasız":
        raise SystemExit(f"DUR: {d} (beklenen tek çapa) — {yol}")
    shutil.copy2(yol, _yedek(yol))
    yol.write_bytes(CAPA.sub(lambda m: f"{m[1]}{{...{m[2]},{EK}}}{m[3]}", b.decode("utf-8")).encode("utf-8"))
    if not (denetle or node_check)(yol):
        yol.write_bytes(b)
        raise SystemExit(f"DUR: node --check kırık → geri alındı — {yol}")
    return "uygulandı"


def geri(yol):
    if durum(yol.read_bytes().decode("utf-8")) == "yamasız":
        return "zaten yamasız: dokunulmadı"
    if not _yedek(yol).exists():
        raise SystemExit(f"DUR: yedek yok — {_yedek(yol)}")
    shutil.copy2(_yedek(yol), yol)
    return "geri alındı"


def main(a=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--dosya", type=Path)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--kontrol", action="store_true")
    g.add_argument("--geri", action="store_true")
    x = p.parse_args(a)
    yol = x.dosya or bul()
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{yol}: {durum(yol.read_bytes().decode('utf-8')) if x.kontrol else geri(yol) if x.geri else uygula(yol)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
