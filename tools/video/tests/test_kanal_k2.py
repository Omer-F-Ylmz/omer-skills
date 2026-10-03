"""KANAL-1 K2: envanter — istekler arası bekleme · 429/403 yeniden deneme · önbellek · kimlik yok (sahte yt-dlp)."""
import json

from video import kanal
from video.cli import main


def _onayli(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    monkeypatch.setattr(kanal, "KOK", repo)
    (repo / "docs" / "video-tarama").mkdir(parents=True)
    (repo / "docs" / "video-tarama" / "kanallar.json").write_text(json.dumps({
        "UCa": {"kanal": "A Kanal", "channel_id": "UCa", "url": "", "karar": "takip"},
        "B Kanal": {"kanal": "B Kanal", "channel_id": "", "url": "", "karar": "bir-kez"},
        "UCc": {"kanal": "C Kanal", "channel_id": "UCc", "url": "", "karar": "atla"},
    }), encoding="utf-8")
    return repo, {"VIDEO_CACHE": str(tmp_path / "onb")}


class Yt:
    """Sahte yt-dlp: sekme → entries; hata verilirse her çağrıda döner."""

    def __init__(self, videos, shorts=(), hata=None):
        self.sekme, self.hata, self.cagri = {"videos": list(videos), "shorts": list(shorts)}, hata, []

    def __call__(self, args, timeout=None):
        self.cagri.append(args)
        if self.hata:
            return 1, b"", self.hata.encode()
        return 0, json.dumps({"entries": self.sekme[args[-1].rsplit("/", 1)[1]]}).encode(), b""


def test_envanter_bekleme_onbellek_kimlik_yok(tmp_path, monkeypatch, capsys):
    repo, env = _onayli(tmp_path, monkeypatch)
    uyku = []
    yt = Yt([{"id": "-tireliVID01", "title": "Uzun", "duration": 900, "upload_date": "20260901"},
             {"id": "VIDVIDVID02", "title": "Tarihsiz", "duration": 600}],
            [{"id": "SHORTSHORT1", "title": "Kısa", "duration": 40, "timestamp": 1788220800}])
    assert main(["kanal", "envanter"], env=env, kos=yt, uyku=uyku.append) == 0
    assert len(yt.cagri) == 2 and all("--flat-playlist" in a and "--skip-download" in a for a in yt.cagri)
    assert [a[-1] for a in yt.cagri] == ["https://www.youtube.com/channel/UCa/videos", "https://www.youtube.com/channel/UCa/shorts"]
    assert uyku and min(uyku) >= 2  # aynı kanalda istekler arası bekleme
    assert "kimlik yok: B Kanal" in capsys.readouterr().out
    j = json.loads((repo / ".kos" / "kanal" / "UCa.json").read_text(encoding="utf-8"))
    v = j["videolar"]
    assert v["-tireliVID01"] == {"baslik": "Uzun", "sure": 900, "tarih": "2026-09-01", "tur": "uzun", "url": "https://www.youtube.com/watch?v=-tireliVID01"}
    assert v["VIDVIDVID02"]["tarih"] == "tarih yok"
    assert v["SHORTSHORT1"]["tur"] == "short" and v["SHORTSHORT1"]["tarih"] == "2026-09-01"
    assert j["yarim"] is False
    yt2 = Yt(yt.sekme["videos"] + [{"id": "YENIYENI003", "title": "Yeni", "duration": 700}], yt.sekme["shorts"])
    assert main(["kanal", "envanter", "--kanal", "UCa"], env=env, kos=yt2, uyku=uyku.append) == 0
    assert "yeni 1" in capsys.readouterr().out
    assert len(json.loads((repo / ".kos" / "kanal" / "UCa.json").read_text(encoding="utf-8"))["videolar"]) == 4


def test_envanter_429_iki_yeniden_deneme_sonra_yarim(tmp_path, monkeypatch, capsys):
    repo, env = _onayli(tmp_path, monkeypatch)
    uyku = []
    yt = Yt([], hata="ERROR: HTTP Error 429: Too Many Requests")
    assert main(["kanal", "envanter", "--kanal", "UCa"], env=env, kos=yt, uyku=uyku.append) == 0
    assert len(yt.cagri) == 3 and len(uyku) == 2  # 1 + 2 yeniden deneme; shorts sekmesine geçilmez
    assert json.loads((repo / ".kos" / "kanal" / "UCa.json").read_text(encoding="utf-8"))["yarim"] is True
    assert "yarım" in capsys.readouterr().out


def test_envanter_onaysiz_kosmaz(tmp_path, monkeypatch):
    monkeypatch.setattr(kanal, "KOK", tmp_path / "repo")
    yt = Yt([])
    assert main(["kanal", "envanter"], env={"VIDEO_CACHE": str(tmp_path)}, kos=yt, uyku=lambda s: None) == 1
    assert yt.cagri == []
