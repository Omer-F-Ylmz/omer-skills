"""BLENDER-4 onay betiği — Desktop/Ömer koşar (main'de, kol/blender4 birleşip push'landıktan sonra).

  python onay/blender_4_uygula.py --kuru   # plan (varsayılan): önkoşullar + kurulu/yeni sürüm + zip listesi; hiçbir şey yazmaz
  python onay/blender_4_uygula.py uygula   # yedek → claude plugin marketplace update + plugin update blender@omer-skills; dist/blender-4/ zip'leri
  python onay/blender_4_uygula.py --geri   # installed_plugins.json'u son yedekten geri koyar (önceki sürümün önbelleği yerinde kalır)
Önkoşul: CC eklentisi araçları mutlak yoldan (C:/Projeler/omer-skills/tools) koşar → yerel main'de tarif.py duzelt + yalin TEK_ENV olmalı;
marketplace kaynağı GitHub → origin/main'de eklenti sürümü YENI olmalı. claude.ai: dist/blender-4/*.zip (zip_denetle temiz) Ömer yükler.
MCP listesi önce=sonra değilse rc=1. Anahtar/hesap değeri okunmaz, yazdırılmaz.
"""
import json, shutil, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "onay"))
sys.path.insert(0, str(KOK / "tools" / "blender"))
sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
from kalite_3_uygula import mcp_var_mi  # noqa: E402

YENI = "1.3.0"
EKLENTI = "blender@omer-skills"
KURULU = Path.home() / ".claude" / "plugins" / "installed_plugins.json"
YEDEK = Path.home() / ".claude" / "yedek"
DIST = KOK / "dist" / "blender-4"


def onkosul(kok=KOK, uzak_surum=None):
    """Eksik önkoşulların listesi (boşsa uygulanabilir)."""
    eksik = []
    if "def duzelt(" not in (kok / "tools" / "blender" / "lib" / "tarif.py").read_text(encoding="utf-8"):
        eksik.append("yerel main'de tarif.py duzelt yok: önce kol/blender4 → main birleşmesi")
    if uzak_surum is None:
        subprocess.run(["git", "-C", str(kok), "fetch", "-q", "origin", "main"], capture_output=True)
        r = subprocess.run(["git", "-C", str(kok), "show", "origin/main:plugins/blender/.claude-plugin/plugin.json"],
                           capture_output=True, text=True, encoding="utf-8")
        uzak_surum = json.loads(r.stdout).get("version") if r.returncode == 0 else None
    if uzak_surum != YENI:
        eksik.append(f"origin/main eklenti sürümü {uzak_surum} ≠ {YENI}: main push'lanmalı (Ömer)")
    return eksik


def kurulu_surum():
    try:
        return [i.get("version") for i in json.loads(KURULU.read_text(encoding="utf-8"))["plugins"].get(EKLENTI, [])]
    except (OSError, ValueError, KeyError):
        return []


def zipler():
    import claude_ai_zip, zip_denetle
    return {str(z): zip_denetle.denetle(z) or "TEMİZ" for z in claude_ai_zip.paketle(DIST)}


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    kip = argv[0] if argv else "--kuru"
    if kip == "--geri":
        yedekler = sorted(YEDEK.glob("blender4-installed_plugins-*.json"))
        if not yedekler:
            print("yedek yok")
            return 1
        shutil.copy2(yedekler[-1], KURULU)
        print("geri konuldu:", yedekler[-1].name, "→ kurulu", kurulu_surum(), "(CC yeniden başlat)")
        return 0
    eksik = onkosul()
    print("kurulu", EKLENTI, kurulu_surum(), "→ yeni", YENI)
    print("önkoşul:", "TAMAM" if not eksik else "; ".join(eksik))
    if kip != "uygula":
        print("claude.ai zip hedefi:", DIST, "(blender-oturum.zip, blender-uretim.zip)")
        return 0
    if eksik:
        return 1
    once = mcp_var_mi()
    YEDEK.mkdir(parents=True, exist_ok=True)
    shutil.copy2(KURULU, YEDEK / f"blender4-installed_plugins-{time.strftime('%Y%m%d-%H%M%S')}.json")
    for komut in (["claude", "plugin", "marketplace", "update", "omer-skills"], ["claude", "plugin", "update", EKLENTI]):
        r = subprocess.run(komut, capture_output=True, text=True, encoding="utf-8", creationflags=0x08000000)
        print(" ".join(komut), "rc", r.returncode)
        if r.returncode:
            print((r.stdout + r.stderr)[-400:])
            return 1
    for z, durum in zipler().items():
        print(z, durum)
    sonra = mcp_var_mi()
    print("kurulu", kurulu_surum(), "· MCP önce=sonra:", once == sonra, "(CC yeniden başlat)")
    return 0 if once == sonra and YENI in kurulu_surum() else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
