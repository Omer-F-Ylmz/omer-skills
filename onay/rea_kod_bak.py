K = r"C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node_modules/rea-agents/dist/"
PARCA = [("server/createServer.js", 355, 392), ("config/mcpInputSchemaProfile.js", 1, 40)]
for dosya, bas, bit in PARCA:
    print("##", dosya, bas, bit)
    for i, s in enumerate(open(K + dosya, encoding="utf-8", errors="replace"), 1):
        if bas <= i <= bit:
            print(i, s.rstrip()[:200])
