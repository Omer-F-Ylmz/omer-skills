"""KİLİT-1: ortak dosyalara 4 süreç aynı anda yazar → kayıp/bozuk satır 0 · parti-gece -Kuyruk ekli log/özet adı + kullanım limiti DUR."""
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
N, P = 200, 4
ISCI = r"""
import sys, types
from pathlib import Path
from video import tarama as tr, cli
kip, d, p = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
for i in range(int(sys.argv[4])):
    if kip == "kayit":
        tr.kayit_ekle(d / "kayit.jsonl", [{"p": p, "i": i}])
    elif kip == "bilinen":
        tr.bilinen_ekle(d, [f"a{p}-{i}"])
    else:
        cli.kuyruk(types.SimpleNamespace(dosya=str(d / "kuyruk.md"), eylem="", isle=f"v{p}-{i}", commit="abc1234"), {"env": {}})
"""


def _kos(kip, d):
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(KOK), str(KOK.parent / "jev")])}
    ps = [subprocess.Popen([sys.executable, "-c", ISCI, kip, str(d), str(p), str(N)], env=env, stdout=subprocess.DEVNULL) for p in range(P)]
    assert all(p.wait(timeout=300) == 0 for p in ps)


def test_kayit_ekleme_kayipsiz(tmp_path):
    _kos("kayit", tmp_path)
    s = [json.loads(x) for x in (tmp_path / "kayit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert sorted((x["p"], x["i"]) for x in s) == [(p, i) for p in range(P) for i in range(N)]


def test_bilinen_oku_degistir_yaz_kayipsiz(tmp_path):
    _kos("bilinen", tmp_path)
    L = (tmp_path / "docs" / "video-tarama" / "bilinen-araclar.txt").read_text(encoding="utf-8").splitlines()
    assert sorted(L) == sorted(f"a{p}-{i}" for p in range(P) for i in range(N))


def test_kuyruk_satir_guncelleme_kayipsiz(tmp_path):
    satir = [f"| v{p}-{i} | 1 | b | n | |" for p in range(P) for i in range(N)]
    (tmp_path / "kuyruk.md").write_bytes(("| id | dk | başlık | not | durum |\r\n|---|---|---|---|---|\r\n" + "\r\n".join(satir) + "\r\n").encode("utf-8"))
    _kos("kuyruk", tmp_path)
    L = (tmp_path / "kuyruk.md").read_bytes().decode("utf-8").split("\r\n")
    assert len(L) == P * N + 3 and sum(s.endswith("| işlendi: abc1234 |") for s in L) == P * N


def _gece(tmp_path, *ek):
    (tmp_path / "video.cmd").write_text(
        '@echo off\r\nif "%2"=="baslat" echo parti: P1 - tamam - 1 video\r\n'
        'echo API Error: 429 rate_limit_error: usage limit reached, resets 7pm (Europe/Istanbul)\r\nexit /b 1\r\n', encoding="ascii")
    (tmp_path / "ram.cmd").write_text("@echo 99999\r\n", encoding="ascii")
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(KOK / "parti-gece.ps1"), "-Kok", str(tmp_path),
                    "-Video", str(tmp_path / "video.cmd"), "-RamOku", str(tmp_path / "ram.cmd"), "-Bekle", "0", *ek], timeout=120, check=True)
    return tmp_path / ".kos"


def test_gece_kuyruk_ekli_ad_ve_kullanim_limiti(tmp_path):
    kos, g = _gece(tmp_path, "-Kuyruk", str(tmp_path / "kuyruk-ig-hesap.md")), date.today().isoformat()
    log = (kos / f"gece-{g}-kuyruk-ig-hesap.log").read_text(encoding="utf-8-sig")
    assert "DUR: kullanım limiti" in log and log.count("> video") == 3
    oz = (kos / f"ozet-{g}-kuyruk-ig-hesap.md").read_text(encoding="utf-8-sig")
    assert "durma nedeni: kullanım limiti" in oz and "resets 7pm (Europe/Istanbul)" in oz


def test_gece_kuyruksuz_eski_ad(tmp_path):
    kos, g = _gece(tmp_path), date.today().isoformat()
    assert (kos / f"gece-{g}.log").is_file() and (kos / f"ozet-{g}.md").is_file()


def test_baslat_eszamanli_ayrik_video_kumesi(tmp_path):  # KILIT-2: seçim + pid mkdir + durum.json yazımı tek kilit altında
    import threading
    import time
    from test_m2a import Sahte, _ctx, _kurulum, _ns
    from video import parti as pt
    vs = [f"a{i:010d}" for i in range(6)]
    kok = _kurulum(tmp_path, vs)
    gercek, hata = pt.tr.kuyruk_parti, []

    def yavas(*a, **k):  # yarış penceresini açar: seçim ile durum.json yazımı arası 0.4 sn
        r = gercek(*a, **k)
        time.sleep(0.4)
        return r
    pt.tr.kuyruk_parti = yavas

    def kos():
        try:
            pt.parti(_ns("baslat", kok / "kuyruk.md", en_fazla=3), _ctx(kok, Sahte()))
        except Exception as e:  # noqa: BLE001
            hata.append(repr(e))
    try:
        ts = [threading.Thread(target=kos) for _ in range(2)]
        [t.start() for t in ts]
        [t.join() for t in ts]
    finally:
        pt.tr.kuyruk_parti = gercek
    kumeler = [set(json.loads(j.read_text(encoding="utf-8"))["videolar"]) for j in sorted((kok / ".kos").glob("*/durum.json"))]
    assert not hata and len(kumeler) == 2 and not (kumeler[0] & kumeler[1]) and kumeler[0] | kumeler[1] == set(vs)
