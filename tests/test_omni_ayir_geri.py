import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "onay"))
import omni_ayir_geri  # noqa: E402


def test_plan_yalniz_yeni_comboyu_siler_sapani_raporlar():
    yedek = {"cc-yedek-dis": {"models": [{"id": "***", "m": "a"}]}, "eski": '{"models": ["b"]}'}  # yedek maskeli
    canli = {"cc-yedek-dis": '{"models":[{"id": "uzun-kimlik", "m": "a"}]}', "eski": '{"models": ["c"]}', "cc-ucuz-free": '{"models": []}'}
    assert omni_ayir_geri.plan(yedek, canli) == (["cc-ucuz-free"], ["eski"])  # biçim farkı sapma sayılmaz
    assert omni_ayir_geri.plan({"x": {"m": "***"}}, {"x": '{"m": {"k": 1}}'}) == ([], [])
    assert omni_ayir_geri.plan({"x": {"m": ["a"]}}, {"x": '{"m": ["a", "b"]}'}) == ([], ["x"])
