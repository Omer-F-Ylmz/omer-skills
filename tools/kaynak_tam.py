"""KAYNAK-TAM-1: docs/video-tarama/derin/*.json → .kos/kopru/rapor/kaynak-tam.tsv (+ yontem/tarif kartları).
  python tools/kaynak_tam.py det                 # kural tabanlı çıkarım (ücretsiz, model yok)
  python tools/kaynak_tam.py llm [--sinir N] [--kod K,K] [--is 4]   # ücretsiz model: prompt · yöntem · akış · tarif (önbellekli, devam eder)
  python tools/kaynak_tam.py birlestir           # det + llm + site-tam.tsv → kaynak-tam.tsv, kartlar, aksiyon.tsv
Model yalnız ucuz_alt zinciri (:free); alıntı transkript/ekran/açıklama metninde birebir yoksa satır dogru=hayir (kütüphaneye girmez).
kare_aciklama alanı kayıplı (U+FFFD) olduğundan alıntı kaynağı sayılmaz."""
import json
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import ucuz_alt as U

DERIN = KOK / "docs/video-tarama/derin"
RAPOR = KOK / ".kos/kopru/rapor"
ONB = RAPOR / "kaynak-tam-llm"
BASLIK = "kod\ttur\tzaman\tkaynak\tdeger\tdogru\talinti"

ALAN = r"(?:com|io|ai|app|dev|co|org|net|so|sh|tools|xyz|gg|tv|me|studio|design|page|cloud|run|new|build|to|fm)"
RE_URL = re.compile(r"https?://[^\s\"'<>)]+", re.I)
RE_ALAN = re.compile(rf"\b(?:[a-z0-9][a-z0-9-]*\.)+{ALAN}\b(?:/[^\s\"'<>)]*)?", re.I)
RE_REPO = re.compile(r"github\.com/([\w.-]+/[\w.-]+)", re.I)
RE_KOM = re.compile(r"^\s*[$>]?\s*((?:npx|npm|pnpm|yarn|pip3?|uv|uvx|git|claude|brew|winget|curl|python3?|docker|bun|cargo|ffmpeg|yt-dlp)\s+\S.{2,160})$", re.I | re.M)
RE_HEX = re.compile(r"#(?:[0-9a-fA-F]{6})\b")
RE_HESAP = re.compile(r"(?<![\w.])@([A-Za-z0-9_.]{3,30})\b")
RE_RAKAM = re.compile(r"(\$\s?\d[\d,.]*\s?[kKmMbB]?\b|\b\d[\d,.]*\s?(?:%|percent|x\b|times|million|billion|bin|milyon|dollars?|dolar|hours?|saat|minutes?|dakika|seconds?|saniye|days?|gün|fps|gb|mb|k\b))", re.I)
MODELLER = ("claude", "opus", "sonnet", "haiku", "gpt-?\\d[\\w.-]*", "chatgpt", "codex", "gemini", "veo ?\\d?", "kimi", "deepseek", "minimax", "glm",
            "qwen", "llama", "mistral", "grok", "sora", "runway", "kling", "seedance", "higgsfield", "midjourney", "flux", "stable diffusion",
            "elevenlabs", "whisper", "nano banana", "imagen", "luma", "pika", "hailuo", "wan ?\\d?", "ltx", "suno", "udio", "heygen", "cursor",
            "windsurf", "copilot", "lovable", "bolt", "v0", "figma", "blender", "after effects", "premiere", "davinci", "capcut", "remotion",
            "hyperframes", "three\\.?js", "gsap", "lottie", "rive", "spline", "comfyui", "ollama", "openrouter", "n8n", "zapier", "make\\.com",
            "notion", "obsidian", "supabase", "vercel", "firebase", "canva", "framer", "webflow", "playwright", "puppeteer")
RE_MODEL = re.compile(r"\b(" + "|".join(MODELLER) + r")\b", re.I)
FONTLAR = ("inter", "geist", "satoshi", "playfair display", "space grotesk", "roboto", "poppins", "montserrat", "helvetica", "neue montreal",
           "general sans", "clash display", "cabinet grotesk", "instrument serif", "dm sans", "manrope", "syne", "fraunces", "jetbrains mono",
           "sf pro", "söhne", "sohne", "gt walsheim", "ibm plex", "lora", "oswald", "bebas neue", "archivo", "outfit", "sora", "urbanist")
RE_FONT = re.compile(r"\b(" + "|".join(re.escape(f) for f in FONTLAR) + r")\b(?=[^.]{0,40}\bfont|\s*\(?font)|\bfont(?:s|-family)?[: ]+(?:called |named |is |= )?([A-Z][\w]+(?: [A-Z][\w]+)?)", re.I)
RE_PROMPT_ACK = re.compile(r"\b(prompt|istem|talimat)\b", re.I)
RE_AKIS = re.compile(r"\b(step \d|first(?:ly)?,|then,|next,|finally,|after that|adım \d|önce\b|sonra\b|ardından|ilk olarak)", re.I)


def yukle(f):
    return json.loads(Path(f).read_text(encoding="utf-8"))


def dak(s):
    s = int(float(s))
    return f"{s // 60}:{s % 60:02d}"


def birimler(d):
    """(zaman, kaynak, metin) listesi — alıntı yalnız bunlardan alınır"""
    u = [(dak(s["b"]), "konusma", s["t"]) for s in d["transkript"] if s.get("t")]
    gor = set()
    for e in d["ekran"]:
        t = (e.get("t") or "").strip()
        if len(t) >= 3 and t not in gor:
            gor.add(t)
            u.append(("kare " + e.get("k", "?").split(".")[0], "ekran", t))
    a = (d["meta"].get("aciklama") or "")
    if a:
        u.append(("-", "aciklama", a))
    u += [("-", "liste", str(x)) for x in (d.get("linkler") or [])] + [("-", "komut", str(x)) for x in (d.get("komutlar") or [])]
    return u


def temiz(s):
    return " ".join(str(s).replace("\t", " ").split())[:600]


def det_satirlar(d):
    kod, S, gor = d["kod"], [], set()

    def ekle(tur, z, k, deger, alinti):
        a = (tur, deger.lower() if tur in ("link", "model", "hex") else deger)
        if a in gor:
            return
        gor.add(a)
        S.append((kod, tur, z, k, temiz(deger), "evet", temiz(alinti)))
    for z, k, m in birimler(d):
        for x in RE_URL.findall(m):
            ekle("link", z, k, x.rstrip(".,"), m)
        for x in RE_ALAN.findall(m):
            if "@" not in x and not re.match(r"^\d", x) and k != "liste":
                ekle("link", z, k, x.rstrip("."), m)
        for x in RE_REPO.findall(m):
            ekle("repo", z, k, x, m)
        for x in RE_KOM.findall(m):
            ekle("komut", z, k, x.strip(), m)
        if k == "komut":
            ekle("komut", z, k, m, m)
        for x in RE_HEX.findall(m):
            ekle("hex", z, k, x, m)
        if k != "konusma":
            for x in RE_HESAP.findall(m):
                ekle("hesap", z, k, "@" + x, m)
        for x in RE_MODEL.findall(m):
            ekle("model", z, k, x.lower(), m)
        for g in RE_FONT.findall(m):
            f = g[0] or g[1]
            if f:
                ekle("font", z, k, f, m)
        if k == "konusma":
            r = RE_RAKAM.search(m)
            if r:
                ekle("rakam", z, k, r.group(1), m)
    y = d["meta"].get("yukleyen")
    if y:
        ekle("hesap", "-", "meta", y, y)
    a = d["meta"].get("aciklama") or ""
    for m in re.finditer(r"(?im)^\s*(?:prompt|istem)\s*[:：]\s*(.{20,})$", a):
        ekle("prompt", "-", "aciklama", m.group(1), m.group(0))
    return S


def cmd_det():
    RAPOR.mkdir(parents=True, exist_ok=True)
    n, sayi = 0, {}
    with open(RAPOR / "kaynak-tam-det.tsv", "w", encoding="utf-8", newline="\n") as o:
        o.write(BASLIK + "\n")
        for f in sorted(DERIN.glob("*.json")):
            for s in det_satirlar(yukle(f)):
                o.write("\t".join(s) + "\n")
                n += 1
                sayi[s[1]] = sayi.get(s[1], 0) + 1
    print("det", n, sayi)


# ---------------- LLM ----------------
KONULAR = "animasyon|3d|ui-tasarim|web-kod|video-kurgu|gorsel-uretim|ses-muzik|ajan-kod|otomasyon|prompt-hilesi|pazarlama|diger"
SEMA = (
    '{"prompt":[{"zaman":"","alinti":"videoda söylenen/ekranda yazan PROMPT metni, birebir"}],'
    '"yontem":[{"konu":"' + KONULAR + '","ad":"kısa ad","ne":"1 cümle","alinti":"birebir"}],'
    '"akis":[{"n":1,"zaman":"","ne":"kişinin yaptığı adım","alinti":"birebir"}],'
    '"tarif":null,"yazi":"araç/ayar/komut/font/palet/rakam gibi kalanları düz metin tek satır"}'
)
TARIF = ('"tarif" yalnız NASIL YAPILIR videosuysa: {"konu":"slug","amac":"","araclar":["" ],"adimlar":[{"n":1,"zaman":"","ne":""}],'
         '"prompt_kod_ayar":"","sonuc":"","bizde":"kurulu araçlarla nasıl","daha_iyi":"","oncelik":"yuksek|orta|dusuk"}; değilse null.')
ISTEM = ("Bir kısa videonun çıkarılmış verisi aşağıda (başlık, açıklama, konuşma transkripti zamanlı, ekran OCR'ı). Görev: videodaki "
         "KAYNAKLARI çıkar: gösterilen/okunan PROMPT metinleri (tam, kısaltma yok), yöntem/teknikler, kişinin ekranda ADIM ADIM yaptıkları, tarif. "
         "KURALLAR: yalnız veride olanı yaz; alinti alanları veriden BİREBİR kopya olsun (uydurma yok, OCR bozuksa olduğu gibi); veri yoksa boş liste. "
         "Reklam/sohbet/selam cümlelerini alma. " + TARIF + "\nYalnız şu JSON'u döndür:\n" + SEMA)


def girdi(d):
    m = d["meta"]
    t = " ".join(f"[{dak(s['b'])}] {s['t']}" for s in d["transkript"])[:14000]
    gor, seen = [], set()
    for e in d["ekran"]:
        x = (e.get("t") or "").strip()
        if len(x) >= 4 and x not in seen:
            seen.add(x)
            gor.append(f"{e.get('k', '?')[:4]}:{x}")
    ek = " | ".join(gor)[:5000]
    return f"BAŞLIK: {m.get('baslik')}\nYÜKLEYEN: {m.get('yukleyen')}\nAÇIKLAMA: {(m.get('aciklama') or '')[:2500]}\nKONUŞMA: {t}\nEKRAN: {ek}"


def nrm(s):
    return U.n(re.sub(r"\s+", " ", str(s)))


def cagir(g):
    """(json | None, kaynak). ucretsiz_havuz (haiku_tavan=0 → ücretli halka yok); JSON dönmeyen yanıt sıradaki halkaya geçer"""
    import ucretsiz_havuz
    if not getattr(ucretsiz_havuz, "_yaz_kilitli", False):  # aynı süreçteki iş parçacıkları ortak durum.<pid>.tmp'de çakışıyordu (PermissionError)
        _y = ucretsiz_havuz._yaz
        yk = threading.Lock()
        ucretsiz_havuz._yaz = lambda d: (yk.acquire(), _y(d), yk.release())[1]
        ucretsiz_havuz._yaz_kilitli = True
    ret = lambda y: None if isinstance(U.json_al(y), dict) else "JSON yok"
    y, k, log = ucretsiz_havuz.cagir("ozet", g["messages"][0]["content"], max_tokens=4000, haiku_tavan=0, dogrula=ret, zaman=120)
    o = U.json_al(y) if y else None
    return (o, k, log) if isinstance(o, dict) else (None, None, log)


def soguma_bekle():
    """Havuz boş: en yakın soğuma bitimine kadar bekle (sn). >900 sn (günlük kota) → None: iş önbelleksiz kalır, koşu sonra devam eder."""
    import ucretsiz_havuz
    now = time.time()
    t = [v - now for v in ucretsiz_havuz._durum().get("soguma", {}).values() if v > now]
    if t and min(t) > 900:
        return None
    return min(t) + 2 if t else 15


def isle(f):
    d = yukle(f)
    kod = d["kod"]
    out = ONB / f"{kod}.json"
    if out.is_file():
        return kod, "onbellek"
    metin = girdi(d)
    if len(metin) < 400:  # içerik yok: model çağrılmaz
        out.write_text(json.dumps({"kod": kod, "bos": True}), encoding="utf-8")
        return kod, "bos"
    g = U.govde(f"[kaynak_tam v1]\n{ISTEM}\n\n<veri>\n{metin}\n</veri>", [])
    for deneme in range(10):
        o, m, log = cagir(g)
        if o is not None:
            break
        print(f"  {kod} deneme{deneme + 1} {log}", flush=True)
        b = soguma_bekle()
        if b is None:
            return kod, "kota"
        time.sleep(b)
    else:
        return kod, "hata"
    corp = nrm(" ".join(x[2] for x in birimler(d)))
    o["kod"], o["model"] = kod, m

    def dg(a):
        a = nrm(a)
        return len(a) >= 8 and a in corp
    for k in ("prompt", "yontem", "akis"):
        for x in o.get(k) or []:
            if isinstance(x, dict):
                x["dogru"] = "evet" if dg(x.get("alinti", "")) else "hayir"
    out.write_text(json.dumps(o, ensure_ascii=False), encoding="utf-8")
    return kod, "ok"


def cmd_llm(arg):
    sinir, kodlar, is_ = None, None, 4
    while arg:
        b, v, *arg = arg
        if b == "--sinir":
            sinir = int(v)
        elif b == "--kod":
            kodlar = set(v.split(","))
        elif b == "--is":
            is_ = int(v)
    ONB.mkdir(parents=True, exist_ok=True)
    fl = [f for f in sorted(DERIN.glob("*.json")) if not kodlar or f.stem in kodlar]
    fl = [f for f in fl if not (ONB / f"{f.stem}.json").is_file()]
    if sinir:
        fl = fl[:sinir]
    say, kilit, t0 = {}, threading.Lock(), time.time()

    def is1(f):
        try:
            k, s = isle(f)
        except Exception as e:
            k, s = f.stem, "hata:" + type(e).__name__
        with kilit:
            say[s] = say.get(s, 0) + 1
            top = sum(say.values())
            if top % 25 == 0:
                print(f"{top}/{len(fl)} {say} {time.time() - t0:.0f}sn", flush=True)
    with ThreadPoolExecutor(is_) as ex:
        list(ex.map(is1, fl))
    print("BITTI", say, f"{time.time() - t0:.0f}sn", flush=True)


# ---------------- birleştir ----------------
def cmd_birlestir():
    satir = (RAPOR / "kaynak-tam-det.tsv").read_text(encoding="utf-8").splitlines()[1:]
    satir = [s.split("\t") for s in satir]
    P, Y, T = [], {}, []
    for f in sorted(ONB.glob("*.json")):
        o = json.loads(f.read_text(encoding="utf-8"))
        if o.get("bos"):
            continue
        kod = o["kod"]
        gecer = bool(RE_PROMPT_ACK.search(" ".join(x[2] for x in birimler(yukle(DERIN / f"{kod}.json")))))
        for p in o.get("prompt") or []:
            if isinstance(p, dict) and p.get("alinti"):
                if not gecer or len(str(p["alinti"])) < 60:  # parça-transkript ≠ prompt: videoda "prompt" sözü + ≥60 karakter şart
                    p["dogru"] = "hayir"
                satir.append([kod, "prompt", str(p.get("zaman", "")), "llm", "", p.get("dogru", "hayir"), temiz(p["alinti"])])
                P.append((kod, p))
        for y in o.get("yontem") or []:
            if isinstance(y, dict) and y.get("alinti"):
                satir.append([kod, "yontem", "", "llm", temiz(f"{y.get('konu')}: {y.get('ad')} — {y.get('ne')}"), y.get("dogru", "hayir"), temiz(y["alinti"])])
                Y.setdefault(y.get("konu") if y.get("konu") in KONULAR.split("|") else "diger", []).append((kod, y))
        for a in o.get("akis") or []:
            if isinstance(a, dict) and a.get("alinti"):
                satir.append([kod, "akis", str(a.get("zaman", "")), "llm", temiz(f"{a.get('n')}. {a.get('ne')}"), a.get("dogru", "hayir"), temiz(a["alinti"])])
        if o.get("yazi"):
            satir.append([kod, "yazi", "", "llm", temiz(o["yazi"]), "-", ""])
        if isinstance(o.get("tarif"), dict):
            T.append((kod, o["tarif"]))
    site = RAPOR / "site-tam.tsv"
    if site.is_file():
        for s in site.read_text(encoding="utf-8").splitlines()[1:]:
            c = s.split("\t")
            if len(c) >= 3:
                for v in c[2].split(","):
                    satir.append([v.strip(), "site", "-", c[7] if len(c) > 7 else "-", temiz(c[0]), "evet", temiz(c[1])])
    with open(RAPOR / "kaynak-tam.tsv", "w", encoding="utf-8", newline="\n") as o:
        o.write(BASLIK + "\n")
        for s in satir:
            o.write("\t".join(s) + "\n")
    sayi = {}
    for s in satir:
        sayi[s[1]] = sayi.get(s[1], 0) + 1
    # kartlar: yöntem (konuya göre) + prompt kütüphanesi
    ky = KOK / "kartlar/yontem"
    kt = KOK / "kartlar/tarif"
    ky.mkdir(parents=True, exist_ok=True)
    kt.mkdir(parents=True, exist_ok=True)
    for d_ in (ky, kt):  # önceki çalıştırmanın ürettiği kartlar (yeniden üretilir)
        for f_ in d_.glob("*.md"):
            f_.unlink()
    for konu, L in Y.items():
        L = [x for x in L if x[1].get("dogru") == "evet"]
        if L:
            (ky / f"{konu}.md").write_text(f"# Yöntemler — {konu}\n\n" + "\n".join(
                f"- **{y.get('ad')}** ({k}): {y.get('ne')} — «{temiz(y['alinti'])[:200]}»" for k, y in L) + "\n", encoding="utf-8")
    pk = [(k, p) for k, p in P if p.get("dogru") == "evet"]
    (ky / "prompt-kutuphanesi.md").write_text("# Prompt kütüphanesi (ekranda/konuşmada geçen, doğrulanmış)\n\n" + "\n".join(
        f"## {k} {p.get('zaman', '')}\n{temiz(p['alinti'])}\n" for k, p in pk), encoding="utf-8")
    ak = ["tarif\tkod\tproje\toncelik"]
    for kod, t in T:
        slug = re.sub(r"[^a-z0-9]+", "-", str(t.get("konu") or kod).lower()).strip("-")[:50] or kod
        ad = f"{slug}-{kod}"[:80]
        a = "\n".join(f"{x.get('n')}. [{x.get('zaman', '')}] {x.get('ne')}" for x in (t.get("adimlar") or []) if isinstance(x, dict))
        (kt / f"{ad}.md").write_text(
            f"# {t.get('konu')} ({kod})\n\n**Amaç:** {t.get('amac')}\n**Araçlar:** {', '.join(map(str, t.get('araclar') or []))}\n\n"
            f"**Adımlar**\n{a}\n\n**Prompt/kod/ayar:** {t.get('prompt_kod_ayar')}\n**Sonuç:** {t.get('sonuc')}\n"
            f"**Bizde (öneri, modelden):** {t.get('bizde')}\n**Daha iyi (öneri):** {t.get('daha_iyi')}\n", encoding="utf-8")
        if t.get("oncelik") in ("yuksek", "orta"):
            ak.append(f"{ad}\t{kod}\tomer-skills (Desktop seçer)\t{t.get('oncelik')}")
    (RAPOR / "aksiyon.tsv").write_text("\n".join(ak) + "\n", encoding="utf-8")
    print("kaynak-tam.tsv", len(satir), sayi, "| yontem kartı", len(list(ky.glob('*.md'))) - 1, "| prompt dogru", len(pk), "/", len(P), "| tarif", len(T))


def cmd_dogrula():
    """tarif adım alıntıları → videonun konuşma/ekran(kare OCR)/açıklama metninde birebir var mı (model yok)"""
    sat = ["kod\tadim\talinti_konusma\talinti_kare\talinti_aciklama\tyok\tkare_dogrulu"]
    kare_ok = tam = 0
    for f in sorted(ONB.glob("*.json")):
        o = json.loads(f.read_text(encoding="utf-8"))
        t = o.get("tarif")
        if o.get("bos") or not isinstance(t, dict):
            continue
        h = {"konusma": "", "ekran": "", "aciklama": ""}
        for _, kay, m in birimler(yukle(DERIN / f"{o['kod']}.json")):
            if kay in h:
                h[kay] += " " + nrm(m)
        c = {"konusma": 0, "ekran": 0, "aciklama": 0, "yok": 0}
        ad = [x for x in (t.get("adimlar") or []) if isinstance(x, dict)]
        for x in ad:
            q = nrm(x.get("alinti") or "")
            bul = [k for k in h if len(q) >= 8 and q in h[k]]
            for k in bul or ["yok"]:
                c[k] += 1
        ok = "evet" if c["ekran"] else "hayir"
        kare_ok += ok == "evet"
        tam += bool(ad) and c["yok"] == 0
        sat.append(f"{o['kod']}\t{len(ad)}\t{c['konusma']}\t{c['ekran']}\t{c['aciklama']}\t{c['yok']}\t{ok}")
    (RAPOR / "tarif-dogrula.tsv").write_text("\n".join(sat) + "\n", encoding="utf-8")
    print("tarif", len(sat) - 1, "| kareyle (ekran OCR) desteklenen", kare_ok, "| tüm adımı kaynakta bulunan", tam)


def cmd_kapsam(n=30):
    """30 videoluk kapsam kapısı: ham metindeki URL ana makinesi/repo/komut, kaynak-tam.tsv'de o videoya ait satırlarda var mı (kaçırılan ≤%2)"""
    import random
    tsv = {}
    for s in (RAPOR / "kaynak-tam.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        c = s.split("\t")
        tsv[c[0]] = tsv.get(c[0], "") + " " + nrm(" ".join(c[4:]))
    derin = sorted(f.stem for f in DERIN.glob("*.json"))
    llm = {f.stem for f in ONB.glob("*.json")}
    ornek = random.Random(3).sample(derin, n)
    top = kac = 0
    sat = ["kod\ttur\tdeger"]
    for kod in ornek:
        ham = " ".join(m for _, _, m in birimler(yukle(DERIN / f"{kod}.json")))
        gt = {("link", re.sub(r"^https?://(www\.)?", "", u).split("/")[0].lower().rstrip(".,;")) for u in RE_URL.findall(ham)}
        gt |= {("repo", r.lower()) for r in RE_REPO.findall(ham)}
        gt |= {("komut", k.strip()[:60]) for k in RE_KOM.findall(ham)}
        for t, v in sorted(gt):
            top += 1
            if nrm(v) not in tsv.get(kod, ""):
                kac += 1
                sat.append(f"{kod}\t{t}\t{v}")
    eksik = [k for k in derin if k not in tsv]
    icerik = [k for k in derin if k not in llm and (yukle(DERIN / f"{k}.json")["transkript"] or yukle(DERIN / f"{k}.json")["ekran"])]
    (RAPOR / "kapsam-kapisi.tsv").write_text("\n".join(sat) + "\n\n# tsvde hiç satırı olmayan: " + ",".join(eksik) + "\n# içerik var, llm çıktısı yok: " + ",".join(icerik) + "\n", encoding="utf-8")
    print(f"örnek {n} video | doğruluk kümesi {top} | kaçırılan {kac} (%{100 * kac / max(top, 1):.1f}) | tsvde satırsız video {len(eksik)} {eksik} | içerik var llm yok {len(icerik)} {icerik}")


if __name__ == "__main__":
    c, *a = sys.argv[1:] or ["?"]
    {"det": cmd_det, "llm": lambda: cmd_llm(a), "birlestir": cmd_birlestir, "dogrula": cmd_dogrula, "kapsam": cmd_kapsam}.get(c, lambda: print(__doc__))()
