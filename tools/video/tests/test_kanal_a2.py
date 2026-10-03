"""KANAL-2a A2: B2 aynı adın tekrar karar kayıtlarını da sayar (liste tekil ad kalır)."""
from test_kanal_k1 import _jsonl
from video import kanal


def test_b2_tekrar_kayit_sayilir(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    (repo / "docs" / "kurulumlar" / "adaylar" / "foo-tool.md").write_text("video: VVVVVVVVVV1\n", encoding="utf-8")
    _jsonl(repo / "docs" / "kurulumlar" / "kayit.jsonl", [
        {"ad": "foo-tool", "karar": "UYARLA (Ömer)"}, {"ad": "foo-tool", "karar": "UYARLA (Ömer, yeniden)"},
        {"ad": "bar", "karar": "DENE", "parti": "yok-parti"}])
    sayac = {}
    _, b2 = kanal.degerli(repo, sayac)
    assert b2 == {"video": ["foo-tool"], "video-dışı": ["bar"]}
    assert sayac == {"video": 2, "video-dışı": 1}
