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
