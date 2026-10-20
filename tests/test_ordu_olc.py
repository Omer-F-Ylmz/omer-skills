"""ORDU-1 d2 kapı kümesi: her işin kabulü bilinen doğru yanıtı geçirir, bilinen yanlışı reddeder (ölçüm sapmasın)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "olcum"))
import ordu_olc as o  # noqa: E402

DOGRU = {
    "K1": str(sum(n for _, n in o.satir)), "K2": sorted(set(o.L1) | set(o.L2)), "K3": [a for a, _ in sorted(o.dos, key=lambda x: -x[1])],
    "K4": "ad\ttur\tn\n" + "\n".join(f"{x['ad']}\t{x['tur']}\t{x['n']}" for x in o.obj),
    "K5": ["t_a.py", "t_b.py", "util.py", "t_c.py", "conftest.py", "t_d.py"],
    "K6": {"docs/a/x.md": "arsiv/x.md", "docs/q.md": "arsiv/q.md", "docs/b/c/w.md": "arsiv/w.md"},
    "O1": "- Modül işi zorluk sınıfına ayırır.\n- Ücretsiz çıktı geçmezse üst kademeye çıkar.\n- İmkansiz sınıf Opus'a gider.",
    "O2": "Read the installation section, then install the dependencies and run the tests.",
    "O3": {"1": "hata-duzelt", "2": "ozellik", "3": "belge", "4": "test"}, "O4": {"karar": "Önce ücretsiz havuz denenecek", "tarih": "2026-11-03"},
    "O5": r"(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.\d{4}|\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])",
    "O6": {k: o.GUNLUK.count(k) for k in ("INFO", "WARN", "ERROR")},
    "Z1": "assert kirp('abc', 3) == 'abc'\nassert kirp('abcd', 3) == 'ab…'\nassert len(kirp('abcdef', 4)) == 4\nassert kirp('', 2) == ''",
    "Z2": "def parcala(liste, n):\n    return [liste[i:i + n] for i in range(0, len(liste), n)]\n",
    "Z3": "def fiyat(tur, adet):\n    b = {'a': 10, 'b': 25, 'c': 40}.get(tur)\n    if b is None:\n        return 0\n    t = adet * b\n    return t * 90 // 100 if adet >= 10 else t\n",
    "Z4": "B",
    "Z5": "def birlestir_aralik(a):\n    c = []\n    for s, e in sorted(a):\n        if c and s <= c[-1][1]:\n            c[-1][1] = max(c[-1][1], e)\n        else:\n            c.append([s, e])\n    return c\n",
    "Z6": "---\nname: log-ozetle\ndescription: Use when a log file must be summarized. Counts levels and lists top errors.\n---\n# Log özetle\n\n## Adımlar\n1. Dosyayı oku\n2. Seviyeleri say\n3. En sık hataları yaz\n",
    "I1": "import time\nimport threading\n\nclass Sinirli:\n    def __init__(self, sinir):\n        self.sinir = sinir\n        self.n = 0\n        self.k = threading.Lock()\n\n    def al(self):\n        with self.k:\n            if self.n < self.sinir:\n                time.sleep(0)\n                self.n += 1\n                return True\n            return False\n",
    "I2": o.GECIKME_REF.replace("def ref(", "def en_iyi_sira("),
}
YANLIS = {
    "K1": "0", "K3": [], "K4": "x", "K6": {}, "O1": "- tek satır", "O2": "Hello", "O5": r"\d+", "Z1": "assert True",
    "Z2": o.PARCA_BUG, "Z3": "def fiyat(tur, adet):\n    return 0\n", "Z4": "A", "Z5": "def birlestir_aralik(a):\n    return a\n",
    "Z6": "yok", "I1": o.SINIRLI, "I2": "def en_iyi_sira(isler):\n    return 0\n",
}


def test_her_is_dogru_yaniti_gecirir():
    assert set(DOGRU) == set(o.GOREV) and len(o.GOREV) == 20
    assert [a for a in o.GOREV if not o.dogru(a, DOGRU[a])] == []


def test_yanlis_yanit_reddedilir():
    assert [a for a, y in YANLIS.items() if o.dogru(a, y)] == []


def test_sinif_dagilimi_heldout_ile_ayni():
    from collections import Counter
    assert Counter(o.sinif_of(a) for a in o.GOREV) == Counter(e for _, e in o.ordu.HELDOUT)
