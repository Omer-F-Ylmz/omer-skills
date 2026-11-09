r"""RAM-OPT-2 (9 Kas 2026): Desktop'un her MCP'yi birkaç kez (ölçümde x2-x4) başlatması RAM'i ~7.6 GB'a çıkarıyor.
Havuzda (mcp-proxy 47800/47801) zaten tek kopya koşan sunucuların Desktop girdilerini hafif köprüye
(tools/ram/mcp_koprusu.py) çevirir: Desktop'un açtığı her kopya ~20 MB'lık python köprüsü olur, gerçek sunucu tek.
Araç kaybı yok: havuz o adı sunmuyorsa ya da araç sayısı 0 ise girdiye DOKUNMAZ.
  python -I tools/ram/desktop_havuz.py [--plan]  (varsayılan; hiçbir şey yazmaz)
  python -I tools/ram/desktop_havuz.py --uygula  (önce yedek; etki için Desktop'u kapatıp aç)
  python -I tools/ram/desktop_havuz.py --geri    (en son yedeği aynen geri yükler)
Env DEĞERİ hiçbir modda basılmaz."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mcp_paylasim as mp  # noqa: E402

KOK = Path(__file__).resolve().parents[2]
KOPRU = str(Path(__file__).resolve().with_name("mcp_koprusu.py"))
PY = sys.executable.replace("pythonw.exe", "python.exe")
YEDEK = KOK / ".kos" / "kopru" / "yedek" / "desktop-mcp"
LA = Path(os.environ.get("LOCALAPPDATA", ""))
ADAYLAR = [LA / "Packages" / "Claude_pzs8sxrjxfjjc" / "LocalCache" / "Roaming" / "Claude" / "claude_desktop_config.json",
           LA / "Claude-Data" / "claude_pzs8sxrjxfjjc" / "claude_desktop_config.json",
           Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"]
HAVUZLAR = [(mp.PORT, Path.home() / ".claude" / "mcp-paylasim" / "sunucular.json"),
            (mp.PORT2, Path.home() / ".claude" / "mcp-paylasim" / "sunucular2.json")]


def config_yolu():
    var = [p for p in ADAYLAR if p.is_file()]
    if not var:
        sys.exit("Desktop config bulunamadi: " + " | ".join(map(str, ADAYLAR)))
    return max(var, key=lambda p: p.stat().st_mtime)


def imza(g):
    return (Path(str(g.get("command", ""))).name.lower().replace(".cmd", "").replace(".exe", ""),
            tuple(str(a) for a in g.get("args", [])))


def havuz_haritasi():
    adlar = {}
    for port, yol in HAVUZLAR:
        if not yol.is_file():
            continue
        s = json.loads(yol.read_text(encoding="utf-8")).get("mcpServers", {})
        for ad, g in s.items():
            adlar.setdefault(("ad", ad), (port, ad))
            adlar.setdefault(("imza", imza(g)), (port, ad))
    for ad in mp.PAYLASIM:
        adlar.setdefault(("ad", ad), (mp.PORT, ad))
    for ad in mp.PAYLASIM2:
        adlar.setdefault(("ad", ad), (mp.PORT2, ad))
    return adlar


def kopru_mu(g):
    return any("mcp_koprusu" in str(a) for a in g.get("args", []))


def plan(cfg):
    harita, sonuc = havuz_haritasi(), []
    for ad, g in cfg.get("mcpServers", {}).items():
        if g.get("type", "stdio") != "stdio" or "command" not in g:
            sonuc.append((ad, "atla", "stdio degil (http/sse; sureci yok)", None)); continue
        if kopru_mu(g):
            sonuc.append((ad, "zaten", "kopru", None)); continue
        hedef = harita.get(("imza", imza(g))) or harita.get(("ad", ad))
        if not hedef:
            sonuc.append((ad, "kalir", "havuzda karsiligi yok", None)); continue
        port, hav = hedef
        try:
            n = len(mp.araclar_http(mp.url(hav, port)))
        except Exception as e:
            sonuc.append((ad, "kalir", f"havuz {port}/{hav} yanit yok ({type(e).__name__})", None)); continue
        if n == 0:
            sonuc.append((ad, "kalir", f"havuz {port}/{hav} 0 arac", None)); continue
        sonuc.append((ad, "kopru", f"havuz {port}/{hav} {n} arac", (hav, port)))
    return sonuc


def main():
    kip = (sys.argv[1] if len(sys.argv) > 1 else "plan").lstrip("-")
    sys.stdout.reconfigure(encoding="utf-8")
    yol = config_yolu()
    print("config:", yol)
    if kip == "geri":
        y = sorted(YEDEK.glob("claude_desktop_config-*.json"))
        if not y:
            sys.exit("yedek yok")
        shutil.copyfile(y[-1], yol)
        return print("geri yuklendi:", y[-1].name, "(Desktop'u kapatip ac)")
    cfg = json.loads(yol.read_text(encoding="utf-8"))
    p = plan(cfg)
    for ad, karar, neden, _ in p:
        print(f"{karar:6} {ad:<28} {neden}")
    degisen = [(ad, h) for ad, k, _, h in p if k == "kopru"]
    print(f"\nkopruye gececek: {len(degisen)} | zaten kopru: {sum(k == 'zaten' for _, k, _, _ in p)} | kalan: {sum(k == 'kalir' for _, k, _, _ in p)}")
    if kip != "uygula" or not degisen:
        return
    YEDEK.mkdir(parents=True, exist_ok=True)
    y = YEDEK / f"claude_desktop_config-{time.strftime('%Y%m%d-%H%M%S')}.json"
    shutil.copyfile(yol, y)
    cfg.setdefault("_havuz_oncesi", {})
    for ad, (hav, port) in degisen:
        cfg["_havuz_oncesi"][ad] = cfg["mcpServers"][ad]
        cfg["mcpServers"][ad] = {"command": PY, "args": ["-I", "-S", KOPRU, hav, str(port)]}
    yol.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("yazildi; yedek:", y, "\nEtki icin Desktop'u kapatip ac. Sorun olursa: python -I tools/ram/desktop_havuz.py geri")


if __name__ == "__main__":
    main()
