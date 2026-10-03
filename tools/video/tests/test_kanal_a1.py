"""KANAL-2a A1: yalnız tarihsiz (eski hat) raporu olup kararı olmayan video → 'etiketsiz (eski hat)'; kararlı olan değerli kalır."""
import json

from test_kanal_k1 import _kur
from video.cli import main

E1, E2 = "EEEEEEEEEE1", "EEEEEEEEEE2"


def test_eski_hat_etiketsiz(tmp_path, monkeypatch):
    repo, env = _kur(tmp_path, monkeypatch)
    rd, onb = repo / "docs" / "video-tarama", tmp_path / "onb"
    for v in (E1, E2):
        (rd / f"{v}.md").write_text("# eski hat\n", encoding="utf-8")
        (onb / v).mkdir(parents=True)
        (onb / v / "meta.json").write_text(json.dumps({"id": v, "channel": "E Kanal", "channel_id": "UCe"}), encoding="utf-8")
    ky = repo / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.write_text(ky.read_text(encoding="utf-8") + "\n" + json.dumps({"ad": "e2", "karar": "AL (Ömer)", "video": E2}), encoding="utf-8")
    assert main(["kanal", "etiket"], env=env) == 0
    j = json.loads((repo / "docs" / "olcumler" / "kanal-etiket.json").read_text(encoding="utf-8"))
    sinif = {x["id"]: x["sinif"] for x in j["videolar"]}
    assert sinif[E1] == "etiketsiz (eski hat)" and sinif[E2] == "değerli" and sinif["CCCCCCCCCC1"] == "değersiz"
    assert (j["ozet"]["degerli"], j["ozet"]["degersiz"], j["ozet"]["etiketsiz"]) == (4, 3, 1)
    assert main(["kanal", "liste"], env=env) == 0
    md = (rd / "kanallar.md").read_text(encoding="utf-8")
    assert "| 2 (eski 1) | 1 |" in next(x for x in md.splitlines() if x.startswith("| E Kanal "))
