"""TELVE-TOKEN-1 d3 (a): durum_ozet/claude_bak durma oranı satırı."""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos" / "kopru"))
from durum_ozet import durma_orani, durma_satiri  # noqa: E402


def _yaz(yol, adimlar):
    satir = [{"type": "user", "message": {"content": "x"}}]
    for i, (g, cw) in enumerate(adimlar):
        satir.append({"type": "assistant", "message": {"id": f"m{i}", "usage": {
            "input_tokens": g, "cache_read_input_tokens": 50000, "cache_creation_input_tokens": cw}}})
    yol.write_text("\n".join(json.dumps(s) for s in satir) + "\nbozuk{\n", encoding="utf-8")


def test_son_20_adim_ve_esik(tmp_path):
    j = tmp_path / "a.jsonl"
    # 10 eski durma pencere dışında kalır; son 20: 6 durma, 2 küçük girdili cw=0 (durma değil), 12 normal
    _yaz(j, [(9000, 0)] * 10 + [(9000, 0)] * 6 + [(500, 0)] * 2 + [(10, 800)] * 12)
    assert durma_orani(j) == (6, 20)
    assert "(%30) · ≥%30" in durma_satiri([j])


def test_ayni_id_bir_kez_ve_alarmsiz(tmp_path):
    j = tmp_path / "b.jsonl"
    _yaz(j, [(9000, 0), (10, 800), (10, 800)])
    j.write_text(j.read_text(encoding="utf-8") * 2, encoding="utf-8")  # akış parçaları aynı id ile tekrarlar
    assert durma_orani(j) == (1, 3)
    assert "≥%30" in durma_satiri([j])


def test_en_yeni_transkript_ve_bos(tmp_path):
    eski, yeni = tmp_path / "eski.jsonl", tmp_path / "yeni.jsonl"
    _yaz(eski, [(9000, 0)] * 5)
    _yaz(yeni, [(10, 800)] * 5)
    os.utime(eski, (1, 1))
    s = durma_satiri([eski, yeni])
    assert "yeni" in s and "son 5 adımda 0 (%0)" in s and "DUR" not in s
    assert durma_satiri([]) == "-- durma: transkript yok"
