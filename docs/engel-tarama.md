# ENGEL-TARAMA-1 (22 Eki 2026)

Tarama kapsamı: köprü (ajan_sira, cc_profil, model_sec, yonlendir, ucretsiz_havuz, cc-kopru `komut`), CC ayarları (global + proje settings, hook'lar, MCP, plugin), skill görünürlüğü. Env değerleri okunmadı/basılmadı.

| # | Yer | Ne engelliyor | Neden konmuş | Etki | Karar | Token |
|---|-----|---------------|--------------|------|-------|-------|
| 1 | `.claude/settings.json` skillOverrides `graphify: off` (proje) | `/graphify` skill'i omer-skills'te gizli; global kural "/graphify'da önce onu kullan" | skill-arac eşlemesi (TOKEN-3b) | Skill yolu kapalı (CLI çalışıyor) | KALDIR → `name-only` (uygulandı) | +~10 jeton (tek ad) |
| 2 | aynı dosya `ui-ux-pro-max: off` | Global kural zincirinde (frontend-craft > impeccable > ui-ux-pro-max) anılan skill çağrılamıyor | aynı | UI işinde zincirin 3. halkası yok | KALDIR → `name-only` (uygulandı) | +~10 jeton |
| 3 | `beyin` komutu PATH'te yok (Git Bash + PowerShell) | ÖN SÖZ 2/2e/6 `beyin ara/kaydet` "command not found" | tools/beyin.py kısayolsuz | Her görevde 2. beyin adımı düşüyor | KALDIR → `~/.local/bin/beyin(.cmd)` kısayolu (uygulandı, `beyin ara` çalışıyor) | 0 |
| 4 | cc_profil "ajan" `ajanTut` yalnız 2 ajan; ~780 `Agent(...)` deny | Köprü oturumunda `ajn-slash-komut-yazar` vb. çağrılamaz/listede yok | TOKEN-2 K2: ajan listesi sabit tabanın %47'si | ZORUNLU-ARAÇ ajanları köprüde yok; yedek yol `Skill ajan-getir` | KALSIN (token kazancı büyük, yedek yol önsözde yazılı) | −büyük |
| 5 | cc_profil "ajan" `--tools` listesinde Skill yok; `--disable-slash-commands` | Köprüde Skill aracı | TOKEN-4 A6 | `ajan-sira.slash` (dar=cekirdek) dosyası var → açık; mcp-ac-1 MCP'yi açtı | KALSIN (bayrak zaten açık) | — |
| 6 | `ajan-sira.ders` / `.ordu` / `.ordu-kabul` | Varsayılan kapalı bayraklar | RUFLO-2 / ORDU-1 | Üçü de dosyada mevcut = açık; `.ordu-on` yok (mekanik ön-özet kapalı) | KALSIN (`.ordu-on` ayrı karar: kapalı kalması token tasarrufu) | — |
| 7 | `block-destructive.ps1` | `rm -rf`, `git push --force`, `reset --hard`, `DROP DATABASE`, ada göre süreç öldürme | Silme/sır koruması | Meşru güvenlik | KALSIN-güvenlik | 0 |
| 8 | cc-kopru `komut` allowlist (vercel `--prod`, python `-c`/dosya zorunlu, git salt-okur, gh repo delete, strix kos:false) | Desktop köprüsünden deploy/yazma | Üretim/ücretli çağrı tavanı kuralı | Desktop'tan `git commit`/`vercel --prod` yok; CC'den yapılır | KALSIN-güvenlik | 0 |
| 9 | Global `skillOverrides`: 329 `off` (314 `anthropic-skills:*` = claude.ai senkron gölgesi; 198'inin başka kaynaktan eşi var) | Gölge kopyalar gizli | Çift listeleme önleme | 131 eşsiz kapalı: cli-*, omni-*, gstack-* (kısa adlı kopyaları açık), roblox/wpf/hetzner. Atlas/departman kitaplarında geçen 42 skill adı hepsi çözülüyor (off olan yok; `example-skills:docx/pptx/xlsx/pdf` varsayılan açık) | KALSIN | — |
| 10 | `skillListingBudgetFraction 0.02`, 2416 `name-only` | Açıklama kesilir; keşif `yetenek-getir`/`katalog_ara` ile | Sabit taban küçültme | Çağrı açık; yalnız otomatik tetik zayıf | KALSIN | −büyük |
| 11 | `ENABLE_TOOL_SEARCH=false` | Ertelenmiş MCP şeması yok, hepsi yüklü | Araç bulma ek turunu önler | Engel değil, maliyet | KALSIN (ölçüm ayrı iş) | — |
| 12 | Global kapalı plugin'ler: banana-claude, claude-mem-cowork, data/engineering/product-management@synced, output-style'lar, playwright@official, watch@claude-video | Bu plugin skill/ajanları | Çift enjektör (cowork, PolyForm-NC), synced gölge, playwright MCP profilde zaten var, `slash-dar:watch` var | Eşleri açık | KALSIN | — |
| 13 | Proje kapalı plugin'ler: dotnet-*, phoenix-*, design-mastery, discernment-nudge, `taste-skill` | omer-skills'te bunların skill'leri | Alaka dışı / token | `taste-skill` global açık, proje kapalı: frontend-craft kuralı gereği zincirin en altı | KALSIN (UI işi başka projede açılır) | — |
| 14 | Sistem `disableClaudeAiConnectors: true` | claude.ai bağlayıcıları (Gmail/Drive vb.) CC'de yok | Jeton/gürültü; MCP'ler yerelde | Bilinçli | KALSIN | — |
| 15 | `.claude/settings.json` çalışma ağacında başkasının bekleyen diff'i (plugin sırası, `supabase: true`) | Bu oturum o dosyayı commit edemedi | Paralel oturum | Yukarıdaki 1–2 değişikliği dosyada, commit dışı | DUR notu: paralel oturum commit edince gelir | — |

Bulgu 15; KALDIR/DARALT 3 (1, 2, 3), KALSIN 12. Kök neden "ajan_sira boş MCP" (mcp-ac-1, `8289e458`) korundu; ayrıca ona ek engel bulunmadı.

Yedek: `.kos/kopru/cop/settings.json.engel-yedek` (değişiklik öncesi proje settings). `beyin` kısayolu yeni dosya; geri alma = `~/.local/bin/beyin` ve `beyin.cmd` silinir.

Ölçüm: jeton etkisi ad sayısından tahmin (2 skill adı ≈ +20 giriş jetonu); `claude -p` ölçümü yapılmadı (tur sınırı).

Uçtan uca kanıt: bu oturumda `Skill` aracı listede (graphify, plan-kur, slash-dar:* vb.), `katalog_ara` koştu, `beyin ara` kısayoldan sonuç döndü; ruflo `memory_search`/`pattern-store` ve `beyin kaydet` bu oturumda koşturulmadı (ruflo MCP ne bu oturumda ne de araştırmada görüldü).
