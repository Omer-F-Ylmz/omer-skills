import subprocess as s, os, time, sys
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000 | 0x00004000, close_fds=True); print("arka planda basladi"); sys.exit(0)
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\pg_kume.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=out)
B = r"C:\Program Files\PostgreSQL\17\bin"
D = os.path.join(os.environ["USERPROFILE"], "Desktop", "Claude ile yap\u0131lanlar", "araclar", "postgres17-veri")
env = dict(os.environ, LC_ALL="C", LANG="C")
def r(a, t=300):
    x = s.run(a, capture_output=True, text=True, errors="ignore", timeout=t, env=env)
    p(" ".join(a)[-120:], "| exit", x.returncode, "|", (x.stdout + x.stderr).strip()[-900:]); return x.returncode
if not os.path.exists(os.path.join(D, "PG_VERSION")):
    r([os.path.join(B, "initdb.exe"), "-D", D, "-U", "postgres", "-E", "UTF8", "--locale=C", "--lc-messages=C", "-A", "trust"])
conf = os.path.join(D, "postgresql.conf")
if os.path.exists(conf):
    t = open(conf, encoding="utf-8").read()
    if "listen_addresses = 'localhost'  # 8 Kas" not in t:
        open(conf, "a", encoding="utf-8").write("\nlisten_addresses = 'localhost'  # 8 Kas: yalniz yerel\nport = 5432\n")
r([os.path.join(B, "pg_ctl.exe"), "-D", D, "-l", os.path.join(D, "sunucu.log"), "start", "-w", "-t", "60"], 120)
r([os.path.join(B, "psql.exe"), "-h", "localhost", "-U", "postgres", "-c", "select version();"], 60)
p("BITTI veri:", D)
