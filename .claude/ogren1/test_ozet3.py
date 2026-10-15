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


def test_ollama_ram_korumasi(monkeypatch):  # ★ 05:48: RAM ≥%80 → ollama yok; num_ctx 8192 · keep_alive 0
    import io, json, types, urllib.request
    import ozet3
    giden = []
    monkeypatch.setattr(urllib.request, "urlopen", lambda q, timeout: giden.append(json.loads(q.data)) or io.BytesIO(
        b'{"message": {"content": "{\\"a\\": 1}"}, "done_reason": "stop"}'))
    monkeypatch.setattr(ozet3.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=86))
    with pytest.raises(RuntimeError, match="atlandi-ram"):
        ozet3.sor("ollama", "qwen3.5:4b", "x")
    assert giden == []
    monkeypatch.setattr(ozet3.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=50))
    assert ozet3.sor("ollama", "qwen3.5:4b", "x") == {"a": 1}
    assert giden[0]["options"]["num_ctx"] == 8192 and giden[0]["keep_alive"] == 0


def test_komut_belirsiz_baslikli_uyari_kendi_ifadesi_asla():  # d10: uydurma baskısı (knowledge-agent·komut)
    from ozet3 import gecerli_a
    m = "# Knowledge Agent\nBuilds a corpus of observations.\n\n## Filter options\nUse `build_corpus name=\"x\" limit=500` to start.\n"
    al = {"ne_yapar": "Builds a corpus of observations"}
    o = {"ne_yapar": "Gözlem korpusu kurar.", "girdi_cikti": "", "sinirlar": "", "alinti": al}
    kendi = dict(o, komut='knowledge-agent iş akışı: build_corpus name="x" ... → query', alinti=dict(al, komut='build_corpus name="x" limit=500'))
    assert gecerli_a(kendi, m) == "komut belgede birebir değil (kendi ifadesi)"
    birebir = dict(kendi, komut='build_corpus name="x" limit=500')
    assert gecerli_a(birebir, m) is None
    belirsiz = dict(o, komut="belirsiz — belge yalnız filtre seçeneklerini anlatıyor, tam çağrı yok", alinti=dict(al, komut="## Filter options"))
    assert gecerli_a(belirsiz, m) == "komut boş, belgede ilgili bölüm var"  # :free yolu (uyari listesi yok) değişmez
    u = []
    assert gecerli_a(belirsiz, m, uyari=u) is None and u and u[0].startswith("komut belirsiz")
    gerekcesiz = dict(belirsiz, komut="belirsiz")
    assert gecerli_a(gerekcesiz, m, uyari=[]) == "komut boş, belgede ilgili bölüm var"
    baska_baslik = dict(belirsiz, alinti=dict(al, komut="Filter options for search"))
    assert gecerli_a(baska_baslik, m, uyari=[]) == "komut boş, belgede ilgili bölüm var"
