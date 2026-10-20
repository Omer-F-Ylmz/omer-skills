"""BEYIN-3 yoklama: sorular.jsonl'de cevabın sayı/terim anahtarları beyin.py çıktısının ilk N parçasında mı?"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import beyin  # noqa: E402

D = Path(__file__).parent


def anahtar(cevap):
    return re.findall(r"\d[\d.,]*\d|\d", cevap)


def calis(dosya, ilk=3, k=3, ids=None):
    sonuc = []
    for s in (D.parent / "beyin2" / dosya).read_text(encoding="utf-8").splitlines():
        if not s.strip():
            continue
        q = json.loads(s)
        if ids and q["id"] not in ids:
            continue
        parca = beyin.ara(q["soru"], k)
        metin = "\n".join("\n".join(p[2]) for p in parca[:ilk])
        ek = anahtar(q["cevap"])
        eksik = [a for a in ek if a not in metin]
        sonuc.append((q["id"], not eksik, eksik, sum(len("\n".join(p[2])) for p in parca)))
    return sonuc


if __name__ == "__main__":
    ids = {int(x) for x in sys.argv[2:]} or None
    r = calis(sys.argv[1] if len(sys.argv) > 1 else "sorular.jsonl", ids=ids)
    print(f"{sum(x[1] for x in r)}/{len(r)} anahtar tamam; ort. çıktı {sum(x[3] for x in r) // max(len(r), 1)} kar.")
    for i, ok, eksik, _ in r:
        if not ok:
            print(i, "eksik", eksik)
