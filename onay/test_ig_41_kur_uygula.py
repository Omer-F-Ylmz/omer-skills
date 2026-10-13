"""ig_41_kur_uygula: SkillSpector kapısı, sha256 denetimi, geri alma (ev dizini tmp)."""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ig_41_kur_uygula as m


def sahte_ss(issues):
    def kos(*a, cwd=None):
        Path(a[a.index("--output") + 1]).write_text(json.dumps({"issues": issues}), encoding="utf-8")
        return subprocess.CompletedProcess(a, 0, "", "")
    return kos


def test_ss_kapisi_incelenen_gecer_yeni_high_durdurur(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "kos", sahte_ss([{"id": "AE1", "severity": "HIGH"}, {"id": "X9", "severity": "LOW"}]))
    assert m.ss_gecer("anatomy", tmp_path)[0]
    monkeypatch.setattr(m, "kos", sahte_ss([{"id": "AE1", "severity": "HIGH"}, {"id": "E2", "severity": "CRITICAL"}]))
    gecer, neden = m.ss_gecer("anatomy", tmp_path)
    assert not gecer and "E2" in neden
    assert not m.ss_gecer("hairline-create", tmp_path)[0]  # anatomy'nin INCELENDI'si başka skill'e geçmez


def test_ss_cikti_yoksa_kurulmaz(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "kos", lambda *a, cwd=None: subprocess.CompletedProcess(a, 1, "", ""))
    assert m.ss_gecer("anatomy", tmp_path) == (False, "skillspector çıktısı yok")


def test_ek_dosyalar_bilinen_skille_ait():
    assert set(m.EK) <= {ad for _, _, ad in m.SKILL}


def test_sha(tmp_path):
    f = tmp_path / "a.zip"
    f.write_bytes(b"x")
    assert m.sha_tamam(f, "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881")
    assert not m.sha_tamam(f, "0" * 64)


def test_geri_yalniz_eklenenleri_alir_plugin_jsonu_doner(monkeypatch, tmp_path):
    monkeypatch.setattr(m, "kos", lambda *a, cwd=None: subprocess.CompletedProcess(a, 0, "", ""))
    sk, pj, y = tmp_path / ".claude" / "skills", tmp_path / ".claude" / "plugins", m.yedek(tmp_path)
    for d in (sk / "anatomy", sk / "onceden", pj, y):
        d.mkdir(parents=True)
    (pj / "installed_plugins.json").write_text("yeni", encoding="utf-8")
    (y / "installed_plugins.json").write_text("eski", encoding="utf-8")
    m.bildirim(tmp_path).write_text(json.dumps([["skill", "anatomy"], ["plugin-guncel", "p@q", str(tmp_path / "yok")]]),
                                    encoding="utf-8")
    assert m.geri(tmp_path)
    assert not (sk / "anatomy").exists() and (sk / "onceden").exists()
    assert (pj / "installed_plugins.json").read_text(encoding="utf-8") == "eski"
    assert not m.bildirim(tmp_path).exists()
