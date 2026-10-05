"""B4: genel web araması (aday başına en fazla N sorgu, ayarda; Agent Reach yolu = mcporter exa.web_search_exa): inceleme, karşılaştırma,
alternatif, bilinen sorun + yazarın duyuru/blog yazısı (B3'ten). Forum/sosyal "düşük güven". Sorgu hatası adayı düşürmez → erisilemedi.
Sahte kos + sahte saat; ağ yok."""
import json

import pytest

from video import getir as gt
from video import tarama as tr


@pytest.fixture
def saat(monkeypatch):
    t = [1000.0]
    monkeypatch.setattr(gt, "saat", lambda: t[0])
    monkeypatch.setattr(gt, "uyku", lambda s: t.__setitem__(0, t[0] + s))
    monkeypatch.setattr(gt, "_son", [float("-inf")])
    return t


def kos_yap(t):
    q = [s.format(ad="arac") for s in gt.SORGU]
    yanit = {q[0]: (0, json.dumps({"results": [{"title": "İnceleme", "url": "https://blog.x/r"},
                                               {"title": "Konu", "url": "https://www.reddit.com/r/a/1"},
                                               {"title": "Üçüncü", "url": "https://e.x/3"},
                                               {"title": "Fazla", "url": "https://e.x/4"}]}).encode(), b""),
             q[1]: (0, "Title: Karşı\nURL: https://c.x/k\nText: uzun\n\nTitle: İnceleme\nURL: https://blog.x/r\n".encode(), b""),
             q[2]: (1, b"", b"mcporter: timeout")}

    def kos(args):
        a = " ".join(args)
        kos.cagri.append((a, t[0]))
        if args[0] != "mcporter":
            return 0, (b"[]" if "releases" in a else b"# R"), b""
        return yanit.get(next(x[6:] for x in args if x.startswith("query=")), (0, b"[]", b""))
    kos.cagri = []
    return kos


def test_web_bolumu_sorgu_tavani_dusuk_guven_tekil(tmp_path, saat):
    kos = kos_yap(saat)
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, web=True).read_text(encoding="utf-8"), "Web araması")
    m = [a for a, _ in kos.cagri if a.startswith("mcporter call exa.web_search_exa")]
    assert len(m) == min(len(gt.SORGU), gt.WEB["sorgu"]) and all("arac" in a for a in m)
    assert any("duyuru" in s or "blog" in s for s in gt.SORGU)  # B3'ten kalan: yazarın duyuru/blog yazısı
    assert "İnceleme · https://blog.x/r" in b and b.count("https://blog.x/r") == 1  # aynı URL tek satır
    assert [s for s in b.splitlines() if "reddit.com" in s][0].endswith("düşük güven") and "https://blog.x/r · düşük güven" not in b
    assert "Karşı · https://c.x/k" in b and ("https://e.x/4" in b) == (gt.WEB["sonuc"] >= 4)  # Title:/URL: metin biçimi · sonuç tavanı


def test_sorgu_hatasi_erisilemedi_aday_dusmez(tmp_path, saat):
    kj = tmp_path / "kapsam.json"
    kj.write_text(json.dumps({"izleme": "tam", "incelenmedi": []}), encoding="utf-8")
    kos = kos_yap(saat)
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, kapsam=kj, web=True).read_text(encoding="utf-8"), "Web araması")
    q2 = gt.SORGU[2].format(ad="arac")
    assert f"- erişilemedi: web: {q2} (" in b and "timeout" in b and "https://blog.x/r" in b
    assert json.loads(kj.read_text(encoding="utf-8"))["erisilemedi"] == [[f"web: {q2}", "mcporter: timeout"]]


def test_web_istekleri_arasi_en_az_iki_sn(tmp_path, saat):
    kos = kos_yap(saat)
    gt.on(tmp_path, "VID", "arac", kos=kos, web=True)
    z = [z for a, z in kos.cagri if a.startswith("mcporter")]
    assert all(b - a >= 2 for a, b in zip(z, z[1:]))


def test_web_verilmezse_arama_yok(tmp_path, saat):
    kos = kos_yap(saat)
    y = gt.on(tmp_path, "VID", "arac", "o/r", kos=kos)
    assert not any(a.startswith("mcporter") for a, _ in kos.cagri) and "## Web araması" not in y.read_text(encoding="utf-8")
