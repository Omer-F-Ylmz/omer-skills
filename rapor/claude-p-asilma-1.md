# CLAUDE-P-ASILMA (takip-24eki-a #1)

**Sonuç:** asılma değil, yavaş açılış: `claude -p "echo ok"` 410 etkin eklentiyle 171–190 sn (tavan 90 sn'de "asılı" görünüyordu). Tek suçlu eklenti yok; maliyet eklenti sayısıyla orantılı.

Kanıt (geçici `--settings` ile `enabledPlugins` kapatma; kullanıcı settings.json'u değişmedi; betik `.kos/kopru/ara/claude_p_bisect.py`):

| koşu | süre |
|---|---|
| `--setting-sources project` | 4,7 sn (stalemap-kur-2) |
| tam (410 eklenti) | 190,5 sn |
| 410 eklentinin hepsi kapalı | 23,5 sn |
| 71 hook'lu eklenti kapalı | 34,2 sn |
| yalnız ikinci yarı (205:410) kapalı | 55,4 sn |
| ilk yarı (0:205) kapalı | >110 sn |
| 94 `.mcp.json`'lu eklenti kapalı | >110 sn |
| yalnız flightdeck kapalı | 193 sn (etkisiz) |

- Hook'lu 71 eklenti kapatılınca 190 → 34 sn: ana yük hook modülleri. Hook alt kümeleri (0:36 / 36:71) tek başına kapatılınca da düşmedi → yük birkaç eklentide değil toplamda.
- Debug günlüğü (`--debug-file`, 18,5k satır, ~42 sn kayıt dışı süre): `flightdeck agent.offer` 723 kez, ort. 349 ms (toplam ~279 sn işçi süresi, eşzamanlı), `session.append` 1,2–5,7 sn; MCP: moneyguide 33 sn CONNECT_TIMEOUT, agent-drugs/definely ENOTFOUND, cockroachdb ECONNREFUSED (başlangıçta ağ bekleme). Ayrıca ilk API baytı 5,5 sn.
- Çıkış sonrası Stop kancası arka plana alınıyor (async), asıl bekleme başlangıçta.

**Köprü ajanları etkileniyor:** `ajan_sira.py` ARGV = `cc_profil.kur("ajan")` (`--settings` profili, `--strict-mcp-config`, boş MCP); profilde `enabledPlugins` kapatması 0 giriş → ölçüm: 171 sn açılış. Köprü ajanı başına ~3 dk sabit yük (`yonlendir.py` / `gorsel_hakem.py` / `ucretsiz_havuz.py` ise `--setting-sources ""` ile hızlı).

**En küçük düzeltme (uygulanmadı):**
1. Köprü ajan profiline `pluginKapat` eklemek (repo içi `tools/cc_profil.py` profil tanımı): yalnız gereken eklentiler (claude-mem, headroom, context-mode, ruflo ihtiyacı) açık kalsın; ölçüm 190 → ~25–35 sn beklenir. Hangi eklentinin gerekli olduğu kararı Ömer'in (ajan davranışı değişir).
2. Kullanıcı CC'si için `~/.claude/settings.json` `enabledPlugins` içinde kullanılmayan eklentileri `false` yapmak.

ÖMER: `enabledPlugins` (410 etkin) kullanıcı ayarı; kapatma listesine onay ver, ya da köprü profiline `pluginKapat` eklememi iste.
