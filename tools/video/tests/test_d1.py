"""DERİNLİK-MASTER D1: rapor "## İz" — her bahis bir satır; "aday değil" sebebi sabit listeden, "zaten kurulu" sebep değil (29 Eyl ilkesi)."""

from video import tarama as tr

IZ = """## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 01:10 | Superpowers | superpowers | "install superpowers" |
| kare 02:00 | MCP | aday değil: genel kavram | ekranda MCP yazısı |
| açıklama | NordVPN | aday değil: sponsor/reklam | sponsor bağlantısı |
| konuşma 03:00 | brainstorm komutu | aday değil: başka adayın parçası (superpowers) | "superpowers brainstorm" |
| yorum | yemek tarifi | aday değil: konu dışı | yorum metni |
{ek}"""


def iz_hata(ek=""):
    return [x for x in tr.denetle(IZ.format(ek=ek)) if x.startswith("İz")]


def test_sabit_sebepler_gecer():
    assert iz_hata() == []


def test_zaten_kurulu_ve_liste_disi_sebep_reddedilir():
    h = iz_hata("| konuşma 04:00 | ruflo | aday değil: zaten kurulu | kurulu |\n| kare 05:00 | x | aday değil: ilginç değil | - |")
    assert len(h) == 2 and "ruflo" in h[0] and "zaten kurulu" in h[0] and "ilginç değil" in h[1]


def test_baska_adayin_parcasi_hangisi_zorunlu_bos_alan_reddedilir():
    h = iz_hata("| konuşma 04:00 | alt komut | aday değil: başka adayın parçası | - |\n| konuşma 06:00 |  | superpowers | k |")
    assert len(h) == 2 and "alt komut" in h[0]
