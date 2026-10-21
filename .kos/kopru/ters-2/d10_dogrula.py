"""d10: taslak maddelerin alıntısını gerçek dosyada satır bazında mekanik doğrular."""
import ast, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from d10_taslak import HEDEF, OUT


def yukle(ad):
    m = re.search(r"\[.*\]", (OUT / f"{ad}.md").read_text(encoding="utf-8"), re.S)
    try:
        return json.loads(m.group(0))
    except ValueError:
        return ast.literal_eval(m.group(0))


def kontrol(ad):
    tur, kaynaklar, _ = HEDEF[ad]
    yol = {Path(k).name: k for k in kaynaklar}
    iyi, kotu = [], []
    for m in yukle(ad):
        k = yol.get(Path(str(m.get("dosya", ""))).name) or (kaynaklar[0] if len(kaynaklar) == 1 else None)
        if not k:
            kotu.append((m, "dosya yok")); continue
        satirlar = Path(k).read_text(encoding="utf-8", errors="replace").splitlines()
        n, a = int(m["satir"]), m["alinti"].strip()
        bulundu = next((i for i in sorted(range(1, len(satirlar) + 1), key=lambda i: abs(i - n)) if a in satirlar[i - 1]), None)
        if bulundu is None:
            kotu.append((m, "alıntı dosyada yok"))
        else:
            iyi.append({"madde": m["madde"], "kanit": {"dosya": k, "satir": bulundu, "alinti": a}, "_kayma": bulundu - n})
    return iyi, kotu


if __name__ == "__main__":
    for ad in sys.argv[1:] or HEDEF:
        try:
            iyi, kotu = kontrol(ad)
        except Exception as e:
            print(ad, "HATA", type(e).__name__, str(e)[:80]); continue
        print(f"{ad}: {len(iyi)} iyi, {len(kotu)} kötü; kayma {[x['_kayma'] for x in iyi]}")
        for m, n in kotu:
            print("   X", n, str(m)[:140])
