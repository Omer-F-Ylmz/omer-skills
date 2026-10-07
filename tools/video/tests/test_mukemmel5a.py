"""MÜKEMMEL-5a: bayat paket koruması — paket kapsam.json'a adım damgası yazar; damgasız ya da eksik adımlı paket parti yolunda
model çağrısı yapmadan yeniden kurulur, deftere "paket yenilendi (eksik: …)" satırı düşer (çağrı saymaz)."""
import json

from video import parti as pt
from test_m9 import _alt, _d


def _kur(onb, v, adimlar):
    (onb / v).mkdir(parents=True, exist_ok=True)
    (onb / v / "paket.md").write_text("# eski\n", encoding="utf-8")
    (onb / v / "kapsam.json").write_text(json.dumps({"izleme": "x", "incelenmedi": [], **({"adimlar": adimlar} if adimlar is not None else {})}),
                                         encoding="utf-8")


def _kos(tmp_path, adimlar):
    pd, onb = tmp_path / "pd", tmp_path / "onb"
    pd.mkdir()

    def pk(v):  # sahte paket kurucusu: tam damga yazar
        (onb / v / "paket.md").write_text("# yeni\n", encoding="utf-8")
        (onb / v / "kapsam.json").write_text(json.dumps({"izleme": "x", "incelenmedi": [], "adimlar": list(pt.PAKET_ADIMLARI)}), encoding="utf-8")
        return 0
    alt, cagri = _alt(onb, sure=600, paket=pk, whisper=RuntimeError("yok"))
    _kur(onb, "e1", adimlar)
    d = _d("e1")
    d["videolar"]["e1"]["tarama"]["durum"] = "tamam"  # yalnız paket aşaması
    pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
    return cagri, [x for x in pt.tr.kayit_oku(pd / "defter.jsonl")], pd, onb


def test_damga_tek_yerde_ocr_dahil():
    assert "ocr" in pt.PAKET_ADIMLARI and len(set(pt.PAKET_ADIMLARI)) == len(pt.PAKET_ADIMLARI)


def test_damgasiz_paket_yeniden_kurulur(tmp_path):
    cagri, defter, pd, onb = _kos(tmp_path, None)
    assert any(a[0] == "paket" for a in cagri) and not any(a[0] == "ozet" for a in cagri)
    assert (onb / "e1" / "paket.md").read_text(encoding="utf-8") == "# yeni\n"
    s = [x for x in defter if x.get("adim") == "paket_yenilendi"]
    assert len(s) == 1 and s[0]["not"] == f"paket yenilendi (eksik: {', '.join(pt.PAKET_ADIMLARI)})"
    assert pt._defter(pd)[0] == 0  # çağrı saymaz


def test_eksik_adimli_paket_yeniden_kurulur(tmp_path):
    _, defter, *_ = _kos(tmp_path, [a for a in pt.PAKET_ADIMLARI if a != "ocr"])
    assert [x["not"] for x in defter if x.get("adim") == "paket_yenilendi"] == ["paket yenilendi (eksik: ocr)"]


def test_tam_damgali_paket_dokunulmaz(tmp_path):
    cagri, defter, _, onb = _kos(tmp_path, list(pt.PAKET_ADIMLARI))
    assert not any(a[0] == "paket" for a in cagri) and not defter
    assert (onb / "e1" / "paket.md").read_text(encoding="utf-8") == "# eski\n"


def test_eksik_adim_olcer(tmp_path):
    (tmp_path / "kapsam.json").write_text(json.dumps({"adimlar": ["ocr"]}), encoding="utf-8")
    assert pt.eksik_adim(tmp_path) == [a for a in pt.PAKET_ADIMLARI if a != "ocr"]
    assert pt.eksik_adim(tmp_path / "yok") == list(pt.PAKET_ADIMLARI)
