"""AJAN-AKIS-1: ucuz/Haiku/Sonnet ajanlarına giren iş-akışı çekirdeği — tek kaynak tools/ajan_cekirdek.md (## cekirdek, ## zor).
onek(zor=False) → çekirdek (+ zor bölümü); prompt önekinde sabit metin = cache isabeti. Opus ajanına EKLENMEZ (model_gerek)."""
from pathlib import Path

DOSYA = Path(__file__).resolve().parent / "ajan_cekirdek.md"


def bolum(ad):
    metin = DOSYA.read_text(encoding="utf-8")
    return metin.split(f"## {ad}\n", 1)[1].split("\n## ", 1)[0].strip()


def model_gerek(model):
    """Çekirdek yalnız haiku|sonnet|ücretsiz (None/diğer) modele; opus'a değil (zaten bu düzeyde, boşa jeton)."""
    return model not in ("opus", "fable")


def onek(zor=False):
    return bolum("cekirdek") + "\n\n" + (bolum("zor") + "\n\n" if zor else "")
