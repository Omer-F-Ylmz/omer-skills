"""RAM-KAPI: NİHAİ kaynak kuralı — RAM >=%95 iken en düşük öncelikli iş ağacını askıya alır (öldürmez), <%88 olunca sırayla devam ettirir."""
import os, time, json, psutil
KOPRU = r"C:\Projeler\omer-skills\.kos\kopru"
LOG = os.path.join(KOPRU, "log", "ram-kapi.log")
DURUM = os.path.join(KOPRU, "ram-kapi.json")
UST, ALT = 95.0, 91.0
ONCELIK = [
    # borsa-egit MUAF (Ömer 6 Kas 2026): RAM %99 olsa bile borsa eğitimi askıya alınmaz.
    ("kategori-kapsam", lambda c: False),
    ("is6-ecc", lambda c: False),
    ("kategori-1", lambda c: False),
    ("cm-chroma-fix", lambda c: False),
    ("calistir-hepsi", lambda c: "ajan_arka_calistir-hepsi" in c or "calistir_hepsi.py" in c),
]


def say(*a):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(map(str, a)) + "\n")


def kilit_pid(ad):
    try:
        return int(open(os.path.join(KOPRU, "arka", ad + ".kilit")).read().strip())
    except Exception:
        return None


def agac(ad, esle):
    kok = []
    pid = kilit_pid(ad)
    if pid and psutil.pid_exists(pid):
        kok.append(psutil.Process(pid))
    for p in psutil.process_iter(["cmdline"]):
        try:
            c = " ".join(p.info["cmdline"] or [])
            if esle(c) and p.pid not in [k.pid for k in kok]:
                kok.append(p)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    hepsi = {}
    for k in kok:
        try:
            hepsi[k.pid] = k
            for ch in k.children(recursive=True):
                hepsi[ch.pid] = ch
        except psutil.NoSuchProcess:
            pass
    return list(hepsi.values())


def uygula(ad, esle, islem):
    n = 0
    for p in agac(ad, esle):
        try:
            getattr(p, islem)()
            n += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return n


def yukle():
    try:
        ad = dict(ONCELIK)
        return [a for a in json.load(open(DURUM, encoding="utf-8")) if a in ad]
    except Exception:
        return []


def kaydet(askida):
    json.dump(askida, open(DURUM, "w", encoding="utf-8"))


def tur(askida):
    ram = psutil.virtual_memory().percent
    if ram >= UST:
        for ad, esle in ONCELIK:
            if ad in askida:
                continue
            n = uygula(ad, esle, "suspend")
            if n:
                askida.append(ad)
                say(f"RAM %{ram:.1f} >= {UST}: ASKIYA {ad} ({n} süreç)")
                return askida
        say(f"RAM %{ram:.1f}: askıya alınacak iş kalmadı")
    elif ram < ALT and askida:
        ad = askida.pop()
        esle = dict(ONCELIK)[ad]
        n = uygula(ad, esle, "resume")
        say(f"RAM %{ram:.1f} < {ALT}: DEVAM {ad} ({n} süreç)")
    return askida


if __name__ == "__main__":
    say("BASLADI")
    askida = yukle()
    while True:
        try:
            askida = tur(askida)
            kaydet(askida)
        except Exception as e:
            say("HATA", repr(e)[:200])
        time.sleep(45)
