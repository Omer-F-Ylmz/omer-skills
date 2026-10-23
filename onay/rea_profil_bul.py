"""rea-agents paketinde REA_MCP_INPUT_SCHEMA_PROFILE ve 'compact' profil seciminin gectigi dosya/satirlar (kisa)."""
import os
KOK = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node_modules/rea-agents"
print("surum:", open(os.path.join(KOK, "package.json"), encoding="utf-8").read().split('"version"')[1][:20])
for d, alt, fs in os.walk(KOK):
    if "node_modules" in d[len(KOK):]:
        continue
    for f in fs:
        if not f.endswith((".mjs", ".js", ".cjs")):
            continue
        p = os.path.join(d, f)
        try:
            for i, s in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
                if "INPUT_SCHEMA_PROFILE" in s or "inputSchemaProfile" in s:
                    print(os.path.relpath(p, KOK), i, s.strip()[:180])
        except Exception:
            pass
