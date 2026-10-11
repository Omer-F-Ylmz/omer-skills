# KALİTE-V1: "İz sebebi geçersiz" DUR'u kapanışta otomatik düzelir (anlam kanıt hücresinde kalır); düzeltilemeyen eskisi gibi DUR
from test_m2a import V, _ns
from test_m2b import _actx, _kos_sahte, _parti, _rapor

from video import parti as pt
from video import tarama as tr

IZ = "## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n"


def test_ic_ice_parantez_sadelesir():
    g, n = tr.iz_duzelt(IZ + "| kare 0:05 | maske | aday değil: başka adayın parçası (Inpaint (v3)) | maske fırçası |\n")
    assert n == 1 and "| aday değil: başka adayın parçası (Inpaint v3) | maske fırçası |" in g
    assert not any(h.startswith("İz sebebi") for h in tr.denetle(g))


def test_izinsiz_sebep_kanita_tasinir():
    g, n = tr.iz_duzelt(IZ + "| kare 0:09 | GitHub | aday değil: konu dışı (Context7'nin sahibi kuruluş) | logo |\n"
                             "| konuşma 0:12 | X | aday değil: belirsiz, model doğrulanamadı | - |\n")
    assert n == 2
    assert "| aday değil: konu dışı | logo [sebep: konu dışı (Context7'nin sahibi kuruluş)] |" in g
    assert "| aday değil: genel kavram | [sebep: belirsiz, model doğrulanamadı] |" in g
    assert not any(h.startswith("İz sebebi") for h in tr.denetle(g))


def test_uzun_alinti_kisalir():
    uzun = " ".join(f"k{i}" for i in range(20))
    g, n = tr.iz_duzelt(f'## Özet\nanlatıcı "{uzun}" dedi\n')
    assert n == 1 and '"' + " ".join(f"k{i}" for i in range(15)) + '…"' in g
    assert not any(h.startswith("alıntı") for h in tr.denetle(g))


def test_gecerli_satira_dokunmaz():
    m = IZ + ("| kare 0:05 | a | aday değil: başka adayın parçası (Seedance 2.5) | x |\n| açıklama | b | aday değil: sponsor/reklam | y |\n"
              "| kare 0:06 | c | Hızlı Araç | z |\n## Özet\nbu (konu dışı (x)) İz dışında | aday değil: belirsiz | kalır\n")
    assert tr.iz_duzelt(m) == (m, 0)


def test_crlf_korunur():
    g, n = tr.iz_duzelt((IZ + "| kare 0:05 | m | aday değil: başka adayın parçası (Inpaint (v3)) | f |\n").replace("\n", "\r\n"))
    assert n == 1 and g.count("\r\n") == g.count("\n") == 4 and "(Inpaint v3)" in g


def test_kapat_iz_sebebini_duzeltip_surer(tmp_path, capsys):
    p = _parti(tmp_path, "2026-09-29-short", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    rap = tmp_path / "docs" / "video-tarama" / f"2026-09-29-{V[0]}.md"
    eski = rap.read_text(encoding="utf-8")
    rap.write_text(eski.replace("## İz\n", "## İz\n| kare 0:05 | maske | aday değil: başka adayın parçası (Inpaint (v3)) | fırça |\n", 1)
                   if "## İz\n" in eski else eski + "\n" + IZ + "| kare 0:05 | maske | aday değil: başka adayın parçası (Inpaint (v3)) | fırça |\n",
                   encoding="utf-8")
    assert any(h.startswith("İz sebebi") for h in tr.denetle(rap.read_text(encoding="utf-8")))
    kos, _ = _kos_sahte(False)
    assert pt.parti(_ns("kapat", p.name), {**_actx(tmp_path, None), "kos": kos}) == 0
    assert "kapat: İz/alıntı biçimi düzeltildi: 1 satır" in capsys.readouterr().out
    assert "başka adayın parçası (Inpaint v3)" in rap.read_text(encoding="utf-8")
