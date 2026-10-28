# DERIN-HIZ-1

## Profil (derin-profil.tsv, 2349 video, toplam 119 077 sn ≈ 33 sa; medyan 20,8 sn/link)
| adım | toplam sn | pay | not |
|---|---|---|---|
| OCR (RapidOCR, ort. 1,4 sn/kare) | 59 643 | %50 | CPU'ya düşen 59 videoda 199 sn ortalama |
| ASR (large-v3 beam5) | 31 376 | %26 | uzun-kuyruk: 17 702 sn yalnız 97 uzun videoda |
| kare açıklama | 17 244 | %14 | Gemini/Ollama, OCR ile örtüşür |
| indirme | 9 752 | %8 | |
| kare çıkarma | 1 062 | %1 | |
Darboğaz uzun kuyruk: >200 sn süren 97 video (%4) toplam sürenin %38'i. 120 saatlik tahmin kuyruk uzun/CPU-düşüşlü videolardan; medyan link 21 sn.

## Değişiklik (tools/video_derin.py)
- cuda ASR: large-v3 → **large-v3-turbo**, beam 5 → **1** (env: VD_ASR_MODEL, VD_ASR_BEAM).
- yt-dlp `-N 4` (parça paralel indirme).
- Toplu ASR (BatchedInferencePipeline) eklendi ama **varsayılan KAPALI** (VD_ASR_BATCH=1): 10 linkte 7XhX8P0ebEU'da sessizce 0 kelime döndü.
- tools/derin_hiz_karsilastir.py: eski/yeni derin json karşılaştırma.

## Önce/sonra (aynı 10 link, eski json = docs/video-tarama/derin)
- 7XhX8P0ebEU ASR 761 sn → 48 sn; 2x-aQy730Ew 301 → 24; -WjVIPc0jT0 332 → 27; kısa videolar ~aynı.
- Kalite (turbo+beam1): link 10/10 aynı, komut 10/10 aynı, OCR örtüşmesi 1,000. Transkript kelime benzerliği ort. 0,886 (min 0,61 DUS8hMijFGv: 112→75 kelime, kısa video).
- **Sapma:** jev MCP bu oturumda yok (ToolSearch boş), jev puanlaması yapılmadı. "Fark ≤%2" kapısı karşılanmadı: kelime benzerliği %11 fark. Ama link/komut/OCR (derin json'un tüketilen alanları) tam aynı; eski çıktı da referans değil (aynı eski ayarı yeniden koşunca kıyas yok). Karar Ömer'de: istenirse VD_ASR_MODEL=large-v3 VD_ASR_BEAM=5 ile eski kalite (hız kazancı azalır).

## 30 dk kesintisiz deneme (--es 2, 877 eksik linkten ilk 52; çıktı test dizinine)
- 52 ok, 1 indirme hatası, medyan 56 sn/link (eşzamanlı 2), duvar saati ≈ 36 sn/link → 877 link ≈ **8–9 saat** (hedef ≤15 sa karşılandı; eski 120 sa).
- GPU: VRAM ≤6,8 GB/12, sıcaklık ≤71 °C, ASR "basarisiz" 0, CPU düşüşü 0, süreç çökmedi.
- RAM: koşu sonunda %92,5'e çıktı (python 1,5 GB + 2 claude oturumu + vmmem); mevcut bekçi (≥88'de yeni video yok) yeni işi durdurur, ama diğer süreçler RAM'i şişirince koşu dışı kalan kısım kontrolsüz. Toplu koşuda başka claude oturumu açık olmamalı.
- TDR/141: bu koşuda yeni çekirdek olayı yok. 14:01'de gelen WER 141 kaydı 21 Eki WATCHDOG dökümünün (WATCHDOG-20261021-2230.dmp) geç raporu. Kök neden hâlâ kanıtsız; 30 dk'da tekrar etmedi (turbo ≈ daha kısa GPU çekirdeği + cuda tek ASR kilidi).

## Toplu koşu planı (BAŞLATILMADI)
- Liste: .kos/kopru/arka/derin-eksik.txt (877 link, 864 YouTube).
- 6 gece/boşta parçası ≈ 150 link (~1,5 sa): `python tools/video_derin.py --es 2 --en 150 --liste .kos/kopru/arka/derin-eksik.txt` (toplu_gozetmen.py ile; biten atlanır, --en yalnız yeni işi sayar).
- Koşu öncesi: başka claude oturumlarını kapat (RAM %70 → %90 kaymasının ana suçlusu), C: ≥80 GB (şu an 254 GB boş).
- Beklenen gecikme uzantıları: ~%2 indirilemedi (silinmiş video), uzun videolar 5–10 dk.
