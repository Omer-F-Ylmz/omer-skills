"""B3: yapımcı nasıl yaptı — sürüm notları + en çok tepki alan açık/kapalı issue + discussion (sahte gh, ağ yok) on.md'ye;
gh kota/oran sınırı adayı düşürmez → kapsam.json "erisilemedi" [[istek, sebep]] (B2 gibi, tekrar yazılmaz)."""
import json

from video import getir as gt
from video import tarama as tr


def kos(args):
    a = " ".join(args)
    kos.cagri.append(a)
    if "releases" in a:
        return 0, json.dumps([{"tag_name": "v2", "html_url": "https://github.com/o/r/releases/v2", "body": "Bilinen sorun: Windows yolu.\nAyar: X=1"}]).encode(), b""
    if "is:open" in a:
        return 0, json.dumps({"items": [{"title": "Token şişmesi", "html_url": "https://github.com/o/r/issues/7", "reactions": {"total_count": 42}}]}).encode(), b""
    if "is:closed" in a:
        return 0, json.dumps({"items": [{"title": "Hook çöküyor", "html_url": "https://github.com/o/r/issues/3", "reactions": {"total_count": 9}}]}).encode(), b""
    if "graphql" in a:
        return 1, b"", b"gh: API rate limit exceeded for user (HTTP 403)"
    return 0, (b"# R" if "readme" in a else b"a/b"), b""


def test_yapimci_on_md_ve_kota_erisilemedi(tmp_path):
    kos.cagri = []
    kj = tmp_path / "kapsam.json"
    kj.write_text(json.dumps({"izleme": "tam", "incelenmedi": [], "erisilemedi": [["https://b.io", "403"]]}), encoding="utf-8")
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", "o/r", kos=kos, kapsam=kj).read_text(encoding="utf-8"), "Yapımcı nasıl yaptı")
    assert "- v2 · https://github.com/o/r/releases/v2 · Bilinen sorun: Windows yolu. Ayar: X=1" in b
    assert "- açık · Token şişmesi · tepki 42 · https://github.com/o/r/issues/7" in b and "- kapalı · Hook çöküyor · tepki 9" in b
    assert any(f"releases?per_page={gt.YAPIMCI['surum']}" in c for c in kos.cagri)
    assert sum(f"per_page={gt.YAPIMCI['issue']}" in c for c in kos.cagri) == 2 and "erişilemedi" in b and "rate limit" in b
    k = json.loads(kj.read_text(encoding="utf-8"))
    assert k["izleme"] == "tam" and k["erisilemedi"][0] == ["https://b.io", "403"] and "rate limit" in k["erisilemedi"][1][1]
    gt.on(tmp_path, "VID", "arac", "o/r", kos=kos, kapsam=kj)
    assert len(json.loads(kj.read_text(encoding="utf-8"))["erisilemedi"]) == 2  # aynı hata tekrar yazılmaz
