import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "laya"))
import puan  # noqa: E402

HAM = json.loads((Path(__file__).parent / "veri" / "omni_ham.json").read_text(encoding="utf-8"))  # OmniRoute cc-ucuz-free ham yanıtları (23 Eki)


def test_gercek_omniroute_temiz_yanit():
    assert [puan.ayikla(h["content"]) for h in HAM if h["finish"] == "stop"] == [0, 5]


def test_gercek_omniroute_kesik_dusunme_puan_degil():
    kesik = [h for h in HAM if h["finish"] == "length"][0]["content"]
    assert "Score 0" in kesik and puan.ayikla(kesik) is None  # taslak "Score 0." son karar sayılmaz


@pytest.mark.parametrize("yanit,beklenen", [
    ('{"score": 4}', 4),
    ('```json\n{"score": 4}\n```', 4),
    ('{"score": "3"}', 3),
    ('{"score": 4.0}', 4),
    ('<think>belki {"score": 2}</think>\n{"score": 4}', 4),
    ('Taslak {"score": 2} ... Son karar: {"score": 3}', 3),
    ('Analiz...\nScore: 4', 4),
    ('**Puan: 5**', 5),
    ('{"score": 4.5}', None),
    ('{"score": 7}', None),
    ('{"score": 10}', None),
    ('Kısmen. Score 3 gibi duruyor ama emin değilim', None),
    ('', None),
    (None, None),
])
def test_ayikla_varyant_0_5(yanit, beklenen):
    assert puan.ayikla(yanit) == beklenen


def test_ayikla_0_10():
    assert puan.ayikla('{"score": 10}', 10) == 10
    assert puan.ayikla('{"score": 7.5}', 10) == 7.5
    assert puan.ayikla('{"score": 11}', 10) is None
