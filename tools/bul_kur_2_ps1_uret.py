"""BUL-KUR-2 adim 5: kurulum-coz-6.tsv (DOGRULANDI) winget/vscode/blender/hf satirlarindan tools/kurulum_coz6.ps1 uretir (sablon: kurulum_gurultu.ps1 ust kismi).
>2 GB hf satirlari yorum + rapor/omer-sor-2gb-coz6.md. Kurulum yapmaz."""
import csv, json, re, sys, urllib.request
from pathlib import Path
csv.field_size_limit(10**7)
R = Path(__file__).resolve().parents[1]
sab = (R / "tools/kurulum_gurultu.ps1").read_text(encoding="utf-8-sig").split("\n")
bas = []
for l in sab:
    if l.startswith("# ---"): break
    bas.append(l)
bas = "\n".join(bas).replace("kurulum-gurultu-sonuc.tsv", "kurulum-coz6-sonuc.tsv").replace("GURULTU-KUR-1", "BUL-KUR-2").replace("kurulum-gurultu", "kurulum-coz6")
rows = list(csv.DictReader(open(R / "docs/video-tarama/kurulum-coz-6.tsv", encoding="utf-8"), delimiter="\t"))
sat, buyuk, say = [], [], 0
def hf_boyut(rp):
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(f"https://huggingface.co/api/models/{rp}?blobs=true", headers={"User-Agent": "omer-skills"}), timeout=30))
        return sum((s.get("size") or 0) for s in j.get("siblings", [])), (j.get("cardData") or {}).get("license", "?")
    except Exception: return -1, "?"
for r in rows:
    if r["sonuc"] != "DOGRULANDI": continue
    k, kay = r["kalem"], r["kaynak"]
    ad = k.replace("'", "''")
    if kay.startswith("winget:"):
        sat.append(f"# --- {k} | WINGET | {r['gerekce'][:60]}\nKur5Winget '{ad}' '{kay[7:]}'"); say += 1
    elif kay.startswith("vscode:"):
        sat.append(f"# --- {k} | VSCODE\nKur5Vscode '{ad}' '{kay[7:]}'"); say += 1
    elif kay.startswith("hf:"):
        b, lic = hf_boyut(kay[3:])
        if b < 0 or b > 2 * 2**30:
            g = f"{b/2**30:.2f} GiB" if b >= 0 else "boyut okunamadi"
            sat.append(f"# --- {k} | OMER-SOR | {lic} | {g}\n# OMER-SOR ({g}): hf download {kay[3:]}"); buyuk.append((k, kay[3:], g, lic))
        else:
            sat.append(f"# --- {k} | HF | {lic} | {b/2**30:.2f} GiB\n# hf download {kay[3:]}  (kucuk: Omer hf CLI ile indirir)"); say += 1
    elif kay.startswith("blender:"):
        sat.append(f"# --- {k} | BLENDER\n# blender uzantisi: Blender icinde Edit>Preferences>Get Extensions: {kay[8:]}")
(R / "tools/kurulum_coz6.ps1").write_text("﻿" + bas + "\n" + "\n".join(sat) + "\n", encoding="utf-8")
rep = ["---", "type: report", "status: done", "tags: [bul-kur-2, 2gb]", "relatedTo: [rapor/bul-kur-2.md]", "---", "# >2 GB / OMER-SOR (BUL-KUR-2)", "kalem | hf repo | boyut | lisans"]
rep += [" | ".join(x) for x in buyuk] or ["(yok)"]
(R / "rapor/omer-sor-2gb-coz6.md").write_text("\n".join(rep) + "\n", encoding="utf-8")
print("calisan satir", say, "buyuk", len(buyuk))
