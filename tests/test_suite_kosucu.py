import re
from pathlib import Path

MD = Path(__file__).resolve().parents[1] / ".claude" / "agents" / "suite-kosucu.md"


def test_her_suite_komutu_sayaci_gecici_dizine_verir():
    # MÜKEMMEL-2c: suite'ler gerçek .claude/cagri-sayac.txt'yi artırmasın (K2)
    komutlar = re.findall(r"^\d\. `(.+)`$", MD.read_text(encoding="utf-8"), re.M)
    assert len(komutlar) == 6
    assert all('export CAGRI_SAYAC_DIZIN="$(mktemp -d)";' in k for k in komutlar)
