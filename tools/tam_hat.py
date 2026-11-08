"""TAM-HAT (5 Kas, Ömer: 2958 videonun BÜTÜN kalemleri): kapsam = arac + kutuphane + ui-kutuphane,
durum = KURULMADI-SIRADA/BULUNAMADI/KAYITSIZ/KURULU-KANITSIZ/KURULUM-HATA.
Sıra: coz (yalnız henüz çözülmemiş video+kalem) -> indir (sıkı zaten_var) -> kurulum_eksik (npm/pypi/gh boşlukları) -> kalem_denetim.
Log: .kos/kopru/tam-hat.log
"""
import os, subprocess, sys, time
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(KOK, ".kos", "kopru", "tam-hat.log")
env = dict(os.environ, KAPSAM="tam", PYTHONIOENCODING="utf-8")


def adim(ad, args):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"\n=== {time.strftime('%H:%M:%S')} {ad} başladı ===\n"); f.flush()
        rc = subprocess.run([sys.executable, "-u"] + args, cwd=KOK, env=env, stdout=f, stderr=subprocess.STDOUT, creationflags=0x08000000).returncode
        f.write(f"=== {time.strftime('%H:%M:%S')} {ad} bitti rc={rc} ===\n")
    return rc


adim("COZ", ["tools/kurulum_coz2.py", "coz"])
adim("INDIR", ["tools/kurulum_coz2.py", "indir"])
adim("EKSIK", ["tools/kurulum_eksik.py"])
adim("DENETIM", ["tools/kalem_denetim.py"])
open(LOG, "a", encoding="utf-8").write(f"=== {time.strftime('%H:%M:%S')} TAM-HAT-BITTI ===\n")
