"""17 derin inceleme: İDDİALAR · özellik düzeyi karar · UYARLA · token varsayılan DENE (K4 kanıt) · lisans T1/T2 · telemetri · iddia sınama · brief."""
import json
from datetime import date
from pathlib import Path

from video import kur, tarama as tr, uygula as uy
from video.cli import main

from test_tarama import rapor
from test_uygula import UKos, calis, gun, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


def ozellikli(kok, ad, *oz, lisans="MIT", ek=""):
    govde = "".join(f"### {o['slug']}\n" + "".join(f"{k}: {v}\n" for k, v in o.items() if k != "slug") for o in oz)
    y = kok / "docs" / "kurulumlar" / "adaylar" / f"{ad}.md"
    y.write_text(f"# {ad}\nad: {ad}\ntur: CLI\nvideo: {VID}\nlisans: {lisans}\n## Ne\ndeneme aracı\n## Özellikler\n{govde}{ek}", encoding="utf-8")
    return y


def kayit(kok):
    y = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    return {k["ad"]: k for k in map(json.loads, y.read_text(encoding="utf-8").splitlines())}


def uygula_raporu(kok):
    return (kok / "docs" / "kurulumlar" / f"{date.today().isoformat()}-uygula.md").read_text(encoding="utf-8")


# --- K1 ---

def test_iddialar_zorunlu():
    assert tr.denetle(rapor(), 300) == []
    assert "bölüm eksik: ## İddialar" in tr.denetle(rapor(iddialar=""), 300)


def test_iddia_turu_denetlenir():
    h = tr.denetle(rapor(iddialar="## İddialar\n| iddia | zaman | tür |\n|---|---|---|\n| hızlı | 1:40 | övgü |"), 300)
    assert any("iddia türü geçersiz" in x for x in h)


# --- K3 · K4 ---

def test_ozellikler_ayri_kayit_ve_uyarla(ortam, kok):
    (kok / "tools").mkdir()
    (kok / "tools" / "x.py").write_text("print(1)\n", encoding="utf-8")
    once = {p: p.read_bytes() for p in kok.rglob("*") if p.is_file()}
    y = ozellikli(kok, "arac",
                  {"slug": "fikir", "ne": "özet çıkarır", "etiket": "-", "karar": "UYARLA", "fikir": "rapor özeti", "hedef": "tools/video",
                   "etki": "kısa rapor", "kapsam": "yalnız rapor"},
                  {"slug": "sikistir", "ne": "girdi sıkıştırır", "etiket": "token", "karar": "DENE", "metrik": "doğruluk"})
    assert calis(ortam, [y], UKos()) == 0
    k = kayit(kok)
    assert {"arac/fikir", "arac/sikistir"} <= set(k)
    assert k["arac/fikir"]["yargi"] == "UYARLA" and k["arac/fikir"]["ozellik"] == "fikir" and k["arac/fikir"]["aday"] == "arac"
    u = (kok / "docs" / "uyarlamalar" / "arac-fikir.md").read_text(encoding="utf-8")
    assert "rapor özeti" in u and "tools/video" in u and "kısa rapor" in u and "yalnız rapor" in u
    degisen = [p for p in kok.rglob("*") if p.is_file() and once.get(p) != p.read_bytes()]
    assert all(p.relative_to(kok).parts[0] == "docs" for p in degisen), degisen
    assert "token" in tr.bolum((kok / "docs" / "denemeler" / "arac-sikistir.md").read_text(encoding="utf-8"), "Metrik")


def test_token_gerekcesiz_red_dene(ortam, kok):
    y = ozellikli(kok, "arac", {"slug": "kisa", "etiket": "token", "karar": "RED", "gerekce": "hoşuma gitmedi"})
    calis(ortam, [y], UKos())
    k = kayit(kok)["arac/kisa"]
    assert k["yargi"] == "DENE" and "K4" in k["gerekce"]
    assert (kok / "docs" / "denemeler" / "arac-kisa.md").is_file()


def test_olcum_kaniti_yoksa_dene(ortam, kok):
    y = ozellikli(kok, "arac", {"slug": "kisa", "etiket": "token", "karar": "RED", "gerekce": "ölçüm: docs/denemeler/yok-sonuc.md"})
    calis(ortam, [y], UKos())
    k = kayit(kok)["arac/kisa"]
    assert k["yargi"] == "DENE" and "K4: kanıt bulunamadı" in k["gerekce"]


def test_olcum_kaniti_varsa_red_kalir(ortam, kok):
    (kok / "docs" / "denemeler").mkdir(parents=True)
    (kok / "docs" / "denemeler" / "caveman-sonuc.md").write_text("# sonuç\n", encoding="utf-8")
    y = ozellikli(kok, "arac", {"slug": "kisa", "etiket": "token", "karar": "RED",
                                "gerekce": "ölçüm: docs/denemeler/caveman-sonuc.md maliyet +%7.7"})
    calis(ortam, [y], UKos())
    assert kayit(kok)["arac/kisa"]["yargi"] == "RED"
    assert not (kok / "docs" / "denemeler" / "arac-kisa.md").exists()


def test_zaten_var_katalogda_yoksa_dene(ortam, kok):
    y = ozellikli(kok, "arac", {"slug": "kisa", "etiket": "token", "karar": "RED", "gerekce": "zaten var: hayaletarac"})
    calis(ortam, [y], UKos())
    k = kayit(kok)["arac/kisa"]
    assert k["yargi"] == "DENE" and "K4: kanıt bulunamadı" in k["gerekce"]


# --- K6 ---

def test_bsl_t2_lisans_notu_t1_red():
    a = {"tur": "CLI", "lisans": "BSL-1.1", "son_commit": gun(10), "arsiv": "hayır"}
    kt, g = uy.sinifla(a, date.today())
    assert kt == "T2" and "lisans notu" in g
    assert uy.sinifla({**a, "tur": "skill"}, date.today(), [], 0)[0] == "RED"


def test_telemetri_kapatma_zorunlu():
    m = "# x\ntelemetri: açık\n## Kurulum\n- npm: x\n## Duman testi\n- komut: x --version\n## Geri alma\n- npm: x\n"
    assert any("Telemetri" in h for h in kur.bicim(m)[1])
    assert not any("Telemetri" in h for h in kur.bicim(m + "## Telemetri kapatma\n- x telemetry off\n")[1])


# --- K5 · K7 ---

SINAMA = """## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| girdi −%33 | https://github.com/o/r | abartılı | yazar ölçümü | k1 |
| kaynaksız iddia | - | doğru | yok | - |
| geçersiz | https://x.y | harika | yok | - |
"""


def test_iddia_sinama_bicimi():
    satir, h = uy.iddia_sinama(SINAMA)
    assert [s["sonuc"] for s in satir] == ["abartılı", "doğrulanamadı", "doğrulanamadı"]
    assert any("kaynaksız" in x for x in h) and any("sonuç geçersiz" in x for x in h)


def test_rapor_sinama_kart_notu_ve_ikinci_gorus(ortam, kok):
    (kok / "bilgi").mkdir()
    (kok / "bilgi" / "k1.md").write_text("---\niddia: x\n---\nx\n", encoding="utf-8")
    y = ozellikli(kok, "arac", {"slug": "kisa", "etiket": "-", "karar": "UYARLA", "fikir": "f", "hedef": "h", "etki": "e", "kapsam": "k"}, ek=SINAMA)
    calis(ortam, [y], UKos())
    r = uygula_raporu(kok)
    assert "## İDDİA SINAMA" in r and "## ÖZELLİK KARARLARI" in r
    assert r.rstrip().endswith("## Desktop ikinci görüş")
    assert "abartılı" in (kok / "bilgi" / "k1.md").read_text(encoding="utf-8")


def test_brief_60_satir(ortam, tmp_path, capsys):
    r = tmp_path / "r.md"
    r.write_text("# video-uygula\n\n## İDDİA SINAMA\n| iddia | kaynak | sonuç | not |\n|---|---|---|---|\n"
                 + "".join(f"| iddia {i} | https://x.y/{i} | doğru | n |\n" for i in range(100))
                 + "\n## ÖZELLİK KARARLARI\n" + "".join(f"- a/o{i} → DENE — g\n" for i in range(50)) + "\n## Desktop ikinci görüş\n", encoding="utf-8")
    assert main(["brief", str(r)], env=ortam) == 0
    out = capsys.readouterr().out.splitlines()
    assert 0 < len(out) <= 60 and any("a/o0 → DENE" in s for s in out) and any("iddia 0" in s for s in out)
