import subprocess as s, os, sys, time
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(r"C:\Projeler\omer-skills\.kos\kopru\log\ek_teshis.log", "w", encoding="utf-8", buffering=1)
def p(*a): print(*a, file=LOG)
t = os.path.join(os.environ["TEMP"], "blender-f2.log")
p("== blender-f2.log"); p(open(t, encoding="utf-8", errors="ignore").read()[-2500:] if os.path.exists(t) else "YOK")
code = s.run(["where", "code"], capture_output=True, text=True, errors="ignore").stdout.strip().splitlines()
p("== code yolu", code)
if code:
    c = code[0]
    for ext in ["GitHub.copilot", "GitHub.copilot-chat"]:
        r = s.run([c, "--install-extension", ext, "--force"], capture_output=True, text=True, errors="ignore", timeout=300, shell=True)
        p("==", ext, "exit", r.returncode, (r.stdout + r.stderr).strip()[-800:])
    r = s.run([c, "--list-extensions"], capture_output=True, text=True, errors="ignore", timeout=120, shell=True)
    p("== listede copilot:", [l for l in r.stdout.splitlines() if "copilot" in l.lower()])
p("BITTI", time.strftime("%H:%M:%S"))
