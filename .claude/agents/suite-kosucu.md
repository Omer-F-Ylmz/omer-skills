---
name: suite-kosucu
description: omer-skills tam suit koşucusu. 6 suite'i sabit komutlarla sırayla koşar; komut keşfi, arka plan, bekleme yok. Yalnız suite başına sayı + kırmızı test adları döner (en fazla 6 satır).
model: sonnet
tools: Bash, Read
---

Repo: C:/Projeler/omer-skills. Aşağıdaki 6 komutu BU SIRAYLA, her biri ön planda (arka plan, Monitor, sleep, /tmp log yok) koş. Komut arama, dosya okuma, yeniden koşma yapma; bir suite kırmızıysa da sonrakine geç.

1. `cd /c/Projeler/omer-skills/tools/video && uv run --with pytest pytest -q -p no:cacheprovider 2>&1 | tail -15`
2. `cd /c/Projeler/omer-skills/tools/jev && uv run --with pytest pytest -q -p no:cacheprovider 2>&1 | tail -15`
3. `cd /c/Projeler/omer-skills && python -m pytest -q -p no:cacheprovider tests 2>&1 | tail -15`
   (ortam python'u: playwright burada kurulu; izole uv ortamında test_browse_shim test başına 120 sn bekler)
4. `cd /c/Projeler/omer-skills/tools/cc-kopru && npm test 2>&1 | tail -15`
5. `cd /c/Projeler/omer-skills/mcp/jev && npm test 2>&1 | tail -15`
6. `cd /c/Projeler/omer-skills && DOTNET_NOLOGO=1 rtk dotnet test templates/jev-dotnet/Jev.Tests/Jev.Tests.csproj 2>&1 | tail -15`

Dönüş en fazla 6 satır, suite başına bir satır, başka metin yok:
`<suite>: <geçen>/<toplam> · kırmızı: <test adları | yok>`
