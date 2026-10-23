"""BEYIN-FIX-1 kırmızı testi: hedef dosyayı başka süreç okurken yazım WinError 5 ile düşmemeli.
Çalıştır: python tools/atomik_yaz_test.py [okuyucu_süre_sn] (çıkış 0 = yeşil; varsayılan 0.3)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "ogrenme"))
import beyin_dusun  # noqa: E402
import ucretsiz_havuz  # noqa: E402


TUT = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3


def okuyucu_tut(yol, saniye):
    """Başka süreç hedefi açık tutar (Python open() FILE_SHARE_DELETE koymaz → os.replace reddedilir)."""
    kod = f"import time\nf = open(r'{yol}', 'rb')\nprint('acik', flush=True)\ntime.sleep({saniye})\nf.close()\n"
    p = subprocess.Popen([sys.executable, "-I", "-c", kod], stdout=subprocess.PIPE, text=True)
    p.stdout.readline()
    return p


def sına(ad, fn):
    with tempfile.TemporaryDirectory() as d:
        yol = Path(d) / "durum.json"
        yol.write_text("{}", encoding="utf-8")
        p = okuyucu_tut(yol, TUT)
        try:
            fn(yol)
        except PermissionError as e:
            print(f"KIRMIZI {ad}: PermissionError {e}")
            return False
        finally:
            p.wait()
        ok = json.loads(yol.read_text(encoding="utf-8")) == {"ok": 1}
        print(f"{'YESIL' if ok else 'KIRMIZI'} {ad}")
        return ok


def bayt_yaz(yol):
    beyin_dusun._yaz_bayt(yol, json.dumps({"ok": 1}))


def havuz_yaz(yol):
    ucretsiz_havuz.DIZIN, ucretsiz_havuz.DURUM = yol.parent, yol
    ucretsiz_havuz._yaz({"ok": 1})


if __name__ == "__main__":
    sonuc = [sına("beyin_dusun._yaz_bayt", bayt_yaz), sına("ucretsiz_havuz._yaz", havuz_yaz)]
    sys.exit(0 if all(sonuc) else 1)
