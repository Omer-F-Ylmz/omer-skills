"""RUFLO-2 d2 kanıt: yalnız ruflo içeren --mcp-config ile yeni `claude -p`; gerçek mcp__ruflo__memory_store/retrieve çağrısı (1 çağrı).
python kanit.py  → çıktıda arac satırları + yanıt"""
import json, subprocess, sys
BANKA = "C:/Projeler/omer-skills/.kos/ruflo"
u = json.load(open("C:/Users/pc/.claude.json", encoding="utf-8"))["mcpServers"]["ruflo"]
yol = f"{BANKA}/mcp_yalniz.json"
json.dump({"mcpServers": {"ruflo": {k: u[k] for k in ("command", "args", "env")}}}, open(yol, "w"))
istem = ("mcp__ruflo__memory_store ile key=kanit-d2 value='ruflo d2 kanit' kaydet, sonra mcp__ruflo__memory_retrieve ile geri oku. "
         "Yanıtta yalnız: araç adları ve okunan değer.")
r = subprocess.run(["claude", "-p", istem, "--strict-mcp-config", "--mcp-config", yol, "--allowedTools", "mcp__ruflo", "--output-format", "stream-json",
                    "--verbose", "--max-turns", "6"], capture_output=True, text=True, encoding="utf-8", timeout=300, creationflags=0x08000000)
sys.stdout.reconfigure(encoding="utf-8")
for s in r.stdout.splitlines():
    try:
        j = json.loads(s)
    except ValueError:
        continue
    for b in (j.get("message") or {}).get("content", []) if isinstance(j.get("message"), dict) else []:
        if isinstance(b, dict) and b.get("type") == "tool_use":
            print("ARAC", b["name"], json.dumps(b["input"], ensure_ascii=False)[:120])
        elif isinstance(b, dict) and b.get("type") == "tool_result":
            print("SONUC", str(b.get("content"))[:200])
    if j.get("type") == "result":
        print("YANIT", str(j.get("result"))[:300])
print("rc", r.returncode, r.stderr[-200:])
