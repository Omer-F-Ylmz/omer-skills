"""arka.py icin: olc.mjs'i out/ icinde olmayan siteler icin tek tek koşar (site basi 150 sn tavan)."""
import os, re, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ads = re.findall(r"\['([\w-]+)', 'https", open("olc.mjs", encoding="utf-8").read())
for ad in ads:
    if os.path.exists(f"out/{ad}.json"):
        continue
    try:
        r = subprocess.run(["node", "olc.mjs", ad], timeout=150, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", creationflags=0x08000000)
        print(ad, "rc", r.returncode, (r.stdout + r.stderr).strip()[-300:], flush=True)
    except subprocess.TimeoutExpired:
        print(ad, "ZAMAN ASIMI", flush=True)
print("BITTI", flush=True)
