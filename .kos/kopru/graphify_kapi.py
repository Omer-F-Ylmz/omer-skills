"""GRAPHIFY-RAM-1 kalite kapısı: python graphify_kapi.py once|sonra → rapor/graphify-ram-1/<etiket>/*.txt
5 graphify query + cc-kopru oku iskelet/sembol çıktısını yazar; karşılaştırma `python graphify_kapi.py fark`."""
import os, subprocess, sys

kok = r"C:\Projeler\omer-skills"
hedef = os.path.join(kok, ".kos", "kopru", "rapor", "graphify-ram-1")
DISLANAN = (".claude/t7f2-birlesik", ".claude/b2-aile", ".claude/b2-olcum", ".claude/v13", ".claude/v9",
            ".claude/b20_gl", ".claude/cagri-sayac", ".secim", ".playwright-cli")
SORGU = ["cc-kopru oku iskelet nasil calisir", "onay betigi hedefler", "video tarama rapor denetle",
         "skill paket zip denetle", "olcum ram bos"]
OKU = [("iskelet", "tools/cc-kopru/oku.mjs", ""), ("sembol", "tools/cc-kopru/oku.mjs", "grafYukle"),
       ("iskelet", "onay/blender_5_uygula.py", ""), ("sembol", "tools/olcum/kosucu.py", "bos_ram_gb")]
JS = ("import {oku} from './tools/cc-kopru/oku.mjs';"
      "const [m,d,a]=process.argv.slice(1);console.log(JSON.stringify(oku({kok:process.cwd(),mod:m,dosya:d,ad:a||undefined}),null,1))")


def kos(komut):
    r = subprocess.run(komut, cwd=kok, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       creationflags=0x08000000)
    return r.stdout + r.stderr


def temiz(metin):
    return [s for s in metin.splitlines() if not any(d in s.replace("\\", "/") for d in DISLANAN)]


if sys.argv[1] == "fark":
    once, sonra = (os.path.join(hedef, e) for e in ("once", "sonra"))
    for ad in sorted(os.listdir(once)):
        a, b = (temiz(open(os.path.join(d, ad), encoding="utf-8").read()) for d in (once, sonra))
        print(ad, "AYNI" if a == b else f"FARK ({len(set(a) ^ set(b))} satır)")
    sys.exit()
dizin = os.path.join(hedef, sys.argv[1])
os.makedirs(dizin, exist_ok=True)
for i, s in enumerate(SORGU):
    open(os.path.join(dizin, f"sorgu{i}.txt"), "w", encoding="utf-8").write(kos(["graphify", "query", s]))
for i, (m, d, a) in enumerate(OKU):
    open(os.path.join(dizin, f"oku{i}.txt"), "w", encoding="utf-8").write(
        kos(["node", "--input-type=module", "-e", JS, m, d, a]))
print("yazıldı:", dizin)
