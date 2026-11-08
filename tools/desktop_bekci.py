"""DESKTOP-BEKCI-1 (24 Eki): Claude Desktop kapalıysa yeniden açar. Zamanlanmış görev omer-desktop-bekci her 2 dk --tek koşar.
Kapatmak için: .kos/kopru/desktop-bekci.kapali dosyası oluştur (Ömer bilerek kapatıyorsa)."""
import subprocess, sys, time
from pathlib import Path

import psutil

KOK = Path(r"C:\Projeler\omer-skills")
KAPALI = KOK / ".kos/kopru/desktop-bekci.kapali"
LOG = KOK / ".kos/kopru/desktop-bekci.log"
SON = KOK / ".kos/kopru/desktop-bekci.son"
AUMID = r"shell:AppsFolder\Claude_pzs8sxrjxfjjc!Claude"
NW = 0x08000000


def yaz(m):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + m + "\n")


def calisiyor():
    for p in psutil.process_iter(["name", "exe"]):
        try:
            if (p.info["name"] or "").lower() == "claude.exe" and "windowsapps" in (p.info["exe"] or "").lower():
                return True
        except (psutil.Error, TypeError):
            continue
    return False


def tek():
    if KAPALI.exists() or calisiyor():
        return
    try:
        if time.time() - float(SON.read_text()) < 180:
            return
    except (OSError, ValueError):
        pass
    SON.write_text(str(time.time()))
    subprocess.Popen(["explorer.exe", AUMID], creationflags=NW)
    time.sleep(20)
    yaz("Claude Desktop kapalıydı → yeniden açıldı · açık mı: " + str(calisiyor()))


if __name__ == "__main__":
    tek()
