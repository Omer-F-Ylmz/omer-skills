import json, os, sys
sys.path[:0] = [r"C:\Projeler\omer-skills\.claude", r"C:\Projeler\omer-skills\tools\olcum"]
import t7f2, kosucu
t7f2.vekil(); os.environ["T7F2_ETIKET"] = "web-" + sys.argv[1]
ist = "Yalnız şu MCP araçlarını sırayla çağır: mcp__mcp-fetch__fetch ile https://example.com getir; mcp__context7__resolve-library-id ile 'react' ara; mcp__brave-search__brave_web_search ile 'anthropic' ara. Her biri için 'ad: ok/hata' yaz."
ek = t7f2.birlesik_ek() if sys.argv[1] == "birlesik" else t7f2.ayar("false")
o = kosucu.kos(ist, ek=ek, model="haiku", butce=0.4, timeout=300)
mc = [a for a in o["araclar"] if a.startswith("mcp__")]
print(sys.argv[1], "mcp_cagri", mc, "usd", round(o["usd"], 4), "rc", o["rc"], "|", o["metin"][-300:].replace("\n", " "))
