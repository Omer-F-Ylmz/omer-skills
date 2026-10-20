"""TOKEN-REA d7 iş deseni kolu: köprü görev şablonu (tur tavanı · okuma listesi · delegasyon yok · kısa yanıt) A/B.
2 görev x 2 kol x 2 tekrar = 8 `claude -p` (tavan 15). A = çıplak soru, B = şablonlu soru. Kalite = yanıtta çapa dizgeleri.
Kullanım: python -I is_deseni_ab.py   → is_deseni_ab.json"""
import json, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
CIKTI = Path(__file__).with_suffix(".json")
DOSYA = ".kos/kopru/token-rea/rtk2.py"
GOREVLER = [
    ("tavan", f"{DOSYA} içinde çıktı özetleme eşiği (TAVAN) kaç karakter ve eşik üstünde tam metin nereye saklanıyor?", ["1500", "rtk2-ac"]),
    ("branch", f"{DOSYA} içindeki tur() fonksiyonu `git branch` için hangi türü döndürür?", ["ham"]),
]
SABLON = ("KÖPRÜ GÖREVİ. Tur tavanı: en çok 4 araç çağrısı. Okuma listesi: yalnız {dosya} (önce Grep ile satırı bul, sonra Read ile ≤30 satır). "
          "Alt ajan çağırma, başka dosya açma, graphify/sor2 kullanma. Yanıt ≤3 satır.\nSORU: {soru}")


def kos(istem):
    t = time.time()
    p = subprocess.run(["claude", "-p", "--output-format", "json", "--max-turns", "12"], input=istem, capture_output=True, text=True,
                       encoding="utf-8", cwd=KOK, timeout=420, creationflags=0x08000000)
    j = json.loads(p.stdout)
    u = sum(m.get("inputTokens", 0) + m.get("cacheReadInputTokens", 0) + m.get("cacheCreationInputTokens", 0) for m in j.get("modelUsage", {}).values())
    agirlikli = sum(m.get("inputTokens", 0) + .1 * m.get("cacheReadInputTokens", 0) + 1.25 * m.get("cacheCreationInputTokens", 0) + 5 * m.get("outputTokens", 0)
                    for m in j.get("modelUsage", {}).values())
    return {"girdi": u, "agirlikli": round(agirlikli), "tur": j.get("num_turns"), "sn": round(time.time() - t), "usd": j.get("total_cost_usd"), "yanit": (j.get("result") or "")[:300]}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sonuc = []
    for tekrar in range(2):
        for ad, soru, capa in GOREVLER:
            for kol in ("A", "B"):
                istem = soru if kol == "A" else SABLON.format(dosya=DOSYA, soru=soru)
                r = kos(istem); r.update(gorev=ad, kol=kol, tekrar=tekrar, dogru=all(c in r["yanit"] for c in capa))
                sonuc.append(r); print(ad, kol, tekrar, r["girdi"], r["agirlikli"], r["tur"], r["dogru"], flush=True)
                CIKTI.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    for kol in ("A", "B"):
        L = [r for r in sonuc if r["kol"] == kol]
        print(kol, "ağırlıklı", sum(r["agirlikli"] for r in L), "girdi", sum(r["girdi"] for r in L), "tur", sum(r["tur"] or 0 for r in L), "doğru", sum(r["dogru"] for r in L), "/", len(L))
