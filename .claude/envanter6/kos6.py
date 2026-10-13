"""ENVANTER-6 madde 3-4 değer kapısı: 12 zor iş (8 karma + 4 alan dışı), 3'lü paket, A (bugünkü düzen) / B' (katalog ön-enjeksiyon); claude -p ≤ 8.
B' = UserPromptSubmit kancası benzetimi: katalog_ara iş başına betikte (yerel, 0 tur) koşar, çıktısı --append-system-prompt ile eklenir.
Jeton transkriptten (benzersiz mesaj id'leri: in+cc+cr+out) — ENVANTER-2'de json usage B'de yalnız ilk+son mesajı sayıyordu.
  python kos6.py --hazirla   → isler6.tsv + ek boyutları + hedef araç isabeti (claude -p yok)
  python kos6.py             → sonuc6.jsonl, kor6.md, anahtar6.json"""
import json, os, random, re, subprocess, sys, time, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
WT = D.parents[1]
sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
from olcum_sira import ram  # noqa: E402

KATALOG = WT / "tools" / "katalog_ara.py"
KARMA = ["k14", "k15", "k16", "k18", "k19", "k22", "k27", "k30"]
DISARI = [  # (id, iş, katalogda beklenen araç) — sistem isteminde (skill/ajan listesi) görünmeyen MCP/CLI/bizim araç
    ("o1", "Bir Android APK dosyasını kaynak koda çevirip istediği izinleri ve gömülü API anahtarlarını raporla.", "droidasc"),
    ("o2", "Hostinger'daki alan adının DNS kayıtlarını güncelle ve sitenin VPS'e yayınını doğrula.", "hostinger"),
    ("o3", "3D ürün modelinin GLB dosyasını web için sıkıştır, doku boyutlarını küçült ve mesh sayısını raporla.", "glb_hat"),
    ("o4", "Bu repodaki bütün skill filosunun API'siz statik kalite denetimini çıkar ve sorunlu skill'leri listele.", "skill_filo_denetim"),
]
ISTEM = ("Aşağıdaki işlerin her biri için bu ortamda kullanacağın araçlarla kısa bir uygulama planı yaz. "
         "Hiçbir işi YAPMA, dosya yazma/değiştirme. Her iş için '### <no>' başlığı altında: "
         "(a) en çok 6 araç (skill, alt ajan, MCP, CLI, plugin, kütüphane, betik) adı + tek satır gerekçe; "
         "(b) en çok 6 adımlık sıra (hangi adımda hangi araç); (c) kapılar (test/güvenlik/erişilebilirlik/KVKK vb. — hangisi, hangi araçla). "
         "Uygun araç yoksa 'yok' yaz.\n\n")
EK_BAS = ("Bu ortamın araç kataloğundan (skill · ajan · plugin · MCP · CLI · kütüphane · bizim betik) her iş için önceden çekilmiş aday listesi aşağıda. "
          "Ek katalog sorgusu yapma; adayları kendi bildiğin araçlarla birlikte değerlendir, ilgili olanları planda adım adım kullan.\n\n")


def isler():
    k = {r["id"]: r["is"] for r in map(json.loads, (D / "isler5.jsonl").read_text(encoding="utf8").splitlines())}
    return [(i, k[i], "") for i in KARMA] + DISARI


def katalog(q):
    return subprocess.run([sys.executable, str(KATALOG), q], capture_output=True, text=True, encoding="utf8").stdout


IS = isler()
paketler = [IS[i:i + 3] for i in range(0, len(IS), 3)]
assert len(paketler) * 2 <= 8, "claude -p tavanı 8 (+2 yedek)"


def ek(grup, p):
    return EK_BAS + "\n".join(f"### {p * 3 + i + 1}. {j}\n{katalog(j)}" for i, (_, j, _) in enumerate(grup))


if "--hazirla" in sys.argv:
    (D / "isler6.tsv").write_text("".join(f"{n}\t{i}\t{j}\t{h}\n" for n, (i, j, h) in enumerate(IS, 1)), encoding="utf8")
    for p, g in enumerate(paketler):
        e = ek(g, p)
        print("paket", p, "ek karakter", len(e), "isabet", [h in e for _, _, h in g if h])
    sys.exit()

env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
cwd = D / "cwd"
cwd.mkdir(exist_ok=True)
PROJ = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
cikti = D / "sonuc6.jsonl"
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
        while ram() >= 86:  # ilk yuva olcum_sira'da <%88; ek çağrı <%86, asla >%90
            time.sleep(30)
        q = ISTEM + "\n".join(f"{p * 3 + i + 1}. {j}" for i, (_, j, _) in enumerate(grup))
        sid = str(uuid.uuid4())
        kmt = ["claude", "-p", q, "--output-format", "json", "--max-turns", "30", "--session-id", sid,
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--allowedTools", "Bash(python:*)", "Read", "Grep", "Glob"]
        if kol == "B":
            kmt += ["--append-system-prompt", ek(grup, p)]
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

# kör dosya: iş başına iki yanıt X/Y karışık; anahtar ayrı
kayit = {(r["kol"], r["paket"]): r["metin"] for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())}
random.seed(6)
anahtar, kor = {}, []
for n, (_, j, _) in enumerate(IS, 1):
    p = (n - 1) // 3
    parca = {k: (re.search(rf"###\s*{n}\b(.*?)(?=###\s*\d+\b|\Z)", kayit.get((k, p), ""), re.S) or [None, kayit.get((k, p), "")[:2500]])[1].strip()
             for k in "AB"}
    x = random.choice("AB")
    anahtar[n] = {"X": x, "Y": "B" if x == "A" else "A"}
    kor.append(f"## {n}. {j}\n### X\n{parca[x][:2500]}\n### Y\n{parca[anahtar[n]['Y']][:2500]}\n")
(D / "kor6.md").write_text("\n".join(kor), encoding="utf8")
(D / "anahtar6.json").write_text(json.dumps(anahtar), encoding="utf8")
print("bitti", len(kayit), "çağrı")
