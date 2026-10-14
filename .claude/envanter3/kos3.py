"""ENVANTER-3 madde 4 kör kapı: 10 iş (7 zor + 3 rutin), 4 paket, A (bugünkü düzen: zor işte katalog_ara tek çağrı) /
B (plan-kur tek çağrı); claude -p ≤ 8 (+2 yedek). kos6.py'nin kalıbı (transkript jetonu, kör dosya, anahtar ayrı).
  python kos3.py   → sonuc3.jsonl, kor3.md, anahtar3.json"""
import json, os, random, re, subprocess, sys, time, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
WT = D.parents[1]
sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
from olcum_sira import ram  # noqa: E402

KATALOG_A = Path(r"C:\Projeler\omer-skills-wt\envanter6\tools\katalog_ara.py")  # bugünkü sürüm (öğrenimsiz)
PLAN_KUR = WT / "tools" / "plan_kur.py"
IS = [
    ("z1", "Küçük bir muhasebe bürosu için 5 sayfalık pazarlama sitesi yap: KVKK uyumlu iletişim formu ve çerez bildirimi, SEO, güvenlik testi, Hostinger'a yayın."),
    ("z2", "ASP.NET Core ile randevu sistemi API'si: JWT kimlik doğrulama, EF Core + PostgreSQL migration, rol bazlı yetki, xUnit testleri ve OpenAPI dokümanı."),
    ("z3", "Three.js tarayıcı oyununa 2-4 kişilik çok oyunculu yarış modu ekle: WebSocket senkron, gecikme telafisi, skor tablosu ve hile önleme."),
    ("z4", "Blender'da parfüm şişesi ürün sahnesi kur: modelleme, cam malzeme, stüdyo ışığı, turntable render ve web için 2 MB altı GLB dışa aktarımı."),
    ("z5", "Instagram Reels için otomatik video hattı: uzun videodan en iyi 3 anı seç, dikey kırp, altyazı ekle, sesi normalize et, zamanlanmış yükleme."),
    ("z6", "TELVE çay markası sitesini (Astro + three.js + GSAP + Lenis) awwwards seviyesinde 3D animasyonlu scroll deneyimiyle baştan yeniden yap."),
    ("z7", "Yayındaki Next.js e-ticaret sitesinin uçtan uca güvenlik testi: SAST, sır taraması, DAST, ödeme akışı ve yetkilendirme kontrolü, öncelikli bulgu raporu."),
    ("r1", "README'deki kurulum komutundaki yazım hatasını düzelt."),
    ("r2", "ffmpeg ile bir videonun ilk 10 saniyesini kes."),
    ("r3", ".NET projesinde bir DTO alanının adını CustomerName olarak değiştir."),
]
PAKET = [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]  # rutin işler ayrı pakette: rutin jetonu A/B ayrı karşılaştırılır
assert len(PAKET) * 2 <= 8, "claude -p tavanı 8 (+2 yedek)"
ISTEM = ("Aşağıdaki işlerin her biri için bu ortamda uygulanabilir sağlam bir plan yaz. Hiçbir işi YAPMA, dosya yazma/değiştirme. "
         "Her iş '### <no>' başlığı altında en çok 40 satır: fazlar; her fazda adım · araç (skill, alt ajan, MCP, CLI, plugin, kütüphane, betik adı) · "
         "kapı (test/güvenlik/erişilebilirlik/SEO/KVKK vb., hangi araçla) · değişikliği inceleyen ajan · kritik kararda tartışma noktası · "
         "faz jeton bütçesi. Rutin işte planı kısa tut.\n\n")
KURAL = {
    "A": f"Araç bulma: zor (≥2 alan ya da alan dışı) işte katalogu TEK çağrıda kullan — tüm zor işler tek Bash'te art arda: "
         f"python {KATALOG_A} \"<iş>\" ; listeyi oku, ek sorgu yapma. Rutin işte katalog çağırma.\n\n",
    "B": f"Plan girdisi: zor işlerin hepsi için TEK Bash çağrısı: python {PLAN_KUR} \"<iş 1>\" \"<iş 2>\" … ; çıktıdaki kapı, inceleme ajanı, "
         f"konsey ve aday listesinden seç, ek sorgu yapma. Rutin işte çağırma.\n\n",
}

env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
env["PYTHONIOENCODING"] = "utf-8"
cwd = D / "cwd"
cwd.mkdir(exist_ok=True)
PROJ = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
EK = sys.argv[1] if len(sys.argv) > 1 else ""  # yeniden koşu: python kos3.py b → sonuc3b/kor3b/anahtar3b (eski A kayıtları kopyalanır)
cikti = D / f"sonuc3{EK}.jsonl"
bitti = {(r["kol"], r["paket"]) for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())} if cikti.exists() else set()


def transkript_jeton(sid):
    f = PROJ / f"{sid}.jsonl"
    if not f.exists():
        return None, None
    u = {}
    for s in map(json.loads, filter(str.strip, f.read_text(encoding="utf8").splitlines())):
        m = s.get("message") or {}
        if s.get("type") == "assistant" and m.get("usage"):
            u[m.get("id")] = m["usage"]
    top = sum(x.get(k, 0) for x in u.values() for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return top, sum(x.get("cache_read_input_tokens", 0) for x in u.values())


t_bas = time.time()
while not (WT / "docs" / "katalog" / "ogrenim.jsonl").exists() and time.time() - t_bas < 3600:
    time.sleep(60)  # B öğrenim kataloğuyla koşsun
for p, grup in enumerate(PAKET):
    for kol in ("A", "B"):
        if (kol, p) in bitti:
            continue
        while ram() >= 86:
            time.sleep(30)
        q = ISTEM + KURAL[kol] + "\n".join(f"{n + 1}. {IS[n][1]}" for n in grup)
        sid = str(uuid.uuid4())
        kmt = ["claude", "-p", q, "--output-format", "json", "--max-turns", "30", "--session-id", sid,
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
               "--allowedTools", "Bash(python:*)", "Read", "Grep", "Glob"]
        t0 = time.time()
        r = subprocess.run(kmt, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf8", timeout=900, shell=False)
        try:
            j = json.loads(r.stdout)
        except ValueError:
            j = {"result": (r.stdout + r.stderr)[-500:], "is_error": True}
        jt, cr = transkript_jeton(sid)
        rec = dict(kol=kol, paket=p, sid=sid, tur=j.get("num_turns"), sure=round(time.time() - t0), jeton=jt, cache_okuma=cr,
                   cikis=(j.get("usage") or {}).get("output_tokens"), hata=j.get("is_error"), metin=j.get("result", ""))
        with cikti.open("a", encoding="utf8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(time.strftime("%H:%M:%S"), kol, p, rec["tur"], rec["jeton"], rec["hata"], flush=True)

kayit = {(r["kol"], r["paket"]): r["metin"] for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())}
random.seed(3 + len(EK))
anahtar, kor = {}, []
for p, grup in enumerate(PAKET):
    for n in grup:
        parca = {k: (re.search(rf"###\s*{n + 1}\b(.*?)(?=###\s*\d+\b|\Z)", kayit.get((k, p), ""), re.S)
                     or [None, kayit.get((k, p), "")[:4000]])[1].strip() for k in "AB"}
        x = random.choice("AB")
        anahtar[n + 1] = {"X": x, "Y": "B" if x == "A" else "A"}
        kor.append(f"## {n + 1}. {IS[n][1]}\n### X\n{parca[x][:4000]}\n### Y\n{parca[anahtar[n + 1]['Y']][:4000]}\n")
(D / f"kor3{EK}.md").write_text("\n".join(kor), encoding="utf8")
(D / f"anahtar3{EK}.json").write_text(json.dumps(anahtar), encoding="utf8")
print("bitti", len(kayit), "çağrı")
