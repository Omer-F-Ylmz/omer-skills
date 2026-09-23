"""12a video-izle: ağsız birim testler. Dış süreçler sahte `kos`, Jev sahte `gonder` ile."""
import json
import struct
import sys
import threading
import time
import types
from pathlib import Path

import pytest

from jev import cekirdek as c
from video import metin as m
from video.cli import main

VID = "yp7gg8cG5wc"

VTT_OTO = """WEBVTT
Kind: captions
Language: en

00:00:00.000 --> 00:00:02.000 align:start position:0%

hello<00:00:00.500><c> world</c>

00:00:02.000 --> 00:00:02.010 align:start position:0%
hello world


00:00:02.010 --> 00:00:04.000 align:start position:0%
hello world
this<00:00:02.500><c> is</c><00:00:03.000><c> fine</c>

00:00:04.000 --> 00:00:06.000
<v Konuşan>tom &amp; jerry</v>
"""


def akis_url(expire=None):
    return f"https://rr1.googlevideo.com/videoplayback?expire={expire or int(time.time()) + 6 * 3600}&sig=GIZLI123&itag=136"


def jpeg(g=768, y=432):
    return b"\xff\xd8\xff\xe0\x00\x04ab" + b"\xff\xc0" + struct.pack(">HBHH", 11, 8, y, g) + b"\x03\x01\x22\x00" + b"\xff\xd9"


def meta(**k):
    d = {"id": VID, "title": "Deneme videosu", "channel": "Kanal", "duration": 300,
         "chapters": [{"start_time": 0, "end_time": 100, "title": "Giriş"}, {"start_time": 100, "end_time": 300, "title": "Asıl"}],
         "description": "Bak https://a.com/x ve (https://b.io/y).", "subtitles": {"en": [{"ext": "vtt"}]}, "automatic_captions": {}}
    d.update(k)
    return d


class Kos:
    """Sahte yt-dlp/ffmpeg. Çağrıları kaydeder; istenen dosyaları yazar."""

    def __init__(self, meta_=None, liste=0, ham=None, bekle=0.0, url=None, ag_hata=False):
        self.meta, self.liste, self.ham, self.bekle = meta_ or meta(), liste, ham or (lambda yol: bytes(range(64))), bekle
        self.url, self.ag_hata = url or akis_url(), ag_hata
        self.cagri, self.anlik, self.tepe, self.kilit = [], 0, 0, threading.Lock()

    def __call__(self, args, timeout=None):
        self.cagri.append(list(args))
        if args[0] == "yt-dlp":
            if "-g" in args:
                return 0, (self.url + "\n").encode(), b""
            if "--flat-playlist" in args:
                return 0, json.dumps({"entries": [{"id": f"v{i:010d}"} for i in range(self.liste)]}).encode(), b""
            if "-J" in args:
                return 0, json.dumps({**self.meta, "id": args[-1]}).encode(), b""
            o = args[args.index("-o") + 1]
            if "--write-subs" in args or "--write-auto-subs" in args:
                with self.kilit:
                    self.anlik += 1
                    self.tepe = max(self.tepe, self.anlik)
                time.sleep(self.bekle)
                with self.kilit:
                    self.anlik -= 1
                dil = args[args.index("--sub-langs") + 1]
                open(o.replace("%(ext)s", f"{dil}.vtt"), "w", encoding="utf-8").write(VTT_OTO)
                return 0, b"", b""
            open(o.replace("%(ext)s", "mp4"), "wb").write(b"video")
            return 0, b"", b""
        if args[0] == "ffmpeg":
            if "rawvideo" in args:
                return 0, self.ham(args[args.index("-i") + 1]), b""
            if self.ag_hata and self.url in args:
                return 1, b"", f"[https @ 0x1] {self.url}: Server returned 403 Forbidden".encode()
            cikti = args[-1]
            for yol in ([cikti % 1, cikti % 2] if "%d" in cikti else [cikti]):
                open(yol, "wb").write(jpeg())
            return 0, b"", b""
        raise AssertionError(args)


def yanit(cevap):
    return 200, {}, json.dumps({"answers": cevap}).encode()


class Jev:
    """Sahte TypeSafe: state'teki işaretlere göre p döner."""

    def __init__(self, goruntu=0.97):
        self.istek, self.goruntu = [], goruntu

    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        s, q = g["state"], g["questions"]
        if "arac" in q or "ekran" in q:
            pa = 0.95 if "ARAC" in s else 0.02 if "BOS" in s else 0.3
            p = {"arac": pa, "ekran": 0.9 if "EKRAN" in s else 0.1}
            return yanit({k: {"type": "noul", "noul": p[k]} for k in q})
        if "goruntu" in q:
            cv = {k: {"type": "choice", "choice": "s2", "probabilities": {"s2": 0.5, "s4": 0.3, "s1": 0.15, "hiçbiri": 0.05}}
                  for k in q if k != "goruntu"}
            return yanit({**cv, "goruntu": {"type": "noul", "noul": self.goruntu}})
        return yanit({k: {"type": "noul", "noul": p} for k, p in zip(q, [0.9, 0.7, 0.2])})


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    monkeypatch.setattr(c, "BANT_YOLU", tmp_path / "yok.json")
    return {"VIDEO_CACHE": str(tmp_path / "onbellek"), "TYPESAFE_API_KEY": "sahte"}


def onbellek(ortam, metinler, **ek):
    from pathlib import Path
    d = Path(ortam["VIDEO_CACHE"]) / VID
    d.mkdir(parents=True, exist_ok=True)
    (d / "meta.json").write_text(json.dumps(meta(**ek)), encoding="utf-8")
    satir = [{"i": i, "bas": i * 60, "son": i * 60 + 60, "metin": t} for i, t in enumerate(metinler)]
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in satir), encoding="utf-8")
    return d


def segmentler(d):
    return [json.loads(x) for x in (d / "segmentler.jsonl").read_text(encoding="utf-8").splitlines()]


# --- saf işlevler ---

def test_vtt_kayan_satir_tekrarsiz_zamanlar_korunur():
    assert m.vtt_ayristir(VTT_OTO) == [(0.0, "hello world"), (2.01, "this is fine"), (4.0, "tom & jerry")]


def test_segmentler_chapter_hizali():
    satirlar = [(t, f"satır {t}") for t in range(0, 300, 10)]
    seg = m.segmentle(satirlar, meta()["chapters"], 300)
    assert [s["i"] for s in seg] == list(range(len(seg)))
    assert 100 in [s["bas"] for s in seg]
    assert all(not (s["bas"] < 100 < s["son"]) for s in seg)
    assert all(s["son"] - s["bas"] <= 60 for s in seg)
    assert seg[0]["metin"].startswith("satır 0") and seg[-1]["son"] == 300


def test_dil_oncelik_sirasi():
    assert m.dil_sec({"subtitles": {"en": [1]}, "automatic_captions": {"tr": [1], "en": [1]}}) == ("en", "elle")
    assert m.dil_sec({"subtitles": {}, "automatic_captions": {"en-orig": [1], "tr": [1]}}) == ("tr", "oto")
    assert m.dil_sec({"subtitles": {"tr-TR": [1], "en": [1]}}) == ("tr-TR", "elle")
    assert m.dil_sec({"subtitles": {"en": [1]}, "automatic_captions": {"de": [1]}}, "de") == ("en", "elle")
    assert m.dil_sec({"subtitles": {"live_chat": [1]}, "automatic_captions": {}}) is None


def test_aciklamadan_url():
    assert m.urller("Bak https://a.com/x, (https://b.io/y) ve https://a.com/x.") == ["https://a.com/x", "https://b.io/y"]


def test_id_cozumu():
    for s in (VID, f"https://www.youtube.com/watch?v={VID}&t=3", f"https://youtu.be/{VID}"):
        assert m.vid(s) == VID
    assert m.vid("https://www.youtube.com/playlist?list=PLabc") is None


# --- ozet ---

def test_ozet_cikti_kompakt_ve_onbellekte_ag_yok(ortam, capsys):
    kos = Kos()
    assert main(["ozet", VID], env=ortam, kos=kos) == 0
    out = capsys.readouterr().out
    assert len(out.strip().splitlines()) <= 6 and "Deneme videosu" in out and "hello world" not in out
    ilk = len(kos.cagri)
    assert main(["ozet", VID], env=ortam, kos=kos) == 0
    assert len(kos.cagri) == ilk  # önbellek: ağ yok
    from pathlib import Path
    d = Path(ortam["VIDEO_CACHE"]) / VID
    assert json.loads((d / "linkler.json").read_text(encoding="utf-8")) == ["https://a.com/x", "https://b.io/y"]
    assert segmentler(d)[0]["metin"].startswith("hello world")


def test_playlist_tavan_8_ve_altyazi_eszamanli_en_fazla_4(ortam, capsys):
    kos = Kos(liste=11, bekle=0.05)
    assert main(["ozet", "https://www.youtube.com/playlist?list=PLabc"], env=ortam, kos=kos) == 0
    out = capsys.readouterr().out
    assert sum("--write-subs" in a for a in kos.cagri) == 8 and "3" in out.splitlines()[-1]
    assert 1 < kos.tepe <= 4


def test_altyazi_yoksa_exit_3(ortam, capsys):
    assert main(["ozet", VID], env=ortam, kos=Kos(meta(subtitles={}, automatic_captions={}))) == 3
    assert "--whisper" in capsys.readouterr().out


# --- suz ---

def test_suz_yalniz_kesin_hayir_atlanir_onbellekte_ag_yok(ortam, capsys):
    d = onbellek(ortam, ["ARAC EKRAN", "BOS", "BELIRSIZ", "ARAC"])
    jev = Jev()
    assert main(["suz", VID], env=ortam, gonder=jev) == 0
    seg = segmentler(d)
    assert [s["atla"] for s in seg] == [False, True, False, False]
    assert seg[0]["p_ekran"] == 0.9 and len(jev.istek) == 4
    assert "okunacak 3" in capsys.readouterr().out
    assert main(["suz", VID], env=ortam, gonder=jev) == 0
    assert len(jev.istek) == 4


def test_suz_istek_tavani_aga_cikmadan(ortam):
    onbellek(ortam, ["ARAC"] * 5)
    jev = Jev()
    assert main(["suz", VID, "--istek-tavan", "3"], env=ortam, gonder=jev) == 1
    assert jev.istek == []


# --- sor ---

def test_sor_tam_2_istek_ve_token_siniri(ortam, capsys):
    onbellek(ortam, [f"segment {i} " + "kelime " * 700 for i in range(6)])
    jev = Jev()
    assert main(["sor", VID, "hangi araç anlatılıyor?"], env=ortam, gonder=jev) == 0
    out = capsys.readouterr().out
    assert len(jev.istek) == 2 and c.token(out) <= 2700
    assert out.strip().splitlines()[-1].startswith("video kare")


# --- kare ---

def kare_kur(ortam, p_ekran):
    d = onbellek(ortam, [f"s{i}" for i in range(len(p_ekran))])
    seg = segmentler(d)
    for s, p in zip(seg, p_ekran):
        s.update(p_arac=0.9, p_ekran=p, atla=False)
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps(s) for s in seg), encoding="utf-8")
    return d


def ayri(yol):
    return bytes((hash(yol) >> i) & 0xFF for i in range(64))


def ag(kos):
    """Akış URL'sini girdi alan ffmpeg çağrıları."""
    return [a for a in kos.cagri if a[0] == "ffmpeg" and kos.url in a]


def test_kare_akis_url_giris_atlamali_video_yazilmaz(ortam, capsys):
    d = kare_kur(ortam, [0.1] * 5)
    kos = Kos(ham=ayri)
    assert main(["kare", VID, "--t", "1:00,2:00", "--genislik", "1200"], env=ortam, kos=kos) == 0
    yt = [a for a in kos.cagri if a[0] == "yt-dlp"]
    assert len(yt) == 1 and "-g" in yt[0] and yt[0][yt[0].index("-f") + 1] == "bv*[height<=720][vcodec!=none]/b"
    net = ag(kos)
    assert len(net) == 4  # zaman başına: tam-t karesi + pencere sahne kareleri
    for a in net:
        assert a.index("-ss") < a.index("-i") and a.index("-rw_timeout") < a.index("-i")  # giriş-atlaması: yalnız pencere okunur
        vf = a[a.index("-vf") + 1]
        assert "min(768,iw)" in vf and "format=yuvj420p" in vf
    pen = [a for a in net if "-t" in a]
    assert all("gt(scene,0.3)" in a[a.index("-vf") + 1] for a in pen)
    assert [(a[a.index("-ss") + 1], a[a.index("-t") + 1]) for a in pen] == [("52", "16"), ("112", "16")]
    assert {p.name for p in d.iterdir()} <= {"meta.json", "segmentler.jsonl", "kareler", "akis.url"}
    assert "tahmini" in capsys.readouterr().out


def test_kare_pencere_0_tek_kare(ortam):
    kare_kur(ortam, [0.1] * 5)
    kos = Kos(ham=ayri)
    assert main(["kare", VID, "--t", "2:30", "--pencere", "0"], env=ortam, kos=kos) == 0
    (a,) = ag(kos)
    assert a.index("-ss") < a.index("-i") and a[a.index("-ss") + 1] == "150"
    assert a[a.index("-frames:v") + 1] == "1" and "-t" not in a and "select" not in a[a.index("-vf") + 1]
    assert "format=yuvj420p" in a[a.index("-vf") + 1]


def test_kare_hicbir_ytdlp_cagrisi_video_indirmez(ortam):
    kare_kur(ortam, [0.1, 0.9, 0.2, 0.8, 0.95])
    kos = Kos(ham=ayri)
    assert main(["kare", VID, "--suzgecten", "--t", "1:00", "--en-fazla", "3"], env=ortam, kos=kos) == 0
    for a in (a for a in kos.cagri if a[0] == "yt-dlp"):
        assert "-g" in a and not {"-o", "--download-sections", "--output", "-x"} & set(a)


def test_kare_akis_url_onbellek_ve_sure(ortam):
    kare_kur(ortam, [0.1] * 5)
    gecerli = Kos(ham=ayri)
    assert main(["kare", VID, "--t", "1:00"], env=ortam, kos=gecerli) == 0
    ikinci = Kos(ham=ayri, url=gecerli.url)
    assert main(["kare", VID, "--t", "2:00"], env=ortam, kos=ikinci) == 0
    assert not [a for a in ikinci.cagri if a[0] == "yt-dlp"]  # geçerli URL önbellekten
    eski = Kos(ham=ayri, url=akis_url(int(time.time()) - 60))
    (Path(ortam["VIDEO_CACHE"]) / VID / "akis.url").write_text(eski.url, encoding="utf-8")
    assert main(["kare", VID, "--t", "1:00"], env=ortam, kos=eski) == 0
    assert len([a for a in eski.cagri if a[0] == "yt-dlp" and "-g" in a]) == 1  # süresi geçmiş → yeniden alınır


def test_kare_url_ciktida_yok(ortam, capsys):
    kare_kur(ortam, [0.1] * 5)
    assert main(["kare", VID, "--t", "1:00"], env=ortam, kos=Kos(ham=ayri)) == 0
    assert main(["kare", VID, "--t", "2:00"], env=ortam, kos=Kos(ham=ayri, ag_hata=True)) == 1
    cikti = capsys.readouterr()
    assert "403" in cikti.out
    assert "GIZLI123" not in cikti.out + cikti.err and "googlevideo" not in cikti.out + cikti.err


def test_kare_suzgecten_en_yuksek_ekran(ortam):
    kare_kur(ortam, [0.1, 0.9, 0.2, 0.8, 0.95])
    kos = Kos(ham=ayri)
    assert main(["kare", VID, "--suzgecten", "--en-fazla", "2"], env=ortam, kos=kos) == 0
    assert sorted(float(a[a.index("-ss") + 1]) for a in ag(kos) if "-t" in a) == [82, 262]
    assert sorted(float(a[a.index("-ss") + 1]) for a in ag(kos) if "-t" not in a) == [90, 270]  # K6: tam-t kareleri


def test_kare_en_fazla(ortam, capsys):
    d = kare_kur(ortam, [0.1] * 5)
    assert main(["kare", VID, "--t", "1:00,2:00,3:00", "--en-fazla", "2"], env=ortam, kos=Kos(ham=ayri)) == 0
    assert len(list((d / "kareler").glob("*.jpg"))) == 2


def test_kare_tekrar_ayiklanir(ortam):
    d = kare_kur(ortam, [0.1] * 5)
    assert main(["kare", VID, "--t", "1:00"], env=ortam, kos=Kos(ham=lambda yol: bytes(64))) == 0
    assert len(list((d / "kareler").glob("*.jpg"))) == 1


# --- whisper ---

def test_whisper_dakika_tavani(ortam, monkeypatch, capsys):
    from pathlib import Path
    d = Path(ortam["VIDEO_CACHE"]) / VID
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps(meta(duration=3600, subtitles={})), encoding="utf-8")

    class Model:
        def __init__(self, *a, **k):
            pass

        def transcribe(self, yol, **k):
            return iter([types.SimpleNamespace(start=0.0, end=5.0, text=" merhaba")]), None

    monkeypatch.setitem(sys.modules, "faster_whisper", types.SimpleNamespace(WhisperModel=Model))
    kos = Kos()
    assert main(["--whisper", VID, "--en-fazla-dk", "20"], env=ortam, kos=kos) == 0
    yt = [a for a in kos.cagri if a[0] == "yt-dlp"]
    assert len(yt) == 1 and yt[0][yt[0].index("--download-sections") + 1] == "*0-1200"
    assert segmentler(d)[0]["metin"] == "merhaba" and not list(d.glob("ses*"))


def test_whisper_kurulu_degilse_exit_2(ortam, monkeypatch, capsys):
    onbellek(ortam, [])
    (onbellek(ortam, []) / "segmentler.jsonl").unlink()
    monkeypatch.setitem(sys.modules, "faster_whisper", None)
    assert main(["--whisper", VID], env=ortam, kos=Kos()) == 2
    assert "faster-whisper" in capsys.readouterr().out
