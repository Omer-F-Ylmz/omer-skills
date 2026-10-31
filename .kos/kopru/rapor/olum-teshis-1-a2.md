OLUM-TESHIS-1-A2 (28 Eki, yalniz okuma)
Kok neden KANITSIZ: derin-hiz-1.md:28 "TDR/141 kok neden hala kanitsiz"; derin-hiz-3.md nedeni kanitlamiyor.
Kanit: WER LiveKernelEvent P1=141 bugun 07:12, 11:07, 12:25, 13:15, 13:18, 14:01, 15:33, 19:08 (8 kayit). System logunda nvlddmkm/Display (4101 TDR) kaydi YOK -> 141 = GPU takilmasi (LiveKernelEvent), klasik TDR sifirlamasi dogrulanmadi.
nvidia-smi simdi: RTX 4070 Ti, surucu 610.88, 68C, util %42, 2611/12282 MiB, throttle 0x1 (yalniz idle) -> sicaklik/bellek baskisi yok.
Sonuc: BITTI sayilmaz. Sonraki: gpu_sinir/nvidia-smi dongu gunlugu (util, bellek, sicaklik, 1 sn) 141 anlarinda ile eslestir; surucu 610.88 yukseltme/geri alma denemesi Omer karari.

## 31 Eki 09:00 ek ölçüm (YARIM-216 tur3)
- WER P1=141: son 30 günde 4169; 1-9 Eki günde 126-684, 10-20 Eki sıfır (kayıt yok), 21 Eki'den beri günde 3-18 (31 Eki 7). Sürücü 32.0.16.1088 (22 Tem) sabit → sürücü yükseltmesi neden değil. 141 = VIDEO_ENGINE_TIMEOUT_DETECTED sınıfı (GPU motor zaman aşımı, WATCHDOG dökümü).
- Düzeltme: System'de nvlddmkm olay 153 VAR (4 günde 23; "Error occurred on GPUID: 100"); eski rapordaki "nvlddmkm kaydı YOK" yanlış/eksik. 153↔141 ±5 dk örtüşme 1/61 → 153 aynı olay değil.
- vram-siper ComfyUI'yi vram %92'de öldürdü (07:08:36, 07:09:21) = 153 zamanları; 141 ile eşleşme: bugünkü 7 olaydan 1'i kill ±3 dk, 2'si nvidia-smi zaman aşımı ±3 dk. Önyükleme (02:49:15, 02:56:25) hemen sonrası 141 (02:49:46, 02:57:01).
- Sonuç: kök neden HÂLÂ KANITSIZ (zaman korelasyonu tutarsız, GPU yük serisi yok). Kanıtsız düzeltme yapılmadı.
- Başlatılan ölçüm: gpu_141_kayit.py (1 sn: util/bellek/sıcaklık/güç/saat/pstate) → arka/gpu-141-kayit.log, en çok 6 sa. Oturum bitince ölebilir (breakaway reddedildi). Sonra: 141 zamanlarıyla eşle (rapor: bellek tepe/güç düşüşü/pstate).
