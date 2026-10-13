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


def test_git_bash_git_kurulumundan_bulunur(monkeypatch, tmp_path):
    (tmp_path / "Git" / "cmd").mkdir(parents=True)
    (tmp_path / "Git" / "bin").mkdir()
    (tmp_path / "Git" / "bin" / "bash.exe").write_bytes(b"")
    monkeypatch.setattr(m.shutil, "which", lambda ad: str(tmp_path / "Git" / "cmd" / "git.exe") if ad == "git" else None)
    assert m.git_bash() == str(tmp_path / "Git" / "bin" / "bash.exe")


def test_kos_bash_git_bashi_kullanir_yoksa_cokmez(monkeypatch):
    cagri = []
    monkeypatch.setattr(m.subprocess, "run", lambda a, **k: cagri.append(a) or subprocess.CompletedProcess(a, 0, "", ""))
    monkeypatch.setattr(m, "git_bash", lambda: r"X:\Git\bin\bash.exe")
    m.kos("bash", "./setup")
    assert cagri[-1][0] == r"X:\Git\bin\bash.exe"
    monkeypatch.setattr(m, "git_bash", lambda: None)
    assert m.kos("bash", "./setup").returncode != 0 and len(cagri) == 1


def _sahte_plan(monkeypatch, kos):
    monkeypatch.setattr(m, "kos", kos)
    monkeypatch.setattr(m, "kurulu_uv", lambda: {})
    monkeypatch.setattr(m, "kurulu_npm", lambda: set())


def test_gstack_guncel_head_origin_main_esitse(monkeypatch, tmp_path):
    (tmp_path / ".git").mkdir()
    monkeypatch.setattr(m, "GSTACK", tmp_path)
    uzak = {"v": "abc"}
    _sahte_plan(monkeypatch, lambda *a, cwd=None: subprocess.CompletedProcess(
        a, 0, "abc\n" if "rev-parse" in a else uzak["v"] + "\trefs/heads/main\n" if "ls-remote" in a else "", ""))
    gst = lambda: [k for t, _, k in m.plan(tmp_path) if t == "gstack-guncel"][0]
    assert gst()
    uzak["v"] = "def"
    assert not gst()
    _sahte_plan(monkeypatch, lambda *a, cwd=None: subprocess.CompletedProcess(a, 128, "", ""))
    assert not gst()  # repo/ağ yoksa güncel sayılmaz


def test_bildirim_cokuste_de_yazilir(monkeypatch, tmp_path):
    def kos(*a, cwd=None):
        if a[0] == "bash":
            raise FileNotFoundError("bash")
        return subprocess.CompletedProcess(a, 0, "onceki\n" if "rev-parse" in a else "", "")
    monkeypatch.setattr(m, "kos", kos)
    hepsi = ([("plugin", a) for _, a in m.PLUGIN] + [("npm", a) for a in m.NPM] + [("skill", a) for *_, a in m.SKILL]
             + [("zip", z[0]) for z in m.ZIP] + [("uv-guncel", a) for a in m.UV_GUNCEL])
    monkeypatch.setattr(m, "plan", lambda ev: [(t, a, True) for t, a in hepsi] + [("gstack-guncel", str(m.GSTACK), False)])
    try:
        m.uygula(tmp_path)
    except FileNotFoundError:
        pass
    assert json.loads(m.bildirim(tmp_path).read_text(encoding="utf-8")) == [["gstack-guncel", "onceki"]]
