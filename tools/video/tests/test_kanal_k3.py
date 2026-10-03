"""KANAL-1 K3: değerli etiketi — iki kayıt · parti aday→video eşlemesi · -gelistirme · iptal parti · tekil · altyazı önbelleği."""
import json

from test_kanal_k1 import _jsonl
from video import kanal
from video.cli import main

V = [f"VVVVVVVVVV{i}" for i in range(6)]


def test_etiket_degerli_kurali(tmp_path, monkeypatch, capsys):
    repo, onb = tmp_path / "repo", tmp_path / "onb"
    monkeypatch.setattr(kanal, "KOK", repo)
    rd = repo / "docs" / "video-tarama"
    rd.mkdir(parents=True)
    for v in V:
        (rd / f"2026-09-30-{v}.md").write_text("# x\n## İddialar\n", encoding="utf-8")
    for p, adaylar in (("P1", {"x": [V[1]], "y": [V[2]]}), ("2026-10-01-uzun", {"z": [V[3]]})):
        (repo / ".kos" / p).mkdir(parents=True)
        (repo / ".kos" / p / "durum.json").write_text(json.dumps({"adaylar": {k: {"videolar": {v: {} for v in vs}} for k, vs in adaylar.items()}}), encoding="utf-8")
    _jsonl(rd / "kayit.jsonl", [{"id": v, "tarih": "2026-09-30", "adaylar": []} for v in V])
    _jsonl(repo / "docs" / "kurulumlar" / "kayit.jsonl", [
        {"ad": "d", "karar": "deneme: docs/denemeler/d.md", "yargi": "DENE", "tarih": "2026-09-24", "video": V[0]},
        {"ad": "x", "karar": "AL (Ömer, panel)", "tarih": "2026-09-30", "parti": "P1"},
        {"ad": "x", "karar": "AL (Ömer, panel)", "tarih": "2026-09-30", "parti": "P1"},
        {"ad": "y-gelistirme", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-09-30", "parti": "P1"},
        {"ad": "z", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-10-01", "parti": "2026-10-01-uzun"},
        {"ad": "r", "karar": "RED (Ömer, panel)", "tarih": "2026-09-30", "video": V[4]},
        {"ad": "o", "karar": "ÖĞREN (Ömer, panel)", "tarih": "2026-09-30", "video": V[5]},
    ])
    (onb / V[0]).mkdir(parents=True)
    (onb / V[0] / "altyazi.en.vtt").write_text("WEBVTT", encoding="utf-8")
    assert main(["kanal", "etiket"], env={"VIDEO_CACHE": str(onb)}) == 0
    j = json.loads((repo / "docs" / "olcumler" / "kanal-etiket.json").read_text(encoding="utf-8"))
    et = {x["id"]: x for x in j["videolar"]}
    assert len(j["videolar"]) == 6
    assert [et[v]["degerli"] for v in V] == [True, True, True, False, False, False]
    assert et[V[1]]["kaynak"] == ["AL:x@P1"] and et[V[2]]["kaynak"] == ["UYARLA:y-gelistirme@P1"]
    assert et[V[0]]["kaynak"] == ["DENE:d"] and et[V[0]]["altyazi"] is True and et[V[1]]["altyazi"] is False
    assert {k: j["ozet"][k] for k in ("toplam", "degerli", "degersiz", "altyazi_onbellekte")} == {"toplam": 6, "degerli": 3, "degersiz": 3, "altyazi_onbellekte": 1}
    assert "değerli 3" in capsys.readouterr().out
