"""ENVANTER-3: katalog_yenile ek.jsonl + plugin ajanları + artımlı öğrenim bekleyeni."""
import json
import os
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import katalog_yenile as ky  # noqa: E402


def test_ek_ve_plugin_ajanlari_katalogda():
    r = {(o["ad"], o["tur"]): o for o in map(json.loads, (KOK / "docs/katalog/yetenek.jsonl").read_text(encoding="utf8").splitlines())}
    for s in (KOK / "docs/katalog/ek.jsonl").read_text(encoding="utf8").splitlines():
        o = json.loads(s)
        assert r[(o["ad"], o["tur"])]["durum"] == o["durum"], o["ad"]
    assert ("differential-review:adversarial-modeler", "ajan") in r


def test_ogrenim_bekleyen_yalniz_yeni_ve_kaynaksiz(tmp_path, monkeypatch):
    (tmp_path / "docs/video-tarama").mkdir(parents=True)
    katalog = tmp_path / "docs/katalog"
    katalog.mkdir()
    eski, yeni, anilan = (tmp_path / "docs/video-tarama" / f"{a}.md" for a in ("eski", "yeni", "anilan"))
    for p in (eski, yeni, anilan):
        p.write_text("x")
    og = katalog / "ogrenim.jsonl"
    og.write_text(json.dumps({"kaynak": "docs/video-tarama/anilan.md:3"}) + "\n")
    t = og.stat().st_mtime
    os.utime(eski, (t - 10, t - 10))
    for p in (yeni, anilan):
        os.utime(p, (t + 10, t + 10))
    monkeypatch.setattr(ky, "KOK", tmp_path)
    monkeypatch.setattr(ky, "CIKTI", katalog)
    assert list(ky.ogrenim_bekleyen()) == ["docs/video-tarama/yeni.md"]
