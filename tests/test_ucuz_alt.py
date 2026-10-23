"""TOKEN-2 K8 + OMNİ-AYIR: tools/ucuz_alt.py — yalnız ücretsiz zincir, alıntı kilidi, kesik → sonraki, ücretli red, önbellek, anahtar sızmaz."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ucuz_alt  # noqa: E402

UYE = ["openrouter/nvidia/nemotron-3-super-120b-a12b:free", "openrouter/google/gemma-4-31b-it:free"]


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    monkeypatch.setenv("OMNIROUTE_KEY", "GIZLI-ANAHTAR")
    monkeypatch.setattr(ucuz_alt, "DIZIN", tmp_path / "onb")
    monkeypatch.setattr(ucuz_alt, "combo_uyeleri", lambda: UYE)
    omni = [("omni", UYE[0]), ("omni", UYE[1]), ("omni", ucuz_alt.COMBO)]  # havuz halkası ağa gider; bu testler yalnız omni zincirini sınar
    monkeypatch.setattr(ucuz_alt, "ZINCIR", {**ucuz_alt.ZINCIR, "ozet": omni, "lisans": omni, "etiket": omni})
    (tmp_path / "b.txt").write_text("Copyright 2024 X. Permission is hereby granted, free of charge — MIT License", encoding="utf-8")
    return tmp_path


def yanit(icerik, model=UYE[0], bitis="stop"):
    return {"model": model, "choices": [{"message": {"content": icerik}, "finish_reason": bitis}], "usage": {"prompt_tokens": 5}}


def test_govde_ve_izin_listesi(tmp_path, monkeypatch):
    d = tmp_path / "a.txt"
    d.write_text("MIT License", encoding="utf-8")
    g = ucuz_alt.govde("lisans?", [d])
    assert g["model"] == "cc-ucuz-free" and g["reasoning_effort"] != "none"  # combo modelleri düşünmesiz 400 (TOKEN-2 d3)
    assert "MIT License" in g["messages"][0]["content"] and g["messages"][0]["content"].startswith("lisans?")
    with pytest.raises(ValueError):
        ucuz_alt.govde("x" * (ucuz_alt.TAVAN + 1), [])
    monkeypatch.setattr(ucuz_alt, "combo_uyeleri", lambda: UYE + ["openai/gpt-6.1-sol"])
    assert not ucuz_alt.ucretsiz("omni", "cc-ucuz-free") and not ucuz_alt.ucretsiz("omni", "x-ai/grok-4.7")
    assert ucuz_alt.ucretsiz("omni", UYE[0]) and ucuz_alt.ucretsiz("ollama", "qwen3.5:4b")
    assert all(ucuz_alt.ucretsiz(k, m) or m == "cc-ucuz-free" for z in ucuz_alt.ZINCIR.values() for k, m in z)
    with pytest.raises(PermissionError):
        ucuz_alt.iste(ucuz_alt.govde("x", []))


def test_lisans_dogrulanir_onbellek_anahtar_basmaz(ortam, monkeypatch, capsys):
    cagri = []
    monkeypatch.setattr(ucuz_alt, "iste", lambda g: cagri.append(g["model"]) or yanit(
        '{"lisans": "MIT", "alinti": "Permission is hereby granted, free of charge — MIT License"}'))
    arg = ["--tur", "lisans", "lisansı bul", str(ortam / "c.json"), str(ortam / "b.txt")]
    assert ucuz_alt.main(arg) == 0 and json.loads((ortam / "c.json").read_text(encoding="utf-8"))["lisans"] == "MIT"
    assert ucuz_alt.main(arg) == 0 and len(cagri) == 1  # ikinci koşu önbellekten
    assert "GIZLI-ANAHTAR" not in capsys.readouterr().out


def test_onbellek_anahtari_ayar_ve_surum_icerir_kesik_yazilmaz(ortam, monkeypatch):
    cagri = []
    def iste(g):
        cagri.append(g)
        return yanit('{"lisans": "MIT", "alinti": "Permission is hereby gr', bitis="length")
    monkeypatch.setattr(ucuz_alt, "iste", iste)
    monkeypatch.setattr(ucuz_alt, "ZINCIR", {**ucuz_alt.ZINCIR, "lisans": [("omni", UYE[0])]})
    assert ucuz_alt.coz("lisans", "lisansı bul", [ortam / "b.txt"])[0] is None
    assert ucuz_alt.coz("lisans", "lisansı bul", [ortam / "b.txt"])[0] is None and len(cagri) == 2  # kesik önbelleğe girmedi
    assert not list((ortam / "onb").glob("*.json"))
    # OmniRoute yanıt önbelleği max_tokens'u anahtara katmaz → istemde sürüm + ayar etiketi
    assert f"[ucuz_alt {ucuz_alt.SURUM} mt{cagri[0]['max_tokens']} {cagri[0]['reasoning_effort']}]" in cagri[0]["messages"][0]["content"]
    a = ucuz_alt.anahtar_ozet("lisans", (), cagri[0])
    assert a != ucuz_alt.anahtar_ozet("lisans", (), {**cagri[0], "max_tokens": 16000})
    assert a != ucuz_alt.anahtar_ozet("lisans", (), {**cagri[0], "reasoning_effort": "high"})
    monkeypatch.setattr(ucuz_alt, "SURUM", "v-test")
    assert a != ucuz_alt.anahtar_ozet("lisans", (), cagri[0])


@pytest.mark.parametrize("ilk", [
    yanit('{"lisans": "Apache-2.0", "alinti": "Licensed under the Apache License"}'),  # uydurma alıntı
    yanit('{"lisans": "MIT", "alinti": "Permission is hereby gr', bitis="length"),  # rtk-desktop kesiği
    yanit("düz metin, JSON yok"),
    yanit('{"lisans": "belirsiz", "alinti": ""}'),
    yanit('{"lisans": "MIT", "alinti": "MIT License"}', model="openai/gpt-6.1-sol"),  # ücretli modelden gelen yanıt
])
def test_ret_sonraki_modele_gecer(ortam, monkeypatch, ilk):
    sira = [ilk, yanit('{"lisans": "MIT", "alinti": "free of charge — MIT License"}', model=UYE[1])]
    monkeypatch.setattr(ucuz_alt, "iste", lambda g: sira.pop(0))
    monkeypatch.setattr(ucuz_alt, "ZINCIR", {"lisans": [("omni", UYE[0]), ("omni", UYE[1])]})
    o, model, deneme, _, _ = ucuz_alt.coz("lisans", "lisans?", [ortam / "b.txt"])
    assert o["lisans"] == "MIT" and model == UYE[1] and deneme == 2


def test_hepsi_gecmezse_cekismeli_ucretliye_yukselmez(ortam, monkeypatch, capsys):
    modeller = []
    monkeypatch.setattr(ucuz_alt, "iste", lambda g: modeller.append(g["model"]) or yanit('{"ozet": "x", "alinti": ["uydurma alıntı metni"]}'))
    monkeypatch.setattr(ucuz_alt, "sor", lambda k, m, g: (modeller.append(m), ('{"ozet": "x", "alinti": ["yok böyle bir şey"]}', "stop", m, {}))[1])
    assert ucuz_alt.main(["özetle", str(ortam / "c.md"), str(ortam / "b.txt")]) == 5
    cikti = capsys.readouterr().out
    assert not (ortam / "c.md").exists() and "ÇEKİŞMELİ" in cikti and "BEKLE" in cikti and "Claude" not in cikti
    assert ucuz_alt.HAVUZ[-1][0] == "ollama"  # ücretsiz → yerel → bekle
    assert modeller == [m for _, m in ucuz_alt.ZINCIR["ozet"]] and not any("gpt-6" in m or "grok" in m for m in modeller)


def test_429_soguma_paralel_atlar(ortam, monkeypatch):
    import urllib.error
    def hata(g):
        raise urllib.error.HTTPError("u", 429, "çok", {"retry-after": "30"}, None)
    monkeypatch.setattr(ucuz_alt, "iste", hata)
    monkeypatch.setattr(ucuz_alt, "ZINCIR", {"lisans": [("omni", UYE[0])]})
    assert ucuz_alt.coz("lisans", "a", [ortam / "b.txt"])[2] == 1
    assert ucuz_alt.soguma(UYE[0]) and ucuz_alt.coz("lisans", "b", [ortam / "b.txt"])[2] == 0


def test_bozuk_json_ret_zinciri_kesmez():
    # O12: parantezli ama geçersiz JSON (sondaki virgül) JSONDecodeError fırlatıp ölçümü kesiyordu
    assert ucuz_alt.json_al('{"lisans": "MIT",}') is None


def test_ollama_ram_korumasi(monkeypatch):  # ★ 05:48: RAM ≥%80 → ollama yok; num_ctx 8192 · keep_alive 0
    import io, types
    giden = []
    monkeypatch.setattr(ucuz_alt.urllib.request, "urlopen", lambda q, timeout: giden.append(json.loads(q.data)) or io.BytesIO(
        b'{"message": {"content": "ok"}, "done_reason": "stop"}'))
    monkeypatch.setattr(ucuz_alt, "YEREL_KAPALI", ucuz_alt.Path("yok/yerel-model.kapali"))
    monkeypatch.setattr(ucuz_alt.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=80))
    with pytest.raises(RuntimeError, match="atlandi-ram"):
        ucuz_alt.sor("ollama", "qwen3.5:4b", {"messages": []})
    assert giden == []
    monkeypatch.setattr(ucuz_alt.psutil, "virtual_memory", lambda: types.SimpleNamespace(percent=50))
    assert ucuz_alt.sor("ollama", "qwen3.5:4b", {"messages": []})[0] == "ok"
    assert giden[0]["options"]["num_ctx"] == 8192 and giden[0]["keep_alive"] == 0


def test_ollama_yerel_kapali_bayragi(monkeypatch, tmp_path):
    bayrak = tmp_path / "yerel-model.kapali"; bayrak.write_text("")
    monkeypatch.setattr(ucuz_alt, "YEREL_KAPALI", bayrak)
    with pytest.raises(RuntimeError, match="atlandi-yerel-kapali"):
        ucuz_alt.sor("ollama", "qwen3.5:4b", {"messages": []})
