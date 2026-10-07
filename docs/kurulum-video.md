# KURULUM-VİDEO K6 — kurulanlar · K0 · S1–S6 · SkillSpector · ölçümler (2026-10-07)

Kaynak: `C:\Projeler\.tmp-video\notlar\k0-k1.md`, `notlar\k2.md`, `olcum\ozet-s1-s5.md`, `olcum\ozet-s6.md`. `tools/video` değişmedi. Claude Code'a MCP/plugin kaydı yok, skill CC'ye kurulmadı.

## 1. Kurulanlar

KAPALI = kayıtsız CLI (MCP/plugin kaydı yok). KUR-AÇIK = venv'e kurulu kütüphane, çağıran kod açar. Kök: `C:\Projeler\.tmp-video`.

| ad | sürüm | yer | durum | lisans | SHA | çalıştırma / açma |
|---|---|---|---|---|---|---|
| claude-real-video (crv) | 0.10.7 (uv tool, [fast]) | `~\.local\bin\crv.exe`, klon `src\claude-real-video` | KAPALI | MIT | 08309bb | `crv <url> -o <çıktı>` |
| summarize | 0.25.1 (npm -g) | node-v24.19.0 dizini, klon `src\summarize` | KAPALI | MIT | 2c136db (v0.25.1) | `summarize <url> --extract` |
| mcp-video-analyzer | 0.10.1 (npm -g) | node dizini, klon `src\mcp-video-analyzer` | KAPALI | MIT | c321734 | `mcp-video-analyzer analyze <url> --ocr-language eng` |
| claude-video (watch) | yalnız klon | `src\claude-video` | KAPALI | MIT | 03ceb42 | `py -3.12 skills\watch\scripts\watch.py <url> --detail transcript --no-whisper` |
| youtube-research-mcp | yt-research-mcp 1.0.0 (editable) | `diterex-venv`, klon `src\youtube-research-mcp` | KAPALI | MIT | 4cf8856 | `diterex-venv\Scripts\yt-research-mcp.exe` (MCP stdio) |
| youtube-mcp-server (coyaSONG) | 1.2.0 | klon `src\youtube-mcp-server` (npm ci + build) | KAPALI | MIT | 06d5e7a | `node dist\stdio-server.js` |
| whisper.cpp | v1.8.0 cuBLAS 12.4.0 | `whisper.cpp\v1.8.0\Release\whisper-cli.exe` | KAPALI | MIT | - | `whisper-cli.exe -m models\ggml-large-v3-turbo.bin -f a.wav -l auto` |
| ggml-large-v3-turbo | 1 558 428 318 B | `models\` | veri | MIT | - | HF ggerganov/whisper.cpp |
| Tesseract | 5.4.0.20240606 (winget) | `C:\Program Files\Tesseract-OCR\tesseract.exe` (PATH'te değil) | KAPALI | Apache-2.0 | - | `$env:TESSDATA_PREFIX='...\tessdata'; tesseract g.png - -l eng+tur` |
| tessdata_best | 4.1.0 (eng, tur) | `tessdata\` | veri | Apache-2.0 | - | `tesseract --list-langs` |
| faster-whisper | 1.2.1 (ctranslate2 4.8.2) | `venv` | KUR-AÇIK | MIT | - | `venv\Scripts\python.exe -c "from faster_whisper import WhisperModel"` |
| faster-whisper modeli | large-v3-turbo CT2 (1.62 GB) | `models\faster-whisper-large-v3-turbo` | veri | MIT | - | HF mobiuslabsgmbh (Systran değil) |
| Silero VAD | v6 | faster_whisper içinde `silero_vad_v6.onnx` | KUR-AÇIK | MIT | - | `transcribe(..., vad_filter=True)` |
| RapidOCR | 3.9.2 (+ onnxruntime 1.30.0) | `venv` | KUR-AÇIK | Apache-2.0 / MIT | - | `venv\Scripts\python.exe ocr_dene.py kare.png` (PYTHONUTF8=1) |
| RapidOCR Latin modeli | PP-OCRv5 rec mobile (7.9 MB) | `models\rapidocr\` | veri | - | - | `RapidOCR(params={"Rec.model_path":..., "Rec.rec_keys_path":...})` |
| google-genai | 2.28.0 | `venv` | KUR-AÇIK | Apache-2.0 | - | `python -c "import google.genai"` |
| sqlite-vec / fastembed | 0.1.9 / 0.8.1 | `venv` | KUR-AÇIK | MIT·Apache / Apache-2.0 | - | `python -c "import sqlite_vec, fastembed"` |
| yt-fts / markitdown | 0.1.62 / 0.1.8 | `venv` | KUR-AÇIK | MIT | - | `venv\Scripts\yt-fts.exe --help` · `markitdown.exe dosya.pdf` |
| yt-dlp | 2026.08.19 (güncel) | `~\.local\bin\yt-dlp.exe` | KUR-AÇIK | Unlicense | - | `yt-dlp --version` |

SHA: 6/6 önek uyumlu. Lisans: 6/6 klon MIT, özel koşul yok. Python 3.12.10, uv 0.12.12, kilit `venv-kilit.txt`. GPU RTX 4070 Ti.

Sapmalar:
- mcp-video-analyzer: npm'de 0.10.2 yok, 0.10.1 kuruldu. Klon c321734 = 0.10.2 kaynak (v0.10.1 üstü 16 commit). `--ocr-language` 0.10.1'de de var.
- Tesseract: winget 5.4.0.20240606 (hedef 5.5.3 değil), UAC istemedi.
- whisper.cpp: v1.9.x release'lerinde binary yok, v1.8.0 cuBLAS (en yeni CUDA paketi 12.4.0).
- RapidOCR: varsayılan PP-OCRv6 ch, Latin değil. Latin PP-OCRv5 mobile elle `model_path` ile (otomatik indirme python'dan ModelScope'ta düştü, curl 200 aldı).
- crv: etiket farkı yok. pyproject 0.10.7 = etiket v0.10.7, klon HEAD etiketin 1 commit üstü. `crv --version` yok (sürüm `uv tool list`).
- coyaSONG `stdio-server.js`: stdin `initialize` isteğine yanıt vermedi. Sürüm/yardım çıktısı yok, çalıştığı doğrulanmadı. `node dist\index.js --help` da çıktısız.
- npm postinstall betikleri koşmadı (summarize: @google/genai, protobufjs; mcp-video-analyzer: ffmpeg-static, tesseract.js, tldjs). ffmpeg-static ikilisi inmemiş olabilir, gerekirse sistem ffmpeg.
- youtube-mcp-server `npm run build` Windows'ta `rm -rf` yüzünden düşer, Git `usr\bin` o oturumda PATH'e eklenerek geçti.
- yt-fts kendi venv'ine yt-dlp 2025.6.30 çekti. Repo'nun kullandığı PATH'teki 2026.08.19, venv'dekini ayrıca güncellemeden kullanma.

## 2. watch

Yalnız klon: `C:\Projeler\.tmp-video\src\claude-video` (03ceb42). Kayıtlı değil, `watch-venv` kurulmadı. Sonraki oturum başında Ömer koşar:

- `/plugin marketplace add bradautomates/claude-video`
- `/plugin install watch@claude-video`
- `/plugin disable watch@claude-video`

K4 (2134ace): `dist/yukle-video/yeni/watch.zip` üretildi. `skill_denetim` 0 hata. `duman_claudeai` 300 sn timeout, sonuç yok.

## 3. Köprü (1a848aa)

`tools/cc-kopru/kopru.json` allowlist, yalnız okuma/analiz:
- crv: pozisyonel URL, alt komut yok. Yasak: `--cookies`, `--cookies-from-browser`, `--yt-dlp-arg`, `--viewer`, `--kb`, `--overwrite`. `-o` serbest.
- summarize: `--extract` zorunlu (LLM çağrısı yok). `--slides --extract` izinli. `daemon`/config alt komutları yasak.
- mcp-video-analyzer: yalnız `analyze`, `--help`, `--version`. Argümansız çalışma MCP sunucusu başlatır, reddedilir.
- whisper-cli: mutlak yol (PATH'te değil), yalnız transkripsiyon. `-of`/`--output-file` yasak.

Desktop duman satırları:

```
komut(arac="crv", args=["https://www.youtube.com/watch?v=aZe5ZTYcF1M"], cwd="C:/Projeler")
komut(arac="summarize", args=["https://www.youtube.com/watch?v=aZe5ZTYcF1M", "--extract"], cwd="C:/Projeler")
komut(arac="mcp-video-analyzer", args=["analyze", "https://www.youtube.com/watch?v=aZe5ZTYcF1M"], cwd="C:/Projeler")
komut(arac="whisper-cli", args=["-m", "<model.bin>", "-f", "<ses.wav>", "-otxt"], cwd="C:/Projeler")
```

## 4. K0 bulguları

- yt-dlp: exe `C:\Users\pc\.local\bin\yt-dlp.exe`, 2026.08.19 (son sürüm). `python -m yt_dlp` yok (modül sistem Python'unda değil). `tools/video` komut adıyla (`yt-dlp`) çağırıyor, PATH yeterli.
- JS runtime: node 24.19.0 (`~\.config\yt-dlp\config`: `--js-runtimes node`). `--verbose --simulate aZe5ZTYcF1M`: 403 yok, ERROR yok.
- Smart App Control: `VerifiedAndReputablePolicyState = 0` (kapalı).
- Port 20128: `node ...\node_modules\omniroute\dist\server-ws.mjs` (pid 42096). `k6-prova.ps1:47` regex `'omniroute\.mjs'` bu komut satırına EŞLEŞMİYOR (dosya adı `server-ws.mjs`, "omniroute" yalnız dizinde). `-OmniKapat` süreci durdurmaz. Düzeltme VİDEO-GÖZ-1'e (ör. `'omniroute[\\/]'`), burada uygulanmadı.

## 5. S1–S6

Segment A: aZe5ZTYcF1M 4:00–6:00 (TR, 9:51). B=FaChtkkG9X4 (EN), C=d_UE-wHLoZY (Short). Soru: S6'da "videoda geçen/ekranda görünen araç, kütüphane, komutları zaman damgasıyla listele".

| aşama | kol | sonuç | token | sn | $ |
|---|---|---|---|---|---|
| S1 | 3.5 Flash-Lite fps1 minimal | 200, 13 öğe | video 10921 + metin 30, çıktı 653 | 6.1 | 0.0049 |
| S1 | 3.5 Flash-Lite fps0.5 minimal | 200, 13 öğe | video 6961 (-36%), çıktı 637 | 14.8 | 0.0037 |
| S1 | 3.7 Flash fps1 | ÇALIŞMADI: minimal 400 ("MINIMAL not supported"), low 503 | - | 5.8 | 0 |
| S1 | 3.7 Flash fps0.5 | ÇALIŞMADI: minimal 400, low 503 | - | 30.1 | 0 |
| S1 | B/C kolları (Lite ve Flash) | koşmadı (istek tavanı) | - | - | - |
| S2 | Interactions agentic, 3.7 Flash | ÇALIŞMADI: 503 kapasite | - | 1.8 | 0 |
| S2 | agentic, 3.5 Flash-Lite (2 deneme) | ÇALIŞMADI: 2×503 | - | 10.9 / 31.7 | 0 |
| S3 | OpenRouter 3.5 Flash-Lite, tam video | 200, 31 öğe (kesik, `finish_reason=length`) | prompt 53860 (video 53788), çıktı 1496 | 11.8 | 0.0199 |
| S4 | Groq whisper-large-v3-turbo, 60 sn | 200 (ilk deneme 403 UA engeli), WER 0.158 | - | 2.7 | ~0.00067 |
| S4 | faster-whisper large-v3-turbo int8 CPU | WER 0.212 (referans otomatik altyazı, göreli) | - | 42.1 | 0 |
| S5 | RapidOCR vs Tesseract, 10 kare | kırpılmış: RapidOCR 1.3–4.7 sn, Tesseract 0.8–5.1 sn; tam kare 0.8–10.4 sn. Doğruluk sayılmadı | - | - | 0 |
| S6 | crv A/B/C | 9/4/5 öğe | 115k / 51k / 57k | 938 / 1021 / 29 | 0 |
| S6 | mcp-video-analyzer A/B/C | 13/12/10 öğe | 30.5k / 36.3k / 31.0k | 470 / 317 / 54 | 0 |
| S6 | summarize --extract A/B/C | 15/9/6 öğe | 2.4k / 2.3k / 0.3k | 5 / 40 / 16 | 0 |
| S6 | summarize --slides A/B/C | A'da +6 slayt, B/C ek yok (OCR yok) | 9.6k / 9.5k / 2.1k | 74 / 25 / 8 | 0 |
| S6 | watch (yerel) A/B/C | 10/4/6 öğe | 15.6k / 27.3k / 6.8k | 101 / 51 / 8 | 0 |
| S6 | taban (mevcut hat) A | 4 öğe | 7.2k (ölçülen girdi 17.9k) | 14.7 | 0.0101 |

Gözlemler:
- S1: iki koşuda çıktı öğeleri yalnız model adları. Vite/Three.js/GSAP/Lenis ekran metni listelenmedi. Doğruluk Desktop'ta sayılacak.
- S6 süreleri 4 kol + S5 aynı anda koşarken alındı, göreli sıralama için, mutlak değil.
- crv B/C: faster-whisper `open() got an unexpected keyword argument 'metadata_errors'` (döküm yok). watch B: otomatik altyazı dili yanlış (`ar`, video EN), `--sub-lang en` verilmeli.
- Kapsam: summarize+slayt (15) ve mva (13) en geniş. summarize --extract ucuz/hızlı ama ekrandaki komutları kaçırır. mva B/C'de de çalıştı, OCR gürültülü (B'de 48 982 karakter).
- İstek sayıları: Gemini 10/10 · Groq 2/4 (S6'da 0) · OpenRouter 2/2 (S6'da 0).

Agentic + YouTube + ücretsiz katman, net cevap: bugün ÖLÇÜLEMEDİ. 3 denemenin üçü 503 kapasite. 400/403/429 yok, yani yetki/şema hatası değil, uç nokta ve model isteği kabul ediyor. Doküman YouTube URL'yi ve ücretsiz katmanı agentic için açıkça listelemiyor (yalnız Files API örneği). Anahtarın faturalı olup olmadığı hata metninden çıkmadı. Karar VİDEO-GÖZ-1'de tek tekrar denemeyle.

Desktop doğruluk sayımı için kare ve çıktılar: `C:\Projeler\.tmp-video\olcum\s5\k<sn>\{kirp.png,tam.png,rapidocr_*.txt,tesseract_*.txt}` + `sonuc.json`. S6 listeleri: `olcum\s6\liste\`.

## 6. SkillSpector (`skillspector scan <klon> --no-llm --format json`)

6/6 klon skor 85–100 CRITICAL/DO_NOT_INSTALL. Bu "skill kurulumu" eşiği, biz yalnız CLI/klon kullanıyoruz (watch'ın plugin kurulumu Ömer'de). Çoğu bulgu test/demo/CI, vendored (ffmpeg wasm, localization json), YARA kalıbı, bytecode gürültüsü. Gerçek kod bulguları ve önlem:

| klon | skor / toplam | gerçek kod bulguları (dosya:satır) | önlem |
|---|---|---|---|
| claude-real-video | 100 / 51 | `install-skill.sh:53`, `src/claude_real_video/cli.py:72`, `core.py:2`, `core.py:84` (credential access), `core.py:1753` | kullanmadan önce satırları oku; anahtar verilmez; köprüde cookie ve yt-dlp ham argümanı yasak |
| summarize | 100 / 357 | `src/cli-main.ts:81,158`, `src/config/env.ts:34`, `src/llm/cli-exec.ts:163`, `src/run/cookies/twitter.ts:303`, `src/run/bird/exec.ts:21`, `src/daemon/launchd.ts:135,154` | yalnız `--extract`, daemon yasak, `envGecir` yok, anahtar verilmez |
| mcp-video-analyzer | 100 / 98 | `package-lock.json:1615` @modelcontextprotocol/sdk 1.27.1 CVE; `src/server.ts:31`, `src/utils/ytdlp.ts:30`, `src/utils/ssrf-guard.ts:26,197` | MCP modu kullanılmaz, yalnız CLI `analyze`; MCP olarak kaydetme |
| claude-video | 100 / 85 | `skills/watch/scripts/config.py:12,103,116`, `gemini.py:133`, `local_whisperx.py:66` | `--no-whisper`/yerel motor, anahtar verilmez (config `~/.config/watch/.env` okur) |
| youtube-research-mcp | 85 / 10 | `src/yt_research_mcp/server.py:95` | kayıtsız, çalıştırılmadı |
| youtube-mcp-server | 100 / 40 | `package-lock.json:2539` proxy-addr CVE (CRITICAL); `:1224` brace-expansion, `:1708` fast-uri, `:2146` ip-address, `:2415` node-forge, `:461` @modelcontextprotocol/sdk 1.29.0 | MCP olarak kaydetme, stdio+yerel, `npm audit`; çalıştığı doğrulanmadı |

claude-real-video'daki tek CRITICAL (`marketing/demo-20260719/bgm/Metaphysik.mp3:7113`, php_webshell YARA) demo ses dosyasında, çalıştırılmaz.

## 7. Ölçümler

**gitleaks** (git geçmişi): `gitleaks detect --source C:\Projeler\omer-skills --no-banner --redact` → 829 commit tarandı, `no leaks found`, leaks: 0. Ham ölçüm klasörü: `olcum` altında 123 dosya + S6 1004 dosya, sızıntı 0/3 ve 0/1004 (K5 taramaları).

**token_olc** (`python tools/token_olc.py olc --gun 4`, oturum başına "taban" = ilk istem ağırlıklı token; omer-skills ana oturumları, bölme noktası 962a9f3 commit zamanı 2026-10-07 13:04:55Z; 2026-10-06 sonrası):

| | oturum | ilk istem ortalama | medyan |
|---|---|---|---|
| önce | 54 | 103 276 | 103 552 |
| sonra | 1 | 106 258 | 106 258 |
| fark | | +2 982 (+2.9%) | +2 706 |

Yorum: bu dalgada CC ilk istemine giren hiçbir şey değişmedi (MCP/plugin kaydı yok, skill CC'ye kurulmadı), `claude mcp list` yeni sunucu göstermiyor. Fark n=1 örnekle gürültü düzeyinde (önceki 54 oturumun aralığı 97 749–105 545), anlamlı değişiklik sayılmaz.
