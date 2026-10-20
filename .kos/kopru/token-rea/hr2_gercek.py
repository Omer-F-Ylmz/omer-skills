"""hr2 GERÇEK YÜK ölçümü: son 14 gün transkriptlerindeki gerçek araç çıktıları → hr2 vs Headroom vs ham (aynı sayaç tiktoken cl100k).
Headroom'un python'uyla koş: <uv tools>/headroom-ai/Scripts/python.exe hr2_gercek.py uret <tohum> | skor <tohum> [headroom: 0|1]
Örnek yalnız ≥MIN kr çıktı (hr2 altını zaten aynen döner); tür başına rezervuar. İğne = ham çıktıdaki sinyal satırları (hata/başarısızlık/exit kodu...),
çıktıda aynen duruyor mu (geri alma komutu hariç — o hep tam metni verir). Geliştiren oturum heldout/hrg_<tohum>.json içeriğini OKUMAZ."""
import glob, importlib.util, json, os, random, re, sys, tempfile, time, subprocess
from pathlib import Path

D = Path(__file__).parent
H = D / "heldout"
GUN, MIN, K = 14, 1500, 40
TURLER = ("test", "log", "build", "grep", "git", "ls", "json")
SIG = re.compile(r"error|fail|exception|traceback|fatal|panic|denied|warn|exit code|passed|✗|✘", re.I)


def tur(ad, girdi, m):
    if ad == "Grep": return "grep"
    if ad == "Glob": return "ls"
    if ad != "Bash": return None
    c = girdi.get("command", "")
    if re.search(r"\b(dotnet test|pytest|npm (run )?test|vitest|jest|unittest|cargo test|go test)\b", c): return "test"
    if re.search(r"\b(dotnet build|msbuild|tsc|npm run build|cargo build|pip install|npm install|npm ci|dotnet publish)\b", c): return "build"
    if re.search(r"\bgit\b", c): return "git"
    if re.search(r"\b(grep|rg|findstr|Select-String)\b", c): return "grep"
    if re.search(r"\b(tail|docker logs|journalctl|gh run)\b|\.log\b", c): return "log"
    if re.search(r"(^|[;&| ])(ls|dir|find|tree|Get-ChildItem)\b", c): return "ls"
    if m.lstrip()[:1] in "[{":
        try:
            json.loads(m); return "json"
        except ValueError: pass
    return None


def uret(tohum):
    rng, simdi = random.Random(tohum), time.time()
    rez, sayac, kr = {t: [] for t in TURLER}, {t: [0, 0, 0] for t in TURLER}, 0  # sayac: adet, ≥MIN adet, ≥MIN toplam kr
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        if simdi - os.path.getmtime(f) > GUN * 86400: continue
        kullan = {}
        for l in open(f, encoding="utf-8", errors="replace"):
            if '"tool_use"' not in l and '"tool_result"' not in l: continue
            try: d = json.loads(l)
            except ValueError: continue
            c = d.get("message", {}).get("content")
            if not isinstance(c, list): continue
            for b in c:
                if b.get("type") == "tool_use": kullan[b["id"]] = (b["name"], b.get("input") or {})
                elif b.get("type") == "tool_result" and b.get("tool_use_id") in kullan:
                    m = b["content"] if isinstance(b["content"], str) else "".join(x.get("text", "") for x in b["content"] if isinstance(x, dict))
                    t = tur(*kullan[b["tool_use_id"]], m)
                    if not t: continue
                    kr += 1; s = sayac[t]; s[0] += 1
                    if len(m) < MIN: continue
                    s[1] += 1; s[2] += len(m)
                    if len(rez[t]) < K: rez[t].append(m)
                    elif (j := rng.randrange(s[1])) < K: rez[t][j] = m
    H.mkdir(exist_ok=True)
    S = [dict(tur=t, yuk=m) for t in TURLER for m in rez[t]]
    (H / f"hrg_{tohum}.json").write_text(json.dumps(S, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(dict(ornek=len(S), tur={t: len(rez[t]) for t in TURLER}, populasyon={t: dict(adet=s[0], uzun=s[1], uzun_kr=s[2]) for t, s in sayac.items()}), ensure_ascii=False))


def iginler(m):
    L = {l.strip() for l in m.splitlines() if SIG.search(l) and l.strip()}
    return sorted(L, key=len)[:60]  # çok uzun sinyal listesi baskın olmasın


def skor(tohum, headroom):
    import tiktoken
    E = tiktoken.get_encoding("cl100k_base")
    tok = lambda s: len(E.encode(s, disallowed_special=()))
    sp = importlib.util.spec_from_file_location("hr2", D / "hr2.py"); hr2 = importlib.util.module_from_spec(sp); sp.loader.exec_module(hr2)
    hr2.AC = tempfile.mkdtemp()
    S = json.loads((H / f"hrg_{tohum}.json").read_text(encoding="utf-8"))
    onb = H / f"hrg_hroom_{tohum}.json"
    HB = json.loads(onb.read_text(encoding="utf-8")) if onb.exists() else {}
    if headroom:
        from headroom import compress
    R = []
    for i, h in enumerate(S):
        m = h["yuk"]; a = tok(m); ig = iginler(m)
        c2 = hr2.hr2(m)
        r = dict(tur=h["tur"], a=a, b2=tok(c2), n=len(ig), k2=sum(x in c2 for x in ig), pass2=int(c2 == m))
        if headroom and str(i) not in HB:
            t = time.time()
            try:
                c = compress([{"role": "user", "content": "ne oldu?"}, {"role": "tool", "content": m}], model="claude-opus-5-5").messages[-1]["content"]
                c = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
            except Exception: c = m  # noqa: BLE001
            HB[str(i)] = dict(bh=tok(c), kh=sum(x in c for x in ig), snh=round(time.time() - t, 2))
            onb.write_text(json.dumps(HB), encoding="utf-8")
        r.update(HB.get(str(i), {}))
        R.append(r)
    out = {}
    for ad, f in (("hepsi", lambda x: True), *[(t, lambda x, t=t: x["tur"] == t) for t in TURLER]):
        L = [x for x in R if f(x)]
        if not L: continue
        a = sum(x["a"] for x in L); n = sum(x["n"] for x in L)
        o = dict(n=len(L), tasarruf_hr2=round(100 * (a - sum(x["b2"] for x in L)) / a, 1), igne_hr2=f'{sum(x["k2"] for x in L)}/{n}',
                 tam_igne_hr2=f'{sum(x["k2"] == x["n"] for x in L)}/{len(L)}', degisti_hr2=sum(not x["pass2"] for x in L))
        H2 = [x for x in L if "bh" in x]
        if H2:
            ah = sum(x["a"] for x in H2)
            o.update(tasarruf_headroom=round(100 * (ah - sum(x["bh"] for x in H2)) / ah, 1), tasarruf_hr2_ayni_kume=round(100 * (ah - sum(x["b2"] for x in H2)) / ah, 1),
                     igne_headroom=f'{sum(x["kh"] for x in H2)}/{sum(x["n"] for x in H2)}', n_headroom=len(H2), sn_headroom=round(sum(x["snh"] for x in H2) / len(H2), 2))
        out[ad] = o
    # 100+ satırlık alt küme (taslak: ≥100 satırlık çıktı)
    U = [(x, len(h["yuk"].splitlines())) for x, h in zip(R, S)]
    for ad, f in (("uzun100", lambda s: s >= 100), ("kisa100", lambda s: s < 100)):
        L = [x for x, s in U if f(s)]
        if L:
            a = sum(x["a"] for x in L)
            out[ad] = dict(n=len(L), tasarruf_hr2=round(100 * (a - sum(x["b2"] for x in L)) / a, 1), igne_kayip_hr2=sum(x["n"] - x["k2"] for x in L))
    print(json.dumps(out, ensure_ascii=False))
    (H / f"hrg_skor_{tohum}.json").write_text(json.dumps(dict(ozet=out, satir=R), ensure_ascii=False), encoding="utf-8")


def e2e(tohum, n=15):  # uçtan uca süre: subprocess, -I -S
    S = json.loads((H / f"hrg_{tohum}.json").read_text(encoding="utf-8"))[:: max(1, len(json.loads((H / f"hrg_{tohum}.json").read_text(encoding="utf-8"))) // n)]
    T = []
    for h in S:
        t = time.time(); subprocess.run(["python", "-I", "-S", str(D / "hr2.py")], input=h["yuk"].encode("utf-8"), capture_output=True); T.append(time.time() - t)
    print(json.dumps(dict(n=len(T), ort=round(sum(T) / len(T), 3), maks=round(max(T), 3))))


if __name__ == "__main__":
    {"uret": lambda: uret(sys.argv[2]), "skor": lambda: skor(sys.argv[2], sys.argv[3:4] == ["1"]), "e2e": lambda: e2e(sys.argv[2])}[sys.argv[1]]()
