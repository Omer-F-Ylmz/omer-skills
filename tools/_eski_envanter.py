"""TARA-KOD-1: iş tarifi → geniş, sıkıştırılmış aday kümesi (aşama 1). Seçimi ana oturum yapar (aşama 2), altin_ornek.py kaydeder (aşama 3).
  python tools/envanter_tara.py "<iş>" [--satir 110] [--yenile] [--json]
Kaynaklar (ara sonuçlar bağlama girmez, yalnız birleşik liste basılır): katalog_ara (BM25) · arac_ara --sec · kart.jsonl (docs/arac-kart)
· kombin.json (iş türü) · graphify query · docs/kaynak-kutuphane/envanter.tsv · tasarim-katalog kaynak.tsv · omer-kutuphaneler raf
· altın örnekler (.kos/kopru/altin-ornek/*.jsonl) · her zaman çok yönlüler. xerj PATH'te yoksa atlanır.
Önbellek: .kos/kopru/tara-onbellek/<hash>.txt, 7 gün."""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
ONBELLEK = KOK / ".kos" / "kopru" / "tara-onbellek"
ALTIN = KOK / ".kos" / "kopru" / "altin-ornek"
GUN7 = 7 * 86400
COK_YONLU = ["impeccable + frontend-craft (UI/görsel işi)", "rea (SS'ten/URL'den kod, site çoğaltma)", "graphify", "beyin ara", "headroom-compress", "context-mode", "rtk",
             "playwright", "jev (toplu yargı)", "markitdown", "yt-dlp", "gitleaks", "semgrep", "code-mode (tools/cm.py)",
             "arac-ara", "kombin-rehber", "is-akisi", "departman-* müdür skill'leri"]
TUR = {  # kombin.json anahtarı ← iş sözcükleri
    "video": "video klip montaj kurgu render reels altyazi", "kod-backend": "api backend net dotnet sunucu veritabani db servis",
    "guvenlik": "guvenlik security acik pentest tarama sizinti sir", "belge": "belge pdf docx sunum rapor tablo",
    "kurulum": "kurulum kur install", "site-3d": "site web sayfa landing 3d frontend arayuz tasarim",
    "render": "3d model blender render mesh", "logo-gorsel": "logo gorsel resim afis ikon",
}
TIP_ADI = {  # iş türü → katalog adı kalıbı (aile girişleri; katalog_ara BM25'inin kaçırdığı aileler: dn-*, departman-*, paketler)
    "site-3d": r"^fe-|frontend|impeccable|ui-ux|^taste|^rea($|[-_])|playwright|tasarim-katalog|omer-kutuphaneler|webgl|threejs|3d-hero",
    "video": r"remotion|hyperframes|ffmpeg|^video|yt-dlp|pixeljury|whisper|caption|premiere",
    "dotnet": r"^dn-|^dotnet|gitleaks|semgrep|^departman-(backend|test)",
    "guvenlik": r"security|guvenlik|gitleaks|semgrep|skillspector|sast|owasp|pentest",
    "render": r"blender|threejs|webgl|3d-hero|img2|pixeljury|^bl-",
}
TIP_SOZ = {"site-3d": TUR["site-3d"], "video": TUR["video"], "guvenlik": TUR["guvenlik"], "render": TUR["render"] + " 3d model",
           "dotnet": ".net net dotnet api backend csharp aspnet efcore"}
TIP_TAVAN = 60
TR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def duz(s):
    return s.translate(TR).lower()


def kelimeler(is_):
    return [w for w in re.findall(r"[a-z0-9.#+]{3,}", duz(is_))]


def calis(args, sn=60):
    try:
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=KOK, timeout=sn)
        return r.stdout or ""
    except Exception:
        return ""


def katalog(is_, n=70):
    out = []
    tur = ""
    for s in calis([sys.executable, "tools/katalog_ara.py", is_, "--aday", str(n)]).splitlines():
        m = re.match(r"## (\S+)", s)
        if m:
            tur = m.group(1)
            continue
        m = re.match(r"\d+\.\s+(.+?) · (.*)", s)
        if m:
            out.append((m.group(1).strip(), tur, m.group(2)[:70].strip()))
    return out


def sec(is_):
    metin = calis([sys.executable, "tools/arac_ara.py", "--sec", is_]).splitlines()
    ilk = metin[0] if metin else ""
    return [(a.strip(), "sec", "arac_ara --sec") for a in ilk.split(" · ") if a.strip()]


def kombin(is_):
    try:
        d = json.loads((KOK / "docs/arac-kart/kombin.json").read_text(encoding="utf-8"))
    except Exception:
        return []
    w = set(kelimeler(is_))
    out = []
    for k, sozler in TUR.items():
        if w & set(sozler.split()) and k in d:
            out += [(a, "kombin", f"kombin:{k}") for a in d[k]]
    return out


def tip_aile(is_):
    w = set(kelimeler(is_))
    ad = [l.split("	")[0] for l in (KOK / "docs/katalog/yetenek.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    out = [(a, "aile", "departman müdürü") for a in dict.fromkeys(ad) if a.startswith("departman-")]
    for k, soz in TIP_SOZ.items():
        if w & set(soz.split()):
            r = re.compile(TIP_ADI[k], re.I)
            es = sorted({a for a in ad if r.search(a) and "motion-prompt" not in a}, key=lambda a: (":" in a, len(a), a))
            out += [(a, "aile", f"aile:{k}") for a in es[:TIP_TAVAN]]
    return out


def tsv_ara(yol, is_, ad_kolon, ne_kolon, etiket, en=8):
    p = KOK / yol
    if not p.exists():
        return []
    w = kelimeler(is_)
    puan = []
    for s in p.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        k = s.split("\t")
        if len(k) <= max(ad_kolon, ne_kolon):
            continue
        m = duz(s)
        z = sum(1 for x in w if x in m)
        if z:
            puan.append((z, (k[ad_kolon], etiket, k[ne_kolon][:70])))
    puan.sort(key=lambda t: -t[0])
    return [x for _, x in puan[:en]]


def kutuphane_raf(is_, en=6):
    raf = KOK / "skills/omer-kutuphaneler/raf"
    if not raf.exists():
        return []
    w = kelimeler(is_)
    return [(d.name, "kutuphane", "omer-kutuphaneler/raf") for d in raf.iterdir() if any(x in duz(d.name) for x in w)][:en]


def graf(is_, en=8):
    if not shutil.which("graphify") or not (KOK / "graphify-out/graph.json").exists():
        return []
    out = []
    for s in calis(["graphify", "query", is_], 60).splitlines():
        m = re.match(r"\s*(?:NODE|node)?\s*([\w./() -]{4,60})\s*\[", s)
        if m and len(out) < en:
            out.append((m.group(1).strip(), "graf", "graphify"))
    return out


def xerj(is_):
    if not shutil.which("xerj"):
        return []
    return [(s.strip()[:60], "xerj", "xerj search") for s in calis(["xerj", "search", is_], 30).splitlines()[:5] if s.strip()]


def altin(is_):
    """Benzer geçmiş işlerin seçimleri; kaçırılanlar (kacirilan) önce gelir."""
    if not ALTIN.exists():
        return []
    w = set(kelimeler(is_))
    sonuc = []
    for f in ALTIN.glob("*.jsonl"):
        for s in f.read_text(encoding="utf-8").splitlines():
            try:
                o = json.loads(s)
            except ValueError:
                continue
            v = set(kelimeler(o.get("is", "")))
            if w and len(w & v) / len(w | v) >= 0.25:
                for a in o.get("kacirilan", []):
                    sonuc.append((a, "ALTIN!", "daha önce kaçırıldı"))
                for a in o.get("secim", []):
                    sonuc.append((a, "altin", "benzer işte seçilmişti"))
    return sonuc


def birlestir(is_, satir):
    kaynaklar = [altin(is_), kombin(is_), tip_aile(is_), sec(is_), katalog(is_), graf(is_), xerj(is_),
                 tsv_ara("docs/kaynak-kutuphane/envanter.tsv", is_, 0, 1, "kaynak"),
                 tsv_ara("skills/tasarim-katalog/references/kaynak.tsv", is_, 0, 5, "tasarim"),
                 kutuphane_raf(is_)]
    gor = {}
    for liste in kaynaklar:  # sıra = öncelik; aynı ad tek satır, kaynaklar birleşir
        for ad, tur, ne in liste:
            a = re.sub(r"^(skill|ajan|mcp):", "", ad)
            if a not in gor:
                gor[a] = [set(), ne]
            gor[a][0].add(tur)
    gruplar = {}
    for a, (turler, ne) in gor.items():
        g = "ALTIN" if {"ALTIN!", "altin"} & turler else (sorted(turler)[0])
        gruplar.setdefault(g, []).append(a if g == "aile" else f"{a} · {'/'.join(sorted(turler))} · {ne}")
    aile = gruplar.pop("aile", [])  # yalnız ad: 8'i bir satırda (jeton ucuz, satır sayısı şişmez)
    bos = max(satir - 4 - 2 * len(gruplar) - len(aile) // 8 - 2, 20)
    tavan = max(bos // max(len(gruplar), 1), 4)  # grup başına adil pay; kısa gruplardan artan pay uzun gruplara
    kullan = {g: min(len(v), tavan) for g, v in gruplar.items()}
    artan = bos - sum(kullan.values())
    for g in sorted(gruplar, key=lambda x: -len(gruplar[x])):
        ek = min(len(gruplar[g]) - kullan[g], max(artan, 0))
        kullan[g] += ek
        artan -= ek
    cikti = []
    for g in sorted(gruplar, key=lambda x: (x != "ALTIN", x)):
        cikti.append(f"## {g} ({len(gruplar[g])})")
        cikti += gruplar[g][:kullan[g]]
        if len(gruplar[g]) > kullan[g]:
            cikti.append(f"... +{len(gruplar[g]) - kullan[g]}")
    if aile:
        cikti.append(f"## aile ({len(aile)}) — departman müdürleri + iş türü aileleri, yalnız ad")
        cikti += [" · ".join(aile[i:i + 8]) for i in range(0, len(aile), 8)]
    kes = cikti
    return [f"# aday kümesi: {is_} (seçim ana oturumda; eksik varsa ekle)"] + kes + ["## çok yönlüler (her zaman)", " · ".join(COK_YONLU)]


def main(a):
    satir = 130
    if "--satir" in a:
        i = a.index("--satir")
        satir = int(a[i + 1])
        del a[i:i + 2]
    yenile = "--yenile" in a
    is_ = " ".join(x for x in a if not x.startswith("--"))
    if not is_:
        print(__doc__)
        return 2
    ONBELLEK.mkdir(parents=True, exist_ok=True)
    f = ONBELLEK / (hashlib.sha1(f"{is_}|{satir}".encode()).hexdigest()[:16] + ".txt")
    # altın örnek eklenince önbellek geçersiz: en yeni altın dosya önbellekten yeniyse yeniden hesapla
    taze = f.exists() and time.time() - f.stat().st_mtime < GUN7 and not yenile
    if taze and ALTIN.exists() and any(g.stat().st_mtime > f.stat().st_mtime for g in ALTIN.glob("*.jsonl")):
        taze = False
    if taze:
        metin = f.read_text(encoding="utf-8")
    else:
        metin = chr(10).join(birlestir(is_, satir))
        f.write_text(metin, encoding="utf-8")
    sys.stdout.buffer.write((metin + chr(10)).encode("utf-8", "replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
