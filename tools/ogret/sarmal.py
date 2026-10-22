"""EGITIM-1: ucretsiz/yerel model istemini damitilmis sablonlarla sarar. onek(tur, zor=False) -> metin; tur: kod|cikarim|mantik|genel (ornek-<tur>.md varsa eklenir).
Havuz: kaydet(tur, istem, yanit) DOGRULANMIS basarili ornegi .kos/kopru/ogret/havuz.jsonl'e ekler; onek ayni turden son 2 ornegi few-shot olarak sona koyar."""
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SB = Path(__file__).resolve().parent / "sablonlar"
HAVUZ = KOK / ".kos/kopru/ogret/havuz.jsonl"


def _oku(ad):
    p = SB / f"{ad}.md"
    return p.read_text(encoding="utf-8").strip() + "\n\n" if p.exists() else ""


def kaydet(tur, istem, yanit):
    HAVUZ.parent.mkdir(parents=True, exist_ok=True)
    k = dict(tur=tur, istem=istem[:400], yanit=yanit[:600])
    if HAVUZ.exists() and k["istem"] in HAVUZ.read_text(encoding="utf-8"):
        return
    with HAVUZ.open("a", encoding="utf-8") as f:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")


def _havuzdan(tur):
    if not tur or not HAVUZ.exists():
        return ""
    s = [json.loads(x) for x in HAVUZ.read_text(encoding="utf-8").splitlines() if x.strip()]
    s = [x for x in s if x["tur"] == tur][-2:]
    return "".join(f"Doğrulanmış örnek:\nİstek: {x['istem']}\nYanıt: {x['yanit']}\n\n" for x in s)


def onek(tur=None, zor=False):
    return _oku("is-yapma-kalibi") + (_oku("dusunme-kalibi") if zor else "") + (_oku(f"ornek-{tur}") if tur else "") + _havuzdan(tur)
