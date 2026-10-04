"""DERİNLİK-MASTER C1: konuşma kaynağı — temiz altyazı → altyazı; bozuk/yok → whisper (süre sınırsız, korumalı, parçalı, sürdürülür)."""
import json
import sys
import types
from pathlib import Path

import pytest

from video import parti as pt
from video.cli import main
from test_video import VID, Kos, meta, ortam, segmentler  # noqa: F401 (ortam fixture)


def _seg(d, *metinler):
    d.mkdir(parents=True, exist_ok=True)
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps({"bas": i * 5, "son": i * 5 + 5, "metin": t})
                                                  for i, t in enumerate(metinler)), encoding="utf-8")


def _alt(cagri, yaz=None):
    def alt(a):
        cagri.append(a)
        if a[0] == "whisper" and yaz:
            _seg(Path(yaz), "whisper metni")
        return 0
    return alt


@pytest.fixture
def kurulu(monkeypatch):
    monkeypatch.setattr(pt, "find_spec", lambda n: True)
    monkeypatch.setattr(pt, "_whisper_engel", lambda: None)


TEMIZ = ("bu araç landing sayfası kuruyor", "kurulum için npx komutunu çalıştırıyoruz", "sonra ayarları açıyoruz")
BOZUK = ("xkcdq brrrr zzzt", "a1b2 qwrtp mmmm", "the the the the")


def test_c1_temiz_altyazi_whisper_yok(tmp_path, kurulu):
    _seg(tmp_path / "v", *TEMIZ)
    cagri = []
    assert pt._konusma(tmp_path / "v", {"duration": 7200}, _alt(cagri)) == "altyazı"
    assert cagri == [] and pt._bozuk_oran(tmp_path / "v" / "segmentler.jsonl") <= pt.BOZUK_ESIK


def test_c1_bozuk_altyazi_whisper_suresiz(tmp_path, kurulu):
    d = tmp_path / "v"
    _seg(d, *BOZUK)
    assert pt._bozuk_oran(d / "segmentler.jsonl") > pt.BOZUK_ESIK
    cagri = []
    e = pt._konusma(d, {"duration": 7200}, _alt(cagri, d))
    assert cagri == [["whisper", "--en-fazla-dk", "0", "--", "v"]]  # 2 saat: ≤5 dk sınırı yok
    assert e.startswith("whisper (altyazı bozuk") and "tahmini" in e and "gerçek" in e
    assert (d / "segmentler.altyazi.jsonl").is_file() and "whisper metni" in (d / "segmentler.jsonl").read_text(encoding="utf-8")


def test_c1_bozuk_whisper_olmazsa_altyazi_geri(tmp_path, kurulu):
    d = tmp_path / "v"
    _seg(d, *BOZUK)
    e = pt._konusma(d, {"duration": 60}, lambda a: (_ for _ in ()).throw(RuntimeError("model yok")))
    assert "bozuk" in e and (d / "segmentler.jsonl").is_file() and not (d / "segmentler.altyazi.jsonl").exists()


def test_c1_altyazi_yok_whisper(tmp_path, kurulu):
    (tmp_path / "v").mkdir()
    cagri = []
    e = pt._konusma(tmp_path / "v", {"duration": 3600}, _alt(cagri, tmp_path / "v"))
    assert cagri[0][0] == "whisper" and e.startswith("whisper (altyazı yok)") and "tahmini" in e


def test_c1_kurulu_degil_ve_koruma(tmp_path, monkeypatch):
    (tmp_path / "v").mkdir()
    cagri = []
    monkeypatch.setattr(pt, "find_spec", lambda n: None)
    assert pt._konusma(tmp_path / "v", {"duration": 60}, _alt(cagri)) == "altyazı yok; whisper kurulu değil"
    monkeypatch.setattr(pt, "find_spec", lambda n: True)
    monkeypatch.setattr(pt, "_bos_ram_gb", lambda: 3.2)
    monkeypatch.setattr(pt, "_surecler", lambda: "")
    assert pt._konusma(tmp_path / "v", {"duration": 60}, _alt(cagri)) == "altyazı yok; whisper atlandı (boş RAM 3.2 GB < 6)"
    monkeypatch.setattr(pt, "_bos_ram_gb", lambda: 16.0)
    for sur, ad in (("blender.exe blender.exe --background", "blender"), ("python.exe python -m pytest tests", "pytest"),
                    ("GenshinImpact.exe", "genshin")):
        monkeypatch.setattr(pt, "_surecler", lambda: sur)
        assert pt._whisper_engel().lower() == f"ağır süreç: {ad}"
    monkeypatch.setattr(pt, "_surecler", lambda: "explorer.exe\ncode.exe")
    assert pt._whisper_engel() is None and cagri == []


def test_c1_kapsamda_konusma(tmp_path):
    from test_m2a import V
    from video import akil as ak
    a = {"ad": "x", "tur": "skill", "repo": None, "kurulu": None, "durum": "tamam", "adlar": ["x"], "videolar": {V[0]: {}}}
    d = {"videolar": {V[0]: {"konusma": "whisper (altyazı yok) · tahmini 3 dk · gerçek 2 dk"}}}
    assert "konuşma whisper (altyazı yok)" in ak._kapsam("x", a, {}, "", "koşmadı: x", d)[0]
    assert "konuşma" not in ak._kapsam("x", a, {}, "", "koşmadı: x", {})[0]


def test_c1_whisper_parcali_suresiz_surdurulur(ortam, monkeypatch):
    d = Path(ortam["VIDEO_CACHE"]) / VID
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps(meta(duration=3000, subtitles={})), encoding="utf-8")
    klip, patla = [], [True]

    class Model:
        def __init__(self, *a, **k):
            pass

        def transcribe(self, yol, clip_timestamps=None, **k):
            klip.append(clip_timestamps)
            if clip_timestamps[0] == 1200 and patla.pop():
                raise RuntimeError("kesildi")
            return iter([types.SimpleNamespace(start=clip_timestamps[0] + 1.0, end=clip_timestamps[0] + 5.0, text=f" parça {clip_timestamps[0]}")]), None

    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=Model))
    kos = Kos()
    with pytest.raises(RuntimeError):
        main(["--whisper", VID, "--en-fazla-dk", "0"], env=ortam, kos=kos)
    yt = [a for a in kos.cagri if a[0] == "yt-dlp"]
    assert len(yt) == 1 and "--download-sections" not in yt[0]  # süre sınırı yok: tam ses
    assert list(d.glob("ses.*")) and json.loads((d / "whisper.json").read_text(encoding="utf-8"))["parca"]
    assert main(["--whisper", VID, "--en-fazla-dk", "0"], env=ortam, kos=kos) == 0
    assert len([a for a in kos.cagri if a[0] == "yt-dlp"]) == 1  # sürdürme: ses yeniden inmez
    assert klip == [[0, 1200], [1200, 2400], [1200, 2400], [2400, 3000]]
    assert [s for s in " ".join(x["metin"] for x in segmentler(d)).split() if s != "parça"] == ["0", "1200", "2400"]
    assert not list(d.glob("ses*")) and not (d / "whisper.json").exists()
