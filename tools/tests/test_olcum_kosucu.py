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


def test_ayristir_read_yollarini_kaydeder():
    s = _akis({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Read", "input": {"file_path": "C:\\p\\.claude\\skills\\k3-x\\references\\a.md"}},
        {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}})
    o = kosucu.ayristir(s)
    assert o["okunan"] == ["C:/p/.claude/skills/k3-x/references/a.md"]


def test_ayristir_result_yoksa_ilk_tur_usage():
    o = kosucu.ayristir(_akis({"type": "assistant", "message": {"usage": {"input_tokens": 9}, "content": []}}, "bozuk"))
    assert o["usage"] == {"input_tokens": 9}


def test_puan_tavan_ve_isabet():
    r = [{"puan": 6, "regex": "pdf"}, {"puan": 6, "regex": "csv"}]
    assert kosucu.puanla("PDF -> CSV", r) == 10
    assert kosucu.isabet([], []) == 1
    assert kosucu.isabet(["Skill:pdf"], ["Skill"]) == 1
    assert kosucu.isabet(["Read"], ["Skill"]) == 0


def test_g06_isabet_yalniz_gercek_web_araci():
    g = next(x for x in json.loads((kosucu.DIZIN / "gorevler.json").read_text(encoding="utf-8")) if x["id"] == "G06")
    for a in ("WebFetch", "WebSearch", "mcp__mcp-fetch__fetch", "mcp__brave-search__brave_web_search", "mcp__context7__query-docs",
              "mcp__plugin_context-mode_context-mode__ctx_fetch_and_index",
              "Skill:anthropic-skills:departman-arastirma-ogrenme", "Skill:departman-arastirma-ogrenme"):
        assert kosucu.isabet(["Bash", a], g["arac"]) == 1, a
    for a in ("mcp__plugin_context-mode_context-mode__ctx_execute", "Bash", "Skill:frontend-craft:frontend-craft"):
        assert kosucu.isabet([a], g["arac"]) == 0, a


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


def test_ayar_birlestir_yalniz_agent_deny_eklenir():
    ayar = {"permissions": {"deny": ["Read(./bin/**)", "Agent(x)"], "allow": ["Bash(git status)"]}}
    profil = {"permissions": {"deny": ["Agent(x)", "Agent(y)", "Bash(rm:*)"], "allow": ["Bash(*)"]}}
    _, degisen = ayar_uygula.birlestir(ayar, profil)
    assert ayar["permissions"] == {"deny": ["Read(./bin/**)", "Agent(x)", "Agent(y)"], "allow": ["Bash(git status)"]}
    assert degisen == {"permissions.deny": (2, 3)} and "env" not in ayar


def test_init_yaz_yalniz_ad(tmp_path):
    y = tmp_path / "i.json"
    kosucu.init_yaz(y, {"mcp_servers": [{"name": "x", "status": "connected"}], "skills": ["a"], "model": "m",
                        "tools": ["Bash", "mcp__netlify__netlify-coding-rules"]})
    d = json.loads(y.read_text(encoding="utf-8"))
    assert d == {"mcp_servers": ["x"], "skills": ["a"], "model": "m", "tools": {"toplam": 2, "mcp": 1}}
    assert "netlify" not in y.read_text(encoding="utf-8")
    kosucu.init_yaz(y, {"skills": ["b"]})
    assert json.loads(y.read_text(encoding="utf-8"))["skills"] == ["a"]


def test_isabet_skill_ad_alani_yok_sayilir():
    assert kosucu.isabet(["Skill:anthropic-skills:blender-oturum"], ["Skill:blender"]) == 1
    assert kosucu.isabet(["Bash"], ["Skill:blender"]) == 0
    assert kosucu.isabet(["Agent:video-tarayici"], ["Skill:video"]) == 0


def test_rubrik_yazilan_dosyayi_da_gorur():
    s = json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Write", "input": {"file_path": "a.ts", "content": "page.goto('/login')"}}]}})
    o = kosucu.ayristir(s)
    assert o["girdi"] == ["page.goto('/login')"]


def test_rubrik_windows_yol_ayiricisi():
    # A01–A03 (16:12): yanıt `C:\\...\\.claude\\ajan-getir-e2e\\A01.md` dedi, rubrik `/` bekledi → kalite 10 yerine 5
    r = [{"puan": 5, "regex": r"ajan-getir-e2e/A01\.md"}, {"puan": 5, "regex": r"C:\\Projeler"}]
    assert kosucu.puanla(r"kaydedildi: C:\Projeler\omer-skills\.claude\ajan-getir-e2e\A01.md", r) == 10


# --- KOSUCU-TEMIZ: süreç sızıntısı ---
import os  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402
import pytest  # noqa: E402

_UZUN = "import time; time.sleep(120)"


def _canli(pid):
    return kosucu.pid_canli(pid)


def _bekle_olu(pid, sn=10):
    t = time.time()
    while time.time() - t < sn:
        if not _canli(pid):
            return True
        time.sleep(0.2)
    return False


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Job Object yalnız Windows")
@pytest.mark.parametrize("zaman_asimi", [False, True])
def test_calistir_torun_surec_biter(tmp_path, zaman_asimi):
    # sarmalayıcı uzun yaşayan bir torun başlatır, pid'ini yazar; ardından ya hemen biter ya da asılır (timeout)
    betik = tmp_path / "sar.py"
    betik.write_text(
        "import subprocess, sys, time\n"
        f"p = subprocess.Popen([sys.executable, '-c', {_UZUN!r}], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\n"
        "print(p.pid, flush=True)\n" + ("time.sleep(120)\n" if zaman_asimi else ""), encoding="utf-8")
    out, rc, _ = kosucu.calistir([sys.executable, str(betik)], dict(os.environ), str(tmp_path), 3 if zaman_asimi else 30)
    pid = int(out.split()[0])
    assert (rc == -9) == zaman_asimi
    assert _bekle_olu(pid), "torun süreç iş kapanınca ölmedi"


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="süpürme Windows komut satırı sorgular")
def test_supur_yalniz_dizin_adi_eslesen_surecleri_oldurur(tmp_path):
    ad = "olcum-supurtest9"
    eslesen = subprocess.Popen([sys.executable, "-c", _UZUN, ad], creationflags=kosucu.PENCERESIZ)
    baska = subprocess.Popen([sys.executable, "-c", _UZUN, "baska-dizin"], creationflags=kosucu.PENCERESIZ)
    try:
        time.sleep(1)
        kosucu.supur(ad)
        assert _bekle_olu(eslesen.pid)
        assert _canli(baska.pid)
    finally:
        eslesen.kill()
        baska.kill()


def test_kos_env_tarayici_acmaz(monkeypatch):
    gorulen = {}

    def sahte(args, env, cwd, timeout):
        gorulen["env"] = env
        return "", 0, ""

    monkeypatch.setattr(kosucu, "calistir", sahte)
    monkeypatch.setattr(kosucu, "supur", lambda ad: None)
    kosucu.kos("x")
    assert gorulen["env"]["BROWSER"] == "none"
    assert gorulen["env"]["DISABLE_AUTOUPDATER"] == "1"  # MCP-HAFIF-2: eklenti güncelleme klonu (temp_git) yok
    assert gorulen["env"]["CLAUDE_MEM_INTERNAL"] == "1"  # claude-mem SessionStart bağlamı yok


def test_kos_mcp_hafif_bayrak_ve_strict_cagiran(monkeypatch):
    gorulen = []
    monkeypatch.setattr(kosucu, "calistir", lambda args, env, cwd, timeout: (gorulen.append(args), ("", 0, ""))[1])
    monkeypatch.setattr(kosucu, "supur", lambda ad: None)
    monkeypatch.setattr(kosucu.mcp_sec, "tanimlar", lambda yol=None: {"serena": {"command": "s"}, "blender": {}})
    monkeypatch.setenv("OLCUM_MCP_HAFIF", "0")  # MCP-HAFIF-2: KABUL eşit → varsayılan açık, 0 = tam user MCP
    kosucu.kos("mcp__blender__x")
    monkeypatch.delenv("OLCUM_MCP_HAFIF", raising=False)
    kosucu.kos("mcp__blender__x")
    kosucu.kos("y", ek=["--strict-mcp-config"])
    assert [a.count("--strict-mcp-config") for a in gorulen] == [0, 1, 1]


def test_jev_doldur_kosu_sonu_toplu_ve_erisilemezse_regex_aynen(tmp_path):
    assert kosucu.BASLIK.endswith("\thata\tjev\tjev_guven")
    d = tmp_path / "2026-10-11-p"
    d.mkdir()
    (d / "G01-1.md").write_text("yanıt", encoding="utf-8")
    y = tmp_path / "2026-10-11-p.tsv"
    kosucu.satir_yaz(y, "G01\t1" + "\tx" * 14)
    once = y.read_text(encoding="utf-8")

    class Bozuk:
        def yargila(self, s, q):
            raise OSError("ağ yok")
    kosucu.jev_doldur(y, d, tasiyici=Bozuk())
    assert y.read_text(encoding="utf-8") == once

    class Sahte:
        cagri = 0
        def yargila(self, s, q):
            Sahte.cagri += 1
            return [{"kalite": {"score": 3.5, "confidence": 0.6}} for _ in s]
    kosucu.jev_doldur(y, d, tasiyici=Sahte())
    assert Sahte.cagri == 1 and y.read_text(encoding="utf-8").splitlines()[1].endswith("\t7.0\t0.6")


def test_karsilastir_regex_doymussa_jev_ayirir(tmp_path, monkeypatch):
    import karsilastir
    monkeypatch.setattr(karsilastir, "D", tmp_path)
    for ad, jv in (("a", ("6.0", "")), ("b", ("9.0", "8.0"))):
        satir = [kosucu.BASLIK] + ["\t".join([g, "1", "0", "0", "0", "5", "100", "1", "1", "0.1", "1", "10", "0", "0", "", "", j, ""])
                                  for g, j in zip(("G01", "G02"), jv)]
        (tmp_path / f"2026-10-11-{ad}.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8")
    assert karsilastir.ozet(karsilastir.oku("2026-10-11", "a"), {"G01", "G02"})["jev"] == 6.0
    karsilastir.main(["2026-10-11", "a", "b"])
    md = (tmp_path / "2026-10-11-karsilastirma.md").read_text(encoding="utf-8")
    assert "jev ayırır: b" in md and "| G01 | 10/1/6.0 | 10/1/9.0 |" in md
