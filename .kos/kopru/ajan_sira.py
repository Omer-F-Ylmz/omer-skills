"""RAM'e duyarlı ajan kuyruğu (Desktop 12 Eki 17:05): köprü tavanı (10) doluyken bekleyen görevleri köprüyle AYNI bayraklarla
(opus · hafif: --disable-slash-commands + boş MCP · cc_profil "ajan" (ttl 5m + ajanTut) · istem stdin'den · izin atlama bayrağı YOK) kopuk
claude -p oturumlarında başlatır. Kuyruk: .kos/kopru/ajan-sira.tsv  (ad <TAB> istem dosyası [<TAB> koşul: yol::alt dize [<TAB> efor=medium|high]]).
Efor: mekanik iş (ölçüm koşusu, paketleme, birleştirme, kapı tekrarı) medium; tasarım/mimari/hata ayıklama high (TOKEN-3 K11).
Başlatma koşulu: RAM < ESIK, bu yöneticinin çalışanı < TAVAN, iki başlatma arası >= ARA sn. Durdurma: .kos/kopru/ajan-sira.dur
Çıktı: .kos/kopru/ajan-sira/<ad>.json · günlük .kos/kopru/ajan-sira.log (arka.py ile koşar).
  python arka.py .kos/kopru/ajan-sira.log .kos/kopru/ajan_sira.py"""
import ctypes, os, subprocess, sys, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
K = KOK / ".kos/kopru"
KUYRUK, DUR, CIKTI = K / "ajan-sira.tsv", K / "ajan-sira.dur", K / "ajan-sira"
CLAUDE = r"C:\Users\pc\.local\bin\claude.exe"
ESIK, TAVAN, ARA, SURE = 88, 9, 90, 10800
sys.path.insert(0, str(KOK / "tools"))
import cc_profil  # TOKEN-2 K2: köprüyle aynı "ajan" profili (ttl 5m + ajanTut deny); CC_PROFIL_ZORLA=tam geri alır
ARGV = [CLAUDE, "-p", "--output-format", "json", "--model", "opus", "--disable-slash-commands", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', *cc_profil.kur("ajan")[0]]


class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                ("t", "a", "tp", "ap", "tv", "av", "ae")]


def ram():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def kuyruk():
    s = []
    for satir in KUYRUK.read_text(encoding="utf-8").splitlines():
        p = satir.split("\t")
        if len(p) >= 2 and not satir.startswith("#"):
            efor = p[3].strip().removeprefix("efor=") if len(p) > 3 else ""
            if efor not in ("", "medium", "high"):
                raise ValueError(f"geçersiz efor: {satir!r}")
            s.append((p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "", efor))
    return s


def baslat_argv(efor):
    """TOKEN-3 K11: efor varsa --effort; CLAUDE_CODE_EFFORT_LEVEL --effort'u ezer → yalnız alt süreçten çıkar (KÖPRÜ-EFFORT-1)."""
    if not efor:
        return ARGV, None
    return [*ARGV, "--effort", efor], {k: v for k, v in os.environ.items() if k != "CLAUDE_CODE_EFFORT_LEVEL"}


def kosul_tamam(k):
    if not k:
        return True
    yol, alt = k.split("::", 1)
    f = KOK / yol
    return f.exists() and alt in f.read_text(encoding="utf-8", errors="replace")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    CIKTI.mkdir(exist_ok=True)
    calisan, baslayan, son = {}, set(), 0.0
    for f in CIKTI.glob("*.basladi"):
        baslayan.add(f.stem)
    log(f"başladı · tavan {TAVAN} · RAM eşiği %{ESIK} · önceden başlamış {sorted(baslayan)}")
    while True:
        for ad, (p, t0, fo) in list(calisan.items()):
            if p.poll() is not None or time.time() - t0 > SURE:
                if p.poll() is None:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, creationflags=0x08000000)
                    log("SÜRE DOLDU", ad)
                fo.close()
                log("BİTTİ", ad, "rc", p.returncode, f"{(time.time() - t0) / 60:.0f} dk")
                del calisan[ad]
        bekleyen = [x for x in kuyruk() if x[0] not in baslayan]
        if not bekleyen and not calisan:
            log("kuyruk boş, çıkış")
            return
        r = ram()
        if not DUR.exists() and len(calisan) < TAVAN and r < ESIK and time.time() - son >= ARA:
            for ad, istem, kosul, efor in bekleyen:
                if not kosul_tamam(kosul):
                    continue
                metin = (KOK / istem).read_text(encoding="utf-8") + "\n\n[bütçe] En fazla 60 tur kullan."
                fo = open(CIKTI / f"{ad}.json", "w", encoding="utf-8")
                argv, env = baslat_argv(efor)
                p = subprocess.Popen(argv, cwd=str(KOK), stdin=subprocess.PIPE, stdout=fo, stderr=subprocess.STDOUT,
                                     env=env, creationflags=0x08000000)
                p.stdin.write(metin.encode("utf-8"))
                p.stdin.close()
                calisan[ad] = (p, time.time(), fo)
                baslayan.add(ad)
                (CIKTI / f"{ad}.basladi").write_text(time.strftime("%H:%M:%S"), encoding="utf-8")
                son = time.time()
                log("BAŞLAT", ad, "pid", p.pid, f"RAM %{r}", "çalışan", len(calisan))
                break
        time.sleep(30)


if __name__ == "__main__":
    main()
