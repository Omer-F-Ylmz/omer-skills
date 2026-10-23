import sys
sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
import kurulum2b as k

for p in k.NPM:
    var = k.calis(["npm.cmd", "ls", "-g", p, "--depth=0"])[0] == 0
    rc = 0 if var else k.calis(["npm.cmd", "i", "-g", p])[0]
    print(f"npm {p}: {'zaten' if var else f'rc={rc}'}", flush=True)
    k.beyin(f"2c npm {p} rc={rc}")
print("BITTI", flush=True)
