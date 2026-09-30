"""MOTOR-M10: _yaz kilit yeniden denemesi · bilinmeyen son_commit SOR · kurulu her yolda ZATEN VAR · OLASI TEKRAR aynı repo ister."""
import json
from datetime import date

import pytest
from test_m2c import PID, _aday, _panel

from video import akil
from video import parti as pt
from video import uygula as uy


# K1 antivirüs/dizinleyici geçici kilidi (WinError 5): kısa beklemeyle yeniden dener
def test_k1_yaz_kilitte_yeniden_dener(tmp_path, monkeypatch):
    gercek, n = pt.os.replace, []

    def sahte(a, b):
        n.append(1)
        if len(n) < 3:
            raise PermissionError(13, "Erişim engellendi")
        gercek(a, b)
    monkeypatch.setattr(pt.os, "replace", sahte)
    monkeypatch.setattr("time.sleep", lambda s: None)
    pt._yaz(y := tmp_path / "durum.json", {"a": 1})
    assert len(n) == 3 and json.loads(y.read_text(encoding="utf-8"))["a"] == 1


def test_k1_yaz_kilit_kalkmazsa_acik_hata(tmp_path, monkeypatch):
    (y := tmp_path / "durum.json").write_text('{"a": 0}', encoding="utf-8")

    def sahte(a, b):
        raise PermissionError(13, "Erişim engellendi")
    monkeypatch.setattr(pt.os, "replace", sahte)
    monkeypatch.setattr("time.sleep", lambda s: None)
    with pytest.raises(SystemExit, match="devam"):
        pt._yaz(y, {"a": 1})
    assert json.loads(y.read_text(encoding="utf-8"))["a"] == 0


# K2 bilinmeyen son_commit RED değil SOR (last30days benzeri: MIT + son_commit yok)
@pytest.mark.parametrize("tur", ["skill", "CLI"])
@pytest.mark.parametrize("sc", [{}, {"son_commit": "yok"}, {"son_commit": None}])
def test_k2_bilinmeyen_son_commit_sor(tur, sc):
    k, g = uy.sinifla({"tur": tur, "lisans": "MIT", "arsiv": "hayır", **sc}, date.today())
    assert k == "SOR" and "eksik: son_commit" in g


# K3 kurulu aday alt tür / eşdeğer p ne olursa olsun ZATEN VAR + karşılaştırma kümesinde
def test_k3_kurulu_her_yolda_zaten_var(tmp_path):
    (pdir := tmp_path / ".kos" / PID).mkdir(parents=True)
    d = {"parti": PID, "videolar": {}, "adaylar": {
        "supabase-cli": _aday("supabase-cli", kurulu="supabase", esdeger_p=0.3, durum="kurulu"),
        "github-cli": _aday("github-cli", kurulu="gh", durum="kurulu")}}
    akil.panel(pdir, d, tmp_path)
    r, _ = _panel(tmp_path)
    for k, a in d["adaylar"].items():
        assert r[k][5] == "ZATEN VAR" and "araştırılmadı (kurulu)" in r[k][6] and akil._karsilastir(a)


# K4 ad benzerliği tek başına tekrar değil; aynı repo tekrar
def test_k4_olasi_tekrar_ayni_repo_ister(tmp_path):
    (a := tmp_path / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    (a / "claude-usage.md").write_text("# claude-usage\nad: claude-usage\ntur: CLI\nrepo: ryoppippi/ccusage\n", encoding="utf-8")
    (a / "claude-mem.md").write_text("# claude-mem\nad: claude-mem\ntur: CLI\nrepo: thedotmack/claude-mem\n", encoding="utf-8")
    (pdir := tmp_path / ".kos" / PID).mkdir(parents=True)
    d = {"parti": PID, "videolar": {}, "adaylar": {
        "claude-agents": _aday("claude-agents"), "claude-memx": _aday("claude-memx", repo="thedotmack/claude-mem")}}
    akil.panel(pdir, d, tmp_path)
    t = _panel(tmp_path)[1].split("## OLASI TEKRAR", 1)[1].split("##", 1)[0]
    assert "claude-agents" not in t and "claude-memx ≈ claude-mem" in t
