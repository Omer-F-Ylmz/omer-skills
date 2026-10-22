"""ZORUNLU-ARAÇ-3 katman 3: kombin seçimi + doğrulama (yerel, jetonsuz).

python tools/kombin_sec.py sec "<görev metni>" [--k 2] [--tur site-3d]  → en iyi k kombin, tek satır (ad: a>b>c)
python tools/kombin_sec.py dogrula                                      → kombin/tur seti adları katalogda var mı
"""
import json
import re
import sys
from pathlib import Path

K = Path(__file__).resolve().parent.parent
KOMBIN = K / "tools/kombinler.json"
TUR_SET = K / "tools/tur_setleri.json"
KATALOG = K / "docs/katalog/yetenek.jsonl"
# katalog dışı ama gerçek: betik/ajan/hafıza adları
EK = {"beyin", "ruflo", "laya", "claude-mem", "gorsel_hakem", "cc-kopru", "okuyucu", "suite-kosucu", "ucuz_alt", "katalog_ara",
      "zip_denetle", "slash_zip", "skill_denetim", "varlik_indir", "design-extractor", "gltf-transform", "mcp-launch", "lenis",
      "rea-agents", "understand", "find-skills", "zaproxy", "context-mode", "strategic-compact"}


def yukle(yol):
    return json.loads(yol.read_text(encoding="utf-8"))


def bilinen():
    ad = set(EK)
    for s in KATALOG.read_text(encoding="utf-8").splitlines():
        o = json.loads(s)
        ad.add(o["ad"].lower())
        ad.add(re.split(r"[:/]", o["ad"])[-1].lower())
    ad |= {p.stem.lower() for p in (K / "tools").glob("*.py")} | {p.stem.lower() for p in (K / ".kos/kopru").glob("*.py")}
    ad |= {p.name.lower() for p in (K / "skills").iterdir() if p.is_dir()} if (K / "skills").is_dir() else set()
    return ad


def dogrula():
    ad = bilinen()
    yok = []
    for k in yukle(KOMBIN)["kombinler"]:
        yok += [(k["id"], a) for a, _ in k["adimlar"] if a.lower() not in ad and re.split(r"[:/]", a)[-1].lower() not in ad]
    for t, s in yukle(TUR_SET)["turler"].items():
        yok += [(t, a) for g in ("skill", "mcp", "cli") for a in s.get(g, []) if a.lower() not in ad and re.split(r"[:/]", a)[-1].lower() not in ad]
    return yok


def sec(metin, k=2, tur=None):
    """tur verilmezse görev metnindeki tür deseniyle bulunur; tür içi sıra = anahtar kelime örtüşmesi (amac+id+adım adları)."""
    ks = yukle(KOMBIN)["kombinler"]
    if not tur:
        say = {t: len(re.findall(d, metin)) for t, d in yukle(TUR_SET)["desen"].items()}
        tur = max(say, key=say.get) if any(say.values()) else None
    kelime = set(re.findall(r"[\w]{4,}", metin.lower()))
    adaylar = [o for o in ks if o["tur"] == tur] if tur else []
    puan = lambda o: len(kelime & set(re.findall(r"[\w]{4,}", (o["amac"] + " " + o["id"] + " " + " ".join(a for a, _ in o["adimlar"])).lower()))) \
        - (0.1 if o["jeton"] == "orta" else 0.2 if o["jeton"] == "pahali" else 0)  # eşitlikte ucuz önde
    return tur, sorted(adaylar, key=puan, reverse=True)[:k]


def satir(o):
    return f"{o['id']}: " + ">".join(a for a, _ in o["adimlar"])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1 and sys.argv[1] == "dogrula":
        yok = dogrula()
        print(f"{len(yukle(KOMBIN)['kombinler'])} kombin · bilinmeyen {len(yok)}")
        for x in yok:
            print(*x)
    elif len(sys.argv) > 2 and sys.argv[1] == "sec":
        a = sys.argv
        tur, ks = sec(a[2], int(a[a.index("--k") + 1]) if "--k" in a else 2, a[a.index("--tur") + 1] if "--tur" in a else None)
        print(tur or "diğer")
        for o in ks:
            print(satir(o))
