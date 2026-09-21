<#
  KURULUM-11l K4 — permissions.deny'a ic ice bin/obj kurallari.

  Acik: `Read(./bin/**)` kalibi proje KOKUNDEN cozuluyor (kos.mjs::okumaDeny), bu yuzden
        ic ice bir bin disarida kaliyor. Olcum: Corvano.Web\bin\Debug\net10.0\
        Corvano.Web.runtimeconfig.json hem CC'de hem kopru gecitinden OKUNDU.

  Eklenen: Read(**/bin/Debug/**) · Read(**/bin/Release/**) · Read(**/obj/**)
  Korunan: Read(./bin/**) · Read(./obj/**) (proje koku kurallari silinmez)
  EKLENMEYEN: Read(**/bin/**) — gstack skill'inin kendi bin/ komut dizinlerini
        (13 dizin, 138 dosya; ornek gstack\bin\dev-setup) okunamaz yapardi.

  Kullanim (PowerShell 5.1; bu makinede pwsh yok):
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\deny-11l.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\deny-11l.ps1 -Apply

  Idempotent: ikinci -Apply hicbir sey yazmaz. Yedek: settings.json.bak11l
  ConvertTo-Json -Depth 100 zorunlu: 5.1 varsayilani 2, derin skillOverrides agaci
  sessizce kirpilir ve dosya bozulur.
#>
[CmdletBinding()]
param(
  [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$DERINLIK = 100

$ayar = "$env:USERPROFILE\.claude\settings.json"
if (-not (Test-Path $ayar)) { throw "settings.json yok: $ayar" }

$yeniKurallar = @(
  'Read(**/bin/Debug/**)',
  'Read(**/bin/Release/**)',
  'Read(**/obj/**)'
)

$s = Get-Content $ayar -Raw | ConvertFrom-Json
if (-not $s.permissions) { throw "settings.json'da permissions blogu yok" }

$mevcut = @($s.permissions.deny)
$eklenecek = @($yeniKurallar | Where-Object { $mevcut -notcontains $_ })
$zatenVar  = @($yeniKurallar | Where-Object { $mevcut -contains $_ })

"settings.json    : $ayar"
"mevcut deny      : $($mevcut.Count)  $($mevcut -join ', ')"
"zaten var        : $($zatenVar.Count) $($zatenVar -join ', ')"
"eklenecek        : $($eklenecek.Count) $($eklenecek -join ', ')"
"deny (sonra)     : $($mevcut.Count + $eklenecek.Count)"

# Guvenlik kapisi: tum bin agacini kapatan kalip asla yazilmaz.
foreach ($k in $eklenecek) {
  if ($k -eq 'Read(**/bin/**)') { throw "yasak kalip uretildi: $k (gstack bin/ dizinlerini kapatir)" }
}

if (-not $Apply) { "`n(kuru kosu) Yazmak icin ayni komuta -Apply ekle."; return }
if ($eklenecek.Count -eq 0) { "`ndegisiklik yok; dosyaya dokunulmadi."; return }

Copy-Item $ayar "$ayar.bak11l" -Force
$s.permissions.deny = @($mevcut + $eklenecek)
[IO.File]::WriteAllText($ayar, ($s | ConvertTo-Json -Depth $DERINLIK), (New-Object Text.UTF8Encoding $false))

# --- dogrulama: JSON gecerli, permissions disindaki her ust-duzey alan birebir ayni
$yeniAyar = Get-Content $ayar -Raw | ConvertFrom-Json
$eskiAyar = Get-Content "$ayar.bak11l" -Raw | ConvertFrom-Json
function Ozet($x) {
  $x.PSObject.Properties | Where-Object { $_.Name -ne 'permissions' } |
    ForEach-Object { $_.Name + '=' + ($_.Value | ConvertTo-Json -Depth $DERINLIK -Compress) }
}
$fark = @(Compare-Object (Ozet $eskiAyar) (Ozet $yeniAyar))

"`nyazildi. deny: $($mevcut.Count) -> $($yeniAyar.permissions.deny.Count)"
"permissions disi fark: $($fark.Count)"
if ($fark.Count -gt 0) { $fark | Format-Table -AutoSize; throw "beklenmeyen fark: baska alanlar degisti" }
"yeni deny        : $($yeniAyar.permissions.deny -join ', ')"
