"""MOTOR-M8 K2: altyazısız video düşmez — kare-yalnız paket (kareler + başlık + açıklama + bağlantılar + not)."""
import json

from video import cli
from video import parti as pt


def _meta(kok, v, sure):
    d = kok / v
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps({"id": v, "title": "Başlık", "channel": "Kanal", "duration": sure,
                                             "description": "bak https://ornek.dev"}), encoding="utf-8")
    return d


def _sahte_kare(monkeypatch):
    monkeypatch.setattr(cli, "_kareler", lambda ctx, d, z, *a: [(t, d / f"k{i}.jpg") for i, t in enumerate(z)])
    monkeypatch.setattr(cli, "_kare_tk", lambda y: (0, 0))


def _paket(tmp_path, v, *ek):
    assert cli.main(["paket", v, "--kare", "3", "--istek-tavan", "0", *ek], env={"VIDEO_CACHE": str(tmp_path)}) == 0
    return pt.paket_oku(tmp_path / v / "paket.md")


def test_altyazisiz_kare_yalniz_paket(tmp_path, monkeypatch):
    _sahte_kare(monkeypatch)
    _meta(tmp_path, "9opJeH9j9qs", 57)
    p = _paket(tmp_path, "9opJeH9j9qs")
    assert p["kare_yalniz"] and len(p["kareler"]) == 3 and p["linkler"] == ["https://ornek.dev"]
    assert "altyazı yok: kare-yalnız" in p["metin"] and "Başlık" in p["metin"]


def test_anlamsiz_whisper_kare_yalniz(tmp_path, monkeypatch):
    _sahte_kare(monkeypatch)
    d = _meta(tmp_path, "9opJeH9j9qs", 57)
    (d / "segmentler.jsonl").write_text(json.dumps({"bas": 0, "son": 57, "metin": "[Music] ♪"}), encoding="utf-8")
    assert not pt._anlamli(d / "segmentler.jsonl") and not pt._anlamli(d / "yok.jsonl")
    p = _paket(tmp_path, "9opJeH9j9qs", "--kare-yalniz")
    assert p["kare_yalniz"] and "[Music]" not in p["metin"] and len(p["kareler"]) == 3
    (d / "s.jsonl").write_text(json.dumps({"bas": 0, "son": 5, "metin": "bu araç landing sayfası kuruyor"}), encoding="utf-8")
    assert pt._anlamli(d / "s.jsonl")


def test_kare_yalniz_rapor_notunda(tmp_path):
    from test_m2a import Sahte, _ctx, _kurulum, _ns
    _kurulum(tmp_path, ["aaaaaaaaaa1"])
    y = tmp_path / "c" / "aaaaaaaaaa1" / "paket.md"
    y.write_text(y.read_text(encoding="utf-8").replace("## Segmentler", "## Segmentler" + chr(10) + "altyazı yok: kare-yalnız"), encoding="utf-8")
    assert pt.paket_oku(y)["kare_yalniz"]
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _ctx(tmp_path, Sahte())) == 0
    raporlar = [r for r in tmp_path.rglob("*.md") if "aaaaaaaaaa1" in r.name and r.parent.name != "aaaaaaaaaa1"]
    assert raporlar and all("kare-yalnız" in r.read_text(encoding="utf-8") for r in raporlar), raporlar
