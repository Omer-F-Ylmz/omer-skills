"""YEREL-GORSEL-TURBO ölçümü: python turbo_olcum.py <model> <cikti_klasoru> -> tepe RAM % · tepe VRAM % · süre/prompt (TSV).
Önce `gorsel_uret.py ac` açılmış olmalı; bu betik yalnız `uret` çağırır ve 0.5 sn'de bir örnekler."""
import subprocess
import sys
import threading
import time
from pathlib import Path

PROMPTLAR = {
    "logo": "a minimalist flat vector logo icon of a coffee cup with steam, bold shapes, white background",
    "portre": "portrait photo of a young woman with freckles, soft window light, 85mm lens, shallow depth of field",
    "sahne": "a cozy mountain cabin at dusk, warm lit windows, snow, pine forest, volumetric fog, cinematic",
    "urun": "studio product photo of a matte black wireless headphone on a white seamless background, soft shadow",
    "metinli": "a bold social media cover with the words \"YENI SEZON\" in big white letters on a deep blue gradient",
}
UT = Path(__file__).resolve().parent / "gorsel_uret.py"
CNW = 0x08000000


def ornekle(tepe, dur):
    import psutil
    while not dur.is_set():
        tepe["ram"] = max(tepe["ram"], psutil.virtual_memory().percent)
        v = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, creationflags=CNW).stdout.split(",")
        tepe["vram"] = max(tepe["vram"], 100 * float(v[0]) / float(v[1]))
        time.sleep(0.5)


def main(model, cikti, adlar):
    tepe, dur = {"ram": 0.0, "vram": 0.0}, threading.Event()
    threading.Thread(target=ornekle, args=(tepe, dur), daemon=True).start()
    print("prompt\tsn\texit\ttepe_ram_%\ttepe_vram_%")
    for ad in adlar:
        bas = time.time()
        r = subprocess.run([sys.executable, str(UT), "uret", "--is", "foto", "--model", model, "--prompt", PROMPTLAR[ad],
                            "--cikti", str(Path(cikti) / ad), "--adet", "1", "--tohum", "42", "--boyut", "1024x1024"],
                           capture_output=True, text=True, creationflags=CNW)
        print(f"{ad}\t{time.time() - bas:.1f}\t{r.returncode}\t{tepe['ram']:.1f}\t{tepe['vram']:.1f}", flush=True)
        if r.returncode:
            print(r.stdout[-300:], r.stderr[-300:])
    dur.set()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:] or list(PROMPTLAR))
