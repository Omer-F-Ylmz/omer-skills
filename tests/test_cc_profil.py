"""TOKEN-1 K2: tools/cc_profil.py — `claude -p` arka plan profili; yalnız başlatma argümanı üretir."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import cc_profil  # noqa: E402

SENTINEL = "${CC_PROFIL_SENTINEL_X}"
JEV = Path.home() / ".claude" / "hooks" / "jev-skill.ps1"
BAZ = KOK / "tests" / "veri" / "jev-skill.baz.ps1"
KORUMA = "if ($env:CC_PROFIL) { exit 0 }"


@pytest.fixture
def kur(tmp_path, monkeypatch):
    monkeypatch.setenv("CC_PROFIL_SENTINEL_X", "SIZMAMALI")
    ana = tmp_path / "claude.json"
    ana.write_text(json.dumps({"mcpServers": {
        "blender": {"command": "uvx", "args": ["blender-mcp"], "env": {"ANAHTAR": SENTINEL}},
        "headroom": {"type": "http", "url": "http://127.0.0.1:1/mcp"},
        "github": {"command": "x"}}}), encoding="utf-8")
    sk = []
    for ad in ("a", "b"):
        (tmp_path / ad).mkdir()
        sk.append(tmp_path / ad / "SKILL.md")
        sk[-1].write_text(f"# {ad} skill\ngövde {ad}", encoding="utf-8")
    pr = tmp_path / "profil.json"
    pr.write_text(json.dumps({
        "tam": {}, "ttl": {"ttl": "5m"},
        "is": {"mcp": ["blender", "headroom"], "skills": [str(s) for s in sk], "pluginKapat": ["claude-mem@x", "ponytail@y"], "ttl": "5m"},
        "mcpyok": {"mcp": ["yok"], "ttl": "5m"},
        "skillyok": {"skills": [str(tmp_path / "yok" / "SKILL.md")], "ttl": "5m"},
    }), encoding="utf-8")
    return lambda ad, env=None, **k: cc_profil.kur(ad, env=env or {}, ana=ana, profiller=pr, gecici=tmp_path / "gecici", **k)


def _d(args, bayrak):
    return args[args.index(bayrak) + 1]


def _ayar(args):
    assert args.count("--settings") == 1
    return json.loads(_d(args, "--settings"))


def test_tam_ek_arguman_uretmez(kur):
    assert kur("tam") == ([], {})


def test_strict_ve_yalniz_listelenen_mcp(kur):
    args, _ = kur("is")
    assert "--strict-mcp-config" in args
    assert set(json.loads(Path(_d(args, "--mcp-config")).read_text(encoding="utf-8"))["mcpServers"]) == {"blender", "headroom"}


def test_var_referansi_acilmaz(kur):
    metin = Path(_d(kur("is")[0], "--mcp-config")).read_text(encoding="utf-8")
    assert SENTINEL in metin and "SIZMAMALI" not in metin


def test_disable_slash_commands_yalniz_skill_profilinde(kur):
    assert "--disable-slash-commands" in kur("is")[0]
    assert "--disable-slash-commands" not in kur("ttl")[0]


def test_settings_hook_kapatmaz(kur):
    for ad in ("ttl", "is"):
        args, _ = kur(ad)
        s = _ayar(args)
        assert "disableAllHooks" not in s and "hooks" not in s
        assert "disableAllHooks" not in " ".join(args) and "--bare" not in args and "--safe-mode" not in args


def test_enabledplugins_yalniz_listedekiler(kur):
    assert _ayar(kur("is")[0])["enabledPlugins"] == {"claude-mem@x": False, "ponytail@y": False}
    assert "enabledPlugins" not in _ayar(kur("ttl")[0])


def test_ttl_5m(kur):
    for ad in ("ttl", "is"):
        assert _ayar(kur(ad)[0])["promptCacheTtl"] == "5m"


def test_bilinmeyen_profil_hata(kur):
    with pytest.raises(ValueError):
        kur("uydurma")


def test_bilinmeyen_mcp_hata(kur):
    with pytest.raises(ValueError, match="yok"):
        kur("mcpyok")


def test_eksik_skill_dosyasi_hata(kur):
    with pytest.raises(FileNotFoundError):
        kur("skillyok")


def test_zorla_tam_geri_alir(kur):
    assert kur("is", env={"CC_PROFIL_ZORLA": "tam"}) == ([], {})


def test_skill_dosyalari_tek_dosyada_ve_sabit(kur):
    a1, a2 = kur("is")[0], kur("is")[0]
    m1 = Path(_d(a1, "--append-system-prompt-file")).read_text(encoding="utf-8")
    assert "# a skill" in m1 and "# b skill" in m1
    assert m1 == Path(_d(a2, "--append-system-prompt-file")).read_text(encoding="utf-8")


def test_ttl_deney_kosulunu_degistirmez(kur):
    args, env = kur("ttl")
    assert args == ["--settings", json.dumps({"promptCacheTtl": "5m"})] and env == {}
    assert kur("is")[1] == {"CC_PROFIL": "is"}


def test_ek_ayar_tek_settings_icinde(kur):
    s = _ayar(kur("ttl", ek_ayar={"env": {"A": "1"}})[0])
    assert s == {"env": {"A": "1"}, "promptCacheTtl": "5m"}
    assert kur("tam", ek_ayar={"env": {"A": "1"}}) == (["--settings", json.dumps({"env": {"A": "1"}})], {})


def test_gercek_profiller_gecerli(tmp_path):
    for ad in json.loads(cc_profil.PROFIL.read_text(encoding="utf-8")):
        cc_profil.kur(ad, env={}, gecici=tmp_path)


def _jev(env_ek):
    env = {k: v for k, v in os.environ.items() if k != "CC_PROFIL"} | env_ek
    return subprocess.run(["powershell.exe", "-NoProfile", "-File", str(JEV)], input='{"prompt":"blender fincan"}',
                          capture_output=True, text=True, env=env, timeout=30)


def test_jev_skill_cc_profil_varken_bos():
    r = _jev({"CC_PROFIL": "blender"})
    assert r.returncode == 0 and r.stdout == ""


def test_jev_skill_cc_profil_yokken_ayni():
    satir = JEV.read_text(encoding="utf-8-sig").splitlines()
    assert KORUMA in satir and satir.index(KORUMA) < next(i for i, s in enumerate(satir) if "ReadToEnd" in s)
    assert [s for s in satir if s != KORUMA] == BAZ.read_text(encoding="utf-8-sig").splitlines()
