"""MOTOR-M4 tarama kalitesi: K1 kurulum/komutlar · K2 tam altyazı + kare seçimi · K3 kare başına kayıt · K4 dilim + birleştirme · K5b görsel yargıç."""
from pathlib import Path

import olcum_m4 as o4
from video import akil, cli
from video import parti as pt

REPO = Path(__file__).resolve().parents[3]
PAKET = """# vid · Başlık · Kanal · süre 30:00 · sure_sn 1800 · short: false · dil tr · https://youtu.be/vid · paket: m4
## Chapter
yok
## Açıklama bağlantıları
yok
## Segmentler
[0:00] npm i foo ile kurulur
[10:00] ortada ayar
[20:00] sonda kod
## Kareler
{k1} · 1:40 · ~442 token
{k2} · 21:40 · ~1844 token · yoğun
"""


def _paket(tmp_path):
    k1, k2 = tmp_path / "k00100_0.jpg", tmp_path / "k01300_0.jpg"
    for k in (k1, k2):
        k.write_bytes(b"\xff\xd8")
    (y := tmp_path / "paket.md").write_text(PAKET.format(k1=k1.as_posix(), k2=k2.as_posix()), encoding="utf-8")
    return pt.paket_oku(y)


def _f(**ek):
    return {"id": "vid", "ozet": "o", "bolumler": [], "aciklama_baglantilari": [], "promptlar": [], "iddialar": [], "belirsizlikler": [],
            "adaylar": [{"ad": "foo", "tur": "CLI", "ne": "x", "kanit_zamani": "0:10", "kaynak": "altyazı", "kanit": "k", "repo_url": None}],
            "site_ui": [{"teknik": "lenis", "ne": "yumuşak kaydırma", "nasil": "raf döngüsü", "kutuphane": "lenis", "kanit_zamani": "0:20", "kaynak": "altyazı"}],
            "kurulum_komutlar": [{"komut": "npm i foo", "ne_yapar": "kurar", "kanit_zamani": "0:10", "kaynak": "altyazı"}],
            "kareden_okunanlar": [{"kare": "1:40", "okunan": "npm i foo"}, {"kare": "21:40", "okunan": "somut bilgi yok"}],
            "oz_denetim": [{"kategori": "adaylar", "baska_kalem": "yok"}], **ek}


def test_k1_kurulum_komutlar_rapor_ve_panel(tmp_path):
    md = pt.rapor_md(_f(), _paket(tmp_path), [])
    assert "## Kurulum/komutlar" in md and "npm i foo" in md.split("## Kurulum/komutlar")[1]
    assert "raf döngüsü" in md and "lenis" in md  # K3 üçlü rapora
    a = next(iter(akil.birlestir([("vid", md)], REPO)[0].values()))
    assert a["videolar"]["vid"]["komutlar"] == ["npm i foo"]


def test_k2_tam_altyazi_esigi():
    p = {"sure": 1200, "metin": "## Segmentler\n" + "x" * (14_000 * 4)}
    assert pt.dilimler(p) == [(0, 1200)]
    assert len(pt.dilimler({**p, "metin": "x" * (16_000 * 4)})) == 2
    assert len(pt.dilimler({"sure": 1800, "metin": "kısa"})) == 2  # >25 dk
    assert len(pt.dilimler({"sure": 600, "metin": "x" * (40_000 * 4)})) == 3


def test_k2_kare_sahne_arti_esit_aralik_ve_yogunluk():
    assert cli.kare_zamanlari(600, 4, [(100, .9), (105, .8), (400, .5)]) == [100, 225, 400, 525]
    assert cli.kare_zamanlari(600, 3, []) == [100, 300, 500]
    duz, cizgili = bytes([128] * 160 * 90), bytes(([0, 255] * 80) * 90)
    assert not cli.yogun_mu(duz, 160) and cli.yogun_mu(cizgili, 160)
    assert cli.YUKSEK == 1568


def test_k3_kare_basina_zorunlu_kayit(tmp_path, monkeypatch):
    monkeypatch.setattr(pt.hafif, "GORSEL", True)
    p = _paket(tmp_path)
    assert p["m4"] and p["kare_zaman"] == [100, 1300]
    tam = pt.dogrula({"videolar": [_f()]}, {"vid": p}, ["vid"]).get("vid", [])
    assert not any("kare kaydı" in h for h in tam)
    eksik = pt.dogrula({"videolar": [_f(kareden_okunanlar=[{"kare": "1:40", "okunan": "npm i foo"}])]}, {"vid": p}, ["vid"])["vid"]
    assert any("kare kaydı yok: 21:40" in h for h in eksik)
    bos = pt.dogrula({"videolar": [_f(kareden_okunanlar=[{"kare": "1:40", "okunan": " "}, {"kare": "21:40", "okunan": "x"}])]}, {"vid": p}, ["vid"])["vid"]
    assert any("okunan: boş olamaz" in h for h in bos)
    s = pt.sema(["vid"])["properties"]["videolar"]["items"]
    assert {"nasil", "kutuphane", "ne"} <= set(s["properties"]["site_ui"]["items"]["required"])
    assert {"oz_denetim", "kurulum_komutlar"} <= set(s["required"])


def test_k4_dilim_cagri_ve_birlestirme(tmp_path, monkeypatch):
    monkeypatch.setattr(pt.hafif, "GORSEL", True)
    p, cagrilar = _paket(tmp_path), []

    def sahte(sistem, metin, sema, kareler=(), **k):
        cagrilar.append((metin, list(kareler)))
        return {"form": {"videolar": [_f(kareden_okunanlar=[{"kare": f"k{len(cagrilar)}", "okunan": "x"}])]},
                "usage": {"input_tokens": 10, "output_tokens": 5}, "usd": .01, "sure": 1.0}
    d = {"model": "m", "butce": .5, "tavan": {"usd": 1.0, "cagri": 10}}
    y = pt._cagir_grup(pdir=tmp_path, d=d, kalan=["vid"], pk={"vid": p}, hatalar={}, temizle=str, cagir=sahte, env={})
    assert len(cagrilar) == 2 and y["dilim"] == 2 and y["usd"] == .02
    assert "[0:00]" in cagrilar[0][0] and "[20:00]" not in cagrilar[0][0] and "[20:00]" in cagrilar[1][0]
    assert [len(k) for _, k in cagrilar] == [1, 1]
    f = y["form"]["videolar"][0]
    assert len(f["adaylar"]) == 1 and len(f["kurulum_komutlar"]) == 1 and len(f["kareden_okunanlar"]) == 2


def test_k5b_gorsel_yargic_siniflama():
    def sahte(sistem, metin, sema, kareler=(), **k):
        assert "1. a" in metin and len(kareler) == 1
        return {"form": {"kararlar": [{"no": 1, "karar": "evet"}, {"no": 2, "karar": "hayır"}, {"no": 3, "karar": "okunamıyor"}]}, "usd": .01}
    k, usd = o4.gorsel_yargi(["a", "b", "c", "d"], ["k.jpg"], sahte)
    assert k == ["dayanıyor", "dayanmıyor", "okunamıyor", "ölçülemedi"] and usd == .01
