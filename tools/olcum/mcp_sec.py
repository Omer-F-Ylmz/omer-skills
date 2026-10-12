"""MCP-HAFIF-1: ölçüm `claude -p` oturumuna yalnız gereken MCP sunucuları (her oturum ~40 user MCP'yi başlatmasın).
Gereken = verilen metinlerdeki (istem, --agents JSON'u, ajan `tools:` alanı, görev tanımı) mcp__<sunucu>__ önekleri;
tanımlar ~/.claude.json mcpServers'tan salt-okunur kopyalanır, gereken yoksa boş config. Bayrak: OLCUM_MCP_HAFIF=0 kapatır."""
import json
import os
import re
from pathlib import Path

ONEK = re.compile(r"mcp__([A-Za-z0-9_.-]+?)(?:__|(?![A-Za-z0-9_.-]))")  # --allowedTools mcp__blender (araçsız) da


def acik():  # MCP-HAFIF-2: KABUL 12/12 eşit → varsayılan açık; OLCUM_MCP_HAFIF=0 tam user MCP
    return os.environ.get("OLCUM_MCP_HAFIF") != "0"


def gereken(*metinler):
    return sorted({a for t in metinler for a in ONEK.findall(str(t))})


def tanimlar(yol=None):
    return json.loads(Path(yol or Path.home() / ".claude.json").read_text(encoding="utf-8")).get("mcpServers", {})


def ek(dizin, *metinler, kaynak=None):
    """Config'i `dizin`e yazar (tanımlarda sır olabilir: geçici, oturum cwd'si dışı) → claude argümanları.
    Bilinmeyen ad (plugin_ önekli vb.) atlanır."""
    t = tanimlar() if kaynak is None else kaynak
    s = {a: t[a] for a in gereken(*metinler) if a in t}
    if "serena" in s:  # arka plan oturumu: dashboard penceresi/tepsi yok, araçlar aynı (Serena CLI bayrağı config'i ezer)
        s["serena"] = {**s["serena"], "args": [*s["serena"].get("args", []), "--enable-web-dashboard", "false"]}
    yol = Path(dizin) / "mcp-hafif.json"
    yol.write_text(json.dumps({"mcpServers": s}), encoding="utf-8")
    return ["--strict-mcp-config", "--mcp-config", str(yol)]


if __name__ == "__main__":
    assert gereken("x mcp__mcp-git__git_status y", '{"tools": "Read, mcp__serena__find_symbol"}') == ["mcp-git", "serena"]
    assert gereken("Read, Grep") == []
    assert gereken('["Bash", "mcp__blender"]', "mcp__plugin_context-mode_context-mode__ctx_x") == [
        "blender", "plugin_context-mode_context-mode"]
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        a = ek(d, "mcp__serena__x mcp__yok__y", kaynak={"serena": {"command": "uvx", "args": ["s"]}, "blender": {}})
        assert json.loads(Path(a[-1]).read_text(encoding="utf-8")) == {
            "mcpServers": {"serena": {"command": "uvx", "args": ["s", "--enable-web-dashboard", "false"]}}}
    print("ok")
