# TOKEN-9 — köprü ajanı oturum verimliliği (13 Eki, yalnız ölçüm)

Kapsam: `entrypoint=sdk-cli` + ilk istemde `gorev/<görev>[-dN].kilit` olan 125 oturum (54 görev); 10'u 04:47–04:49 kredi bitişinde 0 jetonla düştü → 115 gerçek oturum. Etkileşimli oturumlar ilk 40 satırda elendi, içerikleri açılmadı. Betik: `tools/olcum/kopru_oturum.py` (kol/token9), ham tablo: `docs/token-9/oturumlar.tsv`.
Birim "ağırlıklı jeton" = input×1 + cache_write×1,25 + cache_read×0,1 + output×5 (input fiyatına göre).

| ölçü (115 oturum) | medyan | toplam / pay |
|---|---|---|
| tur (API isteği) / araç çağrısı / süre | 39 / 45 / 21 dk | tur en çok 82 |
| ilk istek öneki | 77k (p10 49k, p90 79k) | — |
| oturum ağırlıklı jeton | 755k | 100,2M |
| cache_read / cache_write / output / input payı | — | %49 / %28,5 / %16 / %6 |
| cache_write / oturum | 146k | 22,8M ham |
| durum evresi (ilk 10 istek) ağırlıklı | 220k (oturumun %28'i) | — |
| ≥44 araç çağrısına ulaşan (45 kesmesi) | 68 oturum | son bağlam medyan 131k |
| kesik → devam çifti | 42 | devamların durum evresi 9,6M (%9,6) |

Bulgular:
- 45 kesmesinin ek maliyeti toplamın **%4–10'u**: alt sınır = 42 devamın önek yeniden yazımı (~89k × 42 ≈ 3,7M), üst sınır = devamların tüm durum evresi (9,6M). Kesme bağlamı 131k'da sıfırlıyor (devamda istek başı ~86k), yani kesmenin kendisi cache_read büyümesini de frenliyor; net zarar alt sınıra yakın.
- En büyük kalem önek: her oturum ~77k öneki 1,25× yazıp ~38 kez 0,1× okuyor (≈390k/oturum, toplamın ~%45'i).
- Kanca sayacı güvenilmez: sayaç dosyası `CLAUDE_PROJECT_DIR/.claude` başına tek (ortalama 2,8 eşzamanlı oturum); 52 oturumda araç sayısı − kanca sayısı medyan 7, en çok 65 (ör. fable-video 85/20). 73 oturumda kanca iletisi transkriptte hiç yok (wt oturumları olası). Kanca durdurmaz; ≥45'te "DUR" iletisi verir, ajan uyar.

Öneriler (sıralı; kazanç tahmini toplam 100M'e göre, yalnız öneri — kanca/ayar değişmedi):
1. Köprü önekini küçült (77k→50k; görev türüne göre MCP/skill seti, TOKEN-8 hattı): ~%15. Risk: gereken araç eksik kalırsa görev ikinci oturuma taşar.
2. Toplu komut şablonu (durum çıkarma tek Bash: git status/log/diff --stat + devir + SIRA grep; ölçüm-analiz tek betik): oturum başı −5 tur ≈ %7–8. Risk: büyük toplu çıktı headroom'da sıkışır → retrieve turu; çıktıyı sayıya indir.
3. Devam istemine devir notunu göm (Desktop başlatırken ≤10 satır "KALAN/GÜNLÜK/SONRAKİ KOMUT"): durum evresi 10→~3 istek, ~%3–4. Risk: not eskiyse yanlış adım; ilk komut `git log -3` ile doğrulasın.
4. Devir notu sabit şeması (3'ün önkoşulu): KALAN (sıralı) · ARKA PLAN günlük+bitiş eylemi · SON COMMIT · AÇIK KARAR. Kazanç 3'e dahil, risk düşük.
5. Kanca: sayacı session_id anahtarlı dosyaya taşı + eşiği bağlam boyuna bağla (ör. son istek ≥140k ya da 45 çağrı, hangisi önce). Kazanç ölçüm doğruluğu + gereksiz erken kesmeler; risk düşük ama güvenlik/kanca değişikliği → Ömer onayı.
6. Ara kayıt (15 dk) tek turda: rapor+devir Write + tek Bash (SIRA satırı + commit). Medyan oturum 21 dk → ≤2 kayıt; kazanç <%1, risk yok.

Atlanan: alt ajan (sidechain) transkriptleri sayılmadı (ana oturum araç sayısı yalnız); "durum evresi" sabit N=10 varsayımı; ağırlıklar plan limitinin gerçek sayım biçimi değil, göreli.
