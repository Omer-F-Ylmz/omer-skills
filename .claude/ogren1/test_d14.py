"""d14 (a) kaynak çözümü: kanca → kayıt + çağrılan betiğin tam metni; repo dizini → kök belge/manifest (alt skill değil). (c) token-dışı kapalı listede"""
import json

from d14 import metin
from ozet3 import gecerli_b


def test_kanca_betik_metni(tmp_path):
    (tmp_path / "hooks").mkdir()
    (tmp_path / "hooks" / "routing.mjs").write_text("// fail-open when MCP not ready\n", encoding="utf-8")
    h = {"hooks": {"PreToolUse": [{"matcher": "WebFetch", "hooks": [{"type": "command", "command": 'node "${CLAUDE_PLUGIN_ROOT}/hooks/routing.mjs"'}]},
                                  {"matcher": "Bash", "hooks": [{"type": "command", "command": "echo baska"}]}]}}
    (tmp_path / "hooks" / "hooks.json").write_text(json.dumps(h), encoding="utf-8")
    m = metin("PreToolUse:WebFetch", str(tmp_path / "hooks" / "hooks.json"))
    assert "fail-open when MCP not ready" in m and "routing.mjs" in m and "echo baska" not in m


def test_eslesiyicisiz_kanca_degiskenli_yol(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "worker.cjs").write_text("// flush on stop\n", encoding="utf-8")
    h = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": '_P="${CLAUDE_PLUGIN_ROOT}"; node "$_P/scripts/worker.cjs" hook stop'}]}]}}
    (tmp_path / "hooks").mkdir()
    (tmp_path / "hooks" / "hooks.json").write_text(json.dumps(h), encoding="utf-8")
    assert "flush on stop" in metin("Stop:*", str(tmp_path / "hooks" / "hooks.json"))


def test_zip_ic_yol(tmp_path):
    import zipfile
    with zipfile.ZipFile(tmp_path / "s.zip", "w") as z:
        z.writestr("omni/cli-chat/SKILL.md", "# cli-chat\n")
    assert metin("cli-chat", f"{tmp_path / 's.zip'}!cli-chat/SKILL.md") == "# cli-chat\n"


def test_repo_kok_belge_alt_skill_degil(tmp_path):
    (tmp_path / "package.json").write_text('{"name": "claude-mem"}', encoding="utf-8")
    (tmp_path / "skills" / "baska").mkdir(parents=True)
    (tmp_path / "skills" / "baska" / "SKILL.md").write_text("# agent-cost-report\n", encoding="utf-8")
    m = metin("claude-mem", str(tmp_path))
    assert '"name": "claude-mem"' in m and "agent-cost-report" not in m


def test_claude_json_yalniz_kendi_kaydi_gizli_maskeli(tmp_path):
    j = {"oauthAccount": "x", "mcpServers": {"serena": {"command": "uvx", "args": ["--from", "serena"], "env": {"K": "sk-gizli"}},
                                             "baska": {"command": "npx", "headers": {"Authorization": "Bearer gizli2"}}}}
    (tmp_path / ".claude.json").write_text(json.dumps(j), encoding="utf-8")
    m = metin("serena", str(tmp_path / ".claude.json"))
    assert '"uvx"' in m and "sk-gizli" not in m and "<gizli>" in m and "oauthAccount" not in m and "gizli2" not in m


def test_token_disi_kapali_listede():
    m = "Binds a custom domain to the deployed site for routing."
    assert gecerli_b({"mekanizma": ["token-dışı"], "kanit": "Binds a custom domain to the deployed site"}, m)
