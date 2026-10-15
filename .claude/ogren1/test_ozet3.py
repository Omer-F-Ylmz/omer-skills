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


def test_sinirlar_govdede_uyari_varsa_belirsiz_ret():
    # d7: vrm-headroom-geri-cagirma — başlık yok ama gövdede NEVER satırı vardı, "belirsiz" geçti
    from ozet3 import gecerli_a
    m = "# Ajan\nGeri çağırma işi.\n- NEVER sıkışmış özetten satır numarası uydurmak\n"
    o = {"ne_yapar": "geri çağırır", "komut": "belirsiz", "girdi_cikti": "belirsiz", "sinirlar": "belirsiz",
         "alinti": {"ne_yapar": "Geri çağırma işi."}}
    assert gecerli_a(o, m) == "sinirlar boş, belgede ilgili bölüm var"


def test_komut_olay_adi_ya_da_yonerge_ret():
    # d7: cagri_sayac komut="SessionStart, PostToolUse" · context-engineering komut="Use when starting new session"
    from ozet3 import komut_mu
    m = "SessionStart → sayaç\nUse when starting new session\n```\nqmd search \"x\"\n```\n`--model <M>` ve /compact\n"
    assert not komut_mu("SessionStart, PostToolUse", m)
    assert not komut_mu("Use when starting new session", m)
    assert komut_mu('qmd search "project timeline"', m)
    assert komut_mu("--model <M> --effort <E>", m)
    assert komut_mu("/compact", m)


def test_sinirlar_kucuk_harf_ve_kosullu_uyari_belirsiz_ret():
    # d8: headroom-statusline "do not edit" · ctx-doctor "only if MCP tool call fails" — iki hakem de Y
    from ozet3 import gecerli_a
    o = {"ne_yapar": "durum satırı", "komut": "belirsiz", "girdi_cikti": "belirsiz", "sinirlar": "belirsiz",
         "alinti": {"ne_yapar": "Headroom statusline"}}
    for m in ("# Headroom statusline (managed - do not edit).\n", "# Headroom statusline\n3. Fallback (only if MCP tool call fails)\n"):
        assert gecerli_a(o, m) == "sinirlar boş, belgede ilgili bölüm var"


def test_komut_baska_aracin_komutu_ret():
    # d8: how-it-works komut=/learn-codebase · budget-mode komut=/octo:model-config — belgede anılan BAŞKA komut
    from ozet3 import gecerli_a
    m = "# How it works\nExplain how claude-mem works.\nRun `/learn-codebase` if you want front-loading.\n"
    o = {"ne_yapar": "açıklar", "komut": "/learn-codebase", "girdi_cikti": "belirsiz", "sinirlar": "belirsiz",
         "alinti": {"ne_yapar": "Explain how claude-mem works.", "komut": "Run `/learn-codebase` if you want"}}
    assert gecerli_a(o, m, {"how-it-works"}) == "komut aracın kendi adını içermiyor"
    assert gecerli_a(dict(o, komut="/how-it-works"), m + "`/how-it-works`\n", {"how-it-works"}) is None
    assert gecerli_a(dict(o, komut="python tools/rtk_onisle.py --sina"), m + "    python tools/rtk_onisle.py --sina\n", {"rtk_onisle"}) is None


def test_qmd_kaynagi_readme_paylasilan():
    # d7: README geçersiz kılması yalnız ozet3 __main__'deydi → son.py kaynak=`qmd --help` yazdı, hakem yanlış belgeye baktı
    import ozet_kaynak
    from pathlib import Path
    assert Path(ozet_kaynak.D["qmd"]).as_posix().endswith("@tobilu/qmd/README.md")
