import subprocess as s, time, sys
LOGP = r"C:\Projeler\omer-skills\.kos\kopru\log\msf_wsl_kur.log"
if len(sys.argv) < 2:
    s.Popen([sys.executable, __file__, "calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("arka planda basladi"); sys.exit(0)
LOG = open(LOGP, "w", encoding="utf-8", buffering=1)
def r(cmd, t):
    try:
        p = s.run(["wsl", "-d", "Ubuntu", "-u", "root", "-e", "bash", "-lc", cmd], capture_output=True, timeout=t)
        o = (p.stdout + p.stderr).decode("utf-8", "ignore")
        print(time.strftime("%H:%M:%S"), cmd[:90], "| exit", p.returncode, "|", o.strip()[-1500:], file=LOG)
        return p.returncode
    except Exception as e:
        print(time.strftime("%H:%M:%S"), cmd[:90], "| HATA", e, file=LOG); return -1
print("Windows'ta Defender Metasploit gem'lerini karantinaya aliyor (olay 1116/1117); WSL ext4 icine kuruluyor.", file=LOG)
r("command -v msfconsole && msfconsole --version", 60)
k = r("cd /root && curl -fsSL https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb -o msfinstall && chmod 755 msfinstall && DEBIAN_FRONTEND=noninteractive ./msfinstall", 3000)
r("command -v msfconsole && msfconsole -q -x 'version; exit' 2>&1 | tail -3", 600)
print("SONUC", "KURULDU" if k == 0 else "HATA", time.strftime("%H:%M:%S"), file=LOG)
