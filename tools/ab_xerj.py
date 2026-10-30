"""FILE A/B (LINK-30EKI-17 madde 3): xerj search ↔ graphify query ↔ rg. Korpus: docs/*.md + docs/departmanlar (geçici kopya).
Ölçü: hedef dosya ilk 5 sonuçta mı (isabet), çıktı karakteri (≈jeton*4), süre. Sonuç: .kos/kopru/rapor/link-30eki-17-ab-file.tsv"""
import os, re, shutil, subprocess, sys, tempfile, time, urllib.request

KOK = r"C:\Projeler\omer-skills"
X = os.path.join(KOK, r"araclar\xerj\bin\xerj-1.0.0-rc.98-x86_64-pc-windows-msvc\xerj.exe")
NW = 0x08000000
env = dict(os.environ, XERJ_DISABLE_FEEDBACK="true")
tmp = tempfile.mkdtemp(prefix="xerj-ab-")
corp = os.path.join(tmp, "corp")
os.makedirs(corp)
for f in os.listdir(os.path.join(KOK, "docs")):
    p = os.path.join(KOK, "docs", f)
    if f.endswith(".md"):
        shutil.copy(p, corp)
shutil.copytree(os.path.join(KOK, "docs", "departmanlar"), os.path.join(corp, "departmanlar"))

# (soru, rg anahtarı, hedef dosya adı)
S = [
    ("limit mesajı gelince ne yapılır, ajan sıra kapısı", "limit", "limit-onlem.md"),
    ("proje başına tek kalıcı oturum devam_id küçük iş haiku", "devam_id", "cc-kullanim-kurali.md"),
    ("özel LLM eğitim planı yerel GPU", "özel LLM", "yerel-ai-ozel-llm-plani.md"),
    ("claude.ai'ye skill zip yükleme adımları", "zip", "claude-ai-yukleme.md"),
    ("frontend departmanı tasarım aracı sırası", "frontend", "frontend.md"),
    ("headroom sıkıştırma ölçümü", "headroom", "headroom-1.md"),
    ("claude-mem gözlem hafıza", "claude-mem", "claude-mem.md"),
    ("erişim kapısı hangi siteye giriş", "erişim", "erisim-kapi.md"),
]
srv = subprocess.Popen([X, "--insecure", "-d", os.path.join(tmp, "data")], env=env, creationflags=NW,
                       stdout=open(os.path.join(tmp, "o.log"), "w"), stderr=subprocess.STDOUT)
try:
    for _ in range(30):
        try:
            urllib.request.urlopen("http://localhost:9200", timeout=2)
            break
        except Exception:
            time.sleep(1)
    t = time.time()
    r = subprocess.run([X, "autoindex", corp], env=env, capture_output=True, text=True, errors="replace", creationflags=NW, timeout=300)
    idx_s = time.time() - t
    print("autoindex", round(idx_s, 1), "s rc", r.returncode, r.stdout[-300:], r.stderr[-300:])
    rows = []
    for q, key, hedef in S:
        t = time.time()
        a = subprocess.run([X, "search", q, "-k", "5"], env=env, capture_output=True, text=True, errors="replace", creationflags=NW, timeout=60).stdout
        ta = time.time() - t
        t = time.time()
        g = subprocess.run(["graphify", "query", q], cwd=KOK, capture_output=True, text=True, errors="replace", creationflags=NW, timeout=120).stdout
        tg = time.time() - t
        t = time.time()
        rg = "".join(f"{os.path.relpath(d, corp)}\{fn}:{i}:{ln}" for d, _, fs in os.walk(corp) for fn in fs
                     for i, ln in enumerate(open(os.path.join(d, fn), encoding="utf-8", errors="replace"), 1) if key.lower() in ln.lower())
        tr = time.time() - t
        rows.append((q, hedef, hedef in a, len(a), round(ta, 2), hedef in g, len(g), round(tg, 2), hedef in rg, len(rg), round(tr, 2)))
        print(rows[-1])
finally:
    srv.terminate()
out = os.path.join(KOK, r".kos\kopru\rapor\link-30eki-17-ab-file.tsv")
with open(out, "w", encoding="utf-8") as f:
    f.write("soru\thedef\txerj_isabet\txerj_kar\txerj_sn\tgraphify_isabet\tgraphify_kar\tgraphify_sn\trg_isabet\trg_kar\trg_sn\n")
    for r_ in rows:
        f.write("\t".join(map(str, r_)) + "\n")
print("BITTI", out)
