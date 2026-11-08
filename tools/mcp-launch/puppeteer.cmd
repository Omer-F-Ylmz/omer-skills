@echo off
rem KURULUM-11e/f -- Claude Desktop MCP baslatici.
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem 11f DUZELTME: Desktop yerel MCP sunucularini cwd=C:\Windows\System32 ile baslatir
rem (ize kanitlandi). puppeteer-mcp-server gunlugunu <cwd>\logs altina acmaya calisip
rem yazamayinca sessizce oluyordu. TEMP beyaz listede ve yazilabilir.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Roaming\npm\mcp-server-puppeteer.cmd" %*
