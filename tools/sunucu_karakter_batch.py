"""SUNUCU-KARAKTER-1: yerel Z-Image-Turbo ile iki marka karakteri toplu üretim (donus 3 · ifade 6 · poz 10).
Kullanım: GORSEL_PORT=<port> python tools/sunucu_karakter_batch.py [marka]   (ComfyUI önceden `gorsel_uret.py ac` ile açık)
Aynı karakter açıklaması + sabit tohum = tutarlılık reçetesi; yalnız poz/ifade/kamera cümlesi değişir. Üretilmiş dosya atlanır."""
import os, subprocess, sys
from pathlib import Path

KOK = Path.home() / "Desktop" / "Claude ile yapılanlar" / "sosyal-oto" / "sunucu"
STIL = "stylized 3D animated mascot character, glossy toy-like render, soft studio lighting, clearly a cartoon creature not a real person, no text"
KARAKTER = {
    "free-ai-drop": ("Dropi, a friendly robot-fox host in a glossy neon lime green astronaut suit with a round clear helmet visor, "
                     "orange fox face, big black eyes, pink bow tie, violet gloves and boots, small headphones",
                     "deep dark purple background with faint falling light lines"),
    "curiosity-well": ("Wells, a small wise owl explorer host with warm amber feathers and cream chest, round brass goggles on forehead, "
                       "deep teal hooded explorer cloak with a tiny glowing amber lantern star charm, big curious amber eyes",
                       "midnight navy background with soft stardust and faint concentric well-ring glow"),
}
SEED = {"free-ai-drop": 101, "curiosity-well": 202}
DONUS = {"on": "front view, full body, standing", "yan": "side profile view, full body, standing",
         "uc-ceyrek": "three-quarter view, full body, standing"}
IFADE = {"merak": "head and shoulders close-up, curious expression, head tilted, eyes wide, small smile",
         "saskinlik": "head and shoulders close-up, surprised expression, mouth open in an O, eyes huge",
         "gulme": "head and shoulders close-up, laughing joyfully, eyes happily squinted",
         "iste-bu": "head and shoulders close-up, triumphant 'that's it!' expression, one finger raised, grin",
         "suphe": "head and shoulders close-up, skeptical expression, one eyebrow raised, side glance",
         "notr": "head and shoulders close-up, calm neutral expression, looking at camera"}
POZ = ["waving hello with one hand, full body", "pointing to the right with one arm, full body",
       "holding a glowing tablet, looking at it, full body", "thumbs up, full body", "sitting cross-legged, full body",
       "walking forward mid-step, full body", "arms crossed thinking, full body", "jumping with joy, full body",
       "holding a magnifying glass up to one eye, full body", "presenting with both arms open toward the viewer, full body"]


def isler(marka):
    kar, zemin = KARAKTER[marka]
    s = SEED[marka]
    for ad, c in DONUS.items():
        yield KOK / marka / "uretim" / "donus", f"{ad}", f"{STIL}. {kar}. {c}. {zemin}", s
    for ad, c in IFADE.items():
        yield KOK / marka / "uretim" / "ifade", f"{ad}", f"{STIL}. {kar}. {c}. {zemin}", s
    for i, c in enumerate(POZ, 1):
        yield KOK / marka / "uretim" / "poz", f"poz-{i:02d}", f"{STIL}. {kar}. {c}. {zemin}", s


for marka in (sys.argv[1:] or KARAKTER):
    for klasor, ad, prompt, seed in isler(marka):
        if list(klasor.glob(f"{ad}.png")):
            continue
        gecici = klasor / f"_{ad}"
        r = subprocess.run([sys.executable, str(Path(__file__).with_name("gorsel_uret.py")), "uret", "--is", "foto", "--model", "turbo",
                            "--prompt", prompt, "--cikti", str(gecici), "--tohum", str(seed), "--boyut", "1024x1024"],
                           capture_output=True, text=True, timeout=900, env={**os.environ, "GORSEL_PORT": os.environ["GORSEL_PORT"]})
        png = next(iter(gecici.glob("*.png")), None) if gecici.exists() else None
        if png:
            png.replace(klasor / f"{ad}.png")
            png.with_suffix(".json").replace(klasor / f"{ad}.json")
            print("TAMAM", marka, ad, flush=True)
        else:
            print("HATA", marka, ad, (r.stdout + r.stderr)[-200:], flush=True)
print("BITTI")
