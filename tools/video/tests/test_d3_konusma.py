"""DERİNLİK-MASTER D3 eki (Ömer, 4 Eki O7): koruma whisper'ı durdurduğu ve altyazı da olmadığı video "konuşma alınamadı (sebep)" olarak
panel Denetim'inde sayılır ve KAÇAN? gibi `video parti kapat`ı durdurur — giderilmesi `--paket-yeniden` ile whisper."""
from video import akil as ak
from video import tarama as tr

IZ = "## Künye\nşema 2\n## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n| konuşma 01:00 | rtk | rtk | geçti |\n"
ENGEL = "altyazı yok; whisper atlandı (boş RAM 3.2 GB < 6)"


def _d(tmp_path, konusma):
    (tmp_path / "v1.md").write_text(IZ, encoding="utf-8")
    (tmp_path / "onb" / "v1").mkdir(parents=True)
    (tmp_path / "onb" / "v1" / "paket.md").write_text("## Segmentler\nyok\n", encoding="utf-8")
    v = {"tarama": {"durum": "tamam", "cikti": str(tmp_path / "v1.md")}, "konusma": konusma}
    return {"parti": "p", "tarih": "2026-10-05", "videolar": {"v1": v}, "adaylar": {}}


def test_denetim_konusma_alinamadi_sayilir(tmp_path):
    assert ak.denetim(_d(tmp_path, ENGEL), tmp_path, tmp_path / "onb")["konusma_yok"] == [("v1", ENGEL)]


def test_altyazili_ya_da_whisperli_video_sayilmaz(tmp_path):
    assert ak.denetim(_d(tmp_path, "altyazı"), tmp_path, tmp_path / "onb")["konusma_yok"] == []


def test_kapat_konusma_alinamadi_durdurur(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(tr, "denetle", lambda m: [])
    assert ak.kapat(tmp_path / "pd", _d(tmp_path, ENGEL), tmp_path, {"kok": tmp_path / "onb"}) == 1
    out = capsys.readouterr().out
    assert "konuşma alınamadı 1" in out and f"konuşma alınamadı: v1 ({ENGEL}) → --paket-yeniden" in out
