"""YARIM-BEKCI-1: H1–H6 sahte vakalar (tmp klasör; canlı kuyruğa dokunmaz)."""
import json
import os
import time

import pytest

import yarim_bekci as Y

NIHAI = "NİHAİ 31+32: kapı"


@pytest.fixture
def ort(tmp_path):
    k = tmp_path / ".kos" / "kopru"
    for d in ("gorev", "ajan-sira", "rapor", "devir"):
        (k / d).mkdir(parents=True)
    (k / "ajan-sira.tsv").write_text("# ad\tistem\n", encoding="utf-8")
    return k, tmp_path


def gorev(k, ad, metin=NIHAI, alt="gorev"):
    p = k / alt / f"{ad}.md" if alt else k / f"gorev-{ad}.md"
    p.write_text(metin, encoding="utf-8")
    return p


def kuyruk(k, *satirlar):
    with (k / "ajan-sira.tsv").open("a", encoding="utf-8") as f:
        for s in satirlar:
            f.write(s + "\n")


def bitir(k, ad, sonuc="tamam", subtype="success"):
    (k / "ajan-sira" / f"{ad}.json").write_text(json.dumps({"type": "result", "subtype": subtype, "result": sonuc}) + "\n", encoding="utf-8")


def tur(satirlar, t):
    return {s["ad"]: s for s in satirlar if s["tur"] == t}


def tara(k, kok, **kw):
    return Y.tara(k, kok, **kw)


def test_h1_kuyruga_girmemis_gorev(ort):
    k, kok = ort
    gorev(k, "yetim")
    gorev(k, "kuyrukta")
    kuyruk(k, "kuyrukta\t.kos/kopru/gorev/kuyrukta.md")
    assert set(tur(tara(k, kok), "H1")) == {"yetim"}


def test_h1_biten_gorev_sayilmaz(ort):
    k, kok = ort
    gorev(k, "eski")
    bitir(k, "eski")
    assert not tur(tara(k, kok), "H1")


def test_h1_kok_gorev_dosyasi(ort):
    k, kok = ort
    gorev(k, "kokte", alt=None)
    assert set(tur(tara(k, kok), "H1")) == {"kokte"}


def test_h2_karar_gerekiyor(ort):
    k, kok = ort
    bitir(k, "is-a", "Yaptım. Karar gerekiyor: hangisi?")
    s = tur(tara(k, kok), "H2")
    assert "is-a" in s and "Karar gerekiyor" in s["is-a"]["kanit"]


def test_h2_sonraki_is_temiz_bitirdiyse_kapanir(ort):
    k, kok = ort
    bitir(k, "is-a", "onay gelirse devam ederim")
    os.utime(k / "ajan-sira" / "is-a.json", (time.time() - 500, time.time() - 500))
    bitir(k, "is-a2", "tamam, hepsi bitti")
    assert not tur(tara(k, kok), "H2")


def test_h2_zayif_kalip_yalniz_basarisiz_bitiste(ort):
    k, kok = ort
    bitir(k, "ok-is", "Bitti. Push yapılmadı.")
    bitir(k, "kotu-is", "Rapor yazılamadı, 3. madde yapılmadı.", subtype="error_max_turns")
    assert set(tur(tara(k, kok), "H2")) == {"kotu-is"}


def test_h1_otomatik_deneme_adi_sayilmaz(ort):
    k, kok = ort
    gorev(k, "is-a")
    gorev(k, "is-a2")
    gorev(k, "is-r")
    assert not tur(tara(k, kok), "H1")


def test_h2_temiz_sonuc(ort):
    k, kok = ort
    bitir(k, "is", "Bitti. 12 test geçti.")
    assert not tur(tara(k, kok), "H2")


def test_h3_rapor_istendi_yok(ort):
    k, kok = ort
    gorev(k, "rapor-is", NIHAI + "\nRapor: rapor/rapor-is.md yaz.")
    kuyruk(k, "rapor-is\t.kos/kopru/gorev/rapor-is.md")
    bitir(k, "rapor-is")
    assert "rapor-is" in tur(tara(k, kok), "H3")
    (k / "rapor" / "rapor-is.md").write_text("x", encoding="utf-8")
    assert not tur(tara(k, kok), "H3")


def test_h3_bitmemis_is_sayilmaz(ort):
    k, kok = ort
    gorev(k, "j", NIHAI + "\nrapor/j.md")
    kuyruk(k, "j\t.kos/kopru/gorev/j.md")
    assert not tur(tara(k, kok), "H3")


def test_h4_devirde_dusen_madde(ort):
    k, kok = ort
    gorev(k, "video-x")
    kuyruk(k, "video-x\t.kos/kopru/gorev/video-x.md\t.kos/kopru/yok.txt::a")
    eski = k / "devir" / "desktop-devir-eski.md"
    eski.write_text("# Devir\n## Bekleyenler\n- video-x işi sürecek\n", encoding="utf-8")
    yeni = k / "devir" / "desktop-devir-yeni.md"
    yeni.write_text("# Devir\n## Durum\n- hiçbir şey\n", encoding="utf-8")
    os.utime(eski, (time.time() - 100, time.time() - 100))
    assert "video-x" in tur(tara(k, kok), "H4")
    yeni.write_text("# Devir\n## Bekleyenler\n- video-x hâlâ\n", encoding="utf-8")
    assert not tur(tara(k, kok), "H4")


def test_h5_gorev_yolu_tasindi_yalniz_yol_degisir(ort):
    k, kok = ort
    p = gorev(k, "tasinan")
    kuyruk(k, "tasinan\tC:\\Eski\\Yer\\gorev-tasinan.md\tkosul\tefor=high\tmodel=sonnet", "baska\t.kos/kopru/gorev/baska.md")
    gorev(k, "baska")
    oncesi = sorted(x.name for x in k.rglob("*") if x.is_file())
    govde = p.read_text(encoding="utf-8")
    sonuc = Y.calistir(k, kok)
    satir = (k / "ajan-sira.tsv").read_text(encoding="utf-8").splitlines()[1].split("\t")
    assert satir[0] == "tasinan" and satir[2:] == ["kosul", "efor=high", "model=sonnet"]
    assert (kok / satir[1]).resolve() == p.resolve()
    assert p.read_text(encoding="utf-8") == govde
    assert sorted(x.name for x in k.rglob("*") if x.is_file()) == oncesi + ["yarim.tsv"]
    assert any("YARIM-DUZELTILDI H5 tasinan" in s for s in sonuc[1])
    assert not tur(tara(k, kok), "H5")


def test_h5_cozulemeyen_yol_dokunulmaz(ort):
    k, kok = ort
    kuyruk(k, "kayip\tC:\\Yok\\gorev-kayip.md")
    oncesi = (k / "ajan-sira.tsv").read_text(encoding="utf-8")
    Y.calistir(k, kok)
    assert (k / "ajan-sira.tsv").read_text(encoding="utf-8") == oncesi
    assert "kayip" in tur(tara(k, kok), "H5")


def test_h5_cwd_tasindi(ort):
    k, kok = ort
    gorev(k, "c")
    (kok / "proje-x").mkdir()
    kuyruk(k, f"c\t.kos/kopru/gorev/c.md\t\tefor=low\tcwd={kok.as_posix()}/eski-kok/proje-x")
    assert "c" in tur(tara(k, kok), "H5")
    Y.calistir(k, kok)
    assert f"cwd={kok.as_posix()}/proje-x" in (k / "ajan-sira.tsv").read_text(encoding="utf-8")
    assert not tur(tara(k, kok), "H5")


def test_h5_baslamis_satira_bakilmaz(ort):
    k, kok = ort
    kuyruk(k, "eski\tC:\\Yok\\gorev-eski.md")
    (k / "ajan-sira" / "eski.basladi").write_text("x", encoding="utf-8")
    assert not tur(tara(k, kok), "H5")


def test_h6_nihai_satiri_yok_otomatik_eklenir(ort):
    k, kok = ort
    p = gorev(k, "k", "Görev metni\nikinci satır")
    kuyruk(k, "k\t.kos/kopru/gorev/k.md")
    assert "k" in tur(tara(k, kok), "H6")
    sonuc = Y.calistir(k, kok)
    yeni = p.read_text(encoding="utf-8")
    assert yeni.startswith("Görev metni\nikinci satır") and "NİHAİ 31+32" in yeni
    assert any("YARIM-DUZELTILDI H6 k" in s for s in sonuc[1])
    assert not tur(tara(k, kok), "H6")


def test_h6_baslamis_is_degismez(ort):
    k, kok = ort
    p = gorev(k, "b", "metin")
    kuyruk(k, "b\t.kos/kopru/gorev/b.md")
    (k / "ajan-sira" / "b.basladi").write_text("x", encoding="utf-8")
    Y.calistir(k, kok)
    assert p.read_text(encoding="utf-8") == "metin"


def test_muaf(ort):
    k, kok = ort
    gorev(k, "nikke-3")
    gorev(k, "baska")
    (k / "yarim-muaf.tsv").write_text("# ad\tgerekce\tkarar\nnikke*\tbekliyor\tÖmer\n", encoding="utf-8")
    assert set(tur(tara(k, kok), "H1")) == {"baska"}


def test_muaf_h4_icin_de_gecerli(ort):
    k, kok = ort
    gorev(k, "video-x")
    kuyruk(k, "video-x\t.kos/kopru/gorev/video-x.md\t.kos/kopru/yok.txt::a")
    eski = k / "devir" / "desktop-devir-eski.md"
    eski.write_text("# Devir\n## Bekleyenler\n- video-x işi sürecek\n", encoding="utf-8")
    (k / "devir" / "desktop-devir-yeni.md").write_text("# Devir\n## Durum\n- hiçbir şey\n", encoding="utf-8")
    os.utime(eski, (time.time() - 100, time.time() - 100))
    (k / "yarim-muaf.tsv").write_text("video-x\tBEKLEMEDE\tÖmer\n", encoding="utf-8")
    assert not tur(tara(k, kok), "H4")


def test_h1_sablon_kural_dosyasi_is_degil(ort):
    k, kok = ort
    gorev(k, "DEVAM-KURALI")
    gorev(k, "_sablon")
    gorev(k, "gercek")
    assert set(tur(tara(k, kok), "H1")) == {"gercek"}


def test_tsv_ilk_gorulme_korunur_ve_yeni_satir_bir_kez(ort):
    k, kok = ort
    gorev(k, "yetim")
    tsv, log1 = Y.calistir(k, kok)
    ilk = (k / "yarim.tsv").read_text(encoding="utf-8").splitlines()
    assert ilk[0].startswith("# ad\ttür\tilk görülme") and ilk[1].split("\t")[:2] == ["yetim", "H1"]
    assert any(s.startswith("YARIM H1 yetim") for s in log1)
    time.sleep(1.1)
    _, log2 = Y.calistir(k, kok)
    assert (k / "yarim.tsv").read_text(encoding="utf-8").splitlines()[1] == ilk[1]
    assert not log2


def test_ozet_ve_devir_blogu(ort):
    k, kok = ort
    gorev(k, "yetim")
    Y.calistir(k, kok)
    assert Y.ozet_satirlar(k)[0] == "YARIM: 1 açık (H1:1)"
    assert "yetim" in Y.devir_blogu(k)


def test_tam_kip_eski_isi_gorur_pencere_disinda(ort):
    k, kok = ort
    eski = time.time() - 30 * 86400
    for ad in ("eski-yok", "eski-bitti", "eski-planda", "telve-x"):
        os.utime(gorev(k, ad, alt=None), (eski, eski))
    (k / "ajan-sira.log").write_text("10:00 BAŞLAT eski-yok x\n10:05 BİTTİ eski-bitti rc 0 1 dk\n", encoding="utf-8")
    (k / "gorev-yarim-g1.md").write_text("kapsam: eski-planda", encoding="utf-8")
    assert not {s["ad"] for s in Y.tara(k, kok)} & {"eski-yok", "eski-bitti", "eski-planda"}  # pencere (3 gün) değişmedi: eski iş bekçide görünmez
    assert {(s["ad"], s["tur"]) for s in Y.tam_tara(k, kok)} == {("eski-yok", "YOK:BAŞLADI-BİTMEDİ")}
    assert Y.tam_ozet(k, kok) == "YARIM-TAM: 1 açık (YOK:BAŞLADI-BİTMEDİ:1)"
