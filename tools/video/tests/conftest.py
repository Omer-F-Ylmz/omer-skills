import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK), str(KOK.parent / "jev")]


@pytest.fixture(autouse=True)
def agsiz(monkeypatch):
    """Testler ağa çıkmaz: sahte `gonder` verilmeyen Jev çağrısı bağlanamaz (JevHata)."""
    import urllib.error
    from jev import cekirdek as c
    from video import getir as gt

    def yok(*a, **k):
        raise OSError("test: ağ yok")
    monkeypatch.setattr(c, "http_gonder", yok)

    def sayfa_yok(u):  # B2: sahte okuyucu verilmeyen paket derinliği ağa çıkmaz
        raise urllib.error.URLError("test: ağ yok")
    monkeypatch.setattr(gt, "_al", sayfa_yok)
    monkeypatch.setattr(gt, "uyku", lambda s: None)  # B3 eki: gh arama aralığı/oran sınırı beklemesi testte gerçek uyumaz
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    from video import parti as pt
    monkeypatch.setattr(pt, "YONLENDIRME", {})  # O78: yeni parti A taşıyıcısıyla açılır; V10 testleri rotayı kendisi verir
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: None, raising=False)  # O78: OmniRoute ön kontrolü ağa çıkmaz  # B4 eki: anahtar verilmeyen testte brave adımı ağa çıkmaz
