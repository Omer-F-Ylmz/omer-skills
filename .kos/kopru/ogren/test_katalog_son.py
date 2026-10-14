"""Küçük fikstür: python -m pytest test_katalog_son.py"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import katalog_son as s


def _k(i, ad, tur="skill", kaynak="cc-skills", grup="", aciklama="", bayt=10, kat="diğer"):
    return {"id": i, "ad": ad, "tur": tur, "kaynak": kaynak, "yol": f"x/{i}", "aciklama": aciklama, "bayt": bayt,
            "kopya_grubu": grup, "kategori_tahmin": kat}


def test_karar_oylari():
    assert s.karar({"oy1": "token", "oy2": "token"}, "diğer") == ("token", "iki-oy")
    assert s.karar({"oy1": "token", "oy2": "belge"}, "diğer") == (None, "bekliyor")
    assert s.karar({"oy1": "token", "oy2": "belge", "oy3": "belge"}, "diğer") == ("belge", "üç-oy")
    assert s.karar({"oy1": "token", "oy2": "belge", "oy3": "3d"}, "belge") == ("belge", "düşük")
    assert s.karar({"oy1": "uydurma"}, "3d") == ("3d", "kural")


def test_guven_ve_token_ipucu():
    assert s.kural_guven(_k("a", "blender-mesh", aciklama="blender mesh shader")) == "yüksek"
    assert s.kural_guven(_k("b", "x", aciklama="react test")) == "düşük"
    assert s.oylanacak(_k("c", "ozet-hafiza", aciklama="blender blender oturum hafıza", kat="3d"))  # yüksek ama token ipucu
    assert not s.oylanacak(_k("d", "m", tur="model", kat="diğer"))


def test_kullanim_ayristirma():
    assert s.ilk_sozcukler('cd /c/x && FOO=1 rtk git status | C:\\py\\python.exe -X a') == ["cd", "rtk", "python"]
    assert s.mcp_sunucu("mcp__plugin_context-mode_context-mode__ctx_search") == "context-mode"
    assert s.mcp_sunucu("mcp__blender__execute") == "blender"
    say = __import__("collections").Counter()
    s.satir_say({"type": "assistant", "timestamp": "2026-10-10", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "superpowers:Brainstorming"}},
        {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "okuyucu"}}]}}, say, "2026-09-15")
    s.satir_say({"type": "assistant", "timestamp": "2026-08-01", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "eski"}}]}}, say, "2026-09-15")
    assert say["skill", "brainstorming"] == 1 and say["agent", "okuyucu"] == 1 and say["skill", "eski"] == 0


def test_katman_kanonik():
    rows = [_k("k1", "departman-x"), _k("k2", "kardes", kaynak="plugin:p@m"), _k("k3", "araç-a", kaynak="plugin:p@m"),
            _k("k4", "yalniz"), _k("k5", "az-kullanilan"), _k("k6", "aday-x", tur="aday"),
            _k("g1", "dup", grup="ad:dup", bayt=5), _k("g2", "dup", grup="ad:dup", bayt=9)]
    kull = {"k1": 0, "k2": 0, "k3": 4, "k4": 0, "k5": 1, "k6": 0, "g1": 0, "g2": 0}
    kat = s.katmanla(rows, kull, {"departman-x"})
    assert [kat[i] for i in ("k1", "k2", "k3", "k4", "k5", "k6")] == ["A", "B", "A", "C", "B", "-"]
    kan, fark = s.kanonikle(rows, bilgi=lambda y: {"x/g1": (2.0, "aa"), "x/g2": (1.0, "bb")}.get(y, (0, None)))
    assert kan["g1"] == kan["g2"] == "g1" and fark["g2"] is True and kan["k4"] == "k4"


def test_kullanim_esle_plugin_toplami():
    rows = [_k("p", "pwt", tur="plugin", kaynak="plugins"), _k("s", "kos", kaynak="plugin:pwt@m"), _k("c", "rtk", tur="cli")]
    out = s.kullanim_esle(rows, {"skill\tkos": 2, "cli\trtk": 7})
    assert out == {"p": 2, "s": 2, "c": 7}


def test_modeller_tsv(tmp_path):
    j = tmp_path / "m.json"
    j.write_text(json.dumps({"data": [{"id": "openrouter/a/coder:free", "owned_by": "openrouter", "capabilities": {"vision": True}, "context_length": 9},
                                      {"id": "x/tts-1", "owned_by": "x", "type": "audio", "capabilities": {}}]}), encoding="utf-8")
    assert s.modeller_tsv(j, tmp_path / "m.tsv") == 2
    L = (tmp_path / "m.tsv").read_text(encoding="utf-8").splitlines()
    assert L[1] == "openrouter/a/coder:free\topenrouter\ttrue\t1\t1\t0\t1\t9"
    assert L[2].split("\t")[4:6] == ["0", "1"]  # görsel 0, ses 1
