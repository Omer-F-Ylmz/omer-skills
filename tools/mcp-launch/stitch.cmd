@echo off
rem KURULUM-11e -- Claude Desktop MCP baslatici.
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem Anahtar HKCU'dan okunur, hicbir yere basilmaz (11b anahtar hijyeni istisnasi).
rem setlocal YOK: son satir call'suz baska bir .cmd'ye gecer, bu da ortuk endlocal
rem tetikler ve degiskeni npm shim'e ulasmadan siler. Degisken bu cmd surecinde kalir.
for /f "tokens=2,*" %%a in ('reg query "HKCU\Environment" /v STITCH_API_KEY 2^>nul ^| findstr /r /c:"REG_[A-Z_]* "') do set "STITCH_API_KEY=%%b"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\stitch-mcp.cmd" proxy %*
