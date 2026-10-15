"""OMNİ-AYIR geri alma: OmniRoute'u .kos/kopru/omni-ayir/yedek-*.json (en yeni) durumuna döndürür.
  python onay/omni_ayir_geri.py --kuru   # plan (varsayılan): yedekte olmayan combo'lar + yedekten sapan combo'lar; hiçbir şey yazmaz
  python onay/omni_ayir_geri.py uygula   # yedekte olmayan combo'ları `omniroute combo delete --yes` ile kaldırır
Yedekteki combo'lar silinmez; data'sı sapan combo yalnız raporlanır (CLI'da güncelleme yok; elle geri yükle, yedek yolu basılır).
storage.sqlite yalnız salt-okunur açılır; anahtar değeri ne okunur ne basılır."""
import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DB = os.path.expanduser("~/.omniroute/storage.sqlite")


def esit(c, y):
    """yedekteki '***' (maskelenmiş sır/kimlik) her değerle eşleşir"""
    if y == "***":
        return True
    if isinstance(c, dict) and isinstance(y, dict):
        return c.keys() == y.keys() and all(esit(c[k], y[k]) for k in c)
    if isinstance(c, list) and isinstance(y, list):
        return len(c) == len(y) and all(map(esit, c, y))
    return c == y


def plan(yedek, canli):
    """(silinecek adlar, data'sı sapan adlar); yedek data çözülmüş ya da dizge, canlı dizge"""
    j = lambda x: json.loads(x) if isinstance(x, str) else x
    return sorted(set(canli) - set(yedek)), sorted(a for a in canli if a in yedek and not esit(j(canli[a]), j(yedek[a])))


def main(argv):
    kip = argv[0] if argv else "--kuru"
    yol = max(glob.glob(str(KOK / ".kos/kopru/omni-ayir/yedek-*.json")), key=os.path.getmtime)
    yedek = {c["name"]: c["data"] for c in json.loads(Path(yol).read_text(encoding="utf-8"))["yedek"]["combos"]}
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    canli = dict(c.execute("select name, data from combos"))
    c.close()
    sil, sapan = plan(yedek, canli)
    print(f"yedek {Path(yol).name} · sil {sil or '-'} · sapan {sapan or '-'} · eksik {sorted(set(yedek) - set(canli)) or '-'}")
    if kip != "uygula":
        return 0
    for ad in sil:
        r = subprocess.run([shutil.which("omniroute"), "combo", "delete", ad, "--yes"], capture_output=True, text=True,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        print(f"  {ad} silme çıkış {r.returncode}")
        if r.returncode:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
