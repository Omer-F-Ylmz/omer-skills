import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import wer_altin as w


def test_norm_turkce_harf_ve_sayi():
    assert w.norm("İstanbul ILIK, 5 kişi!") == "istanbul ılık beş kişi"


def test_norm_buyuk_sayi_degismez():
    assert w.norm("120 video") == "120 video"
