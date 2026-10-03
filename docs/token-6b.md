# TOKEN-6b — ara ölçüm · etkileşimli TTL simülasyonu · HR uyarısı

## K1 Ara ölçüm (`olcum/token-6b.json`)
`python tools/token_olc.py olc --karsilastir olcum/token-0.json --bas varsayilan=2026-10-02T15:00:14Z --bas claude-p=2026-10-02T15:20:07Z --bas observer=2026-10-02T16:36:04Z --bas "etk·ana omer-skills=2026-10-02T22:41:44Z" --bas "etk·ana diğer=2026-10-02T23:53:49Z"`

| grup | dönem başı UTC | istek | taban payı | birincil ağ. taban → şimdi | birincil $ | çıktı/istek | ilk istem |
|---|---|---|---|---|---|---|---|
| etk·ana omer-skills (ağ./istek) | 10-02 22:41 | 74 | %51.8 | 34 012 → 86 440 (+%154) | 0.132 → 0.323 | 1154 → 5224 | 89 073 → 100 654 (+%13) |
| etk·ana diğer | 10-02 23:53 | 0 | %14.5 | yetersiz örnek | — | — | — |
| etk·subagent (ağ./istek) | 10-02 15:00 | 439 | %12.9 | 18 757 → 19 212 (+%2) | 0.038 → 0.038 | 427 → 744 | — |
| claude-p (ağ./çağrı) | 10-02 15:20 | 316 | %11.1 | 225 497 → 315 570 (+%40) | 0.61 → 1.09 | 938 → 1354 | 79 660 → 85 424 |
| observer (ağ./gün) | 10-02 16:36 | 32 | %9.7 | 3.30 M → 1.50 M (**−%55**) | 3.30 → 1.50 | 1620 → 2304 | 34 137 → 25 064 |

- Ölçüm koşuları ayrı, karşılaştırma dışı: 22 oturum · 99 istek · 4.15 M ağ.
- **Toplam tahmini tasarruf = Σ kaynak payı × normalize düşüş: ağırlıklı −%79.2 · $ −%98.5** (eksi = artış). claude-p hariç −%74.8 · −%89.8.
- %30 hedefi: **ölçülemedi, bu pencere temsilî değil.**
  - etk·ana omer-skills'in 74 isteğinin tamamı TOKEN-6a/6b dalga oturumu. Çıktı/istek ×4.5 (kod + doküman yazımı).
  - Effort 2026-10-03T10:56Z'de yeniden xhigh'a döndü (d9d2c0d0:14).
  - Gerçek kazanç sinyali tek: observer gün başı −%55, istek başı −%43 (TOKEN-2b yaması).
- Çekince: dönem kısa (observer ~19 sa, omer-skills ~14 sa). İş karışımının çoğu TOKEN dalgaları, taban ise genel iş.
- Dönem başı kanıtları:
  - claude-p: 170eb0a, cc-kopru ttl.
  - observer: worker-service.cjs mtime 19:36:04+03 (yama). Commit 07dda53 bundan 2.5 dk önce.
  - omer-skills: 265315f skill-arac. Diskte 18:42Z'de, commit'ten 4 sa önce.
  - effort high: settings yedeklerinden, en geç 23:53:49Z. git'te kanıt yok.
  - Varsayılan: f3bce7f.
- Ölçüm koşusu ayrımı (`OLCUM`, testli):
  - Kural: ilk istem `ok`, `Yalnız ok yaz`, `Salt-okuma ölçüm görevi` ya da `mekanizma probu` ise oturum ölçüm koşusudur. Alt ajan üst oturumdan miras alır (`<sid>/subagents/`, okuyucu 851/851 doğruladı).
  - **Sınır:** okuyucuya göre dönemdeki 72 sdk-cli oturumunun tamamı ölçüm/prob. tetik-seti istemleri ve 3a okuyucusu kalıba girmiyor, bu yüzden claude-p satırı ölçüm ağırlıklı ve karşılaştırılamaz.

## K2 Etkileşimli önbellek simülasyonu (`olcum/token-6b-ttl.json`, 14 gün)
`python tools/token_olc.py olc --ttl-sim`: 197 etk·ana oturumu · 8700 istek · 60.72 M önbellek yazması.
- Yazma: **yeni içerik %60.6 · kırılma sonrası baştan %39.4** (23.9 M).
- Kırılma sebebi (baştan yazma payı):
  - compact 0
  - ara>TTL 7 kez · 1.49 M · %6.3
  - model/effort 0
  - deferred_tools_delta 2 · 0.25 M · %1.0
  - **diğer 148 · 22.17 M · %92.7**
- Kollar (ağırlıklı M · $):
  - 1h (bugün) 329.39 · 1210
  - 5m 313.11 · 1148 (−%4.9 · −%5.1)
  - hibrit 303.94 · 1105 (−%7.7 · −%8.7). Hibrit, oturum başına ucuz kolu seçer; kehanet üst sınırıdır.
- İstek arası: p50 13.5 sn · p90 76 sn · p99 684 sn · >5 dk %2.6.
- TTL seçme yolu, CC 2.1.288 ikilisi (`~/.local/bin/claude.exe`):
  - Kod: `if(a.FORCE_PROMPT_CACHING_5M)return{ttl:"5m",reason:"force_5m_env"};let s=uUo(e),g=s?a.CLAUDE_CODE_PROMPT_CACHE_TTL:a.CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL;if(g!==void 0)return{ttl:g,reason:"env"};let h=st(),S=s?h.promptCacheTtl:h.subagentPromptCacheTtl;…`
  - Ana iş parçacığı: querySource `repl_main_thread*|sdk|auto_mode|memdir_relevance`.
  - Varsayılan: abonelikte 1h, API anahtarında 5m. Env, settings'in önüne geçer.
- **Önerilen TTL politikası:**
  - Mekanizma: oturum başına `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` ile başlatma. Kısa, yoğun oturumlar 5m, uzun düşünme molalı oturumlar 1h. Global settings değişikliği yok.
  - Tahmini tasarruf: etk·ana'nın %4.9–7.7'si, yaklaşık 1.2–1.8 M ağ./gün (toplamın %3.5–5'i).
  - Risk: >5 dk aralarda baştan yazma. Aralıkların %2.6'sı, kol hesabına dahil.
  - Kapı: kol başına n≥2 A/B, yeni dönemde `--ttl-sim` ile.
  - **Önce** "diğer" kırılması teşhis edilmeli. 22 M, TTL kazancından büyük. Aday nedenler kanıtsız: Headroom'un önek yeniden yazımı, oturum içi sistem istemi değişimi.

## K3 HR uyarısı (`~/.claude/statusline.ps1`)
- Segment en başta. Üç durum:
  - `HR`: settings.json'da `env.ANTHROPIC_BASE_URL` var ve 127.0.0.1:6767 açık.
  - `!!HR KAPALI:env`: anahtar yok. Headroom Desktop çıkışta, pause'da, auto-pause'da ve çökme bekçisinde siler (token-6a §K1).
  - `!!HR KAPALI:port`: anahtar var ama proxy yanıt vermiyor.
- Port denemesi 200 ms. Sonuç `%TEMP%\hr-port-<port>.txt` içinde 30 sn önbelleklenir. settings yalnız boolean okunur, değer basılmaz.
- Segment başta durur ki 80 karakter kesmesi uyarıyı yutmasın. model · ctx · cache · miss aynı sırada kalır.
- Görünce:
  - `:env` → Headroom Desktop'ı aç ya da devam ettir (env'i geri yazar), sonra yeni oturum.
  - `:port` → proxy'yi başlat.
- Test `tests/test_statusline_hr.py`: USERPROFILE/TEMP tmp, `HR_PORT` dikişi, Python soket dinleyici. Yedek `~/.claude/statusline.ps1.bakT6b`.

## Sonraki öncelik
1. **6c çıktı kısaltma A/B önce.** Çıktı ×5 ağırlıklı. Çıktı/istek her grupta arttı: omer-skills +%353, subagent +%74, observer +%42.
2. **"diğer" önbellek kırılması teşhisi (yeni).** 22 M / 14 gün, TTL kolundan büyük.
3. **6d claude-mem bağlam daraltma** (kapatma değil; superpowers + ponytail metni; n≥2).
   - Observer zaten −%55/gün.
   - İlk istem omer-skills'te +%13.
   - 6a'da kapatma Explore'u +%180 tetikledi. Daraltma kolu bu riski ölçmeli.
4. TTL politikası: 2'den sonra, kapılı.
