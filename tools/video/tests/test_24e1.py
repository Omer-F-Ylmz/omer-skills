"""KURULUM-24e-1 hat sağlamlaştırma: slug ASCII · argv \\r · destek idempotent · katman bağlantı toleransı · T0 şeması.
Ağsız; Jev sahte `gonder`, komutlar sahte `kos`."""
from video import cli, ogren as og, uygula as uy
from video.cli import main

from test_ogren import OJev
from test_uygula import UKos, aday, kayit, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

T0 = (f"# kural-x\nad: kural-x\ntur: ipucu\nvideo: {VID}\netiket: yeniden:parti-d\nkural: Tek mesajda sor\nkarar: KURAL\n"
      f"## Ne\nTek mesajda sor\n## Kanıt\n{VID} 1:00: \"sor\"\n## İddia sınama\n| iddia | kaynak | sonuç |\n|---|---|---|\n| x | - | doğrulanamadı |\n"
      "## Bizde durum\n- kurulum: yok\n")


# K1 slug ASCII, idempotent; eski (Türkçe) slug yeni ada çözülür
def test_k1_slug_ascii():
    s = cli._slug("awwwards-seviyesi-tasarım-kuralları-iste")
    assert s == "awwwards-seviyesi-tasarim-kurallari-iste"
    assert cli._slug(s) == s
    assert cli._slug("İŞĞÜÖÇ ışğüöç") == "isguoc-isguoc"


def test_k1_eski_slug_kural_onay_cozulur(ortam, kok, capsys):
    assert main(["kural-onay", "soruları-tek-mesajda-topla", "--kapsam", "genel"], env=ortam) == 1
    assert "kural-sorulari-tek-mesajda-topla.md" in capsys.readouterr().out


# K2 + K5 \r'li yol ve T0 şeması
def test_k2_k5_crlf_yol_t0_gecer(ortam, tmp_path, capsys):
    y = tmp_path / "kural-x.md"
    y.write_text(T0, encoding="utf-8")
    assert main(["rapor-denetle", f"{y}\r"], env=ortam) == 0
    assert "rapor-denetle (T0): GEÇTİ" in capsys.readouterr().out


def test_k5_t0_eksik_alanlar():
    h = uy.t0_denetle(T0.replace("karar: KURAL\n", "").replace("## Bizde durum\n- kurulum: yok\n", ""))
    assert h == ["T0 alanı eksik: karar", "T0 bölümü eksik: Bizde durum"]
    assert uy.t0_denetle(T0) == []


# K3 destek satırı idempotent
def test_k3_destek_idempotent():
    m = og.destek("---\nad: x\n---\n", f"- destek: sor ({VID} 1:00)")
    assert og.destek(m, f"- destek: sor ({VID} 1:00)") == m
    assert m.count("- destek:") == 1


# K4 bağlantı hatası → 2 tekrar, aday SORULMADI: bağlantı, koşu sürer; hepsi düşerse rc 1
class KopukJev(OJev):
    def __init__(self, kopuk, **kw):
        super().__init__(**kw)
        self.kopuk, self.cagri = kopuk, 0

    def __call__(self, url, basliklar, veri):
        self.cagri += 1
        if self.cagri <= self.kopuk:
            raise OSError("bağlanılamadı")
        return super().__call__(url, basliklar, veri)


def _katman(ortam, yollar, g):
    return main(["katman", *map(str, yollar)], env=ortam, kos=UKos(), gonder=g, uyku=lambda s: None)


def test_k4_baglanti_hatasi_isaretli_devam(ortam, kok, capsys):
    y1 = aday(kok, "kopuk-aday", tur="iş akışı", repo="yok", lisans="yok", son_commit="yok", kural="Log dosyasından hata çöz")
    y2 = aday(kok, "saglam-aday", tur="iş akışı", repo="yok", lisans="yok", son_commit="yok", kural="Soruları tek mesajda topla")
    g = KopukJev(3, secim=[("dört tür", "ipucu")])
    assert _katman(ortam, [y1, y2], g) == 0
    k = {x["ad"]: x for x in kayit(kok)}
    assert k["kopuk-aday"]["karar"] == "SORULMADI: bağlantı" and k["saglam-aday"]["karar"] != "SORULMADI: bağlantı"
    out = capsys.readouterr().out
    assert "bağlantı" in out and "Jev istek" in out


def test_k4_hepsi_duserse_rc1(ortam, kok):
    y1 = aday(kok, "kopuk-aday", tur="iş akışı", repo="yok", lisans="yok", son_commit="yok", kural="Log dosyasından hata çöz")
    assert _katman(ortam, [y1], KopukJev(10 ** 6)) == 1
    assert kayit(kok)[-1]["karar"] == "SORULMADI: bağlantı"
