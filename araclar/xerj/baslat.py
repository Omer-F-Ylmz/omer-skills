"""XERJ düğümü (yalnız 127.0.0.1, --insecure): python .kos/kopru/arka.py araclar/xerj/arka.log araclar/xerj/baslat.py
Pencere açmaz (CREATE_NO_WINDOW); düğüm ölürse betik de biter. Dizin indeksleme: baslat.py indeksle <klasör> <önek>."""
import os, subprocess, sys
kok = os.path.dirname(os.path.abspath(__file__))
exe = os.path.join(kok, "bin", "xerj-1.0.0-rc.98-x86_64-pc-windows-msvc", "xerj.exe")
veri = os.path.join(kok, "veri")
env = dict(os.environ, XERJ_DISABLE_FEEDBACK="true")
if sys.argv[1:2] == ["indeksle"]:
    kl, onek = sys.argv[2], sys.argv[3]
    sys.exit(subprocess.run([exe, "autoindex", kl, "--prefix", onek, "--yes", *sys.argv[4:]], env=env, creationflags=0x08000000).returncode)
os.makedirs(veri, exist_ok=True)
sys.exit(subprocess.run([exe, "--insecure", "--data-dir", veri, "--bind", "127.0.0.1"], env=env, creationflags=0x08000000).returncode)
