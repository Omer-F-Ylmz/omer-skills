"""VIDEO-IZLE-KUR-1 tur 2: ucretsiz havuzda mistral sogumasi bitene dek bekler, sonra cikar (tur 1) ve v2arac'i sirayla kosar.
Kullanim: python -I -X utf8 video_izle_kur_1_bekle.py   (arka.py --bagimsiz ile)"""
import json, subprocess, sys, time
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
O = K / ".kos/kopru/ogren"
while (s := json.loads((K / ".kos/kopru/ucretsiz/durum.json").read_text(encoding="utf-8")).get("soguma", {}).get("p:mistral", 0)) > time.time():
    print("bekle mistral", round((s - time.time()) / 60), "dk", flush=True)
    time.sleep(min(600, s - time.time() + 30))
for b, a in (("video_izle_kur_1_cikar.py", ["1"]), ("video_izle_kur_1_v2arac.py", [])):
    print("KOS", b, flush=True)
    subprocess.run([sys.executable, "-I", "-X", "utf8", str(O / b), *a], cwd=K, creationflags=0x08000000)
print("BITTI")
