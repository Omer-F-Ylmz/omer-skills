# C3: Windows.Media.Ocr ile kareleri tr + en tanıyıcıyla oku. Argümanlar: jpg yolları.
# Çıktı (UTF-8 JSON): {"<dosya adı>": {"tr": [[metin, x0, y0, x1, y1], ...], "en": [...]}}. Tanıyıcı yoksa rc=2.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime]
$asTask = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Bekle($islem, [Type]$tip) {
    $g = $asTask.MakeGenericMethod($tip).Invoke($null, @($islem))
    $null = $g.Wait(-1)
    $g.Result
}
$motor = [ordered]@{}
foreach ($d in @(@('tr', 'tr'), @('en', 'en-US'))) {
    $e = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new($d[1]))
    if (-not $e) { [Console]::Error.WriteLine("OCR tanıyıcı yok: $($d[1])"); exit 2 }
    $motor[$d[0]] = $e
}
$sonuc = [ordered]@{}
foreach ($yol in $args) {
    $f = Bekle ([Windows.Storage.StorageFile]::GetFileFromPathAsync($yol)) ([Windows.Storage.StorageFile])
    $akis = Bekle ($f.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $coz = Bekle ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($akis)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bmp = Bekle ($coz.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $k = [ordered]@{}
    foreach ($dil in $motor.Keys) {
        $r = Bekle ($motor[$dil].RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])
        $k[$dil] = @($r.Lines | ForEach-Object {
            $c = @($_.Words | ForEach-Object { $_.BoundingRect })
            , @($_.Text, ($c | ForEach-Object { $_.X } | Measure-Object -Minimum).Minimum, ($c | ForEach-Object { $_.Y } | Measure-Object -Minimum).Minimum,
                ($c | ForEach-Object { $_.X + $_.Width } | Measure-Object -Maximum).Maximum, ($c | ForEach-Object { $_.Y + $_.Height } | Measure-Object -Maximum).Maximum)
        })
    }
    $akis.Dispose()
    $sonuc[[IO.Path]::GetFileName($yol)] = $k
}
$cikti = [Text.Encoding]::UTF8.GetBytes(($sonuc | ConvertTo-Json -Depth 5 -Compress))
[Console]::OpenStandardOutput().Write($cikti, 0, $cikti.Length)
