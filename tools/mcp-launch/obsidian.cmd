@echo off
rem KURULUM-11m-A K1 -- Claude Desktop MCP baslatici (Obsidian koprusu).
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem 11g'de mcp-remote dogrudan uca baglaniyordu: Obsidian kapaliyken initialize hic
rem donmuyor, Desktop sunucuyu dusmus sayiyor, Obsidian sonradan acilsa bile Desktop
rem yeniden baslatilana kadar arac gorunmuyordu. obsidian.mjs acilista baglanmaz;
rem SSE istemcisi SDK'nin kendisinde (mcp-remote katmani dustu).
rem Desktop yerel MCP sunucularini cwd=System32 ile baslatir (11f kaniti).
cd /d "%TEMP%"
"C:\Program Files\nodejs\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\obsidian.mjs" %*
