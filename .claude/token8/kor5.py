"""kapi5_<no>_<kol>.json → kör yargı + sayım.
  python kor5.py kor   → kapi5_kor.md (görev başına X/Y karışık, yalnız son yanıt) + kapi5_anahtar.json
  python kor5.py say   → kapi5_puan.json ({"1": {"X": 0-2, "Y": 0-2}, ...}) ile A/B ölçütleri + kapı"""
import json, random, sys
from pathlib import Path

BURA = Path(__file__).parent
sys.path.insert(0, str(BURA))
from kapi5 import GOREV

BEKLENEN = {1: ("departman-frontend", "frontend-craft"), 2: ("test-driven-development", "departman-test-qa"),
            3: ("systematic-debugging", "debugging-and-error-recovery"), 4: ("departman-veri-db", "supabase"),
            5: ("departman-surec-inceleme", "code-review")}
HAM_TAVAN = 20000  # kr; görev 6–8'de bağlama dökülen araç sonucu


def oku(no, kol):
    return json.loads((BURA / f"kapi5_{no}_{kol}.json").read_text(encoding="utf8"))


def skill_dogru(j, no):  # Skill çağrısı ya da skill dosyasının Read'i
    return int(any(a.split(":")[0] in ("Skill", "Read") and any(b in a for b in BEKLENEN[no]) for a in j["araclar"]))


def ctx_kullanim(j):  # sıkı: ctx_ aracı; gevşek (görev ölçütü): ham sonuç ≤ tavan ve veri aracı kullanıldı
    sik = int(any("ctx_" in a for a in j["araclar"]))
    return sik, int(j["arac_sonuc_kr"] <= HAM_TAVAN and j["ctx_payi"].split("/")[1] != "0")


def kor():
    rnd, anahtar, md = random.Random(1813), {}, []
    for no, g in enumerate(GOREV, 1):
        x, y = ("A", "B") if rnd.random() < 0.5 else ("B", "A")
        anahtar[no] = {"X": x, "Y": y}
        md.append(f"## {no}. {g}\n\n### X\n{oku(no, x).get('result') or '(yanıt yok)'}\n\n### Y\n{oku(no, y).get('result') or '(yanıt yok)'}\n")
    (BURA / "kapi5_kor.md").write_text("\n".join(md), encoding="utf8")
    (BURA / "kapi5_anahtar.json").write_text(json.dumps(anahtar), encoding="utf8")
    print("kör", len(md), "görev")


def say():
    anahtar = json.loads((BURA / "kapi5_anahtar.json").read_text(encoding="utf8"))
    puan = json.loads((BURA / "kapi5_puan.json").read_text(encoding="utf8"))
    t = {k: {"skill": 0, "ctx": 0, "ctx_sik": 0, "kalite": 0} for k in "AB"}
    for no in range(1, len(GOREV) + 1):
        satir = []
        for kol in "AB":
            j = oku(no, kol)
            harf = next(h for h, k in anahtar[str(no)].items() if k == kol)
            t[kol]["kalite"] += puan[str(no)][harf]
            if no in BEKLENEN:
                t[kol]["skill"] += skill_dogru(j, no)
            else:
                sik, gev = ctx_kullanim(j)
                t[kol]["ctx_sik"] += sik; t[kol]["ctx"] += gev
            skl = [a for a in j["araclar"] if a.startswith("Skill")]
            satir.append(f"{kol}: tur {j.get('num_turns')} ctx {j['ctx_payi']} ham {j['arac_sonuc_kr']} skill {skl} kalite {puan[str(no)][harf]}")
        print(no, " | ".join(satir))
    kabul = all(t["B"][m] >= t["A"][m] for m in ("skill", "ctx", "kalite"))
    print(json.dumps(t), "KAPI", "KABUL" if kabul else "RET")


if __name__ == "__main__":
    {"kor": kor, "say": say}[sys.argv[1]]()
