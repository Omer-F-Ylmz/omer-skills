# Erişim haritası (ERİŞİM-TAM-1, 22 Eki) — KISMİ

Ölçüm: `tools/erisim_olc.py` → `docs/token/erisim-tam-1.tsv` (köprü ajanı yolu, haiku, 45 MCP / 858 araç açık, "OK yaz" ve ruflo memory_search çağrısı).

## 1. Ertelemeli yükleme — kök neden ve düzeltme
- CC 2.1.302, `ANTHROPIC_BASE_URL` (headroom vekili) var: araç araması yalnız `ENABLE_TOOL_SEARCH=true|auto` ile açılır (v2.1.304 öncesi, belge: "Tool search through an LLM gateway").
- Köprü profili `--tools` listesinde `ToolSearch` yoktu → MCP araçları ertelenmiyor, tüm şemalar yükleniyordu. Kullanıcı ayarında ve kabuk ortamında `ENABLE_TOOL_SEARCH=false`.
- İlk istem tek başına yanıltıcı: `false`/ertelemesiz kolda ilk istem 25k, ikinci istem 651k (MCP sunucuları arka planda bağlanır).
- Düzeltme: `profiller/cc-arka.json` "ajan": `ToolSearch` araçlara + `env.ENABLE_TOOL_SEARCH=true`. `--settings` env'i kabuk ortamını (`false`) eziyor (profil kolu ile doğrulandı).

| kol (45 MCP, 858 araç) | istek başı giriş jetonu |
|---|---|
| boş MCP (taban) | 14.941 |
| ertelemesiz (eski yol) | 25.187 → **651.421** (2. istem) |
| ertelemeli (yeni profil) | **46.134 / 47.752 / 48.160** (3 istek, ruflo çağrısı başarılı, hata 0) |

Sonuç: istek başına ~651k → ~47k (−%93). Hedef "≤ +%1" **karşılanmadı**: 858 araç adı + sunucu yönergeleri ~31k (+%210) taban üstü. Ad listesini küçültmenin yolları: KEEP süzgecini daha çok MCP'ye yaymak ya da tek "araç kapısı" proxy MCP'si — yapılmadı.

## 2. Alt ajan (Task) MCP mirası
- `~/.claude/agents/*.md` 580 tanım: 493'ü dar yerleşik `tools:` (Read, Grep, Glob…) listeli → MCP görmez; 87'sinde `tools:` yok → tümünü miras alır. Düzenlenmedi (güvenlik/model maliyeti kararı gerekir).

## 3. Yapılmayan / kanıtsız (✗)
- Yüzey × kategori tablosu (CC etkileşimli · Desktop · alt ajan), her MCP'den 1 çağrı, 3 skill yükleme, 3 CLI: koşulmadı. Kapsama % verilemez.
- Madde 4 (skill listesi sığmama) ve 5 (engel-tarama "kalsın" yeniden değerlendirme): yapılmadı. engel-tarama #11 (`ENABLE_TOOL_SEARCH=false`) artık yanlış: kullanıcı ayarı `false` etkileşimli CC'de de MCP'yi ertelemesiz yükletiyor olabilir — ayrıca ölçülmeli.
- Kullanıcı ayarı (`~/.claude/settings.json`) değiştirilmedi.

## 4. Devir (oturum 2, çağrı 10/45'te kanca "ara kayıt + DUR" dedi)
Yeni ölçüm/kod yok; yalnız keşif:
- Tanımlı 45 MCP: 28 `http`, 17 `stdio`. "Araç kapısı" proxy'si stdio'lar için yazılabilir; http sunucularda kimlik (OAuth/başlık jetonu) CC'de tutulur, proxy'ye taşınabilirliği KANITLANMADI. Kapıdan önce hangi http sunucusunun statik başlıkla çalıştığı sınanmalı.
- Alternatif (daha ucuz): KEEP/`mcp_profil.sec` türe göre MCP sayısını azaltır (site-3d 237k→32k); "TÜM MCP açık ≤+%1" yalnız kapıyla olur.
- Sıradaki: (a) 31k ek yükün dökümü (ad listesi vs sunucu yönergeleri; kol başına tek MCP ile `erisim_olc.py`), (b) yüzey×kategori tablosu + sunucu başına 1 çağrı, (c) madde 4–5, (d) `~/.claude/settings.json` ENABLE_TOOL_SEARCH=false kararı.
