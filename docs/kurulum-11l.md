# KURULUM-11l — köprü kontrol 2 açıkları + claude-design köprüsü + ertelenenler

Taban commit: `e3b6faa` (87 test) → faz A `1ae0a99` · B `391d07b` · B2 `fe94de9` (108 node + 44 pytest) → B3.

## K1 — claude-design köprüsü
23 şema `tasarim-semalar.json`'dan birebir yayınlanır; gövde `claude -p` aktarıcısına gider, sonuç `tool_result` bloğundan alınır. Açılışta spawn yok. Ayrıntı: `docs/desktop-eslesme.md` §11.

## K1c — sahte aktarıcı yalnız `test/yardim/`
`CC_KOPRU_SAHTE_AKTARICI` yalnız `tools/cc-kopru/test/yardim/` altındaki **var olan** bir dosyayı kabul eder; `..` ile dışarı çıkılamaz, tanımsız/boş/dış yol yok sayılır → gerçek `claude` seçilir. Pin: dış yol verilip PATH boşaltıldığında `claude PATH'te bulunamadı` döner (sahteye düşmez).

## K2 — `npx`/`bunx` `--` normalleştirmesi
Kök neden npm'in npx argüman ayrıştırması (rtk aklandı). `komutDenetle()` gerekli bayraktan (`--no`/`--no-install`) sonra `--` ekler; zaten varsa ikinci kez eklenmez.

## K3 — katalog blok skaleri + `sayi`
`aciklamaOku()` blok skaler göstergesinde izleyen ilk anlamlı satırı alır; `katalog` aracına `sayi: true` eklendi (yalnız tür başına sayı).

## K4 — deny açığı (iç içe `bin`)
`tools/deny-11l.ps1` (`-Apply`siz kuru koşu, yedek `settings.json.bak11l`, `ConvertTo-Json -Depth 100`): `**/bin/Debug/**` · `**/bin/Release/**` · `**/obj/**` eklenir; `**/bin/**` eklenmez.

## K5 — `durum` yerel günü
`yerelGun()` (`sv-SE` + `Europe/Istanbul`) üç UTC çağrısının yerine geçer.

## K6 — claude-mem kota teşhisi (yalnız teşhis, uygulama yok)
- Worker **sağlıklı**: `/api/health` 200, sürüm 13.25.2, `initialized` + `mcpReady` true, `managed:false`.
- Kuyruk **boş**: `/api/processing-status` → `isProcessing:false · queueDepth:0 · parkedSessions:0` (dalga başındaki 443 kuyruğu kalmamış).
- Sağlayıcı `claude`, kimlik "Claude Code OAuth token (system keychain)"; `lastInteraction: null` — sıfırlamadan beri gözlem denemesi yok.
- **Limit uçtan `allowed` görünüyor:** `rateLimits.five_hour.status = allowed`, `unifiedWindows` beş saat **%0**, yedi gün **%0**; beş saatlik pencere ~4,9 saat, yedi günlük ~6,7 gün sonra sıfırlanıyor. `overageStatus: rejected` (`org_level_disabled`).
- Teşhis: tüketilen kota **şu an uçta görünmüyor** — hesap penceresi boş. Oturum başındaki "allowance exhausted" uyarısı gözlemcinin **kendi geri çekilme (backoff) durumundan** geliyor; tarif gereği worker yeniden başlatılmadı, sağlayıcı değiştirilmedi.
- Seçenekler (karar Ömer'de): (a) beş saatlik pencere sıfırlandıktan sonra gözlemcinin kendi denemesini beklemek · (b) `~/.claude-mem/settings.json`'da sağlayıcıyı Gemini/OpenRouter'a almak — **iki anahtar da boş**, önce anahtar gerekir · (c) worker'ı yeniden başlatıp backoff'u sıfırlamak (uç `allowed` derken en olası düzeltme; tek riski gerçekten kota doluysa yeniden deneme yığını).

## K7 — Headroom yönlendirmesi
Ölçüm (bu dalga, aynı gövdeler): tekrarlı 87 KB log → 3-gram tekrar **0,624**, 6,3 sn, 27006→18915 jeton (**%30**, kayıpsız). Karışık markdown 31 KB → tekrar **0,047**, 4,1 sn, 13784→1834 jeton ama **kayıplı**: `## Bolum` başlıkları ve `Kanit …` ölçüm satırları çıktıda yok, yalnız tablo satırları CSV'ye dönüyor.
Uygulama: `tekrarOrani()` < `TEKRAR_ESIK` (0,3) ise Headroom **hiç çağrılmaz**, doğrudan `kirp`. Tavan tarifte 3 sn'ydi; ölçüm başarılı sıkıştırmanın 6,3 sn sürdüğünü gösterdiği için 3 sn bütün sıkıştırmayı kapatırdı → **10 sn** (aşılırsa fail-open kırpma).

## K8 — frontend-craft 1.5.6
Delta: ÇEKİRDEK'e Design + 21st zinciri satırı · Bölüm 10'a sabit araç eşlemesi (`get_inspiration` + `record_inspiration_feedback` · `get_component` · `get_theme` · `search_logo`) · yeni **Bölüm 12 teslim kapısı** (`design:design-critique` + `design:accessibility-review`, eklenti kapalıysa rapora yazılır; Desktop'taki Design projesi gerekiyorsa cc-kopru `claude-design` köprüsü). Sürüm `1.5.5` → `1.5.6`.
Doğrulama: `skillOverrides`'ta `design` eklentisinin skill'leri için off anahtarı **yok** (eşleşen adların hepsi `anthropic-skills:*` kopyaları); `design:*` skill'leri oturumda görünüyor.
**Kurulu önbellek 1.5.3 → güncelleme komutu (Ömer koşar):** `claude plugin update frontend-craft@omer-skills` — `claude plugin --help` birebir: "update [options] <plugin> · Update plugin to latest version (restart required to apply)". Kurulu sürümün 1.5.6 olduğu doğrulaması **sonraki oturuma** kalır.

## K9 — omni-*/cli-* doğrulama
`~/.claude/settings.json` `skillOverrides`: **23 `omni-*` + 22 `cli-*` girişin hepsi `off`** → CC tarafında ek iş yok. claude.ai'de bu adlar hâlâ açık; Customize → Skills'ten kapatılacak ad listesi:

- `omni-agents-a2a`
- `omni-api-keys`
- `omni-auth`
- `omni-budget`
- `omni-cache`
- `omni-cli-tools`
- `omni-combos-routing`
- `omni-compression`
- `omni-context-rtk`
- `omni-db-backups`
- `omni-github-skills`
- `omni-inference`
- `omni-mcp`
- `omni-models`
- `omni-providers`
- `omni-proxies`
- `omni-resilience`
- `omni-settings`
- `omni-sync-cloud`
- `omni-tunnels`
- `omni-usage-logs`
- `omni-version-manager`
- `omni-webhooks`
- `cli-a2a`
- `cli-anything`
- `cli-backup-sync`
- `cli-batches`
- `cli-chat`
- `cli-compression`
- `cli-contexts`
- `cli-cost-usage`
- `cli-eval`
- `cli-health`
- `cli-keys`
- `cli-mcp`
- `cli-models`
- `cli-plugins-skills`
- `cli-policy-audit`
- `cli-providers`
- `cli-resilience`
- `cli-routing`
- `cli-serve`
- `cli-setup`
- `cli-skill-collector`
- `cli-tunnel`

## K10 — scroll-craft doğrulaması
`node <skill>/scripts/doctor.mjs` → **exit 0, "Ready"**: node v24.19.0 ok · ffmpeg full build (536 filtre, libwebp) ok · Chrome ok · workspace ok. Üç **isteğe bağlı** eksik: `playwright-core` (yalnız doğrulama pass'i için, **build klasörünün içine** `npm i playwright-core` — global kurulum beklenmiyor; scrollcraft proje kökü `Portale` bu bağımlılığı zaten taşıyor), `KIE_AI_API_KEY` (yalnız görsel üretimi için), workspace registry (`workspace.mjs --ensure`). Kök neden: "18 Eyl'den açık" kalemi kusur değil — playwright-core proje-yerel bağımlılık.

## K11 — 7 `-desktop` skill + dağıtım
`dist/yukle-11k/replace` zip'lerinden tek seferlik `skills/<ad>-desktop/SKILL.md` açıldı (her gövdede "cc-kopru" doğrulandı). `description` yeniden yazıldı (ekleme değil): `<araç> CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. Komut şablonu ve çıktı yorumu.` — uzunluklar 117-128 (tavan 200).
Dağıtım `dist/yukle-11l/replace/`: 7 `-desktop` zip + `frontend-craft.zip` (1.5.6, `references/` dahil).

## K12 — docs
`docs/desktop-eslesme.md` §11 (köprü kontrol 2 tablosu · claude-design yapısal sınırı · K1 yolu · B2 kök nedeni) + bu dosya.

## Ölçüm
| ölçüm | değer |
|---|---|
| claude-design çağrı başına (taban, ayarlar açık) | 72.321 girdi jetonu · $0,0910 · 15 sn |
| headroom tekrarlı log | 6,3 sn · 27006→18915 jeton (%30) · 3-gram tekrar 0,624 |
| headroom karışık markdown | 4,1 sn · 13784→1834 jeton ama **kayıplı** · tekrar 0,047 |
| claude-mem rate limit (uç) | five_hour `allowed` · beş saat %0 · yedi gün %0 |
| dağıtım | `skill_denetim` 8 zip · 0 hata · `duman_claudeai` 8 zip · 0 sorunlu |

## Sapmalar
1. K7 tavanı 3 sn yerine **10 sn**: ölçümde başarılı sıkıştırma 6,3 sn sürüyor, 3 sn Headroom'u tümden kapatırdı.
2. K7 kapısının gerekçesi "karışık markdown %0 kazanç" değil **içerik kaybı**: bu dalganın ölçümünde karışık markdown %87 küçüldü ama başlık ve kanıt satırları düştü.
3. K11'de "gövde değişmez" tam tutmadı: 7 gövdede tek bir çit etiketi (bash → text) düzeltildi. Bloklar yer tutuculu komut şablonu; `duman_claudeai` bash bloklarını çalıştırdığı için `<yol>` gibi yer tutucular sözdizimi hatası veriyordu (aynı hata `dist/yukle-11k/replace`'te de vardı: 8 zip · 7 sorunlu). Etiket düzeltmesiyle 0 sorunlu.
4. K9'da `cli-*` giriş sayısı 21 değil **22**; hepsi off.
5. K11 description uzunlukları 117-128 (tarifte 124-135); aynı kalıp, tavanın çok altında.
6. K6'da `claude -p` harcanmadı; teşhis worker'ın kendi uçlarından yapıldı (sayaç 6/6 dolu).
