"""IG-41-KUR d4: envanter.json dar yenileme — tam yenileme ~1691 Jev isteği (1842 yeni araç) ister, tavan 10.
Yalnız ekler/günceller: HEAD envanterindeki araçlar + RED-kurulu kıyasının 3 farkı sınıflanır (hash değişenler yeniden sorulur);
şu an aktif görünmeyen HEAD satırları düşürülmez (yeniden adlandırmalar ve kabukta PATH'te olmayan elle CLI'lar tam yenilemeye kalır).
Kullanım (tools/video'da): VIDEO_UYGULA_KOK=<wt> uv run python ../../.claude/igkur41/envanter_dar.py"""
import json, os, subprocess, sys
from pathlib import Path
import video.departman as dp
from video.cli import calistir

HEDEF = {("plugin", "agent-browser"), ("plugin", "marketing-skills"), ("mcp", "markitdown")}
kok = Path(os.environ["VIDEO_UYGULA_KOK"])
bas = json.loads(subprocess.run(["git", "show", "HEAD:docs/departmanlar/envanter.json"], capture_output=True, cwd=kok, check=True).stdout)
var = {(x["tur"], x["ad"]) for x in bas}
asil_topla, asil_sinifla = dp.topla, dp.siniflandir
dp.topla = lambda ev, k: [a for a in asil_topla(ev, k) if (a["tur"], a["ad"]) in var | HEDEF]


def sinifla(*a, **k):
    e = asil_sinifla(*a, **k)
    olan = {(x["tur"], x["ad"]) for x in e}
    return e + [x for x in bas if (x["tur"], x["ad"]) not in olan]


dp.siniflandir = sinifla
sys.argv = ["video", "departman", "--istek-tavan", "10"]
sys.exit(calistir())
