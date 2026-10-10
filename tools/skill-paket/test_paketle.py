import sys, zipfile, pathlib
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import paketle as P
import ekle as E


def skill(kok, ad, ekler=(), aciklama="Örnek açıklama"):
    d = pathlib.Path(kok) / ad
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: \"{aciklama}\"\n---\n# {ad}\n", encoding="utf-8")
    for yol, icerik in ekler:
        f = d / yol
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(icerik, encoding="utf-8")
    return d


def adlar(zp):
    return zipfile.ZipFile(zp).namelist()


def test_tek_skillmd_ve_talimat(tmp_path):
    a = skill(tmp_path / "k", "a1")
    b = skill(tmp_path / "k", "b1")
    zp, n = P.paketle("deneme-paket", "konu", [a, b], tmp_path / "o")
    L = adlar(zp)
    assert [x for x in L if x.split("/")[-1].lower() == "skill.md"] == ["deneme-paket/SKILL.md"]
    assert "deneme-paket/skills/a1/TALIMAT.md" in L and "deneme-paket/skills/b1/TALIMAT.md" in L
    assert n == 3


def test_derin_skillmd_ornek_olur(tmp_path):
    a = skill(tmp_path / "k", "a1", [("ornek/SKILL.md", "x"), ("SKILL.md.bak", "y")])
    zp, _ = P.paketle("deneme-paket", "konu", [a], tmp_path / "o")
    L = adlar(zp)
    assert "deneme-paket/skills/a1/ornek/SKILL-ornek.md" in L
    assert sum(1 for x in L if x.split("/")[-1].lower() == "skill.md") == 1


def test_200_sinirinda_referans_birlesir(tmp_path):
    a = skill(tmp_path / "k", "a1", [(f"r/{i}.md", f"icerik{i}") for i in range(250)])
    zp, n = P.paketle("deneme-paket", "konu", [a], tmp_path / "o")
    assert n <= 200
    z = zipfile.ZipFile(zp)
    ref = z.read("deneme-paket/skills/a1/REFERANS.md").decode()
    assert "## [r/249.md]" in ref and "icerik249" in ref


def test_birlestirmeye_ragmen_asilirsa_valueerror(tmp_path):
    kaynak = [skill(tmp_path / "k", f"s{i}") for i in range(201)]
    with pytest.raises(ValueError):
        P.paketle("deneme-paket", "konu", kaynak, tmp_path / "o")


@pytest.mark.parametrize("ad", ["claude-paket", "x-Anthropic-y"])
def test_adda_claude_yasak(tmp_path, ad):
    with pytest.raises(ValueError):
        P.paketle(ad, "konu", [skill(tmp_path / "k", "a1")], tmp_path / "o")


def test_aciklama_siniri(tmp_path):
    with pytest.raises(ValueError):
        P.paketle("deneme-paket", "u" * 300, [skill(tmp_path / "k", "a1")], tmp_path / "o")


def test_cli(tmp_path):
    a = skill(tmp_path / "k", "a1")
    assert P.main(["deneme-paket", "konu", str(tmp_path / "o"), str(a)]) == 0
    assert (tmp_path / "o" / "deneme-paket.zip").is_file()


def _temel(tmp_path):
    a = skill(tmp_path / "k", "a1", [("ref.md", "ESKI-ICERIK")])
    zp, _ = P.paketle("deneme-paket", "konu", [a], tmp_path / "o")
    return zp


def test_ekle_yeni_skill_eskiyi_korur(tmp_path):
    zp = _temel(tmp_path)
    eski = zipfile.ZipFile(zp).read("deneme-paket/skills/a1/ref.md")
    yeni = skill(tmp_path / "k2", "c1")
    yzp, n = E.ekle(zp, [yeni], tmp_path / "o2")
    z = zipfile.ZipFile(yzp)
    assert z.read("deneme-paket/skills/a1/ref.md") == eski
    assert "deneme-paket/skills/c1/TALIMAT.md" in z.namelist()
    md = z.read("deneme-paket/SKILL.md").decode()
    assert "`skills/a1/TALIMAT.md`" in md and "`skills/c1/TALIMAT.md`" in md
    assert "2 skill'lik paket (konu)" in md
    assert sum(1 for x in z.namelist() if x.split("/")[-1].lower() == "skill.md") == 1


def test_ekle_cakisma_hata(tmp_path):
    zp = _temel(tmp_path)
    with pytest.raises(ValueError, match="a1"):
        E.ekle(zp, [skill(tmp_path / "k2", "a1")], tmp_path / "o2")


def test_ekle_uzerine_degistirir(tmp_path):
    zp = _temel(tmp_path)
    yeni = skill(tmp_path / "k2", "a1", [("ref2.md", "YENI")])
    yzp, _ = E.ekle(zp, [yeni], tmp_path / "o2", uzerine=True)
    z = zipfile.ZipFile(yzp)
    L = z.namelist()
    assert "deneme-paket/skills/a1/ref.md" not in L
    assert z.read("deneme-paket/skills/a1/ref2.md") == b"YENI"
    assert z.read("deneme-paket/SKILL.md").decode().count("`skills/a1/TALIMAT.md`") == 1


def test_ekle_sinir_asilirsa_hangisi_yeniye(tmp_path):
    a = skill(tmp_path / "k", "a1")
    zp, _ = P.paketle("deneme-paket", "konu", [a], tmp_path / "o")
    kaynak = [skill(tmp_path / "k2", f"n{i:03d}") for i in range(250)]
    with pytest.raises(ValueError) as e:
        E.ekle(zp, kaynak, tmp_path / "o2")
    assert "n249" in str(e.value) and "yeni pakete" in str(e.value)
