---
type: doc
status: aktif
tags: [arka-plan, uygulama, kod-modu]
relatedTo: [tools/arka_uygulama.py]
---
# Uygulamalar arka planda (Ömer'in ekranında görünmeden)

Üretim: `python tools/arka_uygulama.py tablo` (kayıt defteri taraması). Giriş: `python tools/arka_uygulama.py ara|komut|sanal`.
Yol sırası: başsız/CLI/API → ayrı masaüstü nesnesi (CreateDesktop; görev çubuğu + ön plan etkilenmez) → yok (yalnız izinle).
`komut` kısa ömürlü başsız işler içindir (çıktı dosyaya, ekrana ≤30 satır, ön plan örneklenir); ComfyUI gibi artalan sunucusu `gorsel_uret.py ac` ile doğrudan başlatılır (CREATE_NO_WINDOW).
Bölüm 1 (Code Mode her şeye): skill listesi `skillOverrides` name-only (2415/2755), MCP şemaları `ENABLE_TOOL_SEARCH`, MCP zincirleri `tools/cm.py`, CLI/uygulama `arka_uygulama.py komut`; araç kaldırılmadı (geri açma: skillOverrides değeri `on`).

Toplam kayıt 153 · uygulama 122: başsız 41 · sanal masaüstü 57 · yok (yalnız izinle) 24 · bileşen 31

| Uygulama | Yol | Komut kalıbı / not |
|---|---|---|
| 4DDiG File Repair 4.4.3.1 | sanal masaüstü | GUI yalnız; sanal masaüstü (tools/arka_uygulama.py sanal) |
| 7-Zip 23.01 (x64) | başsız | doğrudan CLI (arac-calistir kapısı) |
| Adobe Acrobat (64-bit) | başsız | pypdf/pdfplumber/ocrmypdf (Acrobat penceresi açılmaz) |
| Adobe Redeem Launcher | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| AIDA64 Extreme v6.92 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| Amazon Corretto (x64) | başsız | doğrudan CLI (arac-calistir kapısı) |
| AntiCheatExpert | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Apache NetBeans IDE 19 | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Armoury Crate Service | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| ASUS Framework Service | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| AURA lighting effect add-on | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| AURA lighting effect add-on x64 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| AURA Service | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| Aurora | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Battle.net | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Blender | başsız | blender -b dosya.blend -P betik.py / -o //cikti_#### -f 1 (render) |
| BlueStacks Services | sanal masaüstü | emülatör: GUI sanal masaüstünde; adb ile başsız komut |
| Browser for SQL Server 2022 | başsız | sqlcmd -S . -E -Q "..." |
| BrowserOS | başsız | chrome --headless=new --screenshot/--dump-dom; playwright headless |
| Bun | başsız | doğrudan CLI (arac-calistir kapısı) |
| Canon IJ Printer Assistant Tool | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Cascadeur | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Cloudflare WARP | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| cloudflared | başsız | doğrudan CLI (arac-calistir kapısı) |
| Comfy Desktop 1.1.6 | başsız | python tools/gorsel_uret.py ac/uret/kapat (main.py --disable-auto-launch, API 127.0.0.1:8188) |
| Counter-Strike 2 | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| CPUID CPU-Z MSI 2.03 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| CurseForge 1.298.3-31077 | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| DBX | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Discord | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Docker Desktop | başsız | docker <komut> (motor WSL2; Desktop penceresi gerekmez) |
| DroidCam Client | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| EgeYapı Panel | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Epic Games Launcher | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Epic Online Services | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| FFmpeg (Essentials Build) | başsız | ffmpeg -hide_banner -y -i girdi çıktı |
| GameSDK Service | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Geeks3D FurMark 1.36.0.0 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| Git | başsız | doğrudan CLI (arac-calistir kapısı) |
| GitHub CLI | başsız | doğrudan CLI (arac-calistir kapısı) |
| Gitleaks | başsız | doğrudan CLI (arac-calistir kapısı) |
| Google Chrome | başsız | chrome --headless=new --screenshot/--dump-dom; playwright headless |
| Goose Goose Duck | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| GRYPHLINK | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Headroom | başsız | doğrudan CLI (arac-calistir kapısı) |
| ICAT 0.6.17 | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| IIS 10.0 Express | başsız | doğrudan CLI (arac-calistir kapısı) |
| Intel(R) Chipset Device Software | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Intel(R) Management Engine Components | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| jq | başsız | doğrudan CLI (arac-calistir kapısı) |
| LagoFast | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Laragon 8.7.0 | başsız | laragon\bin\php/mysql/nginx ikili dosyaları doğrudan; laragon.exe açılmaz |
| LDPlayer 9 | sanal masaüstü | emülatör: GUI sanal masaüstünde; adb ile başsız komut |
| League of Legends | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Lua Language Server | başsız | doğrudan CLI (arac-calistir kapısı) |
| Microsoft .NET Core Runtime - 3.1.32 (x64) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft .NET Runtime - 6.0.16 (x64) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft .NET Runtime - 8.0.21 (x64) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft .NET SDK 10.0.400 (x64) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft .NET SDK 9.0.305 (x64) from Visual Studio | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Microsoft Edge | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Microsoft GameInput | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Microsoft Help Viewer 2.3 | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Microsoft MPI (10.1.12498.18) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft ODBC Driver 17 for SQL Server | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft OLE DB Driver for SQL Server | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft OneDrive | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Microsoft SQL Server 2019 LocalDB | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft SQL Server 2022 (64-bit) | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft SQL Server 2022 Setup (English) | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft SQL Server Management Studio - 20.2.1 | başsız | sqlcmd -S . -E -Q "..." (SSMS yerine) |
| Microsoft System CLR Types for SQL Server 2019 | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft Teams Meeting Add-in for Microsoft Office | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Microsoft Update Health Tools | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2005 Redistributable | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2005 Redistributable (x64) | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.4148 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2012 Redistributable (x64) - 11.0.61030 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2012 Redistributable (x86) - 11.0.61030 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2013 Redistributable (x64) - 12.0.30501 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ 2013 Redistributable (x86) - 12.0.30501 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ v14 Redistributable (x64) - 14.51.36247 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual C++ v14 Redistributable (x86) - 14.51.36247 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Microsoft Visual Studio Installer | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Microsoft Visual Studio Tools for Applications 2019 | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Microsoft VSS Writer for SQL Server 2022 | başsız | sqlcmd -S . -E -Q "..." |
| Microsoft Web Deploy 4.0 | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| Microsoft Windows Application Compatibility Fix Database | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Microsoft XNA Framework Redistributable 4.0 Refresh | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Movavi Screen Recorder | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| MSI Center SDK | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| NIKKE | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Node.js | başsız | doğrudan CLI (arac-calistir kapısı) |
| Node.js (LTS) | başsız | doğrudan CLI (arac-calistir kapısı) |
| NVIDIA App 11.0.9.251 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| NVIDIA Canvas 1.4.311 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA FrameView 1.5.9611.33638487 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA FrameView SDK 1.9.12728.38614306 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| NVIDIA GeForce NOW 2.0.58.134 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA Grafik Sürücüsü 610.88 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA HD Ses Sürücüsü 1.4.5.7 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA Omniverse Launcher 1.9.11 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA Omniverse Launcher 1.9.13 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| NVIDIA PhysX Sistem Yazılımı 9.23.1019 | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Obsidian | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Ollama version 0.40.6 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| OP Auto Clicker | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| OpenFic 0.12.0 | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| OpenPencil | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Opera GX Stable 138.0.6044.45 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Opera Stable 138.0.6044.24 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| PHP 8.5 | başsız | doğrudan CLI (arac-calistir kapısı) |
| PICO PARK | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| PromptHub 0.5.9 | sanal masaüstü | GUI; sanal masaüstünde aç, UI Automation ile yönet |
| Python 3.12.10 (64-bit) | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Python Launcher | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Radmin VPN 2.1.1 | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Realtek Audio Driver | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Realtek Ethernet Controller Driver | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Riot Client | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Riot Vanguard | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| RivaTuner Statistics Server 7.3.4 | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| Roblox Player for pc | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Roblox Studio for pc | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| ROG Live Service | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| ROG PELTA | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| ROG PELTA (2.4GHz) | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| ROG PELTA (Bluetooth) | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| ROG STRIX SCOPE TKL | sanal masaüstü | donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız) |
| Skill UI 0.1.0 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Steam | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Steam Game Idler | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Teamfight Tactics | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Telegram Desktop | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Tenorshare 4DDiG 10.9.3.12 | sanal masaüstü | GUI yalnız; sanal masaüstü (tools/arka_uygulama.py sanal) |
| Tesseract-OCR - open source OCR engine | başsız | tesseract girdi.png çıktı -l tur+eng |
| TLauncher | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Ubisoft Connect | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| Unity Hub 3.6.1 | sanal masaüstü | GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok' |
| uv | başsız | doğrudan CLI (arac-calistir kapısı) |
| VALORANT | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Visual Studio Community 2022 | başsız | msbuild/dotnet build / ant/mvn; IDE açılmaz |
| vs_CoreEditorFonts | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| WinRAR 7.13 (64 bit) | başsız | doğrudan CLI (arac-calistir kapısı) |
| Wuthering Waves | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Xbox Service | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| XXMI Launcher | yok (yalnız izinle) | oyun/anti-hile: yalnız Ömer izin verirse |
| Zoom Workplace | yok (yalnız izinle) | hesap/oturum uygulaması: yalnız Ömer izin verirse |
| Zyxel NWD7605 Driver | bileşen | kütüphane/sürücü/servis: ayrı uygulama değil |
| Unity (kurulu değil) | başsız | Unity.exe -batchmode -nographics -quit -projectPath P -executeMethod M |
| Godot (kurulu değil) | başsız | godot --headless --path P --script betik.gd |
| Ghidra (kurulu değil) | başsız | support\analyzeHeadless.bat projeDizin proje -import ikili |
| Power Automate Desktop (kurulu değil) | sanal masaüstü | CLI yok; PAD.Console.Host sanal masaüstünde, akış URL'siyle |
