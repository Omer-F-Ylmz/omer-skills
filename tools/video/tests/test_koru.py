"""20b koru: ~/.claude parmak izi (settings.json · ~/.claude.json ayar anahtarları · hooks/ · skills/ üst düzey + SKILL.md).
Fark → geri yükle, yalnız ad yazılır (değer yok), rc 1 = DUR. Ağsız; dış süreç sahte `kos`."""
import json
from pathlib import Path

from video.cli import main

from test_kur import KKos
from test_uygula import kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)


def ev_kur(ortam):
    ev = Path(ortam["VIDEO_EV"])
    cl = ev / ".claude"
    (cl / "hooks").mkdir(parents=True)
    (cl / "skills" / "a").mkdir(parents=True)
    (cl / "settings.json").write_text('{"env": {"GIZLI": "deger-xyz"}}', encoding="utf-8")
    (ev / ".claude.json").write_text(json.dumps({"numStartups": 1, "mcpServers": {"m": {"command": "x"}},
                                                 "projects": {"p": {"mcpServers": {}, "sayac": 1}}}), encoding="utf-8")
    (cl / "hooks" / "h.py").write_text("print(1)", encoding="utf-8")
    (cl / "skills" / "a" / "SKILL.md").write_text("a", encoding="utf-8")
    return ev


def test_settings_degisirse_dur_ve_geri_yukle(ortam, kok, capsys):
    ev = ev_kur(ortam)
    assert main(["koru", "--al"], env=ortam, kos=KKos()) == 0
    s = ev / ".claude" / "settings.json"
    once = s.read_bytes()
    s.write_text('{"env": {"GIZLI": "yeni-deger-abc"}}', encoding="utf-8")
    capsys.readouterr()
    assert main(["koru"], env=ortam, kos=KKos()) == 1
    out = capsys.readouterr().out
    assert s.read_bytes() == once
    assert "settings.json" in out and "DUR" in out
    assert "deger-xyz" not in out and "yeni-deger-abc" not in out
    assert main(["koru"], env=ortam, kos=KKos()) == 0
    assert "eşit" in capsys.readouterr().out


def test_yeni_skill_karantinaya_hook_geri(ortam, kok, capsys):
    ev = ev_kur(ortam)
    main(["koru", "--al"], env=ortam, kos=KKos())
    (ev / ".claude" / "skills" / "caveman").mkdir()
    (ev / ".claude" / "skills" / "caveman" / "SKILL.md").write_text("c", encoding="utf-8")
    (ev / ".claude" / "hooks" / "h.py").write_text("print(2)", encoding="utf-8")
    assert main(["koru"], env=ortam, kos=KKos()) == 1
    assert not (ev / ".claude" / "skills" / "caveman").exists()
    assert (kok / "docs" / "denemeler" / ".kos" / "caveman" / "karantina" / "caveman" / "SKILL.md").is_file()
    assert (ev / ".claude" / "hooks" / "h.py").read_text(encoding="utf-8") == "print(1)"
    out = capsys.readouterr().out
    assert "skills/caveman" in out and "hooks/h.py" in out


def test_claude_json_yalniz_ayar_anahtarlari(ortam, kok):
    ev = ev_kur(ortam)
    main(["koru", "--al"], env=ortam, kos=KKos())
    j = ev / ".claude.json"
    d = json.loads(j.read_text(encoding="utf-8"))
    d["numStartups"], d["projects"]["p"]["sayac"] = 7, 9
    j.write_text(json.dumps(d), encoding="utf-8")
    assert main(["koru"], env=ortam, kos=KKos()) == 0
    d["mcpServers"]["caveman"] = {"command": "caveman"}
    d["projects"]["p"]["mcpServers"] = {"c": {}}
    j.write_text(json.dumps(d), encoding="utf-8")
    assert main(["koru"], env=ortam, kos=KKos()) == 1
    s = json.loads(j.read_text(encoding="utf-8"))
    assert s["mcpServers"] == {"m": {"command": "x"}} and s["projects"]["p"]["mcpServers"] == {}
    assert s["numStartups"] == 7 and s["projects"]["p"]["sayac"] == 9


def test_komut_agsiz_env_ve_sonra_karsilastir(ortam, kok):
    ev_kur(ortam)
    main(["koru", "--al"], env=ortam, kos=KKos())
    k = KKos()
    e = {**ortam, "ANTHROPIC_API_KEY": "sk-x", "CLAUDE_CODE_OAUTH_TOKEN": "t", "ANTHROPIC_BASE_URL": "http://127.0.0.1:6767"}
    assert main(["koru", "--agsiz", "--", "caveman", "learn"], env=e, kos=k) == 0
    assert Path(k.cagri[-1][0]).stem.lower() == "caveman" and k.cagri[-1][1:] == ["learn"]
    env = k.env[-1]
    assert "ANTHROPIC_API_KEY" not in env and "CLAUDE_CODE_OAUTH_TOKEN" not in env
    assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:9"


def test_komut_ayari_degistirirse_dur(ortam, kok):
    ev = ev_kur(ortam)
    main(["koru", "--al"], env=ortam, kos=KKos())
    s = ev / ".claude" / "settings.json"

    def yazan(args, timeout=None, env=None):
        s.write_text("{}", encoding="utf-8")
        return 0, b"", b""
    assert main(["koru", "--", "caveman", "claude"], env=ortam, kos=yazan) == 1
    assert "GIZLI" in s.read_text(encoding="utf-8")


def test_once_yoksa_hata(ortam, kok, capsys):
    ev_kur(ortam)
    assert main(["koru"], env=ortam, kos=KKos()) == 1
    assert "--al" in capsys.readouterr().out
