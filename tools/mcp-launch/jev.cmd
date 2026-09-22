@echo off
rem KURULUM-13a K4b -- jev MCP yedek baslaticisi (Desktop config'ine GIRMEZ: uzak connector hesapla gelir).
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem Anahtar (OPENROUTER_API_KEY / TYPESAFE_API_KEY) cmd /c ortam mirasiyla gelir; Desktop SDK beyaz listesi
rem onu tasimaz, baglanirsa config "env" blogu gerekir. Dosya anahtar okumaz, basmaz.
rem cd /d "%TEMP%": Desktop cwd'si C:\Windows\System32. setlocal YOK (11e dersi).
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe" "C:\Projeler\omer-skills\mcp\jev\dist\stdio.js" %*
