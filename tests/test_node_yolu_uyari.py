import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import node_yolu_uyari as u  # noqa: E402


def _cfg(tmp_path, komut):
    p = tmp_path / "claude.json"
    p.write_text(json.dumps({"mcpServers": {"a": {"command": komut, "args": ["x.js"]}, "b": {"command": "uvx"}}}),
                 encoding="utf-8")
    return str(p)


def test_olmayan_node_yolu_uyari_satiri_yazar(tmp_path):
    assert u.uyari(_cfg(tmp_path, str(tmp_path / "node-v24.19.0-win-x64" / "node.exe"))) == u.UYARI


def test_var_olan_node_yolu_bos_cikti(tmp_path):
    node = tmp_path / "node.exe"
    node.write_bytes(b"")
    assert u.uyari(_cfg(tmp_path, str(node))) == ""
