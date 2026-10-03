"""KANAL-2b C3: yalnız short yayınlayan kanalın videos sekmesi yok — hata değil; shorts toplanır, yarım sayılmaz."""
import json

from test_kanal_k2 import _onayli
from video.cli import main


def test_videos_sekmesi_yok_hata_degil(tmp_path, monkeypatch, capsys):
    repo, env = _onayli(tmp_path, monkeypatch)

    def yt(args, timeout=None):
        if args[-1].endswith("/videos"):
            return 1, b"", b"ERROR: [youtube:tab] UCa: This channel does not have a videos tab"
        return 0, json.dumps({"entries": [{"id": "SHORTSHORT1", "title": "s", "duration": 40}]}).encode(), b""

    assert main(["kanal", "envanter"], env=env, kos=yt, uyku=[].append) == 0
    onb = json.loads((repo / ".kos" / "kanal" / "UCa.json").read_text(encoding="utf-8"))
    assert onb["yarim"] is False and onb["videolar"]["SHORTSHORT1"]["tur"] == "short"
    assert "yarım" not in capsys.readouterr().out
