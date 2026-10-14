import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import atlas  # noqa: E402


def r(ad, tur="skill", alan="", cc=True):
    return dict(ad=ad, tur=tur, alan=alan, cc=cc, claude_ai=False, aciklama="")


def test_oncelik_site_3d_blender():
    assert atlas.oncelik(r("blender-uretim"))
    assert atlas.oncelik(r("x", alan="3d,frontend"))
    assert not atlas.oncelik(r("dotnet-aspnetcore", alan="backend"))
    assert not atlas.oncelik(r("blender-uretim", cc=False))  # kurulu değil
    assert not atlas.oncelik(r("gsap-x", tur="ajan"))  # ajan: yalnız bl-*
    assert atlas.oncelik(r("bl-isik-kurulumu", tur="ajan", alan="3d,blender"))
    assert not atlas.oncelik(r("three.js video", tur="video-aday"))


def test_norm_birlestirir():
    assert atlas.norm("anthropic-skills:Design_DNA") == atlas.norm("design-dna") == "design-dna"
