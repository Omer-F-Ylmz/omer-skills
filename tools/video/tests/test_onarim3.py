"""VİDEO-PARTİ-YT1-ONARIM-3: kalıcı erişim hatası (üyelere özel / özel / kaldırıldı / yaş) → erisilemez, yeniden denenmez; 403 kalıcı değil."""
import json

import pytest

from video import parti as pt
from video import tarama as tr

V, T = "gXhVFwzN4_4", "Tamam000001"


def _kur(tmp_path, cikti):
    pd, onb, td = tmp_path / "pd", tmp_path / "onb", tmp_path / "t"
    pd.mkdir(), td.mkdir()
    (pd / "defter.jsonl").write_text("", encoding="utf-8")
    d = {"parti": "p", "tarih": "2026-10-09", "durum": "yarim", "tavan": {"cagri": 9, "usd": 1.0}, "model": "m", "butce": 0.1,
         "videolar": {V: {"paket": {"durum": "bekliyor", "deneme": 0}, "tarama": {"durum": "bekliyor", "deneme": 0}},
                      T: {"paket": {"durum": "tamam", "deneme": 1}, "tarama": {"durum": "tamam", "deneme": 1}}}}
    cagri = []

    def alt(a):
        cagri.append(a[0])
        if a[0] == "ozet":
            print(f"{V}: {cikti}")
            return 1
        return 0
    return pd, onb, td, d, alt, cagri


@pytest.mark.parametrize("cikti,sebep", [
    ("ERROR: [youtube] x: Join this channel to get access to members-only content like this video", "üyelere özel"),
    ("ERROR: [youtube] x: This video is available to this channel's members on level: Destek", "üyelere özel"),
    ("ERROR: [youtube] x: Private video. Sign in if you've been granted access", "özel video"),
    ("ERROR: [youtube] x: Video unavailable. This video has been removed by the uploader", "kaldırılmış / yok"),
    ("ERROR: [youtube] x: Sign in to confirm your age. This video may be inappropriate", "yaş doğrulaması"),
])
def test_erisilemez_yeniden_denenmez_parti_tamam(tmp_path, cikti, sebep):
    pd, onb, td, d, alt, cagri = _kur(tmp_path, cikti)
    for _ in range(2):  # devam: ikinci koşu ozet'i yeniden çağırmaz
        assert pt._kos(pd, d, onb, td, alt, str, None, {}) == 0
    a = d["videolar"][V]["paket"]
    assert a["durum"] == "erisilemez" and a["hata"] == f"erişilemez: {sebep}"
    assert cagri == ["ozet"] and d["durum"] == "tamam"
    k = tr.kayit_oku(td / "kayit.jsonl")
    assert [(x["id"], x["not"], x["etiket"]) for x in k] == [(V, f"erişilemez: {sebep}", "erisilemez")] and "rapor" not in k[0]
    assert json.loads((pd / "durum.json").read_text(encoding="utf-8"))["durum"] == "tamam"


def test_403_kalici_degil(tmp_path):
    pd, onb, td, d, alt, _ = _kur(tmp_path, "ERROR: unable to download video data: HTTP Error 403: Forbidden")
    pt._kos(pd, d, onb, td, alt, str, None, {})
    assert d["videolar"][V]["paket"]["durum"] == "hata" and d["durum"] == "yarim" and not (td / "kayit.jsonl").exists()
