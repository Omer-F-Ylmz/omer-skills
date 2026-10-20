"""RAM'e duyarlı ajan kuyruğu (Desktop 12 Eki 17:05): köprü tavanı (10) doluyken bekleyen görevleri köprüyle AYNI bayraklarla
(opus · hafif: --disable-slash-commands + boş MCP · cc_profil "ajan" (ttl 5m + ajanTut) · istem stdin'den · izin atlama bayrağı YOK) kopuk
claude -p oturumlarında başlatır. Kuyruk: .kos/kopru/ajan-sira.tsv  (ad <TAB> istem dosyası [<TAB> koşul: yol::alt dize [<TAB> efor=medium|high]]).
Efor: mekanik iş (ölçüm koşusu, paketleme, birleştirme, kapı tekrarı) medium; tasarım/mimari/hata ayıklama high (TOKEN-3 K11).
Başlatma koşulu: RAM < ESIK, bu yöneticinin çalışanı < TAVAN, iki başlatma arası >= ARA sn. Durdurma: .kos/kopru/ajan-sira.dur
Çıktı: .kos/kopru/ajan-sira/<ad>.json · günlük .kos/kopru/ajan-sira.log (arka.py ile koşar).
  python arka.py .kos/kopru/ajan-sira.log .kos/kopru/ajan_sira.py"""
import ctypes, json, os, re, subprocess, sys, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
K = KOK / ".kos/kopru"
KUYRUK, DUR, CIKTI, ISKAYDI = K / "ajan-sira.tsv", K / "ajan-sira.dur", K / "ajan-sira", K / "is-kaydi.tsv"
CLAUDE = r"C:\Users\pc\.local\bin\claude.exe"
ESIK, TAVAN, ARA, SURE = 82, 3, 90, 10800
TAVAN_DOSYA = K / "ajan-sira.tavan"  # Desktop 20 Eki 12:15 (Ömer: haftalık %7, token düşsün): tavan dosyadan, varsayılan 3  # Desktop 14 Eki 19:45: 88'de başlatılan işle RAM %89'a çıktı (sınır %90, yeni iş ≥%85 yok)
sys.path.insert(0, str(KOK / "tools"))
import cc_profil  # TOKEN-2 K2: köprüyle aynı "ajan" profili (ttl 5m + ajanTut deny); CC_PROFIL_ZORLA=tam geri alır
ARGV = [CLAUDE, "-p", "--output-format", "json", "--model", "opus", "--disable-slash-commands", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', *cc_profil.kur("ajan")[0]]
MODELLER = ("opus", "sonnet", "haiku")
SLASH_DOSYA = K / "ajan-sira.slash"  # SLASH-ÖĞREN d1: dosya varsa köprü oturumlarında Skill aracı açık (onay/slash_ac.py)
DERS_DOSYA = K / "ajan-sira.ders"  # RUFLO-2 d3: ders önsözü açma bayrağı (dosya varsa ya da `--ders`); varsayılan kapalı


def ders_onek(metin):
    """Ana oturum istemine ilgili ders bloğu (≤120 jeton); bayrak kapalı, ders yok ya da hata → '' (0 jeton)."""
    if "--ders" not in sys.argv and not DERS_DOSYA.exists():
        return ""
    try:
        sys.path.insert(0, str(KOK / "tools/ogrenme")); import ders
        blok = ders.getir("general-purpose", metin[:600])[0]
    except Exception:
        return ""
    return blok + "\n\n" if blok else ""


ESIK_DOSYA = K / "ajan-sira.esik"  # Desktop 20 Eki 13:02 (Ömer: RAM %88-90'a kadar çıkabilir): eşik dosyadan, varsayılan 88


def esik():
    try:
        return min(89, max(60, int(ESIK_DOSYA.read_text(encoding="utf-8").split()[0])))
    except (OSError, ValueError, IndexError):
        return 88


def tavan():
    try:
        return max(1, int(TAVAN_DOSYA.read_text(encoding="utf-8").split()[0]))
    except (OSError, ValueError, IndexError):
        return TAVAN


def pid_canli(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    kod = ctypes.c_ulong()
    ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(kod))
    ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and kod.value == 259


def dis_calisan(bilinen):
    n = 0
    for f in CIKTI.glob("*.basladi"):
        if f.stem in bilinen:
            continue
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and pid_canli(p[2]):
            n += 1
    return n


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
            ek = dict(x.strip().split("=", 1) for x in p[3:] if "=" in x)
            efor, model = ek.get("efor", ""), ek.get("model", "opus")
            if efor not in ("", "medium", "high") or model not in MODELLER:
                raise ValueError(f"geçersiz efor/model: {satir!r}")
            s.append((p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "", efor, model))
    return s


def baslat_argv(efor, model="opus"):
    """TOKEN-3 K11: efor varsa --effort; CLAUDE_CODE_EFFORT_LEVEL --effort'u ezer → yalnız alt süreçten çıkar (KÖPRÜ-EFFORT-1).
    20 Eki: model= sütunu (opus|sonnet|haiku), varsayılan opus."""
    argv = [model if (i > 0 and ARGV[i - 1] == "--model") else a for i, a in enumerate(ARGV)]
    if SLASH_DOSYA.exists():  # SLASH-ÖĞREN d1: oturum + alt ajanları Skill aracıyla skill/komut çağırabilir (varsayılan kapalı)
        argv = [("Skill," + a if argv[i - 1] == "--tools" else a) for i, a in enumerate(argv) if a != "--disable-slash-commands"]
        dar = re.search(r"dar=(\w+)", SLASH_DOSYA.read_text(encoding="utf-8"))  # d2: tam skill listesi ≈ +35k token; dar=<küme> → yalnız slash-dar/<küme> eklentisi
        if dar:
            argv += ["--setting-sources", "", "--plugin-dir", str(K / "slash-dar" / dar.group(1))]
    env = taze_env()
    if not efor:
        return argv, env
    env.pop("CLAUDE_CODE_EFFORT_LEVEL", None)
    return [*argv, "--effort", efor], env


def taze_env():
    """Desktop 20 Eki 13:48: kullanıcı ortam değişkenleri (anahtar yenileme vb.) her başlatmada kayıt defterinden tazelenir; PATH/TEMP dokunulmaz."""
    import winreg
    env = dict(os.environ)
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            i = 0
            while True:
                try:
                    ad, deger, tur = winreg.EnumValue(k, i)
                except OSError:
                    break
                i += 1
                if ad.upper() not in ("PATH", "TEMP", "TMP") and isinstance(deger, str):
                    env[ad] = os.path.expandvars(deger) if tur == winreg.REG_EXPAND_SZ else deger
    except OSError:
        pass
    return env


def is_kaydi(ad, rc, dk, efor):
    """TOKEN-3 K17: biten işin claude -p JSON'u → is-kaydi.tsv tek satır (ağırlıklı = g + 1.25·cw + 0.1·cr + 5·ç; kalite = sonuçtaki ilk 'kalite' satırı)."""
    j = {}
    for s in reversed((CIKTI / f"{ad}.json").read_text(encoding="utf-8", errors="replace").splitlines()):
        if s.startswith("{"):
            try:
                j = json.loads(s)
            except ValueError:
                pass
            break
    u = j.get("usage") or {}
    agir = (u.get("input_tokens", 0) + 1.25 * u.get("cache_creation_input_tokens", 0) + 0.1 * u.get("cache_read_input_tokens", 0)
            + 5 * u.get("output_tokens", 0))
    kalite = re.search(r"(?im)^[^\n]*kalite[^\n]*", j.get("result") or "")
    if not ISKAYDI.exists():
        ISKAYDI.write_text("zaman\tis\tefor\tdk\tadim\tagirlikli\tusd\tsonuc\tkalite\n", encoding="utf-8")
    with ISKAYDI.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{ad}\t{efor or '-'}\t{dk:.0f}\t{j.get('num_turns', 0)}\t{agir:.0f}\t"
                f"{j.get('total_cost_usd', 0):.2f}\t{j.get('subtype') or f'rc{rc}'}\t{kalite.group(0).strip()[:80] if kalite else '-'}\n")


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
    log(f"başladı · tavan {tavan()} · RAM eşiği %{esik()} · önceden başlamış {len(baslayan)} · dış çalışan {dis_calisan(set())}")
    while True:
        for ad, (p, t0, fo, ef) in list(calisan.items()):
            if p.poll() is not None or time.time() - t0 > SURE:
                if p.poll() is None:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, creationflags=0x08000000)
                    log("SÜRE DOLDU", ad)
                fo.close()
                log("BİTTİ", ad, "rc", p.returncode, f"{(time.time() - t0) / 60:.0f} dk")
                is_kaydi(ad, p.returncode, (time.time() - t0) / 60, ef)
                del calisan[ad]
        bekleyen = [x for x in kuyruk() if x[0] not in baslayan]
        dis = dis_calisan(set(calisan))
        if not bekleyen and not calisan and not dis:
            log("kuyruk boş, çıkış")
            return
        r = ram()
        if not DUR.exists() and len(calisan) + dis < tavan() and r < esik() and time.time() - son >= ARA:
            for ad, istem, kosul, efor, model in bekleyen:
                if not kosul_tamam(kosul):
                    continue
                metin = (KOK / istem).read_text(encoding="utf-8")
                metin = ders_onek(metin) + metin
                try:  # MAKARA aktarım: kasadan ilgili 3-5 ders satırı (≤600 jeton); hata kuyruğu bozmaz
                    sys.path.insert(0, str(KOK / "tools")); import makara_ders; metin = makara_ders.onek(metin) + metin
                except Exception:
                    pass
                metin += "\n\n[bütçe] En fazla 60 tur kullan."
                fo = open(CIKTI / f"{ad}.json", "w", encoding="utf-8")
                argv, env = baslat_argv(efor, model)
                p = subprocess.Popen(argv, cwd=str(KOK), stdin=subprocess.PIPE, stdout=fo, stderr=subprocess.STDOUT,
                                     env=env, creationflags=0x08000000)
                p.stdin.write(metin.encode("utf-8"))
                p.stdin.close()
                calisan[ad] = (p, time.time(), fo, efor)
                baslayan.add(ad)
                (CIKTI / f"{ad}.basladi").write_text(time.strftime("%H:%M:%S") + f" pid {p.pid}", encoding="utf-8")
                son = time.time()
                log("BAŞLAT", ad, model, efor or "-", "pid", p.pid, f"RAM %{r}", "çalışan", len(calisan) + dis)
                break
        time.sleep(30)


if __name__ == "__main__":
    main()
