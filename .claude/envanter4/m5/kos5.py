"""ENVANTER-4 m5 kör kapı: 15 iş (ENVANTER-5 isler5 kümesi, tarife bakılmadan: ilk 10 karma + ilk 5 farklı alanlı gerçek/rutin).
A = bugünkü katalog_ara tek çağrı (kanca benzetimi, ön-enjeksiyon); B = A + kilavuz_ara.tarif_bul tarifi, yalnız katalog_kanca.tetik (zor) ise.
Paketler türdeş (2×5 zor + 1×5 rutin) → 6 claude -p (tavan 10). Jeton transkriptten (kos6 yöntemi).
  python kos5.py --hazirla   → isler.tsv + ek boyutları + tarif eşleşmeleri (claude -p yok)
  python kos5.py             → sonuc.jsonl, kor.md, anahtar.json"""
import json, os, random, re, subprocess, sys, time, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
WT = D.parents[2]
sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
sys.path.insert(0, str(WT / "tools"))
sys.path.insert(0, r"C:\Projeler\omer-skills\tools")  # bugünkü katalog_kanca (zor/rutin kapısı)
from olcum_sira import ram  # noqa: E402
from kilavuz_ara import tarif_bul  # noqa: E402
from katalog_kanca import tetik  # noqa: E402

KATALOG = Path(r"C:\Projeler\omer-skills\tools\katalog_ara.py")  # bugünkü (main, BİRLEŞTİR-19 sonrası)
ISLER5 = Path(r"C:\Projeler\omer-skills-wt\envanter6\.claude\envanter6\isler5.jsonl")
ISTEM = ("Aşağıdaki işlerin her biri için bu ortamda kullanacağın araçlarla kısa bir uygulama planı yaz. "
         "Hiçbir işi YAPMA, dosya yazma/değiştirme. Her iş için '### <no>' başlığı altında: "
         "(a) en çok 6 araç (skill, alt ajan, MCP, CLI, plugin, kütüphane, betik) adı + tek satır gerekçe; "
         "(b) en çok 6 adımlık sıra (hangi adımda hangi araç); (c) kapılar (test/güvenlik/erişilebilirlik/KVKK vb. — hangisi, hangi araçla). "
         "Uygun araç yoksa 'yok' yaz.\n\n")
EK_BAS = ("Bu ortamın araç kataloğundan (skill · ajan · plugin · MCP · CLI · kütüphane · bizim betik) her iş için önceden çekilmiş aday listesi aşağıda. "
          "Ek katalog sorgusu yapma; adayları kendi bildiğin araçlarla birlikte değerlendir, ilgili olanları planda adım adım kullan.\n\n")
TARIF_BAS = "Birleşim tarifi (bu iş türü için faz faz önerilen araçlar; uymayan kısmı atla):\n"


def isler():
    r = [json.loads(s) for s in ISLER5.read_text(encoding="utf8").splitlines() if s.strip()]
    zor = sorted((x for x in r if x["tur"] == "karma"), key=lambda x: int(re.sub(r"\D", "", x["id"])))[:10]
    rutin, alan = [], set()
    # gerçek tek alanlı yalnız 4 → önce gerçek, sonra sentetik (hepsi tek alanlı)
    for x in sorted((x for x in r if x["tur"] in ("gercek", "sentetik")), key=lambda x: (x["tur"] != "gercek", int(re.sub(r"\D", "", x["id"])))):
        a = tuple(x["alan"])  # rutin = tek alanlı
        if len(a) == 1 and a not in alan and len(rutin) < 5:
            rutin.append(x), alan.add(a)
    return [("zor", x["id"], x["is"]) for x in zor] + [("rutin", x["id"], x["is"]) for x in rutin]


def katalog(q):
    return subprocess.run([sys.executable, str(KATALOG), q], capture_output=True, text=True, encoding="utf8").stdout


IS = isler()
paketler = [IS[i:i + 5] for i in range(0, len(IS), 5)]
assert len(IS) == 15 and len(paketler) * 2 <= 10, "claude -p tavanı 10"


def ek(grup, p, kol):
    out = []
    for i, (_, _, j) in enumerate(grup):
        s = f"### {p * 5 + i + 1}. {j}\n{katalog(j)}"
        t = tarif_bul(j) if kol == "B" and tetik(j) else None  # rutin işte tarif yok
        if t:
            s += "\n" + TARIF_BAS + t.read_text(encoding="utf8").strip() + "\n"
        out.append(s)
    return EK_BAS + "\n".join(out)


if "--hazirla" in sys.argv:
    (D / "isler.tsv").write_text("".join(f"{n}\t{t}\t{i}\t{j}\n" for n, (t, i, j) in enumerate(IS, 1)), encoding="utf8")
    for n, (t, i, j) in enumerate(IS, 1):
        f = tarif_bul(j)
        print(n, t, i, "tarif:", f.stem if f else "-")
    for p, g in enumerate(paketler):
        a, b = ek(g, p, "A"), ek(g, p, "B")
        print("paket", p, g[0][0], "A kr", len(a), "B kr", len(b), "B ek ~jeton", (len(b) - len(a)) // 3)
    sys.exit()

env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
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
            u[m.get("id")] = m["usage"]  # aynı mesajın içerik parçaları aynı usage'ı taşır
    top = sum(x.get(k, 0) for x in u.values() for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return top, sum(x.get("cache_read_input_tokens", 0) for x in u.values())


for p, grup in enumerate(paketler):
    for kol in ("A", "B"):
        if (kol, p) in bitti:
            continue
        while ram() >= 85:  # görev kuralı: RAM ≥%85 iken açma
            time.sleep(30)
        q = ISTEM + "\n".join(f"{p * 5 + i + 1}. {j}" for i, (_, _, j) in enumerate(grup))
        sid = str(uuid.uuid4())
        f = D / f"ek_{kol}{p}.txt"  # komut satırı 32k sınırı (WinError 206) → dosyadan
        f.write_text(ek(grup, p, kol), encoding="utf8")
        kmt = ["claude", "-p", q, "--output-format", "json", "--max-turns", "30", "--session-id", sid, "--disable-slash-commands",
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--allowedTools", "Bash(python:*)", "Read", "Grep", "Glob",
               "--append-system-prompt-file", str(f)]
        t0 = time.time()
        r = subprocess.run(kmt, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf8", timeout=900, shell=False)
        try:
            j = json.loads(r.stdout)
        except ValueError:
            j = {"result": (r.stdout + r.stderr)[-500:], "is_error": True}
        jt, cr = transkript_jeton(sid)
        rec = dict(kol=kol, paket=p, tur_is=grup[0][0], sid=sid, tur=j.get("num_turns"), sure=round(time.time() - t0), jeton=jt, cache_okuma=cr,
                   cikis=(j.get("usage") or {}).get("output_tokens"), hata=j.get("is_error"), metin=j.get("result", ""))
        with cikti.open("a", encoding="utf8") as fo:
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(time.strftime("%H:%M:%S"), kol, p, rec["tur"], rec["jeton"], rec["hata"], flush=True)

# kör dosya: iş başına iki yanıt X/Y karışık; anahtar ayrı
kayit = {(r["kol"], r["paket"]): r["metin"] for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())}
random.seed(45)
anahtar, kor = {}, []
for n, (_, _, j) in enumerate(IS, 1):
    p = (n - 1) // 5
    parca = {k: (re.search(rf"###\s*{n}\b(.*?)(?=###\s*\d+\b|\Z)", kayit.get((k, p), ""), re.S) or [None, kayit.get((k, p), "")[:2500]])[1].strip()
             for k in "AB"}
    x = random.choice("AB")
    anahtar[n] = {"X": x, "Y": "B" if x == "A" else "A"}
    kor.append(f"## {n}. {j}\n### X\n{parca[x][:3000]}\n### Y\n{parca[anahtar[n]['Y']][:3000]}\n")
(D / "kor.md").write_text("\n".join(kor), encoding="utf8")
(D / "anahtar.json").write_text(json.dumps(anahtar), encoding="utf8")
print("bitti", len(kayit), "çağrı")
