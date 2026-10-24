HERMES-KUR-1 (Ömer 24 Eki 16:25: "hermes2'yi bütün alt ajanlarımıza, sana ve CC'ye kuralım")
Varsayım (Desktop): "hermes2" = Nous Research Hermes Agent (github.com/NousResearch/hermes-agent, son sürüm v0.22.5, 23 Eki 2026). "Hermes 2" adında ayrı ürün bulunamadı. Repo/README'de "2" ile anılan ayrı bir şey (ör. Hermes 2 model ailesi, v2 mimari) çıkarsa onu da kur, raporda yaz.

Kurallar: NİHAİ 31/32/32f · silme yok · anahtar dosyaya yazılmaz (yalnız mevcut ortam değişkeni ADLARI) · Claude aboneliği Hermes'e/proxy'ye bağlanmaz · RAM <%89 · C ≥80 GB · işler <4 dk parçalar, indirme arka planda · K2q (varsayılan tarayıcı açılmaz).

PARÇA 1 — öğren (kurmadan önce): README + docs + son 3 sürüm notu (v0.22.x). Çıkar: kurulum yolu (Windows yerel mi, WSL2 mi), model sağlayıcıları, MCP sunucu/istemci kipi, skill sistemi (agentskills uyumu), öğrenen bellek/oturum araması, alt ajan/delegasyon, cron/zamanlayıcı, gateway, plugin/hook. Notu 2. beyne + docs/hermes-ogrenme.md.
PARÇA 2 — güvenlik: gitleaks + semgrep (p/secrets, p/python) + agentshield tara; kurulum betiğini satır satır oku (uzaktan curl|bash ÇALIŞTIRMA; repoyu klonla, pip/uv ile kur). Kırmızı bulgu → DUR.
PARÇA 3 — kur: Windows yerelde çalışıyorsa uv ile ayrı venv (araclar/hermes). Yalnız WSL2 destekliyse docker-kur-1'in kurduğu WSL2'ye kur (docker-kur-1 bitmeden bu parçaya geçme; kuyruk koşulu). Bellek sınırı: WSL .wslconfig memory=3GB paylaşılır.
PARÇA 4 — modeller: ücretsiz havuz önce (OpenRouter ücretsiz modeller, Groq, Gemini, NVIDIA, Mistral, Cloudflare, SambaNova; Nous Portal ücretsiz kotası varsa o da). Yerel Ollama SON ÇARE. Sağlayıcı sırası model merdiveniyle uyumlu.
PARÇA 5 — üç yere bağla:
  a) CC: Hermes'i MCP olarak ~/.claude.json'a (user-scope) ekle; CC'den bir delegasyon testi.
  b) Desktop (Claude): claude_desktop_config.json'a (gerçek dosya %LOCALAPPDATA%\Claude-Data\…\claude_desktop_config.json, komutlar TAM YOL, değişiklik onay/ betiğiyle) MCP ekle; Desktop yeniden başlatma gerekirse raporda "DESKTOP:" satırı.
  c) Alt ajanlar: ajan_sira.py'ye `motor=hermes` seçeneği (görev satırında) + model merdiveninin en alt ücretsiz basamağı olarak Hermes; kırmızı-önce test, tam suit. Kolay işlerde varsayılan aday.
  d) (BEYIN-ARAC-KART-1 notu, 24 Eki) arac-ara MCP'si (tools/arac_ara_mcp.py; kur: tools/arac_ara_kur.py) Hermes'e de eklenir; bütün MCP'ler tek code-mode geçidinden (tools/cm.py) açılırsa Hermes yalnız o geçide bağlanır, arac_ara ile aracı bulup aynı geçitten çağırır.
PARÇA 6 — öğrenme döngüsü: Hermes'in kendi bellek/skill üretimini 2. beyin (Obsidian) + ruflo ile bağla (Hermes'in ürettiği skill'ler omer-skills'e aday olarak düşsün, güvenlik kapısından geçsin). arac-ajan-ozellik-1 ile çakışmasın: o görev Hermes'i de kapsasın diye gorev-arac-ajan-ozellik-1.md'ye tek satır ekle.
PARÇA 7 — skill: skills/hermes-desktop (Desktop/CC kullanım rehberi) + claude.ai zip'i dist/claude-ai/yukle-24eki'ye.
KABUL: CC'den ve Desktop'tan Hermes MCP çağrısı başarılı · bir alt ajan işi motor=hermes ile ücretsiz modelde bitti (çıktı + süre + $0) · güvenlik temiz · RAM ölçümü (boşta/çalışırken).
Rapor rapor/hermes-kur-1.md ≤15 satır. Commit "HERMES-KUR-1:". Push YOK. Bitmezse gorev-hermes-kur-1-devam.md + _ekle.
NİHAİ 31+32: başlamadan nihai kapı; her adımda 2. beyne yaz (≤2 dk), ruflo pattern-search önce + store sonra; 32(f) tam ilgili küme; ders çıkar.