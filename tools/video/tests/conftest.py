import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK), str(KOK.parent / "jev")]


@pytest.fixture(autouse=True)
def agsiz(monkeypatch):
    """Testler ağa çıkmaz: sahte `gonder` verilmeyen Jev çağrısı bağlanamaz (JevHata)."""
    from jev import cekirdek as c

    def yok(*a, **k):
        raise OSError("test: ağ yok")
    monkeypatch.setattr(c, "http_gonder", yok)
