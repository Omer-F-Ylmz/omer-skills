import subprocess
def kos(args, t):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=t)
    print(">", " ".join(args[-4:]), "exit", r.returncode)
    print((r.stdout or "")[-1500:])
    print((r.stderr or "")[-800:])
    return r.returncode
kos(["wsl", "-u", "root", "-e", "dpkg", "--configure", "-a"], 300)
kos(["wsl", "-u", "root", "-e", "env", "DEBIAN_FRONTEND=noninteractive", "apt-get", "install", "-y", "wifite"], 540)
kos(["wsl", "-u", "root", "-e", "sh", "-c", "command -v wifite && dpkg -s wifite | grep -E 'Status|Version'"], 60)
