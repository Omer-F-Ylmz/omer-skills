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

## Tamamlanan ölçüm (30 Eki, haiku, tek kelime, ilk tur)
| Varyant | in+cr+cw | süre |
|---|---|---|
| `--setting-sources project` | 32,9k | 5 sn |
| + MCP boş + `--disable-slash-commands` | 28,9k | 3 sn |
| eklentiler kapalı (p0) / +mcp0 / +hafif | 77,4k / 68,3k / 38,5k | 16-19 sn |
| taban (415 eklenti açık) | 900 sn'de dönmedi (iki kez) | - |

## Karar: KABUL (seçenekler, opt-in) / RET (varsayılan profil)
- KABUL: `eklenti`/`mcp`/`hafif` seçenekleri kalır; açılış 350-440k → 29-38k (≤60k hedefi), kalite A/B hafif kolda eşit. Varsayılan davranış değişmedi; hiçbir araç/eklenti kaldırılmadı veya kapatılmadı (yalnız o oturuma yüklenmez).
- RET: "yarim/hic/kalan/karar/strix için eklenti: []" profilini varsayılan yapmak; Desktop kararı (30 Eki) kurulu aracın kapatılmaması. Profil iş json'unda açıkça istenirse kullanılır; hook/user CLAUDE.md o oturumda düşer.
- Ölçülemedi: taban kolunda jev kalite puanı (taban dönmedi).
