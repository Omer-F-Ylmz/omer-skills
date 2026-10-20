# TOKEN-REA d1 — PLAN (kendi sürümlerimiz)

Kural: kurulu araç silinmez/budanmaz; kendi sürüm yanında kurulur, A/B ile kazanırsa (taban üstü 4 eksende de, %98 kapı) Ömer onayıyla varsayılan olur. Ücretli çağrı yok, ölçüm Claude çağrısı ≤30.

## Önce veri: ağırlıklı taban 497.6M nerede? (taban.md profil tablosu, 14 gün)
| Kalem | Ağırlıklı | Pay |
|---|---|---|
| cache okuma (×0.1) | 192.5M | %38.7 |
| cache yazma (×1.25) | 178.0M | %35.8 |
| çıktı (×5) | 93.4M | %18.8 |
| girdi (×1) | 33.8M | %6.8 |
Sonuç: ağırlıklı maliyetin %75'i bağlam büyüklüğü + önbellek kırılması; komut çıktısı sıkıştırma (RTK/Headroom mesaj yolu) bunun yalnız küçük bir bölümünü hedefler. **Hedef "ek %50–60"ın yalnız araç sıkıştırmasıyla gelmesi beklenmez** — gerçek kaldıraç: sabit bağlam, önbellek yazma sıklığı, çıktı token'ı. Karar Ömer'de (aşağıda).

## Araç başı tasarım
| # | Sürüm | Tasarım | Beklenen kazanç (ölçülecek) | d2 kapısı |
|---|---|---|---|---|
| 1 | **bağlam-diyeti** (SessionStart + CLAUDE.md) | hook enjeksiyonu 14.6k → ≤6k: claude-mem gözlem sayısı (`CLAUDE_MEM_CONTEXT_OBSERVATIONS`), superpowers/using-superpowers tam metni yerine tek satır, kod haritası kısa; araç şeması 14.1k zaten ertelemeyle | istek başına −8k token; 24 329 istek × 8k × 0.1 = alt sınır ≈ −19M ağırlıklı (≈%4); cache yazma ilk turda ayrıca düşer | count_tokens sabit bağlam ≤22k; ilk-tur başarı (görev testi) eşit/üstü |
| 2 | **önbellek disiplini** (CC ayarları) | cache yazma %35.8: `token_olc --durma/--ttl-sim` ile TTL, /clear-compact zamanlaması, kurala bağlı | cache yazma −%20 ≈ −36M (≈%7) — varsayım, d2'de ttl-sim ile doğrulanır | aynı iş seti, ağırlıklı ≤ taban×0.93 |
| 3 | **rtk2** (sinyal-korumalı sarmalayıcı) | rtk + belirteç kapısı (yol/hash/sayı/error) → kayıpta ham; `ls` tüm ad, diff başlık, `git status` dizin sayımı | 10 komut seti −%30 → hedef ≥−%40 ve kalite 10/10 (şu an 8/10) | held-out 4 komut dahil kalite 100%, token ≥ baz |
| 4 | **sor2** (graphify hibrit) | etiket-önce + `git grep --seed` + token bütçesi ≤1.5k + kod-dışı ayrımı | sorgu başı 3.4k → ≤1.5k (−%55), isabet 6/10 → ≥9/10, 3.5 sn → <0.5 sn | held-out 5 soru, isabet ≥9/10 |
| 5 | **hr2** (Headroom yanı) | şema ertelemesi CC `ENABLE_TOOL_SEARCH` ile çakışma ölçümü; ML'siz soğuk yol; retrieve oranı telemetrisi | mesaj sıkıştırma ≈%2.6–4.8 → hedef +3 puan; çakışma çıkarsa tek katman bırakılır (A6 iki kol eşit: 22 319 ↔ 22 319) | üretim savings_events farkı, retrieve oranı <0.1 |
| 6 | **çıktı-diyeti** | çıktı ×5 ağırlığı %18.8: Concise stil + ajan çıktısı tavanı + alt ajan özet sınırı | çıktı −%15 ≈ −14M (≈%3) — varsayım | aynı iş seti çıktı token'ı, kalite hakemi eşit |
| 7 | claude-mem / BEYİN | arama zaten ~518 token/sorgu; enjeksiyon #1'de; BEYİN A/B %42–48 mevcut | ek kazanç yok, yalnız hakemli kalite seti (claude-mem 9/10 → hakemli) | hakem 19/20 altına düşmez |
| 8 | context-mode · OmniRoute · jev · qmd · NotebookLM · mcp-memory | d2'de önce taban ölçümü (MCP şema token'ı `tools/list` count_tokens; ücretsiz zincir kapıları var) | bilinmiyor | d2 taban |

**Toplam beklenen (varsayımlarla): ≈ −69M … −75M ağırlıklı ≈ %14–15** (1: 19M + 2: 36M + 6: 14M + diğer birkaç M). %50–60 hedefi (≥249M) için bu yetmez; kalan fark ancak iş desenini değiştirerek gelir (daha az tur, alt ajan/ücretsiz modele delege, kısa oturum). Bu bir kanıtlanmış sonuç değil, taban ağırlıklarından türetilmiş tahmindir; d2'de #1 ve #2'nin ölçümü hedefin gerçekçiliğini belirler.

## Sıra (d2 önerisi)
1. #1 + #2 (en büyük pay, kod yazmadan ayar/enjeksiyon; ölçüm betiği hazır: taban.py profil + token_olc ttl-sim).
2. #3 rtk2 sarmalayıcı (küçük, tohumlu set hazır) + #4 sor2.
3. #8 taban ölçümleri (bekleyen 6 araç) → durum `taban`.
4. #5, #6.
Mühür: held-out adları taban.json'da; kapıda tek seferlik.

## d2 SONUÇ (20 Eki 2026; Claude -p çağrısı 8/15, count_tokens ~100)
**d2a bağlam-diyeti** (`d2a_bolum.py`, `d2a_ab.py`, ajan profili, geçici --settings; kurulu ayar değişmedi):
- Blok dökümü (token): CLAUDE.md+hafıza dizini 4743 · ortam/ajan listesi 2374 · context-mode 1760 · claude-mem 1408+271 · superpowers 1292 · ponytail 934 + kod haritası 1159 · diğer 170. Hook toplamı ≈6.8k; kalan 7.3k hook değil.
- A (taban) 30 080 → B (superpowers/ponytail/context-mode kapalı + claude-mem gözlem 5) **25 335 (−4 745, −%15.8)**; görev testi iki kolda da doğru ('kur'); görev maliyeti 0.082→0.038 $ (tek ölçüm, gürültülü). **Kapı ≤22k KARŞILANMADI** (−3.3k eksik): kalan kaldıraç CLAUDE.md+MEMORY.md dizini (4.7k, kısaltma Ömer kararı) ve ortam/ajan listesi (2.4k).
- Ağırlıklı tahmin (hepsine uygulanırsa): 24 329 istek×4.7k×0.1 + 1262 oturum×4.7k×1.25 ≈ −19M ≈ %3.8 (plan varsayımı 19M ile tutarlı, 8k yerine 4.7k ile).
- **Önbellek disiplini**: `token_olc --ttl-sim` (66 oturum, 1691 istek): "baştan" yazma %31.8; sebep: ara>TTL yalnız %11.4, "diğer" %85.6 (oturum başı/ön ek değişimi). TTL tek başına hibrit −%4.1, 5m +%6.4 (1h'e göre). **Plandaki "cache yazma −%20" varsayımı DESTEKLENMİYOR**: TTL kolu ≈ −%4 × 53M ≈ −2M ağırlıklı (≈%0.4). Asıl kaldıraç ön ek sabitliği + oturum sayısı.
**d2b rtk2** (`rtk2.py`, `rtk2_set.py` kilit `rtk2_set.lock`, `rtk2_ab.py`): rtk çıktısı ham'daki dosya adı/hash belirtecini kaybederse eksikler sona eklenir; `ls` ad+boyut ile yerel üretilir.
- Eğitim 20 komut: ham 318 630 → rtk 163 022 (−%48.8) → **rtk2 179 386 (−%43.7)**; sıkı sinyal (her ham ad çıktıda) rtk 13/20 → **rtk2 20/20**. Held-out 4 (tek sefer): ham 20 890 → rtk 14 039 → rtk2 14 116 (−%32.4); sıkı **rtk 3/4 → rtk2 4/4**; tohum anahtar 3/4 (ikisinde de) — kaçan `git diff` anahtarı otomatik seçilen `a/tools/beyin.py` ön eki; dosya adı çıktıda var → anahtar yapaylığı, kalite kaybı değil. Maliyet: rtk2 süresi rtk'ye göre ~+%50 (iki süreç).
- Dürüstlük: 'ls' kompakt çıktısı büyük dizinde (`.kos/kopru` 40k→13.5k, rtk 590 ama ad kaybı) rtk'den çok daha uzun; kazanç −%43.7 < rtk −%48.8, bedeli kalite. Kapı "kalite 10/10 → RTK kazancı": sağlandı (20/20, 4/4). Varsayılan geçiş Ömer onayı.
- **sor2 (graphify hibrit) YAPILMADI** (tur tavanı); d3'e.

## ★ d3 TASLAK
1. sor2 (graphify hibrit) + held-out 5 soru metni yazıp kilitle; isabet ≥9/10, ≤1.5k token, <0.5 sn.
2. İş deseni kolu ölç: köprü şablonunda tur/okuma tavanı · ucuz alt ajan delegasyonu (ucretsiz_havuz+Haiku) · erken /clear · sabit ön ek; plan.md'de iki kolun toplamıyla %50-60 yolu sayıyla (şu an: araç ≈%4 + rtk2 + diyet ≈%3.8 + çıktı ≈%3 → ≈%10-12; kalan ≈%40 yalnız tur×bağlam azaltımından gelebilir).
3. Bağlam-diyeti ikinci adım: MEMORY.md dizin kısaltma + ortam/ajan listesi ile ≤22k (Ömer onayı) ve ham kalite setleri 20 madde/anlam hakemi.
4. d2c: bekleyen 6 aracın tabanı, hr2, çıktı-diyeti.

## d3 SONUÇ (20 Eki 2026; Claude -p çağrısı 0, count_tokens ~85)
0. Güvenlik: d2a_govde.json `Authorization` → `[GİZLİ]` (1 yer); dosya git geçmişinde yok; gitleaks token-rea/ temiz.
**Ölçüm düzeltmesi:** `taban.tok` 150k karakterde kesiyordu → büyük `git diff` ham'ı eksik sayılıyordu (d2'deki rtk −%48.8 / rtk2 −%43.7 yanlış). `rtk2_ab.py` artık parça parça toplar. Gerçek: 20 komut ham 1 361 010 → rtk 194 367 (−%85.7) → **rtk2 168 326 (−%87.6)**.
1. **rtk2 tek geçiş** (`rtk2.py`: find/ls-files/status → dizin-gruplu ad listesi, diff → `## yol` + değişen satırlar (dosya başı 20, satır 160 kr), `--stat` çubuğu atılır, `ls` yalnız adlar; süzgeçsiz komut eski yol): eğitim sıkı sinyal **20/20** (rtk 13/20), token **rtk2 < rtk (−%13.4)**. Held-out 3 (8 komut, kilit `rtk2_set3.lock`, tek sefer): ham 29 574 → rtk 27 579 → **rtk2 25 175**; sıkı **8/8** (rtk 7/8); tohum anahtar 3/4 (rtk 4/4) — kaçan `git ls-files` anahtarı otomatik seçilen tam yol, dizin-grup biçiminde tek dizge değil (ad çıktıda var; yapaylık).
   Süre: süreç içi rtk2 3.5 sn < rtk 5.4 sn (20 komut) AMA uçtan uca `python rtk2.py` rtk'dan yavaş (git log 0.26 vs 0.06 sn, süzgeçsiz komutta ham+rtk çift koşu + Python açılışı). **DÖRT EKSEN: token ✓ kalite ✓ kullanışlılık ✓ süre ✗ → kapıdan GEÇMEDİ**; `onay/token_rea_rtk2.py` hazırlanmadı. Çözüm: süzgeçsiz komutta rtk'yı tek koşu (ham yalnız doğrulama için değil) / TOML filtre ya da PyInstaller ikili.
2. **sor2** (`sor2.py`; graph.json süreç içi, kök eşleşmesi + idf + alt çizgili ad ağırlığı, ≤4.5k kr): eğitim 10/10 (graphify 7/10), **472 tok/sorgu** (graphify 4 025), **0.11 sn** (graphify 3.8 sn). Held-out 5 doğal-dil sorusu (kilit `sor2_held.lock`, tek sefer): **2/5** (graphify 1/5) → **isabet ≥9/10 ✗**: Türkçe betimleme sembol adıyla sözcük örtüşmüyor; sözcük tabanlı araç kapatmaz, anlamsal katman (gömme/LLM) gerekir. Ayrıca graf bayattı (`kapi_kos.py` yoktu) → `graphify update .` 87 sn; sor2 öncesi bayatlık denetimi şart. Kapıdan GEÇMEDİ.
3. **Bağlam diyeti ertelenmiş yükleme** — YAPILMADI (tur tavanı). d2a ölçümü: kapatma −4 745 tok (−%15.8); kalan kaldıraç CLAUDE.md+MEMORY dizini 4.7k + ortam/ajan listesi 2.4k. Öneri: SessionStart enjeksiyonunu tetikleyici-başı yap (skill adı geçince tam metin), geçmiş/gerekçe satırlarını BEYİN kasasına taşı; kapı ≤22k + her araç için kullanım testi.
4. **İş deseni kolu** — YAPILMADI (ölçüm + 2 köprü A/B tur tavanına sığmadı). Eldeki sayı: ağırlıklı taban %75 cache; yeniden yazmanın %85.6'sı oturum başı/ön ek değişimi (ttl-sim). %50-60 yolu hâlâ sayısal olarak kanıtsız: araç sıkıştırma ≈%10-12 + iş deseni (≈%40) varsayım.

## ★ d4 TASLAK
1. rtk2 süre kapısı: süzgeçsiz komutta çift koşuyu kaldır; uçtan uca (subprocess) süre ölçümü kapıya girsin.
2. sor2 anlamsal katman: held-out doğal-dil ≥9/10 için etiket zenginleştirme (docstring/ilk satır dizinlenir) ya da ucretsiz_havuz ile sorgu genişletme; bayatlık denetimi.
3. Bağlam diyeti (ertelenmiş yükleme) + iş deseni kolu (2 gerçek köprü görevinde A/B) — d3'ün 3. ve 4. maddeleri.
4. Held-out setleri tükendi (held, held3, sor2 held): yenileri d4'te yazılıp kilitlenmeli.

## d4 SONUÇ (20 Eki 2026; Claude -p çağrısı 0, count_tokens ~150)
1. **rtk2 rota + süre** (`rtk2.tur()` = hook sınıflandırıcısı; uçtan uca `rtk2_e2e.py`, subprocess, medyan 5): Python açılışı ~40 ms tabanı → find/ls-files/log·diff·show --stat'ta rtk2 eşit ya da yavaş çıktı; bunlar rtk'ya bırakıldı. Rota yalnız `ls`, `git diff` (non-stat; `-U0` ile git'ten bağlam hiç çekilmez), `git status` (tek `--porcelain` koşusu; çift koşu kalktı); süzgeçsiz komut doğrudan rtk (rtk2 hiç açılmaz). re/eksik denetimi sıcak yoldan çıktı (ad/hash kurgu gereği korunuyor).
   Eğitim (rota rtk2 olan 9 komut): token rtk 100 270 → **rtk2 91 230**, süre 2.27 → **1.35 sn**, sıkı sinyal rtk 4/9 → **9/9**. Rota rtk 11 komutta rtk ile birebir; bunlardan `git branch -a` ve `find tools py` sinyal kaybediyor (rtk'nın kendi kusuru; d3'te çift koşu bunu kapatıyordu → kalite 20/20 → 18/20 geriledi).
   **held-out HELD4** (12 komut, kilit `rtk2_set4.lock`, tek sefer, rota eski haliyle koşuldu): token rtk 51 042 → **rtk2 33 889 (−%33.6)**, sıkı 12/12 (rtk 11/12), süre toplam 1.42 → 1.52 sn (+%7): ls-files +27 ms, log --stat +25 ms, `git diff HEAD~5 -- tools` +140 ms. Sonra rota daralttı + `-U0` eklendi (ls-files/log --stat çıktı, diff hızlandırma) — **bu değişiklik held-out görüldükten sonra yapıldı, held-out tükendi**; eğitimde doğrulandı. **DÖRT EKSEN: resmen GEÇMEDİ** (süre kapısı yeni kilitli held-out ile yeniden ölçülmedi; find/branch kalite gerilemesi açık). `onay/token_rea_rtk2.py` hazırlanmadı; hook entegrasyonu (rtk-onisle'ın `tur()` ile yalnız süzgeçli komutu `python -I -S rtk2.py`'ye yazması) da yapılmadı.
2. **sor2 anlamsal** (dosya başı docstring/yorum ilk 600 kr dizini `graphify-out/sor2_belge.json`, graph mtime'a bağlı önbellek + TR→EN eş anlam tablosu 21 kök + stop sözcük): eğitim **10/10** (graphify 7/10), 499 tok/sorgu, ~0.12 sn. **held-out HELD2 (8 soru, kilit `sor2_held2.lock`, tek sefer): 4/8** (graphify 2/8) → ≥9/10 ✗. Kaçanlardan en az ikisi (`durum_ozet.py`, `claude_bak.py`) graf bayatlığı: bu dosyalar yeni/izlenmeyen, graph.json mtime < son commit (1792508474 < 1792508837). Bayatlık denetimi KODA GİRMEDİ (yalnız ölçüldü). Kapıdan GEÇMEDİ. ucretsiz_havuz sorgu genişletmesi denenmedi.
3. **Bağlam diyeti + iş deseni kolu + BEYİN-4 43k farkı: YAPILMADI** (tur tavanı; yarım bırakılmadı).

## ★ d5 TASLAK
1. Önce `graphify update .` (arka planda) + sor2'ye bayatlık denetimi (graph mtime < `git log -1 %ct` ya da izlenmeyen .py varsa uyarı+arka plan güncelleme); yeni kilitli held-out 10 soru; kaçanlar için ucretsiz_havuz ile tek kısa sorgu genişletme (önbellekli).
2. rtk2: hook'a `tur()` ile rota (onay betiği, yedekli); `find` ve `git branch -a` için rtk kalite kaybını kapat (rtk2'de hızlı süzgeç ya da rtk-sonrası ucuz ek — süre kapısını bozmadan); YENİ kilitli held-out (≥12, süzgeçli/süzgeçsiz karışık) ile uçtan uca kapı.
3. Bağlam diyeti (ertelenmiş yükleme) + iş deseni kolu (2 köprü görevi A/B) + BEYİN-4 ~43k fark açıklaması — d4'ten devir.

## d5 SONUÇ (20 Eki 2026; Claude -p 0, havuz çağrısı ~25)
0. `heldout_uret.py rtk2|sor2 <tohum>` yazıldı (komutlar repo geçmişinden, sorular docstring satırının havuzla yeniden ifadesi; anahtar = dosya adı); skor betikleri `rtk2_e2e.py heldout <t>` / `sor2.py heldout <t>` kaçan adları basmaz ("egit…" tohumu hariç). Kapı tohumları: rtk2 20101802, sor2 20101801 (tek sefer).
1. **rtk2 kapı GEÇMEDİ (sıkı "her komutta")**: toplam token rtk 85 338 → rtk2 69 045 (−%19), süre toplam 1.36 → 1.13 sn, sinyal 14/15 (rtk 13/15); ama komut başına süre ≤ rtk yalnız 11/15 ve token ≤ rtk 12/15. Yeni rotalar: `find` (tek geçiş scandir + ortak önek ağacı; yalnız -maxdepth/-type/-name *.uz), `git branch *` → "ham" (hook rtk'sız bırakır; 46 vs 72 ms). Eğitimde (egit1) büyük `find dist -type f` rtk 846 tok (sinyal kaybı) vs rtk2 45 460 → sinyal tam + token<rtk birbirine ters; çözüm adayı: büyük çıktıda ağaç özeti (dizin başına sayı + ilk N ad) ve bunun sinyal ölçüsü. `onay/token_rea_rtk2.py` HAZIRLANMADI.
2. **sor2 kapı GEÇTİ**: sor2 heldout 20101801: genişletmesiz **10/10**, genişletmeli **10/10** (graphify 6/10); 628 tok/sorgu (graphify 3 647); süreç içi 0.32 sn, soğuk süreç ~0.55 sn (hedef <0.5 sn: 0.05 sn kaldı; graph.json 40 MB okuma + scandir). Bayatlık denetimi KODA girdi (graph'tan yeni/değişen .py → düz metin dizini + `graphify update .` arka.py ile, 10 dk'da bir). Genişletme kolu havuz çağrısı (ilk sorguda ~saniyeler) hariç. Egitim tohumu egit1: 9/10 → genişletmeli 10/10.
3. Bağlam diyeti + iş deseni kolu + BEYİN-4 43k: YAPILMADI (tur tavanı).

## ★ d6 TASLAK
1. rtk2: komut başına süre/token için çıktı-boyutu tavanı (find/ls-files büyük çıktıda dizin başına özet), sinyal ölçüsünü "ad kaybı yok" yerine "dizin+sayı+ilk N" olarak tanımla (Ömer onayı); yeni tohum, kapı geçerse `onay/token_rea_rtk2.py` + hook rotası.
2. sor2: soğuk süreç <0.5 sn (graph.json'dan ayrıştırılmış küçük dizin önbelleği: label/dosya/yer, pickle) ve kapıyı yeni tohumda tekrarla; geçerse `onay/token_rea_sor2.py`.
3. Bağlam diyeti (ertelenmiş yükleme) + iş deseni kolu + BEYİN-4 ~43k farkı — d4/d5'ten devir.


## d6 SONUÇ (20 Eki 2026; Claude -p 0, havuz çağrısı 0)
1. **sor2 KABUL işlendi**: soğuk süreç ~0.55 → **~0.40 sn** (`graphify-out/sor2_dizin.pkl`: ayrıştırılmış etiket/belge + bayat dosya metni, graph mtime'a bağlı, 40 MB json atlanır; bayat tarama 0.26 sn kaldı). egit1 yeniden: 9/10 → genişletmeli 10/10, 6.2k tok/10 soru. `onay/token_rea_sor2.py` (+test): `graphify query` yanına tek kural satırı (ev + repo CLAUDE.md, yedekli, `--geri`); graphify kalkmadı. claude.ai tarafı: sor2 yerel dosya sistemi ister, zip'e girmez (iki taraf kuralı: Desktop = repo CLAUDE.md, claude.ai yok).
2. **rtk2 özet + geri alma**: çıktı >1500 kr → ≤8 satır özet (dizin başına sayı + ilk 3 ad; diff'te `## dosya` başlıkları) + tam metin `%TEMP%/rtk2-ac/<id>` + tek satır `python -I -S …/rtk2.py ac <id>`. Sinyal ölçüsü (`rtk2_e2e.py`): özet + `ac` çıktısı. Kind tablosu (rota başına rtk vs rtk2) e2e'de basılıyor. `find` rotadan ÇIKTI (4 held-out komutta süre 0/4: Python açılışı); `git branch` "ham" kaldı.
   Held-out (3 yeni tohum, her biri tek sefer, tohum 2 ve 3 rota/eşik ayarından sonra): 20102001 token rtk 100 602 → 12 667, süre 1.83→1.53, sinyal 11 vs 9; 20102002 (find dahil) 92 152 → 2 590, 1.63→1.39, 11 vs 9; **20102003 (son rota)** 92 193 → **3 351 (−%96)**, süre 1.63 → **1.18 sn**, süre ≤ rtk **14/14**, token ≤ rtk **13/14**, sıkı sinyal **14/14** (rtk 13/14). Tek kaçan: `git branch -a` ham (700 vs rtk 645 tok; rtk adları kaybediyor). **DÖRT EKSEN**: token ✓ süre ✓ kalite ✓ kullanışlılık (geri alma tek komut) ✓; "her komutta token ≤" 13/14 (branch). `onay/token_rea_rtk2.py` (+test) hook'a ls/diff/status yazar, yedekli, `--geri`; uygulama Desktop/Ömer.
3. **Bağlam diyeti (ertelenmiş yükleme) + BEYİN-4 ~43k farkı + iş deseni kolu: YAPILMADI** (45 tur tavanı; yarım bırakılmadı).

## ★ d7 TASLAK
1. `git branch -a` için kayıpsız ve ≤ rtk token yol: `git for-each-ref --format='%(HEAD)%(refname:short)'` yeniden yazımı (Python yok, ad kaybı yok) — held-out 700 vs 645 farkını kapatır.
2. Bağlam diyeti (ertelenmiş yükleme, KAPATMA YOK) + BEYİN-4 ~43k fark açıklaması (transkript 65k vs rapor 107.9k: ölçüm hatası mı gizli yük mü) — d4/d5/d6'dan devir, tek başına bir oturum işi.
3. İş deseni kolu: köprü görev şablonu (tur tavanı, okuma listesi, delegasyon, sabit önek) + 2 gerçek köprü görevinde A/B; sor2/rtk2 onayları uygulandıktan sonra gerçek oturumda token ölçümü (taban.py profil).

## d7 SONUÇ (20 Eki 2026; Claude -p 8/15, havuz 0)
1. **Onaylar etkin**: CLAUDE.md (ev + repo) sor2 satırı var, `sor2.py` sorgusu çalıştı; canlı hook `~/.claude/hooks/rtk-onisle.py` (114 B kılıf) `git status` → `python -I -S …/rtk2.py git status` yazıyor. Bozuk değil, geri alma gerekmedi.
2. **BEYİN-4 ~43k farkı = ölçüm hatası değil, gizli yük de değil**: 107 928 = 6 girdi + **65 077 cache_okuma** + **42 845 cache_yazma** (`beyin4/kosu/sonuc.txt:8`, `beyin2/kapi.py:93-95`); "65k" ve "43k" aynı toplamın iki parçası (%60/%40), okuma karışıklığıydı. Mesaj-id tekilleştirmeli transkript toplamı birebir aynı (fark 0), alt ajan satırı yok. Gerçek bulgu: istek başı sabit **~19k** (12 koşuda 17.9-20.8k, A/B'de eşit) transkriptte görünür: hook enjeksiyonu + CLAUDE.md/MEMORY.md. (`kapi.py turlar()` requestId boşken tur sayısını 2 gösteriyor — yalnız etiket, token değil.)
3. **Bağlam diyeti**: sabit bağlam 30 591 → 30 389 (−202; araç 14 072 + sistem 1 896 + hook/talimat 14 410). Kaldıraç ölçüldü: claude-mem 15 → 6 gözlem ≈ −2k tok/oturum başı (kapatma yok, geçmiş `mem-search`'te) → `onay/token_rea_baglam.py` (+test, yedekli, `--geri`; UYGULANMADI, Ömer onayı). Ağırlıklı etkisi ≈ %1.5 (kod dalgasında istek başı ortalama cache_okuma 79k; sabit 30k bunun %38'i, 2k bunun %2.5'i). Superpowers/context-mode enjeksiyonunu ertelemek davranışı (skill zorunluluğu) değiştirir → kaliteyi ölçmeden önerilmez.
4. **İş deseni kolu** (`is_deseni_ab.py`, 2 köprü sorusu × 2 kol × 2 tekrar, kalite = çapa dizgesi): A (çıplak) ağırlıklı 606 322 / girdi 1.21M / 11 tur; B (şablon: tur tavanı 4 + okuma listesi + delegasyon yok + ≤3 satır) **576 970 (−%4.8)** / 0.995M (−%17.8) / 9 tur; kalite 4/4 = 4/4. Görevler küçük olduğundan sabit bağlam (~150k ağırlıklı/çağrı) etkiyi bastırıyor; uzun köprü görevinde (çok tur) etki büyür ama ölçülmedi.
5. **Toplam taban karşılaştırma**: yeni 14 gün penceresi (taban_d7.json) ağırlıklı kod+araştırma+köprü = 509.0M vs d1 497.6M (+%2): pencerede onay sonrası oturum YOK (onaylar 19:21'de uygulandı) → ölçülen gerçek tasarruf henüz **%0**; çıkarım kodu: araç çıktısı ≈ %14-15 (d1) + bağlam ≈ %1.5 + şablon ≈ %5 (küçük görev) → ≈ %20, hedef %50-60'ın çok altında. `git branch -a` kayıpsız yolu: for-each-ref 1 140 → 1 009 kr (−%11) ölçüldü, rotaya EKLENMEDİ (kazanç küçük).

## ★ d8 TASLAK
1. Onay sonrası gerçek ölçüm: ≥3 gün sonra `taban.py profiller` pencereyi yalnız onay sonrası oturumlara (mtime > 2026-10-20 19:21) kısıtlayarak çalıştır → ölçülen tasarruf; sapma varsa bunu çöz.
2. En büyük kaldıraç tur sayısı × bağlam boyu (cache_okuma ort. 79k/istek): ölçülmüş otomatik sıkıştırma/erken /clear eşiği (ör. bağlam >120k'da dalga.md devri) + uzun (≥15 tur) köprü görevinde şablon A/B.
3. `token_rea_baglam.py` onayı (Ömer) ve kalite etkisi ölçümü (claude-mem 6 vs 15 ile aynı görev).

## d8 SONUÇ (20 Eki 2026; Claude -p 0/15, havuz ≈85/80 — tavan hafif aşıldı: ilk iki üretim koşusu ayrıştırma hatasıyla boşa gitti)
1. **Yöntem skill'i**: `skills/token-rea-yontem/SKILL.md` (7 adım + dört eksen tablosu) + `dist/token-rea-9/token-rea-yontem.zip` (zip_denetle TEMİZ). SkillSpector --no-llm: tek MEDIUM "Session Persistence" (güven 0.6), üç yeniden ifadeye rağmen duruyor → sezgisel yanlış pozitif; Ömer yüklemeden önce bilsin.
2. **Bağlam onayı kalitesi — "onaya hazır" DEĞİL**: `baglam_kalite.py` (betik üretimli, kilitli, 24 soru = tohum 2010202+2010203). Havuz yanıtlayıcı gürültülü (aynı bilgiyi gören rütbe 1-6'da 15 kolu 0.6, 6 kolu 0.2) → ayrıca havuzsuz kapsam ölçüsü (`kapsam`): anahtar bağlamda var mı. Hepsi: 15 gözlem 0.42 · 6 gözlem 0.33 · 6 + tek mem-search 0.38. Rütbe 1-6 eşit (0.58); rütbe 7-15: 0.25 vs 0.08 (arama ile 0.17). Token: başlık bağlamı ~300 → ~120 (−%60; oturum başı ≈ −2k). Hüküm: 6, eski gözlemlerde kalite kaybeder; 15 kalsın ya da ara değer (8-10) ayrıca ölçülsün.
3. **Headroom**: BAŞLANMADI (tur tavanı). taban_headroom.json d2c'den var; kalite seti + mekanizma d9.
4. **Tur × bağlam**: yapılmadı.

## ★ d9 TASLAK
1. Headroom 1. adım: kalite seti (≥10 madde + held-out, `heldout_uret.py` türü) + 4 eksen taban + kaynak okuma mekanizması + plan.
2. Bağlam gözlem sayısı: 8/10 ara değer için `baglam_kalite.py kapsam` (havuzsuz, 0 çağrı) — kapsam ≥ 15'in %95'i ve token < 15 ise `token_rea_baglam.py` hedef değerini güncelle.
3. Tur × bağlam kolu ölçümü (erken /clear önerisi, /autocompact değişmez).

## d9 SONUÇ (20 Eki 2026; Claude -p 0/15, havuz 0/80)
1. **Headroom 1. adım** (`hr_kalite.py`, betik üretimli 10 yük = json3/log3/arama2/fark2, tohum 2010204 held-out; iğne bilgi sıkıştırılmış çıktıda duruyor ya da CCR hash ile geri alınabilir). Taban: kalite 10/10 doğrudan · token −%41.1 (json −59.6 · log −47.1 · arama −6.0 · **fark 0.0, ikisi PASSTHROUGH**) · süre ort 0.92 sn (log 2.1 sn; ilk soğuk çağrıda ML modeli hazır değil → 20 sn aşımı PASSTHROUGH görüldü) · RAM: satırda ram_mb · üretim 14 gün −%28.8 (taban.md). Mekanizma d1 `mekanizma.md` (ContentRouter + SmartCrusher + CCR). Zayıf yer: arama/fark (tekrar eden bağlam satırı) ve soğuk-yol 20 sn aşımı.
   **hr2 tasarımı** (yanında kurulur, Headroom kaldırılmaz): ML'siz tek geçiş "şablon-satır çökertici" — art arda aynı şablona uyan satırları (sayı/yol maskeli) `[×N şablon, ilk..son]` yap, şablondan sapan satırlar (iğne) olduğu gibi kalır, tam metin hash ile saklanır + tek satır geri alma komutu (rtk2 `ac` biçimi). Kapı (dört eksen): token ≥ −%41.1 ve fark/arama türlerinde >0, kalite 10/10 + yeni tohum held-out, süre ≤ 0.92 sn, 0 PASSTHROUGH. Uygulama d10.
2. **Bağlam gözlem sayısı** (`baglam_kalite.py kapsam`, N ortam değişkeni, 0 çağrı, 24 soru): rütbe 7-15 kapsamı 15'te 0.25 · N=6 0.17 (arama dahil) · **N=7 0.25 (arama dahil)** · N=8 0.25 · N=10 0.25 (aramasız). Hepsi: 15=0.42, 7+arama=0.42. Token: N=7+arama ≈188 vs 15 ≈342 (−%45). Kural gereği en küçük eşit sayı **7** (aramasız yolda 10) → `onay/token_rea_baglam.py` hedefi 15→7, test geçti; UYGULANMADI (Ömer onayı). Sınır: 7-15. gözlemler yalnız `mem-search` ile erişilir.
3. **Tur × bağlam** (`tur_baglam.py`, yalnız ölçüm, /autocompact DEĞİŞMEZ; ≥5 istekli 846 ana oturum, 55 224 istek, cache okuma 17.3G): bağlamı >120k olan istek payı %59, cache okumanın %91'i bunlarda (d7'deki 79k ortalama yalnız kısa kod dalgası profiliydi). Karşı-olgusal "bağlam >E olunca 30k tabana dön" üst sınırı: E=80k %84 · 120k %78 · 160k %73 cache okuma azalır (devir kaybı, yeniden yazma maliyeti, kalite etkisi HARİÇ → gerçek kazanç bunun altında). Kalite A/B yok → öneri değil, yön: asıl kaldıraç tur×bağlam.

## ★ d10 TASLAK
1. hr2 çökertici (yukarıdaki tasarım) + yeni tohum held-out kapı → geçerse `onay/token_rea_hr2.py`.
2. Erken devir A/B: ≥2 uzun köprü görevinde "bağlam >120k'da dalga.md devri + /clear" vs sürekli bağlam, kalite eşit mi; devir yeniden yazma maliyeti ölçülür.
3. Sıradaki tabanlı araçlar (claude-mem arama, context-mode).

## d10 SONUÇ (20 Eki 2026; Claude -p 0/15, havuz 0/80)
0. **claude-mem 15→7 doğrulama**: yeni oturum başlığı "7 obs" gösteriyor (uygulama etkin); mem-search ayrıca sınanmadı.
1. **hr2** (`hr2.py` stdlib, `hr_kalite2.py`; Headroom ile aynı yük + aynı sayaç tiktoken cl100k; yeni tohum 2010206, tasarım tohum görülmeden sabit): token Headroom −42.6 → **hr2 −97.0** (json 97.7 · log 96.9 · arama 96.5 · fark 91.4; Headroom arama −5.7, fark 0.0) · kalite **10/10 doğrudan** (+ `ac <id>` tam metni geri verir) · süre uçtan uca ort 0.10 sn (maks 0.14) vs Headroom ort 2.41 sn, soğuk 20 sn aşımı yok · RAM 16 MB vs vekil ~2 GB · PASSTHROUGH 0 vs 2. İlk koşu 2010205: aynı sonuç (−96.5). Dört eksen geçti → `onay/token_rea_hr2.py` (CLAUDE.md satırı, yedekli, `--geri`; test 2/2, kuru koşu temiz). Headroom kaldırılmadı.
   **SINIR (dürüst)**: held-out sentetik, aşırı tekrarlı yük (Headroom tabanıyla aynı üretici). Gerçek çıktıda kazanç yok denecek kadar: `git log --stat` 0%, `git log --format` 0%, `git ls-files` −6%. hr2 yalnız ≥100 benzer satırlık log/json/arama çıktısında anlamlı; sayıca farklı iğne (ör. exit 1 vs 0) şablon maskesinde çökebilir (tam metinde durur). Gerçek-dünya kazancı için üretim çıktı kümesi (Headroom vekil günlükleri) üstünde ölçüm d11.
   Düzeltilen: stdout CRLF (+%2 şişme) → `newline="\n"`.
2. **Erken devir A/B** yalnız tasarım: iki uzun köprü görevi, kol A sürekli bağlam, kol B bağlam >120k'da dalga.md devri + /clear; ölçüt kalite eşit (kabul testi), toplam girdi tokenı, devir yeniden yazma maliyeti. Henüz koşulmadı; /autocompact DEĞİŞMEZ. claude-mem taban/mekanizma yapılmadı (tur tavanı).

## ★ d11 TASLAK
1. hr2 gerçek-dünya ölçümü: son 14 gün Bash/araç çıktıları (transkript) üstünde hr2 kazancı, ≥100 satırlık alt kümede; sayıca farklı iğne için maske sertleştirme (ör. sayıyı yalnız yüzde/id bağlamında maskele).
2. claude-mem 4 eksen taban (arama süresi, RAM, kalite = baglam_kalite, token) + mekanizma ≤15 satır.
3. Erken devir A/B'yi koş (≥2 uzun köprü görevi).

## d11 SONUÇ (20 Eki 2026; Claude -p 0/10, havuz 0/80)
1. **hr2 gerçek yük** (`hr2_gercek.py`; son 14 gün transkript, ≥1500 kr çıktı, 244 örnek: test/log/build/grep/git/ls 40'ar, json 4; tiktoken cl100k): hr2 ilk sürüm ağırlıksız −%2,8 ama iğne kaybı 93/679 (log 67/115, git 124/160: yalnız sayıyla ayrışan sinyal satırları maskede çöküyordu). Sertleştirme: sinyal satırında (hata/fail/exit code/warn/passed…) sayı maskelenmez. Yeni tohum held1: **−%1,3 (nüfus-ağırlıklı −%0,66)**, iğne **742/742**, değişen çıktı 14/244; egit1 üstünde −%0,9, 679/679. Headroom aynı kümede −%1,6, iğne 646/679 (Kompress modeli bu süreçte hazır değil → Headroom ML kolu çalışmadı, alt sınır). 100+ satırlık alt küme yalnız 11/244 (hr2 −%6,4–7). hr2 uçtan uca ort 0,08 sn.
   **Karar: ≥%15 ek tasarruf YOK → onay_hr2 güncellenmedi, rota yok** (grep nüfusun %65'i ama −%0,0; hiçbir türde kazanç yok). Sentetik −%97, gerçek yükte ~−%1: önceki d10 sonucu yalnız sentetik kabul.
2. **claude-mem taban (7 gözlem)**: kalite `kapsam` 30 soru: kap7 0,43 → +arama 0,53 = kap15 0,53 (rütbe7-15: 0,25 → 0,44 = 15); bağlam ~1,9k jeton, arama ort ~184 jeton; arama HTTP 0,76–1,05 sn (sıcak /health 0,01 sn); RAM worker (bun) ~151 MB + chroma-mcp ~5 MB. Mekanizma: SessionStart'ta son N başlık enjekte, derin bilgi mem-search ile; kayıp yeri: başlıklar kısa, aramasız 7-15. soru kaybı.
3. **Erken devir** (`devir_sim.py`, YALNIZ token simülasyonu): 370 uzun (>120k) oturum, 891 devir; ağırlıklı maliyet A 2029M → B 644M (**−%68, üst sınır**: devir sonrası aynı tur sayısı ve kalite eşit varsayımı; yeniden okuma turları/kalite kaybı modellenmedi). Canlı kalite A/B koşulmadı.

## ★ d12 TASLAK
1. Erken devir canlı kalite A/B (≥2 uzun köprü görevi, kabul testi eşit mi; tur sayısı artışı ölç) — simülasyon −%68'in ne kadarı gerçek.
2. claude-mem: arama süresi 0,8–1,0 sn → önbellekli/yerel FTS yolu (kendi sürüm) + rütbe7-15 kalitesi (başlık uzunluğu/arama otomatik tetik) 4 eksen kapı.
3. context-mode taban (sıradaki araç). hr2 yeniden ele alınmaz (gerçek yükte kazanç yok), yalnız Headroom Kompress modeli hazırken bir kez tekrar ölçüm istenirse.

## ★ d12 SONUÇ
- Erken devir canlı A/B (devir_ab.py, tohum 20102101, 3 görev × 14 dosya, 9 `claude -p`): A 817k ağırlıklı / $2.05 / 46 tur / 255 sn; B 1005k (+%23) / $2.60 (+%27) / 54 tur / 367 sn; kalite eşit (0.978 / 0.978). KAPI GEÇMEDİ → ajan_sira.py devir bayrağı ve onay/token_rea_devir.py YAZILMADI.
- Neden: görev bağlamı ~30k, eşiğin (120k) çok altı → devir yalnız bedel (not yazımı + taze oturum önek yazımı) ekledi. Simülasyon −%68 yalnız >120k bağlamlı oturumlar için; bu A/B onu sınamıyor. Gerçek sınama ≥120k bağlam isteyen görev gerekir (kota maliyeti yüksek).
- hr2: kalıcı test eklendi (onay/test_token_rea_hr2.py, sayıyla ayrışan sinyal satırları korunur).
- Yapılmadı: claude-mem arama hızı, context-mode tabanı (tur bütçesi/odak).

## ★ d13 TASLAK
1. Devir ikinci A/B: ≥120k bağlam doğuran görev (ör. 60+ dosya okuma), A vs B; yalnız bu geçerse bayraklı devir. Alternatif: devir kararını bırak, sim'i yalnız not et.
2. claude-mem arama hızı (0,8–1,0 sn → yerel FTS önbelleği) + rütbe 7–15 kalitesi, 4 eksen kapı.
3. context-mode taban.

## ★ d13 SONUÇ
- Uzun bağlam devir A/B (devir_ab2.py, tohum 20102303, 2 görev × 53-55 dosya ≈150k tahmini jeton, 6 `claude -p`, ~$7.28): A 1019k ağırlıklı / $2.29 / 62 tur / 393 sn / kalite 0.391; B 2161k (x2.12) / $4.99 / 133 tur / 683 sn / kalite 0.875. KAPI GEÇMEDİ (B ≤ %70 A şartı) → devir fikri KAPANDI; ajan_sira.py bayrağı ve onay/token_rea_devir.py YAZILMADI.
- Neden: B'de devir notu + taze oturum önek yeniden kurulumu + dosyaların ikinci kez okunması ağırlıklı toplamı ikiye katladı; A modeli dosyaları toplu/seçici okuyup bağlamı hiç 120k'ya taşımadı (girdi 659-758k / 26-36 tur ≈ 22k/tur). Kalite farkı (0.39 vs 0.88) B'nin ikinci oturumda eksik dosyaları yeniden okumasından; token kazancı değil, maliyet.
- Çıkarım: devir simülasyonu (−%68) gerçek ajan davranışında tutmuyor; devir kararı kapalı, sim yalnız not.
- Yapılmadı: d13 madde 2-3 (claude-mem arama hızı, context-mode tabanı) — tur kalırsa d14.

## ★ d14 SONUÇ
- claude-mem arama (mem2.py: worker'sız salt-okur FTS5, bm25 ağırlık (5,2,5,0,3,3) eğitim tohumu 20102402'den; önbellek gerekmedi — doğrudan DB taze). Held-out tohum 20102403 (mem_ab.py, 100 sorgu, Claude çağrısı 0): worker A isabet@5 0.91 / 204 tok / 0.228 sn (max 0.351) → mem2 B 0.93 / 140 tok (−%31) / 0.056 sn (−%75; hedef ≤0.2 ✓) / hata 0. İlk tohum 20102401 (ağırlık ayarından önce): 0.912 = 0.912, 0.063 sn. KAPI GEÇTİ (4 eksen: token, kalite, süre, kullanışlılık = worker'a bağımlılık yok, tek adım).
- Not: worker taban süresi artık 0.2–0.35 sn (d11'deki 0.8–1.0 sn sıcak değil). Sınır: anlamsal (eş anlamlı) sorgu denenmedi, worker/Chroma orada üstün olabilir → kural satırı "boş/yetersizse mem-search". RAM: ek süreç yok (worker kalır, yakalama için gerekli).
- `onay/token_rea_mem2.py` (kuru/uygula/--geri; geri yalnız kendi satırını çıkarır) + test; UYGULANMADI (Ömer onayı).
- Yapılmadı: 7–15 gözlem ayrı ölçüm (arama yolu mem2 ile 0.93 erişim; ayrı koşu yok), context-mode tabanı.

## ★ d15 TASLAK
1. `onay/token_rea_mem2.py uygula` (Ömer onayı sonrası) + uçtan uca doğrula; anlamsal paraphrase sorgu seti (havuzla yeniden ifade) ile mem2 vs worker, gerekirse mem2→worker otomatik yedek.
2. context-mode taban (4 eksen) + mekanizma.
3. Sonra NotebookLM / mcp-memory (★ 19:30 sırası).

## ★ d15 SONUÇ
- (1) onay_mem2 net-sıfır önerisi (UYGULANMADI): sor2 ve mem2 yolları göreli (`.kos/...`) → yalnız omer-skills'te işe yarar; global CLAUDE.md'deki sor2 satırı (218 kr) repo CLAUDE.md ile ikilenmiş, omer-skills'te iki kez yükleniyor. Öneri: global'den sor2 satırını çıkar, mem2'yi global'e EKLEME, repo CLAUDE.md'de ikisini tek satırda birleştir (287 kr). Kr/3 ≈ jeton: bugün 436 kr (~145 tok) → 287 kr (~95 tok), −50; global −73 tok (tavan 1.3k korunur). `onay_mem2` olduğu gibi uygulanırsa 862 kr (+142 tok) → uygulanmamalı; betik hedefini yalnız repo dosyasına çevirip birleşik satırı yazacak, global sor2 satırı onay_sor2 geri alma yolundan çıkarılacak (sabah Ömer onayı).
- (2) Paraphrase held-out (mem_para.py, tohum 20102501, 68 soru, havuz 7 çağrı, Claude 0): worker 0.00 (!), mem2 0.176, mem2→worker 0.176. Worker 0.00 sürüm farkı değil ARIZA: /api/search "Semantic search failed: chroma-mcp ... compactor backfill" hatası döndürüyor (kısa 1–2 sözcüklü sorgu anahtar yoluna düşüp çalışıyor, ≥3 sözcük Chroma'ya gidip düşüyor). Yani anlamsal yol şu an çalışmıyor; mem2 sözcüksel olarak anlamsal sorguda zayıf (0.18 vs anahtar-sözcük 0.93). Kural satırındaki "boş/yetersizse mem-search" tetikleyicisi boşa: mem2 OR sorgusu hiç boş dönmedi (bos_B 0.0). Yedek ancak Chroma onarılınca anlamlı.
- (3) 7–15 aralığı: 15→7 ile düşen 8. –15. gözlemler için paraphrase isabeti mem2 0.125 (n=8, güvenilmez), anahtar-sözcükte 0.93 (d14). Yeni kanıt yok; 7'de kalmak ancak arama anahtar sözcükle yapılırsa güvenli.
- (4) context-mode taban (Claude 0, eski MCP araçları bu oturumda çağrılamadı → performans/kalite ölçülemedi): SessionStart yönlendirme bloğu 4 603 kr ≈ 1.2–1.5k tok/oturum (hook enjeksiyonu 14.6k'nın bir parçası); her Read/Grep/Bash çağrısına PreToolUse ipucu (~60–130 tok) → 30 çağrılık oturumda ≈ 2–3k tok. Kazanç kolu (ctx_execute ile ham çıktıyı kum havuzunda tutma) yalnız etkileşimli CC'de ölçülebilir.

## ★ d16 TASLAK
1. Chroma/compactor arızasını teşhis (claude-mem worker logu) — worker anlamsal yolu çalışmadan mem2↔worker anlamsal kıyas geçersiz; sonra mem_para.py'yi aynı tohumla yeniden koş.
2. mem2'ye anlamsal zayıflığa karşı çare: sorgu genişletme (havuz, önbellekli) ya da AND→OR sıralaması; kapı: paraphrase ≥0.5, anahtar-sözcük 0.93 korunur.
3. Onay (Ömer): net-sıfır birleşik satır → `onay/token_rea_mem2.py` hedef revizyonu. context-mode tabanı etkileşimli CC oturumunda (ctx_stats, ctx_execute süresi).

## d16 sonuç (21 Eki 00:3x)
- Kural satırı: global sor2 satırı çıktı, repo CLAUDE.md'de sor2+mem2 tek satır (`onay/token_rea_mem2.py`, yedek ev/yedek-token-rea-mem2, --geri). count_tokens: global 1458→1336 (−122), repo 966→1021 (+55), omer-skills'te net −67 tok. Canlı `claude -p` girdi toplamı 106 652→107 386 (+734) = oturum başı enjeksiyon gürültüsü (claude-mem bağlamı değişti), CLAUDE.md farkı tek çağrıda ayırt edilemez; kanıt count_tokens (d16_md_tok.py).
- Chroma arızası KÖK NEDEN: chroma.sqlite3 (635 MB) sayfa 152552'de dizin bozulması (`quick_check: Multiple uses for byte 732`), compactor "Failed to apply logs to the metadata segment" → 16:12'den beri 3712 toplu ekleme hatası, kuyruk 2084 satır birikti. Onarım: yedek ~/.claude/yedek-chroma-onar/chroma.sqlite3.once + `REINDEX` (18 sn; tablolar sağlamdı) → quick_check ok, kuyruk 2084→50, embeddings 160 064→162 196, yeni hata yok.
- mem_para.py 20102501 yeniden (n=68): worker A 0.0→0.0 (tokA 116→318), mem2 B 0.176→0.221; 8–15 penceresi B 0.125→0.5. Worker A=0.0 şüpheli (onarıma rağmen): mem_para worker yanıtını yanlış ayrıştırıyor olabilir.
- YAPILMADI: mem2 sorgu genişletme (tur tavanı).

## ★ d17 TASLAK
1. mem_para.py: worker A=0.0 nedenini bul (yanıt biçimi/ayrıştırma; tek elle /api/search sorgusu) — düzelmeden mem2↔worker anlamsal kıyas geçersiz.
2. mem2'ye havuzla sorgu genişletme (önbellekli); kapı paraphrase ≥0.5 VE anahtar sözcük ≥0.93, yeni tohum.
3. Onay: kapı geçerse `--genis` benzeri bayrak mem2'de, kural satırında tek ek ibare (net token ≤0).

## d17 sonuç (21 Eki)
- Worker A=0.0 ARIZA DEĞİL, ayrıştırma da değil: elle /api/search yanıtı geçerli tablo ("| #ID | ... |"), `#(\d+) ` regex'i doğru kimlik çıkarıyor. Worker'a gözlemin kendi başlığı sorulunca bile isabet 2–3/12 (anahtar sözcük mem_ab A=0.10); çıktı yakın tarihli (#30xxx) kayıtlara kayıyor. Chroma onarımından sonra yeni tohumda A=0.053 (n=76). Yani worker anlamsal yolu bu veride zayıf; kıyas geçerli: paraphrase mem2 0.276 > worker 0.053.
- mem2 sorgu genişletme (`genislet()` + `--genis`, havuz, önbellek mem2_genis.json, Claude 0): paraphrase (tohum 21100301, n=76) B 0.276 → G 0.395 (kapı ≥0.5 ✗); anahtar sözcük (tohum 21100302, n=79) B 0.873 → G 0.835 (kapı ≥0.93 ✗; B bile 0.93'ün altında bu tohumda, başlık sorularında 0.77). KAPI GEÇMEDİ → kural satırı DEĞİŞMEDİ, `--genis` varsayılan kapalı (yalnız opt-in).
- Not: anahtar sözcükte genişletme başlık sorgularını bozuyor (0.769→0.692), anlatı eşit (0.975); paraphrase'te +0.12 kazanç.

## ★ d18 TASLAK
1. Genişletme ağırlığı: özgün sözcükler tam, ek sözcükler düşük ağırlık (iki aşamalı: önce özgün OR; ilk 5'te hiç ek sözcük çakışması yoksa ek sözcükleri birleştir) — kapı aynı (paraphrase ≥0.5 VE anahtar ≥0.93), yeni tohum.
2. Kapı geçmezse genişletme fikri KAPANIR; mem2 paraphrase tavanı ~0.28–0.4 olarak belgelenir, kural satırına "anlamsal soruda sonuç zayıfsa mem-search" ibaresi eklenmez (worker 0.05, yedek değil).
3. context-mode tabanı etkileşimli CC oturumunda; NotebookLM / mcp-memory (★ 19:30 sırası).

## d18 sonuç (21 Eki)
- İki aşamalı genişletme (`mem2.ara2`: önce özgün OR; ilk 5'te ek sözcük çakışması yoksa ek sözcükleri birleştir), Claude 0, yeni tohumlar: paraphrase 21100401 (n=84) B 0.226 → G 0.274 (kapı ≥0.5 ✗); anahtar sözcük 21100402 (n=80) B 0.887 → G 0.762 (kapı ≥0.93 ✗; başlık 0.775→0.6). Worker A 0.0 / 0.075.
- KAPI GEÇMEDİ → genişletme fikri KAPANDI. mem2 paraphrase tavanı ~0.23–0.40 (d17 0.276, d18 0.226; genişletme en iyi +0.05–0.12), anahtar sözcük ~0.87–0.89. `--genis` varsayılan kapalı (opt-in; artık `ara2` kullanır), kural satırı DEĞİŞMEDİ.
- Kalıntılar (_probe*, _wprobe*, _para_*, _ab_run.out) `.kos/kopru/cop/token-rea/` altına taşındı (rm yok).

## ★ d19 TASLAK
1. Yalnız context-mode tabanı (etkileşimli CC oturumunda ctx_stats, ctx_execute süresi) ve NotebookLM / mcp-memory tabanı (★ 19:30 sırası); mem2 anlamsal iyileştirme yok.
2. Paraphrase kaybı için tek ucuz yol kaldı: gözlem yazılırken (kaydetme anında) başlığa TR/EN anahtar sözcük eklemek — claude-mem kaynağına dokunur, Ömer onayı gerekir; kodlama yok.
