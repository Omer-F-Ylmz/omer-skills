@echo off
rem KURULUM-11k K5 -- kanca gecidi sarmalayicisi (mcp-filesystem).
rem Desktop cagrisi once gecit.mjs'ten gecer: CC'nin PreToolUse/PostToolUse hook'lari
rem ve permissions.deny Read kurallari uygulanir, sonra GERCEK sunucuya iletilir.
rem stdout JSON-RPC kanalidir; gecit gunlugu stderr'e yazar.
rem cd /d "%TEMP%": Desktop yerel MCP sunucularini cwd=C:\Windows\System32 ile baslatir.
cd /d "%TEMP%"
"C:\Program Files\nodejs\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\gecit.mjs" mcp-filesystem -- "C:\Program Files\nodejs\node.exe" "C:\AI\mcp\mcp-filesystem\node_modules\@modelcontextprotocol\server-filesystem\dist\index.js" C:/Users/pc/Desktop C:/Projeler
