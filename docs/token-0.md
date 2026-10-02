# TOKEN-0 — token haritası + ölçüm tabanı · 2 Eki 2026

Birim: ağırlıklı token = girdi×1 + cache okuma×0.1 + cache yazma (5m×1.25, 1h×2) + çıktı×5. Model fiyatından bağımsızdır.
Kaynak: `tools/token_olc.py` → `olcum/token-0.json` · `olcum/token-0-k2.json`. Hiçbir ayar değişmedi.
Headroom vekili açıktı; bütün sayılar Headroom sıkıştırmasından sonradır.

## 1. 14 günlük ağırlıklı token (18 Eyl–2 Eki · 1990 dosya · 13 498 istek)
Toplam **475.9 M** (14 güne bölünce 34.0 M/gün). Bozuk satır 0, usage'sız satır 0, kırılımsız cache 0.

| kaynak · ajan | girdi | okuma | yazma 5m | yazma 1h | çıktı | toplam M | pay |
|---|---|---|---|---|---|---|---|
| etkileşimli · ana | 3.7 | 143.2 | 0 | 113.9 | 54.8 | 315.5 | %66.3 |
| etkileşimli · subagent | 1.8 | 24.7 | 27.9 | 0 | 7.0 | 61.4 | %12.9 |
| claude -p (ana + subagent) | 0.8 | 11.0 | 0.1 | 36.3 | 4.7 | 52.8 | %11.1 |
| claude-mem observer | 0.0 | 0.3 | 0 | 40.5 | 5.5 | 46.2 | %9.7 |
| **toplam** | 6.3 | 179.2 | 28.0 | 190.7 | 72.0 | 475.9 | |

- Model payı: opus-5-5 %51.9 · opus-5 %20.6 · sonnet-5 %13.4 · haiku-4-5 (observer) %10.4 · sonnet-5-5 %3.7.
- Proje payı: omer-skills %59.6 · Kendi oyun modlarim %10.8 · observer %9.7 · TELVE %4.6 · cc-kopru %4.4 · video %3.9. Divisima'da 14 günde oturum yok.
- Etkileşimli ana (n=185): taban medyanı 89.0k · tur medyanı 38 (p90 88) · son ctx medyanı 183k (p90 282k); 69 oturum 200k'yı aşıyor.
- claude -p (n=237): taban medyanı 89.4k, tur medyanı 2; 234 ana oturumun 211'i ≤3 tur. Subagent taban medyanı 42.5k.
- Araç sonucu (ham token, 14 gün): Bash 3.34 M · Read 1.96 M · headroom_retrieve 0.37 M (207 çağrı) · Grep 0.24 M. En büyük 20 sonucun 18'i Read (10–17k).
- Görsel: 599 adet, ≈0.81 M token (PNG başlığından hesaplandı, PNG dışı görsel 1600'de tavanlandı).
- Ek (attachment) boyutları, adet · karakter/adet:
  - skill_listing 565 · 125k
  - agent_listing_delta 479 · 30k
  - deferred_tools_delta 778 · 18.6k
  - mcp_instructions_delta 788 · 7.6k
  - hook_additional_context 1464 · 3.8k
- **Birim uyarısı:** Opus 5.5'te cache okuma gerçekte 0.05× fiyatlanır (pricing, dipnot 2). Birim 0.1× sayar, bu yüzden Opus 5.5 okuması (992.7 M token) 99.3 M ağırlıklı görünür; gerçek fiyat karşılığı 49.6 M'dir. Birim KARAR gereği değişmedi.

## 2. Tur başı taban bileşenleri (K2 · 7 çağrı · `claude -p "ok" --output-format stream-json --verbose`)

| v | bayrak | init kanıtı | ilk istek ctx | bileşen |
|---|---|---|---|---|
| a | varsayılan, omer-skills | tools 371 · mcp 31 (22 bağlı) · skills 393 · slash 489 · agents 58 · hook olayı 9 | 97 034 | — |
| b | `--strict-mcp-config` + boş mcp-config | mcp_servers 0 · tools 29 | 87 861 | MCP = a−b **9.2k** |
| c | `--disable-slash-commands` | skills 0 · slash 7 (yerleşik) | 50 879 | skill/komut listesi = a−c **46.2k** |
| d | `--settings {"disableAllHooks":true}` | hook_started 0 (a'da 9); MCP bağlı 14 (a'da 22) | 92 125 | hook ≤ a−d **4.9k** (MCP bağlantı gürültüsü dahil) |
| e | a + `--model claude-sonnet-5-5` | model claude-sonnet-5-5 | 97 092 | model etkisi +58 ≈ 0 |
| f | a, cwd Desktop\TELVE | agents 54 (proje ajanı 4 az) | 95 508 | proje (CLAUDE.md + proje ajanları + hafıza) = a−f **1.5k** |
| g | b + c + d | tools 28 · mcp 0 · skills 0 · slash 0 · hook 0 | 37 626 | sistem kalanı **37.6k** |

- **Varyantların geçerliliği:** yedi varyantın hepsi init satırıyla kanıtlandı; etkisiz varyant yok.
  - c'de 7 slash komutu kaldı, ama skill sayısı 0 olduğu için kanıtlı sayıldı.
  - d'de 8 MCP sunucusu daha az bağlandı (61 araç adı eksik). Bu yüzden hook payı 4.9k'nın altındadır.
- Bileşenlerin toplamı 99.4k ediyor, a ise 97.0k. Aradaki 2.4k etkileşim ve MCP bağlantı gürültüsünden geliyor: bağlı MCP sayısı 14 ile 24 arasında oynuyor.
- Sistem kalanının içeriği (tahmin): 58 ajan listesi ≈7.5k, global CLAUDE.md + RTK + MEMORY ≈2.5k, 28 yerleşik araç ve sistem istemi.
- Davranış etkisi: a'da "ok" istemi 3 isteğe ve 3 araç çağrısına yol açtı ($0.88). Skill listesi kalkınca (c) tek istek kaldı ($0.41). SessionStart ve skill zorunluluğu boş işe tur ekliyor.
- Maliyet: 7 çağrı toplam $4.10. Boş RAM 6.7–8.0 GB olduğu için beklemeye gerek olmadı.
- **İlk üç bileşen:** skill/komut listesi 46.2k (%48) · sistem kalanı 37.6k (%39) · MCP 9.2k (%9).

## 3. Kaldıraç tablosu
Tasarruf tahminidir, M ağırlıklı/gün, 14 günlük veriye göre. Tahminler örtüşür, toplanmaz. Hiçbiri silme gerektirmez.

| # | kaldıraç (silmesiz yol) | ~M/gün | kalite etkisi ve gerekçe | kalite kapısı | risk |
|---|---|---|---|---|---|
| L1 | Arka plan profili: claude -p'ye işe göre `--strict-mcp-config` + gereken MCP · `--disable-slash-commands` · `--settings` ile SessionStart yok · Sonnet 5.5 · JSON. Taban 89k→≈38–50k | 1.7 | 0/+ : boş tur kalkar (K2 a→c: 3 istek→1) | işin kendi metriği (kör puan ≥3.6, altın recall gürültü içinde) + tur | işin gerektirdiği skill görünmez → SKILL.md yolu istemde |
| L2 | SessionStart enjeksiyonları (claude-mem bağlamı, superpowers ≈0.9k, ponytail ≈1.6k, node uyarısı): matcher daralt, CONTEXT_OBSERVATIONS azalt | 0.5 | −/0 : süreklilik bilgisi azalır | görev başarısı + "geçmiş işi bulma" soruları | hafıza kopukluğu |
| L3 | claude-mem observer: 46.2 M'nin 40.5'i 1h yazma, okuma ≈0. Observer'a 5m TTL ya da settingSources'suz çalıştırma | 1.1–1.45 | 0 : TTL çıktıyı değiştirmez | gözlem/gün ±%10 + 10 örnek gözlem kör karşılaştırma | TTL'in hangi ayardan geldiği doğrulanmalı |
| L4 | Hook enjeksiyonları: hook_additional_context 1464 kez × 3.8k (claude-mem Read file-context, Jev öneri ≈20–40 tok + istem başı ≤2 HTTP). Kaynağa göre kırılım çıkar, yalnız işe yarayan kalsın | 0.3 | 0/− : yanlış bağlam enjeksiyonu da azalır | Jev öneri isabeti + görev başarısı | Jev tetik kaybı |
| L5 | Proje profilleri: proje türüne göre proje `.claude/settings.json` skillOverrides "off" (kurulum kalır). Listede olmayan aileye departman router'ındaki SKILL.md yoluyla erişilir. Liste 46.2k, yarıya inerse | 1.8 | 0/− : tetik kaybı riski, router telafi eder | L15 tetik seti (recall/precision) ≥ taban | yanlış profil |
| L6 | Görsel bütçesi + sayısal kapı (Blender tekniklerinin genellenmesi: thumbnail ≤512 px, iş başına ≤N görsel, önce sayısal ölçü sonra görüntü) | 0.2 | 0 : sayısal kapı görsel kontrolün yerini tutar | kör puan + uygunluk (Blender) | görsel hatanın kaçması |
| L7 | Tur sayısı: paralel araç çağrısı · betik+parametre · tarifte tavan/gerçek tur oranı. Okumanın %20'si | 2.0 | 0/+ : daha az ara durum | görev başarısı + tur oranı | betik hatası |
| L8 | En büyük araç sonuçları: Read 10–17k bloklar (dar aralık kuralı) · Bash çıktısı (rtk/jev log) · Read'den sonra gelen headroom_retrieve turları (207 kez) | 0.6 | 0 : aynı bilgi daha dar | görev başarısı | eksik okuma |
| L9 | İş türü → model/effort: rutin işte xhigh→high (cikti-notlari: xhigh 1.9× çıktı, kazanç yok) · arka planda Sonnet 5.5 ($ yarıya iner; birim modelden bağımsız olduğu için tabloda görünmez) | 0.8 | 0/− : zor işte effort düşerse kalite düşer | altın set + kör puan, iş türü başına | yanlış sınıflandırma |
| L10 | Cache: kısa claude -p'de 1h TTL boşa (36.3 M 1h yazma, %90'ı ≤3 tur) → `--settings` ile 5m. Cache kıran olaylar: >60 dk ara, compact, MCP geç bağlanınca gelen deferred_tools_delta (778 kez × ~5k) | 1.0 | 0 : TTL çıktıyı değiştirmez | tur başı cache_read/yazma oranı | 5–60 dk aralı uzun işte yeniden yazma |
| L11 | FORCE-AB: `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` açık/kapalı A/B · mekanik alt ajana haiku (video-tarayici-haiku kolu var) | ≈0 ağırlıklı / $ düşer | −/0 : küçük modelde kalite riski | altın set recall (video-tarayici) | haiku eksik okuma |
| L12 | Headroom output shaper (`headroom/proxy/handlers/anthropic.py:3128-3175`): tur türüne göre sistem istemi kuyruğuna verbosity talimatı ekler. Ölçülen etki −%38.5 çıktı, kalite 2.50→2.62 (headroom-ayar-sonuc). Ayrıştırma için yerleşik holdout var: `HEADROOM_OUTPUT_HOLDOUT` konuşmayı bütün olarak treatment/control kolu yapar, stratum etiketini kayda yazar | koruma | ? : ayrıştırılmadı | kol başına görev başarısı + çıktı token | holdout kolu çıktı tasarrufunu kaybeder |
| L13 | CLAUDE.md'ler: Divisima 30.4k karakter ≈8.7k tok. İlk 5 bölüm (%42) `sdp`/`surec` skill'lerine taşınır, CLAUDE.md'de dizin kalır | 0 (14 günde Divisima yok); oturum başına ≈50k | 0/− : kural yüklenmezse risk | Divisima denetim kapısı (sdp) | kural kaçağı |
| L14 | Uzun context: >200k'da fiyat farkı yok. Gerekçe fiyat değil, okuma hacmi: 69 oturum 200k'yı aşıyor, mantıksal aralarda /compact ya da /clear | 1.0 | − : compact ayrıntı kaybettirir | görev başarısı + tur | bağlam kaybı |
| L15 | Skill tetiklenme doğruluğu: liste bütçenin %84'ünde, açıklamalar kırpılabilir. Yanlış/eksik tetiklenen skill'in açıklaması netleştirilir, içerik silinmez | ölçüm | + : doğru skill | tetik seti recall/precision | — |
| L16 | Ajan listesi: 58 tür ≈7.5k/oturum (sistem kalanının içinde). Kullanılmayan plugin ajanları gizlenir (permissions deny `Agent(x)`, mekanizma doğrulanacak) | 0.9 | 0 : listede olmayan ajan çağrılmıyor | ajan çağrı başarısı | mekanizma yoksa 0 |
| L17 | Observer/claude -p maliyeti modelden bağımsız birimde görünmüyor: $ sütunu eklenir (haiku 1×, sonnet 2×, opus-5-5 4×) | ölçüm | 0 | — | — |

- Headroom çapraz kontrolü tutmuyor: savings_events (claude-code) 1 497.7 M → 1 297.4 M, 200.3 M tasarruf (%13.4; cc-kopru %51.9); proxy_savings.json aynı dönemde 46.2 M (4.6× fark, tanımlar farklı). Kapı metriği olarak events.saved kullanılmaz.

## 4. Önerilen sıra ve kapılar
1. **TOKEN-1 — L1 + L10 arka plan profili** (≈2.7 M/gün)
   - Kapı: bir B-fincan-rehber koşusu ve bir altın set koşusu profilli; kör puan ≥3.6 ve uygunluk ≥3; recall M3b gürültüsü içinde (±1.3/±5.0/±1.5); taban ≤50k; tur değişimi raporlanır.
2. **TOKEN-2 — L3 observer TTL** (≈1.1–1.45 M/gün)
   - Kapı: gözlem/gün ±%10; örnek gözlem kör puanı eşit.
3. **TOKEN-3 — L15 tetik seti, ardından L5 proje profilleri** (≈1.8 M/gün)
   - Kapı: tetik recall ve precision tabanın altına düşmez; görev başarısı eşit.
4. **TOKEN-4 — L7 + L8 tur ve araç sonucu disiplini** (≈2.6 M/gün)
   - Kapı: görev başarısı eşit ya da üstünde; tur ve ağırlıklı token birlikte raporlanır (tur artıp token düşerse tasarruf sahte sayılır).
5. **TOKEN-5 — L9 effort/model iş türü tablosu** (≈0.8 M/gün)
   - Kapı: altın set + kör puan, iş türü başına.
6. **TOKEN-6 — L2 + L4 + L16 enjeksiyon ve listeler** (≈1.7 M/gün)
   - Kapı: geçmiş-iş soruları + Jev isabeti.
7. **Sonra:** L6 görsel kapısı · L14 compact politikası · L11 FORCE-AB · L12 Headroom ayrıştırma · L13 Divisima (Divisima dalgası açılınca).
- Her dalgada A kolu Opus 5.5 ile yeniden ölçülür. Aşağıdaki eski tabanlar yalnız yön gösterir.
- Her kapıda iki yön raporlanır: düşüş (recall, kör puan, başarı) ve artış (tur, maliyet, ağırlıklı token).

## Ek A — Statik envanter (K3)
- CLAUDE.md, karakter ≈ token (karakter/3.5):
  - global 3040 ≈ 869, `@RTK.md` 452 ≈ 129
  - omer-skills 1149 ≈ 328
  - TELVE 1189 ≈ 340
  - Kendi oyun modlarim 2583 ≈ 738
  - Divisima 30 436 ≈ 8 696
  - @import yalnız global'de.
- Hook'lar (settings.json):
  - Bağlama yazan:
    - SessionStart compact → dalga-durum.ps1 (dalga.md ≤3800 karakter)
    - SessionStart startup → node_yolu_uyari.py (yalnız uyarı varsa)
    - UserPromptSubmit → jev-skill.ps1 (≤3 ad önerisi)
  - Yazmayan: dotnet-format, blender_bekci (stderr), block-destructive, rtk ×2 (yeniden yazım), izin-echo, headroom-claude-guard.
  - Plugin hook'ları:
    - claude-mem: SessionStart bağlamı, PreToolUse Read file-context, PostToolUse * → observer, Stop özeti
    - superpowers: SessionStart
    - ponytail: SessionStart + SubagentStart
    - everything-claude-code: SessionStart/PreCompact
- Jev hook:
  - Olay UserPromptSubmit; istem başına en çok 2 HTTP isteği (jev-mcp / typesafe / openrouter).
  - 2.5 sn bütçe; günlük tavan dosya sayaçlı.
  - Çıktı "Jev skill önerisi: a, b, c" (≈20–40 tok).
  - `JEV_SKILL_HOOK` tanımlı (değer yazılmaz).
- Skill/plugin/MCP:
  - Plugin: enabledPlugins 47 açık / 6 kapalı.
  - Skill: skillOverrides 328 "off"; SKILL.md sayısı skills/ 1054, plugins/ 1014.
  - Skill listesi `SLASH_COMMAND_TOOL_CHAR_BUDGET` doluluğunun %84'ü (ortalama skill_listing / bütçe).
  - MCP: üst düzeyde 19 sunucu, projeye 1; plugin MCP'leri ayrıca.
  - `ENABLE_TOOL_SEARCH` var: MCP araçları ertelemeli, init'te 31 sunucu ve 371 araç adı.
- claude-mem:
  - Ayarlar: provider claude, model haiku-4-5, CONTEXT_OBSERVATIONS 15, SESSION_COUNT 10.
  - Observer ağırlıklı ortalaması günde 3.56 M (13 gün).
  - Tetik PostToolUse * yani her araç çağrısı.
- Uzun context fiyatı: platform.claude.com/docs/en/about-claude/pricing, "Long context pricing" bölümü:
  > "Claude 4.6 and later models … include the full 1M token context window at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.)"
  - Opus 5.5: $4 / $20, 5m yazma $5, 1h yazma $8, okuma $0.20 (0.05×).
  - Sonnet 5.5: $2 / $10, okuma $0.20 (0.1×).

## Ek B — Kalite tabanları (K4, koşu yok)
- **Altın set M3b** (`docs/olcumler/m4-altin-olcum.md:8`, `m5-son-olcum.md:27`, 30 Eyl, Sonnet motoru) — **eski**.
  - M3b: yüksek %90 · genel %81 · dayanmayan %4 · $0.86.
  - M5 ortalaması: %87.3 · %74.7 · %7.4 · $1.08; ölçüt ≥90 / ≥75 / ≤5.
  - Gürültü ±1.3 / ±5.0 / ±1.5.
- **B-fincan-rehber** (`docs/denemeler/blender-uretim-olcum.md:42`, 2 Eki, opus-5-5) — güncel.
  - Kör puan 3.6 · uygunluk 3 · 115 tur · $9.60 · 28 dk.
  - A-v3: 3.6 · uygunluk 2 · 60 tur · $4.98.
- **rtk-ab** (`Desktop\rtk-ab`, tag base, `out/B1.json`, `out/B2.json`, 17 Eyl, opus-5) — **eski**.
  - B1: $0.246 · 5 tur · hata yok.
  - B2: $0.222 · 5 tur · hata yok.
  - `docs/rtk-ab.md`: sıcak-sıcak karşılaştırmada token −%8.0, maliyet +%17.4.
- İki yönlü metrikler:
  - Düşüş: recall (yüksek/genel), kör puan, uygunluk, görev başarısı (is_error / teslim).
  - Artış: tur, ağırlıklı token, $, dayanmayan %.
