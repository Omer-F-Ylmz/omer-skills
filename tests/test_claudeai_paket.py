"""dist/yukle-9b/replace paketi: claude.ai'de 644 dosya + kabuk durumu varsayimlari."""
import re
import zipfile
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
PAKET = KOK / "dist" / "yukle-9b" / "replace"
ENV_SATIR = ('. "${GSTACK_CORE_RO:-$(ls -d /mnt/skills/*/gstack-core '
             '2>/dev/null | head -1)}/bin/gstack-env"')
BASLIK = "> **claude.ai uyarlamasi**"


@pytest.fixture(scope="module")
def skiller():
    if not PAKET.is_dir():
        pytest.fail("paket yok: %s -- once `python tools/gstack_ai.py` kosun" % PAKET)
    out = {}
    for z in sorted(PAKET.rglob("*.zip")):
        with zipfile.ZipFile(z) as zf:
            ad = zf.namelist()[0].split("/")[0]
            out[ad] = zf.read(ad + "/SKILL.md").decode("utf-8")
    assert len(out) == 55, sorted(out)
    return out


def bloklar(md):
    return re.findall(r"```bash\n(.*?)```", md, re.S)


def test_calistirilabilirlik_denetimi_kalmadi(skiller):
    kalan = [a for a, m in skiller.items() if '[ -x "$GS' in m]
    assert kalan == []


def test_islevsiz_gs_atamasi_kalmadi(skiller):
    kalan = [a for a, m in skiller.items() if 'GS="$GS"' in m]
    assert kalan == []


def test_her_gs_blogu_env_satiriyla_baslar(skiller):
    eksik, sayi = [], 0
    for ad, md in skiller.items():
        for b in bloklar(md):
            if not re.search(r"\$GS|\$B\b|\$D\b", b):
                continue
            sayi += 1
            if b.split("\n", 1)[0].strip() != ENV_SATIR:
                eksik.append(ad + ": " + b.split("\n", 1)[0][:60])
    assert sayi >= 500, sayi
    assert eksik == [], eksik[:5]


def test_uyarlama_basligi_kabuk_durumunu_anlatir(skiller):
    alt = {a: m for a, m in skiller.items() if a != "gstack-core"}
    assert len(alt) == 54
    for ad, md in alt.items():
        bas = md.split(BASLIK, 1)
        assert len(bas) == 2, ad
        bas = bas[1].split("\n\n", 1)[0]
        assert "gstack-env ayarlar" in bas, ad
        assert "Kabuk durumu bash cagrilari arasinda korunmaz" in bas, ad
        assert "Pakette yok (bun/.ts)" in bas, ad


def test_gstack_env_pakette_ve_env_satiri_onu_gosterir(skiller):
    z = next(p for p in PAKET.rglob("gstack-core.zip"))
    with zipfile.ZipFile(z) as zf:
        assert "gstack-core/bin/gstack-env" in zf.namelist()
        govde = zf.read("gstack-core/bin/gstack-env").decode("utf-8")
    assert "\r" not in govde
    assert ENV_SATIR.endswith('/bin/gstack-env"')
    kullanan = {a for a, m in skiller.items() if ENV_SATIR in m}
    gereken = {a for a, m in skiller.items()
               if any(re.search(r"\$GS|\$B|\$D", b) for b in bloklar(m))}
    assert gereken - kullanan == set()
    assert "gstack-core" in kullanan
    assert len(kullanan) >= 53, sorted(set(skiller) - kullanan)
