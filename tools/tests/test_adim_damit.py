"""HER-ADIM-1 damıtıcı (tools/adim_damit.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adim_damit as ad  # noqa: E402


def _a(arac, sonuc="ok", jeton=0):
    return {"arac": arac, "sonuc": sonuc, "jeton": jeton}


def test_istatistik_uc_kalip():
    adimlar = [_a("Bash", "hata"), _a("Bash", "hata"), _a("Bash")] + [_a("Read", jeton=900)] * 5
    metin = " | ".join(k["kalip"] for k in ad.istatistik(adimlar))
    assert "Bash adımı %67 hata" in metin and "Read art arda" in metin and "En pahalı adım türü Read" in metin


def test_damit_not_yazar_ruflo_bir_kez(tmp_path, monkeypatch):
    monkeypatch.setattr(ad, "YAZILAN", tmp_path / "yazilan.txt")
    cagrilar = []
    def sahte(c):
        cagrilar.extend(c)
        return {i + 2: {"result": {}} for i in range(len(c))}
    kal = [{"kalip": f"kural {i}", "satir": i, "oturum": "abcdefghij"} for i in range(12)]
    kos = lambda: ad.damit(sahte, tmp_path / "v" / "n.md", adimlar=[], kaliplar=kal)
    assert kos() == (12, 12)
    assert kos() == (12, 0)
    assert len(cagrilar) == 12 and (tmp_path / "v" / "n.md").read_text(encoding="utf-8").count("\n- ") == 12
