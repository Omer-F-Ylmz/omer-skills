"""TERS kapısı koşucusu (docs/ters/kapi-tasarim.md). Hedefler: docs/ters/kapi/hedefler.json (elle ground truth).
  python tools/ters/kapi_kos.py          → docs/ters/kapi/sonuc.md + sonuc.json; --dene → yalnız 1 hedef (kuru deneme)
Kollar: skill (SKILL.md + prob/REA kanıtı + ham kaynak) vs zemin (yalnız ham kaynak), aynı yazar model. Hakem: iki aile ücretsiz bulut, ikisi onaylamazsa madde 0.
Bulut çağrı tavanı yazar 80 / hakem 130 (sayaç + önbellek CIKTI altında); anahtar değerleri basılmaz."""
import functools, hashlib, http.server, json, os, random, re, subprocess, sys, threading, time, urllib.request
from pathlib import Path
from PIL import Image, ImageChops

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "ters"))
from probe import probe  # noqa: E402
sys.path.insert(0, str(KOK / "tools")); import ucretsiz_havuz as HAVUZ  # noqa: E402

DIZ = KOK / "docs/ters/kapi"
CIKTI = Path(os.environ["TEMP"]) / "ters-kapi"
TAVAN = {"yazar": 80, "hakem": 130}  # hakem: yalnız ücretsiz aileler
HAIKU_TAVAN = 0  # üçüncü hakem (Haiku) kapalı
TEKRAR = (1, 2)
YARGIC = ("meta", "openai", "mistral", "google", "alibaba")  # ilk iki yanıt veren aile hakem (Cloudflare llama-3.3-70b + Groq gpt-oss-120b; kota/soğumada sıradaki aile); kullanılanlar sonuca yazılır
KULLANILAN = {}
DUSEN = {}  # hata veren hakem ailesi → soğuma bitişi (SOGUMA sn atlanır; geçici hata aileyi koşu boyunca düşürmesin)
SOGUMA = 150
SKILL = (KOK / "skills/tersine/SKILL.md").read_text(encoding="utf-8")


def ram():
    import psutil
    return psutil.virtual_memory().percent


class RamYok(Exception): pass


def ram_bekle():  # DEVAM-KURALI: RAM ≥%88 iken tarayıcı adımı yok; 10 dk × en çok 3 bekle, sonra koşu yarım kalır
    for _ in range(3):
        if ram() < 88: return
        time.sleep(600)
    if ram() >= 88: raise RamYok("RAM %88 üstünde kaldı")


def onbellekli(tur, anahtar, uret):  # önbellek + tür başına çağrı sayacı (tavan aşılırsa koşu durur)
    (CIKTI / "onbellek").mkdir(parents=True, exist_ok=True)
    o = CIKTI / "onbellek" / (hashlib.sha1((tur + anahtar).encode()).hexdigest() + ".json")
    if o.exists(): return json.loads(o.read_text(encoding="utf-8"))["y"]
    sy = CIKTI / f"sayac-{tur}.json"
    n = json.loads(sy.read_text())["n"] if sy.exists() else 0
    if n >= TAVAN[tur]: raise SystemExit(f"{tur} çağrı tavanı")
    sy.write_text(json.dumps({"n": n + 1}))
    y = uret()
    if y: o.write_text(json.dumps({"y": y}, ensure_ascii=False), encoding="utf-8")
    elif tur == "hakem": sy.write_text(json.dumps({"n": n}))  # hata dönen hakem çağrısı tavana sayılmaz
    return y


def sonnet(istem):  # yazar: plan kotası, araçsız tek tur; hata/boş → "" (hedef atlanır)
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    try:
        p = subprocess.run(["claude", "-p", "--model", "claude-sonnet-5-5", "--output-format", "json", "--max-turns", "1", "--tools", "", "--setting-sources", ""],
                           input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=400, creationflags=0x08000000, cwd=CIKTI, env=env)
        j = json.loads(p.stdout); y = (j.get("result") or "").strip()
    except Exception as e:
        print("sonnet hata", type(e).__name__, flush=True); return ""
    if j.get("is_error") or (len(y) < 200 and re.search(r"(?i)usage limit|limit reached|resets? (at|in)", y)):
        print("sonnet hata", y[:80], flush=True); return ""
    return y


def yazar(istem): return onbellekli("yazar", istem, lambda: sonnet(istem))


def yargic(aile, istem):  # aile "anthropic" → yalnız Haiku (üçüncü hakem)
    def uret():
        y, k, log = HAVUZ.cagir("hakem", istem, max_tokens=4000, aile=aile, haiku_tavan=HAIKU_TAVAN if aile == "anthropic" else 0, etiket="tersine-kapi")
        if not y: DUSEN[aile] = time.monotonic() + SOGUMA; print("hakem hata", aile, ",".join(log), flush=True)  # bu koşuda soğumaya alınır
        return y or ""
    return onbellekli("hakem", aile + istem, uret)


def fark(a, b):
    A = Image.open(a).convert("RGB"); B = Image.open(b).convert("RGB").resize(A.size)
    d = ImageChops.difference(A, B).convert("L").point(lambda v: 255 if v > 16 else 0)
    return d.histogram()[255] / (A.size[0] * A.size[1])


def nor(s): return re.sub(r"\s+", " ", s).strip()


def ham(h, sinir=9000):
    if h["tur"] == "dotnet":
        d = Path(h["derlenmis"]).read_bytes()
        s = [x.decode() for x in re.findall(rb"[\x20-\x7e]{5,}", d)] + [x.decode("utf-16le") for x in re.findall(rb"(?:[\x20-\x7e]\x00){5,}", d)]
        return "\n".join(s)[:sinir]
    return "\n".join(f"### {k}\n{Path(k).read_text(encoding='utf-8', errors='ignore')}" for k in h["kaynaklar"])[:sinir]


def rea_kanit(h):
    if h["tur"] == "dotnet": komut = ["rea", "inspect-managed-members", h["derlenmis"], "--json"]
    else: komut = ["rea", "analyze-javascript-application", h["yol"], "--json"]
    try:
        c = subprocess.run(komut, capture_output=True, text=True, timeout=180, creationflags=0x08000000, encoding="utf-8")
        return c.stdout[:6000]
    except Exception as e:
        return f"REA hata: {type(e).__name__}"


def sunucu():
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(KOK)))
    s.RequestHandlerClass.log_message = lambda *a: None
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


def notu_yaz(h, kol, veri, r):
    site = h["tur"] == "site"
    ist = (f"{SKILL}\n\n" if kol == "skill" else "") + f"Hedef: {h['ad']} ({h['tur']}). Soru: {h['sorular']}\n\nVeri:\n{veri}\n\n" \
          "Görev: tam 5 mekanizma maddesi yaz. Her madde ayrı satırda JSON: {\"madde\":\"...\",\"dosya\":\"...\",\"alinti\":\"veride birebir geçen en çok 120 karakter\"}. " \
          f"[tekrar {r}] Önce yalnız bu 5 JSON satırı." + (" Sonra '### HTML' başlığı ve altında ```html bloğu: ekranda aynı görünümü veren tek dosyalık saf HTML/CSS/JS (harici kütüphane ve ağ yok)." if site else "")
    y = yazar(ist)
    mad = []
    for s in y.splitlines():
        s = s.strip().rstrip(",")
        if s.startswith("{"):
            try: mad.append(json.loads(s))
            except ValueError: pass
    m = re.search(r"```html\s*(.*?)```", y, re.S)
    return mad[:5], (m.group(1) if m else "")


def oyla(oylar):  # oylar: her biri 2×5 (A,B) 0/1; çoğunluk, eşitlikte 0
    return [[int(sum(o[l][i] == 1 for o in oylar) * 2 > len(oylar)) for i in range(5)] for l in range(2)]


def hakem(h, notlar, rng):
    sira = ["skill", "zemin"]; rng.shuffle(sira)  # kör: A/B rastgele
    gt = "\n".join(f"{i + 1}. {m['madde']}" for i, m in enumerate(h["maddeler"]))
    nt = lambda k: "\n".join(f"- {x.get('madde', '')}" for x in notlar[k])
    ist = (f"Referans mekanizma maddeleri ({h['ad']}):\n{gt}\n\nNot A:\n{nt(sira[0])}\n\nNot B:\n{nt(sira[1])}\n\n"
           "Her not için 5 referans maddesinin her birinin notta (aynı olgu, doğru) verilip verilmediğini 1/0 işaretle. "
           "Yalnız JSON: {\"A\":[5 sayı],\"B\":[5 sayı]}")

    def oy(aile):
        try:
            j = json.loads(re.search(r"\{.*?\}", yargic(aile, ist), re.S).group(0))
            return [(list(j[k]) + [0] * 5)[:5] for k in "AB"]
        except Exception: return None

    oylar, KULLANILAN_BU = [], set()
    for _ in range(3):  # yetmezse en yakın soğuma bitince yeniden dene
        for aile in YARGIC:
            if len(oylar) == 2: break
            if aile in KULLANILAN_BU or DUSEN.get(aile, 0) > time.monotonic(): continue
            if o := oy(aile): oylar.append(o); KULLANILAN_BU.add(aile); KULLANILAN[aile] = KULLANILAN.get(aile, 0) + 1
        bek = [t - time.monotonic() for t in DUSEN.values() if t > time.monotonic()]
        if len(oylar) == 2 or not bek: break
        time.sleep(min(bek) + 1)
    if HAIKU_TAVAN and (len(oylar) < 2 or oylar[0] != oylar[1]):  # hakemler ayrıştı ya da biri yanıtsız → Haiku üçüncü
        if o3 := oy("anthropic"): oylar.append(o3)
    if len(oylar) < 2: return None
    a, b = oyla(oylar)
    return {sira[0]: sum(a) / 5, sira[1]: sum(b) / 5}


def hedef_kos(h, port, sat, atlanan):
    d = CIKTI / h["ad"]; d.mkdir(exist_ok=True)
    corp_ham = ham(h, 10**6)
    if h["tur"] == "site":
        ram_bekle()
        kanit = json.dumps(probe(f"http://127.0.0.1:{port}/labs{h['sayfa']}", d / "orijinal"), ensure_ascii=False)[:6000]
    else: kanit = rea_kanit(h)
    veri = {"zemin": ham(h), "skill": ham(h) + "\n\n### Kanıt (prob/REA)\n" + kanit}
    for r in TEKRAR:  # tekrar: yazar örneklemesi + A/B sırası farklı tohum
        rng = random.Random(h["id"] * 10 + r); notlar, html = {}, {}
        for kol in ("skill", "zemin"): notlar[kol], html[kol] = notu_yaz(h, kol, veri[kol], r)
        c1 = hakem(h, notlar, rng) if notlar["skill"] and notlar["zemin"] else None
        if c1 is None: atlanan.append(f"{h['ad']}#{r}"); print("ATLANDI (model/tavan)", h["ad"], r, flush=True); continue
        for kol in ("skill", "zemin"):
            korpus = nor(corp_ham + veri[kol]); bul = [nor(x.get("alinti", "")) in korpus and len(nor(x.get("alinti", ""))) > 3 for x in notlar[kol]]
            c2 = sum(bul) / len(bul) if bul else 0.0; bil = [c1[kol], c2]
            c3 = None
            if h["tur"] == "site":
                f = d / f"{kol}{r}"; f.mkdir(exist_ok=True)
                if html[kol]:
                    ram_bekle(); (f / "yeniden.html").write_text(html[kol], encoding="utf-8")
                    try:
                        probe((f / "yeniden.html").as_uri(), f / "p")
                        c3 = 1 - min(1, sum(fark(d / "orijinal" / f"kare-{n}.png", f / "p" / f"kare-{n}.png") for n in (0, 50, 100)) / 3)
                    except Exception as e: print("yeniden hata", h["ad"], kol, type(e).__name__, flush=True)
                if c3 is None: c3 = 0.0
                bil.append(c3)
            sat.append({"id": h["id"], "ad": h["ad"], "tur": h["tur"], "kol": kol, "tekrar": r, "c1": c1[kol], "c2": c2, "c3": c3, "puan": sum(bil) / len(bil), "iddia": len(notlar[kol])})
            print(sat[-1], flush=True)


def ozet(sat):  # hedef başına tekrar ortalaması → kol ortalaması + eşli fark (skill−zemin) bootstrap %95 GA (hedefler üzerinden)
    ort = lambda v: sum(v) / len(v)
    pt = {(s["ad"], s["kol"]): [x["puan"] for x in sat if x["ad"] == s["ad"] and x["kol"] == s["kol"]] for s in sat}
    ad = sorted({a for a, k in pt if (a, "skill") in pt and (a, "zemin") in pt})
    if not ad: return {"ort": {"skill": 0.0, "zemin": 0.0}, "fark": 0.0, "ga": [0.0, 0.0], "tekrar_sapma": 0.0}
    sk, ze = [ort(pt[a, "skill"]) for a in ad], [ort(pt[a, "zemin"]) for a in ad]
    d = [x - y for x, y in zip(sk, ze)]; rng = random.Random(0)
    b = sorted(ort([rng.choice(d) for _ in d]) for _ in range(5000))
    ts = [abs(v[0] - v[1]) for v in pt.values() if len(v) > 1]  # aynı hedef+kol iki tekrar arası |fark| (gürültü)
    return {"ort": {"skill": ort(sk), "zemin": ort(ze)}, "fark": ort(d), "ga": [b[125], b[4874]], "tekrar_sapma": ort(ts) if ts else 0.0}


def main():
    H = json.loads((DIZ / "hedefler.json").read_text(encoding="utf-8"))["hedefler"]
    if "--dene" in sys.argv: H = H[:1]
    port = sunucu(); CIKTI.mkdir(parents=True, exist_ok=True); sat = []; atlanan = []; hatalar = []
    H.sort(key=lambda h: h["tur"] == "site")  # tarayıcısız hedefler önce (sıralama kararlı)
    for i, h in enumerate(H):
        try: hedef_kos(h, port, sat, atlanan)
        except RamYok as e:  # yarım bırak: bu ve kalan site hedefleri atlanmış sayılır, önbellek kalır
            atlanan += [x["ad"] for x in H[i:] if x["tur"] == "site"]; print("RAM", e, flush=True); break
        except Exception as e:  # bir hedefin hatası koşuyu çökertmez; o hedef hata satırı olur
            hatalar.append({"ad": h["ad"], "hata": f"{type(e).__name__}: {e}"}); atlanan.append(h["ad"]); print("hata", h["ad"], type(e).__name__, e, flush=True)
    o = ozet(sat); ort = o["ort"]
    gec = not atlanan and ort["skill"] >= 0.92 and o["ga"][0] > 0
    cagri = {p.stem[6:]: json.loads(p.read_text())["n"] for p in CIKTI.glob("sayac-*.json")}
    (DIZ / "sonuc.json").write_text(json.dumps({"satirlar": sat, **o, "gecti": gec, "atlanan": atlanan, "hatalar": hatalar, "cagri": cagri, "hakem_aileleri": KULLANILAN}, ensure_ascii=False, indent=1), encoding="utf-8")
    t = ["# TERS kapısı sonucu (Sonnet yazar, 2 tekrar)", "", "| hedef | tür | kol | tekrar | mekanizma | kanıt | yeniden | puan |", "|---|---|---|---|---|---|---|---|"]
    t += [f"| {s['ad']} | {s['tur']} | {s['kol']} | {s['tekrar']} | {s['c1']:.2f} | {s['c2']:.2f} | {'-' if s['c3'] is None else format(s['c3'], '.2f')} | {s['puan']:.2f} |" for s in sat]
    t += ["", f"Ortalama skill {ort['skill']:.3f} · zemin {ort['zemin']:.3f} · fark {o['fark']:+.3f} GA95 [{o['ga'][0]:+.3f}, {o['ga'][1]:+.3f}] · tekrar sapması {o['tekrar_sapma']:.3f} · "
          f"atlanan {len(atlanan)} {atlanan} · hata {hatalar} · çağrı {cagri} · hakem aileleri {KULLANILAN} · KAPI {'GEÇTİ' if gec else 'GEÇMEDİ'}"]
    (DIZ / "sonuc.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    print("ORT", ort, "fark", o["fark"], o["ga"], "gecti", gec)


if __name__ == "__main__":
    main()
