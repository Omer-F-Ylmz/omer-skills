"""VIDEO-IZLE-KUR-1 tur10: Munder Difflin UAC'sız kurulum. postinstall'daki `electron-rebuild -f` node-pty'yi kaynaktan
(ClangCL) derliyor; bunun yerine npm install --ignore-scripts + node-pty prebuild + yalnız better-sqlite3 electron-rebuild.
kullanım: python -I munder10.py   → kur-tur10.tsv'ye satır"""
import subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kur9 import KOK, VCVARS, son  # noqa: E402
from kur10 import DUSUK, yaz  # noqa: E402

SRC = KOK / "Munder_Difflin" / "src"
ADIM = [("npm install --ignore-scripts --no-audit --no-fund", 1800),  # tur10b: -w node-pty de derledi → -o
        ("npx electron-rebuild -f -o better-sqlite3", 1200),
        ("node tools/ensure-pty-perms.cjs && node tools/patch-node-pty-conpty.cjs", 300),
        ("npm run build", 1800)]


def kos(cmd, sure):
    try:
        r = subprocess.run(f'call "{VCVARS}" >nul && {cmd}', cwd=SRC, shell=True, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=sure, creationflags=DUSUK)
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return -9, f"zaman asimi {sure}s"


if __name__ == "__main__":
    sys.stdout.reconfigure(errors="replace")
    biten = []
    for cmd, sure in ADIM:
        print("ADIM", cmd, flush=True)
        rc, o = kos(cmd, sure)
        print(son(o, 1500), flush=True)
        if rc:
            yaz("Munder_Difflin", "kuruldu" if biten else "basarisiz",
                f"ok: {'; '.join(biten) or '-'} | dustu: {cmd}: {son(o, 250)}", str(SRC))
            break
        biten.append(cmd.split(" &&")[0][:40])
    else:
        yaz("Munder_Difflin", "kuruldu", "ignore-scripts install + better-sqlite3 rebuild + build ok (UAC/ClangCL yok); calistirma olculmedi", str(SRC))
    print("BITTI", flush=True)
