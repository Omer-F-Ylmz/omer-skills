"""TERS kapısı koşucusu (docs/ters/kapi-tasarim.md). Hedefler: docs/ters/kapi/hedefler.json (elle ground truth).
  python tools/ters/kapi_kos.py          → docs/ters/kapi/sonuc.md + sonuc.json
Kollar: skill (SKILL.md + prob/REA kanıtı + ham kaynak) vs zemin (yalnız ham kaynak), aynı yazar model. Hakem: iki aile ücretsiz bulut, ikisi onaylamazsa madde 0.
Bulut çağrı tavanı 60 (sayaç + önbellek CIKTI altında); anahtar değerleri basılmaz."""
import functools, hashlib, http.server, json, os, random, re, subprocess, sys, threading, time, urllib.request
from pathlib import Path
from PIL import Image, ImageChops

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools" / "ters"))
from probe import probe  # noqa: E402

DIZ = KOK / "docs/ters/kapi"
CIKTI = Path(os.environ["TEMP"]) / "ters-kapi"
TAVAN = 60
YAZAR = ["openrouter/google/gemma-4-31b-it:free"]
YARGIC = [["openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"],
          ["groq/llama-3.3-70b-versatile", "gemini/gemini-2.5-flash"]]
SKILL = (KOK / "skills/tersine/SKILL.md").read_text(encoding="utf-8")


def ram():
    import psutil
    return psutil.virtual_memory().percent


def ram_bekle():  # DEVAM-KURALI: RAM ≥%88 iken tarayıcı adımı yok
    for _ in range(60):
        if ram() < 88: return
        time.sleep(30)
    raise SystemExit("RAM %88 üstünde kaldı")


def anahtar():
    if os.environ.get("OMNIROUTE_KEY"): return os.environ["OMNIROUTE_KEY"]
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


def llm(modeller, istem, max_tokens=4000):
    (CIKTI / "onbellek").mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1((modeller[0] + istem).encode()).hexdigest()
    o = CIKTI / "onbellek" / (h + ".json")
    if o.exists(): return json.loads(o.read_text(encoding="utf-8"))["y"]
    sy = CIKTI / "sayac.json"
    for m in modeller:
        for deneme in range(2):
            n = json.loads(sy.read_text())["n"] if sy.exists() else 0
            if n >= TAVAN: raise SystemExit("bulut çağrı tavanı")
            sy.write_text(json.dumps({"n": n + 1}))
            q = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", method="POST",
                data=json.dumps({"model": m, "messages": [{"role": "user", "content": istem}], "max_tokens": max_tokens,
                                 "reasoning_effort": "none"}).encode(),
                headers={"content-type": "application/json", "authorization": "Bearer " + anahtar(), "user-agent": "curl/8"})
            try:
                y = json.load(urllib.request.urlopen(q, timeout=240))["choices"][0]["message"]["content"] or ""
                if y.strip():
                    o.write_text(json.dumps({"m": m, "y": y}, ensure_ascii=False), encoding="utf-8"); return y
            except Exception as e:
                print("llm hata", m, type(e).__name__, getattr(e, "code", ""), flush=True); time.sleep(5)
    return ""


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
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(KOK / "labs")))
    s.RequestHandlerClass.log_message = lambda *a: None
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


def notu_yaz(h, kol, veri):
    site = h["tur"] == "site"
    ist = (f"{SKILL}\n\n" if kol == "skill" else "") + f"Hedef: {h['ad']} ({h['tur']}). Soru: {h['sorular']}\n\nVeri:\n{veri}\n\n" \
          "Görev: tam 5 mekanizma maddesi yaz. Her madde ayrı satırda JSON: {\"madde\":\"...\",\"dosya\":\"...\",\"alinti\":\"veride birebir geçen en çok 120 karakter\"}. " \
          "Önce yalnız bu 5 JSON satırı." + (" Sonra '### HTML' başlığı ve altında ```html bloğu: ekranda aynı görünümü veren tek dosyalık saf HTML/CSS/JS (harici kütüphane ve ağ yok)." if site else "")
    y = llm(YAZAR, ist)
    mad = []
    for s in y.splitlines():
        s = s.strip().rstrip(",")
        if s.startswith("{"):
            try: mad.append(json.loads(s))
            except ValueError: pass
    m = re.search(r"```html\s*(.*?)```", y, re.S)
    return mad[:5], (m.group(1) if m else "")


def hakem(h, notlar, rng):
    sira = ["skill", "zemin"]; rng.shuffle(sira)  # kör: A/B rastgele
    gt = "\n".join(f"{i + 1}. {m['madde']}" for i, m in enumerate(h["maddeler"]))
    nt = lambda k: "\n".join(f"- {x.get('madde', '')}" for x in notlar[k])
    ist = (f"Referans mekanizma maddeleri ({h['ad']}):\n{gt}\n\nNot A:\n{nt(sira[0])}\n\nNot B:\n{nt(sira[1])}\n\n"
           "Her not için 5 referans maddesinin her birinin notta (aynı olgu, doğru) verilip verilmediğini 1/0 işaretle. "
           "Yalnız JSON: {\"A\":[5 sayı],\"B\":[5 sayı]}")
    sonuc = {"skill": [1] * 5, "zemin": [1] * 5}
    for aile in YARGIC:
        y = llm(aile, ist)
        m = re.search(r"\{.*?\}", y, re.S)
        try: j = json.loads(m.group(0))
        except Exception: j = {"A": [0] * 5, "B": [0] * 5}  # hakem okunamadı → güvenli taraf 0
        for harf, kol in (("A", sira[0]), ("B", sira[1])):
            v = (list(j.get(harf, [])) + [0] * 5)[:5]
            sonuc[kol] = [a & int(b == 1) for a, b in zip(sonuc[kol], v)]
    return {k: sum(v) / 5 for k, v in sonuc.items()}


def main():
    H = json.loads((DIZ / "hedefler.json").read_text(encoding="utf-8"))["hedefler"]
    port = sunucu(); CIKTI.mkdir(parents=True, exist_ok=True); sat = []
    for h in H:
        d = CIKTI / h["ad"]; d.mkdir(exist_ok=True); rng = random.Random(h["id"])
        corp_ham = ham(h, 10**6)
        if h["tur"] == "site":
            ram_bekle()
            kanit = json.dumps(probe(f"http://127.0.0.1:{port}{h['sayfa']}", d / "orijinal"), ensure_ascii=False)[:6000]
        else: kanit = rea_kanit(h)
        veri = {"zemin": ham(h), "skill": ham(h) + "\n\n### Kanıt (prob/REA)\n" + kanit}
        notlar, html = {}, {}
        for kol in ("skill", "zemin"): notlar[kol], html[kol] = notu_yaz(h, kol, veri[kol])
        c1 = hakem(h, notlar, rng)
        for kol in ("skill", "zemin"):
            korpus = nor(corp_ham + veri[kol]); bul = [nor(x.get("alinti", "")) in korpus and len(nor(x.get("alinti", ""))) > 3 for x in notlar[kol]]
            c2 = sum(bul) / len(bul) if bul else 0.0; bil = [c1[kol], c2]
            c3 = None
            if h["tur"] == "site":
                f = d / kol; f.mkdir(exist_ok=True)
                if html[kol]:
                    ram_bekle(); (f / "yeniden.html").write_text(html[kol], encoding="utf-8")
                    try:
                        probe((f / "yeniden.html").as_uri(), f / "p")
                        c3 = 1 - min(1, sum(fark(d / "orijinal" / f"kare-{n}.png", f / "p" / f"kare-{n}.png") for n in (0, 50, 100)) / 3)
                    except Exception as e: print("yeniden hata", h["ad"], kol, type(e).__name__, flush=True)
                if c3 is None: c3 = 0.0
                bil.append(c3)
            sat.append({"id": h["id"], "ad": h["ad"], "tur": h["tur"], "kol": kol, "c1": c1[kol], "c2": c2, "c3": c3, "puan": sum(bil) / len(bil), "iddia": len(notlar[kol])})
            print(sat[-1], flush=True)
    ort = {k: sum(s["puan"] for s in sat if s["kol"] == k) / len([s for s in sat if s["kol"] == k]) for k in ("skill", "zemin")}
    mn2 = min(s["c2"] for s in sat if s["kol"] == "skill")
    gec = ort["skill"] >= 0.70 and mn2 >= 0.5 and ort["skill"] > ort["zemin"]
    (DIZ / "sonuc.json").write_text(json.dumps({"satirlar": sat, "ort": ort, "min_kanit_skill": mn2, "gecti": gec,
        "bulut_cagri": json.loads((CIKTI / "sayac.json").read_text())["n"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    t = ["# TERS kapısı sonucu (tek koşu)", "", "| hedef | tür | kol | mekanizma | kanıt | yeniden | puan |", "|---|---|---|---|---|---|---|"]
    t += [f"| {s['ad']} | {s['tur']} | {s['kol']} | {s['c1']:.2f} | {s['c2']:.2f} | {'-' if s['c3'] is None else format(s['c3'], '.2f')} | {s['puan']:.2f} |" for s in sat]
    t += ["", f"Ortalama skill {ort['skill']:.3f} · zemin {ort['zemin']:.3f} · skill min kanıt {mn2:.2f} · KAPI {'GEÇTİ' if gec else 'GEÇMEDİ'}"]
    (DIZ / "sonuc.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    print("ORT", ort, "min_kanit", mn2, "gecti", gec)


if __name__ == "__main__":
    main()
