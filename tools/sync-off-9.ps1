<#
  KURULUM-9 sync-off — dist/yukle-9b ile claude.ai'ye giden paketin synced kopyalarini kapatir.

  Kural 1: replace/ altindaki 55 gstack zip'i (gstack-core dahil) kosulsuz off —
           CC'de native gstack gecerli, claude.ai shim'leri (python $B, gstack-env) CC'de kullanilmaz.
  Kural 2: yeni/ altindaki zip (skill-ui-cli) ve web-sahne-desenleri — yalniz aktif yerel
           ya da plugin kopyasi varsa off; yoksa synced kopya acik kalir.
  Kural 3: yalniz synced'e ozgu `anthropic-skills:<ad>` anahtari yazilir. Bare-ad override
           native/yerel kopyayi da kapattigi icin YASAK.

  Kullanim:  .\tools\sync-off-9.ps1            # -WhatIf: sayim + eklenecek anahtarlar
             .\tools\sync-off-9.ps1 -Apply     # yazar (yedek: settings.json.bak9s)
  Idempotent: ikinci -Apply hicbir sey yazmaz.
#>
[CmdletBinding()]
param(
  [switch]$Apply,
  [string]$Dist = "C:\Projeler\omer-skills\dist\yukle-9b"
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem

$ayar = "$env:USERPROFILE\.claude\settings.json"
$skillKok = "$env:USERPROFILE\.claude\skills"
$s = Get-Content $ayar -Raw | ConvertFrom-Json
$oncekiOff = ($s.skillOverrides.PSObject.Properties | Where-Object { $_.Value -eq 'off' }).Count

# --- hedef kume: zip kok klasor adi = frontmatter name (denetim bunu zorunlu tutuyor)
$kural = @{}
Get-ChildItem $Dist -Recurse -Filter *.zip | ForEach-Object {
  $z = [IO.Compression.ZipFile]::OpenRead($_.FullName)
  $ad = $z.Entries[0].FullName.Split('/')[0]
  $z.Dispose()
  if ($_.FullName -like '*\replace\*') { $kural[$ad] = 1 } else { $kural[$ad] = 2 }
}
$kural['web-sahne-desenleri'] = 2
$adlar = $kural.Keys | Sort-Object

# --- envanterler
$syncedKok = Get-ChildItem (Join-Path $skillKok 'synced') -Directory | Select-Object -First 1
$synced = Get-ChildItem $syncedKok.FullName -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | ForEach-Object { $_.Name }
$yerel = Get-ChildItem $skillKok -Directory |
  Where-Object { $_.Name -ne 'synced' } | ForEach-Object { $_.Name }
$plugin = Get-ChildItem "$env:USERPROFILE\.claude\plugins" -Recurse -Filter SKILL.md -ErrorAction SilentlyContinue |
  ForEach-Object { $_.Directory.Name } | Sort-Object -Unique

$eksik = @($adlar | Where-Object { $synced -notcontains $_ })

# --- karar
$eklenecek = @(); $acikKalan = @(); $cift = @(); $zatenOff = @()
foreach ($ad in $adlar) {
  $anahtar = "anthropic-skills:$ad"
  $baskaKopya = ($yerel -contains $ad) -or ($plugin -contains $ad)
  if ($baskaKopya) { $cift += $ad }
  if ($kural[$ad] -eq 2 -and -not $baskaKopya) {
    $acikKalan += $ad
    continue
  }
  $mevcut = $s.skillOverrides.PSObject.Properties[$anahtar]
  if ($mevcut -and $mevcut.Value -eq 'off') { $zatenOff += $ad; continue }
  $eklenecek += $anahtar
}

# --- kural 3 kalkani: bare-ad anahtar asla yazilmaz
$bare = @($eklenecek | Where-Object { $_ -notlike 'anthropic-skills:*' })
if ($bare.Count -gt 0) { throw "bare-ad anahtar uretildi: $($bare -join ', ')" }

"hedef kume      : $($adlar.Count) ad (kural 1: $(($kural.Values | Where-Object { $_ -eq 1 }).Count) . kural 2: $(($kural.Values | Where-Object { $_ -eq 2 }).Count))"
"synced'de eksik : $($eksik.Count) $($eksik -join ', ')"
"off (once)      : $oncekiOff"
"eklenecek (N)   : $($eklenecek.Count)  -> off (sonra): $($oncekiOff + $eklenecek.Count)"
"zaten off       : $($zatenOff.Count)"
"acik kalan      : $($acikKalan.Count) $($acikKalan -join ', ')"
"baska aktif kopyasi olan (cift): $($cift.Count) $($cift -join ', ')"
"bare-ad anahtar : 0"
if ($eklenecek.Count -gt 0) { "--- eklenecek anahtarlar ---"; $eklenecek | Sort-Object }

if (-not $Apply) { "`n(-WhatIf) Yazmak icin: .\tools\sync-off-9.ps1 -Apply"; return }
if ($eklenecek.Count -eq 0) { "`ndegisiklik yok; dosyaya dokunulmadi."; return }

Copy-Item $ayar "$ayar.bak9s" -Force
foreach ($anahtar in $eklenecek) {
  $s.skillOverrides | Add-Member -NotePropertyName $anahtar -NotePropertyValue 'off' -Force
}
[IO.File]::WriteAllText($ayar, ($s | ConvertTo-Json -Depth 30), (New-Object Text.UTF8Encoding $false))

# --- dogrulama: JSON gecerli, skillOverrides disinda anlamca fark yok
$yeniAyar = Get-Content $ayar -Raw | ConvertFrom-Json
$sonraOff = ($yeniAyar.skillOverrides.PSObject.Properties | Where-Object { $_.Value -eq 'off' }).Count
$eskiAyar = Get-Content "$ayar.bak9s" -Raw | ConvertFrom-Json
function Ozet($x) {
  $x.PSObject.Properties | Where-Object { $_.Name -ne 'skillOverrides' } |
    ForEach-Object { $_.Name + '=' + ($_.Value | ConvertTo-Json -Depth 30 -Compress) }
}
$fark = @(Compare-Object (Ozet $eskiAyar) (Ozet $yeniAyar))
"`nyazildi. off: $oncekiOff -> $sonraOff (+$($eklenecek.Count))"
"skillOverrides disi fark: $($fark.Count)"
if ($fark.Count -gt 0) { $fark | Format-Table -AutoSize }
