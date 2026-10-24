"""REA otomatik düşüş: analyze_web_bundle'ı normal modda dener; OOM/RAM-bekçisi yüzünden cevap yoksa rea_parcali.py'a düşer.
Kullanım: python tools/rea_oto.py <url> <dizin> [--bekle 20]  -> <dizin>/oto.json (hangi yol, neden)."""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOWIN = 0x08000000
OOM = 134


def parcali_gerek(sonuc):
    """Normal mod cevap vermediyse ve neden bellekse (OOM çıkışı ya da RAM bekçisi) True."""
    return not sonuc.get("cevap_var") and (sonuc.get("rea_cikis") == OOM or bool(sonuc.get("ram_bekci_durdurdu")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("dizin"); ap.add_argument("--bekle", type=int, default=20)
    a = ap.parse_args()
    os.makedirs(a.dizin, exist_ok=True)
    cikti = os.path.join(a.dizin, "normal.json")
    arg = json.dumps({"cdp_endpoint": "{CDP}", "target_id": "{TARGET}", "observation_ms": 3000})
    env = {**os.environ, "BEKLE": str(a.bekle), "ZAMAN_ASIMI": "240"}
    subprocess.run([sys.executable, os.path.join(HERE, "rea_mcp_cagri.py"), a.url, "analyze_web_bundle", arg, cikti,
                    "--max-old-space-size=2048"], env=env, capture_output=True, creationflags=NOWIN)
    sonuc = json.load(open(cikti, encoding="utf-8"))
    yol = "normal"
    if parcali_gerek(sonuc):
        yol = "parcali"
        subprocess.run([sys.executable, os.path.join(HERE, "rea_parcali.py"), a.url, os.path.join(a.dizin, "parcali"),
                        "--bekle", str(a.bekle)], creationflags=NOWIN)
    json.dump({"yol": yol, "normal": sonuc}, open(os.path.join(a.dizin, "oto.json"), "w", encoding="utf-8"), indent=1)
    print(yol)


if __name__ == "__main__":
    main()
