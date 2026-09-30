"""MOTOR-M4 tarama kalitesi: K1 kurulum/komutlar · K5b görsel yargıç · M4c: K2/K3/K4 geri alındı (86HM testi)."""
from pathlib import Path

import olcum_m4 as o4
from video import akil, hafif
from video import parti as pt
from test_m2a import _ctx, _durum, _ns

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


def test_k5b_gorsel_yargic_siniflama():
    def sahte(sistem, metin, sema, kareler=(), **k):
        assert "1. a" in metin and len(kareler) == 1
        return {"form": {"kararlar": [{"no": 1, "karar": "evet"}, {"no": 2, "karar": "hayır"}, {"no": 3, "karar": "okunamıyor"}]}, "usd": .01}
    k, usd = o4.gorsel_yargi(["a", "b", "c", "d"], ["k.jpg"], sahte)
    assert k == ["dayanıyor", "dayanmıyor", "okunamıyor", "ölçülemedi"] and usd == .01

def test_86hm_kare_kaydi_yoklugu_form_red_yapmaz(tmp_path, monkeypatch):
    """M4c geri alma (M4b ölçümü, db8de15): 86HM0RUWhCk M3b'deki gibi işlenir — kareli pakette kareden_okunanlar boş form kabul."""
    monkeypatch.setattr(hafif, "GORSEL", True)
    v, cagrilar = "86HM0RUWhCk", []
    (d := tmp_path / "c" / v).mkdir(parents=True)
    k1, k2 = d / "k00100_0.jpg", d / "k01300_0.jpg"
    for k in (k1, k2):
        k.write_bytes(b"\xff\xd8")
    (d / "paket.md").write_text(PAKET.replace("vid", v).format(k1=k1.as_posix(), k2=k2.as_posix()), encoding="utf-8")
    (tmp_path / "kuyruk.md").write_text("### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n"
                                        f"| {v} | 30.0 | t | - | bekliyor |\n", encoding="utf-8")

    def sahte(sistem, metin, sema, **k):
        cagrilar.append(k.get("kareler"))
        return {"form": {"videolar": [{**{a: b for a, b in _f().items() if a != "oz_denetim"}, "id": v}]}, "usd": 0.01, "sure": 0.1, "hata": None,
                "usage": {"input_tokens": 10, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 100, "output_tokens": 50}}

    pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _ctx(tmp_path, sahte))
    assert _durum(tmp_path)["videolar"][v]["tarama"]["durum"] not in ("form_red", "tamam_eksik")
    assert len(cagrilar) == 1 and cagrilar[0]  # tek çağrı (dilim yok), kareler gönderildi
