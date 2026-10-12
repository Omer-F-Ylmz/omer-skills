"""MCP-HAFIF-2 onay betiği (Desktop koşar): 12 Eki 18:42'den beri mcp-proxy süreci canlı ama 127.0.0.1:47800 dinlemiyor;
eski bekçi p.wait()'te takılı → CC'nin paylaşımlı 22 MCP'si her yeni oturumda "failed". Asılı proxy ağacı PID ile (adı
mcp-proxy.exe ve port kapalıysa) öldürülür; çalışan bekçi kendiliğinden yeniden başlatır (≈2 dk). Yapılandırma değişmez,
MCP listesi önce=sonra. Asılmaya karşı kalıcı bekçi (kol/mcphafif 5d3bc7d) main'e birleşince bir sonraki oturum açılışında devrede.
python onay/mcp_hafif_2_uygula.py --kuru   # durum + yapılacak
python onay/mcp_hafif_2_uygula.py uygula   # asılı proxy'yi öldür, port açılana dek bekle (≤240 sn)
python onay/mcp_hafif_2_uygula.py --geri   # geri alınacak yapılandırma yok"""
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import mcp_paylasim as mp  # noqa: E402

DIZIN = Path.home() / ".claude" / "mcp-paylasim"


def surec_adi(pid):
    c = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"], capture_output=True, text=True,
                       creationflags=0x08000000).stdout.strip()
    return c.split('","')[0].strip('"') if c.startswith('"') else None


def karar(port_acik, ad):
    """Yalnız port kapalı + süreç gerçekten mcp-proxy.exe ise öldür."""
    return not port_acik and ad == "mcp-proxy.exe"


def mcp_adlari():
    d = json.loads((Path.home() / ".claude.json").read_text(encoding="utf-8"))
    return sorted(d.get("mcpServers", {}))


def main(kip):
    pid = int((DIZIN / "proxy.pid").read_text())
    bekci = int((DIZIN / "bekci.pid").read_text())
    acik, ad = mp.ayakta(mp.PORT), surec_adi(pid)
    print(f"port {mp.PORT} {'AÇIK' if acik else 'KAPALI'} · proxy pid {pid} {ad} · bekçi pid {bekci} {surec_adi(bekci)}")
    if kip == "--geri":
        return print("geri alınacak yapılandırma yok (yalnız asılı süreç öldürüldü; bekçi yeniden başlatır)")
    if not karar(acik, ad):
        return print("ATLA: proxy asılı değil")
    if kip != "uygula":
        return print(f"PLAN: taskkill /F /T /PID {pid} → bekçi yeniden başlatır; MCP listesi değişmez")
    once = mcp_adlari()
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, creationflags=0x08000000)
    for _ in range(48):
        time.sleep(5)
        if mp.ayakta(mp.PORT):
            break
    print(f"port {'AÇIK' if mp.ayakta(mp.PORT) else 'HÂLÂ KAPALI'} · yeni proxy pid {(DIZIN / 'proxy.pid').read_text()} · "
          f"MCP listesi önce=sonra {once == mcp_adlari()} ({len(once)})")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # cp1254 konsolda → yazılamıyor
    main(sys.argv[1] if len(sys.argv) > 1 else "--kuru")
