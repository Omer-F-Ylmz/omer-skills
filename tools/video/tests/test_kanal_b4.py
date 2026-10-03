"""KANAL-1b B4: liste yeniden üretilirken dolu Ömer sütunu korunur (coz sonrası anahtar ad → channel_id değişse de)."""
import json
from pathlib import Path

from test_kanal_k1 import C1, C2, C3, _kur, _satir
from video.cli import main


def test_liste_omer_sutunu_korunur(tmp_path, monkeypatch):
    repo, env = _kur(tmp_path, monkeypatch)
    assert main(["kanal", "liste"], env=env) == 0
    yol = repo / "docs" / "video-tarama" / "kanallar.md"
    md = yol.read_text(encoding="utf-8")
    for ad in ("A Kanal", "C Kanal"):
        md = md.replace(_satir(md, ad), _satir(md, ad)[:-3] + " takip |")
    yol.write_text(md, encoding="utf-8")
    onb = Path(env["VIDEO_CACHE"])
    for v in (C1, C2, C3):
        y = onb / v / "meta.json"
        y.write_text(json.dumps(json.loads(y.read_text(encoding="utf-8")) | {"channel_id": "UCc", "channel_url": "u"}), encoding="utf-8")
    assert main(["kanal", "liste"], env=env) == 0
    md = yol.read_text(encoding="utf-8")
    assert _satir(md, "A Kanal").endswith("| takip | takip |")
    c = _satir(md, "C Kanal")
    assert "| UCc | u |" in c and c.endswith("| atla | takip |")
