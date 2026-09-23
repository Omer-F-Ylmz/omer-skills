"""20b-devam K6: aday raporunda token etiketli her özellik için `## Mekanizma` altında `### <slug>` (nasıl · neden · koşul · bizde) zorunlu; rapor-denetle arar."""
from video.cli import main

from test_video import ortam  # noqa: F401  (ortam fixture)

ADAY = """# Aday: x
## Ne
araç
## Özellikler
### sikistir
ne: bağlamı sıkıştırır
etiket: token
karar: DENE
### panel
ne: panel
etiket: -
karar: RED
"""
MEK = """## Mekanizma
### sikistir
nasıl: araç çıktısını özetler, aslı hash ile saklanır
neden: tekrarlı çıktı girdi tokenını şişirir
koşul: kısa oturumda kazanç yok
bizde: headroom · girdi −%10
"""


def test_token_ozelliginde_mekanizma_yoksa_basarisiz(ortam, tmp_path, capsys):
    y = tmp_path / "x.md"
    y.write_text(ADAY, encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    assert "sikistir: ## Mekanizma yok" in capsys.readouterr().out


def test_mekanizma_alani_eksikse_basarisiz(ortam, tmp_path, capsys):
    y = tmp_path / "x.md"
    y.write_text(ADAY + MEK.replace("koşul: kısa oturumda kazanç yok\n", ""), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    assert "sikistir: Mekanizma koşul eksik" in capsys.readouterr().out


def test_mekanizma_tamsa_gecer_token_olmayan_aranmaz(ortam, tmp_path, capsys):
    y = tmp_path / "x.md"
    y.write_text(ADAY + MEK, encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    assert "GEÇTİ" in capsys.readouterr().out
