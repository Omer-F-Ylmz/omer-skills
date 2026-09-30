"""MOTOR-M9 DAYANIKLILIK-2: 403 akış yenileme · karesiz paket · hata sebebi · kurulu > alt tür · taranan bölen · whisper istisnası."""
import json
from pathlib import Path

from test_m2d import _aday
from test_m2e import _satir

from video import akil, cli
from video import parti as pt

V = "Wz4qYO-91zg"


def _sahte_kos(taze_calisir=True):
    cagri = []

    def kos(ctx, a, sure):
        cagri.append(a)
        if a[0] == "yt-dlp":
            return b"https://taze/expire/9999999999/x\n"
        if a[-1] == "-":  # aHash
            return bytes(range(64))
        url = a[a.index("-i") + 1]
        if "eski" in url or not taze_calisir:
            raise cli.Hata("ffmpeg: Server returned 403 Forbidden")
        Path(a[-1]).write_bytes(b"x")
        return b""
    return kos, cagri


# K1 önbellekteki akış URL'si 403 → akis.url yenilenir, taze -g ile bir kez yeniden
def test_k1_403_onbellek_yenilenir(tmp_path, monkeypatch):
    d = tmp_path / V
    d.mkdir()
    (d / "akis.url").write_text("https://eski/expire/9999999999/x", encoding="utf-8")
    kos, cagri = _sahte_kos()
    monkeypatch.setattr(cli, "_kos", kos)
    k = cli._kareler({}, d, [5.0], 0, 640, 1)
    assert len(k) == 1 and "taze" in (d / "akis.url").read_text(encoding="utf-8")
    assert sum(a[0] == "yt-dlp" for a in cagri) == 1


# K2 taze adresle de kare yok → paket düşmez: altyazı + açıklama + bağlantı + "kare yok: <sebep>"
def test_k2_karesiz_paket(tmp_path, monkeypatch):
    d = tmp_path / V
    d.mkdir()
    (d / "meta.json").write_text(json.dumps({"id": V, "title": "Başlık", "channel": "K", "duration": 600,
                                             "description": "bak https://ornek.dev"}), encoding="utf-8")
    (d / "segmentler.jsonl").write_text(json.dumps({"bas": 0, "son": 5, "metin": "merhaba dünya burada"}) + "\n", encoding="utf-8")
    kos, _ = _sahte_kos(taze_calisir=False)
    monkeypatch.setattr(cli, "_kos", kos)
    assert cli.main(["paket", V, "--kare", "3", "--istek-tavan", "0"], env={"VIDEO_CACHE": str(tmp_path)}) == 0
    p = pt.paket_oku(d / "paket.md")
    assert p["kareler"] == [] and p["linkler"] == ["https://ornek.dev"] and "merhaba" in p["metin"]
    assert (p.get("kare_not") or "").startswith("kare yok: ") and "403" in p["kare_not"]
    assert pt.dogrula is not None and "kare yok: " in "\n".join(pt._notlar({"parti": "p", "model": "m"}, p))


def _d(v, tarama="tamam"):
    return {"parti": "p", "durum": "x", "tavan": {"cagri": 9, "usd": 1.0}, "model": "m", "butce": 0.1,
            "videolar": {v: {"paket": {"durum": "bekliyor", "deneme": 0}, "tarama": {"durum": tarama, "deneme": 0}}}}


def _alt(onb, sure=600, paket=None, whisper=None):
    cagri = []

    def alt(a):
        cagri.append(a)
        v = a[-1]
        if a[0] == "ozet":
            (onb / v).mkdir(parents=True, exist_ok=True)
            (onb / v / "meta.json").write_text(json.dumps({"id": v, "duration": sure}), encoding="utf-8")
        elif a[0] == "whisper" and whisper:
            raise whisper
        elif a[0] == "paket":
            if paket:
                return paket(v)
            (onb / v / "paket.md").write_text("# p\n", encoding="utf-8")
        return 0
    return alt, cagri


# K3 hatalı video özetinde sebep: istisna türü + kısa ileti; "?" yok
def test_k3_hata_sebebi(tmp_path, capsys):
    pd, onb = tmp_path / "pd", tmp_path / "onb"
    pd.mkdir()
    (pd / "defter.jsonl").write_text("", encoding="utf-8")

    def cikis1(v):
        print("hata: 00:05: ffmpeg: Server returned 403 Forbidden")
        return 1
    for v, alt in (("a1", _alt(onb, paket=cikis1)[0]), ("a2", lambda a: (_ for _ in ()).throw(RuntimeError("yt-dlp çöktü")))):
        d = _d(v)
        pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
        pt._ozet(pd, d)
    out = capsys.readouterr().out
    h = [s for s in out.splitlines() if s.startswith("hatalı videolar:")]
    assert len(h) == 2 and not any("?" in s for s in h)
    assert "a1 (paket: Hata: 00:05: ffmpeg: Server returned 403 Forbidden)" in h[0]
    assert "a2 (paket: RuntimeError: yt-dlp çöktü)" in h[1]


# K4 kurulu + servis çakışması → ZATEN VAR (çakışma notu gerekçede) ve karşılaştırma kümesinde
def test_k4_kurulu_cakisma_zaten_var(tmp_path):
    a = _aday("jev-typesafe-ai", "jev")
    a.update(alt_tur="servis", esdeger_p=0.2, arac=True)
    s = _satir(tmp_path, a)
    assert "| ZATEN VAR |" in s and "alt tür çakışması (kurulu > servis)" in s
    assert akil._karsilastir(a)


# K5 taranan video başına jeton: tamam + tamam_eksik sayısına bölünür
def test_k5_taranan_bolen(tmp_path, capsys):
    (tmp_path / "defter.jsonl").write_text(json.dumps({"adim": "tarama", "girdi": 900, "onb_okuma": 0, "onb_yazma": 0,
                                                       "cikti": 0, "usd": 0.0}) + "\n", encoding="utf-8")
    d = _d("b1")
    d["videolar"].update({v: {"paket": {"durum": "tamam"}, "tarama": {"durum": "tamam_eksik"}} for v in ("b2", "b3")})
    d["videolar"]["b1"]["paket"]["durum"] = "tamam"
    pt._ozet(tmp_path, d)
    assert f"taranan video başına {pt._defter(tmp_path)[2] // 3} jeton" in capsys.readouterr().out


# K6 whisper istisna verir → video kare-yalnız yola düşer, hata değil
def test_k6_whisper_istisnasi_kare_yalniz(tmp_path, monkeypatch):
    monkeypatch.setattr(pt, "find_spec", lambda n: True)
    pd, onb = tmp_path / "pd", tmp_path / "onb"
    pd.mkdir()
    alt, cagri = _alt(onb, sure=60, whisper=RuntimeError("model indirilemedi"))
    d = _d("c1")
    pt._kos(pd, d, onb, tmp_path / "t", alt, str, None, {})
    assert d["videolar"]["c1"]["paket"]["durum"] == "tamam"
    assert "--kare-yalniz" in next(a for a in cagri if a[0] == "paket")
