"""Desktop mcp-server-rea.log: 01:07 sonrasi tools/list yanitinda compare_web_captures inputSchema boyutu + hata satirlari (icerik yazdirmaz)."""
import json, os, re
p = os.path.expandvars(r"%LOCALAPPDATA%\Claude\logs\mcp-server-rea.log")
satir = open(p, encoding="utf-8", errors="replace").read().splitlines()
son = [s for s in satir if s.startswith("2026-10-24T22") or "2026-10-24 01:0" in s or "2026-10-23T22:0" in s]
print("toplam satir", len(satir), "| son blok", len(son))
for s in satir[-400:]:
    if '"tools":[' in s and "compare_web_captures" in s:
        m = re.search(r"(\{.*\})", s)
        try:
            j = json.loads(m.group(1)); j = j.get("message", j)
            t = [x for x in j["result"]["tools"] if x["name"] == "compare_web_captures"][0]
            print(s[:24], "tools/list cwc_bayt=", len(json.dumps(t["inputSchema"], separators=(",", ":"))), "arac=", len(j["result"]["tools"]))
        except Exception as e:
            print(s[:24], "tools/list satiri, uzunluk", len(s), "ayristirilamadi", str(e)[:60])
    elif any(k in s.lower() for k in ("error", "problem", "invalid", "fail")):
        print("  ", s[:200])
