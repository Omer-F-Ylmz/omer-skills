"""ERTELE-2 tur5: plugin ajan description'ını tek satırlık özete indirir, tam metni gövdeye '## Ne zaman' olarak taşır.

python tools/ajan_aciklama_tasi.py            # uygula (idempotent; yedek tmp/ertele6/yedek)
python tools/ajan_aciklama_tasi.py --kanca    # SessionStart: plugin kaydı değişmediyse hemen çık
python tools/ajan_aciklama_tasi.py --geri     # yedekten geri yükle
python tools/ajan_aciklama_tasi.py --kuru     # yazmadan say
"""
import glob, hashlib, json, os, re, shutil, sys

H = os.path.expanduser("~/.claude")
KOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tmp", "ertele6")
YEDEK = os.path.join(KOK, "yedek")
MANIFEST = os.path.join(KOK, "manifest.json")
IMZA = os.path.join(KOK, "imza.json")
ISARET = "<!-- ertele6: description buradan taşındı -->"
SINIR = 160
FM = re.compile(r"\A(﻿?---\r?\n)(.*?)(\r?\n---\r?\n)", re.S)
ANAHTAR = re.compile(r"^[A-Za-z_][\w-]*\s*:")


def imza():
    p = os.path.join(H, "plugins")
    return {f: (os.stat(os.path.join(p, f)).st_mtime_ns if os.path.exists(os.path.join(p, f)) else 0)
            for f in ("installed_plugins.json", "known_marketplaces.json")}


def ozet(d):
    d = re.sub(r"<example>.*?</example>", " ", d, flags=re.S | re.I)
    d = re.split(r"\b(?:Examples?|Örnekler?)\s*:", d)[0]
    d = re.sub(r"<[^>]+>", " ", d)
    d = re.sub(r"\s+", " ", d).strip()
    cumle = re.split(r"(?<=[.!?])\s+", d)
    s = cumle[0]
    if len(s) < 50 and len(cumle) > 1:
        s += " " + cumle[1]
    if len(s) > SINIR:
        s = s[:SINIR].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return s


def donustur(metin):
    m = FM.match(metin)
    if not m or ISARET in metin:
        return None
    nl = "\r\n" if "\r\n" in m.group(1) + m.group(3) else "\n"
    satir = m.group(2).split(nl)
    i = next((k for k, s in enumerate(satir) if s.startswith("description:")), None)
    if i is None:
        return None
    j = next((k for k in range(i + 1, len(satir)) if ANAHTAR.match(satir[k])), len(satir))
    try:
        eski = str(__import__("yaml").safe_load(nl.join(satir[i:j]))["description"])
    except Exception:
        eski = nl.join(satir[i:j])[len("description:"):].strip().strip("'\"")
    if len(eski) <= SINIR:
        return None
    satir[i:j] = ["description: " + json.dumps(ozet(eski), ensure_ascii=False)]
    govde = metin[m.end():]
    ek = nl.join([ISARET, "## Ne zaman", "", eski.strip(), "", ""])
    return m.group(1) + nl.join(satir) + m.group(3) + ek + govde


def uygula(kuru=False):
    os.makedirs(YEDEK, exist_ok=True)
    man = json.load(open(MANIFEST, encoding="utf-8")) if os.path.exists(MANIFEST) else {}
    n = once = sonra = 0
    for f in glob.glob(os.path.join(H, "plugins", "cache", "**", "agents", "**", "*.md"), recursive=True):
        ham = open(f, "rb").read()
        try:
            yeni = donustur(ham.decode("utf-8"))
        except UnicodeDecodeError:
            continue
        if yeni is None:
            continue
        n += 1; once += len(ham); sonra += len(yeni.encode("utf-8"))
        if kuru:
            continue
        h = hashlib.sha256(ham).hexdigest()
        y = os.path.join(YEDEK, hashlib.sha1(f.encode()).hexdigest()[:16] + ".md")
        if not os.path.exists(y) or man.get(f, {}).get("once") != h:
            open(y, "wb").write(ham)
        b = yeni.encode("utf-8")
        open(f, "wb").write(b)
        man[f] = {"yedek": y, "once": h, "sonra": hashlib.sha256(b).hexdigest()}
    if not kuru:
        json.dump(man, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(imza(), open(IMZA, "w", encoding="utf-8"))
    print(json.dumps({"donusen": n, "manifest": len(man), "kuru": kuru}, ensure_ascii=False))


def geri():
    man = json.load(open(MANIFEST, encoding="utf-8"))
    n = atla = 0
    for f, v in man.items():
        if not os.path.exists(f):
            atla += 1; continue
        if hashlib.sha256(open(f, "rb").read()).hexdigest() != v["sonra"]:
            atla += 1; continue  # cache güncellenmiş; eski yedeği yazma
        shutil.copyfile(v["yedek"], f); n += 1
    os.replace(MANIFEST, MANIFEST + ".geri")
    if os.path.exists(IMZA):
        os.replace(IMZA, IMZA + ".geri")
    print(json.dumps({"geri": n, "atlanan": atla}))


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--geri" in a:
        geri()
    elif "--kanca" in a:
        if os.path.exists(MANIFEST) and os.path.exists(IMZA) and json.load(open(IMZA)) == imza():
            sys.exit(0)
        if os.path.exists(MANIFEST):
            uygula()
    else:
        uygula("--kuru" in a)
