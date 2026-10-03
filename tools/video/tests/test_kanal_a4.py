"""KANAL-2a A4: shorts sekmesi olmayan kanal hata değil — 0 short, yarım sayılmaz."""
import json

from test_kanal_k2 import _onayli
from video.cli import main


def test_shorts_sekmesi_yok_hata_degil(tmp_path, monkeypatch, capsys):
    repo, env = _onayli(tmp_path, monkeypatch)

    def yt(args, timeout=None):
        if args[-1].endswith("/shorts"):
            return 1, b"", b"ERROR: [youtube:tab] UCa: This channel does not have a shorts tab"
        return 0, json.dumps({"entries": [{"id": "VIDVIDVID01", "title": "u", "duration": 900}]}).encode(), b""

    assert main(["kanal", "envanter"], env=env, kos=yt, uyku=[].append) == 0
    onb = json.loads((repo / ".kos" / "kanal" / "UCa.json").read_text(encoding="utf-8"))
    assert onb["yarim"] is False and len(onb["videolar"]) == 1
    assert "yarım" not in capsys.readouterr().out
