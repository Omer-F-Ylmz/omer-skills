"""MOTOR-M3a K0: kuyruksuz kapat · izlenmeyen docs dosyası (motor klasörleri) · teknik_duzenle idempotent · eylem zorunlu."""
import subprocess

from video import akil


def _git(kok, *a):
    return subprocess.run(["git", "-C", str(kok), *a], capture_output=True, text=True, check=True).stdout


def _repo(tmp_path):
    kok = tmp_path / "r"
    (kok / "docs").mkdir(parents=True)
    _git(kok, "init", "-q")
    _git(kok, "config", "user.email", "t@t")
    _git(kok, "config", "user.name", "t")
    (kok / "docs" / "a.md").write_text("a\n", encoding="utf-8")
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "ilk")
    return kok


def _ctx():
    def kos(args, timeout=300):
        if args[0] == "gitleaks" or "push" in args:
            return 0, b"", b""
        p = subprocess.run(args, capture_output=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    return {"kos": kos, "env": {}}


def _yaz(kok, yol):
    y = kok / yol
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text("x\n", encoding="utf-8")


def _d():
    return {"parti": "p1", "videolar": {}, "adaylar": {}}  # yapay parti: "kuyruk" anahtarı yok


def test_k0a_kuyruksuz_parti_kapanir(tmp_path):
    kok = _repo(tmp_path)
    _yaz(kok, "docs/kurulumlar/parti/p1/panel.md")
    assert akil.kapat(tmp_path, _d(), kok, _ctx()) == 0
    assert "docs/kurulumlar/parti/p1/panel.md" in _git(kok, "show", "--name-only", "HEAD")


def test_k0a_izlenmeyen_docs_motor_klasoru_alinir_kapsam_disi_alinmaz(tmp_path, capsys):
    kok = _repo(tmp_path)
    _yaz(kok, "docs/denemeler/yeni.md")
    _yaz(kok, "docs/baska/disari.md")
    assert akil.kapat(tmp_path, _d(), kok, _ctx()) == 0
    assert "docs/denemeler/yeni.md" in _git(kok, "show", "--name-only", "HEAD")
    assert "?? docs/baska/" in _git(kok, "status", "--porcelain")
    out = capsys.readouterr().out
    assert "docs/denemeler/yeni.md" in out and "disari" not in out  # commit'ten önce listelenir


FRONTEND = """# Frontend

## Teknikler
- Cam kart · backdrop-filter blur · video abc 1:00 · kaynak: altyazı · bizde yok
- cam kart · aynı teknik · video def 2:10 · kaynak: kare
- GSAP ScrollTrigger pin · sahne sabitlenir · video abc 3:00 · kaynak: altyazı (kontrol edilmedi)
- Mavi başlık · video def 0:05 · kaynak: kare

## Sonra
- dokunulmaz
"""


def test_k0b_teknik_duzenle_idempotent(tmp_path):
    y = tmp_path / "docs" / "departmanlar" / "frontend.md"
    y.parent.mkdir(parents=True)
    y.write_bytes(FRONTEND.encode("utf-8"))
    akil.teknik_duzenle(tmp_path)
    bir = y.read_bytes()
    akil.teknik_duzenle(tmp_path)
    assert y.read_bytes() == bir


def test_k0c_eylem_yeni_cagrida_zorunlu_eski_formda_istege_bagli():
    satir = akil.GELISTIRME["properties"]["satirlar"]["items"]
    assert "eylem" in satir["required"]
    eski = {"satirlar": [{"aday": "x", "videodaki_kullanim": "", "bizdeki_durum": "", "fark": "", "gelistirme_onerisi": "", "oneri": "yok", "kanit": ""}]}
    assert not akil._kurulum_red(eski)  # kayıtlı eski form eylemsiz okunur
