"""KUR-TUR2: kurulum_d2 düzeltmeleri — yarım klon (HEAD yok), seyrek SKILL klonu, bin'siz npm deposu."""
import importlib.util, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def _modul():
    sys.path.insert(0, str(KOK / "tools"))
    spec = importlib.util.spec_from_file_location("kurulum_d2_t2", KOK / "tools/kurulum_d2.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def _sahte(m, yanit):
    """run()'ı kaydeden sahte; yanit(a) -> (kod, çıktı)."""
    kayit = []
    def run(a, t=300, cwd=None, env=None):
        kayit.append(list(a)); return yanit(list(a))
    m.run = run
    return kayit


def test_yarim_klon_head_yoksa_arsive_tasinir_ve_yeniden_klonlanir(tmp_path):
    m = _modul(); m.KLON = tmp_path; m.disk_ok = lambda: True
    d = tmp_path / "a__b"; (d / ".git").mkdir(parents=True)
    def yanit(a):
        if "rev-parse" in a: return 128, "fatal: Needed a single revision"
        if "ls-remote" in a: return 0, "abc\tHEAD"
        return 0, ""
    kayit = _sahte(m, yanit)
    sonuc = m.klonla("a/b")
    assert sonuc == (d, "")
    assert any(c[:2] == ["git", "clone"] for c in kayit)
    assert list((tmp_path / "_arsiv").iterdir()), "eski yarım klon _arsiv'e taşınmalı (silinmez)"


def test_uzak_bos_ise_cozumsuz_nedeni_yazilir(tmp_path):
    m = _modul(); m.KLON = tmp_path; m.disk_ok = lambda: True
    d = tmp_path / "a__b"; (d / ".git").mkdir(parents=True)
    _sahte(m, lambda a: (128, "x") if "rev-parse" in a else (0, ""))
    d_, neden = m.klonla("a/b")
    assert d_ is None and "repo boş" in neden


def test_seyrek_ac_yalniz_skill_dizinlerini_dener(tmp_path):
    m = _modul()
    d = tmp_path / "r"; (d / ".git" / "info").mkdir(parents=True)
    liste = "README.md\nskills/a/SKILL.md\nskills/a/x.py\nother/b/SKILL.md\nbig/blob.bin\n"
    _sahte(m, lambda a: (0, liste) if "ls-tree" in a else (0, ""))
    ok, n = m.seyrek_ac(d)
    assert ok
    icerik = (d / ".git/info/sparse-checkout").read_text(encoding="utf-8").splitlines()
    assert icerik == ["/other/b/", "/skills/a/"]


def test_binsiz_npm_deposu_global_kurulmaz_ve_hata_degil_kaynak_olur(tmp_path):
    m = _modul()
    d = tmp_path / "lib"; d.mkdir(); (d / "package.json").write_text('{"name":"lib"}', encoding="utf-8")
    kayit = _sahte(m, lambda a: (1, "") if a[:2] == ["gh", "release"] else (0, ""))
    m.exe_ara = lambda k, a: ""
    durum, not_ = m.gh_cli_kur(d, "o/lib", "lib")
    assert not any("-g" in c for c in kayit), "bin yoksa npm i -g çalışmamalı"
    assert durum == "KURULDU-KAYNAK" and "bin" in not_


def test_pyproject_python_paketi_degilse_release_yoluna_duser_ve_hata_korunur(tmp_path):
    m = _modul()
    d = tmp_path / "go-repo"; d.mkdir(); (d / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    kayit = _sahte(m, lambda a: (1, "") if a[:2] == ["gh", "release"] else (0, ""))
    m.exe_ara = lambda k, a: ""
    m.uv_zincir = lambda src, ad, spec=False: ("HATA", "uv tool: Multiple top-level packages")
    durum, not_ = m.gh_cli_kur(d, "o/podman", "Podman")
    assert any(c[:2] == ["gh", "release"] for c in kayit), "release yolu denenmeli"
    assert durum == "HATA" and "Multiple top-level" in not_


def test_karar_kurallari_plugin_komut_ve_sinif_duzeltme(tmp_path):
    sys.path.insert(0, str(KOK / "tools"))
    spec = importlib.util.spec_from_file_location("kurulum_tur2_t", KOK / "tools/kurulum_tur2.py")
    t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    p = tmp_path / "plg"; (p / ".claude-plugin").mkdir(parents=True); (p / ".claude-plugin/marketplace.json").write_text("{}", encoding="utf-8")
    c = tmp_path / "cmd"; (c / ".claude/commands").mkdir(parents=True); (c / ".claude/commands/a.md").write_text("x", encoding="utf-8")
    x = lambda **k: dict({"neden": "skill-yok", "dizin_turu": "npm-bin", "kalem": "k", "kaynak": "gh:o/r", "sinif": "SKILL", "not": ""}, **k)
    assert t.karar(x(), {"yol": str(p)})[0] == "PLUGIN"
    assert t.karar(x(), {"yol": str(c)})[0] == "KOMUT"
    assert t.karar(x(), {"yol": ""})[:2] == ("D2", "CLI")
    assert t.karar(x(dizin_turu="py"), {"yol": ""})[:2] == ("D2", "PAKET")
    assert t.karar(x(kalem="systemd", neden="yolu-yok", sinif="CLI"), {"yol": ""})[0] == "COZUMSUZ"
