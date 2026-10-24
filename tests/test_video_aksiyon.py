import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import video_aksiyon as va


def test_cizelge_pencere():
    sat = va.cizelge([{"b": 3.0, "s": 5.0, "t": "merhaba"}, {"b": 20.0, "s": 22.0, "t": "dunya"}],
                     [{"k": "0001.jpg", "t": "npm i gsap"}], {"0001.jpg": 4.0})
    assert sat[0].startswith("- [00:00] ekran: npm i gsap | söz: merhaba")
    assert sat[1].startswith("- [00:15]") and "dunya" in sat[1]


def test_github_regex():
    assert va.GH_RE.findall("bak github.com/foo/bar-baz, ve github.com/a/b.git") == ["foo/bar-baz", "a/b.git"]
