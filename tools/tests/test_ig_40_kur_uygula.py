import importlib.util
import json
import subprocess
from pathlib import Path

_s = importlib.util.spec_from_file_location("ig40u", Path(__file__).resolve().parents[2] / "onay" / "ig_40_kur_uygula.py")
ig40u = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ig40u)


def test_uygula_idempotent_geri_yalniz_eklenen(tmp_path, monkeypatch):
    ev = tmp_path / "ev"
    (ev / ".claude" / "plugins").mkdir(parents=True)
    (ev / ".claude.json").write_text(json.dumps({"mcpServers": {"a": {}}}), encoding="utf-8")
    # claude-code-setup önceden kurulu: dokunulmamalı, geri de kaldırmamalı
    (ev / ".claude" / "plugins" / "installed_plugins.json").write_text(
        json.dumps({"plugins": {"claude-code-setup@claude-plugins-official": []}}), encoding="utf-8")
    cagri = []

    def sahte(*a):
        cagri.append(a)
        if a[:2] == ("git", "clone") and a[-1].endswith("/r"):
            (Path(a[-1]) / "skills" / "app-store-screenshots").mkdir(parents=True)
        return subprocess.CompletedProcess(a, 0, "", "")

    monkeypatch.setattr(ig40u, "kos", sahte)
    monkeypatch.setattr(ig40u, "KLON", [("x/y", tmp_path / "klon")])
    assert ig40u.uygula(ev)
    assert ("claude", "plugin", "install", "claude-code-setup@claude-plugins-official") not in cagri
    assert (ev / ".claude" / "skills" / "app-store-screenshots").is_dir()
    eklenen = json.loads(ig40u.bildirim(ev).read_text(encoding="utf-8"))
    assert ["skill", "app-store-screenshots"] in eklenen and len(eklenen) == 6

    # ikinci koşu: skill artık var → yeniden kopyalanmaz (copytree patlamaz)
    assert ig40u.uygula(ev)

    cagri.clear()
    assert ig40u.geri(ev)
    assert not (ev / ".claude" / "skills" / "app-store-screenshots").exists()
    assert ("claude", "plugin", "uninstall", "claude-code-setup@claude-plugins-official") not in cagri
    assert not ig40u.bildirim(ev).exists()
