"""23b: ÜRETİLEBİLİR · kalite takası (omer-kurallar 21) · tasarruf ayrıştırma (24) · onarım turu tavanı."""
import json

import pytest

from video import kur, tarama as tr
from video.cli import main

from test_derin import ozellikli, uygula_raporu
from test_kalite import taslak, uyarlama
from test_kur import KKos, SJev
from test_uygula import UKos, calis, kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

E = {"cikti": 25, "maliyet": None}


# --- K8 ÜRETİLEBİLİR ---

def test_uretilebilir_skill_gorunur_arac_ayari_gorunmez(ortam, kok):
    y = ozellikli(kok, "arac",
                  {"slug": "ozet-skill", "karar": "UYARLA", "fikir": "f", "hedef": "skills/ozet/SKILL.md", "hedef_tur": "skill", "etki": "çıktı −%30"},
                  {"slug": "ayar", "karar": "UYARLA", "fikir": "f", "hedef": "settings.json", "hedef_tur": "arac-ayari", "etki": "girdi −%10"})
    assert calis(ortam, [y], UKos()) == 0
    u = tr.bolum(uygula_raporu(kok), "ÜRETİLEBİLİR")
    assert "arac-ozet-skill" in u and "claude -p" in u and "$" in u
    assert "arac-ayar" not in u


# --- K9 takas tablosu: her kademenin sınırı ---

@pytest.mark.parametrize("s,d,k", [
    (25, 10, "AL"), (25, 10.1, "SOR"),       # %10 kademesi; 10.1 ara durum
    (24.9, 5, "RED"), (25, 5, "AL"),         # tasarruf %25 sınırı
    (30, 15, "AL"), (30, 15.1, "RED"),       # %15 kademesi
    (49.9, 18, "RED"), (50, 18, "SOR"),      # %15-20: %50 sınırı
    (74.9, 18, "SOR"), (75, 18, "AL"),       # %15-20: %75 sınırı
    (75, 20, "AL"), (75, 20.1, "SOR"),       # %20 sınırı
    (49.9, 25, "RED"), (50, 25, "SOR"),      # >%20: %50 sınırı
    (28, 12, "SOR"),                         # tabloya uymayan ara durum
])
def test_takas_kademeleri(s, d, k):
    assert kur.takas(s, d, True)[0].startswith(k)


def test_dusus_sifirsa_esige_bakilir():
    assert kur.takas(5, 0, True)[0] == "AL"
    assert kur.takas(5, 0, False)[0] == "RED(token)"


def test_karar_kademeyi_yazar_ve_gurultu_bandi_sifir():
    a = {"cikti": 100, "girdi": 100, "kalite": 3.0, "maliyet": 1.0, "basari": 1.0}
    k = kur.karar(a, {"cikti": 60, "girdi": 60, "kalite": 2.95, "maliyet": 0.6, "basari": 1.0}, E, 0.1, [(1.0, 1.0)])
    assert k.startswith("AL") and "kademe" in k and "düşüş %0.0" in k and "tasarruf %40.0" in k


def test_basari_dususu_puan_dususunu_ezer():
    a = {"cikti": 100, "girdi": 100, "kalite": 3.0, "maliyet": 1.0, "basari": 1.0}
    b = {"cikti": 60, "girdi": 60, "kalite": 2.85, "maliyet": 0.6, "basari": 0.8}  # kalite −%5 · başarı −%20 · tasarruf %40
    k = kur.karar(a, b, E, 0.0, [(1.0, 0.8)])
    assert k.startswith("RED") and "düşüş %20.0" in k


# --- K10 ayrıştırma adayı yalnız RED(kalite/takas)/SOR ---

@pytest.mark.parametrize("karar,var", [
    ("SOR [ara]: x", True), ("RED(takas) [x]: x", True), ("RED(kalite): x", True),
    ("AL [x]: x", False), ("RED(token): x", False),
])
def test_ayristirma_adayi_yalniz_red_kalite_ya_da_sor(tmp_path, karar, var):
    kur.ayristir_aday(tmp_path, "x", karar, {"cikti": 20.7, "girdi": 0.0, "maliyet": -7.7}, ["1-ozet"])
    assert (tmp_path / "docs" / "uyarlamalar" / "x-ayristir.md").is_file() == var


def test_tasarrufsuz_ozellige_ayristirma_yok(tmp_path):
    kur.ayristir_aday(tmp_path, "x", "SOR [ara]: x", {"cikti": -5.0, "girdi": -1.0, "maliyet": -2.0}, [])
    assert not (tmp_path / "docs" / "uyarlamalar" / "x-ayristir.md").exists()


# --- K10(c) onarım turu tavanı ---

def _oz(kok):
    uyarlama(kok, "u-oz", arac="skill", tavan=200)
    taslak(kok, "Hitap yok. Kod ve komut aynen kalır; yalnız açıklama kısalır.", "u-oz", arac="skill")


def test_ucuncu_onarim_turu_kosmaz(ortam, kok, capsys):
    _oz(kok)
    k = KKos()
    assert main(["uret", "u-oz", "--tur", "3"], env=ortam, kos=k, gonder=SJev()) == 2
    assert not k.claude() and "en fazla 2" in capsys.readouterr().out


def test_toplam_tavan_24_asilmaz(ortam, kok):
    _oz(kok)
    d = kok / "docs" / "denemeler" / ".kos" / "u-oz"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ayristir.json").write_text(json.dumps({"harcanan": 20}), encoding="utf-8")
    k = KKos()
    assert main(["uret", "u-oz", "--tur", "2"], env=ortam, kos=k, gonder=SJev()) != 0
    assert not k.claude()
