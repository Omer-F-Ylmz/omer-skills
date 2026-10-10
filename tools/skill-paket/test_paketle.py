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


# --- büyük mod (--buyuk) ---
def _buyuk_skill(tmp_path):
    return skill(tmp_path / "k", "s1", [
        ("ref.md", "REF-ICERIK"), ("notes/x.md", "NOT-ICERIK"), ("run.py", "print('KOD')"),
        ("data.json", "{}"), ("img.bin", "a\x00b"), ("dev.txt", "x" * 1_100_000)])


def test_buyuk_dosya_turleri(tmp_path):
    [(zp, _)] = P.buyuk("bb-paket", "konu", [_buyuk_skill(tmp_path)], tmp_path / "o")
    z = zipfile.ZipFile(zp)
    L = [x for x in z.namelist() if "/skills/s1/" in x]
    assert sorted(L) == ["bb-paket/skills/s1/KAYNAK-1.md", "bb-paket/skills/s1/REFERANS.md", "bb-paket/skills/s1/TALIMAT.md"]
    ref = z.read("bb-paket/skills/s1/REFERANS.md").decode()
    assert "## [ref.md]" in ref and "## [notes/x.md]" in ref and "REF-ICERIK" in ref
    assert "`img.bin`" in ref and "`dev.txt`" in ref and str(tmp_path / "k" / "s1") in ref  # ikili/büyük: liste + asıl konum
    kay = z.read("bb-paket/skills/s1/KAYNAK-1.md").decode()
    assert "### run.py" in kay and "print('KOD')" in kay and "### data.json" in kay
    assert "xxxxxxxx" not in kay + ref
    assert "REFERANS.md" in z.read("bb-paket/skills/s1/TALIMAT.md").decode()
    assert sum(1 for x in z.namelist() if x.split("/")[-1].lower() == "skill.md") == 1


def test_buyuk_ek_dosyasiz_skill_yalniz_talimat(tmp_path):
    [(zp, n)] = P.buyuk("bb-paket", "konu", [skill(tmp_path / "k", "s1")], tmp_path / "o")
    assert n == 2 and zipfile.ZipFile(zp).namelist().count("bb-paket/skills/s1/TALIMAT.md") == 1


def test_buyuk_kaynak_bolme(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "PARCA", 300)
    s = skill(tmp_path / "k", "s1", [(f"f{i}.py", "y" * 100) for i in range(5)])
    [(zp, _)] = P.buyuk("bb-paket", "konu", [s], tmp_path / "o")
    z = zipfile.ZipFile(zp)
    parcalar = sorted(x for x in z.namelist() if "KAYNAK-" in x)
    assert len(parcalar) >= 2
    toplam = "".join(z.read(x).decode() for x in parcalar)
    assert all(toplam.count(f"### f{i}.py") == 1 for i in range(5))


def test_buyuk_dengeli_bolme(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "SINIR", 12)
    kaynak = [skill(tmp_path / "k", f"s{i}", [("r.md", "x")]) for i in range(8)]
    sonuc = P.buyuk("bb-paket", "konu", kaynak, tmp_path / "o")
    assert [zp.name for zp, _ in sonuc] == ["bb-paket-1.zip", "bb-paket-2.zip"]
    assert all(n <= 12 for _, n in sonuc)
    sayi = [sum(1 for x in zipfile.ZipFile(zp).namelist() if x.endswith("/TALIMAT.md")) for zp, _ in sonuc]
    assert sayi == [4, 4]
    assert "(bölüm 1/2)" in zipfile.ZipFile(sonuc[0][0]).read("bb-paket-1/SKILL.md").decode()


def test_buyuk_zip_siniri_boler(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "BUYUK_BOYUT", 9000)
    rnd = lambda i: __import__("random").Random(i).randbytes(2000).hex()  # sıkışmayan metin ~4 KB
    kaynak = [skill(tmp_path / "k", f"s{i}", [("a.py", rnd(i))]) for i in range(4)]
    sonuc = P.buyuk("bb-paket", "konu", kaynak, tmp_path / "o")
    assert len(sonuc) == 2 and all(zp.stat().st_size <= 9000 for zp, _ in sonuc)


def test_buyuk_tek_skill_sigmazsa_valueerror(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "SINIR", 2)
    with pytest.raises(ValueError):
        P.buyuk("bb-paket", "konu", [skill(tmp_path / "k", "s1", [("r.md", "x")])], tmp_path / "o")


@pytest.mark.parametrize("ad", ["claude-paket", "x-Anthropic-y"])
def test_buyuk_adda_claude_yasak(tmp_path, ad):
    with pytest.raises(ValueError):
        P.buyuk(ad, "konu", [skill(tmp_path / "k", "a1")], tmp_path / "o")


def test_buyuk_aciklama_siniri(tmp_path):
    with pytest.raises(ValueError):
        P.buyuk("bb-paket", "u" * 300, [skill(tmp_path / "k", "a1")], tmp_path / "o")


def test_buyuk_cli(tmp_path):
    assert P.main(["--buyuk", "bb-paket", "konu", str(tmp_path / "o"), str(_buyuk_skill(tmp_path))]) == 0
    assert (tmp_path / "o" / "bb-paket.zip").is_file()
