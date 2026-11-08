import glob, os, sqlite3, time, subprocess as s, sys
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True); sys.exit(0)
out = open(r"C:\Projeler\omer-skills\.kos\kopru\log\winget_idx_bak.log", "w", encoding="utf-8", buffering=1)
def at(f):
    a = os.stat(f).st_file_attributes
    return f"{os.path.getsize(f)//1024}KB {'REPARSE/WOF' if a & 0x400 else '-'} {'COMP' if a & 0x800 else '-'}"
yerler = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Packages\Microsoft.Winget.Source_8wekyb3d8bbwe\**\*"), recursive=True)
yerler += glob.glob(r"C:\Program Files\WindowsApps\Microsoft.Winget.Source_*\**\*.db", recursive=True)
for f in yerler:
    if os.path.isfile(f):
        try: print(f[-120:], at(f), file=out)
        except Exception as e: print(f[-120:], "HATA", e, file=out)
for f in [x for x in yerler if x.endswith(".db")][:3]:
    t0 = time.time()
    try:
        c = sqlite3.connect(f"file:{f}?mode=ro", uri=True, timeout=10)
        n = c.execute("select count(*) from sqlite_master").fetchone()
        print("ACILDI", f[-80:], n, f"{time.time()-t0:.1f}sn", file=out)
    except Exception as e:
        print("ACILAMADI", f[-80:], repr(e)[:150], f"{time.time()-t0:.1f}sn", file=out)
d = os.path.expandvars(r"%LOCALAPPDATA%\Packages\Microsoft.Winget.Source_8wekyb3d8bbwe")
r = s.run(["compact", "/s:" + d], capture_output=True, timeout=60)
print("compact:", (r.stdout + r.stderr).decode("cp857", "ignore").strip()[-400:], file=out)
print("BITTI", file=out)
