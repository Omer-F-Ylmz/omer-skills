# Erişim haritası (ERİŞİM-TAM-1, 22 Eki) — oturum 3: araç kapısı eklendi

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

## 5. Oturum 3 — araç kapısı (`tools/mcp_kapi.py`)
Tek stdio MCP "kapi", iki araç: `ara(sorgu|sunucu)` (katalogdan şema döner) ve `cagir(sunucu, arac, args)`. Katalog: `python tools/mcp_kapi.py katalog` → `.kos/kopru/kapi-katalog.json` (git dışı; yenilemek için komutu koş). `mcp_profil.yaz` her köprü profiline kapıyı ekler (`CC_MCP_KAPI=0` kapatır); OAuth'lu figma/canva/claude-design yalnız görev metninde anılınca doğrudan eklenir. Doğrudan MCP ≤20 araçsa `ajan_sira.baslat_argv` ToolSearch'ü kapatır (`mcp_profil.agir`), çünkü ToolSearch tek başına sabit ~6.5k jeton yükü getiriyor.
- Katalog: 45 sunucudan 41'i tools/list ✓ (801 araç). ✗: figma/canva/claude-design (OAuth 401, doğrudan kalır), auth0 (initialize zaman aşımı).
- Uçtan uca (köprü ajanı, haiku, 14 tur, $0.007): 3 skill yükleme ✓ (yetenek-getir, find-skills, graphify) · 3 CLI ✓ (rtk, graphify, markitdown) · ruflo doğrudan ✓ · kapı→mcp-time ✓ · kapı→mcp-git ✓ · kapı ara→playwright ✓ = 10/10.
- Sayılar: skillOverrides 2416 name-only / 329 off / 11 on · 667 kullanıcı skill'i · 195/204 plugin açık · 580 ajan tanımı · 7/7 CLI PATH'te (rtk graphify beyin markitdown summarize jev headroom). `katalog_ara.py` (skill listesi sığmama yolu) koşuyor.

| ölçüm (haiku, `OK yaz`/çok istemli) | giriş jetonu |
|---|---|
| boş MCP | 15.8k (çok istemli: 15.8k→16.0k) |
| 45 MCP ertelemesiz | 25k → 651k |
| 45 MCP ToolSearch (§1) | 46–48k |
| kapı-tek, ruflo yok, `ara`+`cagir` çağrılı | 15.8k → 26.7k → 27.1k |
| kapı + ruflo doğrudan (5 araç) | 15.8k → 36.9k → 38.1k |

Hedef "boş-MCP'ye göre ≤+%1" **karşılanmadı**: MCP bağlandıktan sonraki istemde kapı-tek ≈ +11k (`ara` sonucu <2k; kalanı kaynağı bulunamadı, CC'nin MCP bağlıyken eklediği sabit yük şüphesi — kanıtsız). İlk istem MCP henüz bağlanmadan ölçülür (arka plan bağlanma) → "+%0" gibi görünür, yanıltıcıdır. Ruflo'yu doğrudan tutmak +10k getiriyor; kapıdan çağırmak daha ucuz (denenmedi).

## 6. Hâlâ yapılmayan / karar bekleyen
- Desktop ve CC etkileşimli yüzeyi için uçtan uca tablo koşulmadı (✗ kanıtsız). Alt ajan (Task) mirası §2'deki gibi; kapıyı dar ajanlara vermek için kapının kullanıcı MCP'sine (`~/.claude.json`) eklenmesi gerekir — yapılmadı.
- engel-tarama #11 (`ENABLE_TOOL_SEARCH=false`, kullanıcı ayarı) değiştirilmedi: karar sende (köprüde artık profil değeri geçerli, etkileşimli CC'de ertelemesiz yükleme sürüyor olabilir).
- auth0 sunucusu kapıdan zaman aşımına düşüyor (ayrı inceleme).
