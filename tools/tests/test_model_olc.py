import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model_olc as mo  # noqa: E402
from olcum import kosucu  # noqa: E402


def test_tanim_frontmatter_modelini_ezer(tmp_path):
    y = tmp_path / "a.md"
    y.write_text("---\nname: fe-x\ndescription: Does x. Use when y.\nmodel: sonnet\ntools: Read\n---\nGövde\n", encoding="utf-8")
    ad, t = mo.tanim(y, "opus")
    assert ad == "fe-x" and t == {"description": "Does x. Use when y.", "prompt": "Gövde", "model": "opus"}


def test_ek_ezme_yalniz_istenince_settings_env_yazar():
    assert "--settings" not in mo.ek("a", {}, None)
    e = mo.ek("a", {"model": "opus"}, "")
    assert json.loads(e[e.index("--settings") + 1]) == {"env": {"CLAUDE_CODE_SUBAGENT_MODEL": ""}}
    assert json.loads(e[e.index("--agents") + 1]) == {"a": {"model": "opus"}}


def test_alt_jeton_ana_modeli_disarida_birakir():
    mu = {"claude-haiku-5-5": {"inputTokens": 5, "outputTokens": 5},
          "claude-opus-5-5": {"inputTokens": 10, "outputTokens": 2, "cacheReadInputTokens": 3, "cacheCreationInputTokens": 1}}
    assert mo.alt(mu) == ("claude-opus-5-5", 16)


def test_karsilastir_ezme_islemezse_ilk_satirdan_sonra_durur(tmp_path, monkeypatch):
    # 18:20 dogrula: "" ezmesi frontmatter opus'u geri getirmedi (alt ajan ana modelde) → eski ön koşul karsilastir'ı hiç koşturmadı.
    # Karsilastir açık model ezmesi (sonnet/opus) kullanır; işlemediği an (alt model ≠ istenen) kalan çağrılar boşa gitmesin.
    aile = tmp_path / "ajan" / "frontend"
    aile.mkdir(parents=True)
    (aile / "fe-x.md").write_text("---\nname: fe-x\ndescription: d\nmodel: opus\n---\nG\n", encoding="utf-8")
    (tmp_path / "ajan" / "gorevler.json").write_text(json.dumps([{"ajan": "fe-x", "istem": "i", "rubrik": []}]), encoding="utf-8")
    monkeypatch.setattr(mo, "AJAN", tmp_path / "ajan")
    monkeypatch.setattr(mo, "TSV", tmp_path / "m.tsv")
    cagri = []

    def sahte(ad, t, ezme, gorev):
        cagri.append(ezme)
        return {"metin": "x", "usd": 0.1, "sure": 1, "araclar": ["Agent:fe-x"],
                "model": {"claude-haiku-5-5": {"inputTokens": 1}, "claude-haiku-5-5-alt": {"inputTokens": 1}}}
    monkeypatch.setattr(mo, "kos", sahte)
    try:
        mo.main("karsilastir")
        assert False, "durmalıydı"
    except SystemExit as e:
        assert "ezme" in str(e)
    assert cagri == ["sonnet"]
    assert len((tmp_path / "m.tsv").read_text(encoding="utf-8").splitlines()) == 2  # başlık + kanıt satırı


def test_ayristir_model_usage_tasir():
    s = json.dumps({"type": "result", "modelUsage": {"m": {"inputTokens": 1}}})
    assert kosucu.ayristir(s)["model"] == {"m": {"inputTokens": 1}}


def test_pilot_departman_sirasiyla_iki_kol_tavanli_surer(tmp_path, monkeypatch):
    # devam-5 adım 3: her yeni ajan tek görevle ajan kolu ↔ ana-oturum kolu; departman başına ilk 2 ajan, çift yarım kalmaz
    g = []
    for dep in ("a-dep", "b-dep"):
        (tmp_path / "ajan" / dep).mkdir(parents=True)
        for i in range(3):
            ad = f"{dep[0]}{i}"
            (tmp_path / "ajan" / dep / f"{ad}.md").write_text(f"---\nname: {ad}\ndescription: d\nmodel: opus\n---\nG\n", encoding="utf-8")
            g.append({"ajan": ad, "model": "opus", "istem": "i", "rubrik": [{"regex": "ok", "puan": 7}]})
    (tmp_path / "ajan" / "gorevler.json").write_text(json.dumps(g), encoding="utf-8")
    monkeypatch.setattr(mo, "AJAN", tmp_path / "ajan")
    monkeypatch.setattr(mo, "PILOT", tmp_path / "p.tsv")
    monkeypatch.setattr(mo, "YANIT", tmp_path / "yanit")
    cagri = []
    sonuc = {"metin": "ok", "usd": 0.1, "sure": 1, "araclar": [], "model": {"claude-opus-5-5": {"inputTokens": 4}}}
    monkeypatch.setattr(mo, "kos", lambda ad, t, ezme, gorev: cagri.append((ad, "ajan", ezme, t["model"])) or sonuc)
    monkeypatch.setattr(mo, "ana", lambda gorev, model: cagri.append(("ana", model)) or sonuc)
    mo.pilot(6)  # devam-10: departman sırası — her turda her departmandan bir ajan
    assert cagri == [("a0", "ajan", "opus", "opus"), ("ana", "opus"), ("b0", "ajan", "opus", "opus"), ("ana", "opus"),
                     ("a1", "ajan", "opus", "opus"), ("ana", "opus")]
    mo.pilot(3)  # sürdürme: yazılmış çiftler atlanır, çift yarım kalmaz
    assert [c[0] for c in cagri[6:]] == ["b1", "ana"]
    mo.pilot(99)  # kalan tüm ajanlar (ilk 2 sınırı yok)
    satirlar = (tmp_path / "p.tsv").read_text(encoding="utf-8").splitlines()
    assert [c[0] for c in cagri[8:]] == ["a2", "ana", "b2", "ana"] and len(satirlar) == 13
    assert (tmp_path / "yanit" / "b1-ana.md").read_text(encoding="utf-8") == "ok"  # Jev yargıcı için


def test_ayristir_arka_plan_ajaninda_bos_son_result_yaniti_ezmez():
    # devam-6 kök neden: Agent arka planda koşunca -p akışında 3 result olur (132 kr "arka planda" → 2186 kr yanıt → 0 kr, num_turns 0);
    # son result'ı almak karsilastir/pilot ajan kolunun ~yarısını 0 puan yaptı.
    s = "\n".join(json.dumps({"type": "result", "result": r, "num_turns": n, "total_cost_usd": 0.26})
                  for r, n in (("running in background", 2), ("YANIT", 1), ("", 0)))
    o = kosucu.ayristir(s)
    assert o["metin"] == "YANIT" and o["usd"] == 0.26


def test_bos_yanit_bir_kez_yeniden_denenir_sonra_hata(monkeypatch):
    cagri = []
    monkeypatch.setattr(kosucu, "kos", lambda *a, **k: cagri.append(1) or {"metin": " "})
    o = mo.ana("i", "sonnet")
    assert len(cagri) == 2 and mo.puan(o, [{"regex": ".", "puan": 10}]) == "hata"
    assert mo.puan({"metin": "ok"}, [{"regex": "ok", "puan": 7}]) == 7


def test_karsilastir_yaniti_saklar_ve_bitmis_satiri_atlar(tmp_path, monkeypatch):
    aile = tmp_path / "ajan" / "frontend"
    aile.mkdir(parents=True)
    (aile / "fe-x.md").write_text("---\nname: fe-x\ndescription: d\nmodel: opus\n---\nG\n", encoding="utf-8")
    (tmp_path / "ajan" / "gorevler.json").write_text(json.dumps([{"ajan": "fe-x", "istem": "i", "rubrik": []}]), encoding="utf-8")
    monkeypatch.setattr(mo, "AJAN", tmp_path / "ajan")
    monkeypatch.setattr(mo, "TSV", tmp_path / "m.tsv")
    monkeypatch.setattr(mo, "YANIT", tmp_path / "yanit")
    cagri = []
    monkeypatch.setattr(mo, "kos", lambda ad, t, ezme, gorev: cagri.append(ezme) or {
        "metin": "Y", "usd": 0.1, "sure": 1, "araclar": [], "model": {f"claude-{ezme}-5-5": {"inputTokens": 1}}})
    mo.main("karsilastir")
    mo.main("karsilastir")  # sürdürme: yazılmış satırlar yeniden koşmaz
    assert cagri == ["sonnet", "opus"]
    assert (tmp_path / "yanit" / "fe-x-opus.md").read_text(encoding="utf-8") == "Y"


def test_haiku_ajanda_ana_oturum_sonnet_alt_usd_ayrilir():
    # devam-10: haiku ajan + haiku ana → tek model anahtarı, alt_model '-' (r9 güvenilmez 3 ajan); ana sonnet olur
    assert mo.ana_model("haiku") == "sonnet" and mo.ana_model("opus") == "haiku"
    mu = {"claude-sonnet-5-5": {"inputTokens": 9, "costUSD": 0.05}, "claude-haiku-5-5": {"inputTokens": 5, "costUSD": 0.01}}
    assert mo.alt(mu, "sonnet") == ("claude-haiku-5-5", 5) and mo.alt_usd(mu, "sonnet") == 0.01
