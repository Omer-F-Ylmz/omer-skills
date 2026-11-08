# F3: headroom uv aracını 0.39.0'a yükseltir (MCP/CLI kopyası; masaüstü proxy zaten 0.39.0). Oturum açılışında BİR KEZ koşar,
# başarıda kendi HKCU Run kaydını (omer-headroom-guncelle; Görev Zamanlayıcı onlogon yönetici ister: Erişim engellendi) siler. Kilit varsa (çalışan `headroom mcp serve`) hiçbir süreç öldürülmez; kayıt kalır, sonraki açılışta yeniden dener.
$ErrorActionPreference = "Stop"
$log = "C:\Projeler\omer-skills\.kos\kopru\headroom-guncelle.log"
function L($m) { Add-Content -Encoding utf8 $log "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $m" }
$exe = "$env:USERPROFILE\.local\bin\headroom.exe"
$once = (& $exe --version 2>&1 | Out-String).Trim()
$kilit = Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -like "*\.local\bin\headroom.exe" -or $_.CommandLine -like "*uv\tools\headroom-ai*" }
if ($kilit) { L "KILIT: $($kilit.ProcessId -join ',') çalışıyor, güncelleme ertelendi (önce: $once)"; exit 0 }
uv tool install "headroom-ai[all]==0.39.0" --force 2>&1 | ForEach-Object { L $_ }
$sonra = (& $exe --version 2>&1 | Out-String).Trim()
L "önce: $once · sonra: $sonra"
if ($sonra -match "0\.39\.0") { Remove-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name omer-headroom-guncelle -ErrorAction SilentlyContinue; L "Run kaydı silindi" } else { L "DOĞRULAMA BAŞARISIZ, kayıt kaldı" }
# Proxy RAM ayarı: proxy masaüstü uygulamasınca (Headroom\headroom-desktop.exe --autostart) başlatılıyor ve argüman ayarı sunmuyor
# (launch-profile.json'da yok); burada değiştirilecek bir şey yok. İzleme: docs/headroom-f3.md ölçüm komutu.
