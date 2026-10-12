"""JEV-2 onay betiği — Desktop/Ömer koşar. CC tarafı canlı kopya değil: hook ve ölçümler main'deki tools/jev + tools/olcum'u
koşar, teslim = kol/jev2'nin main'e birleşmesi. ~/.claude'a dokunmaz; anahtar okumaz.

  python onay/jev_2_uygula.py --kuru   # plan: birleşecek commitler, çatışma ve Ömer'in commitsiz dosyalarıyla çakışma (varsayılan)
  python onay/jev_2_uygula.py uygula   # --kuru temizse main'de `git merge --no-ff kol/jev2`
  python onay/jev_2_uygula.py --geri   # son JEV-2 onay birleşmesini `git revert -m 1` ile geri alır
"""
import subprocess, sys
from pathlib import Path

ANA = Path("C:/Projeler/omer-skills")
DAL = "kol/jev2"
MESAJ = "JEV-2 onay birleşmesi: kol/jev2 → main"


def git(*a, kontrol=True):
    r = subprocess.run(["git", "-C", str(ANA), *a], capture_output=True, text=True, encoding="utf-8")
    if kontrol and r.returncode:
        sys.exit(f"git {' '.join(a)}: {r.stderr.strip()}")
    return r


def kuru():
    commitler = git("log", "--oneline", f"main..{DAL}").stdout.splitlines()
    degisen = set(git("diff", "--name-only", f"main...{DAL}").stdout.split())
    kirli = {s[3:].strip().strip('"') for s in git("status", "--porcelain").stdout.splitlines()}
    catisma = git("merge-tree", "--write-tree", "main", DAL, kontrol=False).returncode != 0
    cakisan = sorted(degisen & kirli)
    print(f"{len(commitler)} commit · {len(degisen)} dosya · çatışma {'VAR' if catisma else 'yok'} · commitsiz dosyayla çakışma {len(cakisan)}")
    for s in commitler:
        print("  ", s[:110])
    for f in cakisan:
        print("  ÇAKIŞAN:", f)
    temiz = bool(commitler) and not catisma and not cakisan
    print("TEMİZ" if temiz else "TEMİZ DEĞİL")
    return temiz


def main(arg):
    if arg == "--geri":
        sha = git("log", "--merges", "-1", "--format=%H", f"--grep={MESAJ}", "main").stdout.strip()
        if not sha:
            sys.exit("geri alınacak JEV-2 birleşmesi yok")
        git("revert", "-m", "1", "--no-edit", sha)
        print("geri alındı:", sha[:7])
    elif arg == "uygula":
        if git("branch", "--show-current").stdout.strip() != "main":
            sys.exit("ana çalışma ağacı main'de değil")
        if not kuru():
            sys.exit(1)
        git("merge", "--no-ff", DAL, "-m", MESAJ)
        print("birleşti:", git("rev-parse", "--short", "HEAD").stdout.strip())
    else:
        sys.exit(0 if kuru() else 1)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "--kuru")
