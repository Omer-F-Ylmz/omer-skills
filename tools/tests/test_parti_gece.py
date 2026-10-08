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
    gun = date.today().isoformat()
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
         "yaz": {"P1": {"durum": d("tamam"), "defter": [satir, satir]}}},
    ]})
    r, log, ozet, cagri = _kos(tmp_path)
    assert "parti devam P1" in cagri and "kapat" not in cagri
    assert "[aşama] A paket" in log
    o = ozet.read_text(encoding="utf-8")
    assert "tamam_eksik: 1" in o and "token: 51" in o and "paket: toplam 20" in o
