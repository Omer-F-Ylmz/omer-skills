"""KANAL-2b C2: `video kanal ekle <kanal-url>` → channel_id çözülür, kanallar.json'a takip (kaynak: Ömer · kanal linki); varsa değer korunur; ardından o kanal envanterlenir."""
import json

from test_kanal_k2 import _onayli
from video.cli import main

URL = "https://www.youtube.com/@Metin/videos"


def _yt(istek):
    def yt(args, timeout=None):
        istek.append(args[-1])
        if args[-1] == URL:
            return 0, json.dumps({"channel_id": "UCm", "channel": "Metin", "channel_url": "https://www.youtube.com/channel/UCm"}).encode(), b""
        if args[-1].endswith("/shorts"):
            return 1, b"", b"ERROR: This channel does not have a shorts tab"
        return 0, json.dumps({"entries": [{"id": "VIDVIDVID01", "title": "u", "duration": 900}]}).encode(), b""
    return yt


def test_kanal_ekle(tmp_path, monkeypatch):
    repo, env = _onayli(tmp_path, monkeypatch)
    istek = []
    assert main(["kanal", "ekle", URL], env=env, kos=_yt(istek), uyku=[].append) == 0
    j = json.loads((repo / "docs" / "video-tarama" / "kanallar.json").read_text(encoding="utf-8"))
    assert j["UCm"] == {"kanal": "Metin", "channel_id": "UCm", "url": "https://www.youtube.com/channel/UCm", "karar": "takip", "kaynak": "Ömer · kanal linki"}
    assert j["UCc"]["karar"] == "atla"
    assert istek == [URL, "https://www.youtube.com/channel/UCm/videos", "https://www.youtube.com/channel/UCm/shorts"]  # yalnız o kanal
    assert len(json.loads((repo / ".kos" / "kanal" / "UCm.json").read_text(encoding="utf-8"))["videolar"]) == 1


def test_kanal_ekle_varsa_deger_korunur(tmp_path, monkeypatch):
    repo, env = _onayli(tmp_path, monkeypatch)
    yol = repo / "docs" / "video-tarama" / "kanallar.json"
    j = json.loads(yol.read_text(encoding="utf-8")) | {"UCm": {"kanal": "Metin", "channel_id": "UCm", "url": "", "karar": "bir-kez"}}
    yol.write_text(json.dumps(j), encoding="utf-8")
    assert main(["kanal", "ekle", URL], env=env, kos=_yt([]), uyku=[].append) == 0
    assert json.loads(yol.read_text(encoding="utf-8"))["UCm"]["karar"] == "bir-kez"
