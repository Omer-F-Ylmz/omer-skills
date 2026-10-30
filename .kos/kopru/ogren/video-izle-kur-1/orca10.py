"""VIDEO-IZLE-KUR-1 tur10: Orca derlemesi. Kök neden (tur10): typecheck TS2307 = package.json'da bildirilmemiş geçişli modüller
(playwright, rolldown, @electron/asar, @tiptap/* 3.31.3, mdast/micromark/unist/vfile, @dnd-kit/utilities, @testing-library/dom);
pnpm add -w -D ile eklendi → node/web/cli typecheck 0 hata. Burada build:cli + build:electron-vite, sonra CLI --help."""
import glob, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kur9 import KOK, VCVARS, son  # noqa: E402
from kur10 import DUSUK, yaz  # noqa: E402

SRC = KOK / "Orca" / "src"


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
    for cmd in ("npx -y pnpm@9 run build:cli", "npx -y pnpm@9 run build:electron-vite"):
        print("ADIM", cmd, flush=True)
        rc, o = kos(cmd, 2700)
        print(son(o, 1500), flush=True)
        if rc:
            yaz("Orca", "kuruldu", f"typecheck 3/3 ok; ok: {'; '.join(biten) or '-'} | dustu: {cmd}: {son(o, 250)}", str(SRC))
            break
        biten.append(cmd.split()[-1])
    else:
        cli = [p for p in glob.glob(str(SRC / "out" / "**" / "*cli*.js"), recursive=True)][:1]
        rc, h = kos(f'node "{cli[0]}" --help', 60) if cli else (1, "cli cikti yok")
        yaz("Orca", "calisiyor" if rc == 0 else "kuruldu",
            f"typecheck 3/3 ok; build:cli + build:electron-vite ok; cli --help rc={rc}: {son(h, 120)}", str(SRC))
    print("BITTI", flush=True)
