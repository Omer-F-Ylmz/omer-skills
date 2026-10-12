"""ig_40_kur_p2_uygula: kuru değişiklik yapmaz, uygula idempotent, --geri baytları geri getirir."""
import importlib.util, shutil, sys, tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("u", KOK / "onay" / "ig_40_kur_p2_uygula.py")
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def test_dongu():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        for s, _ in u.EKLE:
            shutil.copytree(KOK / "skills" / s, t / "skills" / s)
        shutil.copytree(KOK / "tools" / "skill-paket", t / "tools" / "skill-paket")
        once = {s: u._yol(t, s).read_bytes() for s, _ in u.EKLE}
        assert not any(v for _, v in u.plan(t))
        assert u.uygula(t, ev=t) and all(v for _, v in u.plan(t))
        ilk = {s: u._yol(t, s).read_bytes() for s, _ in u.EKLE}
        assert u.uygula(t, ev=t) and ilk == {s: u._yol(t, s).read_bytes() for s, _ in u.EKLE}
        for s, satir in u.EKLE:
            m = u._yol(t, s).read_text(encoding="utf-8")
            assert m.index(satir) < m.index("<!-- profil-disi:bas -->")
        assert sorted(p.name for p in (t / "dist" / "ig-40-p2" / "kendi").glob("*.zip")) == sorted(f"{s}.zip" for s, _ in u.EKLE)
        assert u.geri(t, ev=t) and once == {s: u._yol(t, s).read_bytes() for s, _ in u.EKLE}


if __name__ == "__main__":
    test_dongu()
    print("ok")
