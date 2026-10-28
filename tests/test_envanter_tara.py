import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import altin_ornek as ao  # noqa: E402
import envanter_tara as et  # noqa: E402


def test_aday_kumesi_aile_ve_cok_yonlu():
    m = "\n".join(et.birlestir(".NET API", 130))
    assert "departman-backend-dotnet" in m and "dn-webapi-endpoint" in m and "çok yönlüler" in m
    assert len(m.splitlines()) <= 140


def test_secim_oku_adim_arac_neden(tmp_path):
    f = tmp_path / "s.txt"
    f.write_text("1 · skill:gitleaks · sır\n2 · a + b · x\n", encoding="utf-8")
    assert ao.secim_oku(f) == ["gitleaks", "a", "b"]
