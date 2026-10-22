import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import kurulum_durum as K


def test_instagram_reel_ret():
    assert K.karar("https://www.instagram.com/reel/DXmM2wLkf92/", "x")[0] == "ret"


def test_kaynaksiz_ret():
    assert K.karar("bulunamadı", "Animmaster Lib")[0] == "ret"


def test_web_referans_ref_ve_hesap():
    assert K.karar("https://dribbble.com", "Dribbble")[0] == "ref"
    assert K.karar("https://sketchfab.com", "Sketchfab")[0] == "hesap"


def test_blender_eklentisi_ve_bilinmeyen():
    assert K.karar("https://extensions.blender.org/add-ons/f2/", "F2")[0] == "ret"
    assert K.karar("https://example.org/x", "x")[0] == "?"
