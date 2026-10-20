import importlib.util, json
from pathlib import Path

_s = importlib.util.spec_from_file_location("karar2", Path(__file__).with_name("video764_karar2.py"))
K = importlib.util.module_from_spec(_s); _s.loader.exec_module(K)


def _veri(n):
    return {f"v{i}": dict(id=f"v{i}", url=f"u{i}", baslik=f"b\t{i}", sure="1:00", eski=["u", "b", "1:00", "ELE", "n"] if i else None, ozet="ö") for i in range(n)}


def test_yeniden_toplu_eski_korunur_ve_devam_eder(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "V2", tmp_path / "v2.tsv"); monkeypatch.setattr(K, "veri", lambda: _veri(5))
    cagrilar = []

    def sahte(istem):
        cagrilar.append(istem)
        ids = [s[len("## id="):].split(" ")[0] for s in istem.split("\n") if s.startswith("## id=")]
        return json.dumps([{"id": i, "karar": "ogren" if i != "v3" else "AL", "gerekce": "g", "kanit": "k"} for i in ids if i != "v4"])  # v4 yanıtta eksik

    K.yeniden(n=2, cagri=sahte)
    sat = K.V2.read_text(encoding="utf-8").splitlines()
    assert len(cagrilar) == 3 and len(sat) == 1 + 4  # başlık + v4 hariç 4
    assert sat[1].split("\t")[:5] == ["v0", "u0", "b 0", "", "ÖĞREN"] and sat[-1].split("\t")[7] == "[karar-v2]"
    K.yeniden(n=2, cagri=sahte)  # yalnız eksik v4 yeniden istenir, v2 satırları çoğalmaz
    assert len(cagrilar) == 4 and len(K.V2.read_text(encoding="utf-8").splitlines()) == 5


def test_melez_dusuk_ve_ele_tek_tek_tavan(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "V2", tmp_path / "v2.tsv"); monkeypatch.setattr(K, "veri", lambda: _veri(5))
    monkeypatch.setattr(K, "SAYAC", tmp_path / "sayac.json"); monkeypatch.setitem(K.TAVAN, "tek", 2)
    cagrilar = []

    def sahte(istem):
        cagrilar.append(istem)
        ids = [s[len("## id="):].split(" ")[0] for s in istem.split("\n") if s.startswith("## id=")]
        tek = len(ids) == 1
        return json.dumps([{"id": i, "karar": "UYARLA" if tek else {"v1": "ELE", "v2": "ÖĞREN", "v3": "ELE"}.get(i, "ÖĞREN"), "guven": "dusuk" if i == "v2" and not tek else "yuksek"} for i in ids])

    K.yeniden(n=5, cagri=sahte, melez=True)
    assert '"guven"' in cagrilar[0] and '"guven"' not in cagrilar[1]
    sat = {s.split("\t")[0]: s.split("\t") for s in K.V2.read_text(encoding="utf-8").splitlines()[1:]}
    assert [sat[i][8] for i in ("v0", "v1", "v2", "v3", "v4")] == ["toplu", "tek", "tek", "toplu-tavan", "toplu"]  # düşük önce, sonra ELE; tavan 2
    assert sat["v1"][4] == "UYARLA" and sat["v3"][4] == "ELE" and len(cagrilar) == 3
