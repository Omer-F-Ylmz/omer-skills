"""KANAL-1b B3: kanal coz — '?' videolar + kimliksiz kanal başına 1 video; bekleme · 3 ardışık hata dur · klasör açılmaz · önbellek."""
import json

from video import kanal
from video.cli import main

A1, A2, D1, D2, D3 = "AAAAAAAAAA1", "AAAAAAAAAA2", "DDDDDDDDDD1", "DDDDDDDDDD2", "DDDDDDDDDD3"


def _kur(tmp_path, monkeypatch):
    repo, onb = tmp_path / "repo", tmp_path / "onb"
    monkeypatch.setattr(kanal, "KOK", repo)
    rd = repo / "docs" / "video-tarama"
    rd.mkdir(parents=True)
    for v in (A1, A2, D1, D2, D3):
        (rd / f"2026-09-30-{v}.md").write_text("# x\n## İddialar\n", encoding="utf-8")
    for v in (A1, A2):
        (onb / v).mkdir(parents=True)
        (onb / v / "meta.json").write_text(json.dumps({"id": v, "channel": "A Kanal", "title": "t"}), encoding="utf-8")
    return repo, onb, {"VIDEO_CACHE": str(onb)}


class Yt:
    def __init__(self, hata=None):
        self.cagri, self.hata = [], hata

    def __call__(self, args, timeout=None):
        self.cagri.append(args)
        if self.hata:
            return 1, b"", self.hata.encode()
        v = args[-1].rsplit("=", 1)[1]
        c = "UCa" if v.startswith("A") else "UCd"
        return 0, json.dumps({"id": v, "channel": "A Kanal" if c == "UCa" else "D Kanal", "channel_id": c,
                              "channel_url": f"https://www.youtube.com/channel/{c}"}).encode(), b""


def test_coz_bekleme_klasor_acilmaz_onbellek(tmp_path, monkeypatch):
    repo, onb, env = _kur(tmp_path, monkeypatch)
    uyku, yt = [], Yt()
    assert main(["kanal", "coz"], env=env, kos=yt, uyku=uyku.append) == 0
    assert len(yt.cagri) == 4 and all("-J" in a and "--skip-download" in a for a in yt.cagri)  # A Kanal'dan 1 + 3 '?' video
    assert len(uyku) == 3 and min(uyku) >= 2
    m = [json.loads((onb / v / "meta.json").read_text(encoding="utf-8")) for v in (A1, A2)]
    assert sum(x.get("channel_id") == "UCa" for x in m) == 1 and all(x["title"] == "t" for x in m)
    assert not any((onb / v).exists() for v in (D1, D2, D3))
    vk = json.loads((repo / ".kos" / "kanal" / "video-kanal.json").read_text(encoding="utf-8"))
    assert vk[D1] == {"channel": "D Kanal", "channel_id": "UCd", "channel_url": "https://www.youtube.com/channel/UCd"}
    yt2 = Yt()
    assert main(["kanal", "coz"], env=env, kos=yt2, uyku=uyku.append) == 0 and yt2.cagri == []
    assert main(["kanal", "liste"], env=env) == 0
    md = (repo / "docs" / "video-tarama" / "kanallar.md").read_text(encoding="utf-8")
    assert "| A Kanal | UCa | https://www.youtube.com/channel/UCa | 2 |" in md and "| D Kanal | UCd |" in md and "| ? |" not in md


def test_coz_uc_ardisik_hata_durur(tmp_path, monkeypatch, capsys):
    repo, onb, env = _kur(tmp_path, monkeypatch)
    yt = Yt(hata="ERROR: HTTP Error 500")
    assert main(["kanal", "coz"], env=env, kos=yt, uyku=lambda s: None) == 0
    assert len(yt.cagri) == 3
    assert "çözülemedi 4" in capsys.readouterr().out
