import importlib.util
from pathlib import Path

_s = importlib.util.spec_from_file_location("k25", Path(__file__).resolve().parents[2] / "onay" / "kapi_25_uygula.py")
k25 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(k25)


def test_repo_havuzunda_bes_kabul_ajani_var():
    assert [a for a, _ in k25.plan()] == k25.KABUL


def test_kabul_ajanlari_kurulur_ve_geri_alinir(tmp_path):
    kok, ev = tmp_path / "kok", tmp_path / "ev"
    (kok / "ajanlar" / "kalite3" / "oyun-mod").mkdir(parents=True)
    for ad in k25.KABUL:
        (kok / "ajanlar" / "kalite3" / "oyun-mod" / f"{ad}.md").write_text(f"---\nname: {ad}\n---\nyeni\n", encoding="utf-8")
    (kok / "ajanlar" / "kalite3" / "oyun-mod" / "ajn-skill-yazar.md").write_text("ret\n", encoding="utf-8")
    (ev / ".claude" / "agents").mkdir(parents=True)
    eski = ev / ".claude" / "agents" / "fe-form-tasarimci.md"
    eski.write_text("eski\n", encoding="utf-8")
    assert k25.uygula(ev, kok)
    assert all((ev / ".claude" / "agents" / f"{a}.md").read_text(encoding="utf-8").endswith("yeni\n") for a in k25.KABUL)
    assert not (ev / ".claude" / "agents" / "ajn-skill-yazar.md").exists()  # RET kurulmaz
    assert k25.geri(ev)
    assert eski.read_text(encoding="utf-8") == "eski\n"
    assert not (ev / ".claude" / "agents" / "oyn-oyun-envanter.md").exists()  # önceden yoktu → geri alınca yok
