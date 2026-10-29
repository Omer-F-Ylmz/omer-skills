---
type: rapor
status: tamam
tags: [guvenlik, video-izle-kur-1]
relatedTo: [video-izle-kur-1]
---

# Güvenlik 4 — repo ve skill tarama bulguları

Yöntem: SkillSpector (.ss), semgrep (.sg), gitleaks (.gl) çıktıları python -I ile ayrıştırıldı; her grubun 2-3 örneği klondaki gerçek satıra bakılarak doğrulandı. Klonlardan hiçbir şey çalıştırılmadı, kod değiştirilmedi. Sayılar JSON'dan alındı; sonuc.tsv'deki sayılardan farklı olabilir (onlar başka bir sayım). Gitleaks çıktısında sır değerleri zaten "REDACTED"; raporda hiçbir sır değeri yok.

Genel not: SkillSpector bu repolara hep "DO_NOT_INSTALL / skor 100" veriyor çünkü kural metin eşleştirmesi yapıyor (".env", "rm -rf", "Keychain" kelimesi geçince HIGH). Doğruladığım örneklerde gerçek kötü niyet bulgusu çıkmadı; gerçek riskler aşağıda ayrı belirtildi.

---

## A1. PentAGI (vxcontrol/pentagi)

Tarama: pentagi.ss/sg/gl hepsi mevcut. SkillSpector 407 bulgu (CRITICAL 4, HIGH 165, MEDIUM 230, LOW 8). Semgrep 148 (ERROR 8, WARNING 140). Gitleaks 11.

### SkillSpector HIGH/CRITICAL grupları

| Kural | Sayı |
|---|---|
| Credential Access (".env" geçmesi) | 108 |
| YARA offensive_tool_references | 16 |
| Docker Socket Access | 13 |
| Self-Modification ("self-update") | 8 |
| Memory Manipulation ("reset state") | 4 |
| YARA c2_framework (CRITICAL) | 3 |
| YARA exploit_framework | 3 |
| Hidden Instructions (HTML yorumu) | 2 |
| Tool Parameter Abuse | 2 |
| YARA info_stealer | 2 |
| YARA php_webshell_known (CRITICAL) | 1 |
| Diğer tek bulgular (webshell, concealed artifact, anti-refusal, context leakage, tool-poisoning) | 8 |

Örnekler ve doğrulama:
- Credential Access: `.dockerignore:12`, `.gitignore:2`, `.env.example:412` — dosyada yalnız ".env" adı geçiyor (yok-say listesi / örnek ayar dosyası). Yanlış alarm.
- offensive_tool_references / exploit_framework / c2 / webshell / info_stealer (`backend/pkg/templates/prompts/pentester.tmpl:116,119,179,305,309`, `testdata/sploitus_result_*.json`): pentester ajanının istem şablonunda araç adları listesi (nmap, metasploit, mimikatz, weevely...) ve test verisi. Ürün zaten bir sızma testi aracı; kendisi saldırı kodu içermiyor. Yanlış alarm (ürünün amacı). Ama araç gerçek saldırı araçlarını konteynerde çalıştırır: kullanım tarafı risk.
- Docker Socket: `.env.example:347`, `README.md:625`, `docker-compose.yml:230` — pentagi servisi ana makinenin `/var/run/docker.sock` dosyasını varsayılan olarak bağlıyor ve `user: root` ile çalışıyor (compose:230,235). Gerçek risk, CVE-2026-14784 (Docker API sandbox kaçışı, ≤2.1.0) tam bu yüzeyle ilgili. `.env.example:338-345` kendi uyarısını veriyor: DOCKER_INSIDE=true (soketi sandbox içine verir) varsayılan false; bunu açma. CVE'nin kendisini bu oturumda doğrulamadım (sürüm numarası ve ayrıntı doğrulanamadı: kaynağa erişim yok), sadece kodda soket bağlantısının var olduğunu doğruladım.
- Self-Modification: `backend/cmd/installer/checker/updates.go:106` — kurucunun güncelleme indirme akışının yorumu ve alan adları. Ürünün kendi kurucu güncellemesi; yanlış alarm, ama kurucu buluttan dosya indirir (indirilen dosyanın hash'i kontrol ediliyor gibi: `TargetDigest` alanı var, akışı baştan sona doğrulamadım).
- Hidden Instructions: `.github/PULL_REQUEST_TEMPLATE.md:1,64` — normal HTML yorumu. Yanlış alarm.
- Tool Parameter Abuse: `Dockerfile:150` (`chmod +x entrypoint.sh`), `locale.go:95` (yardım metni `chmod 644 .env`). Yanlış alarm.
- "bypass security": `assistant.tmpl:110` — sızma testi asistanının kullanım senaryosu metni. Yanlış alarm.

### Semgrep ERROR (8)
- gosql-sqli ×2 (`backend/pkg/database/renumbered_migrations.go:44,51`): tablo adı `pq.QuoteIdentifier` ile kaçışlanıyor, değer `$1` parametre. Yanlış alarm.
- dangerous-exec-command ×2 (`checker/helpers.go:186`, `utils_darwin.go:47`): `helpers.go:186` sabit `docker compose version` çalıştırıyor. Yanlış alarm (darwin dosyasını açmadım, doğrulanamadı).
- detect-child-process (`frontend/scripts/generate-ssl.ts:25`): `execSync` ile komut; geliştirme betiği, SSL sertifikası üretiyor. Düşük risk.
- detect-insecure-websocket (`services/graphql.go:201`): origin doğrulayıcıdaki "ws://" önek listesi, bağlantı açmıyor. Yanlış alarm.
- detected-bcrypt-hash (`migrations/sql/20241026_..._initial_state.sql:89`): varsayılan yönetici hesabının hash'i. Gerçek not: README:868 varsayılan giriş `admin@pentagi.com` / `admin`, ilk girişte değiştirilmeli.
- use-of-basic-authentication (`backend/fern/langfuse/openapi.yml:10742`): API şeması dosyası. Yanlış alarm.

### Gitleaks (11) — hepsi yer tutucu/örnek, gerçek sır yok
- `README.md:1169,1175,1276` curl-auth-header: `YOUR_API_TOKEN` yer tutucusu.
- `hardening_test.go:311`: test içinde sahte langfuse anahtarları ("pk-l…", "sk-l…", 1234-4321 desenli).
- `config_test.go:55,74`: test yapısında "sk-p…", "sk-a…", "GOCS…" sahte değerler (1234567890abcdef desenli).
- `routing_test.go:169`: örnek JWT (`eyJh…`, `.e30.sig` boş yük).
- `middleware_test.go:227`: WebSocket el sıkışması için RFC örnek anahtarı.
- `fixtures_test.go:13`: örnek JWT (`eyJh…`, jwt.io örneği).
- `tools_test.go:523`: test lisans anahtarı "PLUM-…" (uydurma).
- `account-password.spec.ts:92`: parola kuralı testi için örnek metin.

### Karar önerisi — PentAGI
Kur ama izole: bulguların hiçbiri kötü niyet göstermiyor; gerçek risk soket bağlama + sızma aracı olması.
Önlemler: (1) `PENTAGI_LISTEN_IP=127.0.0.1` açıkça yaz (compose varsayılanı zaten `127.0.0.1:8443`, satır 33; 5432/9187/9443 de 127.0.0.1); dış arayüze açma. (2) `DOCKER_INSIDE=false` kalsın; `DOCKER_NET_ADMIN` .env.example'da true, compose varsayılanı false — false yap. (3) Docker soketi için docker-socket-proxy düşün (.env.example:343 de öneriyor). (4) ≤2.1.0 sürümünü kurma; düzeltilmiş sürüm var mı kontrol et (doğrulanamadı, CVE sayfasına bakılmadı). (5) admin parolasını ilk girişte değiştir. (6) Ayrı makine/VM'de çalıştır, hedef olarak yalnız yetkin olduğun sistemleri ver.

---

## A2. Xtool (xtool-org/xtool)

Tarama: ss/sg/gl mevcut. SkillSpector 185 bulgu (HIGH 56, MEDIUM 125, LOW 4). Semgrep 14 (ERROR 2). Gitleaks 0 bulgu (`[]`).

### HIGH grupları
| Kural | Sayı |
|---|---|
| Tool Parameter Abuse (rm -rf) | 29 |
| Credential Access (.netrc/Keychain) | 19 |
| Hidden Instructions | 2 |
| Diğer (Subprocess.run vb.) | 6 |

Örnekler:
- `Dockerfile:112` `rm -rf /xtool` — AppImage çıkarıldıktan sonra kendi geçici klasörünü siliyor. Yanlış alarm.
- `Examples/test.sh:58` `rm -rf "$out_dir/$demo.app"` — örnek derleme çıktısını siliyor. Yanlış alarm.
- `Sources/XToolSupport/NewCommand.swift:119` `.netrc` — yeni proje için üretilen .gitignore içeriği (yok-say listesi). Yanlış alarm.
- `EntitlementWithTeamOrBundleID.swift:27` "Keychain" — iOS entitlement adı. Yanlış alarm.
- `Sources/PackLib/Packer.swift:80` `Subprocess.run` — swift build'i çalıştırıyor. Beklenen davranış.
- `SDKBuilder.swift:675` "self-update" — yorum satırı. Yanlış alarm.
- `.github/ISSUE_TEMPLATE/bug_report.md:21` — HTML yorumu. Yanlış alarm.

Semgrep ERROR ×2: `.github/workflows/release.yml:26,85` run-shell-injection — `${{ github.ref_name }}` doğrudan run içinde (satır 28). Gerçek ama yalnız projenin kendi CI'ında, tag adına bağlı; senin kuruluma etkisi yok.

Not: xtool Apple kimliğiyle imzalama yapan bir araç; Apple hesabı/anahtarı nasıl sakladığını (Keychain/dosya) bu taramada ayrıca doğrulamadım.

Karar: yanlış alarm → kur. Önlem: yalnız GitHub release/kaynak derlemesinden; Apple ID için uygulamaya özel parola kullan.

---

## A3. TradingAgents (TauricResearch/TradingAgents)

Tarama: ss/sg/gl mevcut. SkillSpector 136 (CRITICAL 1, HIGH 43, MEDIUM 70, LOW 22). Semgrep 12 (ERROR 2). Gitleaks 2.

### HIGH/CRITICAL grupları
| Kural | Sayı |
|---|---|
| Credential Access (.env) | 30 |
| Prompt Extraction ("return prompt") | 5 |
| Anti-Refusal ("no warnings") | 3 |
| Env Variable Harvesting | 2 |
| Tainted flow environ → requests.post (CRITICAL) | 1 |
| Remote bootstrap (pip install https://) | 1 |
| Hidden Instructions | 1 |
| Self-Modification | 1 |

Örnekler:
- CRITICAL `tradingagents/agents/post_screen.py:87` (`requests.post`, gövde satır 75-80): sosyal medya gönderilerini `https://api.typesafe.ai` (satır 27) adresine, Jev ile süzmek için gönderiyor; `Authorization` olarak kullanıcının kendi `TYPESAFE_API_KEY` değerini kullanıyor. Anahtar sızdırma değil; ama yalnız bu anahtar tanımlıysa çalışıyor (dosya başı açıklaması) ve veri üçüncü tarafa gidiyor. Yanlış alarm, opt-in dış servis çağrısı. Anahtarı tanımlama.
- `README.md:200`, `.gitignore:151`, `docker-compose.yml:5` ".env" — ayar/yok-say dosyası. Yanlış alarm.
- `tradingagents/agents/schemas.py:12`, `cli/selections.py:164` — "output instructions"/"return prompt" sıradan kod. Yanlış alarm.
- `.github/workflows/release-assets.yml:5` `pip install https://...` — yorum satırı (kurulum talimatı). Yanlış alarm.
- `graph/checkpointer.py:86` "Remove check" — kontrol noktası satırlarını siliyor; semgrep ERROR `:94` (sqlalchemy raw query): tablo adı sabit ("writes","checkpoints") döngüsünden geliyor, değer parametre. Yanlış alarm.
- Semgrep ikinci ERROR `report_html.py:11` python37-compatibility: uyumluluk uyarısı. Önemsiz.

Gitleaks (2) — ikisi de test örneği: `tests/test_fred.py:261` (`abcdef0123…` sahte anahtar, 32 karakter desenli) ve `tests/test_alpha_vantage_hardening.py:165` ("AVKE…" sahte). Gerçek sır yok.

Karar: yanlış alarm → kur. Önlem: kendi API anahtarlarını `.env`de tut, TYPESAFE_API_KEY tanımlama (gönderi verisi dışarı gitmesin), ticaret emri gerçek hesaba bağlama.

---

## A4. FreeToken (FlashML-org/FreeToken)

Tarama: ss/sg/gl mevcut. SkillSpector 237 (HIGH 44, MEDIUM 116, LOW 77). Semgrep 23 (ERROR 4). Gitleaks 1.

### HIGH grupları
| Kural | Sayı |
|---|---|
| Env Variable Harvesting (os.environ.copy) | 12 |
| Prompt Extraction ("return prompt") | 12 |
| External Script Fetching (curl\|sh) | 6 |
| Privileged Container | 3 |
| Chaining Abuse | 3 |
| Memory Manipulation ("reset state") | 2 |
| YARA tool-poisoning | 2 |
| Diğer (Credential Access, Data Flow ×2, Output Handling) | 4 |

Örnekler:
- `install.sh:11` `curl ... install.sh | bash` — yorumdaki kullanım örneği; asıl wheel adresleri boş (`DEFAULT_WHEEL_URL=""`, satır 36-37).
- `install.sh:155` `curl -LsSf https://astral.sh/uv/install.sh | sh` — uv yoksa ve kullanıcı onaylarsa (`--yes` ya da y) uv'yi bu yöntemle kuruyor (satır 147-155). Gerçek ama bilinen, onaylı; uv'yi önceden kurarsan hiç çalışmaz.
- `python/freetoken/launch.py:96-120` — Codex/Claude/OpenCode/OpenClaw/Hermes için `curl | sh/bash` komutları; yalnız kullanıcı onayladığında (`_confirm_install`, satır ~1013) çalışıyor. Gerçek ama onaylı; ben bu ajanları zaten kurduğum için kullanılmayacak.
- `launch.py:1020,1039` `os.environ.copy()` — alt süreç için ortam kopyalayıp küçük değişiklik yapıyor, dışarı göndermiyor. Yanlış alarm.
- `docs/install_amd.md:23-25` `--device=/dev/kfd --ipc=host --cap-add=SYS_PTRACE` — AMD ROCm Docker örneği. Dokümandaki yetki; yalnız AMD GPU için, bizde geçerli değil.
- "return prompt" ×12 — tokenizer/API kodu. Yanlış alarm.

Semgrep ERROR ×4: python37-compatibility (`checkpoint/ftw.py:81`, `models/weight.py:54`, `moe/host_banks.py:493` ...) — Python 3.7 uyumluluk uyarısı, güvenlik değil. Yanlış alarm.

Gitleaks (1): `tests/tokenizer/test_tokenize.py:12` — sınıf adı içeren import satırı (entropi 3.5), sır değil. Yanlış alarm.

Karar: yanlış alarm, ama kurulum yolunu değiştir → kur. Önlem: `install.sh`'i ve `curl | sh` yollarını kullanma; uv'yi önceden kur, sonra doğrudan `uv pip install` ile paketi kur. (install.sh wheel adresi boş, yani resmi release henüz bağlanmamış: kurulumu kaynaktan yapmak gerekir; bunun işleyip işlemediği denenmedi.)

---

## B. BEKLE'deki skill repoları

Tarama: video-izle-kur-1-skill/*.ss.json ve .gl.json (gitleaks hepsinde `[]`, answer-me-with-html hariç: o 1.3K, 2 kayıt).

### B1. SlopMonster (ItsssssJack/SlopMonster)
SkillSpector 10 bulgu (HIGH 4, MEDIUM 6), skor 72. Not: önceki inceleme "5 HIGH" demişti, JSON'da 4 HIGH var; hepsi aynı kural.
- 4 HIGH = analysis-evasion, `SKILL.md:72,73,86,110`: `DESLOP_WRITER=claude tools/cleanse.sh ...` komut örnekleri ve `tools/test_cleanse.sh` adı. Doğrulandı: yanlış alarm.
- `tools/cleanse.sh` (satır 12-13,101,120) taslağı, yüklü rakip modelin CLI'sına (codex exec / claude) veriyor; yani taslak metnin ikinci modele gitmesi tasarım gereği. tools içinde curl/wget/sudo/rm -rf bulunmadı (grep sonuçları yalnız yorum/eval `test_cleanse.sh:13`, yerel script parçası).
- Karar: yanlış alarm → kur. Not: taslak metin başka bir model sağlayıcısına gider (gizli içerik için kullanma).

### B2. answer-me-with-html (QingYunA)
SkillSpector 162 (HIGH 42), skor 100. Gruplar: Credential Access 19, Anti-Refusal 8, Hidden Instructions 5, Tool Parameter Abuse 4, Chaining 2, Self-Modification 2, Prompt Extraction 1, Instruction Override 1.
- `src/code.js:26` `.npmrc/.netrc` — gizli dosya adlarını ENGELLEYEN kural listesi (SECRET_FILE regex). Savunma amaçlı. Yanlış alarm. (`am.mjs:9268` aynı kodun paketlenmiş hali.)
- `SKILL.md:91` "no warnings" — komut çıktısını açıklayan metin. Yanlış alarm.
- `test/housekeeping.test.js:291` `am;rm -rf ~/...` ve `test/theme-market.test.js:21` "ignore previous instructions" — saldırı girdisinin temizlendiğini sınayan test dizeleri. Yanlış alarm.
- `.github/workflows/ci.yml:92` `sudo apt-get install ffmpeg` ve `theme-submission.yml:121` `git push --force` (yalnız tema branch'i) — projenin kendi CI'ı. Yanlış alarm.
- `SKILL.md:28` + `references/settings.md:19` "update this skill" — kullanıcı isteyince `npx skills update ...`/`git pull` çalıştırma talimatı. Gerçek ama kullanıcı isteğine bağlı.
- Gerçek davranışlar (HIGH değil ama bilinmeli): `am theme add` answer-me-with-html.com'dan tema indirir (settings.md:15); `src/video/tts.js` yalnız kullanıcının `AM_TTS_URL` adresine istek atar; `cli.js:1090` tarayıcı açar (`spawn detached`) — Ömer'in ekran kuralına aykırı olabilir (varsayılan tarayıcıyı açar; `--no-open` veya `am config` ile kapat).
- Karar: yanlış alarm → kur. Önlem: `am config` ile otomatik tarayıcı açmayı kapat; `am theme add` / TTS kullanma.

### B3. i-have-adhd (ayghri)
SkillSpector 435 (HIGH 150), skor 100. Gruplar: Hidden Instructions 110, Tool Parameter Abuse 32, Env Harvesting 5, Concealed Executable 1, Output Handling 1, Prompt Extraction 1.
- Hidden Instructions: `.github/pull_request_template.md:3,23` HTML yorumu; `.github/install/INSTALL.fa.md:18,31,...` sıfır genişlikli ayırıcı (ZWNJ, Farsça yazımda normal). Yanlış alarm.
- `INSTALL.*.md` `rm ~/.gemini/commands/i-have-adhd.toml` — kaldırma talimatı (örnek: INSTALL.ja.md:218). Yanlış alarm.
- `scripts/check_pi_extension.py:159` — API anahtarlarını SİLEREK izole ortam kuruyor (satır 160-161). Tersine koruma. Yanlış alarm.
- `.opencode/plugins/i-have-adhd.js:1` — tek satır `export default` yönlendirmesi. Yanlış alarm.
- `extensions/i-have-adhd.ts:78` "return rules" — SKILL.md metnini döndürüyor. Yanlış alarm.
- `hooks/always-on.sh` okundu: yalnız kullanıcı `~/.claude/.i-have-adhd-always` dosyasını oluşturursa SKILL.md'yi bağlama ekliyor; ağ/exec yok. Çalışma dizinlerinde (hooks, extensions, skills, .opencode) curl/exec/ağ araması boş döndü.
- Karar: yanlış alarm → kur.

### B4. re-walkthrough-pro (charlesdove977)
SkillSpector 15 (HIGH 1), skor 45. Tek HIGH: `.gitignore:5` `.env` — yok-say satırı. Yanlış alarm → kur.

### B5. brag (latent-spaces)
SkillSpector 38 (HIGH 8), skor 100. Gruplar: Agent Config Dir Access 3, Hidden Instructions 2, External Script Fetching 2, Bilinen zafiyetli bağımlılık 1.
- `README.md:89`, `docs/other-agents.md:29,30` `~/.gemini/config` — hangi ajanın skill'i nereden bulduğunu anlatan dokümantasyon. Yanlış alarm.
- `skills/brag-slim/SKILL.md:97` "curl | sh" — metin tam tersini söylüyor: "`curl | sh` yerine paket yöneticisini tercih et". Yanlış alarm.
- `examples/taxi-for-taxis/index.html:47` — HTML yorumu ("the recursion..."). Yanlış alarm.
- `skills/brag/scripts/uv.lock:359` msgpack==1.2.1, CVE-2026-114613 (bellek sızıntısı): kilit dosyasında gerçek bir bağımlılık sürümü. CVE ayrıntısını doğrulayamadım (kaynağa bakılmadı); etkisi: msgpack'i brag betiğinin kullanıp kullanmadığını da doğrulamadım (scripts içinde doğrudan geçmiyor, geçişli bağımlılık). Düşük risk (yerel video üretimi).
- Karar: yanlış alarm → kur. Not: betikleri çalıştırırsan uv.lock'taki msgpack sürümü eski olabilir.

### B6. claude-commercial-ops-skills (opaiiva)
SkillSpector 6 (HIGH 2), skor 48.
- `skills/closer-prep/CLAUDE.md:20` "Always respond in the team's working language" — dil kuralı. Yanlış alarm.
- `skills/fechamento-github/SKILL.md:38` `git push --force` — metin "Never `git push --force`" diyor (yasaklama). Yanlış alarm. Aynı skill, onay almadan yayın yapmaz (satır 33-34, 43).
- Karar: yanlış alarm → kur. Not: fechamento-github `gh` CLI ile depoya yazar; ayrıca Portekizce/CRM işine özgü, Ömer için işlevsiz olabilir (güvenlik dışı).

### B7. Pynkaro (ralbuque)
SkillSpector 27 (HIGH 14), skor 93. Gruplar: Credential Access 12 (hepsi "Keychain"), YARA info_stealer 1, External Script Fetching 1.
- `Sources/Pynkaro/Config.swift:7,38,43,52,84,85` — macOS uygulaması API anahtarlarını Keychain'e kaydediyor/okuyor (sıra: Keychain > config.json > ortam değişkeni). Gerçek ama normal kullanım. Anahtarlar yalnız `api.anthropic.com` ve `api.elevenlabs.io` adreslerine gidiyor (Sources içindeki URL listesi).
- YARA info_stealer: `.build/arm64-apple-macosx/debug/ModuleCache/.../Foundation-...pcm:23083` — derlenmiş Apple modül önbelleği (ikili), "Cookies" kelimesi geçiyor. Yanlış alarm. Ama `.build/` klasörü depoda git ile takipli; derlenmiş ikili dosyaların kaynağı doğrulanamaz.
- `README.md:99` ElevenLabs sesleri listeleyen curl — dokümantasyon. Yanlış alarm.
- Bu bir Claude skill'i değil: SKILL.md yok (skill-kur.tsv: "SKILL.md yok"), macOS/Swift uygulaması.
- Karar: skill olarak kurulacak bir şey yok; yanlış alarm. Kurma (skill değil, macOS'a özgü).

---

## Karar özeti
- PentAGI: önlemle kur (127.0.0.1 bağlama, DOCKER_INSIDE=false, soket proxy, admin parolası, ≤2.1.0 kurma).
- Xtool: yanlış alarm → kur.
- TradingAgents: yanlış alarm → kur (TYPESAFE_API_KEY tanımlama).
- FreeToken: önlemle kur (install.sh / curl|sh yerine uv'yi önceden kurup doğrudan `uv pip install`).
- SlopMonster: yanlış alarm → kur (5 değil 4 HIGH, hepsi aynı).
- answer-me-with-html: yanlış alarm → kur (otomatik tarayıcı açmayı kapat).
- i-have-adhd: yanlış alarm → kur.
- re-walkthrough-pro: yanlış alarm → kur.
- brag: yanlış alarm → kur (uv.lock msgpack notu).
- claude-commercial-ops-skills: yanlış alarm → kur.
- Pynkaro: skill değil (SKILL.md yok), kurma.
