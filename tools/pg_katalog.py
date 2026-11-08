import subprocess as s, os, glob, time, sys
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000 | 0x00004000, close_fds=True); print("arka planda basladi"); sys.exit(0)
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\pg_katalog.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=out)
t = os.environ["TEMP"]
fs = sorted(glob.glob(t + r"\install-postgresql*.log") + glob.glob(t + r"\bitrock_installer*.log"), key=os.path.getmtime)
p("pg loglari", [os.path.basename(f) for f in fs[-3:]])
if fs:
    L = open(fs[-1], encoding="utf-8", errors="ignore").read().splitlines()
    hata = [l for l in L if any(k in l.lower() for k in ["error", "fail", "password", "exit code", "problem"])]
    p("hata satirlari:\n" + "\n".join(hata[-25:]))
    p("son 15:\n" + "\n".join(L[-15:]))
for d in [r"C:\Program Files\PostgreSQL\17\bin\postgres.exe", r"C:\Program Files\PostgreSQL\17\bin\psql.exe", r"C:\Program Files\PostgreSQL\17\data\PG_VERSION"]:
    p(d, os.path.exists(d))
p("servis:", s.run(["sc", "query", "postgresql-x64-17"], capture_output=True, text=True, errors="ignore").stdout.strip()[:300])
p("nvcc:", s.run(["powershell", "-NoProfile", "-Command", "Get-ChildItem 'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA' -Directory | % Name; & (Get-ChildItem 'C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\*\\bin\\nvcc.exe' | Select -First 1).FullName --version"], capture_output=True, text=True, errors="ignore", timeout=60).stdout.strip()[-300:])
r = s.run([sys.executable, r"C:\Projeler\omer-skills\tools\katalog_yenile.py"], cwd=r"C:\Projeler\omer-skills", capture_output=True, text=True, errors="ignore", timeout=1800)
p("katalog_yenile exit", r.returncode, (r.stdout + r.stderr).strip()[-600:])
p("BITTI")
