"""VIDEO-764-2 koşucu: python video764_kos.py kos <n> [--ids id,id] | parti <n> | durum
kos: sıradaki n işlenmemiş video → metin (altyazı, yoksa Groq ASR) → ücretsiz özet (Gemini→Groq→OpenRouter :free, doğrulamalı), N≤3 paralel.
parti: özeti hazır, kararı yok n videoyu parti-NN.txt'ye döker (Claude karar verir). Kaldığı yerden devam: özet önbelleği + tsv."""
import json, os, re, subprocess, sys, threading, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

R = Path(r"C:\Projeler\omer-skills"); K = Path(r"C:\Projeler\.video-cache"); O = Path(r"C:\Projeler\.video764")
TSV = R / ".kos/kopru/ogren/video-764.tsv"; HATA = R / ".kos/kopru/ogren/video-764-hata.tsv"; OLCUM = R / ".kos/kopru/ogren/video-764-olcum.tsv"
LISTE = R / ".kos/kopru/devir/video-linkleri-20eki.txt"
URL = {"w": "https://www.youtube.com/watch?v=%s", "yt": "https://youtu.be/%s", "y": "https://www.youtube.com/shorts/%s",
       "r": "https://www.instagram.com/reel/%s/", "p": "https://www.instagram.com/p/%s/"}
NW = 0x08000000
sys.path.insert(0, str(R / "tools")); import ucretsiz_havuz as HAVUZ  # noqa: E402
KILIT = threading.Lock(); TEK = threading.Lock()
ISTEM = ("Aşağıdaki video metni (altyazı/ses çevirisi + açıklama). TÜRKÇE, EN FAZLA 900 karakterlik, EN AZ 3 cümlelik özet yaz: "
         "1) video ne anlatıyor/gösteriyor 2) anılan araç/skill/MCP/repo adları ve linkleri 3) bir Claude Code + skill deposu "
         "kullanıcısına somut ne öğretiyor. Metinde olmayanı uydurma.")


def ram():
    import psutil
    return psutil.virtual_memory().percent


def sh(a, t, cwd=R):
    p = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t, creationflags=NW, cwd=cwd,
                       env={**os.environ, "PYTHONPATH": "."} if cwd != R else None)
    return p.returncode, p.stdout + p.stderr


def yeniden(a, t, n=3, cwd=R):  # zaman aşımı + 2 yeniden deneme
    for i in range(n):
        try:
            rc, s = sh(a, t, cwd)
            if rc == 0 and (a[0] != "video" or " · " in (s.splitlines() or [""])[0]):
                return rc, s
        except subprocess.TimeoutExpired:
            rc, s = 124, "zaman aşımı"
        time.sleep(3 * (i + 1))
    return rc, s


def post(url, body, h, t=45):
    q = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", **h})
    return json.loads(urllib.request.urlopen(q, timeout=t).read())


def get(url, h={}):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", **h}), timeout=30).read())


def modeller():
    """Canlı model listesi (sabit ad yok). gemini: en yeni flash'lar; groq: gpt-oss-120b; openrouter: gpt-oss-120b:free."""
    g, q, o = [], [], []
    try:
        ad = [m["name"].split("/")[-1] for m in get("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200&key=" + os.environ["GEMINI_API_KEY"])["models"]
              if "generateContent" in m.get("supportedGenerationMethods", [])]
        g = sorted([a for a in ad if re.fullmatch(r"gemini-[\d.]+-flash(-lite)?", a)],
                   key=lambda a: ([-float(x) for x in re.findall(r"[\d.]+", a)[:1]], "lite" in a))[:3]
    except Exception:
        pass
    try:
        q = [m["id"] for m in get("https://api.groq.com/openai/v1/models", {"Authorization": "Bearer " + os.environ["GROQ_API_KEY"]})["data"] if "gpt-oss-120b" in m["id"]][:1]
    except Exception:
        pass
    try:
        ids = [m["id"] for m in get("https://openrouter.ai/api/v1/models")["data"] if m["id"].endswith(":free")]
        o = [i for p in ("nemotron-3-super", "gemma-4-31b", "minimax-m3") for i in ids if p in i][:3]  # ≥2 farklı model
    except Exception:
        pass
    return [("gemini", m) for m in g] + [("openrouter", m) for m in o] + [("groq", m) for m in q] + [("haiku", "haiku")]


def gecerli(o, girdi, baslik):
    """≥3 cümle, uydurma link yok, başlıkla (ya da metinle) konu uyumu."""
    if len(o) < 150 or len(re.findall(r"[.!?](\s|$)", o)) < 3:
        return "kısa/<3 cümle"
    if any(u.rstrip(".,)*]>`\"'") not in girdi for u in re.findall(r"https?://\S+", o)):
        return "uydurma link"
    kel = {w for w in re.findall(r"\w{4,}", baslik.lower())}
    if kel and not any(w in o.lower() for w in kel) and len(girdi) > 600:
        # başlık çoğu zaman IG açıklaması; metinle de bağ yoksa konu kayması
        if not any(w in o.lower() for w in set(re.findall(r"\w{6,}", girdi.lower()[:3000]))):
            return "konu uyumsuz"
    return None


HAIKU_TAVAN = 800  # koşu başına en fazla çağrı
KAPALI = {}  # (halka, model) -> yeniden deneme zamanı; kota/zaman aşımı alan halka 30 dk devre dışı, BEKLEME YOK
SAY = {}; HK = {"cagri": 0, "usd": 0.0}; SL = threading.Lock()


def haiku(istem):
    """Plan kotasından `claude -p --model haiku` (API anahtarı yok). (metin, usd)"""
    with SL:
        if HK["cagri"] >= HAIKU_TAVAN:
            raise RuntimeError("haiku tavan")
        HK["cagri"] += 1
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    p = subprocess.run(["claude", "-p", "--model", "haiku", "--output-format", "json", "--max-turns", "1", "--tools", "", "--setting-sources", ""],
                       input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150, creationflags=NW, cwd=O, env=env)
    j = json.loads(p.stdout)
    with SL:
        HK["usd"] += j.get("total_cost_usd") or 0
    if j.get("is_error") or not j.get("result"):
        raise RuntimeError("haiku " + str(j.get("result"))[:80])
    return j["result"], j.get("total_cost_usd") or 0


def ozet(girdi, baslik, zincir, r):
    """Ücretsiz havuz (tüm sağlayıcılar, yük dağıtımlı, 429'da bekleme yok); `zincir` eski imza için kalır, kullanılmaz."""
    y, k, log = HAVUZ.cagir("ozet", ISTEM + "\n\n" + girdi, max_tokens=1500, haiku_tavan=HAIKU_TAVAN, etiket="video764",
                            dogrula=lambda o: gecerli(o, girdi, baslik))
    if y:
        r["model"] = k; return y
    r["ozet_log"] = log
    return None


KRITER = ("Bir Claude Code + skill deposu sahibi için aşağıdaki video özetlerini karara bağla. Karar: AL (çok nadir: metinde adı VE repo/linki açık, açık kaynak, doğrudan kurulur) · "
          "UYARLA (tek somut araç/repo adı var, lisans+kurulum raporu ya da uyarlama gerekir; AL'dan şüphe edersen UYARLA) · ÖĞREN (fikir/pratik/araç listesi/zaten kurulu bir şeyin tanıtımı, "
          "ya da adlar eksik ama konu Claude Code/ajan: mevcut kural/skill ile karşılaştırılır; şüphede ELE değil ÖĞREN) · "
          "ELE (yalnız: konu dışı, tamamen içeriksiz ya da ücretli SaaS/hizmet reklamı). Her video için TEK satır, sekmeyle ayrılmış: URL<TAB>KARAR<TAB>neden (≤150 karakter)<TAB>önerilen iş (≤80 karakter, yoksa -). Başka metin yazma.\n\n")


def karar(parca):
    """parca: [(url, baslik, sure, ozet)] → {url: (karar, neden, is)} Haiku ile."""
    o, _ = haiku(KRITER + "\n\n".join(f"## {u} · {b}\n{z[:900]}" for u, b, s, z in parca))
    d = {}
    for ln in o.splitlines():
        c = ln.strip().lstrip("#").strip().split("\t")
        if len(c) >= 3 and c[1].strip().upper() in ("AL", "UYARLA", "ÖĞREN", "OGREN", "ELE"):
            d[c[0].strip()] = (c[1].strip().upper().replace("OGREN", "ÖĞREN"), c[2].strip(), c[3].strip() if len(c) > 3 else "-")
    return d


def video(satir, zincir):
    k, i = satir; r = {"k": k, "id": i, "url": URL[k] % i}; t0 = time.time()
    with KILIT:
        while ram() >= 88:
            time.sleep(10)
    solo = ram() >= 85  # RAM ≥%85 → N=1
    if solo:
        TEK.acquire()
    try:
        rc, s = yeniden(["video", "ozet", r["url"]], 240); l = s.splitlines()
        if rc != 0 or not l:
            r["hata"] = "ozet rc%s %s" % (rc, s[-120:].replace("\n", " ")); return r
        vid = re.match(r"(\S+) ·", l[0]).group(1) if " · " in l[0] else i
        r["vid"] = vid; r["baslik"] = (l[0].split(" · ")[1] if " · " in l[0] else "?")[:90]
        m = re.search(r"süre ([\d:]+) · (\d+) segment", s); r["sure"] = m.group(1) if m else "?"
        d = K / vid; sj = d / "segmentler.jsonl"; gq = d / "groq.txt"
        if int(m.group(2) if m else 0) == 0:
            ta = time.time()  # OCR/kare/link derinliği yok: yalnız ses→Groq (paket 23 sn → 11 sn)
            yeniden([str(R / "tools/video/.venv/Scripts/python.exe"), str(R / ".kos/kopru/video764_asr.py"), vid], 200, 2, R / "tools/video")
            r["asr_sn"] = round(time.time() - ta)
        metin = ""
        if sj.is_file() and sj.stat().st_size:
            metin = " ".join(json.loads(x)["metin"] for x in sj.read_text(encoding="utf-8").splitlines() if x.strip())
        elif gq.is_file():
            metin = " ".join(x.partition("\t")[2] for x in gq.read_text(encoding="utf-8").splitlines())
        desc = ""
        try:
            desc = (json.load(open(d / "meta.json", encoding="utf-8")).get("description") or "")[:1200]
        except Exception:
            pass
        r["karakter"] = len(metin)
        if not (metin.strip() or desc.strip()):
            (O / f"{vid}.ozet.txt").write_text("(içeriksiz: ses/metin/açıklama boş)", encoding="utf-8"); r["model"] = "yok"
        else:
            g = f"BAŞLIK: {r['baslik']}\nAÇIKLAMA: {desc}\nMETİN: {metin[:24000]}"
            o = ozet(g, r["baslik"], zincir, r)
            if o is None:
                r["hata"] = "ozet zinciri düştü " + ",".join(r.get("ozet_log", [])); return r
            (O / f"{vid}.ozet.txt").write_text(o, encoding="utf-8")
        (O / f"{vid}.meta.json").write_text(json.dumps({k_: r[k_] for k_ in ("url", "baslik", "sure", "model") if k_ in r}, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        r["hata"] = f"{type(e).__name__} {e}"[:150]
    finally:
        if solo:
            TEK.release()
        r["sn"] = round(time.time() - t0)
    return r


def liste():
    return [tuple(x.split()) for x in LISTE.read_text(encoding="utf-8").splitlines() if re.match(r"^(r|p|y|yt|w) \S+$", x)]


def islenen():
    s = TSV.read_text(encoding="utf-8") if TSV.is_file() else ""
    return s


def sirada():
    t = islenen(); h = HATA.read_text(encoding="utf-8") if HATA.is_file() else ""
    return [(k, i) for k, i in liste() if i not in t and not (O / f"{i}.ozet.txt").is_file() and i not in h
            and not any(i in p.name for p in O.glob(f"*{i}*.ozet.txt"))]


PARTI = R / ".kos/kopru/ogren/video-764-parti.tsv"


def kararla():
    """Özeti hazır, kararı yok videoları 10'arlı Haiku'ya karar verdirip video-764.tsv'ye ekler; {karar: sayı}."""
    t = islenen(); bek = []
    for f in sorted(O.glob("*.meta.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        if m["url"] not in t:
            bek.append((m["url"], m["baslik"], m["sure"], (O / (f.name[:-10] + ".ozet.txt")).read_text(encoding="utf-8")))
    say = {}
    for a in range(0, len(bek), 10):
        pr = bek[a:a + 10]
        try:
            d = karar(pr)
        except Exception as e:
            HATA.open("a", encoding="utf-8").write(f"karar\t{pr[0][0]}\t{type(e).__name__} {str(e)[:100]}\n"); continue
        with TSV.open("a", encoding="utf-8") as f:
            for u, b, s, _ in pr:
                if u in d:
                    f.write(f"{u}\t{b}\t{s}\t{d[u][0]}\t[Haiku ön-karar] {d[u][1]}\t{d[u][2]}\n"); say[d[u][0]] = say.get(d[u][0], 0) + 1
    return say


def tum(n):
    """kos n: 754 bitene (ya da Haiku tavanına) dek n'lik partiler; her parti sonu video-764-parti.tsv satırı."""
    if not PARTI.is_file():
        PARTI.write_text("parti\tvideo/dk\thalka dağılımı\tHaiku çağrı\tHaiku $\tkarar\n", encoding="utf-8")
    no = len(PARTI.read_text(encoding="utf-8").splitlines())
    while sirada() and HK["cagri"] < HAIKU_TAVAN:
        s0 = dict(SAY); c0 = HK["cagri"]; u0 = HK["usd"]
        ok, hata, dk = kos(n)
        dag = {k: SAY[k] - s0.get(k, 0) for k in SAY if SAY[k] - s0.get(k, 0)}
        kd = kararla()
        with PARTI.open("a", encoding="utf-8") as f:
            f.write(f"{no}\t{ok / dk:.2f} ({ok} ok/{hata} hata)\t{dag}\t{HK['cagri'] - c0}\t{HK['usd'] - u0:.3f}\t{kd}\n"); no += 1
    print("TUM BITTI kalan", len(sirada()), "haiku", HK, flush=True)


def kos(n, ids=None):
    sat = [(k, i) for k, i in liste() if ids and i in ids] if ids else sirada()[:n]
    zincir = modeller(); print("zincir", zincir, flush=True)
    t0 = time.time(); ok = 0; hata = 0
    with ThreadPoolExecutor(3) as ex:
        for r in ex.map(lambda s: video(s, zincir), sat):
            (O / "kos.jsonl").open("a", encoding="utf-8").write(json.dumps(r, ensure_ascii=False) + "\n")
            if r.get("hata"):
                hata += 1
                with HATA.open("a", encoding="utf-8") as f:
                    f.write(f"{r['id']}\t{r['url']}\t{r['hata']}\n")
            else:
                ok += 1
            print(r["id"], r.get("model"), r.get("sn"), r.get("hata", ""), flush=True)
    dk = (time.time() - t0) / 60
    print(f"BITTI ok {ok} hata {hata} {dk:.1f} dk · {ok / dk:.2f} video/dk · halka {SAY} · haiku {HK}", flush=True)
    return ok, hata, dk


def kapi():
    """Kalite kapısı: pilot 10 videonun kayıtlı girdisi yeni zincirle yeniden özetlenir, Haiku karar verir; pilot kararıyla kıyas."""
    zincir = modeller(); print("zincir", zincir, flush=True)
    pilot = {ln.split("\t")[0]: ln.split("\t")[3] for ln in TSV.read_text(encoding="utf-8").splitlines()[1:]}
    parca, ayni = [], 0
    for g in sorted(O.glob("*.girdi.txt")):
        girdi = g.read_text(encoding="utf-8"); vid = g.name[:-10]
        u = next((u for u in pilot if vid.replace("ig-", "") in u), None)
        r = {}; o = ozet(girdi, re.search(r"BAŞLIK: (.*)", girdi).group(1) if "BAŞLIK:" in girdi else "", zincir, r)
        print(vid, r.get("model"), r.get("ozet_log", ""), flush=True)
        if o and u:
            (O / "kapi").mkdir(exist_ok=True); (O / "kapi" / f"{vid}.ozet.txt").write_text(o, encoding="utf-8"); parca.append((u, vid, "", o))
    d = karar(parca)
    for u, vid, _, _ in parca:
        k = d.get(u, ("?",))[0]; ayni += k == pilot[u]
        print(vid, "yeni", k, "pilot", pilot[u], "OK" if k == pilot[u] else "FARK", flush=True)
    print(f"KAPI {ayni}/{len(pilot)} özet {len(parca)} halka {SAY} haiku {HK}", flush=True)


def parti(n):
    t = islenen(); out = []
    meta = {}
    for f in O.glob("*.meta.json"):
        vid = f.name[:-10]; m = json.loads(f.read_text(encoding="utf-8"))
        meta[vid] = m
    for vid, m in meta.items():
        if m["url"] in t:
            continue
        out.append(f"## {m['url']} · {m['baslik']} · {m['sure']}\n{(O / (vid + '.ozet.txt')).read_text(encoding='utf-8')[:900]}")
        if len(out) >= n:
            break
    p = O / "parti.txt"; p.write_text("\n\n".join(out), encoding="utf-8"); print(len(out), "video →", p)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "kos":
        kos(int(a[1]), a[a.index("--ids") + 1].split(",")) if "--ids" in a else tum(int(a[1]))
    elif a[0] == "kapi":
        kapi()
    elif a[0] == "parti":
        parti(int(a[1]))
    else:
        print("sirada", len(sirada()), "hata", len(HATA.read_text(encoding="utf-8").splitlines()) if HATA.is_file() else 0)
