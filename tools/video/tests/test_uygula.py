"""14a video-uygula: katman sınıflandırıcı (T0 · T1 · T2 · RED), kayıt, projeler. Ağsız; dış süreçler sahte `kos`, Jev sahte `gonder`."""
import json
import os
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pytest

from video.cli import main

from test_tarama import KuralJev
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

SHA = "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
KURAL = "# Kurallar\n\n1. Yeterli bilgi varsa harekete geç, soru sorma.\n2. Commit mesajları Türkçe yazılır.\n"
GLOBAL = "# Global\n\n\n- Env değerleri yazdırılmaz, yalnız varlık denetimi.\n"


class UKos:
    """Sahte skillspector · git · skill_denetim. Çağrıları kaydeder."""

    def __init__(self, repo=None, high=0, spector_rc=0, denetim_rc=0):
        self.repo, self.high, self.spector_rc, self.denetim_rc, self.cagri = repo, high, spector_rc, denetim_rc, []

    def __call__(self, args, timeout=None):
        args = [str(a) for a in args]
        self.cagri.append(args)
        if args[0] == "skillspector":
            if self.spector_rc:
                return self.spector_rc, b"", b"hata"
            Path(args[args.index("--output") + 1]).write_text(
                json.dumps({"issues": [{"severity": "HIGH"}] * self.high + [{"severity": "LOW"}]}), encoding="utf-8")
            return 0, b"", b""
        if args[0] == "git":
            return 0, (str(self.repo) if "--show-toplevel" in args else SHA).encode() + b"\n", b""
        if any(a.endswith("skill_denetim.py") for a in args):
            return self.denetim_rc, b"denetim", b""
        raise AssertionError(args)


@pytest.fixture
def kok(ortam, tmp_path):
    k = tmp_path / "repo"
    (k / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    kl = tmp_path / "kaynak"
    kl.mkdir()
    (kl / "omer-kurallar.md").write_text(KURAL, encoding="utf-8")
    (kl / "CLAUDE.md").write_text(GLOBAL, encoding="utf-8")
    ortam.update(VIDEO_UYGULA_KOK=str(k), VIDEO_KURALLAR=os.pathsep.join([str(kl / "CLAUDE.md"), str(kl / "omer-kurallar.md")]),
                 VIDEO_EV=str(tmp_path / "ev"))
    return k


def gun(n):
    return (date.today() - timedelta(days=n)).isoformat()


def aday(kok, ad, **alan):
    a = {"ad": ad, "tur": "skill", "video": VID, "repo": f"o/{ad}", "lisans": "MIT", "son_commit": gun(30), "arsiv": "hayır", "kaynak": "yok", **alan}
    y = kok / "docs" / "kurulumlar" / "adaylar" / f"{ad}.md"
    y.write_text(f"# {ad}\n" + "".join(f"{k}: {v}\n" for k, v in a.items()) + "## Ne\ndeneme\n## Geri alma\nnpm rm deneme\n", encoding="utf-8")
    return y


def skill_klon(tmp_path, ad, *ek):
    repo = tmp_path / "klon" / ad
    s = repo / "skills" / ad
    (s / "references").mkdir(parents=True)
    (repo / "LICENSE").write_text("MIT License", encoding="utf-8")
    (s / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: deneme\n---\n# {ad}\n", encoding="utf-8")
    (s / "references" / "a.md").write_text("ek", encoding="utf-8")
    for e in ek:
        (s / e).write_text("x", encoding="utf-8")
    return repo, s


def kayit(kok):
    y = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    return [json.loads(x) for x in y.read_text(encoding="utf-8").splitlines()] if y.is_file() else []


def calis(ortam, args, kos, gonder=None):
    return main(["katman", *map(str, args)], env=ortam, kos=kos, gonder=gonder)


def test_yalniz_md_skill_t1_zip_ve_kayitta_commit(ortam, kok, tmp_path, capsys):
    repo, s = skill_klon(tmp_path, "md-skill")
    y = aday(kok, "md-skill", kaynak=s)
    assert calis(ortam, [y], UKos(repo)) == 0
    out = capsys.readouterr().out
    hedef = kok / "skills" / "md-skill"
    assert (hedef / "SKILL.md").is_file() and (hedef / "references" / "a.md").is_file() and (hedef / "LICENSE").is_file()
    assert SHA in (hedef / "KAYNAK.md").read_text(encoding="utf-8")
    z = kok / "dist" / "yukle-14" / "yeni" / "md-skill.zip"
    assert "md-skill/SKILL.md" in zipfile.ZipFile(z).namelist()
    k = kayit(kok)[-1]
    assert (k["ad"], k["katman"], k["kaynak_commit"]) == ("md-skill", "T1", SHA)
    assert "OTOMATİK UYGULANDI" in out and "md-skill.zip" in out


@pytest.mark.parametrize("dosya", ["kur.sh", "arac.py", "hook.js", "package.json"])
def test_script_iceren_skill_t2_onay_bekler(ortam, kok, tmp_path, capsys, dosya):
    repo, s = skill_klon(tmp_path, "scriptli", dosya)
    y = aday(kok, "scriptli", kaynak=s)
    assert calis(ortam, [y], UKos(repo)) == 0
    assert not (kok / "skills" / "scriptli").exists()
    assert not (kok / "dist" / "yukle-14" / "yeni" / "scriptli.zip").exists()
    assert (kok / "docs" / "kurulumlar" / "bekleyen" / "scriptli.md").read_text(encoding="utf-8").startswith("# ONAY scriptli")
    assert kayit(kok)[-1]["katman"] == "T2"
    assert "ONAY scriptli" in capsys.readouterr().out


def test_skillspector_high_1_red(ortam, kok, tmp_path):
    repo, s = skill_klon(tmp_path, "riskli")
    kos = UKos(repo, high=1)
    assert calis(ortam, [aday(kok, "riskli", kaynak=s)], kos) == 0
    assert any(a[0] == "skillspector" and "--no-llm" in a for a in kos.cagri)
    assert not (kok / "skills" / "riskli").exists() and not (kok / "docs" / "kurulumlar" / "bekleyen" / "riskli.md").exists()
    assert kayit(kok)[-1]["katman"] == "RED"


def test_skillspector_kosmazsa_red(ortam, kok, tmp_path):
    repo, s = skill_klon(tmp_path, "taranamaz")
    assert calis(ortam, [aday(kok, "taranamaz", kaynak=s)], UKos(repo, spector_rc=1)) == 0
    assert not (kok / "skills" / "taranamaz").exists() and kayit(kok)[-1]["katman"] == "RED"


@pytest.mark.parametrize("alan", [{"lisans": "yok"}, {"lisans": "GPL-3.0"}, {"son_commit": gun(400)}, {"arsiv": "evet"}])
def test_lisans_ya_da_bakim_red(ortam, kok, tmp_path, alan):
    repo, s = skill_klon(tmp_path, "eski")
    assert calis(ortam, [aday(kok, "eski", kaynak=s, **alan)], UKos(repo)) == 0
    assert not (kok / "skills" / "eski").exists() and kayit(kok)[-1]["katman"] == "RED"


def test_lisanssiz_plugin_de_red(ortam, kok):
    assert calis(ortam, [aday(kok, "eklenti", tur="plugin", lisans="yok")], UKos()) == 0
    assert kayit(kok)[-1]["katman"] == "RED"
    assert not (kok / "docs" / "kurulumlar" / "bekleyen" / "eklenti.md").exists()


def test_denetim_hatasi_t1_geri_alinir_t2(ortam, kok, tmp_path):
    repo, s = skill_klon(tmp_path, "bozuk")
    assert calis(ortam, [aday(kok, "bozuk", kaynak=s)], UKos(repo, denetim_rc=1)) == 0
    assert not (kok / "skills" / "bozuk").exists() and not (kok / "dist" / "yukle-14" / "yeni" / "bozuk.zip").exists()
    assert kayit(kok)[-1]["katman"] == "T2"


def kurallar(ortam):
    return [Path(p).read_text(encoding="utf-8") for p in ortam["VIDEO_KURALLAR"].split(os.pathsep)]


def test_ipucu_cift_eklenmez(ortam, kok, capsys):
    once = kurallar(ortam)
    y = aday(kok, "harekete-gec", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural="Yeterli bilgide harekete geç")
    jev = KuralJev()
    assert calis(ortam, [y], UKos(), jev) == 0
    assert kurallar(ortam) == once
    k = kayit(kok)[-1]
    assert k["katman"] == "T0" and "omer-kurallar:3" in k["karar"]
    assert len(jev.istek) <= 3  # 15 K3: tür (kural/olgu) 1 + çift 2


def test_ipucu_yeni_kural_dosyalarina_yazilmaz(ortam, kok, capsys):
    once = kurallar(ortam)
    y = aday(kok, "neden-ver", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural="İsteğin nedenini de yaz")
    assert calis(ortam, [y], UKos(), KuralJev()) == 0
    assert kurallar(ortam) == once  # 15b K1: T0 yalnız bekleyen dosyası yazar, ekleme `kural-onay` ile
    k = kayit(kok)[-1]
    assert k["katman"] == "T0" and "kural-neden-ver.md" in k["geri_alma"]
    assert "ONAY BEKLİYOR" in capsys.readouterr().out


def test_kayittaki_ad_atlanir_yeniden_ile_islenir(ortam, kok, tmp_path, capsys):
    repo, s = skill_klon(tmp_path, "gorulmus")
    (kok / "docs" / "kurulumlar" / "kayit.jsonl").write_text(json.dumps({"ad": "Gorulmus", "katman": "RED"}) + "\n", encoding="utf-8")
    y = aday(kok, "gorulmus", kaynak=s)
    kos = UKos(repo)
    assert calis(ortam, [y], kos) == 0
    assert "atlandı" in capsys.readouterr().out and not kos.cagri and len(kayit(kok)) == 1
    assert calis(ortam, [y, "--yeniden"], kos) == 0
    assert (kok / "skills" / "gorulmus").is_dir() and kayit(kok)[-1]["katman"] == "T1"


def test_projeler_ozet_uretir_mtime_ile_yeniler(ortam, kok, tmp_path, capsys):
    a, b = tmp_path / "p1", tmp_path / "p2"
    for d, metin in ((a, "# P1\n\nPortal uygulaması.\nASP.NET Core."), (b, "# P2\n\nMobil garaj.\n")):
        d.mkdir()
        (d / "CLAUDE.md").write_text(metin, encoding="utf-8")
    ortam["VIDEO_PROJELER"] = json.dumps({"Bir": str(a), "İki": str(b), "Yok": str(tmp_path / "yok")})
    assert main(["projeler"], env=ortam) == 0
    md = (kok / "docs" / "projeler.md").read_text(encoding="utf-8")
    assert "Bir: Portal uygulaması. ASP.NET Core." in md and "İki: Mobil garaj." in md and "Yok: CLAUDE.md yok" in md
    capsys.readouterr()
    assert main(["projeler"], env=ortam) == 0
    assert "güncel" in capsys.readouterr().out
    hp = kok / "docs" / "projeler.md"
    hp.write_text(hp.read_text(encoding="utf-8").replace("İki: Mobil garaj.", "İki: Elle yazılmış özet (elle)"), encoding="utf-8")
    (a / "CLAUDE.md").write_text("# P1\n\nYeni özet.\n", encoding="utf-8")
    ileri = (kok / "docs" / "projeler.md").stat().st_mtime + 10
    os.utime(a / "CLAUDE.md", (ileri, ileri))
    assert main(["projeler"], env=ortam) == 0
    md = hp.read_text(encoding="utf-8")
    assert "Bir: Yeni özet." in md and "İki: Elle yazılmış özet (elle)" in md


def test_ipucu_maddesi_satir_sonlarini_korur(ortam, kok):
    hedef = Path(ortam["VIDEO_KURALLAR"].split(os.pathsep)[1])
    y = aday(kok, "neden-ver", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural="İsteğin nedenini de yaz")
    for nl in ("\n", "\r\n"):
        hedef.write_bytes(KURAL.replace("\n", nl).encode("utf-8"))
        once = hedef.read_bytes()
        assert calis(ortam, [y, "--yeniden"], UKos(), KuralJev()) == 0
        sonra = hedef.read_bytes()
        assert sonra.startswith(once) and sonra[len(once):] == f"3. İsteğin nedenini de yaz (video {VID}, 14a){nl}".encode("utf-8")
