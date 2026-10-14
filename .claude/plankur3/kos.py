"""PLAN-KUR-3 ölçüm: YENİ bekletilmiş 10 iş (tests/fixtures/plan_kur3_isler.tsv, 913dcc7), 4 paket × A/B = 8 claude -p + kör yargıç 1 = 9 (tavan 10).
A = main katalog_ara (e05750a), B = plan_kur v3. kos3.py (ENVANTER-3) kalıbı: transkript jetonu, kör dosya, anahtar ayrı.
  python kos.py   → sonuc.jsonl, kor.md, anahtar.json, yargic.json, ozet.txt"""
import json, os, random, re, subprocess, sys, time, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
WT = D.parents[1]
sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
sys.path.insert(0, str(WT / "tools"))
from olcum_sira import ram  # noqa: E402
import plan_kur as pk  # noqa: E402
import katalog_ara as ka  # noqa: E402

KATALOG_A = Path(r"C:\Projeler\omer-skills\tools\katalog_ara.py")  # main e05750a
PLAN_KUR = WT / "tools" / "plan_kur.py"
IS = [s.split("\t")[2] for s in (WT / "tests" / "fixtures" / "plan_kur3_isler.tsv").read_text(encoding="utf8").splitlines()[1:]]
PAKET = [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]  # rutin ayrı paket
ISTEM = ("Aşağıdaki işlerin her biri için bu ortamda uygulanabilir sağlam bir plan yaz. Hiçbir işi YAPMA, dosya yazma/değiştirme. "
         "Her iş '### <no>' başlığı altında en çok 40 satır: fazlar; her fazda adım · araç (skill, alt ajan, MCP, CLI, plugin, kütüphane, betik adı) · "
         "kapı (test/güvenlik/erişilebilirlik/SEO/KVKK vb., hangi araçla) · değişikliği inceleyen ajan · kritik kararda tartışma noktası · "
         "faz jeton bütçesi. Rutin işte planı kısa tut.\n\n")
KURAL = {
    "A": f"Araç bulma: zor (≥2 alan ya da alan dışı) işte katalogu TEK çağrıda kullan — tüm zor işler tek Bash'te art arda: "
         f"python {KATALOG_A} \"<iş>\" ; listeyi oku, ek sorgu yapma (çıktı dosyaya düşerse yalnız o iş için --aday 40 ile yeniden). Rutin işte katalog çağırma.\n\n",
    "B": f"Plan girdisi: zor işlerin hepsi için TEK Bash çağrısı: python {PLAN_KUR} \"<iş 1>\" \"<iş 2>\" … ; çıktıdan seç, "
         f"ek sorgu yapma. Rutin işte çağırma.\n\n",
}
YARGIC = ("Kör yargıçsın. Aşağıda her iş için iki plan var (X ve Y; kaynakları gizli). Her planı 4 ölçütte 0-2 puanla: "
          "kapsam (işin tüm parçaları) · sağlamlık (sayısal kapı/eşik; sayısal kapı yoksa en çok 1) · araç doğruluğu (araç işe ve yığına uygun, "
          "uydurma ya da yığınla uyumsuz araç puan düşürür) · uygulanabilirlik (sıra, adımlar yapılabilir). Uzunluk ödüllendirilmez. "
          "Dosya okuma, araç çağırma. YALNIZ şu JSON'u döndür: {\"<iş no>\": {\"X\": [k,s,a,u], \"Y\": [k,s,a,u]}, ...}\n\n")

env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
env["PYTHONIOENCODING"] = "utf-8"
cwd = D / "cwd"
cwd.mkdir(exist_ok=True)
PROJ = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
cikti = D / "sonuc.jsonl"
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


def claude(q, sid, araclar=True):
    while ram() >= 85:
        time.sleep(30)
    kmt = ["claude", "-p", "--output-format", "json", "--model", "opus", "--max-turns", "30", "--session-id", sid,
           "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands"]
    kmt += ["--allowedTools", "Bash(python:*)", "Read", "Grep", "Glob"] if araclar else ["--tools", ""]
    # istem stdin'den: argv'de kor.md (61k) WinError 206 verir
    r = subprocess.run(kmt, input=q, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf8", timeout=1200, shell=False)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"result": (r.stdout + r.stderr)[-500:], "is_error": True}


for p, grup in enumerate(PAKET):
    for kol in ("A", "B"):
        if (kol, p) in bitti:
            continue
        sid, t0 = str(uuid.uuid4()), time.time()
        j = claude(ISTEM + KURAL[kol] + "\n".join(f"{n + 1}. {IS[n]}" for n in grup), sid)
        jt, cr = transkript_jeton(sid)
        rec = dict(kol=kol, paket=p, sid=sid, tur=j.get("num_turns"), sure=round(time.time() - t0), jeton=jt, cache_okuma=cr,
                   usage=j.get("usage"), hata=j.get("is_error"), metin=j.get("result", ""))
        with cikti.open("a", encoding="utf8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(time.strftime("%H:%M:%S"), kol, p, rec["tur"], rec["jeton"], rec["hata"], flush=True)

kayit = {(r["kol"], r["paket"]): r for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())}
random.seed(2)
anahtar, kor = {}, []
# görev madde 4: yalnız katalogdaki TAM araç adları (kurulu olmayan, kurulu bir adla aynı olmayan); tek sözcüklü ≤4 harf ad gürültü
kur = {o["ad"].lower() for o in pk.kayitlar() if ka.kurulu(o)}
yasak = {o["ad"].lower() for o in pk.kayitlar() if not ka.kurulu(o) and (len(o["ad"]) > 4 or "-" in o["ad"] or ":" in o["ad"])} - kur
kd = {"A": set(), "B": set()}  # plan metninde kurulu olmayan araç adı (Ömer sert kapısı: B'de 0)
for p, grup in enumerate(PAKET):
    for k in "AB":  # tüm plan metni: iş bölümü ayrıştırması kaçırsa da sayılır
        kd[k] |= {w for w in yasak if re.search(rf"(?<![\w:-]){re.escape(w)}(?![\w-])", kayit[(k, p)]["metin"].lower())}
    for n in grup:
        # B0 '## N' başlığı kullandı; yalnız '###' arayınca 1. işin metni 2-3. işe düşüyordu
        parca = {k: (re.search(rf"^#{{2,4}}\s*{n + 1}\b(.*?)(?=^#{{2,4}}\s*\d+\b|\Z)", kayit[(k, p)]["metin"], re.S | re.M)
                     or [None, kayit[(k, p)]["metin"][:4000]])[1].strip() for k in "AB"}
        x = random.choice("AB")
        anahtar[n + 1] = {"X": x, "Y": "B" if x == "A" else "A"}
        kor.append(f"## {n + 1}. {IS[n]}\n### X\n{parca[x][:5000]}\n### Y\n{parca[anahtar[n + 1]["Y"]][:5000]}\n")
(D / "kor.md").write_text("\n".join(kor), encoding="utf8")
(D / "anahtar.json").write_text(json.dumps(anahtar), encoding="utf8")
y = D / "yargic.json"
if not y.exists():
    j = claude(YARGIC + (D / "kor.md").read_text(encoding="utf8"), str(uuid.uuid4()), araclar=False)
    y.write_text(json.dumps(j, ensure_ascii=False), encoding="utf8")
j = json.loads(y.read_text(encoding="utf8"))
m = re.search(r"\{.*\}", j.get("result", ""), re.S)
puan = {"A": 0, "B": 0}
if m:
    for no, v in json.loads(m.group(0)).items():
        for xy in "XY":
            puan[anahtar[int(no)][xy]] += sum(v[xy])
top = lambda k, ps: sum(kayit[(k, p)]["jeton"] or 0 for p in ps)  # noqa: E731
tur = lambda k, ps: sum(kayit[(k, p)]["tur"] or 0 for p in ps)  # noqa: E731
ozet = (f"kalite A {puan['A']} / B {puan['B']} (fark {puan['B'] - puan['A']:+})\n"
        f"zor jeton A {top('A', [0, 1, 2])} / B {top('B', [0, 1, 2])} · tur A {tur('A', [0, 1, 2])} / B {tur('B', [0, 1, 2])}\n"
        f"paket jeton A/B {[(top('A', [p]), top('B', [p])) for p in range(4)]}\n"
        f"rutin jeton A {top('A', [3])} / B {top('B', [3])}\nkurulu-olmayan araç adı A {len(kd['A'])} / B {len(kd['B'])} {sorted(kd['B'])}")
(D / "ozet.txt").write_text(ozet, encoding="utf8")
print(ozet, flush=True)
