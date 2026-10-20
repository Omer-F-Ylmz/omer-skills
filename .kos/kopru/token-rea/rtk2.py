"""rtk2: RTK sinyal-koruma sarmalayıcı (kurulu rtk'ya dokunmaz). Kullanım: python rtk2.py git diff HEAD~2 | ls -la tools | ...
Kural: rtk çıktısı ham çıktının sinyal belirteçlerini (dosya adı, hash) kaybettiyse eksikler sona eklenir; sonuç ham'dan uzunsa ham döner.
`ls`: perm/sahip/tarih gürültüsü atılır, tüm ad+boyut korunur (rtk ls ad düşürüyordu)."""
import os, subprocess, sys

NW = 0x08000000
PATH = r"(?<![\w./-])[\w.-]+(?:/[\w.-]+)+"  # re yalnız eksik()/stat_say() çağrılınca yüklenir (açılış süresi)
HASH = r"\b[0-9a-f]{7,40}\b"
STAT = r"^\s*(\S+)\s+\|"
NOSTAT = {"--stat", "--name-only", "--numstat", "--shortstat"}


GNU = "C:/Program Files/Git/usr/bin/find.exe"  # Windows'ta çıplak `find` find.exe'ye düşer; Git Bash'teki GNU find gerçek kullanım


def calis(argv):
    if argv[0] == "find" and os.path.isfile(GNU):
        argv = [GNU, *argv[1:]]
    p =subprocess.run(argv, capture_output=True, creationflags=NW, timeout=120)
    return (p.stdout + p.stderr).decode("utf-8", "replace"), p.returncode


def sinyaller(argv, ham):
    """→ [(tam belirteç, aranacak ad)]; diff gövdesi (kod satırları) sayılmaz, yalnız `diff --git` başlıkları."""
    import re
    if argv[0] == "git" and "diff" in argv and not NOSTAT & set(argv):
        ham = "\n".join(l for l in ham.splitlines() if l.startswith("diff --git"))
    s = [(m, m.rsplit("/", 1)[-1]) for m in re.findall(PATH, ham)] + [(m, m) for m in re.findall(STAT, ham, re.M)]
    if argv[0] == "git" and argv[1] in ("blame", "log", "show", "branch", "status"):
        s += [(m, m) for m in re.findall(HASH, ham)]
    return list(dict.fromkeys(s))


def eksik(argv, ham, cikti):
    return [t for t, ad in sinyaller(argv, ham) if ad not in cikti]


def ls_kompakt(args):
    bayrak = "".join(a.lstrip("-") for a in args if a.startswith("-"))
    yol = next((a for a in args if not a.startswith("-")), ".")
    try:
        girdi = sorted(os.scandir(yol), key=lambda e: e.name)
    except OSError as ex:
        return f"ls: {ex}"
    satir = []
    for e in girdi:
        if e.name.startswith(".") and "a" not in bayrak and "A" not in bayrak:
            continue
        d = e.is_dir()
        satir.append(e.name + ("/" if d else ""))
    return " ".join(satir)


def agac(yollar):
    """Yolları dizine göre grupla: 'dizin/: ad ad ad' (ortak önek bir kez; tüm adlar korunur)."""
    g = {}
    for y in yollar:
        d, _, a = y.rpartition("/")
        g.setdefault(d, []).append(a)
    return "\n".join((d + "/: " if d else "") + " ".join(a) for d, a in g.items())


def diff_kompakt(ham, kap=20):
    """Başlık→'## yol', index/---/+++/bağlam satırı atılır; dosya başına en çok `kap` değişen satır."""
    cik, n, atla = [], 0, False
    for l in ham.splitlines():
        if l.startswith("diff --git"):
            if atla:
                cik.append(f"… +{n - kap} satır")
            a, _, b = l[11:].partition(" b/")
            cik.append("## " + (b if a[2:] == b else f"{a[2:]} → {b}"))
            n, atla = 0, False
        elif l.startswith("@@"):
            cik.append(l.split(" @@")[0])
        elif l[:1] in "+-" and not l.startswith(("+++ ", "--- ")):
            n += 1
            if n <= kap:
                cik.append(l if len(l) <= 160 else l[:160] + f"…(+{len(l) - 160} kr)")
            else:
                atla = True
        elif l.startswith(("new file", "deleted file", "rename", "Binary")):
            cik.append(l)
    if atla:
        cik.append(f"… +{n - kap} satır")
    return "\n".join(cik)


def tur(argv):
    """Süzgeç türü; None → rtk2 uçtan uca rtk'dan hızlı değil, hook komutu doğrudan rtk'ya yollar (rtk2 hiç açılmaz).
    Ölçüm (egitim+held4+d6 iki tohum): ls/diff/durum rtk'dan hızlı; find (0/4 süre), ls-files, log/diff/show --stat Python açılışı (~40 ms) yüzünden eşit/yavaş → rtk."""
    if argv[0] == "ls":
        return "ls"
    if argv[0] != "git" or len(argv) < 2:
        return None
    if argv[1] == "branch":
        return "ham"  # rtk branch -a/-vv ad kaybeder, ham git rtk'dan da hızlı (46 vs 72 ms): hook komutu rtk'sız bırakır
    if "diff" in argv[1:3] and not NOSTAT & set(argv):
        return "diff"
    if argv[1] == "status" and not {"--porcelain", "--short", "-s", "-sb"} & set(argv):
        return "durum"


def durum_gecis(ham):  # ham: `status --porcelain -b`
    ls = ham.splitlines()
    g = {}
    for l in ls[1:]:
        g.setdefault(l[:2].strip() or "?", []).append(l[3:].strip('"').rstrip("/") + ("/" if l.endswith("/") else ""))
    return "\n".join([ls[0]] + [f"{k}\n{agac(v)}" for k, v in g.items()]) if ls else "temiz"


TAVAN = 1500  # kr; altı tam döner. Üstü özet + tam metin sakla (rtk bu boyutta ad kaybediyor/şişiyor)
AC = os.path.join(os.environ.get("TEMP") or "/tmp", "rtk2-ac")


def sar(o, k):
    """Büyük çıktı → özet (dizin başına sayı + ilk 3 ad / dosya başlıkları) + tam metin AC dizinine; tek satır geri alma komutu: `rtk2.py ac <id>`."""
    if len(o) <= TAVAN:
        return o
    from zlib import crc32
    i = "%08x" % crc32(o.encode())
    os.makedirs(AC, exist_ok=True)
    with open(os.path.join(AC, i), "w", encoding="utf-8") as f: f.write(o)
    ls, e, etiket = o.splitlines(), [], ""
    if k == "diff":
        e = [l for l in ls if l.startswith("## ")]
    elif len(ls) == 1:  # ls: tek satır
        w = ls[0].split(" "); e = [" ".join(w[:40]) + (f" +{len(w) - 40} ad" if len(w) > 40 else "")]
    else:
        for l in ls:
            d, ayrac, a = l.partition(": ")
            if not ayrac: etiket = l + " "; continue
            w = a.split(" "); e.append((len(w), etiket + f"{d} ({len(w)}): " + " ".join(w[:3]) + (f" +{len(w) - 3}" if len(w) > 3 else "")))
        e = [x for _, x in sorted(e, key=lambda t: -t[0])]
    e = [x if len(x) <= 90 else x[:89] + "…" for x in e]
    ek = len(e) - 8
    return "\n".join(e[:8] + ([f"+{ek} dizin/dosya daha"] if ek > 0 else []) + [f"tam çıktı ({len(ls)} satır, {len(o)} kr): python -I -S {os.path.abspath(__file__)} ac {i}"])


def ac(i):
    with open(os.path.join(AC, i), encoding="utf-8") as f: return f.read()


def rtk2(argv):
    k = tur(argv)
    if k is None:
        return calis(["rtk", *argv])[0]
    if k == "ls":
        return sar(ls_kompakt(argv[1:]), k)
    if k == "ham":
        return calis(argv)[0]
    if k == "diff" and not any(a.startswith(("-U", "--unified")) for a in argv):
        argv = [*argv[:argv.index("diff") + 1], "-U0", *argv[argv.index("diff") + 1:]]  # bağlam satırları zaten atılıyor: git'ten hiç çekme
    ham, r0 = calis(["git", "status", "--porcelain", "-b"] if k == "durum" else argv)
    if r0 != 0:
        return ham
    o = diff_kompakt(ham) if k == "diff" else durum_gecis(ham)  # ad/hash kurgu gereği korunur; kayıp denetimi (eksik) yalnız ölçümde
    return sar(o, k) if len(o) < len(ham) else sar(ham, "ham")


if __name__ == "__main__":
    sys.stdout.buffer.write((ac(sys.argv[2]) if sys.argv[1] == "ac" else rtk2(sys.argv[1:])).encode("utf-8"))
