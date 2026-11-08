"""Postiz'i istek üzerine açar/kapatır (WSL Ubuntu + docker). Kullanım: python -I postiz_ac.py ac|kapat|durum"""
import subprocess, sys, time, urllib.request
from pathlib import Path

DAMGA = Path(__file__).resolve().parent / "son_ac.txt"

URL = "http://127.0.0.1:4007/api/auth/can-register"


def wsl(cmd, t=180):
    return subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "-e", "bash", "-c", cmd], capture_output=True, timeout=t, creationflags=0x08000000)


def ayakta():
    try:
        return urllib.request.urlopen(URL, timeout=5).status == 200
    except Exception:
        return False


def ubuntu_calisiyor():
    o = subprocess.run(["wsl", "-l", "--running", "-q"], capture_output=True, creationflags=0x08000000).stdout.decode("utf-16-le", "ignore")
    return "Ubuntu" in o


def ac(bekle=240):
    DAMGA.write_text(str(time.time()), encoding="utf-8")
    if ayakta():
        return True
    wsl("systemctl start docker; cd /opt/postiz && docker compose up -d", 300)
    son = time.time() + bekle
    while time.time() < son:
        if ayakta():
            return True
        time.sleep(5)
    return False


def kapat():
    if ubuntu_calisiyor():
        wsl("cd /opt/postiz && docker compose stop -t 20", 120)
        subprocess.run(["wsl", "--terminate", "Ubuntu"], capture_output=True, timeout=60, creationflags=0x08000000)
    return not ubuntu_calisiyor()


if __name__ == "__main__":
    k = sys.argv[1] if len(sys.argv) > 1 else "durum"
    if k == "ac":
        print("ac", ac())
    elif k == "kapat":
        print("kapat", kapat())
    else:
        print("ubuntu", ubuntu_calisiyor(), "postiz", ayakta())
