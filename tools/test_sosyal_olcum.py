"""sosyal_olcum kural tablosu birim testi (ağ yok). Çalıştır: python tools/test_sosyal_olcum.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sosyal_olcum as s

H = 3600
assert [s.kural_carpan(x) for x in (3, 1.2, 0.7, 0.3, 0.05)] == [1.5, 1.1, 1.0, 0.6, 0.3]
assert s.izlenme_48s([(0, 5), (10 * H, 50), (47 * H, 900), (100 * H, 5000)], 0) == 900
assert s.izlenme_48s([(0, 5), (10 * H, 50)], 0) is None  # 48. saat henüz yok


def snap(vid, v48):
    return [("m", "yt", vid, [(0, 1), (48 * H, v48)])]


olcum = [{"ts": t, "marka": "m", "plat": "yt", "takipci": 1,
          "videolar": [{"id": i, "izlenme": v[t_i]} for i, v in V.items()]}
         for t_i, t in enumerate((0, 48 * H)) for V in [{"a": [0, 100], "b": [0, 100], "c": [0, 100], "d": [0, 400], "e": [0, 10]}]]
et = {("m", "d"): {"kanca_tip": "soru"}, ("m", "e"): {"kanca_tip": "liste"}, ("m", "a"): {"kanca_tip": "soru"}}
w = s.agirlik_hesapla(olcum, et)["m"]
# medyan=100: d oran 4 -> x1.5, a oran 1 -> x1.1 ; soru = 1*1.5*1.1; e oran 0.1 -> x0.3
assert abs(w["kanca_tip:soru"] - 1.65) < 1e-9 and abs(w["kanca_tip:liste"] - 0.3) < 1e-9, w
assert s.agirlik_hesapla(olcum[:1], et) == {}  # <3 video: karar yok
print("OK")
