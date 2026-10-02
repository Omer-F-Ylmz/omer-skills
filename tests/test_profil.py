"""TOKEN-3b K2: tools/profil.py — proje profili (skillOverrides/enabledPlugins) + router bölümü."""
import copy
import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import profil  # noqa: E402

KORUNAN_HOOK = {"PreToolUse": [{"matcher": "Bash|PowerShell", "hooks": [{"type": "command", "command": "powershell -File korunan_yollar.ps1"}]}]}
DENY = ["Edit(//c/Users/pc/Desktop/zzzmods/**)", "Edit(//c/Program Files/Epic Games/GenshinImpact/**)"]


def skill(d, ad, desc="İşi yapar. İkinci cümle."):
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: {desc}\n---\ngövde\n", encoding="utf-8")


@pytest.fixture
def ev(tmp_path):
    c = tmp_path / "home" / ".claude"
    kayit = {}
    for ad, sks, hook in [("claude-mem", ["mem-search"], True), ("phoenix-x", ["px"], False),
                          ("dotnet-data", ["ef"], False), ("superpowers", ["brainstorming"], True)]:
        p = c / f"plugins/cache/m/{ad}/1.0.0"
        for s in sks:
            skill(p / "skills" / s, s)
        if hook:
            (p / "hooks").mkdir(parents=True)
            (p / "hooks/hooks.json").write_text('{"hooks": {}}', encoding="utf-8")
        kayit[f"{ad}@m"] = [{"installPath": str(p)}]
    (c / "plugins/installed_plugins.json").write_text(json.dumps({"version": 2, "plugins": kayit}), encoding="utf-8")
    for s in ["threejs-bloom", "threejs-x", "graphify", "agent-reach", "review"]:
        skill(c / "skills" / s, s)
    skill(c / "skills/gstack/review", "review")
    (c / "settings.json").write_text('{"skillOverrides": {"anthropic-skills:a": "off"}}', encoding="utf-8")
    proje = tmp_path / "proje"
    (proje / ".claude").mkdir(parents=True)
    veri = {"her_zaman": ["superpowers"], "kucuk_500kr": [],
            "projeler": {str(proje): "p"},
            "profiller": {"p": {"acik": [], "name_only": ["threejs"]}},
            "cagri14": {"dotnet-data": 1, "agent-reach": 1, "gstack": 2},
            "mcp14": {"claude-mem": 3}, "ajan14": {},
            "hook_sinif": {"claude-mem": "H", "superpowers": "E"},
            "router": {"phoenix-x": "guvenlik", "graphify": "arastirma-ogrenme"}}
    return {"home": tmp_path / "home", "proje": proje, "veri": veri, "env": profil.envanter(tmp_path / "home")}


def ayar(e):
    return e["proje"] / ".claude/settings.json"


def uygula(e):
    return profil.uygula(e["proje"], profil.hesapla("p", e["veri"], e["env"]), e["home"])


def test_name_only_off_ayrimi_kurala_gore(ev):
    h = profil.hesapla("p", ev["veri"], ev["env"])
    assert h["skillOverrides"] == {"threejs-bloom": "name-only", "threejs-x": "name-only", "review": "name-only",
                                   "agent-reach": "name-only", "graphify": "off"}
    assert h["enabledPlugins"] == {"phoenix-x@m": False}
    assert set(h["atlanan"]) == {"claude-mem", "dotnet-data"}


def test_birlestirme_mevcut_anahtarlari_korur(ev):
    ayar(ev).write_text('{"skillOverrides": {"benim": "off"}, "env": {"A": "1"}}', encoding="utf-8")
    uygula(ev)
    d = json.loads(ayar(ev).read_text(encoding="utf-8"))
    assert d["skillOverrides"]["benim"] == "off" and d["env"] == {"A": "1"}
    assert d["skillOverrides"]["graphify"] == "off" and d["enabledPlugins"] == {"phoenix-x@m": False}


def test_korunan_yollar_hook_ve_deny_korunur(ev):
    ayar(ev).write_text(json.dumps({"permissions": {"deny": DENY}, "hooks": KORUNAN_HOOK}), encoding="utf-8")
    uygula(ev)
    d = json.loads(ayar(ev).read_text(encoding="utf-8"))
    assert d["permissions"]["deny"] == DENY and d["hooks"] == KORUNAN_HOOK


def test_hook_saglayan_plugin_kapatilamaz(ev):
    veri = copy.deepcopy(ev["veri"])
    veri["mcp14"] = {}  # yalnız H hook'u kalsın
    with pytest.raises(ValueError):
        profil.kapat_dogrula("claude-mem", veri)
    h = profil.hesapla("p", veri, ev["env"])
    assert "claude-mem@m" not in h["enabledPlugins"] and "claude-mem" in h["atlanan"]
    veri["hook_sinif"] = {}
    veri["mcp14"] = {"claude-mem": 1}  # kullanılmış MCP de korur
    with pytest.raises(ValueError):
        profil.kapat_dogrula("claude-mem", veri)


def test_yedek_ve_geri_bayt_esit(ev):
    ham = b'{\r\n  "permissions":   {"deny": []}\r\n}'
    ayar(ev).write_bytes(ham)
    uygula(ev)
    assert ayar(ev).read_bytes() != ham
    assert (ev["proje"] / ".claude/settings.json.bakT3b").read_bytes() == ham
    profil.geri(ev["proje"])
    assert ayar(ev).read_bytes() == ham


def test_bomlu_settings_okunur_geri_bayt_esit(ev):
    ham = b'\xef\xbb\xbf{}\r\n'
    ayar(ev).write_bytes(ham)
    uygula(ev)
    assert json.loads(ayar(ev).read_bytes())["enabledPlugins"] == {"phoenix-x@m": False}
    profil.geri(ev["proje"])
    assert ayar(ev).read_bytes() == ham


def test_geri_dosya_yoksa_yokluga_doner_silmeden(ev):
    uygula(ev)
    profil.geri(ev["proje"])
    assert not ayar(ev).exists()
    assert (ev["proje"] / ".claude/settings.json.geriT3b").exists()


def test_idempotent(ev):
    ayar(ev).write_text('{"a": 1}', encoding="utf-8")
    uygula(ev)
    bir = ayar(ev).read_bytes()
    uygula(ev)
    assert ayar(ev).read_bytes() == bir
    assert (ev["proje"] / ".claude/settings.json.bakT3b").read_bytes() == b'{"a": 1}'


def test_bilinmeyen_skill_adi_hata(ev):
    ev["veri"]["profiller"]["p"]["acik"] = ["boyle-bir-sey-yok"]
    with pytest.raises(ValueError, match="bilinmeyen"):
        profil.hesapla("p", ev["veri"], ev["env"])


def test_kapali_aile_router_eslemesi_yoksa_hata(ev):
    del ev["veri"]["router"]["graphify"]
    with pytest.raises(ValueError, match="router"):
        profil.hesapla("p", ev["veri"], ev["env"])


def test_router_blogunda_yalniz_var_olan_yollar(ev):
    bloklar = profil.router_bloklari(ev["veri"], ev["env"])
    assert set(bloklar) == {"guvenlik", "arastirma-ogrenme"}
    yollar = [y for b in bloklar.values() for y in profil.blok_yollari(b)]
    assert len(yollar) == 2 and all(Path(y).exists() for y in yollar)
    assert "yalnız CC" in bloklar["guvenlik"] and "Read ile aç" in bloklar["guvenlik"]


def test_router_yaz_idempotent(tmp_path):
    f = tmp_path / "SKILL.md"
    f.write_text("---\nname: d\ndescription: x\n---\n# D\n", encoding="utf-8")
    blok = profil.BLOK_BAS + "\n- a\n" + profil.BLOK_SON
    assert profil.router_yaz(f, blok) is True
    assert profil.router_yaz(f, blok) is False
    assert f.read_text(encoding="utf-8").count(profil.BLOK_BAS) == 1


def test_global_settingse_yazmaz(ev):
    g = ev["home"] / ".claude/settings.json"
    once = g.read_bytes()
    with pytest.raises(ValueError):
        profil.uygula(ev["home"], profil.hesapla("p", ev["veri"], ev["env"]), ev["home"])
    uygula(ev)
    assert g.read_bytes() == once


def test_kontrol_sapmayi_ve_ezilmeyi_yakalar(ev, tmp_path):
    kok = tmp_path / "routerlar"
    for dep in ("guvenlik", "arastirma-ogrenme"):
        skill(kok / f"departman-{dep}", f"departman-{dep}")
    uygula(ev)
    for dep, blok in profil.router_bloklari(ev["veri"], ev["env"]).items():
        profil.router_yaz(kok / f"departman-{dep}/SKILL.md", blok)
    assert profil.kontrol(ev["veri"], ev["env"], [kok]) == []
    d = json.loads(ayar(ev).read_text(encoding="utf-8"))
    del d["skillOverrides"]["graphify"]
    ayar(ev).write_text(json.dumps(d), encoding="utf-8")
    skill(kok / "departman-guvenlik", "departman-guvenlik")  # senkron ezdi
    u = profil.kontrol(ev["veri"], ev["env"], [kok])
    assert any("graphify" in x for x in u) and any("ROUTER" in x and "guvenlik" in x for x in u)
