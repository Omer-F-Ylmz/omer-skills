@echo off
rem KURULUM-11k K5 -- kanca gecidi sarmalayicisi (mcp-filesystem).
rem Desktop cagrisi once gecit.mjs'ten gecer: CC'nin PreToolUse/PostToolUse hook'lari
rem ve permissions.deny Read kurallari uygulanir, sonra GERCEK sunucuya iletilir.
rem stdout JSON-RPC kanalidir; gecit gunlugu stderr'e yazar.
rem cd /d "%TEMP%": Desktop yerel MCP sunucularini cwd=C:\Windows\System32 ile baslatir.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\gecit.mjs" mcp-filesystem -- "%ComSpec%" /d /s /c "C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\npx.cmd" -y @modelcontextprotocol/server-filesystem@2026.8.31 C:/Users/pc/Desktop C:/Projeler
