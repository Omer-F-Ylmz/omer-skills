"""CALISTIR-2: tools/calistir_hepsi.py yeni işleyiciler (tür tespiti, ENGEL-*, SKILL-KURULDU, modül adı, ZAYIF)."""
import importlib.util
import os
import shutil
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "tools" / "calistir_hepsi.py"
spec = importlib.util.spec_from_file_location("calistir_hepsi", SRC)
ch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ch)


def mk(tmp_path, files):
    for rel, txt in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    return str(tmp_path)


# ---- tür tespiti: gerçek doküman = yalnız md/txt/pdf ----
@pytest.mark.parametrize("files,primary", [
    ({"CMakeLists.txt": "project(x)"}, "cmake"),
    ({"Makefile": "all:"}, "make"),
    ({"Gemfile": "source 'x'"}, "ruby"),
    ({"x.gemspec": ""}, "ruby"),
    ({"pom.xml": "<project/>"}, "java"),
    ({"build.gradle": ""}, "java"),
    ({"a.csproj": "<Project/>"}, "dotnet"),
    ({"Package.swift": ""}, "swift"),
    ({"a.xcodeproj/project.pbxproj": ""}, "swift"),
    ({"run.sh": "echo"}, "src"),
    ({"a.c": "int x;", "b.c": "int y;", "c.h": ""}, "src"),
    ({"README.md": "x", "doc.txt": "y", "paper.pdf": "z"}, "doc"),
])
def test_detect_turleri(tmp_path, files, primary):
    d = mk(tmp_path, files)
    assert ch.detect(d)[2] == primary


def test_mevcut_turler_oncelikli(tmp_path):
    d = mk(tmp_path, {"package.json": "{}", "CMakeLists.txt": ""})
    assert ch.detect(d)[2] == "npm"


def test_gercek_dokuman_sayilir(tmp_path):
    assert ch.real_doc(mk(tmp_path, {"a.md": "x", "img/a.png": "x"}))
    assert not ch.real_doc(mk(tmp_path / "b", {"a.md": "x", "x.c": "", "y.c": "", "z.c": ""}))


# ---- araç eksik -> ENGEL-DERLEYICI + araç adı ----
def test_eksik_arac_engel(tmp_path, monkeypatch):
    monkeypatch.setattr(ch.shutil, "which", lambda n: None)
    d = mk(tmp_path, {"Gemfile": "x"})
    c = ch.Ctx(d, d, {})
    assert ch.do_ruby(c) is False
    assert c.status[0] == "ENGEL-DERLEYICI" and "ruby" in c.status[1]


def test_swift_platform(tmp_path, monkeypatch):
    monkeypatch.setattr(ch.shutil, "which", lambda n: None)
    monkeypatch.setattr(ch.sys, "platform", "win32")
    d = mk(tmp_path, {"Package.swift": ""})
    c = ch.Ctx(d, d, {})
    assert ch.do_swift(c) is False
    assert c.status[0] == "ENGEL-PLATFORM" and "swift" in c.status[1]


def test_cmake_eksik_paket_adi():
    out = 'CMake Error at x.cmake:1 (find_package):\n  Could not find a package configuration file provided by "Qt5"\n'
    assert ch.cmake_missing(out) == "Qt5"
    assert ch.cmake_missing("-- Could NOT find ZLIB (missing: ZLIB_LIBRARY)") == "ZLIB"
    assert ch.cmake_missing("ok") == ""


def test_derleyici_baslik_eksik():
    assert ch.missing_header("a.c:1:10: fatal error: mach/mach.h: No such file or directory") == "mach/mach.h"
    assert ch.missing_header("fine") == ""


def test_kabuk_betigi_sozdizimi(tmp_path):
    if not ch.bash():
        pytest.skip("bash yok")
    d = mk(tmp_path, {"a.sh": "echo ok\n"})
    c = ch.Ctx(d, d, ch.child_env())
    assert ch.do_src(c) is True
    d2 = mk(tmp_path / "b", {"a.sh": "if then fi (\n"})
    c2 = ch.Ctx(d2, d2, ch.child_env())
    assert ch.do_src(c2) is False


# ---- modül adı: dist-info top_level / RECORD, import adı -> pip adı ----
def test_dist_modules_top_level(tmp_path):
    d = mk(tmp_path, {"top_level.txt": "bs4\n"})
    assert ch.dist_modules(d) == ["bs4"]


def test_dist_modules_record(tmp_path):
    d = mk(tmp_path, {"RECORD": "bs4/__init__.py,sha,1\nbs4/x.py,sha,1\nbeautifulsoup4-1.dist-info/METADATA,,\n"})
    assert ch.dist_modules(d) == ["bs4"]


def test_dist_modules_namespace(tmp_path):
    d = mk(tmp_path, {"RECORD": "google/protobuf/__init__.py,,\ngoogle/protobuf/a.py,,\nprotobuf-1.dist-info/RECORD,,\n"})
    assert ch.dist_modules(d) == ["google.protobuf"]


def test_dist_modules_tek_dosya(tmp_path):
    d = mk(tmp_path, {"RECORD": "six.py,,\n../../Scripts/x.exe,,\n"})
    assert ch.dist_modules(d) == ["six"]


@pytest.mark.parametrize("imp,pip", [("serial", "pyserial"), ("cv2", "opencv-python"), ("yaml", "pyyaml"),
                                     ("grpc", "grpcio"), ("PIL", "pillow"), ("sklearn", "scikit-learn"),
                                     ("bs4", "beautifulsoup4"), ("google.protobuf", "protobuf")])
def test_import_pip_adi(imp, pip):
    assert ch.import_to_pip(imp) == pip


def test_import_pip_bilinmeyen():
    assert ch.import_to_pip("zzz_yok_modul") is None


def test_modnf_siniflandir():
    r = ch.classify_modnf("Traceback...\nModuleNotFoundError: No module named 'qgis'")
    assert r[0] == "ENGEL-BAGIMLILIK" and "qgis" in r[1]
    assert ch.classify_modnf("boom") is None


# ---- SKILL-KURULDU ----
def test_skill_kur_cakisma_onek(tmp_path):
    repo = tmp_path / "owner__repo"
    mk(repo, {"a/SKILL.md": "---\nname: foo\ndescription: d\n---\n", "LICENSE": "MIT License\nPermission"})
    dest = tmp_path / "skills"
    (dest / "a").mkdir(parents=True)
    (dest / "a" / "keep.txt").write_text("eski")
    got = ch.install_skills(str(repo), str(dest))
    assert got == ["owner__repo-a"]
    assert (dest / "owner__repo-a" / "SKILL.md").exists()
    assert (dest / "a" / "keep.txt").read_text() == "eski"  # silme/ezme yok


def test_skill_lisans_kapisi(tmp_path):
    repo = tmp_path / "r"
    mk(repo, {"a/SKILL.md": "---\nname: foo\ndescription: d\n---\n"})
    assert ch.license_kind(str(repo)) == ""
    mk(repo, {"LICENSE": "Apache License\nVersion 2.0"})
    assert ch.license_kind(str(repo)) == "apache"
    assert ch.license_kind(str(mk(tmp_path / "x", {"LICENSE.md": "MIT License"}))) == "mit"
    assert ch.license_kind(str(mk(tmp_path / "y", {"LICENSE": "GNU GENERAL PUBLIC LICENSE"}))) == "other"


def test_heavy_nvidia_ml_py_agir_degil(tmp_path):
    assert ch.heavy(mk(tmp_path / "a", {"requirements.txt": "nvidia-ml-py\nrequests\n"})) == ""
    assert ch.heavy(mk(tmp_path / "b", {"requirements.txt": "nvidia-cudnn-cu12\n"})) == "nvidia-cudnn-cu12"
    assert ch.heavy(mk(tmp_path / "c", {"requirements.txt": "torch>=2\n"})) == "torch"


def test_derleme_engeli_arac_adi():
    assert "MSVC" in ch.classify_build("error: Microsoft Visual C++ 14.0 or greater is required")[1]
    assert "pg_config" in ch.classify_build("Error: could not determine PostgreSQL version")[1]
    assert "0.13.0" in ch.classify_build("error: Required uv version `>=0.13.0` does not match the running version")[1]
    assert ch.classify_build("all good") is None


# ---- ZAYIF ----
@pytest.mark.parametrize("kanit,weak", [
    ("[py] rc=0 (çıktı yok)", True),
    ("", True),
    ("kurulum tamam; çalıştırılacak giriş yok", True),
    ("build tamam; exe yok (kütüphane)", True),
    ("go build tamam; kök paket main değil", True),
    ("[py] usage: tool [-h]", False),
    ("import bs4 ok", False),
])
def test_zayif(kanit, weak):
    assert ch.is_weak({"durum": "CALISTI", "kanit": kanit}) is weak


def test_zayif_yalniz_calisti():
    assert ch.is_weak({"durum": "HATA", "kanit": ""}) is False


# ---- CALISTIR-3: pnpm yolu, 80 GB taban, ağır-ml ----
def test_taban_80gb_ve_pnpm_deposu():
    assert ch.MIN_FREE == 80e9
    assert ch.PNPM_STORE == r"C:\Projeler\_araclar\pnpm-store"


def test_pnpm_komutlari_kilitsiz(tmp_path):
    d = mk(tmp_path, {"package.json": "{}"})
    cmds = ch.pnpm_cmds(d)
    assert len(cmds) == 1
    assert cmds[0][:2] == ["pnpm.cmd", "install"]
    for f in ("--prefer-offline", "--no-frozen-lockfile", "--config.strictDepBuilds=false", "--store-dir", ch.PNPM_STORE):
        assert f in cmds[0]


@pytest.mark.parametrize("lock", ["package-lock.json", "yarn.lock"])
def test_pnpm_komutlari_kilitli_import(tmp_path, lock):
    d = mk(tmp_path, {"package.json": "{}", lock: ""})
    cmds = ch.pnpm_cmds(d)
    assert cmds[0][:2] == ["pnpm.cmd", "import"] and cmds[1][:2] == ["pnpm.cmd", "install"]


def test_pnpm_kilidi_varsa_import_yok(tmp_path):
    d = mk(tmp_path, {"package.json": "{}", "package-lock.json": "", "pnpm-lock.yaml": ""})
    assert [c[1] for c in ch.pnpm_cmds(d)] == ["install"]


def test_nm_link_istatistik(tmp_path):
    a = tmp_path / "store" / "a.bin"
    a.parent.mkdir()
    a.write_bytes(b"x" * 1000)
    nm = tmp_path / "nm"
    nm.mkdir()
    os.link(a, nm / "a.bin")
    (nm / "solo.bin").write_bytes(b"y" * 500)
    s = ch.nm_link_stats(str(nm))
    assert s["dosya"] == 2 and s["bagli"] == 1
    assert s["gorunur_bayt"] == 1500 and s["kopya_bayt"] == 500


def test_platform_engeli(tmp_path):
    d = mk(tmp_path, {"requirements.txt": "torch\nvllm>=0.5\ndeepspeed\nflash-attn\nnumpy\n"})
    assert ch.platform_block(d) == ["deepspeed", "flash-attn", "vllm"]
    assert ch.platform_block(mk(tmp_path / "b", {"requirements.txt": "torch\n"})) == []


def test_agir_req_suzgeci():
    txt = "numpy\ntorch>=2\n# c\ntorchvision==0.1\nrequests\n-e git+x\nnvidia-cudnn-cu12\ntransformers\n"
    assert ch.filter_req(txt) == ["numpy", "requests", "transformers"]


def test_agir_kur_disk_bekle(monkeypatch):
    monkeypatch.setattr(ch, "disk_ok", lambda: False)
    assert ch.agir_kur() == "DISK-BEKLE"


def test_tekrar_sunucu_ayakta_kaldi():
    assert ch.tekrar_rc({"kanit": "[py] [ayakta kaldı (sunucu/uzun süreli) 90s]"}, 124) == 0
    assert ch.tekrar_rc({"kanit": "import piper ok"}, 124) == 124
    assert ch.tekrar_rc({"kanit": "x"}, 1) == 1


# ---- (d) tekrar: ayakta kalan komut ana koşuyla aynı sınıflanır ----
def test_ayakta_kaldi_timeout_rc0():
    rc, out = ch.ayakta_kaldi(124, "Jev: http://127.0.0.1:8766\n[zaman aşımı 90s]")
    assert rc == 0 and "ayakta kaldı" in out


def test_ayakta_kaldi_gercek_hata_degismez():
    assert ch.ayakta_kaldi(1, "boom")[0] == 1
    assert ch.ayakta_kaldi(124, "zaman aşımı (öğe bütçesi bitti)")[0] == 124


def test_tekrar_ayakta_kalani_ayni_sayar(tmp_path, monkeypatch):
    tsv = tmp_path / "calistirma.tsv"
    monkeypatch.setattr(ch, "OUT", str(tmp_path))
    monkeypatch.setattr(ch, "read_rows", lambda p: [dict(durum="CALISTI", calistirma_kmt="x --help", yol="Y", rc="0")])
    monkeypatch.setattr(ch, "child_env", lambda: {})
    monkeypatch.setattr(ch, "run", lambda cmd, cwd, env, t: (124, "srv\n[zaman aşımı %ds]" % t))
    import types
    ch.tekrar(types.SimpleNamespace(tekrar=1))
    assert "True" in (tmp_path / "calistirma-tekrar.tsv").read_text(encoding="utf-8")


# ---- (a) kodlu repo DOKUMAN kalmaz: gevşek .py/.js, examples/ altı, alt klasör Dockerfile ----
@pytest.mark.parametrize("files,primary", [
    ({"a.py": "x = 1\n"}, "src"),
    ({"sub/b.js": "var x = 1;\n"}, "src"),
    ({"examples/a.py": "x = 1\n"}, "src"),
    ({"docs/a.py": "x = 1\n", "README.md": "# hi"}, "src"),
    ({"sub/Dockerfile": "FROM scratch\n"}, "docker"),
    ({"README.md": "# hi", "a.pdf": "x", "n.txt": "x"}, "doc"),
])
def test_kodlu_repo_dokuman_degil(tmp_path, files, primary):
    assert ch.detect(mk(tmp_path, files))[2] == primary


def test_do_src_python_sozdizimi(tmp_path):
    d = mk(tmp_path, {"a.py": "print('ok')\n"})
    assert ch.do_src(ch.Ctx(d, d, ch.child_env())) is True
    d2 = mk(tmp_path / "b", {"a.py": "def (:\n"})
    assert ch.do_src(ch.Ctx(d2, d2, ch.child_env())) is False


def test_do_src_js_sozdizimi(tmp_path):
    if not shutil.which("node"):
        pytest.skip("node yok")
    d = mk(tmp_path, {"a.js": "var x = 1;\n"})
    assert ch.do_src(ch.Ctx(d, d, ch.child_env())) is True
