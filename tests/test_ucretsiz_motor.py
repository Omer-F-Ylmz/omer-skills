"""UCRETSIZ-MOTOR-1: ücretsiz motor — sınıflayıcı, kimlik temizliği, merdiven, kayıt, defter oranı, kanıt."""
import http.server
import importlib.util
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / ".kos/kopru"))
sys.path.insert(0, str(KOK / "tools"))
import maliyet_defter  # noqa: E402
import ucretsiz_motor as um  # noqa: E402

_s = importlib.util.spec_from_file_location("ajan_sira", KOK / ".kos/kopru/ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)

ANAHTAR = "omni-test-anahtar-123"
KIRLI = {"ANTHROPIC_API_KEY": "sk-ant-api-x", "ANTHROPIC_API_KEY_AJAN": "sk-ant-ajan-x", "CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat-x",
         "ANTHROPIC_BASE_URL": "http://127.0.0.1:8787", "OMNIROUTE_KEY": ANAHTAR, "PATH": "p"}


@pytest.fixture(autouse=True)
def _izole(tmp_path, monkeypatch):
    sys.path.insert(0, str(KOK / "tools"))
    import beyin_dusun
    monkeypatch.setattr(beyin_dusun, "OLAY", tmp_path / "olay.jsonl")
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")
    monkeypatch.setattr(ajan_sira, "taze_env", lambda: dict(os.environ))  # HKCU'daki gerçek anahtar testi ezmesin


ISTEM = 'Rapor rapor/ucretsiz-motor-2.md ≤12 satır. Commit "UCRETSIZ-MOTOR-2:". Push YOK.'


def test_bos_kosu_selamlama():
    # gerçek kanıt: zip-yukle-24eki.json — success ama selamlama, 3 tur
    j = {"result": "Session started in `C:\\Projeler\\omer-skills`. What would you like to work on?", "num_turns": 3}
    assert um.bos_kosu(j, um.anahtarlar("zip-yukle-24eki", "KABUL: zip")) is True


def test_bos_kosu_gercek_is():
    j = {"result": "ucretsiz-motor-2 bitti. KABUL: 3/3, rapor/ucretsiz-motor-2.md yazıldı", "num_turns": 9}
    assert um.bos_kosu(j, um.anahtarlar("ucretsiz-motor-2", ISTEM)) is False


def test_bos_kosu_tek_tur_araçsız():
    assert um.bos_kosu({"result": "ucretsiz-motor-2 tamam", "num_turns": 1}, um.anahtarlar("ucretsiz-motor-2", ISTEM)) is True


def test_anahtarlar_rapor_ve_commit():
    a = um.anahtarlar("x", ISTEM)
    assert "rapor/ucretsiz-motor-2.md" in a and "ucretsiz-motor-2:" in a


def test_hatirlat_gorevi_sona_koyar():
    s = um.hatirlat("zip-yukle-24eki", "ZIP görevi\nikinci satır")
    assert "zip-yukle-24eki" in s and "ZIP görevi" in s and "ikinci" not in s


def test_kolay_siniflayici():
    assert um.kolay("paket-1", "Zip denetimi ve paketleme\ndetay") is True
    assert um.kolay("kanit-2", "Kanıt doğrulama raporu") is True
    assert um.kolay("x-1", "Mimari rapor tasarımı") is False  # zor işaret kolayı ezer
    assert um.kolay("x-2", "Güvenlik düzeltmesi: katalog") is False
    assert um.kolay("x-3", "Bilinmeyen iş") is False  # işaretsiz → kolay sayılmaz
    assert um.kolay("x-4", "") is False


def test_env_kur_kimlik_temizler():
    e = um.env_kur(KIRLI)
    assert e["ANTHROPIC_BASE_URL"] == um.URL and e["ANTHROPIC_AUTH_TOKEN"] == ANAHTAR and e["ANTHROPIC_MODEL"] == um.MODEL
    assert "OMNIROUTE_KEY" not in e and "ANTHROPIC_API_KEY" not in e and "ANTHROPIC_API_KEY_AJAN" not in e
    assert "CLAUDE_CODE_OAUTH_TOKEN" not in e and e["PATH"] == "p"
    assert not [v for v in e.values() if "sk-ant" in v]


def test_env_kur_anahtarsiz_hata(monkeypatch):
    monkeypatch.setattr(um, "anahtar", lambda env=None: None)
    with pytest.raises(RuntimeError):
        um.env_kur({"PATH": "p"})
    assert um.hazir({}) is False


def test_baslat_argv_ucretsiz(monkeypatch):
    for a, d in KIRLI.items():
        monkeypatch.setenv(a, d)
    argv, env = ajan_sira.baslat_argv("high", "ucretsiz")
    assert argv[argv.index("--model") + 1] == um.MODEL
    assert env["ANTHROPIC_AUTH_TOKEN"] == ANAHTAR and env["ANTHROPIC_BASE_URL"] == um.URL
    assert not [a for a in env if a.startswith("ANTHROPIC_API_KEY")] and "CLAUDE_CODE_OAUTH_TOKEN" not in env and "OMNIROUTE_KEY" not in env
    ayar_yolu = Path(argv[argv.index("--settings") + 1])
    ayar = ayar_yolu.read_text(encoding="utf-8")
    assert json.loads(ayar)["env"]["ANTHROPIC_BASE_URL"] == um.URL and ANAHTAR not in ayar  # anahtar dosyaya yazılmaz
    argv2, env2 = ajan_sira.baslat_argv("high", "haiku")
    assert "ANTHROPIC_AUTH_TOKEN" not in env2 or env2["ANTHROPIC_AUTH_TOKEN"] != ANAHTAR  # Claude kolları etkilenmez


def test_motor_sutunu(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tmotor=ucretsiz\nb\ti.md\t\tefor=high\tmotor=ucretsiz\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "", None, 0, None), ("b", "i.md", "", "high", None, 0, None)]
    tsv.write_text("a\ti.md\t\tmotor=baska\n", encoding="utf-8")
    with pytest.raises(ValueError):
        ajan_sira.kuyruk()


def test_merdiven_ucretsiz_basamagi(tmp_path, monkeypatch):
    monkeypatch.setattr(maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    monkeypatch.setattr(um, "hazir", lambda env=None: True)
    assert ajan_sira.MERDIVEN[0] == ("ucretsiz", "high") and ajan_sira.MERDIVEN[1] == ("haiku", "medium")
    assert ajan_sira.basamak_sec("paket-1-d1", None, "Zip denetimi") == 0  # kolay → ücretsiz
    assert ajan_sira.basamak_sec("atlas-1-d1", None, "Mimari karar") == 1  # zor/bilinmeyen → haiku medium
    maliyet_defter.yaz("paket-0-d1", "ucretsiz-high", 0.0, False)  # türde ücretsiz başarı %0 < %80
    assert ajan_sira.basamak_sec("paket-1-d1", None, "Zip denetimi") == 1  # doğrudan haiku'dan
    maliyet_defter.yaz("token-1-d1", "haiku-medium", 0.5, False)
    assert ajan_sira.basamak_sec("token-2-d3", None, "Zip") == 3  # Haiku-zayıf tür → sonnet medium
    assert ajan_sira.basamak_sec("x-1-r", 2, "") == 2  # yeniden deneme aynen
    monkeypatch.setattr(um, "hazir", lambda env=None: False)
    assert ajan_sira.basamak_sec("belge-1-d1", 0, "Belge") == 1  # anahtar yok → ücretsiz atlanır


def test_defter_ucretsiz_oran(tmp_path):
    y = tmp_path / "m.tsv"
    for ok in (1, 1, 1, 1, 0):
        maliyet_defter.yaz("rapor-1", "ucretsiz-high", 0.0, ok, y)
    for ok in (1, 0, 0):
        maliyet_defter.yaz("log-1", "ucretsiz-high", 0.0, ok, y)
    maliyet_defter.yaz("log-2", "haiku-medium", 0.1, False, y)  # ücretsiz değil → sayılmaz
    rows = maliyet_defter.oku(y)
    assert maliyet_defter.ucretsiz_oran(rows) == {"rapor": (4, 5), "log": (1, 3)}
    assert maliyet_defter.ucretsiz_zayif(rows) == {"log"}  # rapor %80 → zayıf değil, log %33 → zayıf


def test_is_kaydi_ucretsiz_sifir_usd_ve_kabul(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    (tmp_path / "a.json").write_text('{"subtype":"success","num_turns":3,"total_cost_usd":1.5,"result":"KABUL: tamam"}\n', encoding="utf-8")
    (tmp_path / "b.json").write_text('{"subtype":"success","num_turns":3,"total_cost_usd":1.5,"result":"bitti"}\n', encoding="utf-8")
    assert ajan_sira.is_kaydi("a", 0, 1.0, "high", "ucretsiz", None, True) is True
    assert ajan_sira.is_kaydi("b", 0, 1.0, "high", "ucretsiz", None, True) is False  # kabul satırı raporda yok
    assert ajan_sira.is_kaydi("b", 0, 1.0, "high", "ucretsiz", None, False) is True  # görevde KABUL satırı yoksa aranmaz
    d = [s.split("\t") for s in (tmp_path / "maliyet.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    assert [r[3] for r in d] == ["0.00", "0.00", "0.00"] and d[0][2] == "ucretsiz-high"  # tahmini Claude fiyatı yazılmaz


def _sahte_sunucu(kayit):
    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.rfile.read(int(self.headers.get("content-length") or 0))
            kayit.append({k.lower(): v for k, v in self.headers.items()})
            self.send_response(400)
            self.send_header("content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"type":"error","error":{"type":"invalid_request_error","message":"sahte"}}')

        def log_message(self, *a):
            pass
    s = http.server.HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


@pytest.mark.skipif(not Path(ajan_sira.CLAUDE).exists(), reason="claude yok")
def test_kanit_abonelik_kimligi_proxy_surecine_gecmez(monkeypatch, tmp_path):
    """Gerçek claude süreci ücretsiz motor env'iyle sahte uç noktaya istek atar; başlıklarda yalnız proxy anahtarı olmalı."""
    kayit = []
    sunucu = _sahte_sunucu(kayit)
    try:
        for a, d in {**KIRLI, "ANTHROPIC_API_KEY": "sk-ant-api-SIZMA", "CLAUDE_CODE_OAUTH_TOKEN": "sk-ant-oat-SIZMA"}.items():
            monkeypatch.setenv(a, d)
        monkeypatch.setattr(um, "URL", f"http://127.0.0.1:{sunucu.server_port}")
        argv, env = ajan_sira.baslat_argv("", "ucretsiz")
        p = subprocess.Popen(argv + ["--session-id", "00000000-0000-4000-8000-000000000001"], cwd=str(tmp_path), stdin=subprocess.PIPE,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env, creationflags=0x08000000)
        p.stdin.write(b"merhaba")
        p.stdin.close()
        t0 = time.time()
        while not kayit and time.time() - t0 < 240 and p.poll() is None:
            time.sleep(0.5)
        p.kill()
    finally:
        sunucu.shutdown()
    assert kayit, "claude uç noktaya hiç istek atmadı"
    tum = json.dumps(kayit)
    assert "SIZMA" not in tum and "sk-ant" not in tum  # abonelik/API kimliği hiçbir istekte yok
    assert any(ANAHTAR in (h.get("authorization", "") + h.get("x-api-key", "")) for h in kayit)  # kimlik = yalnız proxy anahtarı


# --- UCRETSIZ-MOTOR-2-DEVAM: ağ hatası + ücretsiz sağlayıcı zinciri ---
SAHTE_502 = {"subtype": "success", "num_turns": 1, "is_error": True, "api_error_status": 502,
             "result": 'API Error: 502 event: error {"type": "connection_error", "message": "getaddrinfo failed"}'}


def test_ag_hatasi_502_basari_sayilmaz(tmp_path, monkeypatch):
    assert um.ag_hatasi(SAHTE_502) is True
    assert um.ag_hatasi({"subtype": "success", "num_turns": 6, "result": "ucretsiz-motor-2 tamam, 502 satır işlendi"}) is False
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(ajan_sira, "K", tmp_path)
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    (tmp_path / "x.json").write_text(json.dumps(SAHTE_502), encoding="utf-8")
    ajan_sira.AG_ISLER.clear()
    assert ajan_sira.is_kaydi("x", 0, 1, "", "haiku") is False
    assert "x" in ajan_sira.AG_ISLER
    assert (tmp_path / "maliyet.tsv").read_text(encoding="utf-8").splitlines()[1].split("\t")[-1] == "0"


def test_ag_karar_ustel_bekleme_ve_kesik(monkeypatch):
    monkeypatch.setattr(ajan_sira, "log", lambda *a: None)
    ajan_sira.AG_DENEME.clear(); ajan_sira.AG_BEKLE.clear()
    ajan_sira.AG_DURUM.update(ardisik=0, kesik=False)
    sonuc = [ajan_sira.ag_karar(ad, 1, None, None, "g.md", "", None, simdi=1000) for ad in ("t", "t-a1", "t-a2", "t-a3")]
    assert [s[0] if s else None for s in sonuc] == ["t-a1", "t-a2", "t-a3", None]  # 4. denemede vazgeçer
    assert [ajan_sira.AG_BEKLE[n] - 1000 for n in ("t-a1", "t-a2", "t-a3")] == [120, 300, 600]
    assert all(s[5] == 1 for s in sonuc[:3])  # basamak yükselmez
    assert ajan_sira.AG_DURUM["kesik"] is True
    monkeypatch.setattr(um, "ag_var", lambda *a: False)
    assert ajan_sira.ag_bekliyor("baska") is True  # AĞ-KESİK: DNS dönmedi → yeni iş yok
    monkeypatch.setattr(um, "ag_var", lambda *a: True)
    assert ajan_sira.ag_bekliyor("baska") is False and ajan_sira.AG_DURUM["kesik"] is False
    assert ajan_sira.ag_bekliyor("t-a1", simdi=1001) is True and ajan_sira.ag_bekliyor("t-a1", simdi=1121) is False


def test_zincir_iki_saglayici_hatasi_ucuncuye_gecer(monkeypatch):
    monkeypatch.setattr(ajan_sira, "log", lambda *a: None)
    monkeypatch.setattr(ajan_sira.hermes_motor, "hazir", lambda *a: True)
    ajan_sira.ZINCIR_ADIM.clear()
    y1 = ajan_sira.zincir_karar("g", 0, "hermes", "g.md", "", None)        # hermes boş koştu → 2. sağlayıcı
    y2 = ajan_sira.zincir_karar(y1[0], 0, "ucretsiz", "g.md", "", None)    # 2. de boş → 3. sağlayıcı
    assert (y1[0], y2[0]) == ("g-z1", "g-z2") and y2[5] == 0
    assert um.ZINCIR[ajan_sira.ZINCIR_ADIM[y2[0]]] == "openrouter/nvidia/nemotron-3.5-lightning:free"
    assert ajan_sira.zincir_karar("g", 1, "haiku", "g.md", "", None) is None  # claude modelleri zincire girmez
    assert um.sonraki(len(um.ZINCIR) - 1) is None and um.sonraki(0, False) == 1


def test_anahtarlar_yeniden_deneme_eki_soyulur():
    assert um.anahtarlar("g-z2-a1-r", "x")[0] == "g"
    assert um.anahtarlar("ucretsiz-motor-1-b", "x")[0] == "ucretsiz-motor-1-b"


def test_ayar_env_zincir_modelini_kullanir(monkeypatch):
    monkeypatch.setattr(um, "AKTIF", "ucretsiz-groq")
    assert um.ayar_env()["ANTHROPIC_MODEL"] == "ucretsiz-groq"
    monkeypatch.setattr(um, "AKTIF", None)
    assert um.ayar_env()["ANTHROPIC_MODEL"] == um.MODEL
