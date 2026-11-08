@echo off
rem KURULUM-11l K1 -- claude-design artik cc-kopru'nun tasarim.mjs koprusuyle acilir.
rem Eski yol (mcp-remote + OAuth tarayici akisi) claude-design.cmd.bak11l'de duruyor:
rem DCR 405 verdigi icin Desktop'a hic baglanamiyordu. Yeni yol CC'nin kendi yetkili
rem baglantisini `claude -p` ile kullanir; 23 sema tasarim-semalar.json'dan birebir gelir.
rem cd /d "%TEMP%": Desktop cwd'yi C:\Windows\System32 yapiyor, orasi yazilabilir degil.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\tasarim.mjs" %*
