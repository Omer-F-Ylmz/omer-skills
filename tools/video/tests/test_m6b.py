"""MÜKEMMEL-6b: V10s = V10, tek fark response_format json_schema yok; şema sistem metninin sonuna metin olarak girer
(sabit önek SISTEM + EKSIKSIZLIK10 + örnek + şema). V10 isteği değişmez. Sahte çağrıcı; canlı çağrı 0."""
import json

import test_f3_v5 as v5
from test_f1 import ENV as OENV, SEMA, Omni
from test_f3_v5 import E1
from video import yonlendir as yon


def test_omni_sema_metin_response_format_yok():
    o = Omni()
    yon.omni_cagir("m", OENV, gonder=o, sema_metin=True)("SİS", "metin", SEMA)
    g = o.cagrilar[0][1]
    assert "response_format" not in g
    s = g["messages"][0]["content"]
    assert s.startswith("SİS") and s.endswith(json.dumps(SEMA, ensure_ascii=False))


def test_omni_varsayilan_degismedi():
    o = Omni()
    y = yon.omni_cagir("m", OENV, gonder=o)("SİS", "metin", SEMA)
    g = o.cagrilar[0][1]
    assert g["response_format"]["json_schema"]["schema"] == SEMA and g["messages"][0]["content"] == "SİS" and y["form"] == {"a": "b"}


def test_eleme_v10s_sema_metin_v10_degismedi(tmp_path):
    gor = {}

    def kur(c):
        def b_kur(m, env, **kw):
            gor.setdefault(len(gor), kw)
            kw.pop("sema_metin", None)
            return v5._b6(c)(m, env, **kw)
        return b_kur

    c10, c10s = [], []
    for ad, v, c in (("a", "V10", c10), ("b", "V10s", c10s)):
        (tmp_path / ad).mkdir()
        v5._e6(tmp_path / ad, [f"{E1}@{v}"], c, b_kur=kur(c))
    assert "sema_metin" not in gor[0] and gor[1].get("sema_metin") is True
    assert c10s == c10  # aynı parça/son geçiş sistemleri, metinler, kareler (şema eklemesi omni_cagir içinde)
    assert v5._kayit(tmp_path / "b", f"{E1}@V10s")["form"] == v5._kayit(tmp_path / "a", f"{E1}@V10")["form"]
