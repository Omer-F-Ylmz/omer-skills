"""DERİNLİK-1: araştırma kapsamı — R2 sınıf ne olursa olsun repo araştırılır · R3 repo araması · R5 kapsam · R6 --yeniden · R1 güncellik · R4 yorum/kare."""
import json

from test_m2a import V, _ns
from test_m2b import _parti, _rapor
from test_m2c import Ar, _ctx, _jev, _panel

from video import parti as pt

PID = "2026-10-03-short"


# R2 servis/ürün sınıfı reposu varsa normal araştırmadan geçer (eskiden arac_degil → atlanıyordu)
def test_r2_servis_repolu_arastirilir(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("harness-audit", "servis", "https://github.com/ornek/harness-audit")])})
    ar = Ar({"harness-audit": {"alt_tur": "araç"}})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, ar, _jev("servis")))
    assert "harness-audit" in ar.adlar
    assert json.loads((p / "durum.json").read_text(encoding="utf-8"))["adaylar"]["harness-audit"]["durum"] == "tamam"


# R2 paket içi parça kurulu paketteki karşılığıyla eşleşir; dosya yolu panelde
def test_r2_paket_ici_eslesir(tmp_path):
    evi = tmp_path / "evi"
    s = evi / "plugins" / "cache" / "everything-claude-code" / "1.0" / "skills" / "harness-audit"
    s.mkdir(parents=True)
    (s / "SKILL.md").write_text("---\nname: harness-audit\n---\n", encoding="utf-8")
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("harness-audit (ECC içinde)", "skill", None)])})
    c = _ctx(tmp_path, Ar({}))
    c["env"]["CLAUDE_EVI"] = str(evi)
    pt.parti(_ns("akil", p.name), c)
    _, t = _panel(tmp_path, PID)
    assert "paket içi: " in t and "everything-claude-code/1.0/skills/harness-audit" in t
