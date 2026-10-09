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
    _yaz(kok, "docs/kurulumlar/parti/p1/denetim.md")
    _yaz(kok, "docs/denemeler/yeni.md")  # KAPANIŞ-2: motor klasöründe ama partiye ait değil → alınmaz
    _yaz(kok, "docs/baska/disari.md")
    assert akil.kapat(tmp_path, _d(), kok, _ctx()) == 0
    assert "docs/kurulumlar/parti/p1/denetim.md" in _git(kok, "show", "--name-only", "HEAD")
    assert "?? docs/baska/" in _git(kok, "status", "--porcelain") and "?? docs/denemeler/" in _git(kok, "status", "--porcelain")
    out = capsys.readouterr().out
    assert "p1/denetim.md" in out and "disari" not in out and "yeni.md" not in out  # commit'ten önce listelenir


def test_kapanis2_yalniz_parti_dosyalari_stage_edilir(tmp_path):
    """KAPANIŞ-2: kapat yalnız partinin dosyalarını (parti dizini · aday · ortak kayıt) alır; Ömer'in değişikliği (izli/izlenmeyen/staged) commit'e girmez."""
    kok = _repo(tmp_path)
    _yaz(kok, "docs/departmanlar/frontend.md")
    _yaz(kok, "docs/kurulumlar/adaylar/eski.md")
    _git(kok, "add", "-A")
    _git(kok, "commit", "-q", "-m", "omer")
    (kok / "docs/departmanlar/frontend.md").write_text("omer degisikligi\n", encoding="utf-8")
    (kok / "docs/kurulumlar/adaylar/eski.md").write_text("omer degisikligi\n", encoding="utf-8")
    _yaz(kok, "docs/kurulumlar/adaylar/omer-notu.md")
    _yaz(kok, "docs/video-tarama/baska-parti.md")
    _yaz(kok, "docs/a2.md")
    _git(kok, "add", "docs/a2.md")  # Ömer'in staged dosyası
    _yaz(kok, "docs/kurulumlar/parti/p1/panel.md")
    _yaz(kok, "docs/kurulumlar/adaylar/hizli-arac.md")
    _yaz(kok, "docs/video-tarama/kayit.jsonl")
    d = {**_d(), "adaylar": {"hizli-arac": {"durum": "tamam"}}}
    assert akil.kapat(tmp_path, d, kok, _ctx()) == 0
    giren = set(_git(kok, "show", "--name-only", "--format=", "HEAD").split())
    assert {"docs/kurulumlar/parti/p1/panel.md", "docs/kurulumlar/adaylar/hizli-arac.md", "docs/video-tarama/kayit.jsonl"} <= giren
    assert not giren & {"docs/departmanlar/frontend.md", "docs/kurulumlar/adaylar/eski.md", "docs/kurulumlar/adaylar/omer-notu.md",
                        "docs/video-tarama/baska-parti.md", "docs/a2.md"}
    assert "A  docs/a2.md" in _git(kok, "status", "--porcelain")  # Ömer'in staged dosyası olduğu gibi kalır


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


def test_kapanis2_devam_yeniden_tek_video_sayaci_sifirlar():
    """KAPANIŞ-2: devam --yeniden <video> → tavan/deneme sınırındaki videonun sayacı sıfırlanır, durum.json'a not düşer; diğerleri değişmez."""
    from video import parti as pt
    d = {"videolar": {"T7": {"paket": {"durum": "tamam", "deneme": 1}, "tarama": {"durum": "tavan", "deneme": 3, "hata": "tavan: x"}},
                      "B": {"paket": {"durum": "tamam", "deneme": 1}, "tarama": {"durum": "tavan", "deneme": 3, "hata": "y"}}}}
    pt.yeniden_ac(d, "T7")
    assert d["videolar"]["T7"]["tarama"] == {"durum": "bekliyor", "deneme": 0, "hata": None}
    assert d["videolar"]["B"]["tarama"]["deneme"] == 3 and d["videolar"]["T7"]["paket"]["durum"] == "tamam"
    assert d["notlar"][-1]["video"] == "T7" and d["notlar"][-1]["onceki"] == {"tarama": "tavan/3"}
    import pytest
    with pytest.raises(SystemExit):
        pt.yeniden_ac(d, "yok")
