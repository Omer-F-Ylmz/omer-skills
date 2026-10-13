"""MCP-HAFIF-2 d6 onay betiği (Desktop koşar): CC üst düzey stdio auth0'ı paylaşımlı mcp-proxy'ye (:47800) ekler.
azure / banana / nano-banana-2 eklenti MCP'si: çevirmek eklenti dosyasını değiştirmeyi ya da eklenti MCP'sini kapatmayı
gerektirir → kapsam dışı. Proxy yapılandırmayı yalnız açılışta okur: uygula proxy'yi PID ile kapatır, bekçi yeni
yapılandırmayla yeniden açar (≈2 dk paylaşımlı MCP kesintisi — açık CC oturumu yokken koşun; önce mcp_hafif_2_bekci.py uygula).
  python onay/mcp_hafif_2_paylas.py --kuru   # varsayılan: geçici port 47898, canlıya yazmaz; stdio tools/list == http tools/list
  python onay/mcp_hafif_2_paylas.py uygula
  python onay/mcp_hafif_2_paylas.py --geri"""
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mcp_hafif_2_bekci import GIZLI, bizim_bekci, komut_satiri  # noqa: E402
from mcp_hafif_2_uygula import DIZIN, mcp_adlari, mp, surec_adi  # noqa: E402

EK = ["auth0"]
CJ = Path.home() / ".claude.json"
ONCE = DIZIN / "claude-json-once-d6.json"
DAMGA = time.strftime("%Y%m%d-%H%M%S")


def oku(yol):
    return json.loads(Path(yol).read_text(encoding="utf-8-sig"))


def yaz(yol, d):
    metin = json.dumps(d, ensure_ascii=False, indent=2)
    json.loads(metin)
    Path(yol).write_text(metin, encoding="utf-8")


def bekle_port(port, sure=180):
    for _ in range(sure // 3):
        if mp.ayakta(port):
            return True
        time.sleep(3)
    return False


def proxy_yeniden():
    """Proxy ağacını PID ile kapatır; bekçi yeni yapılandırmayla açar."""
    pid = int((DIZIN / "proxy.pid").read_text())
    if surec_adi(pid) == "mcp-proxy.exe":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, creationflags=GIZLI)
    time.sleep(10)
    if not bekle_port(mp.PORT):
        raise SystemExit(f"proxy 180 sn'de açılmadı — {DIZIN / 'proxy.log'}")


def esitler(sunucular, port):
    sonuc = mp.karsilastir(sunucular, port, EK)
    for a, r in sonuc.items():
        print(f"{'OK ' if r['esit'] else 'FARK'} {a:<10} stdio={r['stdio']:<3} http={r['http']:<3} {r['hata']}")
    return [a for a, r in sonuc.items() if r["esit"]]


def kuru():
    sunucular = oku(CJ)["mcpServers"]
    dizin = Path(tempfile.mkdtemp(prefix="mh2-paylas-"))
    cfg = dizin / "sunucular.json"
    yaz(cfg, mp.proxy_config(sunucular, EK))
    with open(dizin / "proxy.log", "a") as log:
        p = subprocess.Popen([str(mp.PROXY), "--host", "127.0.0.1", "--port", "47898", "--pass-environment",
                              "--named-server-config", str(cfg)], stdout=log, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, creationflags=GIZLI)
    try:
        ok = esitler(sunucular, 47898) if bekle_port(47898) else []
    finally:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=GIZLI)
    yeni = mp.donustur(sunucular, ok)
    print(f"KURU: {ok or 'hiçbiri'} çevrilebilir · ad kümesi {'aynı' if sorted(yeni) == sorted(sunucular) else 'DEĞİŞİRDİ'}"
          f" ({len(sunucular)}) · canlıya yazılmadı")
    return ok


def uygula():
    if not bizim_bekci(komut_satiri(int((DIZIN / "bekci.pid").read_text()))):
        raise SystemExit("bekçi canlı değil — önce onay/mcp_hafif_2_bekci.py uygula")
    ok = kuru()  # açılmayan sunucu (ör. auth0 init yapılmamış) canlı proxy'ye hiç girmez
    if not ok:
        raise SystemExit("çevrilebilir sunucu yok — canlıya dokunulmadı")
    adlar = mcp_adlari()
    sunucular = oku(CJ)["mcpServers"]
    cfg_yol = DIZIN / "sunucular.json"
    cfg = oku(cfg_yol)
    shutil.copy2(cfg_yol, cfg_yol.with_name(f"sunucular.json.bak-d6-{DAMGA}"))
    cfg["mcpServers"].update(mp.proxy_config(sunucular, ok)["mcpServers"])
    yaz(cfg_yol, cfg)
    proxy_yeniden()
    ok = esitler(sunucular, mp.PORT)
    if not ok:
        print("eşit değil — ~/.claude.json'a yazılmadı (proxy'de fazladan durur; --geri temizler)")
        return
    d = oku(CJ)  # CC arada yazmış olabilir
    yeni = mp.donustur(d["mcpServers"], ok)
    if sorted(yeni) != adlar:
        raise SystemExit("ad kümesi değişirdi — yazılmadı")
    if not ONCE.exists():
        yaz(ONCE, {a: d["mcpServers"][a] for a in ok})
    shutil.copy2(CJ, CJ.with_name(f".claude.json.bak-d6-{DAMGA}"))
    d["mcpServers"] = yeni
    yaz(CJ, d)
    assert mcp_adlari() == adlar
    print(f"uygulandı: {ok} → http://127.0.0.1:{mp.PORT} · MCP listesi önce=sonra ({len(adlar)}) · yeni CC oturumunda geçerli")


def geri():
    if ONCE.exists():
        once = oku(ONCE)
        d = oku(CJ)
        shutil.copy2(CJ, CJ.with_name(f".claude.json.bak-d6-geri-{DAMGA}"))
        d["mcpServers"].update(once)
        yaz(CJ, d)
        ONCE.unlink()
    cfg_yol = DIZIN / "sunucular.json"
    cfg = oku(cfg_yol)
    if any(a in cfg["mcpServers"] for a in EK):
        for a in EK:
            cfg["mcpServers"].pop(a, None)
        yaz(cfg_yol, cfg)
        proxy_yeniden()
    print("geri alındı:", EK)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    geri() if kip == "--geri" else uygula() if kip == "uygula" else kuru()
