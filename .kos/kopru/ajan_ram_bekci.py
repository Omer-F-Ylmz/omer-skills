"""RAM-BEKCI-1: yönetici ana döngüsünün RAM bekçisi (Desktop 23 Eki 23:16, RAM %89.8: kaçak grep + tam repo graphify update).
RAM >= ADAY_ESIK (87) → ajanların alt süreç ağacındaki en büyük çalışma kümesi bulunup günlüğe yazılır; >= DUR_ESIK (88) → o süreç ağacı durdurulur.
Hedef yalnız yöneticinin başlattığı ajan köklerinin (claude.exe) alt/torun süreçleri; kökler, Headroom, Claude Desktop, Chrome, sistem süreçleri izin listesindedir."""
import os

ADAY_ESIK, DUR_ESIK = 87, 88
# izin listesi: ad (küçük harf) ya da komut satırında geçen parça → asla hedef değil
IZIN_AD = {"claude.exe", "chrome.exe", "headroom.exe", "system", "registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe",
           "lsass.exe", "svchost.exe", "winlogon.exe", "dwm.exe", "explorer.exe", "msmpeng.exe", "conhost.exe", "cmd.exe", "bash.exe"}
IZIN_KOMUT = ("headroom", "claude desktop", "claude.exe")


def surecler_listele():
    """[(pid, ppid, ad, ws_bayt, komut)] — psutil; erişilemeyen süreç atlanır."""
    import psutil
    s = []
    for p in psutil.process_iter(["pid", "ppid", "name", "memory_info", "cmdline"]):
        try:
            i = p.info
            s.append((i["pid"], i["ppid"], (i["name"] or "").lower(), i["memory_info"].rss if i["memory_info"] else 0, " ".join(i["cmdline"] or [])))
        except Exception:
            pass
    return s


def izinli(ad, komut):
    return ad.lower() in IZIN_AD or any(k in komut.lower() for k in IZIN_KOMUT)


def hedef_sec(surecler, kokler):
    """kokler (ajan claude.exe pid'leri) altındaki alt/torun süreçlerden izin listesinde olmayan EN BÜYÜK çalışma kümeli; yoksa None."""
    cocuk = {}
    for s in surecler:
        cocuk.setdefault(s[1], []).append(s)
    altlar, kuyruk, gorulen = [], list(kokler), set(kokler)
    while kuyruk:
        for s in cocuk.get(kuyruk.pop(), []):
            if s[0] not in gorulen:
                gorulen.add(s[0])
                altlar.append(s)
                kuyruk.append(s[0])
    aday = [s for s in altlar if not izinli(s[2], s[4]) and s[0] != os.getpid()]
    return max(aday, key=lambda s: s[3]) if aday else None


def oldur_agac(pid):
    import subprocess
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True, creationflags=0x08000000)


def kontrol(r, kokler, surecler, oldur, log):
    """(durum, hedef): durum None (RAM düşük) | 'aday' (>=87, yalnız günlük) | 'durdurdu' (>=88) | 'hedef-yok'."""
    if r < ADAY_ESIK:
        return None, None
    h = hedef_sec(surecler, kokler)
    if h is None:
        log("RAM-BEKÇİ", f"RAM %{r}", "hedef yok (ajan alt süreci bulunamadı ya da hepsi izin listesinde)")
        return "hedef-yok", None
    ayr = f"pid {h[0]} {h[2]} {h[3] // 2**20} MB · {h[4][:80]}"
    if r < DUR_ESIK:
        log("RAM-BEKÇİ", f"RAM %{r}", "ADAY", ayr)
        return "aday", h
    oldur(h[0])
    log("RAM-BEKÇİ", f"RAM %{r}", "DURDURULDU", ayr)
    return "durdurdu", h
