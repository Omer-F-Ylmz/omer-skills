# ATLAS-2 devam (d1 ara, 14 Eki ~19:00)
Görev: .kos/kopru/gorev/atlas-2.md. Yöntem atlas-1 ile aynı.

## Yapılan
- S01 kaçışı (site/3D 2 kaçış = S01 × 2 tekrar): departman-frontend Adımlar 4 "scroll → önce animasyon-atolyesi" diyordu; atölye tarifi yalnız scroll'la belirme (giris-scroll.html), scrub/pin yok. Satır düzeltildi: scroll-driven → `gsap-scrolltrigger`.
- Küme süzgeci `.claude/atlas2/kume.py` → K1.jsonl 121 öğe (94 kartsız), K2.jsonl 292 (288 kartsız; ad regex + alan guvenlik). K12.jsonl birleşik.
- `tools/atlas.py kart --kume <jsonl>` eklendi; arka plan `.claude/atlas2/kart.log` (parti 16, kart.jsonl'a ekler).
- Ölçüm koşucusu `.claude/atlas2/olc.py <set_ad> <id,...>` (zor set `z:Sxx`; ayrıştırıcı yalnız Sxx → id çakışmasın).
- Taban (kitapsız) K1+K2 11 görev: S21,S24,S41,z:S59,S08,S09,S10,S11,S36,z:S42,z:S49 → docs/kutuphane/olcum/2026-10-14-secim-toplu-k12-atlas2-taban-sonra.tsv.
- claude -p: 1 başlatılıp ~1 dk içinde öldürüldü (Zxx id hatası) + taban 1 = 2/3. Kalan 1: kitaplı birleşik koşu.

- TABAN SONUCU: 10/11 ($0.99, son girdi 707k, 13 tur). Tek kaçan S41 ("reel'i izle, hangi aracı gösteriyor, nasıl kurulur") → video-uygula; altın video-izle/video-tarama/video-cli. Kitapta ayrım satırı: tek video izle/anlat → video-izle; aday dosyasına çevir → video-uygula. Tavan 11/11 → artış ancak +1.
- Kart 19:00'da 48/382 (çağrı başı ~3 dk → ~70 dk). Bekleme: `python .kos/kopru/bekle.py .claude/atlas2/kart.log "BITTI|Traceback" 540`. Öldürülürse aynı komut kaldığı yerden sürer (hazır kartlar atlanır).

## Kalan
1. Kart bitince Opus kararı (K1+K2 kartları; karar + kosul alanı, `.claude/atlas/karar.py` biçimi) → katalog_yenile.
2. docs/atlas/video-icerik.md + guvenlik-test.md (≤60 satır: VARSAYILAN · GEREKİNCE · KULLANMA · iş sırası · token ipucu).
3. Atıf satırı: departman-video? / departman-guvenlik / departman-test SKILL.md (tek satır).
4. Kitaplı tek koşu (son claude -p): site/3D 7 (S01,S02,S03,S04,z:S43,z:S46,z:S50 — dikkat: zor S46/S50 ana S46/S50 ile çakışmaz çünkü ana S46/S50 seçilmiyor) + K1/K2 11 → set_ad k12s3-atlas2-kitapli.
5. Kullanım izi sayacı .kos/kopru/atlas_iz.py (salt-okur; transkriptte kitap VARSAYILAN araç adlarını sayar).
6. dist zip (claude.ai) `.claude/atlas/dist.py` · rapor/atlas-2.md · SIRA satırı · commit.

## d1 ara 2 (20:20) — 1–5 BİTTİ (rapor/atlas-2.md), claude -p 3/3 bitti
## d2 ara (20:50) — K3 kitap + dist betiği hazır, kart arka planda
- K3: kume.py K3 (173 öğe, 160 kartsız) → `tools/atlas.py kart --parti 16 --kume .claude/atlas2/K3.jsonl` arka plan (.claude/atlas2/kart3.log, 20:50'de 80/160). docs/atlas/belge-sunum.md yazıldı (ölçüm yok → kabul değil). departman-belge atıf satırı eklendi.
- Kalan sıra: (1) kart3.log BITTI bekle (`python .kos/kopru/bekle.py .claude/atlas2/kart3.log "BITTI|Traceback" 540`; ölürse aynı kart komutu kaldığı yerden) → (2) `python .claude/atlas2/karar3.py` (assert eksik yoksa) → `tools/katalog_yenile` (atlas-2 d1'deki gibi) → (3) commit → (4) `python .claude/atlas2/dist.py` (HEAD'den, dist/claude-ai-25, 4 departman + kitap + kart.jsonl; zip_denetle) → commit. (5) rapor/atlas-2.md + SIRA satırı.
- CC tarafı: departman skill'leri ~/.claude/plugins/marketplaces/omer-skills (GitHub klonu, 18704c6) üzerinden gelir; push yasak → atıf satırları CC'ye push+`/plugin marketplace update` ile ulaşır (ATLAS-1 site-3d atfı da henüz orada yok). Rapora sapma olarak yaz.

Eski kalan: (a) dist zip `.claude/atlas/dist.py` — değişen skill: departman-guvenlik, departman-test-qa, departman-arastirma-ogrenme; zip_denetle temiz; CC tarafı onay betiği. (b) K3 belge-sunum kitabı (ölçüm bütçesi yok → yalnız iş akışı belgesi). (c) atlas_iz.py VİDEO-KISA / TELVE-R2f sonrası tekrar; `video` adı gürültülü, gerekirse `video <altkomut>` deseni.
