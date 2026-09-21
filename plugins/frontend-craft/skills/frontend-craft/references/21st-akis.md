# 21st MCP akışı

> Kaynak: CC'deki canlı `21st` MCP araç listesi (`https://21st.dev/api/mcp`) · ölçüm 21 Eyl 2026.
> Uydurma ad yok: aşağıdaki her ad ya listede ya da listedeki bir aracın şemasında geçiyor.
> Sunucu tanımı: `docs/claude-ai-mcp.md` · claude.ai tarafında Connectors'ta aynı sunucu.

Bu dosya yalnız hangi adımda hangi aracın çağrılacağını söyler. Tasarım kararları
`frontend-craft` SKILL.md'de; bileşen kurulum/uyarlama pratiği `21st-ui` skill'inde.

| Adım | Araç | Not |
|---|---|---|
| referans çıkarma | `get_inspiration` → `record_inspiration_feedback` | metadata döner, ücretli kod dönmez; feedback yalnız `feedbackId` + sonuç kimliğiyle |
| bileşen arama | `search` · `search_picker` | `search_picker` seçimi kullanıcıya gösterir; kendin tarıyorsan `search` |
| bileşen kodu | `get_component` | tam kod + demo + install komutu; ÜCRETLİ, günlük kotadan düşer → **yalnız seçilen tek bileşen için** |
| tema | `get_theme` | `:root`/`.dark` token CSS'i; ücretsiz |
| logo | `search_logo` | svgl.app SVG url'leri; ücretsiz, limitsiz |
| taslak | `iterate_generation` → `get_generation_job` · `get_generation` · `get_take` | okuma uçları (`get_*`) AI kapalıyken de ücretsiz |
| kayıt | `bookmark` · `add_to_list` | `add_to_list` için liste id'si `list_bookmark_lists`'ten |
| kota | `get_usage` | `aiGenerationEnabled` + kalan bileşen çekme hakkı |

## Kapılar

- **Üretim uçları koşullu:** `generate` ve `iterate_generation` yalnız
  `get_usage.aiGenerationEnabled` doğruyken araç listesine girer. Bu kurulumun canlı
  listesinde ikisi de yok → taslak akışı okuma uçlarıyla sınırlı. Kaynak: `get_usage`
  aracının kendi açıklaması ("do not call generate or iterate_generation").
- **Kota:** `get_component` ücretli. Arama sonucundan bileşen seçilmeden çağrılmaz;
  aday karşılaştırması `search`/`get_inspiration` metadata'sıyla yapılır.
- **Sıra:** önce `get_usage`, sonra akış. Kota bilinmeden ücretli uç çağrılmaz.
- 21st çıktısı frontend-craft Bölüm 4'ün audit + görsel optimizasyon kapısından
  geçmeden teslim edilmez.
