"""VIDEO-PARTI-YT1 4: tools/video/parti-gece.ps1 (gece koşturucu). Gerçek video/claude çağrısı yok: sahte -Video (.cmd -> python)."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

PS1 = Path(__file__).resolve().parents[1] / "video" / "parti-gece.ps1"

SAHTE = '''import json, os, sys
from pathlib import Path
d = Path(os.environ["FAKE_DIR"])
sc = json.loads((d / "sc.json").read_text(encoding="utf-8"))
sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")


def say(ad):
    p = d / ad
    n = int(p.read_text()) if p.exists() else 0
    p.write_text(str(n + 1))
    return n


if sys.argv[1] == "--ram":
    r = sc["ram"]
    print(r[min(say("ram.n"), len(r) - 1)])
    sys.exit(0)
with (d / "calls.log").open("a", encoding="utf-8") as f:
    f.write(" ".join(sys.argv[1:]) + "\\n")
n = say("calls.n")
a = sc["adimlar"][n] if n < len(sc["adimlar"]) else {"kod": 1, "cikti": ["parti: kuyrukta bekleyen video yok"]}
for pid, y in (a.get("yaz") or {}).items():
    pd = Path(sc["kok"]) / ".kos" / pid
    pd.mkdir(parents=True, exist_ok=True)
    (pd / "durum.json").write_text(json.dumps(y["durum"]), encoding="utf-8")
    (pd / "defter.jsonl").write_text("".join(json.dumps(r) + "\\n" for r in y.get("defter", [])), encoding="utf-8")
for s in a.get("cikti", []):
    print(s)
for s in a.get("hata", []):
    print(s, file=sys.stderr)
sys.exit(a.get("kod", 0))
'''


def _kur(tmp_path, sc):
    (tmp_path / "fake.py").write_text(SAHTE, encoding="utf-8")
    (tmp_path / "video.cmd").write_text(f'@"{sys.executable}" "{tmp_path / "fake.py"}" %*\r\n', encoding="ascii")
    (tmp_path / "ram.cmd").write_text(f'@"{sys.executable}" "{tmp_path / "fake.py"}" --ram\r\n', encoding="ascii")
    (tmp_path / "sc.json").write_text(json.dumps({"kok": str(tmp_path), "ram": [8000], **sc}), encoding="utf-8")


def _kos(tmp_path, *ek):
    env = {**os.environ, "FAKE_DIR": str(tmp_path)}
    env.pop("VIDEO_UYGULA_KOK", None)
    r = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(PS1),
         "-Video", str(tmp_path / "video.cmd"), "-RamOku", str(tmp_path / "ram.cmd"),
         "-Kok", str(tmp_path), "-Bekle", "0", *ek],
        capture_output=True, text=True, encoding="utf-8", env=env, timeout=120)
    gun = date.today().isoformat() + (f"-{Path(ek[ek.index('-Kuyruk') + 1]).stem}" if "-Kuyruk" in ek else "")  # KİLİT-1: kuyruk adı eki
    log = tmp_path / ".kos" / f"gece-{gun}.log"
    ozet = tmp_path / ".kos" / f"ozet-{gun}.md"
    cagri = (tmp_path / "calls.log").read_text(encoding="utf-8") if (tmp_path / "calls.log").exists() else ""
    return r, (log.read_text(encoding="utf-8") if log.exists() else ""), ozet, cagri


def test_ps1_ascii_bomsuz():
    b = PS1.read_bytes()
    assert not b.startswith(b"\xef\xbb\xbf")
    b.decode("ascii")


def test_uc_ardisik_403_durur(tmp_path):
    satir = "https://youtu.be/V{} · altyazı otomatik · göz: yok (indirme 403)"
    _kur(tmp_path, {"adimlar": [{
        "cikti": ["parti: P1 · short · 3 video · tavan 50 çağrı / $1.0"] + [satir.format(i) for i in range(3)],
        "yaz": {"P1": {"durum": {"parti": "P1", "durum": "calisiyor", "videolar": {}}}}}]})
    r, log, ozet, cagri = _kos(tmp_path)
    assert "DUR: 403" in log
    assert "kapat" not in cagri
    assert cagri.count("baslat") == 1 and "devam" not in cagri
    assert ozet.is_file()


def test_ram_iki_dusuk_sonra_devam(tmp_path):
    _kur(tmp_path, {"ram": [100, 100, 8000], "adimlar": []})
    r, log, ozet, cagri = _kos(tmp_path)
    assert log.count("RAM dusuk") == 2
    assert "baslat" in cagri  # kapi gecildi
    assert "DUR: kuyruk bos" in log


def test_ram_hep_dusuk_on_sonra_durur(tmp_path):
    _kur(tmp_path, {"ram": [100], "adimlar": []})
    r, log, ozet, cagri = _kos(tmp_path)
    assert log.count("RAM dusuk") == 10
    assert "DUR: RAM" in log
    assert cagri == ""


def test_tavan_baslattan_once_durur(tmp_path):
    _kur(tmp_path, {"adimlar": []})
    r, log, ozet, cagri = _kos(tmp_path, "-Tavan", "10")
    assert "DUR: tavan" in log
    assert cagri == ""


def test_kuyruk_bos_temiz_ozet(tmp_path):
    _kur(tmp_path, {"adimlar": []})
    r, log, ozet, cagri = _kos(tmp_path)
    assert r.returncode == 0
    assert "DUR: kuyruk bos" in log
    assert "--cagri-tavan 50" in cagri and "--en-fazla 25" in cagri and "--paralel 4" in cagri
    assert "islenen" in ozet.read_text(encoding="utf-8")


def test_tam_akis_devam_ve_ozet(tmp_path):
    def d(durum):
        return {"parti": "P1", "durum": durum, "videolar": {
            "A": {"tarama": {"durum": "tamam"}}, "B": {"tarama": {"durum": "tamam_eksik"}}}}
    satir = {"adim": "tarama", "girdi": 2, "onb_okuma": 10, "onb_yazma": 0, "cikti": 5, "usd": 0.05}
    _kur(tmp_path, {"adimlar": [
        {"cikti": ["parti: P1 · short · 2 video · tavan 50 çağrı / $1.0"],
         "yaz": {"P1": {"durum": d("calisiyor"), "defter": [satir]}}},
        {"hata": ["[aşama] A paket bitti 2026-10-08T01:00:00 12.5", "[aşama] B paket bitti 2026-10-08T01:00:05 7.5"],
         "yaz": {"P1": {"durum": d("tamam"), "defter": [satir, satir, satir]}}},
    ]})
    r, log, ozet, cagri = _kos(tmp_path)
    assert "parti devam P1" in cagri and "kapat" not in cagri
    assert "[aşama] A paket" in log
    o = ozet.read_text(encoding="utf-8")
    assert "tamam_eksik: 1" in o and "token: 51" in o and "paket: toplam 20" in o


def test_baslat_usd_tavani_gecer(tmp_path):
    _kur(tmp_path, {"adimlar": []})
    r, log, ozet, cagri = _kos(tmp_path)
    assert "--usd-tavan 3.75" in cagri and "--usd-tavan-max 3.75" in cagri


def test_kuyruk_parametresi_baslata_gecer(tmp_path):
    _kur(tmp_path, {"adimlar": []})
    ky = str(tmp_path / "kuyruk-yt1-uzun.md")
    r, log, ozet, cagri = _kos(tmp_path, "-Kuyruk", ky)
    assert cagri.startswith(f"parti baslat {ky} ") and f"> video parti baslat {ky} " in log
    (b := tmp_path / "b").mkdir()
    _kur(b, {"adimlar": []})
    assert _kos(b)[3].startswith("parti baslat --en-fazla")  # -Kuyruk yok: davranis ayni


def test_kod3_kimlikli_tavan_ayni_partide_devam(tmp_path):
    """Gece 2026-10-09: baslat tavanda 3 döndü, kimlik satırı vardı → 'kuyruk bos' sanıldı, özet 0."""
    def d(b):
        return {"parti": "P1", "durum": "tavan" if b == "tavan" else "tamam", "tavan": {"cagri": 50, "usd": 3.75},
                "videolar": {"A": {"tarama": {"durum": "tamam_eksik"}}, "B": {"tarama": {"durum": b}}}}
    satir = {"adim": "tarama", "girdi": 1, "onb_okuma": 0, "onb_yazma": 0, "cikti": 0, "usd": 1.9, "cagri": 2}
    _kur(tmp_path, {"adimlar": [
        {"kod": 3, "cikti": ["parti: P1 · short · 2 video · tavan 50 çağrı / $3.75", "parti: tavan aşıldı (50 çağrı / $3.75), motor durdu"],
         "yaz": {"P1": {"durum": d("tavan"), "defter": [satir, satir]}}},
        {"yaz": {"P1": {"durum": d("tamam_eksik"), "defter": [satir, satir, satir]}}},
    ]})
    r, log, ozet, cagri = _kos(tmp_path)
    s = cagri.splitlines()
    assert s[1].startswith("parti devam P1") and "--cagri-ek" in s[1] and "--usd-ek" in s[1]
    assert "DUR: kuyruk bos" in log  # ikinci baslat: gerçekten boş
    o = ozet.read_text(encoding="utf-8")
    assert "partiler: P1" in o and "tamam_eksik: 2" in o and "tavan: 0" in o and "hata: 0" in o


def test_usd_ek_defter_ortalamasindan(tmp_path):
    """uzun-4 2026-10-09: sabit 0.075 $/çağrı, uzun videoda ~0.16; kalan 1 videonun ön tahmini tavanı aşıp parti ilerlemedi."""
    def d(b):
        return {"parti": "P1", "durum": "tavan" if b == "tavan" else "tamam", "tavan": {"cagri": 40, "usd": 6.66},
                "videolar": {"A": {"tarama": {"durum": "tamam"}}, "B": {"tarama": {"durum": b}}}}
    satir = {"adim": "tarama", "girdi": 0, "onb_okuma": 0, "onb_yazma": 0, "cikti": 0, "usd": 0.16, "cagri": 1}
    _kur(tmp_path, {"adimlar": [
        {"kod": 3, "cikti": ["parti: P1 · uzun · 2 video · tavan 40 çağrı / $6.66"],
         "yaz": {"P1": {"durum": d("tavan"), "defter": [satir] * 40}}},
        {"yaz": {"P1": {"durum": d("tamam"), "defter": [satir] * 42}}},
    ]})
    r, log, ozet, cagri = _kos(tmp_path)
    s = cagri.split()
    ek = float(s[s.index("--usd-ek") + 1])
    assert 6.66 + ek - 6.4 >= 2 * 0.16 * 1.5 - 1e-6  # kalan 1 video = 2 çağrı × ortalama × 1.5


def test_tavan_gecelik_butce_bitince_durur(tmp_path):
    d = {"parti": "P1", "durum": "tavan", "tavan": {"cagri": 50, "usd": 3.75},
         "videolar": {"A": {"tarama": {"durum": "tavan"}}}}
    satir = {"adim": "tarama", "girdi": 0, "onb_okuma": 0, "onb_yazma": 0, "cikti": 0, "usd": 3.8, "cagri": 50}
    _kur(tmp_path, {"adimlar": [{"kod": 3, "cikti": ["parti: P1 · short · 1 video · tavan 50 çağrı / $3.75"],
                                 "yaz": {"P1": {"durum": d, "defter": [satir]}}}]})
    r, log, ozet, cagri = _kos(tmp_path, "-Tavan", "50")
    assert "devam" not in cagri and "DUR: tavan" in log
    assert "tavan: 1" in ozet.read_text(encoding="utf-8")


def test_kimliksiz_kod1_kuyruk_bos_kod2_hata(tmp_path):
    _kur(tmp_path, {"adimlar": [{"kod": 2, "cikti": ["parti: kuyruğun sıradaki partisi uzun"]}]})
    r, log, ozet, cagri = _kos(tmp_path)
    assert "DUR: baslat hata (cikis 2)" in log


# ONARIM-3: kalan yalnız erisilemez video → parti devam tamam döner; koşucu "ilerlemiyor" demez, erisilemez hata sayılmaz
def test_erisilemez_parti_ilerlemiyor_demez(tmp_path):
    v = lambda p, t: {"paket": {"durum": p}, "tarama": {"durum": t}}
    d = lambda durum: {"durum": durum, "tavan": {"cagri": 4, "usd": 0.3}, "videolar": {"A": v("tamam", "tamam"), "B": v("erisilemez", "bekliyor")}}
    _kur(tmp_path, {"adimlar": [
        {"kod": 0, "cikti": ["parti: P1 · short · 2 video"], "yaz": {"P1": {"durum": d("yarim")}}},
        {"kod": 0, "cikti": ["parti P1 · durum tamam"], "yaz": {"P1": {"durum": d("tamam")}}}]})
    r, log, ozet, cagri = _kos(tmp_path, "-EnFazla", "2", "-Tavan", "20")
    assert "ilerlemiyor" not in log and "DUR: kuyruk bos" in log, log
    assert cagri.count("parti devam P1") == 1
    o = ozet.read_text(encoding="utf-8")
    assert "tamam: 1" in o and "hata: 0" in o


# ONARIM-5: kalan yalnız kalıcı paket hatası (3 kez düştü) → parti tamam; koşucu "ilerlemiyor" deyip durmaz, sonraki partiye geçer
def test_kalici_paket_hatasi_sonraki_partiye_gecer(tmp_path):
    v = lambda p, t, h=None: {"paket": {"durum": p, "deneme": 3, "hata": h}, "tarama": {"durum": t}}
    d = lambda durum: {"durum": durum, "tavan": {"cagri": 4, "usd": 0.3},
                       "videolar": {"A": v("tamam", "tamam"), "B": v("hata", "bekliyor", "hata: paket 3 kez düştü: TypeError: x")}}
    _kur(tmp_path, {"adimlar": [
        {"kod": 0, "cikti": ["parti: P1 · short · 2 video"], "yaz": {"P1": {"durum": d("yarim")}}},
        {"kod": 0, "cikti": ["parti P1 · durum tamam"], "yaz": {"P1": {"durum": d("tamam")}}},
        {"kod": 0, "cikti": ["parti: P2 · short · 1 video"], "yaz": {"P2": {"durum": {"durum": "tamam", "tavan": {"cagri": 2, "usd": 0.15},
                                                                                       "videolar": {"C": v("tamam", "tamam")}}}}}]})
    r, log, ozet, cagri = _kos(tmp_path, "-EnFazla", "2", "-Tavan", "20")
    assert "ilerlemiyor" not in log and "DUR: kuyruk bos" in log, log
    assert cagri.count("parti devam P1") == 1 and "partiler: P1, P2" in ozet.read_text(encoding="utf-8")
