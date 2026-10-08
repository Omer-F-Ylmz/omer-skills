"""VİDEO-PARTİ-YT1 3: boru hattı paralelliği (ikili yol). Sahte taşıyıcı/alt/kos; ağ ve claude -p yok.
Süre testleri (a)/(A) gerçek kısa uyku kullanır: tarif 2 s / 3 s / 12 s eşikleri 10'a bölündü (0.2 / 0.3 / 1.2 s)."""
import json
import threading
import time
from pathlib import Path

import pytest

from video import cli
from video import goz as gz
from video import parti as pt
from video import tarama as tr
from test_m2a import _form, _ns

SON, HAI = "claude-sonnet-5-5", "claude-haiku-5-5"
IKILI = {"tarama": {"yontem": "ikili", "modeller": [SON, HAI]}}


def _idler(n):
    return [f"vid{i:08d}" for i in range(n)]


class Say:
    """Eşzamanlılık sayacı: with s: → anlık ve en çok eşzamanlı giriş."""

    def __init__(self):
        self.k, self.anlik, self.en = threading.Lock(), 0, 0

    def __enter__(self):
        with self.k:
            self.anlik += 1
            self.en = max(self.en, self.anlik)

    def __exit__(self, *a):
        with self.k:
            self.anlik -= 1


def _paket_yaz(onb, v):
    d = onb / v
    d.mkdir(parents=True, exist_ok=True)
    (d / "paket.md").write_text(f"# {v} · Başlık · Kanal · süre 5:00 · sure_sn 300 · short: false · dil tr · https://youtu.be/{v}\n"
                                "## Chapter\nyok\n## Açıklama bağlantıları\nyok\n## Segmentler\n[0:00] merhaba\n[0:05] bu araç işi hızlandırıyor\n## Kareler\nyok\n", encoding="utf-8")


def _sahte_alt(onb, uyku=0.0):
    def alt(argv):
        v = argv[-1]
        if argv[0] == "ozet":
            (onb / v).mkdir(parents=True, exist_ok=True)
            (onb / v / "segmentler.jsonl").write_text(json.dumps({"bas": 0, "son": 5, "metin": "merhaba bu araç işi hızlandırıyor"}) + "\n", encoding="utf-8")
        elif argv[0] == "paket":
            time.sleep(uyku)
            _paket_yaz(onb, v)
        return 0
    return alt


def _kur(tmp_path, monkeypatch, idler, alt=None, cagir=None, **ns_ek):
    monkeypatch.setattr(pt, "YONLENDIRME", IKILI)
    kok = tmp_path
    (kok / "kuyruk.md").write_text("### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n"
                                   + "".join(f"| {v} | 5.0 | t | - | bekliyor |\n" for v in idler), encoding="utf-8")
    ctx = {"env": {"VIDEO_UYGULA_KOK": str(kok), "VIDEO_CACHE": str(kok / "c")}, "kok": kok / "c", "tarama_dizin": kok / "docs" / "video-tarama",
           "cagir": cagir, "temizle": lambda s: s, "kos": None, "gonder": None, "uyku": lambda s: None}
    if alt:
        ctx["alt"] = alt
    return kok, ctx, _ns("baslat", kok / "kuyruk.md", cagri_tavan=500, usd_tavan=50.0, **ns_ek)


def _pdir(kok):
    return next((kok / ".kos").iterdir())


def _durum(kok):
    return json.loads((_pdir(kok) / "durum.json").read_text(encoding="utf-8"))


def _cagir_uyku(s, say=None):
    def cagir(sistem, metin, sema, **k):
        ids = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"]
        with say or Say():
            time.sleep(s)
        return {"form": {"videolar": [_form(v) for v in ids]}, "usage": {"input_tokens": 1, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0, "output_tokens": 1},
                "usd": 0.01, "sure": 0.1, "hata": None}
    return cagir


# (a) iki model eşzamanlı: 0.2 s + 0.3 s uyuyan sahte taşıyıcı → toplam < 0.4 s (art arda 0.5 s)
def test_tara_ikili_modeller_eszamanli(tmp_path):
    v = "aaaaaaaaaa1"
    pk = {v: {"kareler": [], "sure": 300, "metin": "x"}}
    d = {"butce": .5, "tavan": {"usd": 5.0}, "videolar": {v: {"tarama": {}}}}
    gecen = {SON: .2, HAI: .3}

    def cagir(sistem, metin, sema, **k):
        time.sleep(gecen[k["model"]])
        return {"form": {"videolar": [_form(v)]}, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": None, "model": k["model"]}
    t0 = time.monotonic()
    y = pt._tara_ikili([v], pk, {}, lambda s: s, d, tmp_path, {}, cagir, [SON, HAI])
    assert time.monotonic() - t0 < .4 and y["cagri"] == 2 and "tek kol" not in d["videolar"][v]["tarama"]["kunye"]
    assert d["videolar"][v]["tarama"]["kunye"].startswith(f"{SON}:")  # sıra model listesi sırası


# (A) 4 video, paketleme 0.2 s + tarama 0.3 s, N=2 → toplam < 1.2 s (bariyerli sürüm ≥ 1.4 s)
def test_boru_hatti_bariyersiz(tmp_path, monkeypatch):
    kok, ctx, ns = _kur(tmp_path, monkeypatch, _idler(4), cagir=_cagir_uyku(.3), paralel=2)
    ctx["alt"] = _sahte_alt(kok / "c", .2)
    t0 = time.monotonic()
    assert pt.parti(ns, ctx) == 0
    assert time.monotonic() - t0 < 1.2
    assert all(s["tarama"]["durum"] == "tamam" for s in _durum(kok)["videolar"].values())


# (ii) N=4, 9 video: kayit/defter/durum sağlam, her iş parçacığının kendi ctx'i
def test_dokuz_video_dort_is_parcacigi(tmp_path, monkeypatch):
    idler = _idler(9)
    ctxler = []

    def paket_(ns, ctx):
        ctxler.append(ctx)
        time.sleep(.02)
        _paket_yaz(ctx["kok"], ns.id)
        return 0

    def ozet_(ns, ctx):
        _sahte_alt(ctx["kok"])(["ozet", "--", ns.hedef[0]])
        return 0
    monkeypatch.setattr(cli, "paket", paket_)
    monkeypatch.setattr(cli, "ozet", ozet_)
    kok, ctx, ns = _kur(tmp_path, monkeypatch, idler, cagir=_cagir_uyku(.03), paralel=4, en_fazla=25)
    assert pt.parti(ns, ctx) == 0
    assert len(ctxler) == 9 and len({id(c) for c in ctxler}) == 9
    kayit = [json.loads(s) for s in (kok / "docs" / "video-tarama" / "kayit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert sorted(k["id"] for k in kayit) == idler and all("konu" in k for k in kayit)
    defter = tr.kayit_oku(_pdir(kok) / "defter.jsonl")
    assert sorted(v for x in defter if x["adim"] == "tarama" for v in x["videolar"]) == idler
    assert _durum(kok)["durum"] == "tamam" and not list(_pdir(kok).glob("*.tmp"))


# (iii) bir video hata verir, diğerleri sürer
def test_bir_video_hata_digerleri_surer(tmp_path, monkeypatch):
    idler = _idler(4)
    kok, ctx, ns = _kur(tmp_path, monkeypatch, idler, cagir=_cagir_uyku(.01), paralel=3)
    temel = _sahte_alt(kok / "c")

    def alt(argv):
        if argv[0] == "paket" and argv[-1] == idler[1]:
            raise RuntimeError("indirme patladı")
        return temel(argv)
    ctx["alt"] = alt
    pt.parti(ns, ctx)
    d = _durum(kok)["videolar"]
    assert d[idler[1]]["paket"]["durum"] == "hata" and "indirme patladı" in d[idler[1]]["paket"]["hata"]
    assert sorted(v for v, s in d.items() if s["tarama"]["durum"] == "tamam") == [idler[0], idler[2], idler[3]]


# (iv) 429 → tam bir yeniden tur (BEKLE sonrası); yine 429 → o video hata, öbürü tamam
def test_429_tam_bir_yeniden(tmp_path, monkeypatch):
    idler = _idler(2)
    uykular, say = [], {}
    monkeypatch.setattr(pt, "BEKLE", uykular.append)

    def cagir(sistem, metin, sema, **k):
        v = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"][0]
        say[v] = say.get(v, 0) + 1
        if v == idler[0]:
            return {"form": None, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": "HTTP 429 rate limit"}
        return _cagir_uyku(0)(sistem, metin, sema, **k)
    kok, ctx, ns = _kur(tmp_path, monkeypatch, idler, cagir=cagir, paralel=2)
    ctx["alt"] = _sahte_alt(kok / "c")
    pt.parti(ns, ctx)
    d = _durum(kok)["videolar"]
    assert say[idler[0]] == 4 and say[idler[1]] == 2  # 2 tur × 2 kol; sağlam video yeniden alınmaz
    assert uykular == [pt.SON_TUR_SN] and d[idler[0]]["tarama"]["durum"] == "hata" and d[idler[1]]["tarama"]["durum"] == "tamam"


# model çağrısı eşzamanlılığı CAGIR ile sınırlı (6)
def test_cagir_semaforu_altiyi_asmaz(tmp_path, monkeypatch):
    say = Say()
    kok, ctx, ns = _kur(tmp_path, monkeypatch, _idler(8), cagir=_cagir_uyku(.05, say), paralel=8)
    ctx["alt"] = _sahte_alt(kok / "c")
    pt.parti(ns, ctx)
    assert 2 <= say.en <= 6


def _goz_kur(tmp_path, monkeypatch):
    """_goz_ocr için sahte ffmpeg/OCR: sahne (ffmpeg) ve ocr eşzamanlılığı + tampon doluluğu ölçülür."""
    sahne, ocr = Say(), Say()
    en_tampon = [0]
    monkeypatch.setattr(gz, "sahneler", lambda h, f: [(0.0, 64), (1.0, 64)])
    monkeypatch.setattr(gz, "kare_sec", lambda s, *a, **k: s)
    monkeypatch.setattr(cli, "_ram_kapi", lambda ctx: None, raising=False)

    def indir(ctx, d):
        en_tampon[0] = max(en_tampon[0], 3 - cli.TAMPON._value)
        time.sleep(.03)
        return d / "goz-video.mp4"

    def kos(ctx, args, timeout):
        with sahne:
            time.sleep(.03)
        if "-start_number" in args:
            for i in (1, 2):
                (Path(args[-1]).parent / f"s{i:04d}.jpg").write_bytes(b"x")
        return b""

    def ocr_(ctx, yollar, ham=False):
        with ocr:
            time.sleep(.03)
        return {}
    monkeypatch.setattr(cli, "_video_indir", indir)
    monkeypatch.setattr(cli, "_kos", kos)
    monkeypatch.setattr(cli, "_ocr", ocr_)
    return sahne, ocr, en_tampon


def test_sahne_ve_ocr_asla_iki_olmaz_tampon_uc(tmp_path, monkeypatch):
    sahne, ocr, en_tampon = _goz_kur(tmp_path, monkeypatch)
    hatalar = []

    def is_(i):
        try:
            (kd := tmp_path / f"kd{i}").mkdir()
            cli._goz_ocr({"uyku": lambda s: None}, tmp_path / f"v{i}", kd, 10, 1)
        except Exception as e:  # noqa: BLE001
            hatalar.append(repr(e))
    ts = [threading.Thread(target=is_, args=(i,)) for i in range(6)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    assert not hatalar, hatalar
    assert sahne.en == 1 and ocr.en == 1 and 1 <= en_tampon[0] <= 3
    assert cli.TAMPON._value == 3  # her iş sonunda bırakıldı


# RAM kapısı: düşükse 60 sn bekler; 10 ardışık düşük → durdurur
def test_ram_dusuk_bekler_sonra_gecer(monkeypatch):
    degerler, uykular = iter([1.0, 1.5, 3.0]), []
    monkeypatch.setattr(cli, "bos_ram", lambda: next(degerler))
    cli._ram_kapi({"uyku": uykular.append})
    assert uykular == [60, 60]


def test_ram_on_ardisik_dusuk_durur(monkeypatch):
    uykular = []
    monkeypatch.setattr(cli, "bos_ram", lambda: 0.5)
    with pytest.raises(cli.RamYetersiz, match="RAM yetersiz"):
        cli._ram_kapi({"uyku": uykular.append})
    assert len(uykular) == 9  # 10. ölçümde durur


def test_ram_yetersiz_parti_durur(tmp_path, monkeypatch):
    idler = _idler(3)
    kok, ctx, ns = _kur(tmp_path, monkeypatch, idler, cagir=_cagir_uyku(0), paralel=1)

    def alt(argv):
        if argv[0] == "paket":
            print("hata: RAM yetersiz: boş 0.5 GB < 2")
            return 1
        return _sahte_alt(kok / "c")(argv)
    ctx["alt"] = alt
    assert pt.parti(ns, ctx) == 6
    d = _durum(kok)["videolar"]
    assert d[idler[0]]["paket"]["durum"] == "hata" and all(d[v]["paket"]["durum"] == "bekliyor" for v in idler[1:])


# indirme başlangıçları arası rastgele boşluk yalnız paralel > 1'de
def test_indirme_boslugu_yalniz_paralelde(tmp_path, monkeypatch):
    uykular = []
    monkeypatch.setattr(cli, "RASTGELE", lambda a, b: 7.0)
    monkeypatch.setattr(cli, "_ram_kapi", lambda ctx: None)
    monkeypatch.setattr(cli, "_kos", lambda ctx, a, t: (tmp_path / "goz-video.mp4").write_bytes(b"x") and b"")
    cli._INDIR_SON[0] = None
    monkeypatch.setattr(cli, "INDIR_ARA", None)
    cli._video_indir({"uyku": uykular.append}, tmp_path)
    assert uykular == []
    (tmp_path / "goz-video.mp4").unlink()
    monkeypatch.setattr(cli, "INDIR_ARA", (5, 15))
    cli._video_indir({"uyku": uykular.append}, tmp_path)  # ilk başlangıç: beklemez
    (tmp_path / "goz-video.mp4").unlink()
    cli._video_indir({"uyku": uykular.append}, tmp_path)
    assert len(uykular) == 1 and 0 < uykular[0] <= 7.0


# aşama zamanlaması stderr'e, paket.md'ye değil
def test_asama_stderr(capsys):
    with cli.asama("abc", "ocr"):
        pass
    e = capsys.readouterr()
    assert "[aşama] abc ocr başla " in e.err and "[aşama] abc ocr bitti " in e.err and e.out == ""


# --yalniz-paket: paketleme biter, model çağrısı 0
def test_yalniz_paket_model_cagirmaz(tmp_path, monkeypatch):
    def cagir(*a, **k):
        raise AssertionError("model çağrılmamalı")
    kok, ctx, ns = _kur(tmp_path, monkeypatch, _idler(2), cagir=cagir, paralel=2, yalniz_paket=True)
    ctx["alt"] = _sahte_alt(kok / "c")
    assert pt.parti(ns, ctx) == 0
    d = _durum(kok)["videolar"]
    assert all(s["paket"]["durum"] == "tamam" and s["tarama"]["durum"] == "bekliyor" for s in d.values())


# ikili yolda kuyruk_parti sınırı (3 uzun) uygulanmaz; en_fazla geçerli
def test_ikili_parti_boyu_en_fazla(tmp_path, monkeypatch):
    kok, ctx, ns = _kur(tmp_path, monkeypatch, _idler(6), cagir=_cagir_uyku(0), paralel=2, en_fazla=5)
    ctx["alt"] = _sahte_alt(kok / "c")
    pt.parti(ns, ctx)
    assert len(_durum(kok)["videolar"]) == 5
