import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ters"))
import kapi_kos as K  # noqa: E402

HEDEFLER = json.loads((K.DIZ / "hedefler.json").read_text(encoding="utf-8"))["hedefler"]


def test_dotnet_kayitlarinda_derlenmis_var():
    dn = [h for h in HEDEFLER if h["tur"] == "dotnet"]
    assert dn and all(Path(h["derlenmis"]).exists() for h in dn)


def test_bir_hedefin_hatasi_kosuyu_cokertmez(tmp_path, monkeypatch):
    H = [{"id": 1, "ad": "bozuk", "tur": "dotnet"}, {"id": 2, "ad": "iyi", "tur": "js"}]
    (tmp_path / "hedefler.json").write_text(json.dumps({"hedefler": H}), encoding="utf-8")
    (tmp_path / "t").mkdir()
    (tmp_path / "t" / "sayac.json").write_text('{"n": 0}')
    monkeypatch.setattr(K, "DIZ", tmp_path); monkeypatch.setattr(K, "CIKTI", tmp_path / "t"); monkeypatch.setattr(K, "sunucu", lambda: 0)

    def sahte(h, port, sat, atlanan):
        if h["ad"] == "bozuk": raise KeyError("derlenmis")
        for kol in ("skill", "zemin"): sat.append({"id": 2, "ad": "iyi", "tur": "js", "kol": kol, "c1": 1, "c2": 1, "c3": None, "puan": 1, "iddia": 5})
    monkeypatch.setattr(K, "hedef_kos", sahte)
    K.main()
    r = json.loads((tmp_path / "sonuc.json").read_text(encoding="utf-8"))
    assert r["hatalar"][0]["ad"] == "bozuk" and r["atlanan"] == ["bozuk"] and not r["gecti"] and len(r["satirlar"]) == 2
