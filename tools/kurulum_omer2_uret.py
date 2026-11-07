"""KURULUM-5B: tmp/k5b/*-sonuc.tsv doğrulama çıktılarından tools/kurulum_omer2.ps1 üretir (kurulum yapmaz).
Kullanım: python tools/kurulum_omer2_uret.py  -> ps1 + rapor/kurulum-5b-sayim.json"""
import csv, glob, json, re
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / "tmp/k5b"
OUT = R / "tools/kurulum_omer2.ps1"
SAY = R / "rapor/kurulum-5b-sayim.json"
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


def satir(k, y, h):
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


def onsoz():
    return (R / "tools/kurulum_omer2_onsoz.ps1").read_text(encoding="utf-8").replace("__KLON__", KLONYOL)


def main():
    rows = oku_hepsi()
    sayim, satirlar, yorum, goruldu = Counter(), [], [], set()
    for x in rows:
        k, kar = x["kalem"], x["karar"]
        if kar in ("KURULABILIR", "GERI-AL"):
            s, neden = satir(k, x["yontem"], x["hedef"])
            if s is None:
                yorum.append(f"# OMER-SOR (betik satiri yok: {neden}): {k} | {x['yontem']} | {x['hedef'][:80]}")
                sayim["OMER-SOR(satir-yok)"] += 1
                continue
            if s in goruldu:
                sayim["TEKRAR"] += 1
                continue
            goruldu.add(s)
            satirlar.append((x["yontem"].upper().replace("-TOPLU", ""), s, x["lisans"]))
            sayim["KURULABILIR:" + x["yontem"].upper()] += 1
        elif kar == "OMER-SOR":
            n = BOSLUK.sub(" ", x["not"])[:110]
            yorum.append(f"# OMER-SOR: {k} | lisans={x['lisans'][:40]} | {n}")
            sayim["OMER-SOR"] += 1
        else:
            sayim[kar] += 1
    for k, kar, s, n in HATA10:
        if s:
            satirlar.append(("HATA10", s, ""))
            sayim["KURULABILIR:HATA10"] += 1
        elif kar == "OMER-SOR":
            yorum.append(f"# OMER-SOR: {k} | {n}")
            sayim["OMER-SOR"] += 1
        else:
            sayim[kar + "(hata10)"] += 1
    govde = []
    for y, s, lis in sorted(satirlar, key=lambda t: t[0]):
        l = (lis or "").strip()
        govde.append(s + (f"  # lisans: {l}" if l and l not in ("MIT", "Apache-2.0", "BSD-3-Clause") else ""))
    OUT.write_text(onsoz() + "\n".join(govde) + "\n\n" + "\n".join(yorum) + "\n", encoding="utf-8-sig")
    SAY.write_text(json.dumps({"betik_satiri": len(satirlar), "sayim": sayim}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(satirlar), dict(sayim))


main()
