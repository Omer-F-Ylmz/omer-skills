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
