# BASLANGIC-HIZ-1: `claude -p` başlangıç süresi

Hedef (≤30 sn, araç kaybı yok) **tutmadı**. Kök neden kanıtlandı; çözüm eklenti koduna ya da eklenti kapamaya dokunmadan mümkün değil.

## Ölçüm (varsayılan ayarlar, haiku, `x` istemi)
- Önce: 166 / 188 / 192 sn (ort. 182). Sonra (pazaryeri onarımı): 180 sn. Hata payı ±15 sn.

## Kök neden
- `--settings '{"disableAllHooks":true}'`: **14 sn**, tam eklenti yeniden yükleme geçişi 1.
- Günlükte 28 tam geçiş (2984 skill + komut + 368 eklenti, her biri ~5 sn). Her geçişin hemen öncesinde `$.command.register (<eklenti>): /<komut> listed` var: 27 kayıt = 27 ek geçiş.
- Doğrusal uyum: mods grubu (26 eklenti, `claude-code-mods` + flightdeck) kapalı → 9 geçiş / 100 sn; diğer 43 hook'lu eklenti kapalı → 20 geçiş / 110 sn.
- Kaydı yapan: flightdeck/claude-code-mods hook modüllerinin `session.start` işleyicisi (`hooks/register.tsx`, `$.command.register`). Host her kayıtta komut/skill önbelleğini siler ve hepsini yeniden okur.

## Çürütülen hipotezler (her biri tek başına ölçüldü, süre düşmedi)
- flightdeck kapalı: 159 sn, 27 geçiş.
- Tüm MCP kapalı (`--strict-mcp-config`): 163 sn, 28 geçiş (moneyguide/auth0/godot/unity/serena sebep değil).
- `yerel-kurulum7` cache-miss (86 hata): onarıldı, 180 sn, 26 geçiş.
- 236 YAML frontmatter hatası: 212'si onarıldı, hata 6500→564 satır, 158 sn, 28 geçiş. Onarılan 212 skill listeye girip her oturumun skill listesini şişirdiği için **geri alındı**.
- `MCP_TIMEOUT` (önceki oturum): etkisiz.

## Kalıcı değişiklik
- `~/.claude/plugins/marketplaces/yerel-kurulum7/` oluşturuldu (manifest + supabase 0.1.15 kopyası), `known_marketplaces.json` oradaki yola çevrildi. Süreye etkisi yok; yalnız `cache-miss` hatalarını keser.
- Araç sayısı eşit: etkin eklenti 407, MCP bağlantısı 71/71, "Loaded 2984 unique skills" önce/sonra aynı, `settings.json` bayt-bayt aynı.
- Geri alma: `python -I .kos/kopru/ara/bh/geri_al.py` (yedek: `.kos/kopru/ara/bh/yedek/`). Betikler (gap, bisect, yaml_*) aynı dizinde (`.kos` gitignore'da).

## Karar Ömer'in (araç kapatma/kod yaması gerekir)
1. `claude-code-mods` + flightdeck eklentilerini (27 komut kaydı) yalnız ihtiyaç duyulan projelerde etkinleştir: tahmini −130 sn.
2. Ya da hamzafer/claude-code-mods ve flightdeck `session.start` kaydını tek toplu kayda çevir (üçüncü taraf kodu; güncellemede ezilir).
3. `claude -p` otomasyonu: `--setting-sources project,local` (7 sn) ya da `--settings` ile `disableAllHooks` (14 sn).
