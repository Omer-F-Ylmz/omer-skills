"""KURULUM-TOPLU-2: kurulum_coz2 sonrası açıkları kapatır. python tools/kurulum_tamamla.py
1) bozuk (dict) değerleri düzeltir  2) kota yüzünden sorgulanmamış + 404 veren kalemleri GitHub aramasıyla çözer (0 token)
3) hâlâ sorgulanmamış kalan videoları modelle tekrar dener (3 tur, turlar arası bekleme)  4) indir  5) sayım -> .kos/kopru/kurulum-tamamla-ozet.json"""
import json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_coz2 as K  # noqa: E402

LOG = os.path.join(KOK, ".kos", "kopru", "kurulum-tamamla.log")
OZET = os.path.join(KOK, ".kos", "kopru", "kurulum-tamamla-ozet.json")


def yaz(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    open(LOG, "a", encoding="utf-8").write(s + "\n")


def nrm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def en_iyi():
    son, sonnet = {}, {}
    for l in open(K.COZ, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(l)
        except Exception:
            continue
        v = o.get("video")
        es = son.setdefault(v, {})
        for kalem, d in (o.get("eslesme") or {}).items():
            if o.get("kaynak") == "sonnet":
                sonnet.setdefault(v, {})[kalem] = d
                continue
            e = es.get(kalem)
            if e is None or (str(e).startswith("bilinmiyor") and not str(d).startswith("bilinmiyor")):
                es[kalem] = d
    for v, es in sonnet.items():
        son.setdefault(v, {}).update(es)
    return son


def ekle(video, eslesme, kaynak, kanit=None):
    with open(K.COZ, "a", encoding="utf-8") as f:
        f.write(json.dumps({"video": video, "kaynak": kaynak, "rapor_var": True, "eslesme": eslesme, "kanit": kanit or {}}, ensure_ascii=False) + "\n")


def duzelt_bozuk(son):
    n = 0
    for v, es in son.items():
        yeni = {}
        for kalem, d in es.items():
            if isinstance(d, dict):
                deger = d.get("deger") or next((x for x in d.values() if isinstance(x, str)), "")
                yeni[kalem] = deger
            elif isinstance(d, str) and re.match(r"^(gh/|github\.com/)", d):
                yeni[kalem] = "gh:" + re.sub(r"^(gh/|github\.com/)", "", d)
        if yeni:
            ekle(v, yeni, "duzeltme"); n += len(yeni)
    yaz("bozuk duzeltildi", n)


def yok_404():
    s = set()
    for l in open(K.TOPLU, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(l)
        except Exception:
            continue
        if o.get("durum") == "REPO-YOK":
            s.add(o.get("repo_istenen"))
    return s


def gh_ara(kalem):
    q = re.sub(r"\(.*?\)|[/`'\"]", " ", kalem).strip()
    if len(nrm(q)) < 3:
        return None
    time.sleep(2.2)
    rc, o, e = K.k(["gh", "search", "repos", q, "--limit", "5", "--sort", "stars", "--json", "fullName,name,stargazersCount,description"], 60)
    if rc != 0:
        if "rate limit" in (e or "").lower():
            time.sleep(65)
        return None
    try:
        sonuc = json.loads(o or "[]")
    except Exception:
        return None
    nk = nrm(q)
    for r in sonuc:
        nr = nrm(r["name"])
        if r.get("stargazersCount", 0) >= 10 and (nk == nr or (len(nk) >= 5 and len(nr) >= 4 and (nk in nr or nr in nk))):
            return r["fullName"]
    return None


def arama_turu(son):
    olu = yok_404()
    hedef = []
    for v, es in son.items():
        for kalem, d in es.items():
            s = str(d)
            if "cevabı yok" in s or (s.startswith("gh:") and s[3:].strip().strip("/") in olu):
                hedef.append((v, kalem))
    yaz("gh arama hedef", len(hedef))
    bulunan = 0
    for i, (v, kalem) in enumerate(hedef, 1):
        r = gh_ara(kalem)
        if r:
            ekle(v, {kalem: "gh:" + r}, "gh-arama"); bulunan += 1
        if i % 50 == 0:
            yaz("arama", i, "/", len(hedef), "bulunan", bulunan)
    yaz("gh arama bitti bulunan", bulunan, "/", len(hedef))


def model_turu():
    idx = K.rapor_dizini()
    for tur in range(1, 4):
        son = en_iyi()
        isler = [(v, [k for k, d in es.items() if "cevabı yok" in str(d)]) for v, es in son.items()]
        isler = [x for x in isler if x[1]]
        yaz("model tur", tur, "video", len(isler), "kalem", sum(len(x[1]) for x in isler))
        if not isler:
            return
        cevap = 0
        for v, kalemler in isler:
            r = K.coz_video(v, kalemler, idx)
            if any("cevabı yok" not in str(d) for d in r.get("eslesme", {}).values()):
                cevap += 1
                with open(K.COZ, "a", encoding="utf-8") as f:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        yaz("model tur", tur, "cevap gelen video", cevap)
        if tur < 3:
            time.sleep(1800)


def say():
    son = en_iyi()
    from collections import Counter
    c = Counter(str(d).split(":")[0] if isinstance(d, str) else "BOZUK" for es in son.values() for d in es.values())
    kota = sum(1 for es in son.values() for d in es.values() if "cevabı yok" in str(d))
    t = {}
    for l in open(K.TOPLU, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(l); t[o.get("repo_istenen")] = o.get("durum")
        except Exception:
            pass
    oz = {"zaman": time.strftime("%Y-%m-%d %H:%M"), "video": len(son), "kalem": sum(len(x) for x in son.values()), "coz": dict(c),
          "kota_kalan": kota, "indir": dict(Counter(t.values()))}
    json.dump(oz, open(OZET, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    yaz("OZET", json.dumps(oz, ensure_ascii=False))


if __name__ == "__main__":
    while subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | ?{$_.CommandLine -match 'kurulum_coz2.py indir'}).Count"],
                         capture_output=True, text=True, creationflags=0x08000000).stdout.strip() not in ("", "0"):
        time.sleep(60)
    yaz("BASLADI")
    duzelt_bozuk(en_iyi())
    arama_turu(en_iyi())
    K.indir()
    model_turu()
    arama_turu(en_iyi())
    K.indir()
    say()
    yaz("TAMAMLA-BITTI")
