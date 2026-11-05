"""IS6-ECC: ecc-inceleme-1105.md bulgulari icin regresyon testleri (H1-H10, O9). Bolumler '# === Hn ===' ile ayrilir."""
import json, os, sys, time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import kurulum_coz2 as K  # noqa: E402
import kurulum_eksik as KE  # noqa: E402
import sonnet_coz as S  # noqa: E402
import ucretsiz_havuz as UH  # noqa: E402


def _is(i, hazir=0):
    return {"id": i, "hazir": hazir, "tur": "ozet", "istem": "x", "max_tokens": 1, "aile": None, "haric_aile": None, "haiku_tavan": 0, "etiket": None, "zaman": 1}


@pytest.fixture
def ert(tmp_path, monkeypatch):
    monkeypatch.setattr(UH, "DIZIN", tmp_path)
    monkeypatch.setattr(UH, "ERT", tmp_path / "ertelenen.jsonl")
    monkeypatch.setattr(UH, "SONUC", tmp_path / "ertelenen-sonuc.jsonl")
    monkeypatch.setattr(UH, "_durum", lambda: {})
    return tmp_path


@pytest.fixture
def kok(tmp_path, monkeypatch):
    v = tmp_path / "v"
    v.mkdir()
    monkeypatch.setattr(K, "HEDEF", str(v))
    monkeypatch.setattr(K, "ESKI", [])
    monkeypatch.setattr(K.shutil, "disk_usage", lambda p: SimpleNamespace(free=999 * 2**30))
    return v


# === H1 ===
def _paket(monkeypatch, tmp_path, son):
    cmds = []

    def k(cmd, t=120):
        cmds.append(cmd)
        if "ls" in cmd:
            return 0, "{}", ""
        if "list" in cmd:
            return 0, "[]", ""
        return 0, "", ""
    monkeypatch.setattr(K, "k", k)
    monkeypatch.setattr(KE, "NPM_DIR", str(tmp_path / "npm"))
    monkeypatch.setattr(KE, "VENV", str(tmp_path / "venv"))
    monkeypatch.setattr(KE, "kayit", lambda d: None)
    monkeypatch.setattr(KE, "yaz", lambda *a: None)
    KE.paket_bolum(son, {})
    return cmds


def test_h1_npm_install_prefix_alir(monkeypatch, tmp_path):
    cmds = _paket(monkeypatch, tmp_path, {"v": {"a": "npm:left-pad"}})
    ins = [c for c in cmds if "install" in c]
    assert ins and "--prefix" in ins[0] and ins[0][ins[0].index("--prefix") + 1] == str(tmp_path / "npm")


# === H2 ===
def _canli(pid):
    import subprocess
    return str(pid) in subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout


def test_h2_zaman_asimi_torunu_oldurur(tmp_path):
    pf = str(tmp_path / "pid.txt")
    torun = tmp_path / "torun.py"
    torun.write_text(f"import os,time\nopen({pf!r},'w').write(str(os.getpid()))\ntime.sleep(40)\n", encoding="utf-8")
    kod = ("import subprocess,sys,time,os\n"
           f"subprocess.Popen([sys.executable,{str(torun)!r}])\n"
           f"[time.sleep(0.2) for _ in range(100) if not os.path.exists({pf!r})]\n"
           "time.sleep(90)")
    t0 = time.time()
    rc, o, e = K.k([sys.executable, "-c", kod], 8)
    assert rc == -2 and "TIMEOUT" in e and time.time() - t0 < 25
    pid = int(Path(pf).read_text())
    time.sleep(0.5)
    assert not _canli(pid)


def test_h2_stdin_devnull_git_istem_kapali():
    rc, o, e = K.k([sys.executable, "-c", "import os,sys;print(os.environ.get('GIT_TERMINAL_PROMPT'), repr(sys.stdin.read()))"], 20)
    assert o.strip() == "0 ''"


def test_o9_arac_yok_ayirt_edilir():
    rc, o, e = K.k(["yok-boyle-bir-arac-xyz"], 5)
    assert rc == -3 and "ARAC-YOK" in e


# === H3 ===
@pytest.mark.parametrize("rc,hata,beklenen", [(1, "gh: Not Found (HTTP 404)", "REPO-YOK"), (1, "gh: API rate limit exceeded (HTTP 403)", "GH-HATA"), (-3, "ARAC-YOK", "GH-HATA"), (-2, "TIMEOUT", "GH-HATA")])
def test_h3_gh_hatasi_repo_yok_degil(kok, monkeypatch, rc, hata, beklenen):
    monkeypatch.setattr(K, "k", lambda cmd, t=120: (rc, "", hata))
    assert K.indir_repo("o/r")["durum"] == beklenen


# === H4 ===
def test_h4_gecici_durumlar_tekrar_denenir(kok, tmp_path, monkeypatch):
    coz, toplu = tmp_path / "coz.jsonl", tmp_path / "toplu.jsonl"
    coz.write_text(json.dumps({"video": "v1", "kaynak": "sonnet", "eslesme": {"foo": "gh:o/r", "bar": "gh:o/done"}, "kanit": {"foo": "raporda", "bar": "raporda"}}) + "\n", encoding="utf-8")
    toplu.write_text("".join(json.dumps(d) + "\n" for d in ({"repo_istenen": "o/r", "durum": "INDIRME-HATA"}, {"repo_istenen": "o/done", "durum": "INDIRILDI"})), encoding="utf-8")
    monkeypatch.setattr(K, "COZ", str(coz)); monkeypatch.setattr(K, "TOPLU", str(toplu))
    cagrilan = []
    monkeypatch.setattr(K, "indir_repo", lambda full: cagrilan.append(full) or {"repo": full, "durum": "INDIRILDI"})
    K.indir()
    assert cagrilan == ["o/r"]


# === H5 ===
def test_h5_yarim_klon_birakilmaz(kok, monkeypatch):
    def k(cmd, t=120):
        if cmd[0] == "gh":
            return 0, "o/r\t10\tMIT\t5\n", ""
        os.makedirs(os.path.join(cmd[-1], ".git"))  # yarim klon
        return -2, "", "TIMEOUT"
    monkeypatch.setattr(K, "k", k)
    assert K.indir_repo("o/r")["durum"] == "INDIRME-HATA"
    assert not (kok / "o__r").exists() and not (kok / "o__r.tmp").exists()
    assert K.zaten_var("o", "r") is None


def test_h5_zaten_var_bos_klasor_sayilmaz(kok, tmp_path, monkeypatch):
    eski = tmp_path / "eski"
    (eski / "o__r").mkdir(parents=True)
    monkeypatch.setattr(K, "ESKI", [str(eski)])
    (kok / "o__r" / ".git").mkdir(parents=True)
    assert K.zaten_var("o", "r") is None
    (kok / "o__r" / ".git" / "HEAD").write_text("ref: refs/heads/main")
    assert K.zaten_var("o", "r") == str(kok / "o__r")


# === H6 ===
def test_h6_adim_rc_sifir_degilse_durur(tmp_path, monkeypatch):
    monkeypatch.setattr(S, "LOG", str(tmp_path / "l.log")); monkeypatch.setattr(S, "yaz", lambda *a: None)
    monkeypatch.setattr(S.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=3))
    with pytest.raises(SystemExit) as e:
        S.adim("INDIR", ["x.py"])
    assert e.value.code == 3


def test_h6_adim_zaman_asimi_var(tmp_path, monkeypatch):
    kw_ = {}
    monkeypatch.setattr(S, "LOG", str(tmp_path / "l.log")); monkeypatch.setattr(S, "yaz", lambda *a: None)
    monkeypatch.setattr(S.subprocess, "run", lambda *a, **kw: kw_.update(kw) or SimpleNamespace(returncode=0))
    S.adim("INDIR", ["x.py"])
    assert kw_.get("timeout")


# === H7 ===
def test_h7_nihai49_ertele_calisir(ert, monkeypatch):
    monkeypatch.setattr(UH, "_nihai49_katman", lambda t, z: "sonnet")
    monkeypatch.setattr(UH, "_claude_cagir", lambda *a, **k: (None, "claude/opus", ["x"]))
    monkeypatch.setattr(UH, "_sec", lambda *a, **k: None)
    y, k, log = UH.cagir("ozet", "istem", ertele="is-1")
    assert y is None and "ertelendi" in log
    assert UH.ERT.exists() and "is-1" in UH.ERT.read_text(encoding="utf-8")


@pytest.mark.parametrize("kw", [{"haric_aile": "anthropic"}, {"aile": "groq"}])
def test_h7_nihai49_aile_kisitina_uyar(ert, monkeypatch, kw):
    cagrilar = []
    monkeypatch.setattr(UH, "_nihai49_katman", lambda t, z: "sonnet")
    monkeypatch.setattr(UH, "_claude_cagir", lambda *a, **k: cagrilar.append(1) or ("yanit", "claude/sonnet", []))
    monkeypatch.setattr(UH, "_sec", lambda *a, **k: None)
    UH.cagir("ozet", "istem", **kw)
    assert not cagrilar


# === H8 ===
def test_h8_plan_limiti_yanit_sayilmaz(monkeypatch, tmp_path):
    monkeypatch.setenv("TEMP", str(tmp_path))
    monkeypatch.setattr(UH.subprocess, "run", lambda *a, **kw: SimpleNamespace(returncode=0, stdout="You've reached your usage limit, resets at 5pm", stderr=""))
    m, k, log = UH._claude_cagir("opus", "x", 100, 10, None, None)
    assert m is None and any("plan-limiti" in l for l in log)


# === H9 ===
def test_h9_tekrar_istisnada_is_kaybolmaz(ert, monkeypatch):
    UH.ERT.write_text("".join(json.dumps(_is(i)) + "\n" for i in ("a0", "a1")), encoding="utf-8")

    def cagir(*a, **k):
        raise RuntimeError("boom")
    monkeypatch.setattr(UH, "cagir", cagir)
    try:
        UH.tekrar()
    except RuntimeError:
        pass
    ids = [json.loads(l)["id"] for l in UH.ERT.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert sorted(ids) == ["a0", "a1"]


def test_h9_isleniyor_kalintisi_ezilmez(ert):
    ara = UH.ERT.with_suffix(".isleniyor")
    ara.write_text(json.dumps(_is("old", time.time() + 1000)) + "\n", encoding="utf-8")
    UH.ERT.write_text(json.dumps(_is("new", time.time() + 1000)) + "\n", encoding="utf-8")
    UH.tekrar()
    ids = [json.loads(l)["id"] for l in UH.ERT.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert sorted(ids) == ["new", "old"]


# === H10 ===
def test_h10_pypi_npm_bayrak_adi_ve_sdist(monkeypatch, tmp_path):
    cmds = _paket(monkeypatch, tmp_path, {"v": {"a": "pypi:--user", "b": "pypi:requests", "c": "npm:--prefix", "d": "npm:left-pad"}})
    assert not any("--user" in c for c in cmds)
    pip = [c for c in cmds if "pip" in c and "install" in c]
    assert pip and "--only-binary=:all:" in pip[0] and pip[0][-2] == "--" and pip[0][-1] == "requests"
    npm = [c for c in cmds if c[0] == "npm.cmd" and "install" in c]
    assert len(npm) == 1 and npm[0][-2:] == ["--", "left-pad"]
