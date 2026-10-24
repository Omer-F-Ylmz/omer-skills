# RAM-BEKCI-1: yönetici RAM bekçisi — hedef seçimi (izin listesi dokunulmaz, en büyük alt süreç) ve eşik kararı
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos/kopru"))
import ajan_ram_bekci  # noqa: E402

MB = 2**20
# (pid, ppid, ad, ws_bayt, komut)
AGAC = [
    (10, 1, "claude.exe", 900 * MB, "claude -p"),       # ajan kökü: asla hedef değil
    (11, 10, "bash.exe", 5 * MB, "bash"),
    (12, 11, "grep.exe", 670 * MB, "grep -ril foo tools"),
    (13, 10, "python.exe", 987 * MB, "python -m graphify update ."),
    (14, 10, "node.exe", 120 * MB, "node mcp"),
    (20, 1, "headroom.exe", 3000 * MB, "headroom proxy"),  # ajan dışı + izin listesi
    (21, 10, "chrome.exe", 2000 * MB, "chrome --headless"),  # ajan altında ama izin listesinde
    (22, 10, "python.exe", 1500 * MB, "python -m headroom.proxy"),  # komutta headroom → izin
    (30, 1, "python.exe", 2500 * MB, "python baska.py"),   # ajan ağacı dışı
]


def test_en_buyuk_alt_surec_secilir_izin_listesi_dokunulmaz():
    h = ajan_ram_bekci.hedef_sec(AGAC, {10})
    assert h[0] == 13 and h[2] == "python.exe"


def test_kok_ve_agac_disi_asla_hedef_degil():
    sadece_koklar = [s for s in AGAC if s[0] in (10, 20, 30)]
    assert ajan_ram_bekci.hedef_sec(sadece_koklar, {10}) is None


def test_torun_da_alt_surectir():
    agac = [(10, 1, "claude.exe", 1, ""), (11, 10, "bash.exe", 1, ""), (12, 11, "rg.exe", 50 * MB, "rg x")]
    assert ajan_ram_bekci.hedef_sec(agac, {10})[0] == 12


def test_esikler():
    olaylar = []
    oldur = lambda pid: olaylar.append(pid)
    log = lambda *a: None
    assert ajan_ram_bekci.kontrol(86, {10}, AGAC, oldur, log)[0] is None
    assert ajan_ram_bekci.kontrol(87, {10}, AGAC, oldur, log)[0] == "aday" and olaylar == []
    d, h = ajan_ram_bekci.kontrol(88, {10}, AGAC, oldur, log)
    assert d == "durdurdu" and h[0] == 13 and olaylar == [13]


def test_hedef_yoksa_durdurmaz():
    olaylar = []
    d, h = ajan_ram_bekci.kontrol(95, {10}, [AGAC[0]], olaylar.append, lambda *a: None)
    assert d == "hedef-yok" and olaylar == []


# RAM-BEKCI-2: ağaç düzeyi durdurma (>=92), korumalar, uyarı eşikleri
def _agac(kok, n_alt, mb_alt):
    s = [(kok, 1, "claude.exe", 100 * MB, "claude -p")]
    s += [(kok * 1000 + i, kok, "node.exe", mb_alt * MB, "node rea") for i in range(n_alt)]
    return s


def test_agac_en_buyuk_kok_secilir():
    s = _agac(10, 3, 100) + _agac(40, 3, 900)
    kok, toplam, alt, pidler = ajan_ram_bekci.agac_sec(s, {10, 40})
    assert kok == 40 and alt == 3 and pidler[-1] == 40


def test_agac_korumalilar_ve_altlari_dokunulmaz():
    s = _agac(10, 2, 50) + [
        (500, 10, "windowsapps-claude.exe", 800 * MB, r"C:\Program Files\WindowsApps\Claude_1.0\app\Claude.exe"),
        (501, 500, "node.exe", 900 * MB, "node altsurec"),            # korumalı sürecin altı da korunur
        (502, 10, "zenlesszonezero.exe", 3000 * MB, "zzz"),
        (503, 10, "epicgameslauncher.exe", 400 * MB, "epic"),
        (504, 10, "python.exe", 400 * MB, "python -m headroom.proxy"),
        (505, 10, "explorer.exe", 200 * MB, "explorer"),
    ]
    kok, toplam, alt, pidler = ajan_ram_bekci.agac_sec(s, {10})
    assert set(pidler) == {10, 10000, 10001} and toplam == 200 * MB and alt == 2


def test_agac_pidleri_yapraktan_koke():
    s = [(10, 1, "claude.exe", 1, ""), (11, 10, "bash.exe", 1, ""), (12, 11, "node.exe", 1, "")]
    assert ajan_ram_bekci.agac_pidleri(s, 10) == [12, 11, 10]


def test_agac_esigi_92_altinda_durdurmaz_ustunde_durdurur():
    s = _agac(10, 2, 100)
    olaylar, kayit = [], []
    assert ajan_ram_bekci.agac_kontrol(91, {10: "iş-a"}, s, olaylar.extend, lambda *a: None, set())[0] is None and olaylar == []
    d, kok, ad = ajan_ram_bekci.agac_kontrol(92, {10: "iş-a"}, s, olaylar.extend, lambda *a: kayit.append(a), set())
    assert (d, kok, ad) == ("kesildi", 10, "iş-a") and olaylar == [10000 + 1, 10000, 10] and kayit


def test_agac_kok_yoksa_hedef_yok():
    d, kok, ad = ajan_ram_bekci.agac_kontrol(99, {10: "x"}, [(30, 1, "python.exe", 1, "")], lambda p: 1 / 0, lambda *a: None, set())
    assert d == "hedef-yok" and kok is None


def test_uyari_alt_sayi_bir_kez():
    s = _agac(10, 61, 1)
    uyari, kayit = set(), []
    d1 = ajan_ram_bekci.agac_kontrol(80, {10: "iş-a"}, s, lambda p: 1 / 0, lambda *a: None, uyari)
    d2 = ajan_ram_bekci.agac_kontrol(80, {10: "iş-a"}, s, lambda p: 1 / 0, lambda *a: None, uyari)
    assert d1[0] == "uyari" and d2[0] is None


def test_uyari_mb():
    s = _agac(10, 2, 800)  # 1.7 GB
    assert ajan_ram_bekci.agac_kontrol(80, {10: "iş-a"}, s, lambda p: 1 / 0, lambda *a: None, set())[0] == "uyari"
    assert ajan_ram_bekci.agac_kontrol(80, {10: "iş-a"}, _agac(10, 2, 100), lambda p: 1 / 0, lambda *a: None, set())[0] is None
