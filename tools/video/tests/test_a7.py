"""DERİNLİK-MASTER A7: prompt adayı (arac_degil) parti akışında paket altyazısından metnini alır (model 0)."""
import json

from test_m2a import V, _ns
from test_m2b import Arastirici, _actx, _aday_md, _parti, _rapor

from video import getir as gt
from video import parti as pt
from video import tarama as tr


def _kos(kok, seg):
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("Sihirli Prompt", "prompt", None)])})
    if seg:
        (s := kok / "c" / V[0] / "segmentler.jsonl").parent.mkdir(parents=True, exist_ok=True)
        s.write_text(json.dumps({"bas": 6.0, "metin": "Şu promptu yapıştırın: her adımı test et"}, ensure_ascii=False) + "\n", encoding="utf-8")
    a = Arastirici()
    pt.parti(_ns("akil", p.name), _actx(kok, a))
    return (kok / "docs" / "kurulumlar" / "parti" / p.name / "panel.md").read_text(encoding="utf-8"), a


def test_prompt_metni_segmentten_aday_dosyasina(tmp_path):
    panel, a = _kos(tmp_path, seg=True)
    assert "her adımı test et" in tr.bolum(_aday_md(tmp_path, "sihirli-prompt"), "Prompt metni")
    assert "prompt metni ✓" in panel
    assert a.cagrilar == []  # model çağrısı 0


def test_segment_yoksa_sebep_kapsamda(tmp_path):
    panel, a = _kos(tmp_path, seg=False)
    assert "prompt metni alınamadı: altyazı yok" in panel
    assert a.cagrilar == []


# A7 eki: zamanı kapsayan segment de alınır (O45 canlı: short'ta 0–61.28 tek segment, prompt 0:50)
def test_kapsayan_segment_alinir(tmp_path):
    (s := tmp_path / "segmentler.jsonl").write_text(json.dumps({"bas": 0.0, "son": 61.3, "metin": "kapsayan prompt metni"}) + "\n", encoding="utf-8")
    m = gt.prompt_metni(_rapor(V[0], [("Sihirli Prompt", "prompt", None)]).replace("0:05", "0:50"), s)
    assert "kapsayan prompt metni" in m


def _onceden(kok, bolum):
    (y := kok / "docs" / "kurulumlar" / "adaylar" / "sihirli-prompt.md").parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"# sihirli-prompt\n\n## Prompt metni\n{bolum}\n", encoding="utf-8")


def test_bos_bolum_yeniden_yazilir(tmp_path):
    _onceden(tmp_path, "### Sihirli Prompt · 0:05\naltyazı yok (paket segmentleri bulunamadı)")
    _kos(tmp_path, seg=True)
    assert "her adımı test et" in tr.bolum(_aday_md(tmp_path, "sihirli-prompt"), "Prompt metni")


def test_dolu_bolume_dokunulmaz(tmp_path):
    _onceden(tmp_path, "elle yazılmış prompt")
    _kos(tmp_path, seg=True)
    m = tr.bolum(_aday_md(tmp_path, "sihirli-prompt"), "Prompt metni")
    assert "elle yazılmış prompt" in m and "her adımı test et" not in m
