"""SUIT-KIRMIZI-2: kart.jsonl'de etiketi boş kartlara TR+EN arama anahtarı (ücretsiz havuz, Claude jetonu 0).
python tools/etiket_uret.py [en_çok_paket=20]  → docs/arac-kart/kart.jsonl yerinde güncellenir; tekrar koşulabilir."""
import json
import re
import sys
from pathlib import Path

KART = Path(__file__).resolve().parents[1] / "docs/arac-kart/kart.jsonl"
PAKET = 10
ISTEM = ("Each line is a tool/skill/agent: 'name :: description'. For each, write 8-12 search keywords/synonyms that a user might use "
         "to ask for it, mixing ENGLISH and TURKISH. Concrete task words, no tool names, no generic words like 'tool' or 'skill'. "
         "Return ONLY a JSON array: [{\"i\":0,\"t\":\"kw1, kw2, ...\"}, ...]\n\n")


def eksik(kartlar):
    return [k for k in kartlar if not k.get("etiket")]


def doldur(kartlar, uretici, paket=PAKET, tavan=20):
    """En çok `tavan` paket üretici çağrılır; uretici(paket_kartlar) -> {ad: etiket}. Doldurulan kart sayısı döner."""
    n = 0
    for i in range(tavan):
        bek = eksik(kartlar)
        yeni = uretici(bek[:paket]) if bek else {}
        if not yeni:
            break
        for k in kartlar:
            if yeni.get(k["ad"]) and not k.get("etiket"):
                k["etiket"] = yeni[k["ad"]]
                n += 1
    return n


def havuz_uretici(paket):
    import ucretsiz_havuz as uh
    m, _, _ = uh.cagir("kolay", ISTEM + "\n".join(f"{i}. {k['ad']} :: {k.get('ne', '')[:160]}" for i, k in enumerate(paket)),
                       max_tokens=6000, etiket="kart-etiket")
    s = {}
    try:
        liste = json.loads(re.search(r"\[.*\]", m, re.S).group(0)) if m else []
    except (AttributeError, ValueError):
        liste = []
    for o in liste:
        try:
            s[paket[int(o["i"])]["ad"]] = str(o["t"])
        except (KeyError, ValueError, IndexError, TypeError):
            pass
    return s


if __name__ == "__main__":
    tavan = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ks = [json.loads(s) for s in KART.read_text(encoding="utf8").splitlines() if s.strip()]
    n = doldur(ks, havuz_uretici, tavan=tavan)
    KART.write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in ks) + "\n", encoding="utf8")
    print(f"doldurulan {n} · kalan {len(eksik(ks))}")
