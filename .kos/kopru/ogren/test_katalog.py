"""Sahte ağaç fikstürü: python -m pytest test_katalog.py"""
import json, sys, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import katalog


def _yaz(p, metin):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(metin, encoding="utf-8")


def test_sahte_agac(tmp_path):
    ev, repo, proj = tmp_path / "ev", tmp_path / "proj/omer-skills", tmp_path / "proj"
    sk = "---\nname: tok-sikistir\ndescription: >\n  Token bağlam sıkıştırma. İkinci cümle.\n---\n# T\n"
    _yaz(ev / ".claude/skills/tok-sikistir/SKILL.md", sk)
    _yaz(repo / "skills/tok-sikistir/SKILL.md", sk)  # aynı içerik -> kopya grubu
    _yaz(ev / ".claude/agents/blend.md", "---\nname: blend\ndescription: Blender mesh onarır\n---\n")
    pk = tmp_path / "pk"
    _yaz(pk / ".claude-plugin/plugin.json", json.dumps({"description": "Playwright test eklentisi"}))
    _yaz(pk / "commands/kos.md", "Testleri koşar.\n")
    _yaz(pk / "hooks/hooks.json", json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"command": "C:/x/py.exe gizli=ABC"}]}]}}))
    _yaz(pk / ".mcp.json", json.dumps({"mcpServers": {"pw": {"command": "npx", "env": {"K": "GIZLI"}}}}))
    _yaz(ev / ".claude/plugins/installed_plugins.json", json.dumps({"plugins": {"pwt@m": [{"installPath": str(pk)}]}}))
    _yaz(ev / ".claude.json", json.dumps({"mcpServers": {"jev": {"command": "C:/a/jev.exe", "env": {"T": "GIZLI"}}}}))
    (repo / "dist/claude-ai-1").mkdir(parents=True)
    with zipfile.ZipFile(repo / "dist/claude-ai-1/paket.zip", "w") as z:
        z.writestr("paket/a/SKILL.md", "---\nname: a\ndescription: PDF belge üretir\n---\n")
        z.writestr("paket/b/SKILL.md", "---\nname: b\ndescription: SEO pazarlama\n---\n")
    _yaz(proj / ".tmp-video/klon1/README.md", "# Klon Bir\n\nVideo kırpar. Detay.\n")
    _yaz(proj / ".tmp-video/klon1/LICENSE", "MIT")
    _yaz(repo / "docs/atlas/kart.jsonl", json.dumps({"ad": "blend"}) + "\n")
    _yaz(repo / "docs/kurulumlar/kacan-karar.tsv", "parti\tvideo\tkaynak\tterim\tkarar\tsebep\n1\tv\tp\tfoo\taday\tx\n1\tv\tp\tlearn\tkapat\ty\n")
    omni = tmp_path / "omni.json"
    omni.write_text(json.dumps([{"id": "x/vis:free", "owned_by": "openrouter", "capabilities": {"vision": True}}]))

    kalemler, kapat = katalog.topla(ev, repo, proj, omni, tmp_path / "yok.json", cli=False)
    ad = {(k["tur"], k["ad"], k["kaynak"]): k for k in kalemler}

    a = ad[("skill", "tok-sikistir", "cc-skills")]
    assert a["aciklama"] == "Token bağlam sıkıştırma. İkinci cümle."
    assert a["kategori_tahmin"] == "token" and a["kopya_grubu"].startswith("h:")
    assert ad[("agent", "blend", "cc-agents")]["atlasta"] and ad[("agent", "blend", "cc-agents")]["kategori_tahmin"] == "3d"
    assert ("skill", "a", "dist:claude-ai-1") in ad and ("skill", "b", "dist:claude-ai-1") in ad  # paket içi ayrı satır
    assert ad[("skill", "b", "dist:claude-ai-1")]["kategori_tahmin"] == "pazarlama"
    assert ad[("plugin", "pwt", "plugins")]["kategori_tahmin"] == "test-qa"
    assert ("komut", "kos", "plugin:pwt@m") in ad
    r = ad[("repo", "klon1", "indirme:.tmp-video")]
    assert r["lisans"] == "LICENSE" and r["aciklama"].startswith("Klon Bir · Video kırpar.")
    assert ad[("model", "x/vis:free", "omniroute:openrouter")]["free"]
    assert ("aday", "foo", "video:kacan-karar") in ad and kapat == 1
    metin = json.dumps(kalemler, ensure_ascii=False)
    assert "GIZLI" not in metin and "gizli=ABC" not in metin  # env/argüman değeri sızmaz
    assert len(katalog.ozet(kalemler, kapat).splitlines()) <= 60
