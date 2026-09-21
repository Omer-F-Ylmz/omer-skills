@echo off
rem KURULUM-11k K7 -- claude-design MCP'si Desktop'a (obsidian kalibi).
rem Ucta OAuth var: kimliksiz POST 401 + www-authenticate: Bearer resource_metadata=...
rem Statik anahtar yok; mcp-remote tarayici akisini yurutur, jetonu ~/.mcp-auth'ta tutar.
rem cd /d "%TEMP%": Desktop cwd'yi C:\Windows\System32 yapiyor, orasi yazilabilir degil.
cd /d "%TEMP%"
"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\mcp-remote.cmd" https://api.anthropic.com/v1/design/mcp --transport http-only %*
