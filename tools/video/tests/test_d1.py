"""DERİNLİK-MASTER D1: rapor "## İz" — her bahis bir satır; "aday değil" sebebi sabit listeden, "zaten kurulu" sebep değil (29 Eyl ilkesi)."""

from pathlib import Path

from video import tarama as tr


def test_tarayici_talimati_iz_sema2():
    """D1 (b): alt ajan şablonu künyede "şema 2" ve ## İz tablosu üretir; skill gövdesi İz denetimini anar."""
    kok = Path(__file__).resolve().parents[3]
    t = (kok / ".claude" / "agents" / "video-tarayici.md").read_text(encoding="utf-8")
    assert "url · şema 2" in t and "## İz\n| kaynak | ne | bağlandığı | kanıt |" in t and "zaten kurulu" in t
    s = (kok / "skills" / "video-tarama" / "SKILL.md").read_text(encoding="utf-8")
    assert "## İz" in s and "şema 2" in s

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


def test_sema2_kunyede_iz_zorunlu_eski_sema_serbest():
    """D1 (a) (Ömer kararı, 4 Eki): İz yalnız künyesinde "şema 2" (ya da üstü) olan raporda zorunlu; eski raporlar geçerli kalır."""
    kunye = "## Künye\nBaşlık · kanal · süre: 10:00 · tr · https://youtu.be/x{}\n"
    eksik = [x for x in tr.denetle(kunye.format(" · şema 2")) if "İz" in x]
    assert eksik and "şema 2" in eksik[0]
    assert [x for x in tr.denetle(kunye.format(" · şema 3") + "## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n") if "İz" in x]
    assert not [x for x in tr.denetle(kunye.format(" · şema 2") + IZ.format(ek="")) if "İz" in x]
    assert not [x for x in tr.denetle(kunye.format("")) if "İz" in x]


def test_baska_adayin_parcasi_hangisi_zorunlu_bos_alan_reddedilir():
    h = iz_hata("| konuşma 04:00 | alt komut | aday değil: başka adayın parçası | - |\n| konuşma 06:00 |  | superpowers | k |")
    assert len(h) == 2 and "alt komut" in h[0]


def test_motor_form_iz_sema2(tmp_path):
    """D1 (b) motor: form "iz" → rapor künyede şema 2 + ## İz; iz yoksa şema 1 (eski form geçerli); boş/eksik/geçersiz İz form_red;
    model şemasında iz zorunlu; SISTEM, motor-sema.md ve haiku ajanı İz'i anar."""
    from test_m2a import V, _form
    from test_m2b import _pk
    from video import parti as pt
    pk, eski = _pk(tmp_path), _form(V[0])
    dg = lambda f: pt.dogrula({"videolar": [f]}, {V[0]: pk}, [V[0]]).get(V[0])
    assert dg(eski) is None and "şema" not in pt.rapor_md(eski, pk, [])
    iz = {"kaynak": "konuşma 0:05", "ne": "Hızlı Araç", "baglandigi": "Hızlı Araç", "kanit": "araç işi hızlandırıyor"}
    md = pt.rapor_md({**eski, "iz": [iz]}, pk, [])
    assert "· şema 2" in md and "## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n| konuşma 0:05 | Hızlı Araç | Hızlı Araç |" in md
    assert dg({**eski, "iz": [iz]}) is None
    assert dg({**eski, "iz": []}) and dg({**eski, "iz": [{**iz, "kanit": " "}]}) and dg({**eski, "iz": [{"kaynak": "yorum", "ne": "X"}]})
    assert dg({**eski, "iz": [{**iz, "baglandigi": "aday değil: zaten kurulu"}]})
    v = lambda s: s["properties"]["videolar"]["items"]["required"]
    assert "iz" in v(pt.sema([V[0]], iz=True)) and "iz" not in v(pt.sema([V[0]]))
    assert "iz" in pt.SISTEM and "zaten kurulu" in pt.SISTEM
    kok = Path(__file__).resolve().parents[3]
    assert "## İz" in (kok / ".claude" / "agents" / "video-tarayici-haiku.md").read_text(encoding="utf-8")
    assert "iz: [" in (kok / "docs" / "tasarim" / "motor-sema.md").read_text(encoding="utf-8").split("## 1.")[1].split("## 2.")[0]
