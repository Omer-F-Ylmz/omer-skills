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
        o = [m["id"] for m in get("https://openrouter.ai/api/v1/models")["data"] if m["id"].endswith(":free") and re.search(r"gpt-oss-120b|nemotron-3-super|gemma-4-31b", m["id"])][:1]
    except Exception:
        pass
    return [("gemini", m) for m in g] + [("groq", m) for m in q] + [("openrouter", m) for m in o]


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


def ozet(girdi, baslik, zincir, r):
    log = []
    for ad, m in zincir:
        for deneme in range(2):
            try:
                if ad == "gemini":
                    j = post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key=" + os.environ["GEMINI_API_KEY"],
                             {"contents": [{"parts": [{"text": ISTEM + "\n\n" + girdi}]}], "generationConfig": {"maxOutputTokens": 1500}}, {})
                    o = j["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    url, key = (("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY") if ad == "groq" else
                                ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY"))
                    j = post(url, {"model": m, "max_tokens": 1500, "reasoning_effort": "low", "messages": [{"role": "user", "content": ISTEM + "\n\n" + girdi}]},
                             {"Authorization": "Bearer " + os.environ[key]})
                    o = j["choices"][0]["message"]["content"]
                o = (o or "").strip()
                neden = gecerli(o, girdi, baslik) if o else "boş"
                if not neden:
                    r["model"] = f"{ad}/{m}"; return o
                log.append(f"{m}:{neden}"); break
            except Exception as e:
                c = getattr(e, "code", "")
                log.append(f"{m}:{type(e).__name__}{c}")
                if c in (429, 503):
                    time.sleep(4 * (deneme + 1))  # geri çekilme, sonra aynı model bir kez daha
                    continue
                break
    r["ozet_log"] = log
    return None


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
    print(f"BITTI ok {ok} hata {hata} {dk:.1f} dk · {ok / dk:.2f} video/dk", flush=True)


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
        kos(int(a[1]), a[a.index("--ids") + 1].split(",") if "--ids" in a else None)
    elif a[0] == "parti":
        parti(int(a[1]))
    else:
        print("sirada", len(sirada()), "hata", len(HATA.read_text(encoding="utf-8").splitlines()) if HATA.is_file() else 0)
