"""MCP-HAFIF-2 d6 onay betiği (Desktop koşar): canlı bekçi (12 Eki 16:25) asılı-proxy düzeltmesinden (5d3bc7d) ÖNCEKİ kodu
bellekte koşuyor; main'deki tools/mcp_paylasim.py düzeltmeyi taşıyor. Bekçi yalnız PID ile (ağaçsız: proxy ayakta kalır,
MCP kesintisi yok) durdurulur, Startup kaydındaki aynı komutla (pythonw, pencere yok) yeniden başlatılır.
  python onay/mcp_hafif_2_bekci.py --kuru   # varsayılan: yalnız PLAN
  python onay/mcp_hafif_2_bekci.py uygula
  python onay/mcp_hafif_2_bekci.py --geri   # yapılandırma değişmiyor; yalnız bekçi canlı değilse başlatır (eski kod geri getirilmez)"""
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_hafif_2_uygula import DIZIN, mcp_adlari, mp  # noqa: E402

ANA = Path(r"C:\Projeler\omer-skills\tools\mcp_paylasim.py")  # Startup vbs'nin koştuğu yol
KOMUT = [str(Path(sys.executable).with_name("pythonw.exe")), str(ANA), "bekci", str(DIZIN / "sunucular.json"), str(mp.PORT)]
GIZLI = 0x08000000


def komut_satiri(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"(Get-CimInstance Win32_Process -Filter 'ProcessId={pid}').CommandLine"],
                       capture_output=True, text=True, creationflags=GIZLI)
    return r.stdout.strip()


def bizim_bekci(satir):
    """PID yeniden kullanılmışsa başka süreci öldürmemek için: yalnız mcp_paylasim.py bekci komutu."""
    return "mcp_paylasim.py" in satir and "bekci" in satir


def baslat():
    subprocess.Popen(KOMUT, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     creationflags=GIZLI | 0x00000200, close_fds=True)
    for _ in range(20):
        time.sleep(1)
        yeni = int((DIZIN / "bekci.pid").read_text())
        if bizim_bekci(komut_satiri(yeni)):
            return yeni
    raise SystemExit("yeni bekçi 20 sn'de bekci.pid yazmadı")


def main(kip):
    if "kapali >= 20" not in ANA.read_text(encoding="utf-8"):
        raise SystemExit(f"{ANA} asılı-proxy düzeltmesini taşımıyor — main güncel değil")
    eski = int((DIZIN / "bekci.pid").read_text())
    satir = komut_satiri(eski)
    canli = bizim_bekci(satir)
    print(f"bekçi pid {eski} {'CANLI' if canli else 'YOK/başka süreç'} · port {mp.PORT} {'AÇIK' if mp.ayakta(mp.PORT) else 'KAPALI'}"
          f" · proxy pid {(DIZIN / 'proxy.pid').read_text()}")
    if kip == "--geri":
        print("canlı, dokunulmadı" if canli else f"bekçi başlatıldı: pid {baslat()}")
        return
    if kip != "uygula":
        print(f"PLAN: taskkill /F /PID {eski} (ağaçsız; proxy kalır) → {' '.join(KOMUT)}" if canli else f"PLAN: bekçi başlat → {' '.join(KOMUT)}")
        return
    adlar = mcp_adlari()
    if canli:
        subprocess.run(["taskkill", "/F", "/PID", str(eski)], capture_output=True, creationflags=GIZLI)
    yeni = baslat()
    time.sleep(20)  # yeni bekçi en az bir tur koşsun
    assert bizim_bekci(komut_satiri(yeni)), "yeni bekçi düştü"
    assert mcp_adlari() == adlar
    print(f"uygulandı: bekçi {eski} → {yeni} (main kodu) · port {'AÇIK' if mp.ayakta(mp.PORT) else 'KAPALI'} · MCP listesi önce=sonra ({len(adlar)})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1] if len(sys.argv) > 1 else "--kuru")
