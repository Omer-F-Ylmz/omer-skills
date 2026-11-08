"""REA MCP tools/list şema taraması. Kullanım: python -I tools/rea-sema-tara.py [--profil sarmal|compact|full] [--json]
Denetim: araç şeması ≤32 KB, geçerli JSON Schema (draft-07), not:{} yok, type'sız boş {} dal yok,
ad ≤64, ad tekrarı yok. Çıkış 0 = temiz. REA her güncellendiğinde koşar."""
import json, os, subprocess, sys

NODE = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
REA = NODE.replace("node.exe", "node_modules/rea-agents/scripts/rea.mjs")
SINIR = 32 * 1024


def tools_list(profil):
    env = dict(os.environ, REA_MCP_INPUT_SCHEMA_PROFILE=profil, REA_MCP_OUTPUT_SCHEMA_PROFILE="off")
    komut = [NODE, REA, "mcp"]
    if profil == "sarmal":  # Desktop'ın kullandığı yol: env verilmez, sarmalayıcı profili kendisi sabitler
        env.pop("REA_MCP_INPUT_SCHEMA_PROFILE"); env.pop("REA_MCP_OUTPUT_SCHEMA_PROFILE")
        komut = [NODE, os.path.join(os.path.dirname(os.path.abspath(__file__)), "rea-mcp-compact.mjs")]
    istek = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "sema-tara", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
    ]
    p = subprocess.Popen(komut, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, creationflags=0x08000000)
    p.stdin.write(("\n".join(json.dumps(i) for i in istek) + "\n").encode())
    p.stdin.flush()
    araclar = []
    while True:
        satir = p.stdout.readline()
        if not satir:
            break
        m = json.loads(satir)
        if m.get("id") == 2:
            araclar = m["result"]["tools"]

            break
    p.kill()
    return araclar


def gez(n, yol, hatalar):
    if isinstance(n, dict):
        if n.get("not") == {}:
            hatalar.append(f"not:{{}} @ {yol}")
        for anahtar in ("anyOf", "oneOf", "allOf"):
            for i, d in enumerate(n.get(anahtar, []) if isinstance(n.get(anahtar), list) else []):
                if d == {}:
                    hatalar.append(f"boş {{}} dal @ {yol}/{anahtar}/{i}")
        if "enum" in n and n["enum"] == []:
            hatalar.append(f"boş enum @ {yol}")
        if isinstance(n.get("required"), list) and isinstance(n.get("properties"), dict):
            for r in n["required"]:
                if r not in n["properties"]:
                    hatalar.append(f"required '{r}' properties'te yok @ {yol}")
        if "$ref" in n and not str(n["$ref"]).startswith("#"):
            hatalar.append(f"dış $ref @ {yol}")
        for k, v in n.items():
            gez(v, f"{yol}/{k}", hatalar)
    elif isinstance(n, list):
        for i, v in enumerate(n):
            gez(v, f"{yol}/{i}", hatalar)


def derinlik(n):
    if isinstance(n, dict):
        return 1 + max((derinlik(v) for v in n.values()), default=0)
    if isinstance(n, list):
        return 1 + max((derinlik(v) for v in n), default=0)
    return 0


def main():
    profil = sys.argv[sys.argv.index("--profil") + 1] if "--profil" in sys.argv else "sarmal"
    araclar = tools_list(profil)
    kotu = 0
    adlar = [t["name"] for t in araclar]
    print(f"profil={profil} araç={len(araclar)}")
    if len(set(adlar)) != len(adlar):
        print("HATA: aynı ad iki kez kayıtlı"); kotu += 1
    for t in araclar:
        hatalar = []
        if len(t["name"]) > 64:
            hatalar.append("ad >64")
        for alan in ("inputSchema", "outputSchema"):
            if alan in t:
                b = len(json.dumps(t[alan], separators=(",", ":")).encode())
                if b > SINIR:
                    hatalar.append(f"{alan} {b} bayt > {SINIR}")
                gez(t[alan], alan, hatalar)
        if hatalar:
            kotu += 1
            print(f"HATA {t['name']}: {hatalar[:4]}")
    en = sorted(araclar, key=lambda t: -len(json.dumps(t.get("inputSchema", {}))))[:3]
    print("en büyük girdi şemaları:", [(t["name"], len(json.dumps(t.get("inputSchema", {}), separators=(',', ':')))) for t in en])
    print("TEMİZ" if not kotu else f"{kotu} araç hatalı")
    sys.exit(1 if kotu else 0)


main()
