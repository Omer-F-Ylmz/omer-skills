"""KATALOG-KANCA-1 madde 2: UserPromptSubmit katalog kancası — rutinde sessiz, zor işte <katalog> eki, hata yolunda boş."""
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import katalog_kanca as kk  # noqa: E402

BETIK = Path(kk.__file__)
ISLER = [l.split("\t") for l in (Path(__file__).parent / "katalog_kanca_isler.tsv").read_text(encoding="utf8").splitlines()]
RUTIN = [j for s, _, j in ISLER if s == "rutin"]
ZOR = [j for s, _, j in ISLER if s == "zor"]


@pytest.fixture(autouse=True)
def dizin(tmp_path, monkeypatch):
    monkeypatch.setattr(kk, "DIZIN", tmp_path)


def olay(istem, sid=None):
    return json.dumps({"session_id": sid or str(uuid.uuid4()), "hook_event_name": "UserPromptSubmit", "prompt": istem}).encode("utf8")


def test_kume_boyutu():
    assert len(RUTIN) == 30 and len(ZOR) == 22


def test_rutinde_tetik_en_cok_yuzde_10():
    yp = [j for j in RUTIN if kk.tetik(j)]
    assert len(yp) <= 3, yp


def test_zorda_tetik_en_az_yuzde_90():
    yn = [j for j in ZOR if not kk.tetik(j)]
    assert len(yn) <= 2, yn


@pytest.mark.parametrize("istem", ["devam", "evet, tamam", "/commit", "/plan bir landing sayfası, ödeme API'si ve Docker dağıtımı",
                                   "tamam devam et lütfen şimdi", "kısa: React + Postgres + Docker"])
def test_kisa_slash_devam_tetiklemez(istem):
    assert not kk.tetik(istem)


def test_acik_arac_sorusu_tetikler():
    assert kk.tetik("Bu PDF'leri toplu olarak metne çevirmek için hangi araç ya da skill uygun olur?")


def test_ek_bicimi_ve_tavan():
    cikti = kk.isle(olay(ZOR[0]))
    ek = json.loads(cikti)["hookSpecificOutput"]["additionalContext"]
    # talimat başta: CC 10k üstünü dosyaya yazıp yalnız 2k önizleme verir; liste B' ile aynı (katalog_ara varsayılanı)
    assert ek.startswith(kk.SON + "\n<katalog>\n```text") and ek.rstrip().endswith("```\n</katalog>")
    assert kk.katalog_ara.metin(kk.katalog_ara.aday(ZOR[0])) in ek and len(ek) <= kk.TAVAN


def test_numarali_isler_ayri_sorgulanir():
    ek = kk.ek("\n".join(f"{i}. {j}" for i, j in enumerate(ZOR[:3], 1)))
    assert all(a["ad"] in ek for j in ZOR[:3] for a in kk.katalog_ara.aday(j)[:10])


def test_ayni_oturumda_tekrar_yok():
    sid = str(uuid.uuid4())
    assert kk.isle(olay(ZOR[1], sid))
    assert kk.isle(olay(ZOR[1], sid)) == ""
    assert kk.isle(olay(ZOR[1]))  # başka oturum yine alır


@pytest.mark.parametrize("girdi", [b"", b"{bozuk", b'{"prompt": 5}', b"\xff\xfe"])
def test_bozuk_girdi_bos(girdi):
    assert kk.isle(girdi) == ""


def test_katalog_hatasi_bos(monkeypatch):
    monkeypatch.setattr(kk.katalog_ara, "aday", lambda *a, **k: 1 / 0)
    assert kk.isle(olay(ZOR[2])) == ""


def test_zaman_asimi_bos(monkeypatch):
    monkeypatch.setattr(kk, "SURE", 0.2)
    monkeypatch.setattr(kk.katalog_ara, "aday", lambda *a, **k: time.sleep(2) or [])
    t0 = time.time()
    assert kk.isle(olay(ZOR[3])) == ""
    assert time.time() - t0 < 1


def test_alt_surec_cp1252_konsol_utf8_cikti(tmp_path):
    env = {**os.environ, "PYTHONIOENCODING": "cp1252", "TEMP": str(tmp_path), "TMP": str(tmp_path)}
    r = subprocess.run([sys.executable, str(BETIK)], input=olay("Şirket içi ağ: Ğüİ çok dilli " + ZOR[4]), capture_output=True, env=env, timeout=30)
    assert r.returncode == 0, r.stderr.decode("utf8", "replace")
    ek = json.loads(r.stdout.decode("utf8"))["hookSpecificOutput"]["additionalContext"]
    assert "<katalog>" in ek and kk.SON in ek  # SON "seç" taşır: cp1252 çıktısı utf8 çözümde bozulurdu


def test_alt_surec_bozuk_girdi_cikis_0():
    r = subprocess.run([sys.executable, str(BETIK)], input=b"{bozuk", capture_output=True, timeout=30)
    assert r.returncode == 0 and r.stdout == b""
