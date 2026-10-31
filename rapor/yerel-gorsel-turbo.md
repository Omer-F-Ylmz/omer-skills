# YEREL-GORSEL-TURBO — TUR BITTI (tamamlanmadı, DUR)

**Model:** reel'deki model Qwen-Image-2.1-Turbo (unsloth GGUF, 729k indirme). Lisans Qwen Research = yalnız ticari olmayan. Sosyal medya ticari → KURULMADI (lisans kapısı). "Apache" etiketli yeniden yüklemeler aynı ağırlıkların türevi, geçerli sayılmaz.
**Ticari-güvenli yedek:** Z-Image-Turbo GGUF Q4_K_M (3,67 GB, Apache-2.0) + Qwen3-4B GGUF Q4_K_M (2,5 GB, Apache-2.0); ComfyUI-GGUF zaten kurulu. C: boş ~125 GB.

**Yapılan:** `MODELLER["turbo"]` + `tools/gorsel/akislar/turbo.json` + `tools/turbo_olcum.py`; `ac` açılış bekçisi artık HTTP'ye de bakıyor (netstat bu makinede dinleyen 8188 soketini göstermiyor → `ac` hep zaman aşımı veriyordu, kanıtlı); `ac` bayrakları `--disable-smart-memory --reserve-vram 2.5`.

**Ölçüm (1024², seed 42, 12 GB RTX 4070 Ti, 32 GB RAM, taban RAM ~%70 / VRAM ~%24):**
| koşu | sn | tepe RAM | tepe VRAM |
|---|---|---|---|
| varsayılan bayrak, logo (soğuk) | 45,5 | %91,6 | %90,5 |
| +smart-memory kapalı, reserve 2,5: portre | 14,8 | %87,2 | %89,7 |
| aynı, logo (önbellekten) | 1,8 | %86,4 | %72,8 |
| `--lowvram` | çöktü | — | — |
| son tam 5'li koşu | çöktü / RAM freni | %96,3 | %50,1 |

**Hedef (RAM ≤%89, VRAM ≤%80): TUTMADI.** Son koşuda iş başında boş RAM 7,4 GB iken sunucu çöktü, acil fren devreye girdi (1,3 GB). Kök neden: sistemde diğer süreçler ~7 GB boş bırakıyor; soğuk yüklemede GGUF + encoder çözümleme tepesi bunu aşıyor. Kısmen işe yarayan: bayraklar tepeyi %91,6→%87,2'ye indirdi, ama VRAM tepesi %89,7 (VAE çözümü).

**Yapılmadı:** 5 prompt benchmark + bağımsız hakem + flux/z_image karşılaştırması; gorsel-uret skill'ine turbo yolu; profil-gorsel-1 / sunucu-karakter-1 `devam_notu` satırı (başarısız olduğu için eklenmedi); 2. beyne yazım.
**Sonraki adım:** diğer RAM tüketicilerini kapatıp (≥14 GB boş) yeniden ölç; VAE için `VAEDecodeTiled` dene; sonra hakem + skill.
Dalga dosyası: `.claude/dalga.md`; çıktılar: Masaüstü\yerel-gorsel-turbo (kısmi).

## Tur 2 (30 Eki 04:2x) — DUR
`ram_top.py` / `yetim.py` / `gpu_sinir_olcum.py` repoda yok (var olan: gpu_sinir.py, vram_bekci.py). Süreç dökümü: kapatılabilir kendi sürecimiz yok (headroom 1,4 GB, omniroute 0,9 GB araç altyapısı; sqlservr/opera/chrome Ömer'in) → boş RAM ~8,7 GB, ≥14 GB hedefine ulaşılamadı.
Değişiklik: turbo.json `VAEDecodeTiled` (512/64), `ac` `--reserve-vram 3`. Ölçüm: logo 41,8 sn, tepe RAM %94,9, VRAM %52,4 (VRAM hedefi tuttu), sonra RAM 1,9 GB altına inince acil fren ComfyUI'yi kapattı; kalan 4 prompt koşmadı.
Kök neden: RAM (VRAM değil). Soğuk yükleme tepesi ~6 GB, boş 7,9 GB yetmiyor. Benchmark/hakem/skill/devam_notu yapılmadı.
Öneri (Ömer kararı): Ömer'in kendi uygulamalarını (Opera/Chrome/SQL Server) kapatıp ≥14 GB boşla tekrar koş, ya da sayfa dosyasını büyüt.

## Tur 3 (31 Eki 08:5x) — HEDEF TUTTU (boş RAM 13,7 GB iken)
Önkoşul: boş RAM bu turda ~13,7 GB (önceki turlarda 7,9). Aynı model/akış (turbo, Z-Image GGUF Q4_K_M, VAEDecodeTiled, `--disable-smart-memory --reserve-vram 3`), 5 prompt 1024², tohum 42, çıktı Masaüstü\yerel-gorsel-turbo\<etiket>:
| koşu | logo sn | sonraki 4 sn | tepe RAM | tepe VRAM |
|---|---|---|---|---|
| A taban | 48,8 | 21–31 | %84,4 | %50,3 |
| B +`--disable-pinned-memory` | 40,9 | ~20 | %82,3 | %50,0 |
| C +`--disable-mmap` | 41,0 | 20–29 | %80,6 | %50,5 |
| D +`--cache-none` | ölçülemedi: 180 sn içinde açılmadı (neden bakılmadı) | — | — | — |
Hedef (RAM <%89, VRAM ≤%80): A, B, C üçünde de 5/5 prompt tuttu (logo dahil). En düşük tepe: C (`--disable-mmap`). fp8/gguf değişimi gerekmedi (model zaten Q4); model yükleme sırası denenmedi.
Bulgu: kapatılan ComfyUI sonrası 8188'de PID 0 "hayalet" LISTEN kalıyor (taskkill sonrası, curl bağlanamıyor) → `ac` "başka süreçte" diye reddediyor. Her yeniden başlatma yeni port gerektirdi; `GORSEL_PORT` env eklendi. 5/6 yeniden başlatma kullanıldı.
Yapılmadı: bağımsız hakem (5 görsel üretildi, puanlanmadı), flux/zimage karşılaştırması, C bayrağının `ac` varsayılanına alınması (şimdilik `COMFY_EK="--disable-mmap"`), skill zip'inin (dist) yeniden yapımı, `devam_notu` satırları. Boş RAM ~8 GB'a düşerse soğuk yükleme riski sürer (bu turda ölçülmedi).
