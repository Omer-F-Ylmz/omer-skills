import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import akis_damit as A  # noqa: E402


def _jsonl(tmp_path, olaylar):
    p = tmp_path / "o.jsonl"
    p.write_text("\n".join(json.dumps(o) for o in olaylar), encoding="utf-8")
    return p


def _oturum(tmp_path):
    return _jsonl(tmp_path, [
        {"type": "user", "message": {"role": "user", "content": "Görev: testi düzelt"}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "id": "a", "name": "Bash", "input": {"command": "pytest -q"}}]}},
        {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "a", "is_error": True, "content": "1 failed"}]}},
        {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": "Kök neden bulundu, düzelttim. 12 passed."}]}},
    ])


def test_iz_arac_hata_ve_kapanisi_numarali_satir_yapar(tmp_path):
    iz = A.iz(_oturum(tmp_path))
    assert any("ARAC Bash" in s and "pytest -q" in s for s in iz)
    assert any("HATA" in s and "1 failed" in s for s in iz)
    assert iz[-1].startswith("L") and "12 passed" in iz[-1]


def test_dogrula_alinti_o_satirda_yoksa_atilir(tmp_path):
    iz = A.iz(_oturum(tmp_path))
    n = next(int(s.split()[0][1:]) for s in iz if "pytest -q" in s)
    assert A.dogrula({"kalip": "x", "satir": n, "alinti": "pytest -q"}, iz)
    assert not A.dogrula({"kalip": "x", "satir": n, "alinti": "uydurma"}, iz)
    assert not A.dogrula({"kalip": "x", "satir": 999, "alinti": "pytest"}, iz)


def test_cikar_kanitsiz_maddeyi_atar(tmp_path):
    iz = A.iz(_oturum(tmp_path))
    n = next(int(s.split()[0][1:]) for s in iz if "pytest -q" in s)
    yanit = json.dumps([{"kalip": "doğrulamayı koş", "satir": n, "alinti": "pytest -q"}, {"kalip": "uydurma", "satir": n, "alinti": "yok böyle"}])
    k = A.cikar(iz, lambda istem: yanit)
    assert [x["kalip"] for x in k] == ["doğrulamayı koş"]


def test_cikar_bozuk_yanit_bos_doner(tmp_path):
    assert A.cikar(A.iz(_oturum(tmp_path)), lambda i: "json degil") == []


def test_ekle_ayni_kalibi_iki_kez_yazmaz(tmp_path):
    k = {"kalip": "doğrulamayı koş", "satir": 3, "alinti": "pytest", "oturum": "s1"}
    assert A.ekle(k, tmp_path) is True
    assert A.ekle(dict(k, oturum="s2"), tmp_path) is True  # farklı oturum = ikinci kanıt
    assert A.ekle(k, tmp_path) is False
    assert len((tmp_path / "kaliplar.jsonl").read_text(encoding="utf-8").splitlines()) == 2


def test_oneri_en_az_iki_oturumda_gorulen_kalibi_listeler(tmp_path):
    for o in ("s1", "s2"):
        A.ekle({"kalip": "doğrulamayı koş", "satir": 3, "alinti": "pytest", "oturum": o}, tmp_path)
    A.ekle({"kalip": "tek seferlik", "satir": 4, "alinti": "x", "oturum": "s1"}, tmp_path)
    metin = A.oneri(tmp_path).read_text(encoding="utf-8")
    assert "doğrulamayı koş" in metin and "tek seferlik" not in metin


def test_kanca_yalniz_basarili_opus_isinde_calisir(tmp_path, monkeypatch):
    cagrilar = []
    monkeypatch.setattr(A, "oturum_bul", lambda sid: _oturum(tmp_path))
    monkeypatch.setattr(A, "model_cagir", lambda istem: cagrilar.append(istem) or "[]")
    assert A.kanca("s1", "tamam", "haiku", dizin=tmp_path) is None
    assert A.kanca("s1", "hata", "opus", dizin=tmp_path) is None
    assert cagrilar == []
    assert A.kanca("s1", "tamam", "opus", dizin=tmp_path) == 0
    assert len(cagrilar) == 1


def test_secki_numaralari_korur_ve_boyu_sinirlar():
    sat = [f"L{i} ARAC Bash: x{i}" for i in range(1, 2001)]
    sat[999] = "L1000 HATA: patladı"
    s = A.secki(sat, 220)
    assert len(s) <= 260 and sat[999] in s and sat[0] in s and sat[-1] in s
