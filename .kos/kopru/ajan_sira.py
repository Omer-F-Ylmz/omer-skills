"""RAM'e duyarlı ajan kuyruğu (Desktop 12 Eki 17:05): köprü tavanı (10) doluyken bekleyen görevleri köprüyle AYNI bayraklarla
(opus · hafif: --disable-slash-commands + boş MCP · cc_profil "ajan" (ttl 5m + ajanTut) · istem stdin'den · izin atlama bayrağı YOK) kopuk
claude -p oturumlarında başlatır. Kuyruk: .kos/kopru/ajan-sira.tsv  (ad <TAB> istem dosyası [<TAB> koşul: yol::alt dize [<TAB> efor=medium|high] [<TAB> cwd=<yol>]]).
Efor: mekanik iş (ölçüm koşusu, paketleme, birleştirme, kapı tekrarı) medium; tasarım/mimari/hata ayıklama high (TOKEN-3 K11).
Başlatma koşulu: RAM < ESIK, bu yöneticinin çalışanı < TAVAN, iki başlatma arası >= ARA sn. Durdurma: .kos/kopru/ajan-sira.dur
Çıktı: .kos/kopru/ajan-sira/<ad>.json · günlük .kos/kopru/ajan-sira.log (arka.py ile koşar).
  python arka.py .kos/kopru/ajan-sira.log .kos/kopru/ajan_sira.py"""
import atexit, ctypes, json, os, re, subprocess, sys, tempfile, time
from pathlib import Path

import maliyet_defter  # maliyet.tsv: biten her iş + haftalık Haiku-zayıf türler (merdiven başlangıcı)

KOK = Path(r"C:\Projeler\omer-skills")
K = KOK / ".kos/kopru"
KUYRUK, DUR, CIKTI, ISKAYDI = K / "ajan-sira.tsv", K / "ajan-sira.dur", K / "ajan-sira", K / "is-kaydi.tsv"
CLAUDE = r"C:\Users\pc\.local\bin\claude.exe"
ESIK, TAVAN, ARA, SURE = 82, 3, 90, 10800
TAVAN_DOSYA = K / "ajan-sira.tavan"  # Desktop 20 Eki 12:15 (Ömer: haftalık %7, token düşsün): tavan dosyadan, varsayılan 3  # Desktop 14 Eki 19:45: 88'de başlatılan işle RAM %89'a çıktı (sınır %90, yeni iş ≥%85 yok)
sys.path.insert(0, str(KOK / "tools"))
import zorunlu_arac  # ZORUNLU-ARAÇ-1: ön uçuş bloğu + son denetim
import arka_istek  # ARKA-KALICI-1: ajan yerine yönetici başlatır
import cc_profil  # TOKEN-2 K2: köprüyle aynı "ajan" profili (ttl 5m + ajanTut deny); CC_PROFIL_ZORLA=tam geri alır
ARGV = [CLAUDE, "-p", "--output-format", "json", "--model", "opus", "--disable-slash-commands", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', *cc_profil.kur("ajan")[0]]
MODELLER = ("opus", "sonnet", "haiku")
MERDIVEN = [("haiku", "medium"), ("haiku", "high"), ("sonnet", "medium"), ("sonnet", "high")]  # tsv'de model yok → 0. basamak; başarısız → bir üst (en fazla 1 kez)
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


ORDU_DOSYA = K / "ajan-sira.ordu"  # ORDU-1: derleyici önsözü bayrağı (onay/ordu_1.py); varsayılan kapalı
ORDU_ONEK = ("ORDU-1 derleyici (bu oturumda okuma/keşif/özet/log/test koşusunu KENDİN yapma): ilk araç çağrından önce "
             "alt işleri say. Birden çok dosya okuma, kod keşfi, uzun log/doküman özeti → "
             "`python tools/ucuz_alt.py --tur ozet \"<soru>\" .claude/ordu3/<n>.md <dosya...>` (ücretsiz; çıktı .md'yi Read ile oku; çıkış 3 → kendin yap). "
             "Test/suit koşusu → Agent suite-kosucu, salt okuma analizi → Agent okuyucu. Sende yalnız plan, yazma, derleme, karar kalsın. "
             "Tek dosya/tek satır işi delege edilmez.\n\n")


def ordu_onek():
    return ORDU_ONEK if ORDU_DOSYA.exists() else ""


def cekirdek_onek(model):
    """AJAN-AKIS-1: iş-akışı çekirdeği (tools/ajan_cekirdek.md) haiku|sonnet kuyruk işine; opus'a eklenmez."""
    sys.path.insert(0, str(KOK / "tools")); import ajan_cekirdek
    return ajan_cekirdek.onek() if ajan_cekirdek.model_gerek(model) else ""


def dongu_onek(model, metin):
    """DERS-DONGU-1: haiku|sonnet|ücretsiz ajana ≤5 ders (≤150 jeton), çekirdekten sonra sabit konum; opus'a eklenmez."""
    try:
        sys.path.insert(0, str(KOK / "tools")); import ajan_cekirdek, ders_dongu
        return ders_dongu.onek(metin) if ajan_cekirdek.model_gerek(model) else ""
    except Exception:
        return ""


def on_ek_kur(model, metin):
    """Çekirdek istemin EN BAŞINA (sabit önek → prompt cache isabeti); model=None merdiven seçiminden sonra çağrılır."""
    return cekirdek_onek(model) + dongu_onek(model, metin) + metin


ON_SOZ = K / "on-soz.md"  # ARAÇ-DENETİM-1: her göreve ortak ön söz; yoksa boş


def arac_onek(cwd=None):
    on = ON_SOZ.read_text(encoding="utf-8") + "\n" if ON_SOZ.exists() else ""
    return f"Çalışma dizini: {cwd}\n" + on if cwd else on


def ogren_blok(metin):
    """OGREN-OTO-1: ruflo pattern-search/store sabit bloğu; görev metni zaten içeriyorsa '' (ikinci kez eklenmez)."""
    if "hooks_intelligence_pattern-search" in metin:
        return ""
    return ("Başlarken: ruflo hooks_intelligence_pattern-search (sorgu = görev adı + ilk başlık, topK 5) → uygula.\n"
            "Bitirirken: en az 1 ders hooks_intelligence_pattern-store (type hata-dersi veya basari, confidence 0.6-0.9).\n\n")


ON_DOSYA = K / "ajan-sira.ordu-on"  # ORDU-1 d12: mekanik ön-özet bayrağı; varsayılan kapalı


def ordu_on_ozet(ad, metin):
    """Bayrak açık + istemde ≥3 var olan repo dosyası → ücretsiz `ucuz_alt.py --tur ozet` önceden koşar, özet isteme eklenir; hata → ''."""
    if not ON_DOSYA.exists():
        return ""
    yollar = []
    for t in re.findall(r"[\w./\\-]+\.(?:py|md|tsv|json|cs|js|ts|txt)\b", metin):
        if t not in yollar and (KOK / t).is_file():
            yollar.append(t)
    if len(yollar) < 3:
        return ""
    cikti = KOK / ".claude/ordu3" / f"on-{ad}.md"
    try:
        r = subprocess.run([sys.executable, "-I", str(KOK / "tools/ucuz_alt.py"), "--tur", "ozet",
                            "Bu dosyalarda görevle ilgili yapıyı, işlev adlarını ve satır konumlarını özetle.",
                            str(cikti), *yollar[:8]], cwd=KOK, capture_output=True, timeout=180,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode == 0 and cikti.is_file():
            return f"[ön-özet (ücretsiz model; {', '.join(yollar[:8])}) — doğrulamadan önce kritik satırı Read ile kontrol et]\n{cikti.read_text(encoding='utf-8')}\n\n"
    except (OSError, subprocess.SubprocessError):
        pass
    return ""


ESIK_DOSYA = K / "ajan-sira.esik" # Desktop 20 Eki 13:02 (Ömer: RAM %88-90'a kadar çıkabilir): eşik dosyadan, varsayılan 88


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


def claude_sureci(pid, basladi):
    """Hayalet ayıklama: pid canlı + görüntü adı claude* + süreç başlangıcı .basladi yazılışından (basladi, epoch) sonra değil."""
    k32 = ctypes.windll.kernel32
    k32.OpenProcess.restype = ctypes.c_void_p
    h = k32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    try:
        ad = ctypes.create_unicode_buffer(520)
        n = ctypes.c_ulong(520)
        if not k32.QueryFullProcessImageNameW(ctypes.c_void_p(h), 0, ad, ctypes.byref(n)):
            return False
        t = [ctypes.c_ulonglong() for _ in range(4)]
        if not k32.GetProcessTimes(ctypes.c_void_p(h), *(ctypes.byref(x) for x in t)):
            return False
        bas = t[0].value / 1e7 - 11644473600  # FILETIME → epoch
        return os.path.basename(ad.value).lower().startswith("claude") and bas <= basladi + 5
    finally:
        k32.CloseHandle(ctypes.c_void_p(h))


def dis_calisan(bilinen):
    n = 0
    for f in CIKTI.glob("*.basladi"):
        if f.stem in bilinen:
            continue
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and pid_canli(p[2]) and claude_sureci(p[2], f.stat().st_mtime):
            n += 1
    return n


KILIT = K / "ajan-sira.kilit"  # TEKİL-YÖNETİCİ: "pid saat"; canlı bir başka ajan_sira varsa ikinci kopya çıkar


def ajan_sira_canli(pid):
    """Pid canlı ve komut satırında ajan_sira.py varsa True (pid'i başka süreç almışsa ayrılır)."""
    if not pid_canli(pid):
        return False
    ps = f"(Get-CimInstance Win32_Process -Filter 'ProcessId={int(pid)}').CommandLine"
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", creationflags=0x08000000)
    return "ajan_sira.py" in r.stdout


def kilit_al():
    """Kilit yoksa, pid'i ölmüşse ya da kendi pid'i ise yazar ve True; canlı bir başka yönetici varsa False."""
    try:
        eski = int(KILIT.read_text(encoding="utf-8").split()[0])
    except (OSError, ValueError, IndexError):
        eski = 0
    if eski not in (0, os.getpid()) and ajan_sira_canli(eski):
        return False
    KILIT.write_text(f"{os.getpid()} {time.strftime('%H:%M:%S')}", encoding="utf-8")
    atexit.register(kilit_sil)
    return True


def kilit_sil():
    try:
        if KILIT.read_text(encoding="utf-8").split()[0] == str(os.getpid()):
            KILIT.unlink()
    except (OSError, IndexError):
        pass


class MEM(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in
                ("t", "a", "tp", "ap", "tv", "av", "ae")]


def ram():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.dwMemoryLoad


def ram_toplam_mb():
    m = MEM()
    m.dwLength = ctypes.sizeof(MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.t // 2**20


# RAM-1: ajan başına tahmini MB (docs/ram/olcum.md ölçümü): claude+bash ≈450, ajan başı stdio MCP'ler (http/paylaşımlı 0), render/blender ≈1500
AJAN_MB, MCP_MB, RENDER_MB = 450, {"playwright": 330, "chrome-devtools": 300, "premiere-pro": 170, "ruflo": 90}, 1500


def tahmin_mb(ham):
    sys.path.insert(0, str(KOK / "tools")); import mcp_profil
    return AJAN_MB + sum(MCP_MB.get(m, 0) for m in mcp_profil.sec(ham)) + (RENDER_MB if re.search(r"(?i)\b(render\w*|blender)\b", ham) else 0)


def ram_izin(r, tahmin, toplam_mb, esik_, bos):
    """Başlatmadan sonraki tahmini RAM% eşiği aşmıyorsa True; hiçbir iş çalışmıyorsa her zaman True (kilitlenme olmasın)."""
    return bos or r + tahmin * 100 / toplam_mb < esik_


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def kuyruk():
    s = []
    for satir in KUYRUK.read_text(encoding="utf-8").splitlines():
        p = satir.split("\t")
        if len(p) >= 2 and not satir.startswith("#"):
            ek = dict(x.strip().split("=", 1) for x in p[3:] if "=" in x)
            efor, model = ek.get("efor", ""), ek.get("model")  # model yok → MERDIVEN (haiku medium'dan)
            if efor not in ("", "medium", "high") or (model is not None and model not in MODELLER):
                raise ValueError(f"geçersiz efor/model: {satir!r}")
            s.append((p[0].strip(), p[1].strip(), p[2].strip() if len(p) > 2 else "", efor, model, None, ek.get("cwd")))
    return s


def basamak_sec(ad, bas):
    """Merdiven başlangıcı: yeniden deneme (bas verili) aynen; yoksa son 7 günde Haiku'da başarısız tür → sonnet medium (2), diğer → haiku medium (0)."""
    if bas is not None:
        return bas
    return 2 if maliyet_defter.tur(ad) in maliyet_defter.haiku_zayif(maliyet_defter.oku()) else 0


def baslat_argv(efor, model="opus", mcp=None, ajanlar=(), butce=None):
    """TOKEN-3 K11: efor varsa --effort; CLAUDE_CODE_EFFORT_LEVEL --effort'u ezer → yalnız alt süreçten çıkar (KÖPRÜ-EFFORT-1).
    20 Eki: model= sütunu (opus|sonnet|haiku), varsayılan opus. MCP-AÇ-1: mcp= profil dosyası yolu (yoksa boş MCP)."""
    argv = [model if (i > 0 and ARGV[i - 1] == "--model") else a for i, a in enumerate(ARGV)]
    if mcp:
        argv[argv.index("--mcp-config") + 1] = str(mcp)
    if ajanlar and "--settings" in argv:  # ENGEL-TARAMA-1: ZORUNLU ARAÇLAR'daki ajanlar Agent(ad) deny'dan çıkar (görev başına ayrı ayar dosyası)
        yeni = cc_profil.kur("ajan", tut_ek=ajanlar, gecici=Path(tempfile.gettempdir()) / f"cc_profil_{os.getpid()}_{abs(hash(tuple(ajanlar)))}")[0]
        argv[argv.index("--settings") + 1] = yeni[yeni.index("--settings") + 1]
    if SLASH_DOSYA.exists():  # SLASH-ÖĞREN d1: oturum + alt ajanları Skill aracıyla skill/komut çağırabilir (varsayılan kapalı)
        argv = [("Skill," + a if argv[i - 1] == "--tools" else a) for i, a in enumerate(argv) if a != "--disable-slash-commands"]
        dar = re.search(r"dar=(\w+)", SLASH_DOSYA.read_text(encoding="utf-8"))  # d2: tam skill listesi ≈ +35k token; dar=<küme> → yalnız slash-dar/<küme> eklentisi
        if dar:
            kume = K / "slash-dar" / dar.group(1)  # d3: --setting-sources "" kullanıcı ayarlarını düşürüyordu → profil --settings'ine küme ayarı birleştirilir (ikinci --settings öncekini ezer)
            i = argv.index("--settings") + 1
            birlesik = {**json.loads(Path(argv[i]).read_text(encoding="utf-8")), **json.loads((kume / "ayar.json").read_text(encoding="utf-8"))}
            (kume / "birlesik-ayar.json").write_text(json.dumps(birlesik), encoding="utf-8")
            argv[i] = str(kume / "birlesik-ayar.json")
            argv += ["--plugin-dir", str(kume)]
    if mcp and os.environ.get("CC_MCP_ERTELE") != "0":  # MCP-AÇ-2: KEEP dışı MCP araçları kapanır; CC_MCP_ERTELE=0 geri alır
        sys.path.insert(0, str(KOK / "tools")); import mcp_profil
        argv = mcp_profil.ertele(argv, mcp, os.environ.get("CC_MCP_ERTELE") == "1")
    if mcp and os.environ.get("CC_MCP_KAPI") != "0" and "--settings" in argv:  # ERİŞİM-TAM-1: doğrudan MCP az (kapı-tek) → ToolSearch kapalı (sabit ~6.5k jeton yükü)
        sys.path.insert(0, str(KOK / "tools")); import mcp_profil
        if not mcp_profil.agir(mcp):
            i = argv.index("--settings") + 1
            ayar = json.loads(Path(argv[i]).read_text(encoding="utf-8"))
            ayar.setdefault("env", {})["ENABLE_TOOL_SEARCH"] = "false"
            kayit = Path(tempfile.gettempdir()) / f"cc_ts_{os.getpid()}_{abs(hash(argv[i]))}.json"
            kayit.write_text(json.dumps(ayar), encoding="utf-8")
            argv[i] = str(kayit)
    if butce is not None:  # 22 Eki (Ömer): bütçe HEDEFTİR, işi kesmez. Sert sınır yalnız kaçak döngüye karşı emniyet: hedefin 8 katı (≥ $3)
        argv = [*argv, "--max-budget-usd", f"{max(3.0, butce * EMNIYET_KAT):g}"]
    env = taze_env()
    env["AJAN_SIRA_KUYRUK"] = "1"  # SAYAC-FIX-1: cagri_sayac.py bu ajanda devir/DUR uyarısı basmaz
    if "max-old-space-size" not in env.get("NODE_OPTIONS", ""):  # RAM-1: ajan başı node MCP'leri (rea, chrome-devtools) sınırsız heap büyütmesin
        env["NODE_OPTIONS"] = (env.get("NODE_OPTIONS", "") + " --max-old-space-size=2048").strip()
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


BUTCE_VARSAYILAN = 0.50  # BÜTÇE-KAPI-1: görev dosyasında "BÜTÇE ... ≤$X" satırı yoksa (22 Eki: HEDEF, kesme değil)
EMNIYET_KAT = 8  # yalnız kaçak döngü emniyeti
BUTCE_ASTI = set()  # bütçesi dolup durdurulan işler (error_max_budget_usd): merdiven bunları yeniden denemez


def butce_bul(metin):
    """BÜTÇE-KAPI-1: görev metnindeki ilk 'BÜTÇE ... ≤$X' (ondalık virgül ya da nokta) → USD; yoksa varsayılan."""
    m = re.search(r"BÜTÇE[^\n≤]*≤\s*\$\s*(\d+(?:[.,]\d+)?)", metin)
    return float(m.group(1).replace(",", ".")) if m else BUTCE_VARSAYILAN


def sonuc_temizle(ad):
    """BÜTÇE-KAPI-1: ad.json yalnız geçerli JSON satırı taşısın. claude stdout'una JSON dışı satır (ör. 'Background tasks still running' uyarısı)
    ya da kesik parça karışırsa dosya bozulur; geçersiz satırlar ad.stray.txt'ye taşınır."""
    yol = CIKTI / f"{ad}.json"
    temiz, stray = [], []
    for s in yol.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            json.loads(s)
            temiz.append(s)
        except ValueError:
            if s.strip():
                stray.append(s)
    if stray:
        yol.write_text("\n".join(temiz) + "\n", encoding="utf-8")
        (CIKTI / f"{ad}.stray.txt").write_text("\n".join(stray) + "\n", encoding="utf-8")
        log("JSON TEMİZLE", ad, f"{len(stray)} satır taşındı")


def is_kaydi(ad, rc, dk, efor, model, butce=None):
    """TOKEN-3 K17: biten işin claude -p JSON'u → is-kaydi.tsv tek satır (ağırlıklı = g + 1.25·cw + 0.1·cr + 5·ç; kalite = sonuçtaki ilk 'kalite' satırı).
    Dönüş: kabul (rc 0 ve subtype success); aynı anda maliyet.tsv'ye yazılır."""
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
    ok = rc == 0 and j.get("subtype") == "success"
    usd = j.get("total_cost_usd", 0)
    maliyet_defter.yaz(ad, f"{model}-{efor}" if efor else model, usd, ok)
    if butce is not None:  # BÜTÇE-KAPI-1: %100 durdurma claude'un --max-budget-usd'si; burada yalnız kayıt ve son %80 uyarısı
        durum = j.get("subtype") or f"rc{rc}"
        maliyet_defter.yaz_butce(ad, butce, usd, durum)
        if durum == "error_max_budget_usd":
            BUTCE_ASTI.add(ad)
        if usd >= 0.8 * butce:
            log("BÜTÇE %80+", ad, f"${usd:.2f} / ${butce:.2f} · {durum}")
    if model == "opus" and ok and j.get("session_id"):  # AJAN-AKIS-1 2. beyin: başarılı Opus oturumundan kalıp damıt (arka plan iş parçacığı, hata kuyruğu bozmaz)
        try:
            import threading; sys.path.insert(0, str(KOK / "tools")); import akis_damit
            threading.Thread(target=akis_damit.kanca, args=(j["session_id"], "tamam", "opus"), daemon=True).start()
        except Exception:
            pass
    return ok


def cwd_hedef(cwd):
    """KÖPRÜ-CWD-1: cwd= sütunu KOK'a göre çözülür; sütun yoksa KOK, klasör yoksa None (satır başlatılmaz)."""
    if not cwd:
        return KOK
    h = KOK / cwd
    return h if h.is_dir() else None


def kosul_tamam(k):
    if not k:
        return True
    yol, alt = k.split("::", 1)
    f = KOK / yol
    return f.exists() and alt in f.read_text(encoding="utf-8", errors="replace")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if not kilit_al():  # TEKİL-YÖNETİCİ: aynı anda iki yönetici kuyruğu işlemesin
        log("zaten çalışıyor · ikinci kopya çıkıyor")
        return
    CIKTI.mkdir(exist_ok=True)
    calisan, baslayan, son = {}, set(), 0.0
    yeniden, tekrar, uyari = [], set(), set()  # merdiven: başarısız işin bir üst basamakta tek yeniden denemesi; uyari: "cwd yok" günlüğü bir kez
    for f in CIKTI.glob("*.basladi"):
        baslayan.add(f.stem)
    log(f"başladı · tavan {tavan()} · RAM eşiği %{esik()} · önceden başlamış {len(baslayan)} · dış çalışan {dis_calisan(set())}")
    while True:
        for ad, (p, t0, fo, ef, mdl, bas, istem, kosul, cwd, butce) in list(calisan.items()):
            if p.poll() is not None or time.time() - t0 > SURE:
                if p.poll() is None:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True, creationflags=0x08000000)
                    log("SÜRE DOLDU", ad)
                fo.close()
                (CIKTI / f"{ad}.mcp.json").unlink(missing_ok=True)  # MCP-AÇ-1: profil dosyası env taşıyabilir
                sonuc_temizle(ad)  # BÜTÇE-KAPI-1: JSON dışı satırlar ayrılır, ad.json geçerli kalır
                log("BİTTİ", ad, "rc", p.returncode, f"{(time.time() - t0) / 60:.0f} dk")
                ok = is_kaydi(ad, p.returncode, (time.time() - t0) / 60, ef, mdl, butce)
                if bas is not None and not ok and ad not in tekrar and ad not in BUTCE_ASTI and bas + 1 < len(MERDIVEN):  # bütçe dolan iş üst modelle yeniden koşmaz
                    yeniden.append((ad + "-r", istem, kosul, None, None, bas + 1, cwd))
                    tekrar.add(ad + "-r")
                    log("YENİDEN", ad, "→ bir üst basamak", MERDIVEN[bas + 1])
                den = zorunlu_arac.denetle(ad)  # ZORUNLU-ARAÇ-1: döküm sayımı; arac_eksik → aynı görev bir kez eksik araç ekiyle yeniden
                if den and den["durum"] != "ok":
                    log("DENETİM", ad, den["durum"], "eksik:", ", ".join(den["eksik"]))
                    yeni, dk = zorunlu_arac.devam(ad, den)  # ARAÇ-KAPI-1: üç işaretten biri → en fazla 2 devam turu (Haiku), sonra DUR
                    if zorunlu_arac.YENIDEN and dk == "devam" and yeni not in tekrar:
                        yeniden.append((yeni, zorunlu_arac.yeniden_istem(ad, istem, zorunlu_arac.eksik_liste(den), yeni), kosul, None, None, 0, cwd))
                        tekrar.add(yeni)
                    elif dk == "dur":
                        log("DUR", ad, "2 devam turundan sonra hâlâ eksik:", ", ".join(zorunlu_arac.eksik_liste(den)))
                subprocess.Popen([sys.executable, str(KOK / "tools" / "beyin_kayit.py"), ad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)  # BEYIN-KAYIT-1: ikinci beyne yaz (arka plan, beklemez)
                del calisan[ad]
        bekleyen = yeniden + [x for x in kuyruk() if x[0] not in baslayan]
        dis = dis_calisan(set(calisan))
        if not bekleyen and not calisan and not dis:
            log("kuyruk boş, çıkış")
            return
        r = ram()
        if not DUR.exists() and len(calisan) + dis < tavan() + (3 if r < esik() - 10 else 0) and r < esik() and time.time() - son >= ARA:  # RAM-1: RAM boşken tavan +3; asıl koruma aday başına tahmin kapısı
            for ad, istem, kosul, efor, model, bas, cwd in bekleyen:
                if ("k", ad) not in uyari:  # ZORUNLU-ARAÇ-1 d4: koşul görev dosyasının kendinde geçiyorsa erken başlar
                    uyari.add(("k", ad))
                    if u := zorunlu_arac.kosul_uyari(kosul, istem):
                        log("KOŞUL UYARI", ad, u)
        try:  # ARKA-KALICI-1: ajanların yazdığı uzun iş istekleri burada (ajandan bağımsız) başlar
            arka_istek.isle(log=log)
        except Exception as e:
            log("arka-istek hata", repr(e)[:120])
                if not kosul_tamam(kosul):
                    continue
                hedef = cwd_hedef(cwd)
                if hedef is None:
                    if ad not in uyari:
                        log("cwd yok", ad, cwd)
                        uyari.add(ad)
                    continue
                tah = tahmin_mb((KOK / istem).read_text(encoding="utf-8"))
                if not ram_izin(r, tah, ram_toplam_mb(), esik(), not (calisan or dis)):  # RAM-1: ağır iş RAM'i eşiğin üstüne taşıyacaksa bekler, hafif olan sıradan geçer
                    if ("r", ad) not in uyari:
                        uyari.add(("r", ad))
                        log("RAM BEKLE", ad, f"tahmin {tah} MB · RAM %{r} · eşik %{esik()}")
                    continue
                if model is None:
                    bas = basamak_sec(ad, bas)
                    model, efor = MERDIVEN[bas]
                metin = (KOK / istem).read_text(encoding="utf-8")
                butce = butce_bul(metin)  # BÜTÇE-KAPI-1: ham görev metninden (ön ekler karışmadan)
                log("BÜTÇE", ad, f"${butce:.2f}")
                metin = arac_onek(str(hedef) if cwd else None) + zorunlu_arac.blok(ad, metin) + ders_onek(metin) + ordu_onek() + ordu_on_ozet(ad, metin) + metin  # ZORUNLU-ARAÇ-1: ön uçuş
                try:  # MAKARA aktarım: kasadan ilgili 3-5 ders satırı (≤600 jeton); hata kuyruğu bozmaz
                    sys.path.insert(0, str(KOK / "tools")); import makara_ders; metin = makara_ders.onek(metin) + metin
                except Exception:
                    pass
                metin = on_ek_kur(model, metin)
                metin = ogren_blok((KOK / istem).read_text(encoding="utf-8")) + metin
                metin += (f"\n\n[bütçe] Hedef ${butce:.2f}: az oku, az dene, ücretsiz araç önce. Hedefi aşman gerekse bile işi YARIM BIRAKMA — "
                          "bitir, doğrula, raporla. Hedefi aştıysan raporda nedenini tek satır yaz.")
                fo = open(CIKTI / f"{ad}.json", "w", encoding="utf-8")
                mcp = None
                if not os.environ.get("CC_MCP_BOS"):  # MCP-AÇ-1: tür bazlı MCP profili; CC_MCP_BOS=1 eski boş config'e döner
                    try:
                        sys.path.insert(0, str(KOK / "tools")); import mcp_profil
                        mcp = CIKTI / f"{ad}.mcp.json"
                        log("MCP", ad, " ".join(mcp_profil.yaz((KOK / istem).read_text(encoding="utf-8"), mcp)))  # ham görev metni: ön ek tür tespitini kirletmesin
                    except Exception as e:
                        mcp = None
                        log("MCP profil hatası", ad, repr(e)[:80])
                argv, env = baslat_argv(efor, model, mcp, zorunlu_arac.ajan_adlari(ad), butce)
                p = subprocess.Popen(argv, cwd=str(hedef), stdin=subprocess.PIPE, stdout=fo, stderr=subprocess.STDOUT,
                                     env=env, creationflags=0x08000000)
                p.stdin.write(metin.encode("utf-8"))
                p.stdin.close()
                calisan[ad] = (p, time.time(), fo, efor, model, bas, istem, kosul, cwd, butce)
                baslayan.add(ad)
                yeniden = [y for y in yeniden if y[0] != ad]
                (CIKTI / f"{ad}.basladi").write_text(time.strftime("%H:%M:%S") + f" pid {p.pid}", encoding="utf-8")
                son = time.time()
                log("BAŞLAT", ad, model, efor or "-", "pid", p.pid, f"RAM %{r}", f"tahmin {tah} MB", "çalışan", len(calisan) + dis)
                break
        time.sleep(30)


if __name__ == "__main__":
    main()
