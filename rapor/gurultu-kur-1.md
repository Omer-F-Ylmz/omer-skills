# GURULTU-KUR-1
Kaynak doğrulama: gh api (sahip/lisans/son push/boyut), HF API (boyut, lisans), PyPI, winget-pkgs manifest. Kurulum YAPILMADI.
- Cloudflare/clef 51.2 GiB, clef-flash 17.8 GiB, convaiinnovations/laya 2.2 GiB: GitHub'da yok, HF ağırlığı, Apache-2.0 → OMER-SOR yorum. MegaTTS3 (ByteDance/MegaTTS3) 3.98 GiB Apache-2.0, indirme yok → OMER-SOR.
- clef-decision-demo: Tijo2000 hesabı yok; gerçek ajmontalbano/clef-decision-demo (MIT) klon.
- axolotl (Apache-2.0), langgraph (MIT; langchain-ai için tek repo, ajan orkestrasyonu), LightRAG (MIT; HKUDS için tek repo, V2RIVnGCy74 videosu listesinde), 3dcodeverse (ilabai yok → gaoypeng, Apache-2.0), Nakama (Apache-2.0), nanochat (MIT), Paperclip (MIT): klon.
- andrej-karpathy-skills: lisans YOK (engel değil), skills/ altı skill. storm-research: openwhat007 (MIT), SevenBaylor kopyası lisanssız.
- nano-pdf: PyPI 0.2.1 (MIT) → uv tool. himalaya: winget manifesti yok, GitHub v2.2.1 zip (19 MB); skills/himalaya zaten var. manim-video: skill zaten kurulu.
- Typst: winget Typst.Typst (manifest doğrulandı; `winget search` bu makinede takılıyor). Spacedrive: winget yok, 86 MB msi → UYGULAMA yorum.
Sınıf sayıları (19 satır): KLON 8 · OMER-SOR 4 · SKILL 2 · UV 1 · INDIR 1 · WINGET 1 · UYGULAMA(yorum) 1 · ZATEN(yorum) 1. npm kütüphane düzeltmesi: 0 (npm kalemi yok).
-Deneme: 13 satır yazdı (12 DENEME, Typst ATLANDI), sonuç rapor/kurulum-gurultu-sonuc.tsv.
Ömer'in iki satırı (PowerShell, repo kökünde):
1. `powershell -ExecutionPolicy Bypass -File tools\kurulum_gurultu.ps1 -Deneme`
2. `powershell -ExecutionPolicy Bypass -File tools\kurulum_gurultu.ps1 -Sistem`
Dosyalar: tools/kurulum_gurultu.ps1, tools/kurulum_gurultu_uret.py, docs/envanter/kurulum-kuyruk.tsv.
Araçlar: gh, curl (HF API), PowerShell -Deneme. Kullanılmayan: departman skill/xerj (tek seferlik doğrulama işi, gerekçe: kaynak doğrulaması CLI ile doğrudan).
