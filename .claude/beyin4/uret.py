"""BEYIN-4 tohum üretimi — BETİK üretir (Claude yok): kaynak cümlesindeki bir sayı maskelenir, cevap o sayı.
Her tohum: 6 tek/ajan-sira, 2 tek/SIRA, 4 tek/diğer, 8 çok (iki ayrı kaynak; en az 4'ü ajan-sira ya da SIRA) = 20 soru.
Önceki tohumların (beyin2/beyin3 sorular*.jsonl) kaynak dosyaları ve önceki yeni tohumun kaynakları kullanılmaz.
Kullanım: python .claude/beyin4/uret.py 2009 2010 2011:ad   → sorular-<tohum>.jsonl (cevap = sayı, ":ad" ise backtick adı; çok için "a; b")"""
import json
import random
import re
import sys
from pathlib import Path

D = Path(__file__).parent
KOK = D.parent.parent
sys.path.insert(0, str(KOK / "tools"))
import beyin_al  # noqa: E402

SAYI = re.compile(r"(?<![\w.,/-])\d+(?:[.,]\d+)?(?![\w/-]|\.\d)")  # 127.0.0.1 / 1.2.3 gibi noktalı dizinin parçası sayı değil
SIRA = KOK / ".kos/kopru/gorev/SIRA.md"
DIGER = [KOK / ".kos/kopru/gorev", KOK / ".kos/kopru/gorev-gecmis", KOK / ".kos/kopru/devir", KOK / "docs/ogren", KOK / "docs/kurulumlar"]


def kullanilmis():
    """Önceki tohumların kaynak dosya adları (uzantısız, küçük harf)."""
    s = set()
    for f in [*D.parent.glob("beyin*/sorular*.jsonl"), *D.glob("sorular-*.jsonl")]:
        for q in map(json.loads, filter(str.strip, f.read_text(encoding="utf-8").splitlines())):
            s |= kaynak_kume(q["kaynak"])
    return s


def kaynak_kume(kaynak):
    """"yol:satır; yol:satır" → dosya adı kümesi; SIRA.md yerine "sira:<satır>" (tek dosya, satır bazlı elenir)."""
    s = set()
    for k in kaynak.split(";"):
        y, _, no = k.strip().replace("\\", "/").rpartition(":")
        s.add(f"sira:{no}" if y.endswith("SIRA.md") else Path(y).stem.lower())
    return s


AD = re.compile(r"`[^`\s]{3,40}`")  # sayısal olmayan tohum: cümlede bir kez geçen backtick adı (dosya/komut/kimlik)


def adaylar(yol, satirlar, sayisal=True):
    """[(soru bağlamı, sayı, kaynak "yol:satır")]: ≥6 sözcüklük cümlede, backtick dışında ve cümlede bir kez geçen bir sayı;
    bağlam sayı çevresinde ≤14 sözcük, sayı ___ olur."""
    out = []
    for no, s in enumerate(satirlar, 1):
        for c in beyin_al.cumleler(s):
            yasak = [m.span() for m in re.finditer(r"`[^`\n]*`", c)]
            tum = [x.group() for x in SAYI.finditer(c)]
            tek = [m for m in SAYI.finditer(c) if (len(m.group()) > 1 or "." in m.group()) and tum.count(m.group()) == 1
                   and not any(x <= m.start() < y for x, y in yasak)] if sayisal else [m for m in AD.finditer(c) if c.count(m.group()) == 1]
            if len(c.split()) < 6 or c.count("`") % 2 or not tek:
                continue
            m = tek[0]
            on, son = c[:m.start()].split(), c[m.end():].split()
            out.append((" ".join(on[-7:] + ["___"] + son[:7]), m.group().strip("`"), f"{yol}:{no}"))
    return out


def havuz(yasak, sayisal=True):
    ajan, diger = {}, {}
    for p in sorted((KOK / ".kos/kopru/ajan-sira").glob("*.json")):
        if p.stem.lower() in yasak or f"ajan-{p.stem}".lower() in yasak:
            continue
        try:
            r = json.loads(p.read_text(encoding="utf-8")).get("result") or ""
        except ValueError:
            continue
        if a := adaylar(str(p), r.split("\n"), sayisal):
            ajan[p.stem] = a
    for d in DIGER:
        for p in sorted(d.glob("*.md")):
            if p.stem.lower() not in yasak and (a := adaylar(str(p), p.read_text(encoding="utf-8", errors="replace").split("\n"), sayisal)):
                diger[p.stem] = a
    sira = []
    # SIRA tek dosya: dosya değil, önceki tohumların kullandığı satırlar elenir (yasak kümesinde "sira:<no>")
    satirlar = [s if re.search(r"BİTTİ|KARAR|[Kk]ararı|★|GEÇMEDİ|\bARA\b", s) and f"sira:{n}" not in yasak else ""
                for n, s in enumerate(SIRA.read_text(encoding="utf-8").splitlines(), 1)]
    sira = adaylar(str(SIRA), satirlar, sayisal)
    return ajan, diger, sira


def uret(tohum, yasak, sayisal=True):
    rng = random.Random(tohum)
    ajan, diger, sira = havuz(yasak, sayisal)
    ak, dk = sorted(ajan), sorted(diger)
    rng.shuffle(ak)
    rng.shuffle(dk)
    # SIRA tek dosya: 2 tek + çokların bir kısmı aynı dosyadan farklı satırlar olabilir (aynı satır tekrarlanmaz)
    rng.shuffle(sira)
    sec_a = lambda: (lambda k: (k, rng.choice(ajan[k])))(ak.pop())  # noqa: E731
    sec_d = lambda: (lambda k: (k, rng.choice(diger[k])))(dk.pop())  # noqa: E731
    sec_s = lambda: ("SIRA", sira.pop()) if sira else sec_d()  # noqa: E731  # SIRA'da backtick adlı cümle az → havuz bitince diğer notlar
    plan = ([("tek", [sec_a]) for _ in range(6)] + [("tek", [sec_s]) for _ in range(2)] + [("tek", [sec_d]) for _ in range(4)]
            + [("çok", [sec_a, sec_d]) for _ in range(4)] + [("çok", [sec_a, sec_s]) for _ in range(2)] + [("çok", [sec_a, sec_a]), ("çok", [sec_d, sec_d])])
    qs = []
    for i, (tur, parcalar) in enumerate(plan):
        ps = [f() for f in parcalar]
        sorular = [f"{k} kaynağında «{b}» cümlesindeki ___ {'kaç' if sayisal else 'nedir'}?" for k, (b, _, _) in ps]
        soru = sorular[0] if tur == "tek" else " ".join(f"({n}) {s}" for n, s in enumerate(sorular, 1))
        qs.append({"id": tohum * 100 + i + 1, "soru": soru, "cevap": "; ".join(c for _, (_, c, _) in ps),
                   "kaynak": "; ".join(y for _, (_, _, y) in ps), "cok": tur == "çok"})
    return qs


if __name__ == "__main__":
    yasak = kullanilmis()
    for a in sys.argv[1:]:
        t, _, tur = a.partition(":")  # "2011:ad" → sayısal olmayan tohum
        t = int(t)
        qs = uret(t, yasak, tur != "ad")
        (D / f"sorular-{t}.jsonl").write_text("\n".join(json.dumps(q, ensure_ascii=False) for q in qs) + "\n", encoding="utf-8")
        for q in qs:
            yasak |= kaynak_kume(q["kaynak"])
        print(t, len(qs), "çok", sum(q["cok"] for q in qs))
