"""KATALOG-KANCA-1 madde 3b: uçtan uca — gerçek kanca (--settings ile UserPromptSubmit) ENVANTER-6 düzeninde; claude -p ≤ 10 (+2 yedek).
Zor: 4 paket × K kolu (A ve B' ENVANTER-6 sonuc6.jsonl'dan). Rutin: 3 tek iş × A/K. İstem yönergesi --append-system-prompt'ta
(kos6'da kullanıcı isteminin başındaydı; içindeki "test/güvenlik/KVKK/skill/MCP" sözcükleri her rutin işte kancayı tetiklerdi).
  python kos_kanca.py         → sonuc.jsonl (+ kanca ekinin transkriptte görülüp görülmediği), kor.md, anahtar.json"""
import json, os, random, re, subprocess, sys, time, uuid
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
D = Path(__file__).resolve().parent
WT = D.parents[1]
E6 = WT / ".claude" / "envanter6"
sys.path.insert(0, r"C:\Projeler\omer-skills\.kos\kopru")
from olcum_sira import ram  # noqa: E402

ISTEM = ("Kullanıcının verdiği işlerin her biri için bu ortamda kullanacağın araçlarla kısa bir uygulama planı yaz. "
         "Hiçbir işi YAPMA, dosya yazma/değiştirme. Her iş için '### <no>' başlığı altında: "
         "(a) en çok 6 araç (skill, alt ajan, MCP, CLI, plugin, kütüphane, betik) adı + tek satır gerekçe; "
         "(b) en çok 6 adımlık sıra (hangi adımda hangi araç); (c) kapılar (test/güvenlik/erişilebilirlik/KVKK vb. — hangisi, hangi araçla). "
         "Uygun araç yoksa 'yok' yaz.")
ZOR = [l.split("\t")[2] for l in (E6 / "isler6.tsv").read_text(encoding="utf8").splitlines()]
RUTIN = {i: j for s, i, j in (l.split("\t") for l in (WT / "tools/tests/katalog_kanca_isler.tsv").read_text(encoding="utf8").splitlines())
         if s == "rutin" and i in ("r1", "r4", "r28")}  # frontend · veri · alan-dışı tek alan
ISLER = [("zor", p, ZOR[p * 3:p * 3 + 3]) for p in range(4)] + [("rutin", i, [j]) for i, j in RUTIN.items()]
assert sum(1 if s == "zor" else 2 for s, _, _ in ISLER) <= 10

AYAR = D / "kanca_ayar.json"
AYAR.write_text(json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [
    {"type": "command", "command": f'python "{(WT / "tools" / "katalog_kanca.py").as_posix()}"', "timeout": 5}]}]}}), encoding="utf8")
env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL")}
cwd = E6 / "cwd"
cwd.mkdir(exist_ok=True)
PROJ = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(cwd))
cikti = D / "sonuc.jsonl"
bitti = {(r["kol"], str(r["paket"])) for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines())} if cikti.exists() else set()


def transkript(sid):
    f = PROJ / f"{sid}.jsonl"
    if not f.exists():
        return None, None, None
    ham, u = f.read_text(encoding="utf8"), {}
    for s in map(json.loads, filter(str.strip, ham.splitlines())):
        m = s.get("message") or {}
        if s.get("type") == "assistant" and m.get("usage"):
            u[m.get("id")] = m["usage"]
    top = sum(x.get(k, 0) for x in u.values() for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    return top, sum(x.get("cache_read_input_tokens", 0) for x in u.values()), "<katalog>" in ham


for sinif, p, isler in ISLER:
    for kol in (("K",) if sinif == "zor" else ("A", "K")):
        if (kol, str(p)) in bitti:
            continue
        while ram() >= 86:
            time.sleep(30)
        q = "\n".join(f"{(p * 3 if sinif == 'zor' else 0) + i + 1}. {j}" for i, j in enumerate(isler))
        sid = str(uuid.uuid4())
        kmt = ["claude", "-p", q, "--output-format", "json", "--max-turns", "30", "--session-id", sid, "--append-system-prompt", ISTEM,
               "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--allowedTools", "Bash(python:*)", "Read", "Grep", "Glob"]
        if kol == "K":
            kmt += ["--settings", str(AYAR)]
        t0 = time.time()
        r = subprocess.run(kmt, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf8", timeout=900)
        try:
            j = json.loads(r.stdout)
        except ValueError:
            j = {"result": (r.stdout + r.stderr)[-500:], "is_error": True}
        jt, cr, ekli = transkript(sid)
        rec = dict(sinif=sinif, kol=kol, paket=p, sid=sid, tur=j.get("num_turns"), sure=round(time.time() - t0), jeton=jt, cache_okuma=cr,
                   katalog_eki=ekli, cikis=(j.get("usage") or {}).get("output_tokens"), hata=j.get("is_error"), metin=j.get("result", ""))
        with cikti.open("a", encoding="utf8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(time.strftime("%H:%M:%S"), sinif, kol, p, rec["tur"], rec["jeton"], ekli, rec["hata"], flush=True)

# kör dosya: zor 12 işte K vs B' (ENVANTER-6), X/Y karışık; anahtar ayrı
k = {r["paket"]: r["metin"] for r in map(json.loads, cikti.read_text(encoding="utf8").splitlines()) if r["sinif"] == "zor"}
b = {r["paket"]: r["metin"] for r in map(json.loads, (E6 / "sonuc6.jsonl").read_text(encoding="utf8").splitlines()) if r["kol"] == "B"}
random.seed(61)
anahtar, kor = {}, []
for n, j in enumerate(ZOR, 1):
    p = (n - 1) // 3
    parca = {kol: (re.search(rf"###\s*{n}\b(.*?)(?=###\s*\d+\b|\Z)", m.get(p, ""), re.S) or [None, m.get(p, "")[:2500]])[1].strip()
             for kol, m in (("K", k), ("B", b))}
    x = random.choice("KB")
    anahtar[n] = {"X": x, "Y": "B" if x == "K" else "K"}
    kor.append(f"## {n}. {j}\n### X\n{parca[x][:2500]}\n### Y\n{parca[anahtar[n]['Y']][:2500]}\n")
(D / "kor.md").write_text("\n".join(kor), encoding="utf8")
(D / "anahtar.json").write_text(json.dumps(anahtar), encoding="utf8")
print("bitti")
