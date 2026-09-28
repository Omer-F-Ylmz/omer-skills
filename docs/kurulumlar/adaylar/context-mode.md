# context-mode
ad: context-mode
tur: MCP
video: v-vRYtvWDYs
repo: mksglu/context-mode
lisans: Elastic-2.0
son_commit: 2026-09-28
arsiv: hayır
kaynak: yok
telemetri: kapalı
arastirma: tam
## Ne
MCP sunucusu + hook seti: araç çıktısını (Playwright/log/GitHub issue vb.) sandbox'ta işleyip özet döndürür, oturum verisini SQLite+FTS5'e kaydeder, ctx_execute ile "kod yazıp sadece sonucu döndür" akışı sunar.
## Kanıt
- yıldız 24172 · son commit 2026-09-28 (aktif, arşiv değil) · lisans Elastic-2.0 (source-available, OSI açık kaynak değil)
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok (tür MCP, skill klasörü yok)
- README: "No telemetry, no cloud sync, no usage tracking" — bağımsız derleme (PulseMCP dizini, community post) bu iddiayı tekrarlıyor; ctx_insight (hosted dashboard) istisna, kodu doğrulanmadı
## Kurulum
- mcp: context-mode -- npx -y context-mode
## İzinler
Hooks (PreToolUse/PostToolUse/UserPromptSubmit/PreCompact/SessionStart/Stop) her araç çağrısını ve prompt'u görür; ctx_execute sandbox'ta js/py çalıştırır (dosya sistemi erişimi var); SQLite (ev dizini) dosya/git/hata/karar geçmişini yerelde saklar.
## Duman testi
- komut: npx -y context-mode --version
- cikis: 0
- desen: \d+\.\d+\.\d+
## Geri alma
- mcp: context-mode
## Köprü izni
- arac: context-mode
- altIzin: --version, doctor
## Önerilen katman
T2 (çalıştırılabilir her şey) — MCP server + hooks + sandbox kod çalıştırma; .md-only değil
## Özellikler
### sandbox-context-saving
ne: Ham MCP çıktısını (56 KB Playwright snapshot vb.) sandbox'ta işler, context'e özet döndürür (README iddiası: 315 KB → 5.4 KB, %98)
kurulum: MCP tool ctx_execute/ctx_batch_execute, plugin kurulumunda otomatik devrede
lisans: Elastic-2.0
etiket: token
karar: DENE
gerekce: hipotez: RTK+headroom üstüne ek kazanç var mı · metrik: token · bütçe: 1 aday görev · geri_alma: mcp kaldır · eşik: %20 üstü ek tasarruf yoksa RED
## Mekanizma
### sandbox-context-saving
nasıl: Araç çıktısı alt süreçte (sandbox) tutulur, context'e yalnız istenen alan/özet yazılır; ham veri SQLite/diskte kalır, ctx_search ile FTS5 üzerinden geri çağrılır
neden: Bağlam penceresine giren token miktarı ham veri boyutundan bağımsızlaşır, tekrar okuma tam metin değil BM25 sorgusuna döner
koşul: Tek seferlik küçük çıktılarda (zaten <1 KB) kazanç yok; sandbox/IPC kurulum maliyeti küçük görevde net kaybettirebilir
bizde: RTK proxy + headroom zaten aynı sıkıştırma katmanını yapıyor; context-mode eklemek olası ikinci/çakışan katman
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
