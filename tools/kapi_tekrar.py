"""UCRETSIZ-HAVUZ-2: kapıyı ertesi gün kotalar sıfırlanınca (03:05 yerel) yeniden ölçer: python tools/kapi_tekrar.py [--simdi] [--tavan=N]
Sonuç .kos/kopru/ucretsiz/kapi.json (havuz kolu) + kapi5.log. Arka planda yalnız .kos/kopru/arka.py ile başlat:
python .kos/kopru/arka.py .kos/kopru/ucretsiz/kapi5.log tools/kapi_tekrar.py"""
import datetime as dt, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    n = dt.datetime.now(); h = n.replace(hour=3, minute=5, second=0, microsecond=0)
    if "--simdi" not in sys.argv:
        h = h if h > n else h + dt.timedelta(days=1)
        print("bekleniyor:", h, flush=True)
        while dt.datetime.now() < h:
            time.sleep(60)
    tavan = next((a for a in sys.argv if a.startswith("--tavan=")), "--tavan=100")
    raise SystemExit(subprocess.run([sys.executable, str(KOK / "tools/ucretsiz_kapi.py"), "--havuz", tavan], creationflags=0x08000000).returncode)
