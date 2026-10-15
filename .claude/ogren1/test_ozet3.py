"""ÖĞREN-1 d6: kesik yanıt RET · tek-kol null ≠ çekişme · gecerli_b kapalı liste.  python -X utf8 -m pytest .claude/ogren1/test_ozet3.py -q"""
import pytest
from ozet3 import gecerli_b, icerik, oyla

BELGE = "This tool measures token usage per session and writes a report."


def test_kesik_yanit_ret():
    with pytest.raises(ValueError, match="kesik"):
        icerik({"choices": [{"finish_reason": "length", "message": {"content": '{"a": 1}'}}]})
    with pytest.raises(ValueError, match="kesik"):
        icerik({"message": {"content": '{"a": 1}'}, "done_reason": "length"})  # ollama /api/chat
    assert icerik({"message": {"content": 'x {"a": 1} y'}, "done_reason": "stop"}) == {"a": 1}


def test_gecerli_b_kapali_liste():
    kanit = "measures token usage per session"
    assert not gecerli_b({"mekanizma": ["ölçmek"], "kanit": kanit}, BELGE)
    assert not gecerli_b({"mekanizma": ["ölçüm"], "kanit": "uydurma alıntı burada yok"}, BELGE)
    assert gecerli_b({"mekanizma": ["ölçüm"], "kanit": kanit}, BELGE)  # d4 listesinde 8. değer


def test_oyla_iki_gecerli_oy_kesisirse():
    assert oyla([["sıkıştırma"], None]) == []  # tek kol: üçüncü oy gerekir
    assert oyla([["sıkıştırma"], None, ["sıkıştırma", "özetleme"]]) == ["sıkıştırma"]
    assert oyla([["ölçüm"], ["önbellek"], ["ölçüm"]]) == ["ölçüm"]
    assert oyla([["a"], ["b"], ["c"]]) == []
