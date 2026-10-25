"""JEV-2: suz() adayları kart seçicisiyle göreve göre daraltır; fail-open."""
from jev import skill


def test_suz_ilgiliyi_one_alir_ve_dilimi_asmaz():
    aday = [(f"zz-{i:04d}", "x") for i in range(500)] + [("tailwindcss", "x"), ("departman-frontend", "x")]
    out = skill.suz("react bileşeni yaz, tailwind ile tasarla", aday, ust=50)
    ad = [a for a, _ in out]
    assert len(out) <= 50 and "tailwindcss" in ad and "departman-frontend" in ad


def test_suz_fail_open(monkeypatch):
    import arac_ara
    monkeypatch.setattr(arac_ara, "ara", lambda *a, **k: (_ for _ in ()).throw(RuntimeError))
    aday = [("a", "x"), ("b", "y")]
    assert skill.suz("x", aday) == aday
