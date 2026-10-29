# TUR 7: gitleaks-20 — her bulgu tek tek: dosya:satir, kural, sinif, gerekce. Anahtar degeri yazilmaz (ilk 4 + uzunluk).
import json, re, csv, sys
from pathlib import Path
KOK = Path(r"C:\Projeler\araclar\video-izle-kur-1")
CIKTI = Path(__file__).with_name("gitleaks20.tsv")
TEST = re.compile(r"(^|[/\\])(tests?|__tests__|spec|specs|fixtures?|mocks?|testdata|e2e|__snapshots__|cassettes?|benchmarks?|goldens?|comparisons|upgrade_tests)([/\\]|$)|[._-](test|spec)\.[a-z]+$|_test\.go$|test_[^/\\]*\.py$", re.I)
DOC = re.compile(r"(^|[/\\])(docs?|examples?|samples?|website|blog|guides?|tutorials?)([/\\]|$)|\.(md|mdx|rst|txt|ipynb|html)$|\.env\.(example|sample|template)$|example", re.I)
LOCK = re.compile(r"(package-lock\.json|yarn\.lock|pnpm-lock\.yaml|uv\.lock|poetry\.lock|Cargo\.lock|go\.sum|\.svg$|\.min\.js$|\.map$)", re.I)
YER = re.compile(r"(x{4,}|your[_-]?|<[^>]+>|\.\.\.|placeholder|dummy|fake|example|sample|changeme|replace|test|demo|mock|1234|abcd|redacted|\*{3,}|\$\{|\{\{|process\.env|os\.environ|getenv)", re.I)

def sinifla(f):
    yol = f.get("File", ""); s = f.get("Secret", "") or ""; m = f.get("Match", "") or ""; kural = f.get("RuleID", "")
    if LOCK.search(yol): return "yanlis-alarm", "kilit/ozet/derlenmis dosya (hash/integrity)"
    if YER.search(s): return "ornek-yer-tutucu", "deger yer tutucu kalibinda"
    if TEST.search(yol): return "test-verisi", "test/fixture dizini"
    if DOC.search(yol): return "ornek-yer-tutucu", "dokuman/ornek dosyasi"
    if kural == "generic-api-key" and (f.get("Entropy", 5) < 3.5 or re.fullmatch(r"[a-z_]+", s)): return "yanlis-alarm", "dusuk entropi/tanimlayici"
    return "emin-degil", "elle bakilacak"

rows = []
for d in sorted(KOK.iterdir()):
    j = d / "src.gitleaks.json"
    if not j.exists(): continue
    for f in json.loads(j.read_text(encoding="utf-8") or "[]"):
        sinif, ger = sinifla(f)
        yol = f.get("File", "").replace("\\", "/").split(f"/{d.name}/src/", 1)[-1]
        s = f.get("Secret", "") or ""
        rows.append([d.name, f"{yol}:{f.get('StartLine')}", f.get("RuleID"), f"{s[:4]}…/{len(s)}", sinif, ger])
with CIKTI.open("w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t"); w.writerow(["arac", "dosya:satir", "kural", "deger", "sinif", "gerekce"]); w.writerows(rows)
from collections import Counter
print(len(rows)); print(Counter((r[0], r[4]) for r in rows if r[4] == "emin-degil"))
print(Counter(r[4] for r in rows))

# --- elle bakilan 60 satir (TUR 7, maskeli baglamla okundu) ---
ELLE = [
 ("Cloudroom", "github-login.ts", "yanlis-alarm", "GitHub OAuth client ID (Ov23..) herkese acik tanimlayici, sir degil"),
 ("Cloudroom", "env-vars.ts", "yanlis-alarm", "PostHog phc_ proje anahtari: istemci tarafi icin herkese acik tasarim"),
 ("Fallow", "fuzz-smoke.yml", "yanlis-alarm", "actions/cache 'key:' onbellek anahtari dizgesi"),
 ("Fallow", "hardcoded_secret.rs", "test-verisi", "Fallow'un sir-tespit kuralinin test ornekleri"),
 ("Fallow", "visitor/tests.rs", "test-verisi", "ayristirici testindeki uydurma degerler"),
 ("Fallow", "signing-migration.json", "yanlis-alarm", "GitHub ortam PUBLIC key'i (key_id+key, sealed-box acik anahtar); workflow 'unchanged public key' diyor"),
 ("Hindsight", "config.py", "yanlis-alarm", "xAI OAuth client ID: herkese acik tanimlayici"),
 ("Hindsight", "config.rs", "test-verisi", "#[test] fn icinde ayristirma testi degeri"),
 ("Hypit", "oauth.ts", "yanlis-alarm", "OAuth client ID (hyc_): herkese acik tanimlayici"),
 ("iFix_AI", "telemetry.py", "yanlis-alarm", "PostHog phc_ proje anahtari: herkese acik (telemetri; kurulumda kapatilabilir)"),
 ("Jcode", "_tests.rs", "test-verisi", "*_tests.rs test degeri"),
 ("Jcode", "tests.rs", "test-verisi", "test modulu JWT ornegi"),
 ("Jcode", "jcode-fuzzy", "yanlis-alarm", "bulanik arama test dizgesi ('claude...' model adi)"),
 ("Magpie", "google.go", "yanlis-alarm", "Gemini CLI / Antigravity'nin kurulu-uygulama OAuth istemcisi; kodda yorum: 'secret is no secret: it ships in CLI' — Google installed-app akisi, sir sayilmaz, Magpie'nin kendi sirri degil"),
 ("Magpie", "fieldvalue.go", "yanlis-alarm", "redakte kurali deseni (env.X degisken adi)"),
 ("Magpie", "model.go", "yanlis-alarm", "model adi dizgesi (llama...)"),
 ("Magpie", "stats.go", "yanlis-alarm", "PostHog phc_ proje anahtari: herkese acik"),
 ("Magpie", "worker.js:185", "yanlis-alarm", "PostHog phc_ proje anahtari: herkese acik"),
 ("Magpie", "worker.js:315", "yanlis-alarm", "Cloudflare Web Analytics beacon token: HTML'e gomulu herkese acik"),
 ("Orca", ".patch", "yanlis-alarm", "xterm kucultulmus kodu yamasi (degisken atamasi)"),
 ("Orca", "google-services.json", "yanlis-alarm", "Firebase mobil API anahtari (AIza): uygulamaya gomulu herkese acik tasarim"),
 ("Orca", "pilot-scenarios.json", "test-verisi", "RPC senaryo fixture'i (token hash)"),
 ("Orca", "e2ee-primitives.ts", "yanlis-alarm", "fonksiyon adi eslesmesi (deriveV2KeySchedule)"),
 ("Orca", "https-test-certificate.ts", "test-verisi", "yerel HTTPS test sertifikasi anahtari (dosya adi test)"),
 ("Orca", "browser-extension-crx.ts", "yanlis-alarm", "Chrome Web Store yayinci anahtar OZETI (hash), sir degil"),
 ("Orca", "test-constants.ts", "test-verisi", "test sabiti (e30. = '{}' bos JWT basligi)"),
 ("Orca", "test-cell.ts", "yanlis-alarm", "RFC 6455 ornek Sec-WebSocket-Key (dGhl.. 'the sample nonce')"),
 ("Orca", "appimage-cache-identity.ts", "yanlis-alarm", "surum dizgesi (NAMESPACE_KEY_VERSION)"),
 ("Orca", "-fixtures.ts", "test-verisi", "E2EE test vektoru fixture'i"),
 ("prompts.chat", "prompts.csv", "ornek-yer-tutucu", "istem metnindeki ornek ('demo secret dev-secret' JWT / 'LinkedIn: Recommendation' basligi)"),
 ("ReelMimic", "telemetry.mjs", "yanlis-alarm", "PostHog phc_ proje anahtari: herkese acik"),
 ("Reicon", "ping.mjs", "yanlis-alarm", "IndexNow anahtari: tasarim geregi sitede /<key>.txt olarak yayimlanir"),
 ("tcl-lsp", "lib.rs", "ornek-yer-tutucu", "doc-test ornegi (//! satiri, sonucu 'KEY45678')"),
]
for r in rows:
    if r[4] != "emin-degil": continue
    for a, parca, s, g in ELLE:
        if r[0] == a and parca in r[1]: r[4], r[5] = s, g; break
with CIKTI.open("w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t"); w.writerow(["arac", "dosya:satir", "kural", "deger", "sinif", "gerekce"]); w.writerows(rows)
print("elle sonrasi", Counter(r[4] for r in rows))
