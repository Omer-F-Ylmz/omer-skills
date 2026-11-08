---
type: report
status: tur-bitti
tags: [bul-kur-2]
relatedTo: [docs/video-tarama/kurulum-coz-6.tsv, rapor/hizmet-hesap.md, rapor/omer-sor-2gb-coz6.md]
---
# BUL-KUR-2 (7 Kas 2026) — TUR BITTI
Sinif | once | sonra
- SINIFSIZ AD 1821 + URL 268 | siniflanmamis | siniflandi (GENEL 484, HIZMET 404, SKILL 222, UYGULAMA 108, CLI 82, PAKET 21, MODEL 15, BELIRSIZ 485). Slash/yol/CC-yerlesik 196 kalem bu siniflayicinin disinda (onceki sinif korunur).
- REPO-LINKLI 215 gh linki | kontrolsuz | 47 erisilebilir, 167 404 (OCR bozuk link; 68'i yeniden aranacak sete eklendi), 1 HATA (tmp/bk2-repo.tsv). Kalan ~860 "link" urun sitesi (HIZMET/UYGULAMA), gh degil.
- Yeniden arama 1699 kalem (SKILL/CLI/PAKET BULUNAMADI-2 + YANLIS-ESLESME, MODEL, BELIRSIZ, KESIN, REPO404) | hepsi YOK/BULUNAMADI | 83 CLI/SKILL/PAKET/BELIRSIZ/KESIN/REPO404 DOGRULANDI + 17 MODEL; ADAY 210; YOK ~1390 (kurulum-coz-6.tsv, 1699 satir, kalem basina 1).
- DOGRULANDI yol: gh 63 · hf 20 · npm 7 · pip 4 · vscode 1 · winget 1 · blender 1.
- Kapi (kurulum yok): gh/npm/pip DOGRULANDI 74 -> KAPI-GECTI 44, HATA 28 (klon/zaman asimi), GUVENLIK-RED 1, YOL-YOK 1.
- HIZMET 1413: rapor/hizmet-hesap.md (ucretsiz EVET 629, HAYIR 43, BILINMIYOR 741; model tahmini, siteden dogrula).
- kurulum_coz6.ps1: -Deneme HATA 0 (2 satir calisir: VSCODE, WINGET -Sistem ister). >2 GB hf 17 satir yorum: rapor/omer-sor-2gb-coz6.md.
Sapmalar/sinirlar:
- gh arama yalniz oncelikli 578 kalemde (SKILL/CLI/PAKET + REPO404); BELIRSIZ (778) ve KESIN (100) yalniz PyPI/npm/HF/VSCode/Blender/winget.run'da arandi. gh search 30/dk siniri ~7 kalem/dk verdi.
- Sinif BELIRSIZ/KESIN/REPO404 satirlari kurulum_d2 sinif kapisi icin CLI/PAKET/MODEL'e cevrildi (ilk sinif gerekce sonunda).
- Yargic: ucretsiz havuz (haiku tavani 60/cagri-kolu), Sonnet yargic cagrilmadi; ADAY'lar insan/Sonnet dogrulamasi ister. Bozuk 2 erken calisma _arsiv/ altinda.
- UYGULAMA sinifi kapsam disi (Ömer ayri konusacak).
Omer'in TEK komutu (kapi gecenleri kurar): python tools/kurulum_d2.py --faz kur --coz docs/video-tarama/kurulum-coz-6.tsv --sinif SKILL,CLI,PAKET
Araclar: ucretsiz_havuz, gh api, PyPI/npm/HF/VSCode/Blender/winget.run, kurulum_d2 kapisi, kurulum_gurultu.ps1 sablonu. Atlanan: graphify/xerj (liste isi, grafik gerekmedi), Sonnet yargic (tavan korundu).
