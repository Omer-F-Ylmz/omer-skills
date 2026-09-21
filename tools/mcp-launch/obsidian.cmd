@echo off
rem KURULUM-11g -- Claude Desktop MCP baslatici (Obsidian koprusu).
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem Desktop yalniz stdio tanimi kabul eder; eklenti HTTP+SSE konusur, arasi mcp-remote.
rem 11f kalibi: Desktop yerel MCP sunucularini cwd=C:\Windows\System32 ile baslatir;
rem TEMP 12 degiskenlik beyaz listede ve yazilabilir.
rem 127.0.0.1 zorunlu: eklenti yalniz IPv4 dinler, "localhost" ::1'e cozulebilir.
rem sse-only: eklentide /mcp rotasi yok, mcp-remote varsayilani http-first bos yoklar.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\mcp-remote.cmd" http://127.0.0.1:22360/sse --transport sse-only %*
