# TOKEN-ACILIS-1 (28 Eki)

Ölçüm: `claude -p`, haiku, tek kelimelik görev, ilk tur girdi = input + cache_read + cache_write. Betik: `.kos/kopru/arka/token-acilis/olc.py`.

| Varyant | Açılış token |
|---|---|
| taban (415 eklenti + 33 MCP + 2397 skill) | 350–440k (arka işlerde ölçülmüş); `claude -p` bu haliyle >900 sn'de dönmedi |
| `--setting-sources project` | 33,7k (user ayarı/hook/skill/CLAUDE.md düşer) |
| eklentiler kapalı (`--settings` enabledPlugins hepsi false) | 77k |
| + `--strict-mcp-config` boş | 68k |
| + `--disable-slash-commands` | 38k |

Katkı: eklentiler ≈ 300k+ (skill listesi, ajanlar, hook'lar, 415 eklentinin MCP'leri), kullanıcı MCP'leri ≈ 9k, skill listesi ≈ 30k, geri kalan çekirdek ≈ 28k.
Önemli yan bulgu: eklentiler açıkken her başlangıç dakikalarca sürüyor (yüzlerce hook/MCP 30 sn zaman aşımı); `strix` işi ve A/B taban kolu bu yüzden hiç dönmedi.

## arka_ajan.py seçenekleri (iş json'u, varsayılan değişmez)
- `"eklenti": [liste]`, yalnız listedekiler açık, diğer eklentiler o oturumda kapalı (`--settings` geçici dosya; kullanıcı ayarı değişmez).
- `"mcp": [liste]`, `~/.claude.json` sunucularından yalnız listedekiler (`--strict-mcp-config`).
- `"hafif": true`, `--disable-slash-commands` (skill/komut yok).
Sapma: tarif eklenti seçeneği istemedi; en büyük kalem eklentiler olduğu için eklendi.

## Profiller (öneri; Skill gereken iş "orta")
| İş | eklenti | mcp | hafif | açılış |
|---|---|---|---|---|
| yarim, hic, kalan, karar, strix | [] | [] | true | ≈38k |
| video-kaynak (departman/video skill'i lazım) | [] | [] | false | ≈68k |
Araç silinmedi; gerekirse iş json'undan profil gevşetilir.

## A/B
Hafif kol (`ab-hafif`): 3 tur, temiz, doğru çıktı (3 madde özet + 3 doğru commit), 2 dk. Taban kolu 900+ sn dönmedi, elle sonlandırıldı → jev puanı ve %2 kalite farkı ölçülemedi (taban çıktısı yok). Kalite kanıtı: görev çıktısı beklenen içeriği tam taşıyor.
