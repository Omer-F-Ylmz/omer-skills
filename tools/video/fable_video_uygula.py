"""FABLE-VIDEO d3 onay betiği: kol/fable-video2 → main birleştirme (video16_uygula.py kopyası). kol/fable-video2 kol/video-shorts ucundan
açıldı: VİDEO-16 önce uygulandıysa yalnız FABLE-VIDEO commit'leri gelir, uygulanmadıysa VİDEO-16 (short low) da birlikte gelir.
Birleştirince short/uzun Sonnet taramasına video-özel protokol öneki varsayılan açık (VIDEO_FABLE_PROTOKOL=0 kapatır; Haiku hariç).
Kullanım: python fable_video_uygula.py [--kuru | uygula | --geri]   (varsayılan --kuru: yalnız rapor, hiçbir şey değişmez)
uygula: main'deki commitsiz dosyalarla örtüşme ya da birleştirme çakışması varsa reddeder; önceki main ucu + birleştirme .kos/fv3/onay-once.txt.
--geri: birleştirme commit'i `git revert -m 1` ile geri alınır (commitsiz dosyalara dokunulmaz).
"""
import subprocess
import sys
from pathlib import Path

ANA = Path(r"C:\Projeler\omer-skills")
KOL = "kol/fable-video2"


def git(repo, *a, kontrol=True):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, encoding="utf-8", errors="replace")
    if kontrol and r.returncode:
        sys.exit(f"git {' '.join(a)}: {r.stderr.strip()[:300]}")
    return r


def main(arg="--kuru", repo=ANA, kol=KOL):
    kayit = repo / ".kos" / "fv3" / "onay-once.txt"
    dal = git(repo, "branch", "--show-current").stdout.strip()
    if arg == "--geri":
        if not kayit.is_file():
            sys.exit("geri: kayıt yok (uygula koşulmamış)")
        once, birles = kayit.read_text(encoding="utf-8").split()
        if dal != "main":
            sys.exit(f"geri: {repo} main'de değil ({dal})")
        git(repo, "revert", "-m", "1", "--no-edit", birles)
        kayit.unlink()
        print(f"geri alındı: {birles[:8]} revert edildi (önceki uç {once[:8]})")
        return
    degisen = set(git(repo, "diff", "--name-only", f"main...{kol}").stdout.split())
    kirli = {s[3:].strip('"') for s in git(repo, "status", "--porcelain").stdout.splitlines()}
    ortusen = sorted(degisen & kirli)
    cakisma = git(repo, "merge-tree", "--write-tree", "main", kol, kontrol=False).returncode != 0
    print(f"{kol} → main: {len(git(repo, 'rev-list', f'main..{kol}').stdout.split())} commit, {len(degisen)} dosya · "
          f"commitsiz örtüşen: {ortusen or 'yok'} · çakışma: {'VAR' if cakisma else 'yok'} · main dalda: {dal == 'main'}")
    if arg != "uygula":
        print("kuru: değişiklik yok. Uygulamak için: python fable_video_uygula.py uygula")
        return
    if ortusen or cakisma or dal != "main":
        sys.exit("uygula reddedildi (örtüşme/çakışma/dal)")
    once = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "merge", "--no-ff", "--no-edit", "-m", f"FABLE-VIDEO: {kol} → main (video-özel protokol öneki varsayılan açık)", kol)
    birles = git(repo, "rev-parse", "HEAD").stdout.strip()
    kayit.parent.mkdir(parents=True, exist_ok=True)
    kayit.write_text(f"{once} {birles}\n", encoding="utf-8")
    print(f"uygulandı: {birles[:8]} (önceki {once[:8]}); geri: python fable_video_uygula.py --geri")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(*sys.argv[1:2])
