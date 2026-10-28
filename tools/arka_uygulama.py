"""Uygulamaları Ömer'in ekranında görünmeden koşar (KOD-MODU-HER-SEY, Bölüm 2) + tek 'arac-calistir' kapısı.

Öncelik: (1) başsız/CLI/API  (2) ayrı Windows MASAÜSTÜ nesnesi (CreateDesktop; görev çubuğu ve ön plan etkilenmez)
         (3) 'yok' = yalnız Ömer izin verirse.

  python tools/arka_uygulama.py ara "<görev/uygulama>"     # hangi yol, hangi komut kalıbı
  python tools/arka_uygulama.py komut [--ad AD] -- <cmd..>  # başsız koş; çıktı dosyaya, ekrana ≤30 satır özet
  python tools/arka_uygulama.py sanal <exe> [args..] [--sn 3]  # gizli masaüstünde aç, pencereleri say, kapat
  python tools/arka_uygulama.py tablo                       # docs/arka-uygulama.md üret (kayıt defteri taraması)
Her koşuda GetForegroundWindow önce/sonra karşılaştırılır; değişirse çıkış 3."""
import argparse, ctypes, os, re, subprocess, sys, time
from ctypes import wintypes as W
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / ".kos" / "kopru" / "arka-cikti"
NW = 0x08000000  # CREATE_NO_WINDOW
U = ctypes.WinDLL("user32", use_last_error=True)
K = ctypes.WinDLL("kernel32", use_last_error=True)
U.GetForegroundWindow.restype = W.HWND

# (regex, mod, yol/komut kalıbı) — ilk eşleşen kazanır. mod: basiz | sanal | yok | bilesen
KURALLAR = [
    (r"^Blender", "basiz", 'blender -b dosya.blend -P betik.py | -o //cikti_#### -f 1 (render)'),
    (r"Comfy", "basiz", "python tools/gorsel_uret.py ac|uret|kapat (main.py --disable-auto-launch, API 127.0.0.1:8188)"),
    (r"FFmpeg", "basiz", "ffmpeg -hide_banner -y -i girdi çıktı"),
    (r"Tesseract", "basiz", "tesseract girdi.png çıktı -l tur+eng"),
    (r"SQL Server Management Studio", "basiz", "sqlcmd -S . -E -Q \"...\" (SSMS yerine)"),
    (r"SQL Server|LocalDB", "basiz", "sqlcmd -S . -E -Q \"...\""),
    (r"Docker", "basiz", "docker <komut> (motor WSL2; Desktop penceresi gerekmez)"),
    (r"^Git$|GitHub CLI|Gitleaks|^jq|^uv$|^Bun$|Node\.js|cloudflared|Lua Language|Corretto|^PHP|Headroom|7-Zip|WinRAR|IIS 10", "basiz", "doğrudan CLI (arac-calistir kapısı)"),
    (r"Laragon", "basiz", "laragon\\bin\\php|mysql|nginx ikili dosyaları doğrudan; laragon.exe açılmaz"),
    (r"Google Chrome|BrowserOS", "basiz", "chrome --headless=new --screenshot|--dump-dom; playwright headless"),
    (r"Acrobat", "basiz", "pypdf/pdfplumber/ocrmypdf (Acrobat penceresi açılmaz)"),
    (r"Visual Studio|NetBeans|Web Deploy|Help Viewer", "basiz", "msbuild/dotnet build | ant/mvn; IDE açılmaz"),
    (r"4DDiG", "sanal", "GUI yalnız; sanal masaüstü (tools/arka_uygulama.py sanal)"),
    (r"OpenPencil|Cascadeur|Movavi|DroidCam|Aurora|PromptHub|ICAT|DBX|OpenFic", "sanal", "GUI; sanal masaüstünde aç, UI Automation ile yönet"),
    (r"BlueStacks|LDPlayer", "sanal", "emülatör: GUI sanal masaüstünde; adb ile başsız komut"),
    (r"AIDA64|CPU-Z|FurMark|RivaTuner|NVIDIA App|Armoury|AURA|ROG|MSI Center", "sanal", "donanım aracı: sanal masaüstü (CPU-Z -txt=, AIDA64 /R rapor kipi başsız)"),
    (r"Discord|Zoom|Battle\.net|Epic Games|OneDrive|Teams|Cloudflare WARP|VPN|LagoFast|CurseForge|TLauncher", "yok", "hesap/oturum uygulaması: yalnız Ömer izin verirse"),
    (r"League of Legends|VALORANT|Counter-Strike|Goose|NIKKE|PICO|Wuthering|GRYPHLINK|XXMI|AntiCheat|Xbox|GameInput|GameSDK", "yok", "oyun/anti-hile: yalnız Ömer izin verirse"),
    (r"Redistributable|Runtime|\.NET|SDK|Driver|Update|Service|Framework|Chipset|Management Engine|Compatibility|CLR Types|VSS Writer|MPI|Fonts|Targeting|Installer|Add-in|add-on|Canon IJ|Intel|PhysX|Epic Online", "bilesen", "kütüphane/sürücü/servis: ayrı uygulama değil"),
]
HEDEF = [  # kurulu değil ama istenen başsız yollar
    ("Unity", "basiz", "Unity.exe -batchmode -nographics -quit -projectPath P -executeMethod M"),
    ("Godot", "basiz", "godot --headless --path P --script betik.gd"),
    ("Ghidra", "basiz", "support\\analyzeHeadless.bat projeDizin proje -import ikili"),
    ("Power Automate Desktop", "sanal", "CLI yok; PAD.Console.Host sanal masaüstünde, akış URL'siyle"),
]


def sinifla(ad):
    for rx, mod, yol in KURALLAR:
        if re.search(rx, ad, re.I):
            return mod, yol
    return "sanal", "GUI (başsız yol bilinmiyor): sanal masaüstü; olmazsa 'yok'"


def kurulu():
    import winreg
    cikti = {}
    for hv, p in ((winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                  (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
                  (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")):
        try:
            k = winreg.OpenKey(hv, p)
        except OSError:
            continue
        for i in range(winreg.QueryInfoKey(k)[0]):
            try:
                s = winreg.OpenKey(k, winreg.EnumKey(k, i))
                g = lambda n: str(winreg.QueryValueEx(s, n)[0]) if _var(s, n) else ""
                ad = g("DisplayName")
                if ad and g("SystemComponent") != "1" and not g("ParentKeyName"):
                    cikti[ad.strip()] = g("DisplayVersion")
            except OSError:
                pass
    return cikti


def _var(s, n):
    import winreg
    try:
        winreg.QueryValueEx(s, n)
        return True
    except OSError:
        return False


def on_plan():
    return U.GetForegroundWindow()


def on_plan_ad(h=None):
    b = ctypes.create_unicode_buffer(80)
    U.GetWindowTextW(h or U.GetForegroundWindow(), b, 80)
    return b.value


class Izle:
    """Koşu boyunca ön plan penceresini 50 ms'de bir örnekler; değişimleri (başlık) toplar."""
    def __init__(self):
        import threading
        self.gor, self.dur = [], False
        self.t = threading.Thread(target=self._dongu, daemon=True)

    def _dongu(self):
        while not self.dur:
            h = U.GetForegroundWindow()
            if not self.gor or self.gor[-1][0] != h:
                self.gor.append((h, on_plan_ad(h)))
            time.sleep(0.05)

    def __enter__(self):
        self.t.start()
        return self

    def __exit__(self, *e):
        self.dur = True
        self.t.join()

    def degisti(self):
        return len({h for h, _ in self.gor}) > 1


def ozet(metin, n=30):
    s = metin.splitlines()
    if len(s) <= n:
        return metin
    hata = [x for x in s if re.search(r"error|hata|fail|traceback|exception", x, re.I)][:6]
    return "\n".join(s[:10] + [f"... ({len(s)} satır; tam çıktı dosyada) ..."] + hata + s[-(n - 11 - len(hata)):])


def komut(a):
    CIKTI.mkdir(parents=True, exist_ok=True)
    ad = a.ad or Path(a.cmd[0]).stem
    dosya = CIKTI / f"{ad}-{int(time.time())}.log"
    with Izle() as iz:
        r = subprocess.run(a.cmd, capture_output=True, creationflags=NW, timeout=a.zaman, env=dict(os.environ))
    metin = (r.stdout + r.stderr).decode("utf-8", "replace")
    dosya.write_text(metin, encoding="utf-8")
    print(ozet(metin))
    dur = "AYNI" if not iz.degisti() else "DEĞİŞTİ " + " → ".join(repr(t) for _, t in iz.gor)
    print(f"[kod {r.returncode} · {len(metin.splitlines())} satır · {dosya.relative_to(KOK)} · ön plan {dur}]")
    return 3 if iz.degisti() else r.returncode


class SI(ctypes.Structure):
    _fields_ = [("cb", W.DWORD), ("r", W.LPWSTR), ("d", W.LPWSTR), ("t", W.LPWSTR), ("x", W.DWORD), ("y", W.DWORD),
                ("xs", W.DWORD), ("ys", W.DWORD), ("xc", W.DWORD), ("yc", W.DWORD), ("fa", W.DWORD), ("fl", W.DWORD),
                ("sw", W.WORD), ("r2", W.WORD), ("r3", ctypes.c_void_p), ("i", W.HANDLE), ("o", W.HANDLE), ("e", W.HANDLE)]


class PI(ctypes.Structure):
    _fields_ = [("hp", W.HANDLE), ("ht", W.HANDLE), ("pid", W.DWORD), ("tid", W.DWORD)]


def pencereler(hdesk=None, pid=None):
    """Masaüstündeki üst düzey pencereler (başlık, görünür, pid)."""
    bul = []
    CB = ctypes.WINFUNCTYPE(W.BOOL, W.HWND, W.LPARAM)

    def cb(h, _):
        p = W.DWORD()
        U.GetWindowThreadProcessId(h, ctypes.byref(p))
        if pid is None or p.value == pid:
            b = ctypes.create_unicode_buffer(120)
            U.GetWindowTextW(h, b, 120)
            bul.append((h, b.value, bool(U.IsWindowVisible(h)), p.value))
        return True
    (U.EnumDesktopWindows(hdesk, CB(cb), 0) if hdesk else U.EnumWindows(CB(cb), 0))
    return bul


def sanal(a):
    ad = f"Arka{os.getpid()}"
    U.CreateDesktopW.restype = W.HANDLE
    hd = U.CreateDesktopW(ad, None, None, 0, 0x10000000, None)
    if not hd:
        print("masaüstü açılamadı", ctypes.get_last_error())
        return 1
    once = on_plan()
    si = SI(); si.cb = ctypes.sizeof(SI); si.d = f"winsta0\\{ad}"
    pi = PI()
    cmd = ctypes.create_unicode_buffer(subprocess.list2cmdline([a.exe] + a.args))
    if not K.CreateProcessW(None, cmd, None, None, False, 0, None, None, ctypes.byref(si), ctypes.byref(pi)):
        print("süreç açılamadı", ctypes.get_last_error())
        U.CloseDesktop(hd)
        return 1
    time.sleep(a.sn)
    # çocuk süreçler (ör. Electron/UWP) için masaüstünün tüm pencereleri
    pen = pencereler(hd)
    gor = [x for x in pen if x[2] and x[1]]
    # varsayılan masaüstünde bu pid'ye ait pencere görev çubuğunda çıkmamalı
    sizan = pencereler(None, pi.pid.real if hasattr(pi.pid, "real") else pi.pid)
    for h, *_ in pen:
        U.PostMessageW(h, 0x0010, 0, 0)  # WM_CLOSE
    time.sleep(1)
    K.TerminateProcess(pi.hp, 0)
    K.CloseHandle(pi.hp); K.CloseHandle(pi.ht)
    for _ in range(10):  # masaüstü ancak içinde pencere yokken kapanır
        if U.CloseDesktop(hd):
            break
        time.sleep(0.3)
    sonra = on_plan()
    print(f"masaüstü {ad}: {len(pen)} pencere ({len(gor)} görünür) {[x[1] for x in gor][:3]}")
    print(f"varsayılan masaüstüne sızan pencere: {len(sizan)} · ön plan {'AYNI' if sonra == once else 'DEĞİŞTİ'}")
    return 0 if sonra == once and not sizan else 3


def tablo(a):
    k = kurulu()
    sayac, satir = {}, []
    for ad in sorted(k, key=str.lower):
        mod, yol = sinifla(ad)
        sayac[mod] = sayac.get(mod, 0) + 1
        satir.append((ad, mod, yol))
    for ad, mod, yol in HEDEF:
        satir.append((ad + " (kurulu değil)", mod, yol))
    uyg = sum(v for m, v in sayac.items() if m != "bilesen")
    gos = {"basiz": "başsız", "sanal": "sanal masaüstü", "yok": "yok (yalnız izinle)", "bilesen": "bileşen"}
    md = ["---", "type: doc", "status: aktif", "tags: [arka-plan, uygulama, kod-modu]", "relatedTo: [tools/arka_uygulama.py]", "---",
          "# Uygulamalar arka planda (Ömer'in ekranında görünmeden)", "",
          "Üretim: `python tools/arka_uygulama.py tablo` (kayıt defteri taraması). Giriş: `python tools/arka_uygulama.py ara|komut|sanal`.",
          "Yol sırası: başsız/CLI/API → ayrı masaüstü nesnesi (CreateDesktop; görev çubuğu + ön plan etkilenmez) → yok (yalnız izinle).",
          "`komut` kısa ömürlü başsız işler içindir (çıktı dosyaya, ekrana ≤30 satır, ön plan örneklenir); ComfyUI gibi artalan sunucusu `gorsel_uret.py ac` ile doğrudan başlatılır (CREATE_NO_WINDOW).",
          "Bölüm 1 (Code Mode her şeye): skill listesi `skillOverrides` name-only (2415/2755), MCP şemaları `ENABLE_TOOL_SEARCH`, MCP zincirleri `tools/cm.py`, CLI/uygulama `arka_uygulama.py komut`; araç kaldırılmadı (geri açma: skillOverrides değeri `on`).", "",
          f"Toplam kayıt {len(k)} · uygulama {uyg}: " + " · ".join(f"{gos[m]} {sayac.get(m, 0)}" for m in ("basiz", "sanal", "yok")) + f" · bileşen {sayac.get('bilesen', 0)}", "",
          "| Uygulama | Yol | Komut kalıbı / not |", "|---|---|---|"]
    md += [f"| {ad} | {gos[m]} | {y.replace('|', '/')} |" for ad, m, y in satir]
    (KOK / "docs" / "arka-uygulama.md").write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"docs/arka-uygulama.md: kayıt {len(k)} · uygulama {uyg} · {sayac}")


def ara(a):
    q = a.sorgu.lower()
    for rx, mod, yol in KURALLAR + [(h[0], h[1], h[2]) for h in HEDEF]:
        if re.search(rx, q, re.I) or q in rx.lower():
            print(f"{mod}: {yol}")
            return 0
    print("sanal: başsız yol bilinmiyor; GUI ise 'sanal' dene")
    return 1


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="arka_uygulama")
    al = ap.add_subparsers(dest="k", required=True)
    al.add_parser("ara").add_argument("sorgu")
    c = al.add_parser("komut"); c.add_argument("--ad"); c.add_argument("--zaman", type=int, default=600); c.add_argument("cmd", nargs=argparse.REMAINDER)
    s = al.add_parser("sanal"); s.add_argument("exe"); s.add_argument("args", nargs="*"); s.add_argument("--sn", type=float, default=3)
    al.add_parser("tablo")
    a = ap.parse_args(argv)
    if a.k == "komut" and a.cmd and a.cmd[0] == "--":
        a.cmd = a.cmd[1:]
    return {"ara": ara, "komut": komut, "sanal": sanal, "tablo": tablo}[a.k](a)


if __name__ == "__main__":
    sys.exit(main())
