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
        satir.append(e.name + ("/" if d else "") + (f" {e.stat().st_size}" if "l" in bayrak and not d else ""))
    return "\n".join(satir)


def rtk2(argv):
    if argv[0] == "ls":
        return ls_kompakt(argv[1:])
    ham, r0 = calis(argv)
    if r0 != 0:
        return ham
    out, r1 = calis(["rtk", *argv])
    if r1 != 0 or not out.strip():
        return ham
    if m := eksik(argv, ham, out):
        out += "\n[rtk2 eksik]\n" + "\n".join(m)
    return out if len(out) < len(ham) else ham


if __name__ == "__main__":
    sys.stdout.buffer.write(rtk2(sys.argv[1:]).encode("utf-8"))
