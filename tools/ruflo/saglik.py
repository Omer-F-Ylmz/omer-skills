"""Ruflo MCP sağlık: filtreli araç listesi + bellek yaz/oku/ara + öğrenme (agentdb pattern) gerçek çağrıları."""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
SECIM = ("memory_store,memory_retrieve,memory_search,memory_list,memory_delete,memory_stats,agentdb_health,agentdb_pattern-store,"
         "agentdb_pattern-search,agentdb_feedback,hooks_intelligence_pattern-store,hooks_intelligence_pattern-search,"
         "hooks_intelligence_learn,hooks_intelligence_stats")
os.environ["CLAUDE_FLOW_MCP_TOOLS"] = SECIM
import mcp_dene  # noqa: E402


def cagri(ad, **a):
    return ("tools/call", {"name": ad, "arguments": a})


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.time()
    c = [("tools/list", {}),
         cagri("memory_store", key="ruflo2-saglik", value="CC'de MCP bellek yazma denemesi", namespace="ruflo2", tags=["deneme"]),
         cagri("memory_retrieve", key="ruflo2-saglik", namespace="ruflo2"),
         cagri("memory_search", query="MCP bellek yazma", namespace="ruflo2"),
         cagri("agentdb_pattern-store", pattern="test koşulu -> önce kırmızı gör -> kanıt: pytest rc1", type="ders", confidence=0.8),
         cagri("agentdb_pattern-search", query="kırmızı test", topK=3),
         cagri("agentdb_health")]
    o, _ = mcp_dene.kos(c)
    print(len(o[2]["result"]["tools"]), "araç", round(time.time() - t0, 1), "sn")
    for k in range(3, 9):
        print(k, json.dumps(o.get(k), ensure_ascii=False)[:400])
