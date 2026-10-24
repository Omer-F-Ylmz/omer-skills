"""RAM-BEKCI-1: yönetici ana döngüsünün RAM bekçisi (Desktop 23 Eki 23:16, RAM %89.8: kaçak grep + tam repo graphify update).
RAM >= ADAY_ESIK (87) → ajanların alt süreç ağacındaki en büyük çalışma kümesi bulunup günlüğe yazılır; >= DUR_ESIK (88) → o süreç ağacı durdurulur.
Hedef yalnız yöneticinin başlattığı ajan köklerinin (claude.exe) alt/torun süreçleri; kökler, Headroom, Claude Desktop, Chrome, sistem süreçleri izin listesindedir."""
import importlib.util
import os

ADAY_ESIK, DUR_ESIK = 87, 88
# RAM-BEKCI-2 (24 Eki 09:45, oyun açıkken claude -p ağacı 93 alt süreç/2.5 GB, RAM %98): tek alt süreç yetmedi → >= AGAC_ESIK'te ajan ağacının tamamı
AGAC_ESIK, UYARI_RAM, UYARI_MB, UYARI_ALT = 92, 80, 1536, 60
TEK_MIN_MB = 600
# izin listesi: ad (küçük harf) ya da komut satırında geçen parça → asla hedef değil
IZIN_AD = {"claude.exe", "chrome.exe", "headroom.exe", "system", "registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe",
           "lsass.exe", "svchost.exe", "winlogon.exe", "dwm.exe", "explorer.exe", "msmpeng.exe", "conhost.exe", "cmd.exe", "bash.exe"}
IZIN_KOMUT = ("headroom", "claude desktop", "claude.exe")


def _oyunlar():
    try:
        sp = importlib.util.spec_from_file_location("oyun_modu", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools", "oyun_modu.py"))
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return set(m.OYUNLAR)
    except Exception:
        return {"zenlesszonezero.exe", "genshinimpact.exe", "yuanshen.exe", "client-win64-shipping.exe"}


# ağaç durdurmada ASLA dokunulmayan (kendileri ve altları): oyunlar + başlatıcıları, Desktop (WindowsApps), Headroom, sistem
KORUMA_AD = _oyunlar() | {"epicgameslauncher.exe", "epicwebhelper.exe", "hoyoplay.exe", "hyp.exe", "explorer.exe", "system", "registry", "smss.exe",
                          "csrss.exe", "wininit.exe", "services.exe", "lsass.exe", "svchost.exe", "winlogon.exe", "dwm.exe", "msmpeng.exe", "headroom.exe"}
KORUMA_KOMUT = ("windowsapps", "headroom", "hoyoplay", "hoyoverse", "epic games", "epicgames", "kuro")


# TARAYICI-KAPI-1: ajan alt süreçleri varsayılan tarayıcıyı (Opera) açmasın (node `open`, vite/next --open, react-scripts vb.)
TARAYICI_ENV = {"BROWSER": "none", "CI": "1", "OPEN_BROWSER": "false"}
TARAYICI_AD = {"opera.exe", "msedge.exe"}


def tarayici_kapat(surecler, kokler, oldur, log):
    """kokler (ajan claude.exe pid'leri) ağacında kalan opera/msedge süreçlerini oldur(pidler) ile kapatır, günlüğe yazar; kapatılan pidler.
    Ajan ağacı dışındakine (kullanıcının kendi tarayıcısı) dokunulmaz."""
    cocuk = {}
    for s in surecler:
        cocuk.setdefault(s[1], []).append(s)
    pidler, kuyruk, gorulen = [], list(kokler), set(kokler)
    while kuyruk:
        for s in cocuk.get(kuyruk.pop(), []):
            if s[0] not in gorulen:
                gorulen.add(s[0])
                kuyruk.append(s[0])
                if s[2].lower() in TARAYICI_AD:
                    pidler.append(s[0])
    if pidler:
        oldur(pidler)
        log("TARAYICI-KAPI", f"{len(pidler)} tarayıcı süreci kapatıldı", f"pid {pidler[:8]}")
    return pidler


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
    # 24 Eki 11:20 (Desktop): 87/88 tek-süreç yolu ajanların 30-300 MB MCP sunucularını tek tek öldürüp araçlarını bozuyordu,
    # RAM düşmüyordu (oyun). Yalnız TEK_MIN_MB üstü kaçak süreç hedef; küçükler için ağaç yolu (>=%92) var.
    aday = [s for s in altlar if not izinli(s[2], s[4]) and not korumali(s[2], s[4]) and s[0] != os.getpid() and s[3] >= TEK_MIN_MB * 2**20]
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


def korumali(ad, komut):
    return ad.lower() in KORUMA_AD or any(k in komut.lower() for k in KORUMA_KOMUT)


def agac_pidleri(surecler, kok):
    """kok + torunları (korumalı süreç ve altı hariç), yapraktan köke: önce torunlar ölür."""
    cocuk = {}
    for s in surecler:
        cocuk.setdefault(s[1], []).append(s)
    sira, kuyruk, gorulen = [kok], [kok], {kok}
    while kuyruk:
        for s in cocuk.get(kuyruk.pop(0), []):
            if s[0] not in gorulen and not korumali(s[2], s[4]):
                gorulen.add(s[0])
                sira.append(s[0])
                kuyruk.append(s[0])
    return sira[::-1]


def agac_ozet(surecler, kok):
    """(toplam çalışma kümesi bayt, alt süreç sayısı, pid listesi) — yalnız durdurulacak süreçler sayılır."""
    pidler = agac_pidleri(surecler, kok)
    ws = {s[0]: s[3] for s in surecler}
    return sum(ws.get(p, 0) for p in pidler), len(pidler) - 1, pidler


def agac_sec(surecler, kokler):
    """kokler içinde (var olan) toplam çalışma kümesi en büyük ajan ağacı: (kok, toplam, alt, pidler) ya da None."""
    var = {s[0] for s in surecler}
    adaylar = [(agac_ozet(surecler, k), k) for k in kokler if k in var]
    if not adaylar:
        return None
    (toplam, alt, pidler), kok = max(adaylar, key=lambda a: a[0][0])
    return kok, toplam, alt, pidler


def oldur_pidler(pidler):
    """taskkill /T kullanmaz (korumalı alt süreçler yaşasın); pidler yapraktan köke."""
    import subprocess
    for p in pidler:
        subprocess.run(["taskkill", "/F", "/PID", str(p)], capture_output=True, creationflags=0x08000000)


def agac_kontrol(r, kok_ad, surecler, oldur, log, uyari):
    """kok_ad {ajan kök pid: iş adı}. (durum, kok, ad): 'kesildi' (r >= AGAC_ESIK, en büyük ağaç oldur(pidler) ile), 'uyari' (ağaç > UYARI_MB ya da
    > UYARI_ALT alt süreç; uyari kümesi sayesinde kök başına bir kez), 'hedef-yok' (r >= AGAC_ESIK ama kök yok), aksi None."""
    s = agac_sec(surecler, set(kok_ad))
    if r >= AGAC_ESIK:
        if s is None:
            log("RAM-BEKÇİ", f"RAM %{r}", "ağaç yok (ajan kökü çalışmıyor)")
            return "hedef-yok", None, None
        kok, toplam, alt, pidler = s
        oldur(pidler)
        log("RAM-BEKÇİ", f"RAM %{r}", "AĞAÇ DURDURULDU", f"{kok_ad[kok]} kök {kok} · {toplam // 2**20} MB · {alt} alt süreç")
        return "kesildi", kok, kok_ad[kok]
    var = {x[0] for x in surecler}
    for kok in (k for k in kok_ad if k in var):
        toplam, alt, _ = agac_ozet(surecler, kok)
        for tur, asildi in (("mb", toplam > UYARI_MB * 2**20), ("alt", alt > UYARI_ALT)):
            if asildi and (kok, tur) not in uyari:
                uyari.add((kok, tur))
                log("RAM-BEKÇİ", f"RAM %{r}", "UYARI ağaç büyük", f"{kok_ad[kok]} kök {kok} · {toplam // 2**20} MB · {alt} alt süreç")
                return "uyari", kok, kok_ad[kok]
    return None, None, None
