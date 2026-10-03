# TOKEN-6c — effort kayması + "diğer" kırılma teşhisi

KARAR: plan kabul, K1 değişikliğiyle (2026-10-03). Ayar değişikliği yok; tek istisna ~/.claude/xhigh.json (oturum başı bayrak dosyası; settings.json'a dokunulmaz).

Kabul:
- K1: A'dan yalnız (a) CC /effort kalıcılık kanıt satırı (b) Headroom yazma yolu YAMA/ANLIK (+ANLIK ise etkilenen değişiklik listesi). xhigh.json + 1 prob: effort xhigh kanıtı + settings.json bayt-eşit. docs/token-6c.md §K1 kullanım satırı.
- K2: B veri + C Headroom kaynağı → olay | kırılma % | taban % | kaldıraç · cache_read-at-break · 2 hipotez · 1 örnek kendim.
- K3: 4 claude -p (açık/kapalı/açık/kapalı), RAM ≥4 GB, sonnet plan modu, OLCUM "8 dosya oku → özetle" → olcum/token-6c-k3.json · §K3.
- K4: kök nedenler · seçenekler · öncelik · %30 haftalık --karsilastir planı.
- Kapanış: mühür eşit · diff-filter=D boş · gitleaks · arşiv · push · ≤8 satır.
- claude -p tavanı 5. Tur 21'de bitmediyse kalan iş + DUR.

Durum:
- Açılış mühürü: scratchpad/muhur-6c.json settings 02372fb94f3e5e29 · mcpServers 23452893b846a828 · hooks a0801fdfd21676e2 · plugin [47,53] · mcp 19 · skill 1054
- HR: ANTHROPIC_BASE_URL var · ENABLE_TOOL_SEARCH var · SessionStart e0d759be42561ee5 (6b ile eşit)
- modelSettings bugün: opus-5-5 xhigh · opus-5 high · fable-5-1 medium
- K1 ✓ e1eeb93: A hüküm YAMA (Headroom yalnız env anahtarı); /effort kalıcı kanıtı bayt 205779411; prob opus-5 → transcript effort xhigh, settings.json bayt-eşit ($0.72). Sapma: probda --model claude-opus-5 (opus-5-5 zaten xhigh, ayırt etmezdi).
- C ✓ (rapor bu oturumda): Headroom CACHE modu, önceki turlar donuk + ham bayta geri yazım (anthropic.py:685-750); aday mekanizmalar cold-prefix recompaction (TTL sonrası, :1596-1628/:2010-2028) ve append-only bozulması (kanıtsız). savings_events'te dönüşüm/konum alanı yok; proxy-6768.log PERF satırlarında istek başı cache_read/tok_inflated var (467 PERF'te 11 inflated). Süreç portu 6768 (statusline 6767'yi yokluyor — K4'te kontrol).
- Arka planda: okuyucu B (K2 veri) · K3 betiği scratchpad/k3.py (bb2wscf03; 4 koşu, --max-turns 12 sapması) → olcum/token-6c-k3.json. claude -p: 1/5 + 4 koşuda.
- K3 betiği 3. koşuda kendi RAM kapısıyla durdu (boş 3.9 GB < 4). Biten: 1 açık + 1 kapalı, ham: scratchpad/k3-1-acik.jsonl, k3-2-kapali.jsonl. olcum json YAZILMADI. claude -p: 3/5 (kalan 2 = K3 koşu 3-4).
- B ✓ (rapor bu oturumda; betikler %TEMP%\s\*.py, scratchpad dışında): 148/22.17 M birebir tuttu. Kök neden kanıtlanamadı. Karıştırıcı ara süre (<60 sn %0.6 → 1800-3600 sn %80 kırılma; önceki yazma 148/148 1h). 123/148'de cr 7.4-8.4k sabit (≈system+tools varsayımı, kanıtsız) → mesajlar baştan kopuyor. Kaldıraç: away_summary 128× · file-history-snapshot 38× · turn_duration/stop_hook 15.7×. compact/temizleme işareti/effort değişimi 0. Headroom ±60 sn ayırt etmiyor (%100 vs %99.9). Hipotez 1: boşta kalma sonrası mesaj başı yeniden yazılıyor (away_summary). Hipotez 2: oturum başı blok değişiyor (4 sn aralıkla kırılma örneği, f3511826:708). Doğrulanacak örnek: edcf592d:649 req_011CfcQdE4FJ1AHEXrBK4GPe.
- TUR SINIRI AŞILDI: onaydan sonra 24 tur (21 sınırı; 5'te bir sayaç bildirilmedi). DUR.
## TOKEN-6c-2 (devam; tur ≤15, 5'te bir sayaç, 12'de DUR; claude -p tavanı 7)
- tur 5/15: örnek edcf592d:649 doğrulandı (640 cr=216573 22:49:39 → 649 cr=7537 cc=203616 23:46:03; ara 56.4 dk < 1h TTL; arada stop_hook/turn_duration/away_summary 22:52:44/queue-operation×2). Soğuk-önek: HEADROOM_COLD_RECOMPACT opt-in (anthropic.py:1614-1618), eşik idle > TTL+60 sn (cold_prefix.py:33,67), TTL CC isteğinden (1h→3600). proxy-6768.log'da "cold-prefix recompaction" 0 satır.
- tur 10/15: K3b arka planda (bl79wd1tq, 35 dk; eşik+2 = 63 dk > 1h TTL → iki kol da TTL'den kırılırdı, ayırt etmez; sapma). claude -p 1h TTL (5m=0). HEADROOM_COLD_RECOMPACT User/Machine yok. CC: awaySummaryEnabled ayarı + CLAUDE_CODE_ENABLE_AWAY_SUMMARY (qKe), settings.json'da yok. Bantlar: ≤1 45/7428 %0.6 · 1–5 23/813 %2.8 · 5–30 68/132 %34 · 30–60 12/3 %80 · >60 0.
- tur 12/15 — DUR (12. tur kuralı). Bitti: K3 json b1b878b · §K2 commit · mühür EŞİT (scratchpad d7f08cfc…/muhur-6c2.json; HR alanları settings.json hash'i içinde, eşit) · diff-filter=D 1b182eb..HEAD boş · repo kodu değişmedi (e1eeb93 yalnız docs) → suite gerekmez.
Kalan iş (6c-2):
1. H3b değerleri: COMPRESSION_CACHE_TTL_SECONDS (server.py:133 import kaynağı) ve config.prefix_freeze_session_ttl varsayılanı → §K2 H3b'ye ekle.
2. K3b: bl79wd1tq bitince olcum/token-6c-k3b.json otomatik yazılır (claude -p 7/7). §K3: aralıksız 2 koşu (9'ar istek, kırılma 0/0, $0.84/$0.63) + K3b sonucu (yalnız açık kolda kırık → H3b güçlenir; ikisinde yok → etkileşimliye özgü H1/H2) → commit.
3. §K4: kök neden durumu · seçenekler (H3b: Headroom oturum TTL'ini ≥3600 ile hizala · H1: awaySummaryEnabled:false / CLAUDE_CODE_ENABLE_AWAY_SUMMARY=0 kanıtı qKe · alışkanlık) tasarruf/risk/kapı · notlar (opus-5-5 xhigh kalıntısı Ömer, xhigh.json · 6767 Desktop ön kapı = ANTHROPIC_BASE_URL hedefi, statusline doğru) · %30 haftalık --karsilastir planı → commit.
4. Kapanış: gitleaks 1b182eb..HEAD · dalga → .claude/dalga-arsiv/TOKEN-6c.md · push (e1eeb93 dahil).
- ek tur 5/10 (17:07): Headroom süreleri okundu — prefix_freeze_session_ttl=600 (proxy/models.py:342; env/CLI bağı yok, yalnız server.py:1095 okur), COMPRESSION_CACHE_TTL_SECONDS=3900 (helpers.py:1449-1454, env HEADROOM_COMPRESSION_CACHE_TTL_SECONDS, ayarlı değil). Desktop argümanı: `proxy --port 6768 --no-http2 --no-rate-limit --log-messages`. NET_COST_POLICY/COLD_RECOMPACT kapalı. K3b 2. istekleri ~17:21-17:23.

Eski kalan iş (6c): B raporu → 1 örnek kendim doğrula → §K2 (tablo · dağılım · 2 hipotez; C ile birleştir) → commit · K3 json → §K3 → commit · §K4 (seçenekler: settings opus-5-5 xhigh kalıntısı, 6767/6768 portu, cold-recompact) → commit · kapanış (mühür eşit · D-boş · gitleaks · arşiv · push).
- ek tur 8/10: K3b iki kolda kırılma yok (H3b zayıf) · §K3 e707750 · §K4 ff189ac · mühür EŞİT · D boş · gitleaks temiz → arşiv + push.
