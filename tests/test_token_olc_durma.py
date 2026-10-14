"""TELVE-TOKEN-1: tools/token_olc.py --durma — önbellek durması alarmı (art arda cw=0 + büyüyen önbelleksiz girdi, ardından okuma düşüşü)."""
from test_token_olc import SIMDI, asistan, t, usage, yaz


def ist(mid, girdi=2, okuma=0, m5=0):
    return asistan(mid, usage(girdi=girdi, okuma=okuma, yazma=m5, m5=m5, h1=0), entry="sdk-cli")


def durma(tmp_path, satirlar, **kw):
    yaz(tmp_path / "p" / "s0.jsonl", satirlar)
    return t.durma(tmp_path / "p", gun=14, simdi=SIMDI, **kw)


def test_kosu_ve_kirilma(tmp_path):
    r = durma(tmp_path, [ist("a", okuma=100, m5=5000), ist("b", girdi=4000, okuma=5100), ist("c", girdi=6000, okuma=5100),
                         ist("d", girdi=9000, okuma=5100), ist("e", okuma=600, m5=14000)])
    assert r["alarm"] and len(r["kosular"]) == 1
    k = r["kosular"][0]
    assert (k["bas"], k["uzunluk"], k["onbelleksiz"], k["kirilma"]) == (2, 3, 19000, 14000)
    assert r["istek"] == 5 and r["durma_istek"] == 3


def test_kisa_kosu_ve_kucuk_girdi_alarm_degil(tmp_path):
    r = durma(tmp_path, [ist("a", m5=5000), ist("b", girdi=4000, okuma=5000), ist("c", girdi=2, okuma=5000),
                         ist("d", girdi=500, okuma=5000), ist("e", okuma=5000, m5=10)])
    assert not r["alarm"] and r["kosular"] == [] and r["durma_istek"] == 1
