# VİDEO-AKIL-1b-2a DEVAM-1: paket "## Açıklama" — düz metin; URL ve chapter satırları çıkar (başka bölümde var), ≤600 tk
from pathlib import Path

from video.cli import main
from test_c3 import OcrKos
from test_video import VID, onbellek, ortam  # noqa: F401

ACIKLAMA = """Topview'ü keşfedip Claude ve GPT ile böyle etkili web siteler yapmak istiyorsanız Topview'ü buradan inceleyebilirsiniz:
https://www.topview.ai/?via=dlws

Bu video Topview sponsorluğunda üretilmiştir.

Bu videoda Claude, GPT Astra, Fable ve Seedance 2.5 kullanarak Awwwards tarzı bir web sitesi hazırladım.

00:00 Giriş
01:23 Referans Görselleri Bulma
11:57 - Web Sitesinin Mobil Görünümü
13:40 Bitiş

#topview #claude #seedance25"""


def test_paket_aciklama_bolumu(ortam):
    onbellek(ortam, [], duration=600, description=ACIKLAMA)
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=OcrKos({}), uyku=lambda s: None) == 0
    md = (Path(ortam["VIDEO_CACHE"]) / VID / "paket.md").read_text(encoding="utf-8")
    ac = md.split("## Açıklama\n")[1].split("\n## ")[0]
    assert "sponsorluğunda" in ac and "Seedance 2.5" in ac and "#topview" in ac
    assert "http" not in ac and "00:00" not in ac and "Referans Görselleri" not in ac and "11:57" not in ac
