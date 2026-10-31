"""TUR 27: tur25/26 kurulan kalemlerin usta kartlari -> usta-tur27.jsonl (kanit kur-tur25/26 tsv'den)."""
import csv, json, time
from pathlib import Path

D = Path(__file__).parent
K = {}
for f in ("kur-tur25.tsv", "kur-tur26.tsv", "kur-tur26-agir.tsv"):
    for r in csv.reader((D / f).open(encoding="utf-8"), delimiter="\t"):
        if len(r) >= 3 and r[0] != "ad":
            K[r[0]] = (r[1], r[2])

# ad, tsv anahtari, tur, lisans, kullanim, kombin, dogrulanamadi
C = [
 ("Ollama", "Ollama", "cli", "MIT",
  ["Yerel model sunucusu: `ollama run gemma4:e4b` (hizli), `qwen3.5:9b` (genel), `bge-m3` (embedding)",
   "API: /api/chat think:false + options.num_ctx (OpenAI /v1 ucu 4096 baglamda dusunmeyle bos donebilir)",
   "Gerekmedikce kapali tut (NIHAI VRAM <=%80): is bitince `ollama stop <model>`"],
  ["ucretsiz_havuz.py son care yerel kol", "Aider/opencode/Cline yerel saglayici olarak", "bge-m3 + gbrain/graphify embedding"],
  ["kalite karsilastirmasi bu turda olculmedi"]),
 ("Claude Code Router (ccr)", "Claude Code Router", "cli", "MIT",
  ["CC isteklerini baska saglayiciya yonlendirir: ~/.claude-code-router/config.json Providers + Router.default", "`ccr code` ile CC'yi router uzerinden ac; `ccr ui` yapilandirma arayuzu"],
  ["OmniRoute ile ayni katman: ikisini zincirleme (ANTHROPIC_BASE_URL cakisir)", "ucretsiz Groq/OpenRouter anahtariyla arka plan isleri"],
  ["anahtar yok: yonlendirilmis gercek cagri olculmedi (`ccr -v` 'No available models')"]),
 ("codex-plugin-cc", "codex-plugin-cc", "plugin", "Apache-2.0",
  ["CC icinden Codex'e is devri: /codex komutlari, codex rescue/review ajanlari", "Ikinci gorus incelemesi icin bagimsiz model (NIHAI hakem kurali)"],
  ["jev/pixeljury ile hakem paneli", "TokenEconomizer Codex tarafi (config.toml enabled)"], []),
 ("Stripe Agent Toolkit", "Stripe Agent Toolkit", "plugin", "MIT",
  ["stripe@stripe plugin: odeme/urun/fiyat islemleri MCP araclariyla", "Test modu anahtariyla (sk_test_) basla, canli anahtar yalniz Omer"],
  ["borsa/e-ticaret siteleri odeme akisi", "api-tester ajaniyla webhook denetimi"],
  ["STRIPE anahtari yok: gercek cagri olculmedi"]),
 ("security-audit skill", "security-audit skill", "skill", "MIT",
  ["Cloudflare security-audit: kod tabaninda OWASP/sir/yapilandirma denetimi, Skill security-audit", "Kurulum oncesi 3. katman (gitleaks + semgrep + bu skill)"],
  ["security-auditor ajani (claude-code-agents) ile ayni ise iki goz", "gitleaks/semgrep ham bulgularini bu skill ile siniflandir"], []),
 ("diagram-design", "diagram-design", "skill", "MIT",
  ["HTML/SVG mimari diyagram uretir; `python scripts/verify-geometry.py <html>` ust uste binme/tasma denetimi (0 finding = gecer)", "Koyu/acik tema ornekleri sablon olarak"],
  ["frontend-craft gorsel kurallari", "graphify ciktisindan mimari cizim", "playwright ile ekran goruntusu + pixeljury hakem"], []),
 ("social-media-skills", "social-media-skills", "skill", "MIT",
  ["17 skill (hook, karusel, thread, icerik takvimi vb.) ~/.claude/skills; `bash validate-skills.sh` 87/0", "Platforma gore skill sec, cikti metnini Voice DNA ile Omer sesine uydur"],
  ["Content Research Writer + Voice DNA", "marketing-skills-paket", "Postiz (yayinlama)"],
  ["gercek bir gonderi uretimi bu turda yapilmadi"]),
 ("Gemini CLI", "Gemini CLI", "cli", "Apache-2.0",
  ["`gemini -p \"...\"` tek seferlik; 1M baglam buyuk repo okuma", "GEMINI_API_KEY ya da Google girisi (Omer)"],
  ["ucretsiz_havuz Gemini kolu ile ayni kota (gunluk PerDay 429)", "buyuk log/rapor ozetini Gemini'ye ver, Claude jetonu harcama"],
  ["anahtar yok: gercek istem olculmedi"]),
 ("opencode", "opencode", "cli", "MIT",
  ["`opencode run \"...\"` acik kaynak kodlama ajani; saglayici olarak Ollama/OpenRouter/Groq", "install-script onayi verilmedi; CLI 1.19.5 calisiyor"],
  ["Ollama yerel kol", "TokenEconomizer opencode destegi (kurulu degil, eklenebilir)"],
  ["saglayici anahtari girilmedi: kod gorevi olculmedi"]),
 ("Cline", "Cline", "cli", "Apache-2.0",
  ["`cline` 3.0.74 CLI: plan/act modlu kodlama ajani; VS Code eklentisinin terminal surumu", "Saglayici: OpenRouter/Ollama"],
  ["opencode/Aider ile ayni sinif: kisa isi Aider, cok dosyali isi Cline"],
  ["saglayici anahtari girilmedi: kod gorevi olculmedi"]),
 ("Repomix", "Repomix", "cli", "MIT",
  ["`repomix --style markdown --compress -o tmp/repo.md <dizin>` repoyu tek dosyaya paketler (LLM'e verilecek baglam)", "--include/--ignore ile dar paket; --token-count-tree jeton dagilimi"],
  ["Gemini CLI 1M baglama tek dosya", "ucretsiz modele repo ozeti", "graphify yerine tek-seferlik dis repo incelemesi"], []),
 ("Aider", "Aider", "cli", "Apache-2.0",
  ["`aider --model <saglayici/model> dosya.py` git-farkindaliklı duzenleme, her degisiklik commit", "--no-auto-commits ile Omer kurali (yalniz kendi dosyalarin)"],
  ["Ollama/Groq ucretsiz kolu", "Repomix paketiyle baglam"],
  ["LLM anahtari girilmedi: duzenleme olculmedi"]),
 ("scrapling", "scrapling", "cli", "BSD-3-Clause",
  ["`uv tool install \"scrapling[shell]\"` (yalin kurulum click eksik exit 1)", "`scrapling extract get <url> out.md` statik; fetch/stealthy-fetch dinamik/korumali sayfa"],
  ["playwright MCP (etkilesimli), scrapling (toplu cekim)", "markitdown/anydoc donusum", "ScrapeGraph LLM cikarimi"], []),
 ("anydoc", "anydoc", "cli", "MIT",
  ["`anydoc <dosya>` CSV/PDF/DOCX/XLSX -> markdown (stdout)", "skill convert-documents-to-markdown CC'de"],
  ["markitdown ile ayni sinif: ikisinden temiz tablo vereni sec", "Repomix/ucretsiz model ozetine girdi"], []),
 ("openai-whisper", "openai-whisper", "cli", "MIT",
  ["`whisper ses.mp3 --model tiny --language en` (CPU); Windows'ta PYTHONUTF8=1 sart (cp1254 --help UnicodeEncodeError)", "Agir is icin faster-whisper large-v3 (WER yarisi) tercih"],
  ["video_derin.py Groq ASR yedegi (cevrimdisi)", "yt-dlp ses indirme + whisper"],
  ["large model WER bu turda olculmedi"]),
 ("Playwright MCP", "Playwright MCP", "mcp", "Apache-2.0",
  ["Kurulu yol %APPDATA%/npm/playwright-mcp --headless (npx zaman asimi veriyordu)", "25 arac: browser_navigate/snapshot/click/take_screenshot"],
  ["ekran kurali: yalniz headless, varsayilan tarayici acilmaz", "frontend-craft tur raporu ekran goruntusu", "scrapling toplu cekim"], []),
 ("genjutsu", "genjutsu", "plugin", "MIT",
  ["genjutsu@genjutsu v4.1.1, 20 skill; konu/skill adina gore cagir", "check-evals.py 6 hata upstream (bizim kurulum degil)"],
  ["frontend-craft > diger skill kurali gecerli"], ["skill ciktilarinin kalite olcumu yapilmadi"]),
 ("motionsites-web-builder", "motionsites-web-builder", "plugin", "MotionSites ozel lisans",
  ["Tek SKILL.md: hareketli site bolumleri uretimi", "Lisans kosullari: ticari kullanimdan once okunmali"],
  ["frontend-craft + impeccable sirasi", "K2c-anim hazir animasyon kaynaklari"], ["gercek site uretimi olculmedi"]),
 ("scientific-agent-skills", "scientific-agent-skills", "plugin", "MIT",
  ["177 bilimsel skill (biyoinformatik, kimya, veri bilimi, NOAA/dnanexus API)", "Konu alani dardir: is bu alandaysa adiyla cagir"],
  ["markitdown/anydoc makale donusumu", "jev ile literatur siniflama"], ["skill ciktilari olculmedi"]),
 ("filmcraft (storytold)", "storytold/filmcraft (filmcraft-cli 0.15.0)", "cli", "kaynak repo lisansi",
  ["target/release/filmcraft-cli.exe; `filmcraft-cli commands` komut listesi (file.newProject ...)", "Derleme: cargo build --release -j 2 -p filmcraft-cli (~18 dk, RAM dusuk)"],
  ["Remotion/LTX klip uretimi sonrasi kurgu", "OpenMontage"], ["gercek proje dosyasi uretimi olculmedi"]),
 ("open-seo", "open-seo (every-app/open-seo, MIT)", "uygulama", "MIT",
  ["pnpm install --frozen-lockfile --ignore-scripts; vitest 4/4", "DATAFORSEO kimligi env'e (omer-anahtar-listesi.md) sonra pnpm dev"],
  ["marketing-skills-paket SEO skill'leri", "scrapling site cekimi"], ["anahtar yok: canli SEO sorgusu olculmedi"]),
]

out = []
for ad, anahtar, tur, lis, kul, kom, dog in C:
    durum, kanit = K[anahtar]
    out.append({"ad": ad, "tur": tur, "kaynak": "ana-liste (video)", "lisans": lis, "kullanim": kul, "kombin": kom,
                "kanit": f"{durum}: {kanit}"[:600], "dogrulanamadi": dog, "parti": "video-izle-kur-1-tur27",
                "tarih": int(time.time()), "model": "opus"})
(D / "usta-tur27.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in out) + "\n", encoding="utf-8")
print(len(out), "kart")
