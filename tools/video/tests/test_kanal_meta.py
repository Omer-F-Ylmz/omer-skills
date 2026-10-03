"""KANAL-1: meta.json channel_id/channel_url mevcut `yt-dlp -J` çıktısından; ek istek yok."""
import json

from video import cli


def test_meta_kanal_kimligi_tek_istek(tmp_path):
    cagri = []

    def kos(args, timeout=None):
        cagri.append(args)
        return 0, json.dumps({"id": "AAAAAAAAAA1", "channel": "A", "channel_id": "UCa", "channel_url": "https://www.youtube.com/channel/UCa"}).encode(), b""

    d = tmp_path / "AAAAAAAAAA1"
    d.mkdir()
    m = cli._meta({"kos": kos, "uyku": lambda s: None}, d)
    assert len(cagri) == 1
    assert (m["channel_id"], m["channel_url"]) == ("UCa", "https://www.youtube.com/channel/UCa")
    assert json.loads((d / "meta.json").read_text(encoding="utf-8"))["channel_id"] == "UCa"
