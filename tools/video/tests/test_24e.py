"""VİDEO-PARTİ-D-DEVAM-2: `video on` ham adı slug'lar (iskelet + .kos) · kurulu araç on/araştırıcıdan önce ZATEN VAR ·
ipucu/teknik iskelete girmez. Ağsız; komutlar sahte `kos`."""
import json

from video.cli import _slug, main

from test_24c import _kos
from test_ogren import OJev
from test_uygula import UKos, calis, kayit, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

HAM = 'ekran görüntüsü + "fix this" / plugin marketplace add'


def _adaylar(kok):
    return kok / "docs" / "kurulumlar" / "adaylar"


# Slug: tırnaklı/bölülü ad tek dosya (alt klasör yok, OSError yok); `ad:` ham kalır; mevcut adlar değişmez
def test_slug_tirnakli_bolulu_ad_tek_dosya(ortam, kok):
    assert main(["on", VID, HAM, "--tur", "prompt"], env=ortam, kos=_kos()) == 0
    d = _adaylar(kok)
    assert [p.name for p in d.iterdir()] == [f"{_slug(HAM)}.md"]
    assert f"ad: {HAM}" in (d / f"{_slug(HAM)}.md").read_text(encoding="utf-8")
    assert [p.name for p in (kok / ".kos" / VID).iterdir()] == [_slug(HAM)]
    for ad in ("cm", "context-mode"):
        assert main(["on", VID, ad, "--tur", "plugin"], env=ortam, kos=_kos()) == 0
        assert (d / f"{ad}.md").is_file() and (kok / ".kos" / VID / ad / "on.md").is_file()


# Sıra: envanterde kurulu araç → ön getirme/klon/SkillSpector yok, iskelet ZATEN VAR (kurulu), katman kaydı ZATEN VAR
def test_kurulu_arac_on_ve_arastirici_yok(ortam, kok, capsys):
    (kok / "docs" / "departmanlar").mkdir(parents=True, exist_ok=True)
    (kok / "docs" / "departmanlar" / "envanter.json").write_text(json.dumps([{"ad": "taste-skill", "tur": "skill", "departman": "frontend", "aciklama": "Anti-slop frontend skill."}]), encoding="utf-8")
    kos = _kos()
    assert main(["on", VID, "taste-skill", "--repo", "o/ts", "--tur", "skill"], env=ortam, kos=kos) == 0
    assert kos.cagri == [] and not (kok / ".kos" / VID / "taste-skill" / "on.md").exists()
    assert "araştırıcı yok" in capsys.readouterr().out
    y = _adaylar(kok) / "taste-skill.md"
    m = y.read_text(encoding="utf-8")
    assert "karar: ZATEN VAR" in m and "gerekce: kurulu: taste-skill" in m and "## Özellikler" in m and "yarım" not in m
    assert calis(ortam, [y], UKos(), OJev()) == 0 and kayit(kok)[-1]["yargi"] == "ZATEN VAR"


# ipucu/teknik/iş akışı iskelete girmez (T0 yolundan geçer)
def test_ipucu_teknik_iskelete_girmez(ortam, kok):
    for tur in ("ipucu", "teknik", "iş akışı"):
        assert main(["on", VID, "context rot", "--tur", tur], env=ortam, kos=_kos()) == 2
    assert not _adaylar(kok).exists() or not any(_adaylar(kok).iterdir())
