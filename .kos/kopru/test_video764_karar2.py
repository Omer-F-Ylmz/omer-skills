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
