"""ARAC-BUL-2 adım 1-2: arac-indir-2.tsv 'bulunamadi' adlarını video bağlamıyla ücretsiz havuza sınıflat, aday adı düzelt, gh/npm/pypi ile çöz, çözülenleri clone --depth 1 + gitleaks/semgrep.
Çıktı: .kos/kopru/rapor/arac-bul-2.tsv (ad, sinif, aday, link, durum, boyut, tarama, kanit). Önbellek: .kos/kopru/arac-bul-2-onbellek.json (kaldığı yerden).
Sınıflar: bulundu · uygulama · komut · ocr · bilinmiyor. Kullanım: python tools/arac_bul_2.py [--indir]"""
import csv, difflib, json, os, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arac_indir_1 as ai  # noqa: E402
import ucretsiz_havuz  # noqa: E402

KOK = ai.KOK
DERIN = os.path.join(KOK, "docs", "video-tarama", "derin")
GIRDI = os.path.join(ai.RAPOR, "arac-indir-2.tsv")
CIKTI = os.path.join(ai.RAPOR, "arac-bul-2.tsv")
ONBELLEK = os.path.join(KOK, ".kos", "kopru", "arac-bul-2-onbellek.json")
GH = re.compile(r"github\.com/([A-Za-z0-9][\w.-]{0,38})/([A-Za-z0-9][\w.-]{1,60})", re.I)
SINIFLAR = {"repo", "paket", "uygulama", "site", "komut", "ocr"}


def kelimeler(t):
    return [norm(w) for w in re.findall(r"[A-Za-z0-9._@/-]+", t) if len(norm(w)) >= 3]


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def eslesir(k, metin):
    for w in kelimeler(metin):
        if w == k or (len(k) >= 4 and (w.startswith(k) or difflib.SequenceMatcher(None, k, w).ratio() >= 0.8)):
            return True
    return False


def baglam(ad, videolar):
    k = norm(ad)
    kons, ekr, ipucu, baslik = [], [], [], ""
    for v in videolar[:6]:
        p = os.path.join(DERIN, v + ".json")
        if not os.path.isfile(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        baslik = baslik or (d.get("meta") or {}).get("baslik", "")
        ek = [str(e.get("t", "")) for e in d.get("ekran") or [] if isinstance(e, dict)]
        tr = [str(s.get("t", "")) for s in d.get("transkript") or [] if isinstance(s, dict)]
        for o, r in GH.findall("\n".join(ek + tr + [str(x) for x in d.get("linkler") or []])):
            if f"{o}/{r}" not in ipucu:
                ipucu.append(f"{o}/{r}")
        if len(k) >= 3:
            for i, t in enumerate(tr):
                if len(kons) < 2 and eslesir(k, t):
                    kons.append(" ".join(tr[max(0, i - 2):i + 3])[:320])
            for i, t in enumerate(ek):
                if len(ekr) < 2 and eslesir(k, t):
                    ekr.append(" | ".join(ek[max(0, i - 2):i + 3])[:200])
    return {"ad": ad, "baslik": baslik[:80], "konusma": kons, "ekran": ekr, "gh_ipucu": ipucu[:6]}


ISTEM = """Her kayıt, bir YouTube videosundan OCR/konuşma çözümüyle çıkmış, bozuk olabilen bir araç adıdır; kayıtta videonun bağlamı var.
Her kayıt için karar ver: "sinif": repo (GitHub reposu) | paket (npm/pypi/brew paketi) | uygulama (masaüstü/mobil uygulama) | site (web servisi) | komut (araç değil; CLI komutu/özellik/ayar) | ocr (anlamsız OCR artığı/kırpık, düzeltilemez).
"aday": düzeltilmiş gerçek ad ("sahip/repo" biçiminde ise yaz; bilinmiyorsa yalnız ad; sınıf komut/ocr ise boş). Yalnız bağlamdan ya da kesin bildiğin gerçek bir araçtan düzelt, uydurma.
"kanit": kararı destekleyen bağlamdan BİREBİR ≤100 karakter alıntı (yoksa boş).
YALNIZ JSON dizisi döndür: [{"ad":"<kayıttaki ad aynen>","sinif":"...","aday":"...","kanit":"..."}]
Kayıtlar:
"""


def sinifla(grup, onb):
    bekleyen = [g for g in grup if g["ad"] not in onb]
    if not bekleyen:
        return
    metin = ISTEM + json.dumps(bekleyen, ensure_ascii=False, indent=0)
    y, kol, log = ucretsiz_havuz.cagir("ozet", metin, max_tokens=3500)
    if y is None:
        print("havuz boş", log[:2], flush=True)
        return
    m = re.search(r"\[.*\]", y, re.S)
    try:
        for o in json.loads(m.group(0)):
            if isinstance(o, dict) and o.get("ad") in {g["ad"] for g in bekleyen}:
                onb[o["ad"]] = {"sinif": o.get("sinif", ""), "aday": str(o.get("aday") or ""), "kanit": str(o.get("kanit") or "")[:100], "model": kol}
    except (ValueError, AttributeError, TypeError):
        print("ayrıştırılamadı", kol, flush=True)


def temiz(ad):
    a = re.sub(r"(?i)readme$|@latest$", "", ad.strip())
    if "@" in a[1:]:
        a = a[0] + a[1:].split("@")[0]
    return a.strip("-_. ")


def yakin(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


ARA_KILIT = threading.Lock()
ARA_ONB = os.path.join(KOK, ".kos", "kopru", "arac-bul-2-ara.json")
ARA = json.load(open(ARA_ONB, encoding="utf-8")) if os.path.isfile(ARA_ONB) else {}


def gh_ara(q, n=8):
    """gh search API sınırı 30/dk: tek kilit, ~2.3 sn aralık, hata/sınırda bekleyip yeniden dene; sonuç diske önbelleklenir"""
    k = f"{q}|{n}"
    if k in ARA:
        return ARA[k]
    for deneme in range(4):
        with ARA_KILIT:
            rc, o = ai.calis(["gh", "search", "repos", q, "--match", "name", "--sort", "stars", "--limit", str(n), "--json", "fullName,stargazersCount,description"], 40)
            time.sleep(2.3)
        if rc == 0:
            try:
                ARA[k] = json.loads(o or "[]")
                json.dump(ARA, open(ARA_ONB, "w", encoding="utf-8"), ensure_ascii=False)
                return ARA[k]
            except ValueError:
                pass
        time.sleep(20 * (deneme + 1))
    return []


def gh_ara_genis(q, n=6):
    """ad eşleşmesi şartı olmadan (OCR bozuk adlar için) arama; aynı kilit/önbellek"""
    k = f"genis:{q}|{n}"
    if k in ARA:
        return ARA[k]
    for deneme in range(3):
        with ARA_KILIT:
            rc, o = ai.calis(["gh", "search", "repos", q, "--sort", "stars", "--limit", str(n), "--json", "fullName,stargazersCount,description"], 40)
            time.sleep(2.3)
        if rc == 0:
            try:
                ARA[k] = json.loads(o or "[]")
                json.dump(ARA, open(ARA_ONB, "w", encoding="utf-8"), ensure_ascii=False)
                return ARA[k]
            except ValueError:
                pass
        time.sleep(20 * (deneme + 1))
    return []


def npm_repo(n):
    rc, o = ai.calis(["npm", "view", n, "repository.url"], 40)
    m = GH.search(o) if rc == 0 else None
    return f"{m.group(1)}/{re.sub(r'(.git)?$', '', m.group(2))}" if m else ""


def cozum(ad, aday, ipucu):
    """aday → (gh bilgisi, kaynak) | (None, '')"""
    if "@claude-plugins-official" in ad:
        d = ai.gh_goruntule("anthropics/claude-plugins-official")
        if d:
            return d, "marketplace"
    adaylar = [a for a in dict.fromkeys([aday, temiz(aday), ad, temiz(ad)]) if a and len(norm(a)) >= 4]
    for a in adaylar:
        if a.count("/") == 1 and not a.startswith("@"):
            d = ai.gh_goruntule(a)
            if d:
                return d, "gh-aday"
    for a in adaylar:
        for h in ipucu:
            if yakin(h.split("/")[1], a.split("/")[-1]) >= 0.8:
                d = ai.gh_goruntule(h)
                if d:
                    return d, "gh-video-ipucu"
    for a in adaylar:
        h = npm_repo(a) if (a.startswith("@") or "/" not in a) else ""
        if h:
            d = ai.gh_goruntule(h)
            if d:
                return d, "npm-repo"
    for a in adaylar:
        q = a.split("/")[-1]
        for d in gh_ara(q):
            if yakin(d["fullName"].split("/")[1], q) >= 0.85 and d["stargazersCount"] >= 5:
                v = ai.gh_goruntule(d["fullName"])
                if v:
                    return v, "gh-arama"
    return None, ""


PICK = """Her kayıt için bir video bağlamı ve GitHub arama adayları var. Bağlama göre doğru repo ADAY NUMARASINI seç; hiçbiri uymuyorsa null.
Yalnız ad benzerliği değil, açıklamanın bağlamla uyumu da şart (eğitim videosunda anılan proje adı için aynı adlı en çok yıldızlı repo kabul edilir). YALNIZ JSON dizisi: [{"ad":"<kayıttaki ad aynen>","secim":<numara|null>}]
Kayıtlar:
"""


def sec(bekleyen, bag, onb):
    """çözülemeyenler: gh arama adayları (temiz ad + LLM adayı) → havuz seçer; ad benzerliği ≥0.6 şart"""
    kayit = []
    for r, o in bekleyen:
        q = {temiz(r["ad"]), temiz(o["aday"]).split("/")[-1]}
        cs = {}
        for x in q:
            if len(norm(x)) >= 4:
                for d in gh_ara(x, 6):
                    if d["stargazersCount"] >= 2 and max(yakin(d["fullName"].split("/")[1], y) for y in q if y) >= 0.6:
                        cs[d["fullName"]] = d
        if cs:
            kayit.append((r, o, list(cs.values())[:6]))
    sonuc = {}
    for i in range(0, len(kayit), 6):
        grup = kayit[i:i + 6]
        gov = [{"ad": r["ad"], "baslik": bag.get(r["ad"], {}).get("baslik", ""), "konusma": bag.get(r["ad"], {}).get("konusma", [])[:1], "adaylar": [f"{j}: {c['fullName']} ({c['stargazersCount']}*) {str(c.get('description') or '')[:90]}" for j, c in enumerate(cs)]} for r, o, cs in grup]
        y, kol, log = ucretsiz_havuz.cagir("ozet", PICK + json.dumps(gov, ensure_ascii=False), max_tokens=1500)
        m = re.search(r"\[.*\]", y or "", re.S)
        try:
            for o in json.loads(m.group(0)):
                for r, _, cs in grup:
                    if o.get("ad") == r["ad"] and isinstance(o.get("secim"), int) and 0 <= o["secim"] < len(cs):
                        sonuc[r["ad"]] = cs[o["secim"]]["fullName"]
        except (ValueError, AttributeError, TypeError):
            print("sec ayrıştırılamadı", kol, flush=True)
    return sonuc


def paket_link(ad):
    n = ad.split("@")[0] if not ad.startswith("@") else ad
    rc, o = ai.calis(["npm", "view", n, "name", "version"], 40)
    if rc == 0 and o.strip():
        return "https://www.npmjs.com/package/" + n
    rc, o = ai.calis([sys.executable, "-I", "-c", "import json,sys,urllib.request as u;print(u.urlopen('https://pypi.org/pypi/%s/json'%sys.argv[1],timeout=20).status)", n], 40)
    return "https://pypi.org/project/" + n if rc == 0 and "200" in o else ""


def main():
    with open(GIRDI, encoding="utf-8") as f:
        satirlar = [r for r in csv.DictReader(f, delimiter="\t") if r["durum"] == "bulunamadi"]
    onb = json.load(open(ONBELLEK, encoding="utf-8")) if os.path.isfile(ONBELLEK) else {}
    bag = {}
    for r in satirlar:
        if len(norm(r["ad"])) < 3:
            onb.setdefault(r["ad"], {"sinif": "ocr", "aday": "", "kanit": f"ad {len(norm(r['ad']))} harf", "model": "kural"})
        else:
            bag[r["ad"]] = baglam(r["ad"], [v for v in r["video"].split(",") if v])
    grup = [list(bag.values())[i:i + 8] for i in range(0, len(bag), 8)]
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(lambda g: sinifla(g, onb), grup))
    json.dump(onb, open(ONBELLEK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("sınıflanan", len(onb), "/", len(satirlar), flush=True)
    cikti = []
    iscozum = []
    for r in satirlar:
        o = onb.get(r["ad"])
        if not o:
            cikti.append([r["ad"], "bilinmiyor", "", "", "-", "-", "-", "sınıflanamadı", r["video"]])
        elif o["sinif"] in ("repo", "paket"):
            iscozum.append((r, o))
        else:
            cikti.append([r["ad"], {"komut": "komut", "ocr": "ocr", "uygulama": "uygulama", "site": "uygulama"}.get(o["sinif"], "bilinmiyor"), o["aday"], "", "-", "-", "-", o["kanit"], r["video"]])
    def coz(x):
        r, o = x
        ipucu = bag.get(r["ad"], {}).get("gh_ipucu", [])
        d, k = cozum(r["ad"], o["aday"], ipucu)
        return r, o, d, k, (paket_link(o["aday"] or r["ad"]) if d is None and o["sinif"] == "paket" else "")
    with ThreadPoolExecutor(6) as ex:
        sonuc = list(ex.map(coz, iscozum))
    bos = [(r, o) for r, o, d, k, pl in sonuc if d is None and not pl]
    secilen = sec(bos, bag, onb)
    print("seçim ile çözülen", len(secilen), "/", len(bos), flush=True)
    sonuc = [(r, o, ai.gh_goruntule(secilen[r["ad"]]), "gh-arama+secim", pl) if (d is None and r["ad"] in secilen) else (r, o, d, k, pl) for r, o, d, k, pl in sonuc]
    tekil = {}
    for r, o, d, k, pl in sonuc:
        if d:
            tekil.setdefault(d["nameWithOwner"].lower(), {"d": d, "kaynak": k, "video": r["video"], "ad": r["ad"], "kanit": o["kanit"]})
        elif pl:
            cikti.append([r["ad"], "bulundu", o["aday"], pl, "paket-linki", "-", "-", o["kanit"], r["video"]])
        else:
            cikti.append([r["ad"], "bilinmiyor", o["aday"], "", "-", "-", "-", o["kanit"], r["video"]])
    print("çözülen tekil repo", len(tekil), flush=True)
    if "--indir" in sys.argv:
        with ThreadPoolExecutor(3) as ex:
            islenen = list(ex.map(ai.isle, [{"d": t["d"], "kaynak": t["kaynak"], "video": t["video"]} for t in tekil.values()]))
        for t, s in zip(tekil.values(), islenen):
            cikti.append([t["ad"], "bulundu", s[0], "https://github.com/" + s[0], s[2], s[3], s[4], t["kanit"], t["video"]])
            print(t["ad"], "->", s[0], s[2], flush=True)
    else:
        for t in tekil.values():
            cikti.append([t["ad"], "bulundu", t["d"]["nameWithOwner"], "https://github.com/" + t["d"]["nameWithOwner"], "indirilmedi", f"{t['d']['diskUsage']//1024}MB", "-", t["kanit"], t["video"]])
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ad", "sinif", "aday", "link", "durum", "boyut", "tarama", "kanit", "video"])
        w.writerows(cikti)
    import collections
    print("DAĞILIM", collections.Counter(c[1] for c in cikti), flush=True)


if __name__ == "__main__":
    main()
