"""kurulum_d2.bitenler(): kalemin SON satırı karar verir; KAPI-GECTI ile biten kalem kurulmayı bekler (eski satırlar sayılmaz)."""
import csv
import importlib.util
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def _modul(tmp_path):
    sys_path = str(KOK / "tools")
    import sys
    if sys_path not in sys.path:
        sys.path.insert(0, sys_path)
    spec = importlib.util.spec_from_file_location("kurulum_d2_t", KOK / "tools/kurulum_d2.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_son_satir_karar_verir(tmp_path):
    m = _modul(tmp_path)
    p = tmp_path / "sonuc.tsv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["kalem", "sinif", "kaynak", "durum", "yol", "not", "kanit"])
        for k, d in [("a", "BULUNAMADI-2"), ("a", "KAPI-GECTI"),   # eski ret, sonra kapı: takılı (kurulmalı)
                     ("b", "KAPI-GECTI"),                          # yalnız kapı: takılı
                     ("c", "KAPI-GECTI"), ("c", "KURULDU"),        # kuruldu: bitti
                     ("d", "HATA")]:                               # hata: bitti (tur2 yeniden dener)
            w.writerow([k, "SKILL", "", d, "", "", ""])
    m.SONUC = p
    assert m.bitenler() == {"c", "d"}
