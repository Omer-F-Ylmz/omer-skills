@echo off
rem KURULUM-11k K5 -- kanca gecidi sarmalayicisi (mcp-git).
rem Yazan git araclari (commit/add/reset/checkout/create_branch/init) Bash matcher'ina
rem eslenir; block-destructive gibi PreToolUse hook'lari komut satirini gorur.
rem Salt okur git araclari (status/log/diff/show/branch) eslenmez, dokunulmadan iletilir.
cd /d "%TEMP%"
"C:\Program Files\nodejs\node.exe" "C:\Projeler\omer-skills\tools\cc-kopru\gecit.mjs" mcp-git -- "C:\Users\pc\.local\bin\mcp-server-git.exe"
