@echo off
rem KURULUM-11i -- cc-kopru: CC katmanini (CLI allowlist + hook runner + gercek CC
rem oturumu + claude-mem) Desktop sohbetine acan yerel stdio MCP sunucusu.
rem stdout JSON-RPC kanalidir: sunucu disinda tek bayt basilmaz.
rem Desktop yerel MCP sunucularini cwd=C:\Windows\System32 ile baslatir (11f kaniti);
rem TEMP beyaz listede ve yazilabilir.
rem setlocal YOK: 11e'de call'suz .cmd gecisi ortuk endlocal tetikliyordu.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\sunucu.mjs" %*
