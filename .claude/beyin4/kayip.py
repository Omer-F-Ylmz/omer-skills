"""BEYIN-4 kayıp türü tanısı (ayar değil): sorular-<tohum>.jsonl için `beyin.py ara` çıktısında cevap parçası var mı;
hakem sonucuyla çaprazla. Tür: A=kaynak aramada yok · B=kaynak var, cevap metni çıktıda yok · C=cevap çıktıda, model yanlış.
Kullanım: python .claude/beyin4/kayip.py [tohum ...]  (varsayılan 2007 2008; hakem = beyin3/kosu/hakem<tohum>-1.json)"""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).parent
KOK = D.parent.parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402


def cevap_var(cevap, out):
    """Cevaptaki sayıların hepsi çıktıda tam sayı olarak; sayı yoksa ≥%60 sözcük örtüşmesi."""
    sayilar = re.findall(r"\d+(?:[.,]\d+)?", cevap)
    if sayilar:
        return all(re.search(rf"(?<![\d.,]){re.escape(s)}(?![\d])", out) for s in sayilar)
    sz = {w for w in re.findall(r"\w{4,}", cevap.lower())}
    return bool(sz) and sum(w in out for w in sz) / len(sz) >= 0.6


def tani(q, out, dogru):
    ks = [re.sub(r":\d+$", "", k.strip()).replace("\\", "/") for k in q["kaynak"].split(";")]
    kaynak = all(Path(k).stem.lower() in out for k in ks)
    parca = [p.strip() for p in re.split(r";|\bve\b", q["cevap"]) if p.strip()] if q.get("cok") else [q["cevap"]]
    cevapta = all(cevap_var(p, out) for p in parca)
    if dogru:
        return "doğru"
    return "C-model" if cevapta else ("B-parça-içi" if kaynak else "A-aramada-yok")


def main():
    sayac = Counter()
    for t in [int(x) for x in sys.argv[1:]] or (2007, 2008):
        qs = [json.loads(s) for s in (D.parent / f"beyin3/sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
        yol = D.parent / f"beyin3/kosu/hakem{t}-1.json"
        d = {p.get("id"): p.get("d", 0) for p in kapi.satirlar(json.loads(yol.read_text(encoding="utf-8")))}
        for q in qs:
            out = subprocess.run([sys.executable, "tools/beyin.py", "ara", q["soru"]], capture_output=True, text=True,
                                 encoding="utf-8", cwd=KOK).stdout.lower().replace("\\", "/")
            tur = ("çok" if q.get("cok") else "tek") + "/" + ("sira" if re.search(r"ajan-sira|SIRA\.md", q["kaynak"]) else "diğer")
            sayac[(tur, tani(q, out, d.get(q["id"])))] += 1
    for k, v in sorted(sayac.items()):
        print(*k, v)


if __name__ == "__main__":
    main()
