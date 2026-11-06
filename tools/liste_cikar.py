"""LISTE-CIKAR-1: derin/*.json + derin-2/*.json -> kalem çıkarma. det = deterministik (link/repo/komut), llm = ücretsiz havuz, kaldığı yerden sürer.
Kullanım: python -I tools/liste_cikar.py det | llm [--parti N] [--en-cok M] | durum"""
import json, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

K = Path(r"C:\Projeler\omer-skills")
C = K / ".kos/kopru/ogren/liste-cikar-1"
C.mkdir(parents=True, exist_ok=True)
DET, LLM, HATA = C / "det.jsonl", C / "llm.jsonl", C / "llm-hata.jsonl"
URL = re.compile(r"https?://[^\s)>\]\"']+")
GH = re.compile(r"github\.com/([\w.-]+/[\w.-]+)")
KOM = re.compile(r"(npx|npm i|npm install|pip install|pipx|uv tool install|uvx|claude mcp add|/plugin|git clone|brew install|winget install)\s+[^\n]{0,120}")


def dosyalar():
    out = {}
    for d in ("derin", "derin-2", "derin-3"):
        for f in sorted((K / "docs/video-tarama" / d).glob("*.json")):
            out.setdefault(f.stem, f)
    return out


def oku(f):
    return json.loads(f.read_text(encoding="utf-8", errors="replace"))


def det():
    n = 0
    with open(DET, "w", encoding="utf-8") as o:
        for vid, f in dosyalar().items():
            d = oku(f)
            m = d.get("meta") or {}
            acik = m.get("aciklama") or ""
            tr = " ".join(x.get("t", "") for x in d.get("transkript") or [])
            urls = sorted(set((d.get("linkler") or []) + URL.findall(acik)))
            urls = [u.rstrip(".,") if isinstance(u, str) else str(u) for u in urls]
            komut = [k.get("t", k) if isinstance(k, dict) else k for k in (d.get("komutlar") or [])]
            komut += [x.group(0).strip() for x in KOM.finditer(acik + " " + tr)]
            repos = sorted({g.group(1).removesuffix(".git") for u in urls for g in [GH.search(u)] if g})
            o.write(json.dumps({"id": vid, "baslik": m.get("baslik"), "yukleyen": m.get("yukleyen"), "urls": urls, "repos": repos,
                                "komut": komut[:15], "tr_uzun": len(tr)}, ensure_ascii=False) + "\n")
            n += 1
    print("det", n)


def girdi(vid, f):
    d = oku(f)
    m = d.get("meta") or {}
    tr = " ".join(x.get("t", "") for x in d.get("transkript") or [])
    ekran = " | ".join(dict.fromkeys(x.get("t", "") for x in d.get("ekran") or []))
    return (f"[{vid}] BASLIK: {m.get('baslik')} | KANAL: {m.get('yukleyen')}\nACIKLAMA: {(m.get('aciklama') or '')[:600]}\n"
            f"LINKLER: {' '.join((d.get('linkler') or [])[:15])}\nEKRAN: {ekran[:500]}\nKONUSMA: {tr[:1500]}")


ISTEM = """Asagidaki videolarin her birinde GECEN arac/skill/plugin/MCP/CLI/repo/kutuphane/site/model/ui-kutuphane/prompt-kaynagi/varlik/yontem adlarini cikar.
Yalniz metinde acikca gecenler; tahmin yok, uydurma yok. Genel kelime (ChatGPT'ye benzer olsa bile) metinde geciyorsa yaz. Her kalem icin tur sec:
arac | site-ucretsiz | site-ilham | ui-kutuphane | prompt | varlik | kutuphane | yontem. Link metinde varsa ekle.
ONEMLI: Marka/sirket/platform adlari, yazilim ve model surumleri, programlama dilleri, font adlari, kutuphane/AI modeli adlari, hashtag icindeki arac adlari DAHIL; kisa ve bilinen adlari ATLAMA; ekran/OCR ve KARE aciklamasindaki adlari da al.
CIKTI: yalniz JSON dizisi, her video icin {"id":"...","kalemler":[{"ad":"","tur":"","link":""}]}; kalem yoksa kalemler bos dizi.

"""


def llm(parti, en_cok, is_parcacigi=3):
    sys.path.insert(0, str(K / "tools"))
    import ucretsiz_havuz as H
    biten = set()
    if LLM.exists():
        for l in LLM.read_text(encoding="utf-8").splitlines():
            try:
                biten.add(json.loads(l)["id"])
            except Exception:
                pass
    bekle = [(v, f) for v, f in dosyalar().items() if v not in biten][:en_cok]
    partiler = [bekle[i:i + parti] for i in range(0, len(bekle), parti)]
    kilit, say = threading.Lock(), [0, 0]

    def is_(p):
        istem = ISTEM + "\n\n".join(girdi(v, f) for v, f in p)
        try:
            for deneme in range(8):
                met, kim, log = H.cagir("kolay", istem, max_tokens=3500, zaman=120, etiket="liste-cikar-1")
                if met:
                    break
                time.sleep(15 * (deneme + 1))
            if not met:
                raise ValueError("bos:" + str(log)[:200])
            met = re.sub(r"^```\w*|```$", "", met.strip(), flags=re.M).strip()
            arr = json.loads(met[met.index("["):met.rindex("]") + 1])
            by = {a.get("id"): a for a in arr if isinstance(a, dict)}
            with kilit:
                with open(LLM, "a", encoding="utf-8") as o:
                    for v, _ in p:
                        if v in by:
                            o.write(json.dumps({"id": v, "kalemler": by[v].get("kalemler") or [], "model": kim}, ensure_ascii=False) + "\n")
                            say[0] += 1
                say[1] += 1
                if say[1] % 10 == 0:
                    print(f"parti {say[1]}/{len(partiler)} video {say[0]}", flush=True)
        except Exception as e:
            with kilit:
                with open(HATA, "a", encoding="utf-8") as o:
                    o.write(json.dumps({"ids": [v for v, _ in p], "hata": str(e)[:300]}, ensure_ascii=False) + "\n")

    with ThreadPoolExecutor(is_parcacigi) as ex:
        list(ex.map(is_, partiler))
    print("bitti", say)


# --- llm2: doğrudan sağlayıcı halkaları, uyku yok; hata → parti kuyruğa döner, başka halka alır ---
HALKA = [("groq", "openai/gpt-oss-120b", 1), ("groq", "qwen/qwen3.8-27b", 1), ("groq", "openai/gpt-oss-20b", 1), ("gemini", "gemini-3.5-flash-lite", 1),
         ("gemini", "gemini-3-flash-preview", 1), ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b", 8), ("nvidia", "meta/muse-glimmer-30b", 2), ("haiku", "claude-haiku-5-5", 14)]
LOG = C / "llm.log"
TAVAN_KARAKTER = 12000


def girdi2(vid, f):
    """Tam metin: konuşma TAVAN_KARAKTER'lik parçalara bölünür; parça anahtarı vid, vid~1, ... (liste döner)."""
    d = oku(f)
    m = d.get("meta") or {}
    tr = " ".join(x.get("t", "") for x in d.get("transkript") or [])
    ekran = " | ".join(dict.fromkeys(x.get("t", "") for x in d.get("ekran") or []))
    kare = d.get("kare_aciklama") or ""
    kare = kare if isinstance(kare, str) else json.dumps(kare, ensure_ascii=False)
    out = []
    for k, i in enumerate(range(0, max(len(tr), 1), TAVAN_KARAKTER)):
        a = vid if k == 0 else f"{vid}~{k}"
        ust = (f"[{a}] BASLIK: {m.get('baslik')} | KANAL: {m.get('yukleyen')}\nACIKLAMA: {(m.get('aciklama') or '')[:3000]}\n"
               f"LINKLER: {' '.join((d.get('linkler') or [])[:30])}\nEKRAN: {ekran[:20000]}\nKARE: {kare[:4000]}\n") if k == 0 else f"[{a}] BASLIK: {m.get('baslik')} (konusma devami)\n"
        out.append((a, ust + f"KONUSMA: {tr[i:i + TAVAN_KARAKTER]}"))
    return out


def llm2(en_cok, cikti=None, ters=False):
    global LLM, HALKA
    if cikti:
        LLM = C / cikti
    if ters:
        HALKA = HALKA[::-1]
    import queue
    sys.path.insert(0, str(K / "tools"))
    import ucretsiz_havuz as H
    biten = {json.loads(l)["id"] for l in LLM.read_text(encoding="utf-8").splitlines() if l.strip()} if LLM.exists() else set()
    bekle = [(v, f) for v, f in dosyalar().items() if v not in biten][:en_cok]
    q, parti, cur = queue.Queue(), [], 0
    for v, f in bekle:
        for a, g in girdi2(v, f):
            if parti and cur + len(g) > TAVAN_KARAKTER:
                q.put({"p": parti, "g": [], "den": set()}); parti, cur = [], 0
            parti.append((a, g)); cur += len(g)
    if parti:
        q.put({"p": parti, "g": [], "den": set()})
    kilit, say, t0 = threading.Lock(), [0, 0, 0], time.time()
    E = {(a, b): next(e for e in H.ENT if e.prov == a and e.model == b) for a, b, _ in HALKA if a != "haiku"}
    olu = set()
    HK = [0, 0]

    def yaz_hata(b, neden):
        with kilit, open(HATA, "a", encoding="utf-8") as o:
            o.write(json.dumps({"ids": [v for v, _ in b["p"]], "hata": neden, "den": sorted(b["den"])}, ensure_ascii=False) + "\n")

    def isci(h):
        e = E.get(h[:2])
        while not q.empty():
            try:
                b = q.get_nowait()
            except queue.Empty:
                return
            if h[:2] in b["den"]:
                if len(b["den"]) >= len(HALKA) - len(olu):
                    yaz_hata(b, "tum-halka:" + ";".join(b["g"][-4:]))
                else:
                    q.put(b); time.sleep(1)
                continue
            try:
                istem_ = ISTEM + "\n\n".join(g for _, g in b["p"])
                met = H._haiku(istem_) if e is None else H._istek(e, istem_, 6000, 100)
                if e is None:
                    with kilit:
                        say[2] += 0; HK[0] += 1; HK[1] += len(istem_)
                met = re.sub(r"^```\w*|```$", "", met.strip(), flags=re.M).strip()
                arr = json.loads(met[met.index("["):met.rindex("]") + 1])
                by = {a.get("id"): a for a in arr if isinstance(a, dict)}
            except Exception as x:
                kod = getattr(x, "kod", type(x).__name__); print(time.strftime("%H:%M:%S"), h[1], kod, str(x)[:70].replace(chr(10), " "), flush=True)
                b["den"].add(h[:2]); b["g"].append(f"{h[1]}:{kod}"); q.put(b)
                if kod in (402, 429, 404):
                    with kilit:
                        olu.add(h[:2]) if kod in (402, 404) else None
                    if kod == 429:
                        time.sleep(20)
                    if kod in (402, 404):
                        return
                continue
            gec = [v for v, _ in b["p"] if v in by and by[v].get("kalemler")]
            with kilit:
                with open(LLM, "a", encoding="utf-8") as o:
                    for v in gec:
                        o.write(json.dumps({"id": v.split("~")[0], "kalemler": by[v]["kalemler"], "model": f"{h[0]}/{h[1]}"}, ensure_ascii=False) + "\n")
                onceki = say[0]; say[0] += len(gec); say[1] += 1
                if say[0] // 50 > onceki // 50:
                    s_ = f"{time.strftime('%H:%M:%S')} islenen {say[0]} parti {say[1]} {round(say[0] / (time.time() - t0) * 3600)} video/saat"
                    print(s_, flush=True)
                    with open(LOG, "a", encoding="utf-8") as o:
                        o.write(s_ + "\n")
            bos = [(v, g) for v, g in b["p"] if v not in gec]
            if bos:  # boş/eksik dönenler tek tek, başka halka
                with kilit:
                    say[2] += len(bos)
                for it in bos:
                    q.put({"p": [it], "g": [], "den": {h[:2]} if len(b["p"]) == 1 else set()})
    ths = []
    for h in HALKA:
        for _ in range(h[2]):
            t = threading.Thread(target=isci, args=(h,)); t.start(); ths.append(t)
    for t in ths:
        t.join()
    print("bitti", say, "haiku cagri/karakter", HK, "olu", olu, "kuyruk", q.qsize())


def durum():
    t = len(dosyalar())
    b = len(set(json.loads(l)["id"] for l in LLM.read_text(encoding="utf-8").splitlines())) if LLM.exists() else 0
    print(f"toplam {t} llm-biten {b} kalan {t - b}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["det"]:
        det()
    elif a[:1] == ["llm2"]:
        llm2(int(a[a.index("--en-cok") + 1]) if "--en-cok" in a else 10**9, a[a.index("--cikti") + 1] if "--cikti" in a else None, "--ters" in a)
    elif a[:1] == ["llm"]:
        g = lambda k, v: int(a[a.index(k) + 1]) if k in a else v
        llm(g("--parti", 4), g("--en-cok", 10**9))
    else:
        durum()
