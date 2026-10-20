"""rtk2: RTK sinyal-koruma sarmalayıcı (kurulu rtk'ya dokunmaz). Kullanım: python rtk2.py git diff HEAD~2 | ls -la tools | ...
Kural: rtk çıktısı ham çıktının sinyal belirteçlerini (dosya adı, hash) kaybettiyse eksikler sona eklenir; sonuç ham'dan uzunsa ham döner.
`ls`: perm/sahip/tarih gürültüsü atılır, tüm ad+boyut korunur (rtk ls ad düşürüyordu)."""
import os, re, subprocess, sys

NW = 0x08000000
PATH = re.compile(r"(?<![\w./-])[\w.-]+(?:/[\w.-]+)+")
HASH = re.compile(r"\b[0-9a-f]{7,40}\b")
STAT = re.compile(r"^\s*(\S+)\s+\|", re.M)


GNU = "C:/Program Files/Git/usr/bin/find.exe"  # Windows'ta çıplak `find` find.exe'ye düşer; Git Bash'teki GNU find gerçek kullanım


def calis(argv):
    if argv[0] == "find" and os.path.isfile(GNU):
        argv = [GNU, *argv[1:]]
    p =subprocess.run(argv, capture_output=True, creationflags=NW, timeout=120)
    return (p.stdout + p.stderr).decode("utf-8", "replace"), p.returncode


def sinyaller(argv, ham):
    """→ [(tam belirteç, aranacak ad)]; diff gövdesi (kod satırları) sayılmaz, yalnız `diff --git` başlıkları."""
    if argv[0] == "git" and "diff" in argv and not {"--stat", "--name-only", "--numstat", "--shortstat"} & set(argv):
        ham = "\n".join(l for l in ham.splitlines() if l.startswith("diff --git"))
    s = [(m, m.rsplit("/", 1)[-1]) for m in PATH.findall(ham)] + [(m, m) for m in STAT.findall(ham)]
    if argv[0] == "git" and argv[1] in ("blame", "log", "show", "branch", "status"):
        s += [(m, m) for m in HASH.findall(ham)]
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


STATSAT = re.compile(r"^ (.+?)\s+\|\s+(\d+)\s[+-]*$", re.M)


def stat_say(m):  # histogram çubuğu atılır, ad+sayı kalır
    return f" {m.group(1)} {m.group(2)}"


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


def tek_gecis(argv, ham):
    """rtk'ya gitmeden, ham çıktıyı bir kez süzer; süzgeç yoksa None."""
    if argv[0] == "find" or argv[:2] == ["git", "ls-files"]:
        return agac([l.removeprefix("./") for l in ham.splitlines()])
    if argv[0] == "git" and "diff" in argv[1:2] + argv[2:3] and not {"--stat", "--name-only", "--numstat", "--shortstat"} & set(argv):
        return diff_kompakt(ham)
    if argv[:2] == ["git", "status"] and not {"--porcelain", "--short", "-s", "-sb"} & set(argv):
        p, _ = calis(["git", "status", "--porcelain", "-b"])
        ls = p.splitlines()
        g = {}
        for l in ls[1:]:
            g.setdefault(l[:2].strip() or "?", []).append(l[3:].strip('"').rstrip("/") + ("/" if l.endswith("/") else ""))
        return "\n".join([ls[0]] + [f"{k}\n{agac(v)}" for k, v in g.items()]) if ls else "temiz"
    if argv[0] == "git" and argv[1] in ("log", "show", "diff") and "--stat" in argv:
        return STATSAT.sub(stat_say, ham)
    return None


def rtk2(argv):
    if argv[0] == "ls":
        return ls_kompakt(argv[1:])
    ham, r0 = calis(argv)
    if r0 != 0:
        return ham
    if (o := tek_gecis(argv, ham)) is not None and not eksik(argv, ham, o):
        return o if len(o) < len(ham) else ham
    out, r1 = calis(["rtk", *argv])
    if r1 != 0 or not out.strip():
        return ham
    if m := eksik(argv, ham, out):
        out += "\n[rtk2 eksik]\n" + "\n".join(m)
    return out if len(out) < len(ham) else ham


if __name__ == "__main__":
    sys.stdout.buffer.write(rtk2(sys.argv[1:]).encode("utf-8"))
