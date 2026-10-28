"""TARA-KOD-1: iş tarifi → geniş, sıkıştırılmış aday kümesi (aşama 1). Seçimi ana oturum yapar (aşama 2), altin_ornek.py kaydeder (aşama 3).
  python tools/envanter_tara.py "<iş>" [--satir 110] [--yenile] [--json]
Kaynaklar (ara sonuçlar bağlama girmez, yalnız birleşik liste basılır): katalog_ara (BM25) · arac_ara --sec · kart.jsonl (docs/arac-kart)
· kombin.json (iş türü) · graphify query · docs/kaynak-kutuphane/envanter.tsv · tasarim-katalog kaynak.tsv · omer-kutuphaneler raf
· altın örnekler (.kos/kopru/altin-ornek/*.jsonl) · her zaman çok yönlüler. xerj PATH'te yoksa atlanır.
KAYNAK-DIZIN-1: `--dizin [--tam]` birleşik kaynak dizinini (.kos/kopru/kaynak-dizin/dizin.tsv) artımlı günceller; `--kaynak "<iş>" [--hepsi]` yalnız kaynaklar bölümü.
Önbellek: .kos/kopru/tara-onbellek/<hash>.txt, 7 gün."""
import hashlib
import json
import math
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
    onb = ONBELLEK / ("calis-" + hashlib.sha1(json.dumps(args).encode()).hexdigest()[:16] + ".txt")  # aynı komut 6 saat önbellekli
    if onb.exists() and time.time() - onb.stat().st_mtime < 6 * 3600:
        return onb.read_text(encoding="utf-8")
    cikti = _calis(args, sn)
    if cikti:
        ONBELLEK.mkdir(parents=True, exist_ok=True)
        onb.write_text(cikti, encoding="utf-8")
    return cikti


def _calis(args, sn=60):
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

# ---- KAYNAK-DIZIN-1: tüm kaynak türleri tek yerel dizinde (tür · ad · yol/URL · özet · etiket); artımlı (mtime önbelleği) ----
DIZIN = KOK / ".kos" / "kopru" / "kaynak-dizin"
MASA = Path.home() / "Desktop" / "Claude ile yapılanlar"
ATLA = {"node_modules", ".git", ".venv", "venv", "__pycache__", "dist", "build", ".next", "site-packages", "Library", "Temp"}
VARLIK = {".glsl", ".frag", ".vert", ".blend", ".gltf", ".glb", ".lottie", ".hdr", ".exr", ".ttf", ".otf"}
VARLIK_AD = re.compile(r"shader|logo|hero|anim|scene|sahne|component|bilesen|design[-_ ]?system|tokens", re.I)
EL = chr(92)
SINONIM = {"video": "ffmpeg whisper remotion", "logo": "pixeljury brand", "gorsel": "pixeljury", "blender": "bpy 3d", "borsa": "trading algoritmik",
           "kripto": "trading algoritmik", "scroll": "gsap hero-video", "arka": "hero-video"}


def ozet_md(metin):
    """Dosyanın tek satırlık özeti: **Ne:** satırı, yoksa başlık + ilk düz cümle."""
    govde = metin.split("---", 2)[-1] if metin.startswith("---") else metin
    satirlar = [l.strip() for l in govde.splitlines() if l.strip()]
    for l in satirlar[:12]:
        m = re.match(r"[-*\s]*\*\*(?:Ne|Amaç|Özet):\*\*\s*(.+)", l)
        if m:
            return m.group(1)[:110]
    baslik = next((l.lstrip("# ") for l in satirlar if l.startswith("#")), "")
    duzyazi = next((l for l in satirlar if not l.startswith(("#", "|", "```", "<", "![", "-")) and len(l) > 20), "")
    return (baslik + (" — " + duzyazi if duzyazi else ""))[:110]


def md_satir(tur, f, etiket, kok):
    try:
        t = f.read_text(encoding="utf-8", errors="replace")[:3000]
    except OSError:
        return []
    try:
        yol = str(f.relative_to(kok)).replace(EL, "/") if kok == KOK else str(f).replace(EL, "/")
    except ValueError:
        yol = str(f)
    return [(tur, f.stem[:60], yol, ozet_md(t), etiket)]


def json_video(f):
    try:
        d = json.loads(f.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return []
    if not isinstance(d, dict):
        return []
    m = d.get("meta")
    baslik = (m.get("title") or m.get("baslik") or "") if isinstance(m, dict) else ""
    tr = d.get("transkript") or ""
    ozet = baslik or (tr if isinstance(tr, str) else json.dumps(tr, ensure_ascii=False))
    return [("yontem", f.stem, d.get("url") or f"docs/video-tarama/{f.parent.name}/{f.name}", str(ozet).replace(chr(10), " ")[:110], "video yontem")]


def tsv_satir(f, tur, ad_k, yol_k, ozet_k, etiket):
    out = []
    for s in f.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        k = s.split("\t")
        if len(k) > max(ad_k, yol_k, ozet_k):
            out.append((tur, k[ad_k][:60], k[yol_k][:140], k[ozet_k][:110], etiket))
    return out


def dosya_kaynaklari():
    """(dosya, üretici) çiftleri; dosya mtime'ı aynıysa satırlar yeniden üretilmez."""
    r = []
    ekle = lambda dosyalar, uret: r.extend((f, uret) for f in dosyalar)
    ekle(sorted((KOK / "docs/site-inceleme").glob("*.md")), lambda f: md_satir("site", f, "site inceleme", KOK))
    ekle(sorted((KOK / "docs/site-inceleme/kart").glob("*.md")), lambda f: md_satir("site", f, "site kart", KOK))
    ekle([KOK / "docs/kaynak-kutuphane/envanter.tsv"], lambda f: tsv_satir(f, "site", 0, 7, 1, "kaynak-kutuphane"))
    ekle([KOK / "skills/tasarim-katalog/references/kaynak.tsv"], lambda f: tsv_satir(f, "site", 0, 1, 5, "tasarim-katalog"))
    ekle(sorted((KOK / "docs/kaynak-kutuphane").glob("*.md")), lambda f: md_satir("klon", f, "kaynak-kutuphane", KOK))
    ekle(sorted((KOK / "docs/video-tarama").glob("derin*/*.json")), json_video)
    ekle(sorted((KOK / "docs/video-tarama").glob("kaynak/*.json")), json_video)
    for d, tur, e in (("docs/ogren", "yontem", "ders"), ("docs/mekanizmalar", "yontem", "mekanizma"), ("docs/uyarlamalar", "yontem", "uyarlama"),
                      (".roast-room", "yontem", "roast"), ("docs/kutuphane", "klon", "kutuphane"), ("templates", "sablon", "sablon")):
        ekle([f for f in sorted((KOK / d).rglob("*.md")) if "olcum" not in f.parts][:600], lambda f, tur=tur, e=e: md_satir(tur, f, e, KOK))
    ekle([KOK / "docs/kaynak-dizin/baglayici.tsv"], lambda f: tsv_satir(f, "baglayici", 0, 1, 2, "baglayici"))
    obs = MASA / "Obsidian"
    if obs.exists():
        ekle([f for f in sorted(obs.rglob("*.md")) if not ATLA & set(f.parts) and not f.name.startswith("gorev-")][:4000], lambda f: md_satir("yontem", f, "2.beyin obsidian", obs))
    return r


def proje_satirlari():
    """Geçmiş proje varlığı: her proje dizini (yol + özet) + varlık dosyaları (shader/blend/logo/animasyon…); içerik kopyalanmaz."""
    import os
    out = []
    if not MASA.exists():
        return out
    for p in sorted(MASA.iterdir()):
        if not p.is_dir() or p.name in ATLA:
            continue
        oz = ""
        for ad in ("README.md", "readme.md", "CLAUDE.md"):
            if (p / ad).exists():
                oz = ozet_md((p / ad).read_text(encoding="utf-8", errors="replace")[:3000])
                break
        try:
            alt = ", ".join(sorted(x.name for x in p.iterdir() if x.is_dir() and x.name not in ATLA)[:6])
        except OSError:
            alt = ""
        out.append(("proje", p.name[:60], str(p).replace(EL, "/"), (oz or ("alt: " + alt))[:110], "gecmis-proje"))
        sayac = 0
        for yol, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in ATLA and not d.startswith(".")]
            if len(Path(yol).relative_to(p).parts) >= 4:
                dirs[:] = []
            for f in files:
                e = Path(f).suffix.lower()
                if sayac < 25 and (e in VARLIK or (e in {".svg", ".tsx", ".jsx", ".vue", ".css", ".json"} and VARLIK_AD.search(f))):
                    sayac += 1
                    out.append(("varlik", f[:60], str(Path(yol) / f).replace(EL, "/"), f"{p.name} · {e[1:]}", "gecmis-proje " + e[1:]))
    return out


def klon_satirlari():
    out = []
    for kok, etiket in ((KOK / "araclar", "klon araclar"), (MASA / "kaynak-kutuphane", "klon kaynak-kutuphane"), (MASA / "araclar", "klon araclar")):
        if not kok.exists():
            continue
        for p in sorted(kok.iterdir()):
            if p.is_dir() and p.name not in ATLA:
                oz = ""
                for ad in ("README.md", "readme.md"):
                    if (p / ad).exists():
                        oz = ozet_md((p / ad).read_text(encoding="utf-8", errors="replace")[:3000])
                        break
                out.append(("klon", p.name[:60], str(p).replace(EL, "/"), oz or "dizin", etiket))
    t = KOK / "templates"
    if t.exists():
        out += [("sablon", x.name[:60], str(x.relative_to(KOK)).replace(EL, "/"), "şablon " + ("dizini" if x.is_dir() else x.suffix[1:]), "sablon") for x in sorted(t.iterdir())]
    return out


def sistem_satirlari():
    """Yerel modeller, global npm paketleri, Chrome yer imleri."""
    out = []
    ol = calis(["ollama", "list"], 15).splitlines()[1:] if shutil.which("ollama") else []
    out += [("model", s.split()[0], "ollama:" + s.split()[0], "yerel model " + " ".join(s.split()[2:4]), "model ollama yerel") for s in ol if s.split()]
    npm = Path.home() / "AppData/Roaming/npm/node_modules"
    if npm.exists():
        for p in sorted(npm.iterdir()):
            alt = [x for x in p.iterdir() if x.is_dir()] if p.name.startswith("@") else [p]
            for q in alt:
                ad = f"{p.name}/{q.name}" if p.name.startswith("@") else q.name
                out.append(("arac", ad[:60], f"npm -g:{ad}", "global npm paketi", "npm global cli"))
    yi = Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Bookmarks"
    if yi.exists():
        def gez(n):
            if n.get("type") == "url":
                yield ("site", n.get("name", "")[:60], n.get("url", ""), "Chrome yer imi", "yer-imi")
            for c in n.get("children", []):
                yield from gez(c)
        try:
            for k in json.loads(yi.read_text(encoding="utf-8")).get("roots", {}).values():
                if isinstance(k, dict):
                    out += list(gez(k))
        except ValueError:
            pass
    return out


def dizin_guncelle(tam=False):
    """Artımlı: dosya mtime'ı değişmeyen kaynağın satırları önbellekten gelir. Tekilleştirme: aynı yol/URL tek satır."""
    DIZIN.mkdir(parents=True, exist_ok=True)
    onb_yol = DIZIN / "onbellek.json"
    try:
        onb = {} if tam else json.loads(onb_yol.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        onb = {}
    yeni, satirlar = {}, []
    for f, uret in dosya_kaynaklari():
        try:
            mt = f.stat().st_mtime
        except OSError:
            continue
        k = str(f)
        if k in onb and onb[k][0] == mt:
            rows = onb[k][1]
        else:
            try:
                rows = [list(x) for x in uret(f)]
            except Exception:
                rows = []
        yeni[k] = [mt, rows]
        satirlar += rows
    ts = time.time()
    if "_dizin" in onb and ts - onb["_dizin"][0] < 6 * 3600:  # proje/klon/sistem taraması pahalı: 6 saatte bir
        rows = onb["_dizin"][1]
        yeni["_dizin"] = onb["_dizin"]
    else:
        rows = [list(x) for x in proje_satirlari() + klon_satirlari() + sistem_satirlari()]
        yeni["_dizin"] = [ts, rows]
    satirlar += rows
    gor, son = set(), []
    for r in satirlar:
        anahtar = re.sub(r"^https?://(www\.)?|/$", "", r[2]).lower()
        if anahtar in gor:
            continue
        gor.add(anahtar)
        son.append(r)
    temiz = lambda x: re.sub(r"\s+", " ", str(x)).strip()
    (DIZIN / "dizin.tsv").write_text("tur\tad\tyol\tozet\tetiket\n" + "\n".join("\t".join(temiz(x) for x in r) for r in son) + "\n", encoding="utf-8")
    onb_yol.write_text(json.dumps(yeni, ensure_ascii=False), encoding="utf-8")
    return son


def dizin_oku():
    p = DIZIN / "dizin.tsv"
    if not p.exists():
        dizin_guncelle()
    return [s.split("\t") for s in p.read_text(encoding="utf-8").splitlines()[1:] if s.count("\t") == 4]


def kaynak_ara(is_, en=15, kuyruk=0, tur=None):
    """İşe en ilgili ≤en kaynak; tür başına adil pay, kalan boş yerler en yüksek puanlılara."""
    w = [x for x in kelimeler(is_) if x not in {"icin", "yap", "bir", "ile"}]
    if not w:
        return []
    satirlar = dizin_oku()
    metin = [duz(" ".join(r)) for r in satirlar]
    n = len(satirlar)
    for k, ek in SINONIM.items():  # iş türü → ilgili araç/kaynak adları (dizinde ad/etiket eşleşmesi)
        if any(x.startswith(k) for x in w):
            w += [e for e in ek.split() if e not in w]
    w = [x[:5] if len(x) > 6 else x for x in w]  # Türkçe ek: 7+ harfli sözcük 5 harf köküyle aranır (videosu→video)
    agirlik = {x: math.log(1 + n / (sum(1 for m in metin if x in m) or 1)) for x in w}
    puan = {}
    for r, m in zip(satirlar, metin):
        on = duz(r[1] + " " + r[4])
        z = sum(agirlik[x] * (2 if x in on else 1) for x in w if x in m)
        if z:
            puan.setdefault(r[0], []).append((z, r))
    ak = {duz(a[0]) for a in altin(is_)}  # altın örnekte geçen kaynaklar öne çıkar
    for t, v in puan.items():
        puan[t] = [(z + (3 if any(a and a in duz(r[1]) for a in ak) else 0), r) for z, r in v]
    for v in puan.values():
        v.sort(key=lambda t: -t[0])
    # aynı kaynağın varyantları (omer-logo-2, kart/inceleme çifti) tek satırda toplanır: yer açar, hiçbiri kaybolmaz
    kok = lambda ad: re.sub(r"(?:[-_ ]*(?:\d+|final|v\d+))+$", "", re.split(r" \(", ad.lower())[0]).strip(" -_.") or ad.lower()
    for t, v in list(puan.items()):
        gr, sira = {}, []
        for z, r in v:
            k = kok(r[1])
            if k not in gr:
                gr[k] = [z, r, []]
                sira.append(k)
            elif r[1] != gr[k][1][1]:
                gr[k][2].append(r[1][:30])
        puan[t] = [(gr[k][0], gr[k][1][:1] + [gr[k][1][1] + (f" (+{len(set(gr[k][2]))}: {', '.join(sorted(set(gr[k][2]))[:4])})" if gr[k][2] else "")] + gr[k][1][2:]) for k in sira]
    if tur:
        puan = {t: v for t, v in puan.items() if t == tur}
    turler = sorted(puan, key=lambda t: -puan[t][0][0])
    pay = max(en // max(len(turler), 1), 2)
    secilen = [x for t in turler for x in puan[t][:pay]]
    secilen += sorted((x for t in turler for x in puan[t][pay:]), key=lambda t: -t[0])[:max(en - len(secilen), 0)]
    secilen.sort(key=lambda t: -t[0])
    toplam = sum(len(v) for v in puan.values())
    cik = [f"{r[0]} · {r[1][:70]} · {r[2][-48:]} · {r[3][:34]}" for _, r in secilen[:en]]
    if en < 1000 and toplam > len(cik):
        gor = {id(r) for _, r in secilen[:en]}
        kalan = sorted(((z, r) for v in puan.values() for z, r in v if id(r) not in gor), key=lambda t: -t[0])[:kuyruk]
        gr = {}  # kayıpsız özet: ilk en kalemden sonraki en iyi `kuyruk` kaynağın yalnız adı, tür başına tek satır
        for _, r in kalan:
            gr.setdefault(r[0], []).append(r[1].split(" (+")[0][:26])
        cik += [f"  ({t}) " + ", ".join(v) for t, v in gr.items()]
        if toplam > len(cik_ilk := secilen[:en]) + len(kalan):
            cik.append(f"+{toplam - len(cik_ilk) - len(kalan)} daha: --kaynak \"{is_[:40]}\" --hepsi [--tur <tür>]")
    return cik


def birlestir(is_, satir, brief=False):
    from concurrent.futures import ThreadPoolExecutor  # yavaş alt süreçler (katalog, graphify) paralel: toplam süre en yavaşı kadar
    with ThreadPoolExecutor(6) as ex:
        fl = [ex.submit(f, is_) for f in (altin, kombin, tip_aile, sec, katalog, (lambda _: []) if brief else graf, xerj, kutuphane_raf)]  # brief'te graphify kod grafı atlanır (kaynak brief'ine katkısı yok, 4-6 sn)
        kaynaklar = [f.result() for f in fl]
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
    kay = kaynak_ara(is_, 15, 70)
    bos = max(satir - 4 - 2 * len(gruplar) - len(aile) // 8 - 2 - (len(kay) + 1 + 50 if kay else 0), 20)  # kaynaklar bölümü payı gövdeden düşer (jeton artmasın)
    if brief:
        bos = 3 * len(gruplar)
        aile = []
    tavan = max(bos // max(len(gruplar), 1), 3 if brief else 4)  # grup başına adil pay; kısa gruplardan artan pay uzun gruplara
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
    ust = [f"## kaynaklar ({len(kay)}; tam küme: python tools/envanter_tara.py --kaynak \"<iş>\" --hepsi)"] + kay if kay else []
    return [f"# aday kümesi: {is_} (seçim ana oturumda; eksik varsa ekle)"] + kes + ust + ["## çok yönlüler (her zaman)", " · ".join(COK_YONLU)]


def main(a):
    satir = 130
    brief = "--brief" in a
    if "--satir" in a:
        i = a.index("--satir")
        satir = int(a[i + 1])
        del a[i:i + 2]
    yenile = "--yenile" in a
    if "--dizin" in a:  # artımlı dizin güncelleme (günlük görev); --tam: sıfırdan
        son = dizin_guncelle("--tam" in a)
        sayi = {}
        for r in son:
            sayi[r[0]] = sayi.get(r[0], 0) + 1
        print(len(son), "satır:", ", ".join(f"{k} {v}" for k, v in sorted(sayi.items())))
        return 0
    if "--kaynak" in a:  # yalnız kaynaklar bölümü; --hepsi: tüm eşleşmeler (geri açma yolu)
        tur = a[a.index("--tur") + 1] if "--tur" in a else None
        sorgu = " ".join(x for x in a if not x.startswith("--") and x != tur)
        sys.stdout.buffer.write((chr(10).join(kaynak_ara(sorgu, 5000 if "--hepsi" in a else 15, 0 if "--hepsi" in a else 70, tur)) + chr(10)).encode("utf-8", "replace"))
        return 0
    is_ = " ".join(x for x in a if not x.startswith("--"))
    if not is_:
        print(__doc__)
        return 2
    ONBELLEK.mkdir(parents=True, exist_ok=True)
    f = ONBELLEK / (hashlib.sha1(f"{is_}|{satir}|{brief}".encode()).hexdigest()[:16] + ".txt")
    # altın örnek eklenince önbellek geçersiz: en yeni altın dosya önbellekten yeniyse yeniden hesapla
    taze = f.exists() and time.time() - f.stat().st_mtime < GUN7 and not yenile
    if taze and ALTIN.exists() and any(g.stat().st_mtime > f.stat().st_mtime for g in ALTIN.glob("*.jsonl")):
        taze = False
    if taze:
        metin = f.read_text(encoding="utf-8")
    else:
        metin = chr(10).join(birlestir(is_, satir, brief))
        f.write_text(metin, encoding="utf-8")
    sys.stdout.buffer.write((metin + chr(10)).encode("utf-8", "replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
