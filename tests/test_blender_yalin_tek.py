"""BLENDER-2 adım 2: yalin.tek — model araçsız tek yanıtta spec verir, yalin Blender'ı kendisi koşar; hata/eksikte tek düzeltme turu."""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / "tools" / "blender" / "lib"))
sys.path.insert(0, str(KOK / "tools" / "blender"))
import yalin  # noqa: E402

SPEC = '{"nesneler": [{"ad": "Kupa", "tur": "silindir"}], "ozet": ["ad", "boyut"]}'


def _kos(yanitlar, istemler):
    def kos(istem, ek):
        istemler.append((istem, ek))
        return {"metin": yanitlar.pop(0), "usage": {"input_tokens": 5, "output_tokens": 100}, "tur": 1, "usd": 0.01, "sure": 2.0}
    return kos


def test_tek_turda_spec_kosulur():
    istemler, kosulan = [], []
    o = yalin.tek("kupa yap", kos=_kos([f"```json\n{SPEC}\n```"], istemler),
                  calistir=lambda b, a, bl: kosulan.append(a) or (0, {"gecti": True, "ozet": {"Kupa": 1}}, 1))
    assert o["rc"] == 0 and o["hata"] == "" and o["tur"] == 1 and kosulan[0]["nesneler"][0]["ad"] == "Kupa"
    ek = istemler[0][1]
    assert ek[ek.index("--tools") + 1] == "" and "Write" not in ek  # araçsız: tur başına önek bir kez
    assert '"Kupa": 1' in o["metin"]


def test_hatada_tek_duzeltme_turu_ve_jeton_toplanir():
    istemler = []
    o = yalin.tek("kupa yap", kos=_kos(['{"nesneler": [{"ad": "K", "tur": "yok"}]}', SPEC], istemler),
                  calistir=lambda b, a, bl: (0, {"gecti": True}, 1))
    assert o["rc"] == 0 and o["tur"] == 2 and o["usage"]["output_tokens"] == 200
    assert "yok" in istemler[1][0]  # dogrula hatası ikinci isteme gider (Blender açılmadan)


def test_beklenen_sapmada_duzeltme_turu():
    bek = '{"nesneler": [{"ad": "Kupa", "tur": "silindir"}], "beklenen": {"Kupa": [0.08, 0.08, 0.09]}}'
    istemler, kosulan = [], []
    olcu = [[0.11, 0.08, 0.09], [0.08, 0.08, 0.09]]
    o = yalin.tek("kupa yap", kos=_kos([bek, bek], istemler),
                  calistir=lambda b, a, bl: kosulan.append(a) or (0, {"gecti": True, "ozet": [{"ad": "Kupa", "boyut": olcu.pop(0)}]}, 1))
    assert "beklenen" not in kosulan[0] and {"ad", "boyut"} <= set(kosulan[0]["ozet"])  # dogrula'dan önce çıkarılır
    assert o["rc"] == 0 and o["tur"] == 2 and "Kupa" in istemler[1][0] and "0.11" in istemler[1][0]


def test_beklenen_tutarsa_tek_tur():
    bek = '{"nesneler": [{"ad": "Kupa", "tur": "silindir"}], "beklenen": {"Kupa": [0.08, 0.08, 0.09]}}'
    o = yalin.tek("kupa yap", kos=_kos([bek], []),
                  calistir=lambda b, a, bl: (0, {"gecti": True, "ozet": [{"ad": "Kupa", "boyut": [0.085, 0.08, 0.09]}]}, 1))
    assert o["rc"] == 0 and o["tur"] == 1


def test_iki_hatada_durur():
    o = yalin.tek("kupa yap", kos=_kos([SPEC, SPEC], []), calistir=lambda b, a, bl: (1, {"gecti": False}, 1))
    assert o["rc"] == 1 and o["tur"] == 2 and "exit 1" in o["hata"]
