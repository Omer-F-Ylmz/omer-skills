r"""MCP RAM ölçümü (9 Kas 2026): her MCP süreç ağacını istemciye (Desktop / CC / havuz / köprü-cc) ve türe
(gercek sunucu / hafif kopru) ayırır. 'Desktop x4' sayısının köprü mü gerçek kopya mı olduğunu gösterir.
  python -I tools/ram/mcp_olcum.py"""
import sys
from collections import defaultdict

import psutil

ADLAR = ["server-filesystem", "playwright", "puppeteer", "claude-mem", "chroma", "gecit", "obsidian", "tasarim", "rea-mcp",
         "hostinger", "code-mode", "mcp-server-git", "markitdown", "clickhouse", "headroom.exe mcp", "hermes", "blender",
         "arxiv", "code-review", "mcp-server-fetch", "sequential", "mcp-time", "memory", "xerj", "ruflo", "brave", "context7",
         "binlog", "arac-ara", "stitch", "omniroute", "gsc_server", "mcp-proxy", "airtable", "apify", "n8n", "netlify", "jev"]


def cmd(p):
    try:
        return " ".join(p.cmdline())
    except psutil.Error:
        return ""


def istemci(p):
    try:
        for a in p.parents():
            n, c = (a.name() or "").lower(), cmd(a)
            if "mcp-proxy" in c or "mcp_paylasim" in c:
                return "havuz"
            if n == "claude.exe":
                return "Desktop" if "WindowsApps" in c or "AnthropicClaude" in c else "CC"
            if "cc-kopru" in c.lower():
                return "kopru"
    except psutil.Error:
        pass
    return "sahipsiz"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    g = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for p in psutil.process_iter(["name"]):
        n = (p.info["name"] or "").lower()
        if n not in ("node.exe", "python.exe", "pythonw.exe", "uv.exe", "uvx.exe", "headroom.exe", "npx.exe", "bun.exe"):
            continue
        c = cmd(p).lower()
        tur = "kopru" if "mcp_koprusu" in c else "gercek"
        ad = next((k for k in ADLAR if k in c), None)
        if not ad:
            continue
        try:
            ust = p.parent()
            if ust and ad in cmd(ust).lower() and (ust.name() or "").lower() in ("node.exe", "python.exe", "pythonw.exe", "uv.exe", "uvx.exe", "npx.exe"):
                continue
            rss = sum(q.memory_info().rss for q in [p] + p.children(recursive=True))
        except psutil.Error:
            continue
        k = g[ad][(istemci(p), tur)]
        k[0] += 1
        k[1] += rss
    top, topk = 0, defaultdict(int)
    for ad, d in sorted(g.items(), key=lambda t: -sum(v[1] for v in t[1].values())):
        mb = sum(v[1] for v in d.values()) // 2**20
        top += mb
        for (i, t), v in d.items():
            topk[f"{i}/{t}"] += v[1] // 2**20
        print(f"{ad:20} {mb:5} MB  " + "  ".join(f"{i}/{t}:x{v[0]}={v[1] // 2**20}MB" for (i, t), v in d.items()))
    print(f"\nTOPLAM {top} MB | " + " | ".join(f"{k} {v} MB" for k, v in sorted(topk.items(), key=lambda t: -t[1])))
    print(f"RAM %{psutil.virtual_memory().percent}")


if __name__ == "__main__":
    main()
