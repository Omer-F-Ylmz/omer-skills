import subprocess as s, sys, os, time
K = r"C:\Projeler\omer-skills"
CL = os.path.expanduser(r"~\.local\bin\claude.exe")
if len(sys.argv) < 2:
    print("kullanim: cc_arka.py <gorev.md> [devam_session_id]"); sys.exit(2)
gorev = sys.argv[1]
ad = os.path.splitext(os.path.basename(gorev))[0]
log = os.path.join(K, r".kos\kopru\log", f"cc_{ad}_{time.strftime('%H%M')}.jsonl")
args = [CL, "-p", "--model", "sonnet", "--effort", "medium", "--max-turns", "400",
        "--output-format", "stream-json", "--verbose"]
ek = sys.argv[2:]
if "hafif" in ek:
    args += ["--disable-slash-commands", "--strict-mcp-config", "--mcp-config", os.path.join(K, r"tmp\bos-mcp.json")]
    ek = [x for x in ek if x != "hafif"]
if ek and ek[0] != "yeni":
    args += ["--resume", ek[0]]
stdin = open(gorev, "rb")
out = open(log, "wb")
p = s.Popen(args, cwd=K, stdin=stdin, stdout=out, stderr=s.STDOUT,
            creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
print("basladi pid", p.pid, "log", log)
