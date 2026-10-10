import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import kosucu  # noqa: E402
import profil_uret  # noqa: E402
import profil_varyant  # noqa: E402
import ayar_uygula  # noqa: E402


def _akis(*olaylar):
    return "\n".join(json.dumps(o) for o in olaylar)


def test_ayristir_result_usage_tur_ve_araclar():
    s = _akis(
        {"type": "system", "subtype": "init", "skills": ["a", "b"], "mcp_servers": [{"name": "x", "status": "connected"}]},
        {"type": "assistant", "message": {"usage": {"input_tokens": 1}, "content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "frontend-craft"}},
            {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "okuyucu"}}]}},
        {"type": "result", "usage": {"input_tokens": 3, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 50,
                                     "output_tokens": 7}, "total_cost_usd": 0.5, "num_turns": 2, "result": "tamam"},
    )
    o = kosucu.ayristir(s)
    assert kosucu.jeton(o["usage"]) == (3, 100, 50, 7)
    assert o["tur"] == 2 and o["metin"] == "tamam"
    assert o["araclar"] == ["Skill:frontend-craft", "Agent:okuyucu"]
    assert o["init"]["skills"] == ["a", "b"]


def test_ayristir_result_yoksa_ilk_tur_usage():
    o = kosucu.ayristir(_akis({"type": "assistant", "message": {"usage": {"input_tokens": 9}, "content": []}}, "bozuk"))
    assert o["usage"] == {"input_tokens": 9}


def test_puan_tavan_ve_isabet():
    r = [{"puan": 6, "regex": "pdf"}, {"puan": 6, "regex": "csv"}]
    assert kosucu.puanla("PDF -> CSV", r) == 10
    assert kosucu.isabet([], []) == 1
    assert kosucu.isabet(["Skill:pdf"], ["Skill"]) == 1
    assert kosucu.isabet(["Read"], ["Skill"]) == 0


def test_profil_ek_settings_mutlak_yol():
    ek = kosucu.profil_ek({"ek": ["--strict-mcp-config"], "settings": "profil-x.json"})
    assert ek[0] == "--strict-mcp-config" and ek[1] == "--settings"
    assert Path(ek[2]).is_absolute() and ek[2].endswith("profil-x.json")
    assert kosucu.profil_ek({"ek": []}) == []


def test_satir_yaz_baslik_bir_kez(tmp_path):
    y = tmp_path / "a.tsv"
    kosucu.satir_yaz(y, "G01\t1")
    kosucu.satir_yaz(y, "G02\t1")
    satirlar = y.read_text(encoding="utf-8").splitlines()
    assert satirlar[0] == kosucu.BASLIK and satirlar[1:] == ["G01\t1", "G02\t1"]


def test_profil_uret_mevcut_korunur_cekirdek_aciklamali():
    skills = ["ecc:api-design", "anthropic-skills:departman-frontend", "frontend-craft:frontend-craft", "animate", "eski"]
    blok, n, korunan = profil_uret.uret(skills, {"eski": "off"})
    assert blok["eski"] == "off"
    assert blok["ecc:api-design"] == "name-only" and blok["animate"] == "name-only"
    assert "anthropic-skills:departman-frontend" not in blok and "frontend-craft:frontend-craft" not in blok
    assert n == 2 and korunan == ["anthropic-skills:departman-frontend", "frontend-craft:frontend-craft"]


def test_profil_varyant_env_butce(tmp_path, monkeypatch):
    monkeypatch.setattr(profil_varyant, "D", tmp_path)
    (tmp_path / "taban.json").write_text(json.dumps({"skillOverrides": {"a": "name-only"}}), encoding="utf-8")
    d = json.loads(profil_varyant.uret("v", 75000, "taban.json").read_text(encoding="utf-8"))
    assert d == {"skillOverrides": {"a": "name-only"}, "env": {"SLASH_COMMAND_TOOL_CHAR_BUDGET": "75000"}}
    assert json.loads(profil_varyant.uret("w", 40000).read_text(encoding="utf-8")) == {"env": {"SLASH_COMMAND_TOOL_CHAR_BUDGET": "40000"}}


def test_ayar_birlestir_mevcut_ezilmez_env_yazilir():
    ayar = {"skillOverrides": {"a": "off"}, "env": {"SLASH_COMMAND_TOOL_CHAR_BUDGET": "150000", "X": "1"}, "hooks": {"h": 1}}
    profil = {"skillOverrides": {"a": "name-only", "b": "name-only"}, "env": {"SLASH_COMMAND_TOOL_CHAR_BUDGET": "75000"}}
    eklenen, degisen = ayar_uygula.birlestir(ayar, profil)
    assert ayar["skillOverrides"] == {"a": "off", "b": "name-only"} and eklenen == 1
    assert ayar["env"] == {"SLASH_COMMAND_TOOL_CHAR_BUDGET": "75000", "X": "1"} and ayar["hooks"] == {"h": 1}
    assert degisen == {"SLASH_COMMAND_TOOL_CHAR_BUDGET": ("150000", "75000")}


def test_init_yaz_yalniz_ad(tmp_path):
    y = tmp_path / "i.json"
    kosucu.init_yaz(y, {"mcp_servers": [{"name": "x", "status": "connected"}], "skills": ["a"], "model": "m"})
    d = json.loads(y.read_text(encoding="utf-8"))
    assert d == {"mcp_servers": ["x"], "skills": ["a"], "model": "m"}
    kosucu.init_yaz(y, {"skills": ["b"]})
    assert json.loads(y.read_text(encoding="utf-8"))["skills"] == ["a"]
