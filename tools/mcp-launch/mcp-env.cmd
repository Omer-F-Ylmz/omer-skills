@echo off
rem Claude Desktop envHelper -- stdout'a tek JSON nesnesi basar.
rem Desktop yerel MCP sunucularini MCP SDK'nin 12 degiskenlik beyaz listesiyle
rem baslatir (app.asar ofset 3899305), bu yuzden ozel anahtarlar surece ulasmaz.
rem Deger yalniz stdout'taki JSON'a girer; ekrana/log'a/hataya yazilmaz.
rem Bu betigin HKCU okumasi, anahtar hijyeni kuralinin TEK istisnasidir.
setlocal enabledelayedexpansion
set DQ=^"
set "OUT="
call :oku BRAVE_API_KEY
call :oku STITCH_API_KEY
if not defined OUT (
  echo mcp-env: BRAVE_API_KEY STITCH_API_KEY - none set in HKCU\Environment 1>&2
  exit /b 1
)
echo {!OUT!}
exit /b 0

:oku
for /f "tokens=2,*" %%a in ('reg query "HKCU\Environment" /v %1 2^>nul ^| findstr /r /c:"REG_[A-Z_]* "') do (
  if not "%%b"=="" (
    if defined OUT set "OUT=!OUT!,"
    set "OUT=!OUT!!DQ!%1!DQ!:!DQ!%%b!DQ!"
  )
)
exit /b 0
