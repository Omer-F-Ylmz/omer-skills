import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gsd_catal as G  # noqa: E402


def _h(e, ad, matcher=None):
    m = {"hooks": [{"type": "command", "command": f'node "${{CLAUDE_PLUGIN_ROOT}}/hooks/{ad}.js"'}]}
    return e, ({"matcher": matcher, **m} if matcher else m)


def sahte(k: Path):
    (k / ".claude-plugin").mkdir(parents=True)
    (k / ".claude-plugin" / "plugin.json").write_text(json.dumps({"name": "gsd-core", "version": "1.16.0", "commands": "./commands/gsd/", "skills": "./skills/"}))
    (k / ".claude-plugin" / "marketplace.json").write_text(json.dumps({"name": "gsd-core", "plugins": [{"name": "gsd-core", "version": "1.16.0", "source": "./"}]}))
    (k / "LICENSE").write_text("MIT License")
    for ad, acik in (("gsd-plan-phase", "Create detailed phase plan"), ("gsd-debug", "Systematic debugging")):
        (k / "skills" / ad).mkdir(parents=True)
        (k / "skills" / ad / "SKILL.md").write_text(f'---\nname: {ad}\ndescription: "{acik}"\n---\n<objective>{ad} gövde</objective>\n', encoding="utf-8")
    (k / "commands" / "gsd").mkdir(parents=True); (k / "commands" / "gsd" / "plan-phase.md").write_text("x")
    (k / "agents").mkdir(); (k / "agents" / "gsd-planner.md").write_text("---\nname: gsd-planner\n---\nrol")
    hooks = {}
    for e, m in (_h("SessionStart", "gsd-ensure-canonical-path"), _h("SessionStart", "gsd-check-update"),
                 _h("PreToolUse", "gsd-read-guard", "Write|Edit"), _h("PreToolUse", "gsd-write-guard", "Write"),
                 _h("PreToolUse", "gsd-secret-read-guard", "Read|Grep|Bash"), _h("PostToolUse", "gsd-context-monitor", "Bash|Edit"),
                 _h("PostToolUse", "gsd-read-injection-scanner", "Read|WebFetch|WebSearch"), _h("Stop", "gsd-context-monitor"),
                 _h("FileChanged", "gsd-config-reload", "config.json")):
        hooks.setdefault(e, []).append(m)
    (k / "hooks").mkdir(); (k / "hooks" / "hooks.json").write_text(json.dumps({"hooks": hooks}))


def test_catal(tmp_path):
    sahte(tmp_path)
    G.catal(tmp_path, "651bd2f")
    # liste: tek skill girişi, komut yok, ajan yok (auto-discovery dışında)
    assert [p.name for p in (tmp_path / "skills").iterdir()] == ["gsd"]
    assert not (tmp_path / "commands").exists() and not (tmp_path / "agents").exists()
    assert (tmp_path / "ajanlar" / "gsd-planner.md").read_text() == "---\nname: gsd-planner\n---\nrol"
    # içerik korunur: alt komut dosyası birebir
    alt = tmp_path / "skills" / "gsd" / "alt" / "plan-phase.md"
    assert "gsd-plan-phase gövde" in alt.read_text(encoding="utf-8")
    sk = (tmp_path / "skills" / "gsd" / "SKILL.md").read_text(encoding="utf-8")
    acik = sk.split("description:", 1)[1].split("\n", 1)[0]
    assert len(acik) <= 260 and "plan-phase — Create detailed phase plan" in sk and "ajanlar/" in sk
    pj = json.loads((tmp_path / ".claude-plugin" / "plugin.json").read_text())
    assert "commands" not in pj and pj["version"] == "1.16.0-omer.1"
    mj = json.loads((tmp_path / ".claude-plugin" / "marketplace.json").read_text())
    assert mj["name"] == "gsd-core-omer" and mj["plugins"][0]["version"] == "1.16.0-omer.1"
    # hook'lar: yalnız seçilenler, injection tarayıcı yalnız dış içerik
    hj = json.loads((tmp_path / "hooks" / "hooks.json").read_text())["hooks"]
    kalan = {(e, h["command"].split("/hooks/")[1][:-4], m.get("matcher")) for e, L in hj.items() for m in L for h in m["hooks"]}
    assert kalan == {("SessionStart", "gsd-ensure-canonical-path", None), ("PreToolUse", "gsd-write-guard", "Write"), ("PreToolUse", "gsd-secret-read-guard", "Read|Grep|Bash"),
                     ("PostToolUse", "gsd-read-injection-scanner", "WebFetch|WebSearch"), ("FileChanged", "gsd-config-reload", "config.json")}
    atif = (tmp_path / "ATIF.md").read_text(encoding="utf-8")
    assert "MIT" in atif and "651bd2f" in atif and (tmp_path / "LICENSE").exists()
