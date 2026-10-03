"""KANAL-1b (canlıda bulundu): video-tarama kaydındaki video olmayan satırlar (kaynak-*, kurulum-*) işlenmiş video sayılmaz."""
from test_kanal_k1 import _jsonl
from video import kanal


def test_video_olmayan_kayit_satiri_sayilmaz(tmp_path):
    repo = tmp_path / "repo"
    _jsonl(repo / "docs" / "video-tarama" / "kayit.jsonl", [
        {"id": "kaynak-claude-code-setup", "tarih": "2026-09-28", "rapor": "kaynak-claude-code-setup.md", "adaylar": []},
        {"id": "kurulum-3db", "tarih": "2026-10-01", "rapor": "../../bilgi/x.md", "adaylar": []},
        {"id": "lipJRiztOgM", "tarih": "2026-09-29", "rapor": "2026-09-29-lipJRiztOgM.md", "adaylar": []},
        {"id": "0ewGD79TMkM", "tarih": "2026-09-18", "adaylar": []},
    ])
    vs, _ = kanal.videolar({"kok": tmp_path / "onb"}, repo)
    assert sorted(vs) == ["0ewGD79TMkM", "lipJRiztOgM"]
