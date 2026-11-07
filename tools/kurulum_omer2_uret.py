"""KURULUM-5B: tmp/k5b/*-sonuc.tsv doğrulama çıktılarından tools/kurulum_omer2.ps1 üretir (kurulum yapmaz).
Kullanım: python tools/kurulum_omer2_uret.py  -> ps1 + rapor/kurulum-5b-sayim.json"""
import csv, glob, json, re, sys
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / "tmp/k5b"
OUT = R / "tools/kurulum_omer2.ps1"
SAY = R / "rapor/kur-hepsi-sayim.json"
KLONYOL = "C:\\Users\\pc\\Desktop\\Claude ile yapılanlar\\araclar\\ana-liste"
BOSLUK = re.compile(r"\s+")


def q(s):
    return "'" + str(s).replace("'", "''") + "'"


def repo_of(h):
    h = h.strip()
    m = re.search(r"->\s*([\w.-]+/[\w.-]+)", h)
    if m: return m.group(1)
    m = re.match(r"([\w.-]+/[\w.-]+)", h)
    return m.group(1) if m else None


def satir(k, y, h, kanit=""):
    """(ps1 satırı | None, neden) — None ise OMER-SOR yorumuna düşer."""
    y = (y or "").upper(); h = (h or "").strip()
    if y in ("SKILL", "SKILL-TOPLU"):
        m = re.match(r"([\w.-]+/[\w.-]+)(?::(\S+))?", re.sub(r"\(->\s*", "", h))
        if not m: return None, "repo çözülemedi"
        sub = (m.group(2) or "").rstrip("/")
        return f"Kur5Skill {q(k)} {q(m.group(1))} {q(sub)}", ""
    if y == "KLON":
        r = repo_of(h)
        return (f"Kur5Klon {q(k)} {q(r)}", "") if r else (None, "repo çözülemedi")
    if y == "NPM":
        t = re.sub(r"^npm:", "", h).split()[0] if h else ""
        if t and "/" in t and not t.startswith("@"): return None, "hedef GitHub repo yolu, npm paket adı değil"
        return (f"Kur5Npm {q(k)} {q(t)}", "") if t and not t.startswith("(") else (None, "paket adı yok")
    if y == "PIP":
        t = re.sub(r"^pip:", "", h).split()[0] if h else ""
        return (f"Kur5Pip {q(k)} {q(t)}", "") if t and not t.startswith("(") else (None, "paket adı yok")
    if y == "UV":
        return f"Kur5Uv {q(k)} {q(h.split(' (')[0])}", ""
    if y == "WINGET":
        m = re.match(r"([A-Za-z0-9][\w.+-]*\.[\w.+-]+)", h)
        return (f"Kur5Winget {q(k)} {q(m.group(1))}", "") if m else (None, "winget kimliği yok")
    if y in ("RELEASE", "ZIP"):
        m = re.match(r"(https?://\S+)", h)
        if m and re.search(r"\.(zip|exe|msi)(\?|$)", m.group(1)): return f"Kur5Indir {q(k)} {q(m.group(1))}", ""
        r = repo_of(h)
        if r and "downloads.apache.org" not in h:
            ip = re.search(r"([\w.\-]+\.(?:zip|exe|msi))", h + " " + kanit)
            return f"Kur5Rel {q(k)} {q(r)} {q(ip.group(1) if ip else '')}", ""
        return None, "asset URL'si yok (yalnız repo/dizin)"
    if y == "COMPOSER":
        t = h.split()[0] if h else ""
        return (f"Kur5Composer {q(k)} {q(t)}", "") if "/" in t else (None, "paket adı yok")
    if y == "VSCODE":
        return f"Kur5Vscode {q(k)} {q(h.split()[0])}", ""
    return None, f"yöntem {y} betikte desteklenmiyor"


def oku_hepsi():
    rows = []
    for p in sorted(glob.glob(str(D / "g[345]*-sonuc.tsv"))):
        for x in csv.DictReader(open(p, encoding="utf-8-sig"), delimiter="\t"):
            rows.append({"kalem": x["kalem"], "karar": x.get("karar") or x.get("durum"), "yontem": x.get("yontem") or "",
                         "hedef": x.get("hedef") or "", "lisans": x.get("lisans") or "",
                         "not": (x.get("kanit") or x.get("kanit_not") or x.get("neden") or "")})
    return rows


HATA10 = [  # tmp/k5b/hata10.tsv (kanıtlı; dosya kaçış hatalı olduğundan elle aktarıldı)
    ("LEANN", "KURULABILIR", "Kur5Uv 'LEANN' 'leann-core'", "PyPI 'leann' yanlış ad; CLI leann-core içinde (leann=leann.cli:main)"),
    ("Chatterbox", "OMER-SOR", None, "chatterbox-tts kütüphane (entry_points yok), torch/GB indirme: venv + uv pip; Ömer karar"),
    ("MLSharp", "OMER-SOR", None, "PyPI 'sharp' başka paket; doğrusu git+https://github.com/apple-aiml-research/ml-sharp, lisans NOASSERTION"),
    ("ScriptCreatorGraph", "KURULABILIR", "Kur5Venv 'ScriptCreatorGraph' 'scrapegraphai' '3.12'", "scrapegraphai kütüphane (entry_points yok): venv + uv pip, py3.12"),
    ("build-error-resolver", "KURULABILIR", "Kur5Ajan 'build-error-resolver' 'agents/build-error-resolver.md'", "PyPI değil, ECC ajan dosyası (MIT)"),
    ("e2e-runner", "KURULABILIR", "Kur5Ajan 'e2e-runner' 'agents/e2e-runner.md'", "ECC ajan dosyası (MIT)"),
    ("harness-optimizer", "KURULABILIR", "Kur5Ajan 'harness-optimizer' 'agents/harness-optimizer.md'", "ECC ajan dosyası (MIT)"),
    ("xet", "YOK", None, "hf-xet Rust kütüphane, bağımsız araç değil"),
    ("pgnx", "OMER-SOR", None, "install.js yalnız Node 22 (ABI 127) prebuild; makinede Node 24"),
    ("pi coding agent", "YOK", None, "zaten kurulu: @earendil-works/pi-coding-agent (pi.cmd); EEXIST bin çakışması"),
]


BLOK2GB = re.compile(r">\s*2\s*gb|(?<![\d.])([3-9]|\d{2,})(\.\d+)?\s*gb|13gb|devasa", re.I)
BLOKDIGER = re.compile(r"ticari|eula|sistem|yeniden baslatma|olculemedi|saldiri|ofansif|jailbreak|ps5|kalem belirsiz|kalem yazimi|ad belirsiz|ad farkli|ayni mi|esle[sş]mesi belirsiz|belirsiz esle|belirsiz:|yanlis|api anahtari|ucretli|linux|self-host|sunucu|docker|gpu|kaynak yok|kaynak yonerge|playbook|release yok|derleme|arsiv|yazimi|ayna|ad \(|kalem \(|yildiz, lisans belirsiz|buyuk|dokuman goruntuleyici|kalem belirsiz|<1MB.*GPL", re.I)
UYG = re.compile(r"(gui|uygulama)", re.I)
MB = re.compile(r"=?\(?<?\s*(\d+(?:\.\d+)?)\s*MB", re.I)


AMBIG = re.compile(r"kalem belirsiz|kalem yazimi|ad belirsiz|ad farkli|ayni mi|esle[sş]mesi belirsiz|belirsiz esle|ad \(|kalem \(|yanlis", re.I)
RISK = re.compile(r"saldiri|ofansif|jailbreak|ps5|pentest|bughunter|bug-hunter|exploit|wifite|linux", re.I)


def sinif_os(x):
    """OMER-SOR satırı -> (KURULABILIR|2GB|BELIRSIZ|RISK|SATIR-YOK, neden)."""
    t = " ".join([x["not"], x["lisans"], x["hedef"], x["yontem"]])
    if BLOK2GB.search(t): return "2GB", "boyut >2 GB"
    d = BLOKDIGER.search(t)
    if d: return "BELIRSIZ", d.group(0)
    if UYG.search(x["not"]):
        m = MB.search(x["not"])
        if m and float(m.group(1)) <= 2048: return "KURULABILIR", f"uygulama {m.group(1)} MB <= 2 GB"
        return "BELIRSIZ", "uygulama boyutu ölçülmemiş"
    return "KURULABILIR", "yalnız lisans gerekçesi"


def npm_durum():
    d = {}
    f = R / "tmp/kh1/npm-bin.tsv"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            a = ln.split("	")
            if len(a) >= 3: d[a[1]] = a[2]
    return d


def winget_durum():
    d = {}
    f = R / "tmp/kh1/winget-dogrula.tsv"
    if f.exists():
        for ln in f.read_text(encoding="utf-8").splitlines():
            a = ln.split("	")
            if len(a) >= 3: d[a[1]] = a[2]
    return d


def onsoz():
    return (R / "tools/kurulum_omer2_onsoz.ps1").read_text(encoding="utf-8").replace("__KLON__", KLONYOL)


def anahtar(s):
    """Tekilleştirme: kalem adını yok say, fonksiyon + hedef argümanları kalsın."""
    m = re.match(r"(\w+) '(?:[^']|'')*' (.*)$", s)
    return (m.group(1), m.group(2)) if m else (s, "")


def main():
    hazirla = "--hazirla" in sys.argv
    rows = oku_hepsi()
    npmd, wgd = npm_durum(), winget_durum()
    belirs = {}
    bf = R / "tmp/kh1/belirsiz-sonuc.tsv"
    if bf.exists():
        for ln in bf.read_text(encoding="utf-8").splitlines():
            a = ln.split("\t")
            if len(a) >= 5: belirs[a[0]] = a
    sayim, satirlar, yorum, goruldu = Counter(), [], [], set()
    kutup, iki_gb, geri = [], [], []   # kütüphane listesi, >2GB tablosu, lisans yüzünden OMER-SOR'dan KURULABILIR'e geçenler
    belirsiz_liste = []                # repo doğrulaması gereken satırlar (--hazirla)

    def ekle(x, k, y, h, lis, kanit):
        s, neden = satir(k, y, h, kanit)
        if s is None:
            yorum.append(f"# OMER-SOR (betik satiri yok: {neden}): {k} | {y} | {h[:80]}")
            sayim["OMER-SOR(satir-yok)"] += 1
            return False
        if s.startswith("Kur5Npm") and npmd.get(re.findall(r"'((?:[^']|'')*)'", s)[1], "") == "KUTUPHANE":
            kutup.append((k, re.findall(r"'((?:[^']|'')*)'", s)[1]))
            sayim["KUTUPHANE(npm bin yok)"] += 1
            return False
        if s.startswith("Kur5Winget"):
            d = wgd.get(re.findall(r"'((?:[^']|'')*)'", s)[1], "")
            if d == "DOGRULANAMADI":
                yorum.append(f"# WINGET-KIMLIK-YOK (search bos): {k} | {s}")
                sayim["WINGET-KIMLIK-YOK"] += 1
                return False
            if d == "ZAMAN":   # winget search/show bu makinede 90 sn+ takiliyor: kimlik ölçülemedi, satır kalır ve işaretlenir
                lis = "WINGET-OLCULEMEDI(zaman asimi)"
                sayim["WINGET-OLCULEMEDI"] += 1
        a = anahtar(s)
        if a in goruldu:
            sayim["TEKRAR"] += 1
            return False
        goruldu.add(a)
        satirlar.append((y.upper().replace("-TOPLU", ""), s, lis))
        sayim["KURULABILIR:" + y.upper()] += 1
        return True

    for x in rows:
        k, kar = x["kalem"], x["karar"]
        if kar in ("KURULABILIR", "GERI-AL"):
            ekle(x, k, x["yontem"], x["hedef"], x["lisans"], x["not"])
        elif kar == "OMER-SOR":
            n = BOSLUK.sub(" ", x["not"])[:110]
            sn, neden = sinif_os(x)
            rp = repo_of(x["hedef"]) if x["hedef"] else None
            if sn == "BELIRSIZ" and rp and k in belirs and AMBIG.search(neden) and not RISK.search(x["not"] + " " + rp + " " + k):   # kaynak yeniden doğrulandı: ad eşleşiyorsa geç
                b = belirs[k]
                metin = (rp + " " + b[2] + " " + b[4]).lower()
                tok = [w for w in re.findall(r"[a-z0-9]{4,}", k.lower())]
                if tok and any(w in metin for w in tok) and "arsiv=True" not in b[3] and re.search(r"push=(202[5-9]|20[3-9]\d)", b[3]):
                    sn, neden = "KURULABILIR", "repo yeniden doğrulandı (gh repo view + README)"
            if sn == "KURULABILIR" and "lisans" in neden:
                if ekle(x, k, x["yontem"], x["hedef"], x["lisans"], x["not"]):
                    geri.append((k, x["lisans"][:30]))
                    sayim["LISANS-GERI-ALINDI"] += 1
                continue
            if sn == "KURULABILIR":
                if ekle(x, k, x["yontem"], x["hedef"], x["lisans"], x["not"]):
                    geri.append((k, neden))
                    sayim["UYGULAMA<=2GB-KURULABILIR"] += 1
                continue
            if hazirla and (sn == "BELIRSIZ" and rp and AMBIG.search(neden) or sn == "2GB" and rp and x["yontem"] in ("KLON", "RELEASE", "")): belirsiz_liste.append(f"{k}\t{rp}")
            if sn == "2GB": iki_gb.append((k, x["yontem"], x["hedef"], n, rp))
            yorum.append(f"# OMER-SOR[{sn}: {neden}]: {k} | lisans={x['lisans'][:40]} | {n}")
            sayim["OMER-SOR:" + sn] += 1
        else:
            sayim[kar] += 1
    for k, kar, s, n in HATA10:
        if s:
            a = anahtar(s)
            if a not in goruldu:
                goruldu.add(a)
                satirlar.append(("HATA10", s, ""))
                sayim["KURULABILIR:HATA10"] += 1
        elif kar == "OMER-SOR":
            yorum.append(f"# OMER-SOR: {k} | {n}")
            sayim["OMER-SOR"] += 1
        else:
            sayim[kar + "(hata10)"] += 1
    if hazirla:
        (R / "tmp/kh1/belirsiz.tsv").write_text("\n".join(belirsiz_liste) + "\n", encoding="utf-8")
        print("hazirla:", len(belirsiz_liste), "repo")
        return
    govde = []
    for y, s, lis in sorted(satirlar, key=lambda t: t[0]):
        l = (lis or "").strip()
        govde.append(s + (f"  # lisans: {l}" if l and l not in ("MIT", "Apache-2.0", "BSD-3-Clause") else ""))
    OUT.write_text(onsoz() + "\n".join(govde) + "\n\n" + "\n".join(yorum) + "\n", encoding="utf-8-sig")
    (R / "rapor/kur-hepsi-kutuphane.tsv").write_text("kalem\tnpm_paketi\n" + "\n".join(f"{a}\t{b}" for a, b in kutup) + "\n", encoding="utf-8")
    (R / "rapor/kur-hepsi-lisans-geri.tsv").write_text("kalem\tgerekce\n" + "\n".join(f"{a}\t{b}" for a, b in geri) + "\n", encoding="utf-8")
    md = ["# OMER-SOR: 2 GB üstü kalemler (Ömer evet/hayır der)", "",
          "| ad | ölçülen boyut | kaynak | ne işe yarar |", "|---|---|---|---|"]
    for k, y, h, n, rp in iki_gb:
        b = belirs.get(k)
        boyut = (re.search(r"kb=(\d+)", b[3]) and f"{int(re.search(r'kb=(\d+)', b[3]).group(1)) / 1048576:.2f} GB (gh diskUsage)") if b else None
        if not boyut:
            m = re.search(r"((?:>\s*)?\d+(?:\.\d+)?\s*GB)", n + " " + h, re.I)
            boyut = (m.group(1) + " (kayıt notu)") if m else "ölçülemedi (kayıt notunda sayı yok, kaynakta boyut alanı yok)"
        md.append(f"| {k} | {boyut} | {(rp or h or '-')[:60]} | {(b[2] if b and b[2] else n)[:90]} |")
    (R / "rapor/omer-sor-2gb.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    SAY.write_text(json.dumps({"betik_satiri": len(satirlar), "sayim": sayim}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(satirlar), dict(sayim))


main()
