"""K15: arsiv.md'deki (eski DEVAM-KURALI.md) her kural satırı is-akisi SKILL.md'de Lnn etiketiyle yer alır — kural silinmez."""
import re
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "skills" / "is-akisi"
BASLIK = {19, 29}  # "HER İŞTE ÇALIŞMA BİÇİMİ" ve "DEVAM KURALI" giriş satırları: kural değil, başlık/gerekçe


def test_her_kural_etiketli():
    kurallar = {i for i, s in enumerate((D / "arsiv.md").read_text(encoding="utf-8").splitlines(), 1) if s.strip()} - BASLIK
    etiket = {int(n) for n in re.findall(r"\bL(\d+)\b", (D / "SKILL.md").read_text(encoding="utf-8"))}
    assert kurallar - etiket == set()
    assert etiket - kurallar == set()
