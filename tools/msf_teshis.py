import subprocess as s, time, sys, os, stat, glob
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\msf_teshis.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def p(*a): print(time.strftime("%H:%M:%S"), *a, file=LOG)
c = os.path.expanduser(r"~\.local\share\gem\ruby\3.4.0\cache")
p("cache var mi", os.path.isdir(c))
for f in sorted(glob.glob(os.path.join(c, "rex-exploitation*")) + glob.glob(os.path.join(c, "*.gem")))[:3]:
    try:
        st = os.stat(f); a = st.st_file_attributes
        p(f, st.st_size, hex(a), "REPARSE" if a & 0x400 else "-", "COMPRESSED" if a & 0x800 else "-")
    except Exception as e: p(f, "HATA", e)
r = s.run(["compact", os.path.join(c, "rex-exploitation-0.1.44.gem")], capture_output=True, timeout=30)
p("compact:", (r.stdout + r.stderr).decode("cp857", "ignore").strip()[-400:])
r = s.run(["compact", c], capture_output=True, timeout=60)
p("compact dizin:", (r.stdout + r.stderr).decode("cp857", "ignore").strip()[-500:])
log = os.path.expanduser(r"~\Desktop\Claude ile yap\u0131lanlar\araclar\guvenlik\_indir\msf-bundle.log")
try:
    t = open(log, encoding="utf-8", errors="ignore").read()
    i = t.find("Errno"); p("hata cevresi:", t[max(0, i-1500):i+600] if i >= 0 else t[:2000])
except Exception as e: p("log okunamadi", e)
p("BITTI")
