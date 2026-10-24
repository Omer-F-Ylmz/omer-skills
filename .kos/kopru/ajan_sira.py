"""RAM'e duyarlı ajan kuyruğu (Desktop 12 Eki 17:05): köprü tavanı (10) doluyken bekleyen görevleri köprüyle AYNI bayraklarla
(opus · hafif: --disable-slash-commands + boş MCP · cc_profil "ajan" (ttl 5m + ajanTut) · istem stdin'den · izin atlama bayrağı YOK) kopuk
claude -p oturumlarında başlatır. Kuyruk: .kos/kopru/ajan-sira.tsv  (ad <TAB> istem dosyası [<TAB> koşul: yol::alt dize [<TAB> efor=medium|high] [<TAB> cwd=<yol>]]).
Efor: mekanik iş (ölçüm koşusu, paketleme, birleştirme, kapı tekrarı) medium; tasarım/mimari/hata ayıklama high (TOKEN-3 K11).
Başlatma koşulu: RAM < ESIK, bu yöneticinin çalışanı < TAVAN, iki başlatma arası >= ARA sn. Durdurma: .kos/kopru/ajan-sira.dur
Çıktı: .kos/kopru/ajan-sira/<ad>.json · günlük .kos/kopru/ajan-sira.log (arka.py ile koşar).
  python arka.py .kos/kopru/ajan-sira.log .kos/kopru/ajan_sira.py"""
import atexit, ctypes, io, json, os, re, subprocess, sys, tempfile, time, uuid
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
import ajan_ram_bekci  # RAM-BEKCI-1: çalışan ajanların alt süreçleri için RAM bekçisi
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


def kural_ilgili(metin):
    """KURAL-BEYİN-1: karttan sonra göreve uyan ≤3 kuralın tam metni (Obsidian Kurallar.md, yerel eşleşme); hata/dosya yok → ''."""
    try:
        sys.path.insert(0, str(KOK / "tools"))
        import kural_uret
        return kural_uret.ilgili(metin) + "\n"
    except Exception:
        return ""
    finally:
        sys.path.pop(0)


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


def oyun_modu():
    """Ömer 24 Eki 09:25: oyun açıkken de arka işler DURMAZ — her zaman False. Oyunu koruyan tek sınır RAM eşiği (esik(), ≤%89).
    Bayrak dosyası (tools/oyun_modu.py) yalnız kayıt için kalır; yeniden durdurma gerekirse .kos/kopru/oyun-modu.durdur dosyası oluştur."""
    if not (K / "oyun-modu.durdur").exists():
        return False
    f = K / "oyun-modu.bayrak"
    return f.exists() and time.time() - f.stat().st_mtime < 60


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


def kok_pidler(calisan):
    """RAM-BEKCI-1: bu yöneticinin ajan kökleri = kendi başlattıkları + .basladi'dan canlı dış çalışanlar."""
    pidler = {v[0].pid for v in calisan.values()}
    for f in CIKTI.glob("*.basladi"):
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and claude_sureci(p[2], f.stat().st_mtime):
            pidler.add(int(p[2]))
    return pidler


def kok_adlari(calisan):
    """RAM-BEKCI-2: kok_pidler ile aynı kökler, iş adıyla: {pid: ad}."""
    adlar = {v[0].pid: ad for ad, v in calisan.items()}
    for f in CIKTI.glob("*.basladi"):
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and claude_sureci(p[2], f.stat().st_mtime):
            adlar.setdefault(int(p[2]), f.stem)
    return adlar


RAM_YENIDEN = 85  # RAM-BEKCI-2: RAM ile kesilen iş (-b) yalnız RAM bunun altına inince yeniden başlar


def ram_kesti_isaretle(ad, r):
    (CIKTI / f"{ad}.ramkesti").write_text(f"{time.strftime('%H:%M:%S')} RAM %{r}", encoding="utf-8")


def ram_kesti_al(ad):
    """İş RAM bekçisince kesildiyse işareti tüketir (bir kez) ve True döner."""
    f = CIKTI / f"{ad}.ramkesti"
    var = f.exists()
    f.unlink(missing_ok=True)
    return var


def ram_yeniden(ad, istem, kosul, ef, mdl, bas, cwd):
    """RAM ile kesilen işin '-b' yeniden satırı; zaten -b ise (ikinci kesilme) None. Efor/model asıl işinki, basamak yükselmez."""
    if ad.endswith("-b"):
        return None
    return (ad + "-b", istem, kosul, ef, mdl, bas or 0, cwd)


def ram_yeniden_hazir(ad, r):
    return not ad.endswith("-b") or r < RAM_YENIDEN


def ram_bekle(calisan):
    """RAM-BEKCI-1/2: RAM >= %87'de ajan alt süreçlerinin en büyüğü bulunur, >= %88'de durdurulur; RAM >= %92'de en büyük ajan ağacının tamamı
    (kök dahil; oyun/Desktop/Headroom/sistem hariç) durdurulur ve iş 'RAM ile kesildi' işaretlenir; ağaç >1.5 GB ya da >60 alt süreçse uyarı.
    Bekçi hatası döngüyü düşürmez."""
    try:  # TARAYICI-KAPI-1: RAM'den bağımsız; ajan ağacındaki opera/msedge kapanır
        ajan_ram_bekci.tarayici_kapat(ajan_ram_bekci.surecler_listele(), kok_pidler(calisan), ajan_ram_bekci.oldur_pidler, log)
    except Exception as e:
        log("tarayici-kapi hata", repr(e)[:120])
    r = ram()
    if r < ajan_ram_bekci.UYARI_RAM:
        return
    try:
        sys.path.insert(0, str(KOK / "tools")); import beyin_dusun
        if r >= ajan_ram_bekci.DUR_ESIK:  # RAM-BEKCI-3: önce ≥600 MB tek kaçak süreç (cerrahi); yoksa aşağıda en yeni ağaç
            durum, h = ajan_ram_bekci.kontrol(r, kok_pidler(calisan), ajan_ram_bekci.surecler_listele(), ajan_ram_bekci.oldur_agac, log)
            if durum == "durdurdu":
                beyin_dusun.olay("ram-bekci", "yonetici", f"RAM %{r} {durum} pid {h[0]} {h[2]} {h[3] // 2**20} MB", True)
                time.sleep(3)
                r = ram()
                if r < ajan_ram_bekci.DUR_ESIK:
                    return
        for _ in range(3):  # RAM düşmediyse sıradaki ağaç (her tur 30 sn beklemeden)
            surecler = ajan_ram_bekci.surecler_listele()
            kokler = kok_adlari(calisan)
            durum, kok, ad = ajan_ram_bekci.agac_kontrol(r, kokler, surecler, ajan_ram_bekci.oldur_pidler, log, UYARI_KOK)
            if durum == "uyari":
                beyin_dusun.olay("ram-bekci", ad, f"RAM %{r} ajan ağacı büyük (kök {kok})", False)
            if durum != "kesildi":
                break
            ram_kesti_isaretle(ad, r)
            log("RAM İLE KESİLDİ", ad, f"RAM %{r}", f"RAM < %{RAM_YENIDEN}'te -b ile yeniden")
            beyin_dusun.olay("ram-bekci", ad, f"RAM %{r} ajan ağacı durduruldu (kök {kok}); RAM < %{RAM_YENIDEN}'te {ad}-b", True)
            time.sleep(3)
            r = ram()
            if r < ajan_ram_bekci.AGAC_ESIK:
                return
        if r < ajan_ram_bekci.ADAY_ESIK or r >= ajan_ram_bekci.DUR_ESIK:  # ≥88 yukarıda işlendi; burada yalnız 87 aday günlüğü
            return
        durum, h = ajan_ram_bekci.kontrol(r, kok_pidler(calisan), ajan_ram_bekci.surecler_listele(), ajan_ram_bekci.oldur_agac, log)
        if durum in ("aday", "durdurdu"):
            beyin_dusun.olay("ram-bekci", "yonetici", f"RAM %{r} {durum} pid {h[0]} {h[2]} {h[3] // 2**20} MB", durum == "durdurdu")
    except Exception as e:
        log("ram-bekci hata", repr(e)[:120])


UYARI_KOK = set()  # RAM-BEKCI-2: uyarı verilmiş (kök pid, tür) çiftleri


KURTAR_TAVAN, KURTAR_TOPLAM, KURTAR_YAS = 2, 3, 6 * 3600  # YÖNETİCİ-BAĞIMSIZ-1 d3: iş başına en çok 2 deneme, açılış başına en çok 3 iş; KURTAR-FİX-1: >6 saatlik iş kurtarılmaz (alarm + Desktop'a soru)
DEVAM = {}  # ad → kesilen oturumun session_id'si (transkript varsa --resume) ya da None (baştan)
DEVAM_ISTEM = "Oturum yönetici/Desktop kapanınca yarıda kesildi. Kaldığın yerden devam et, görevi bitir ve raporla."


def sonuc_var(ad):
    """ad.json'un son JSON satırı claude -p sonucu (type=result) mu? Öldürülen iş sonucu sonda yazdığı için boş/yarım kalır."""
    try:
        for s in reversed((CIKTI / f"{ad}.json").read_text(encoding="utf-8", errors="replace").splitlines()):
            if s.startswith("{"):
                return json.loads(s).get("type") == "result"
    except (OSError, ValueError):
        pass
    return False


def git_var(ad):
    """git log'da görev adı (tam sözcük olarak) geçen commit var mı? KURTAR-FİX-1: iş başka adla/elle bitmiş olabilir."""
    r = subprocess.run(["git", "log", "-1", "--format=%h", "-E", f"--grep=(^|[^A-Za-z0-9-]){re.escape(ad)}($|[^A-Za-z0-9-])"],
                       cwd=KOK, capture_output=True, text=True, errors="replace", creationflags=0x08000000)
    return bool(r.stdout.strip())


def kurtar(satirlar, baslayan):
    """YÖNETİCİ-BAĞIMSIZ-1 d3: kuyruktaki, .basladi'sı olup sonucu olmayan ve süreci ölmüş işleri baslayan'dan çıkarır (yeniden sıraya girer).
    satirlar = kuyruk() satırları (ad, görev dosyası, ...). KURTAR-FİX-1: aynı görev dosyasını kullanan başka satırın sonucu varsa, git log'da
    görev adı geçiyorsa ya da iş >6 saatlikse kurtarma YOK ("KURTAR-ATLA <ad> neden"; yaşlıysa ayrıca beyin alarmı).
    Dönüş {ad: session_id|None}: transkripti diskte olan oturum --resume, yoksa baştan."""
    devam = {}
    for ad, dosya, *_ in satirlar:
        f = CIKTI / f"{ad}.basladi"
        if len(devam) >= KURTAR_TOPLAM or ad not in baslayan or not f.exists() or sonuc_var(ad):
            continue
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and pid_canli(p[2]) and claude_sureci(p[2], f.stat().st_mtime):
            continue
        kardes = next((x[0] for x in satirlar if x[0] != ad and x[1] == dosya and sonuc_var(x[0])), None)
        if kardes:
            log("KURTAR-ATLA", ad, f"aynı görev dosyasıyla {kardes} bitmiş")
            continue
        if git_var(ad):
            log("KURTAR-ATLA", ad, "git log'da görev adı var (iş commit'lenmiş)")
            continue
        if time.time() - f.stat().st_mtime > KURTAR_YAS:
            log("KURTAR-ATLA", ad, "yaş >6 saat; Desktop'a soru: yeniden koşsun mu?")
            try:
                sys.path.insert(0, str(KOK / "tools")); import beyin_dusun
                beyin_dusun.olay("kurtar-atla", ad, f"{ad} >6 saatlik yarım iş, kurtarılmadı; Desktop: yeniden koşsun mu?", True)
            except Exception:
                pass
            continue
        sayac = CIKTI / f"{ad}.kurtar"
        n = int(sayac.read_text(encoding="utf-8") or 0) if sayac.exists() else 0
        if n >= KURTAR_TAVAN:
            continue
        sayac.write_text(str(n + 1), encoding="utf-8")
        sid = p[4] if len(p) >= 5 and p[3] == "sid" else None
        if sid and not any(Path.home().glob(f".claude/projects/*/{sid}.jsonl")):
            sid = None
        devam[ad] = sid
        baslayan.discard(ad)
        log("KURTAR", ad, f"deneme {n + 1}/{KURTAR_TAVAN}", f"--resume {sid}" if sid else "baştan")
    return devam


KILIT = K / "ajan-sira.kilit"  # TEKİL-YÖNETİCİ: "pid saat"; canlı bir başka ajan_sira varsa ikinci kopya çıkar


def ajan_sira_canli(pid):
    """Pid canlı ve komut satırında ajan_sira.py varsa True (pid'i başka süreç almışsa ayrılır)."""
    if not pid_canli(pid):
        return False
    ps = f"(Get-CimInstance Win32_Process -Filter 'ProcessId={int(pid)}').CommandLine"
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, errors="replace", creationflags=0x08000000)
    return "ajan_sira.py" in r.stdout or "yonetici_gorev.py" in r.stdout  # Desktop 18:55: yönetici Görev Zamanlayıcı'dan yonetici_gorev.py adıyla koşuyor; eski kontrol onu ölü sanıyordu


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


def izlenen_mtime():
    """YONETICI-YENILE-1: yöneticinin belleğe yüklediği .kos/kopru ve tools modüllerinin (yonetici_gorev.py dahil) {yol: mtime}'ı."""
    klasorler = (K.resolve(), (KOK / "tools").resolve())
    r = {}
    for m in list(sys.modules.values()):
        f = getattr(m, "__file__", None)
        if f and Path(f).resolve().parent in klasorler:
            try:
                r[str(Path(f).resolve())] = Path(f).stat().st_mtime
            except OSError:
                pass
    return r


def kod_degisti(ilk, simdi=None):
    """İlk görülen mtime'dan farklı olanlar {yol: yeni mtime}; sonradan yüklenen modül ilk görüldüğü mtime ile ilk'e girer."""
    simdi = izlenen_mtime() if simdi is None else simdi
    for f, t in simdi.items():
        ilk.setdefault(f, t)
    return {f: t for f, t in simdi.items() if ilk[f] != t}


def derleme_hatalari(degisen):
    """Değişen dosyaları `python -m py_compile` ile derler; hata satırları ["dosya: SyntaxError ..."]."""
    hatalar = []
    for f in degisen:
        r = subprocess.run([sys.executable, "-m", "py_compile", f], capture_output=True, text=True, errors="replace", creationflags=0x08000000)
        if r.returncode:
            hatalar.append(f"{Path(f).name}: {(r.stderr.strip().splitlines() or ['derleme başarısız'])[-1]}")
    return hatalar


def yenile_karar(ilk, onceki, simdi=None):
    """(karar, degisen, hatalar): karar 'yenile' (hepsi derleniyor) | 'alarm' (derleme hatası) | None (değişim yok ya da onceki ile aynı küme)."""
    degisen = kod_degisti(ilk, simdi)
    if not degisen or degisen == onceki:
        return None, degisen, []
    hatalar = derleme_hatalari(degisen)
    return ("alarm" if hatalar else "yenile"), degisen, hatalar


YENILE_BEKLE_SN = 300  # YONETICI-YENILE-2: bekleyen yeniden denemeler yenilemeyi en çok bu kadar tutar


def yenile_hazir(yeniden, yenile_t0, simdi):
    """Çalışan ajanlar yenilemeyi tutmaz (yeni yönetici .basladi'dan devralır, devral); yalnız bellekteki yeniden denemeler tutar, en çok YENILE_BEKLE_SN."""
    return not yeniden or simdi - yenile_t0 >= YENILE_BEKLE_SN


class Devralinan:
    """Eski yöneticinin başlattığı, hâlâ koşan ajan: Popen yerine pid ile izlenir (poll/pid/returncode). rc yalnız sonuç satırından çıkarılır."""

    def __init__(self, ad, pid, basladi):
        self.ad, self.pid, self.basladi, self.returncode = ad, int(pid), basladi, None

    def poll(self):
        if self.returncode is None and not claude_sureci(self.pid, self.basladi):
            self.returncode = 0 if sonuc_var(self.ad) else 1
        return self.returncode


def devral(calisan, satirlar):
    """YONETICI-YENILE-2: .basladi'sı canlı, sonucu olmayan, kuyrukta satırı olan ajanları calisan'a alır → BİTTİ/iş kaydı/denetim yeni yöneticide yazılır.
    satirlar = kuyruk() satırları. Üst basamak yeniden denemesi yok (bas=None)."""
    for ad, istem, kosul, efor, model, _, cwd in satirlar:
        f = CIKTI / f"{ad}.basladi"
        if ad in calisan or not f.exists() or sonuc_var(ad):
            continue
        p = f.read_text(encoding="utf-8", errors="replace").split()
        if not (len(p) >= 3 and p[1] == "pid" and p[2].isdigit() and claude_sureci(p[2], f.stat().st_mtime)):
            continue
        try:
            butce = butce_bul((KOK / istem).read_text(encoding="utf-8"))
        except OSError:
            butce = None
        calisan[ad] = (Devralinan(ad, p[2], f.stat().st_mtime), f.stat().st_mtime, io.StringIO(), efor, model, None, istem, kosul, cwd, butce)
        log("DEVRAL", ad, "pid", p[2])


def yenile_et(degisen):
    """Kendini yeniden başlatır. os.execv atexit çalıştırmaz → kilit elle bırakılır, kalp atışına çıkış izi yazılır."""
    log("YENİLE", ", ".join(sorted(Path(f).name for f in degisen)))
    kilit_sil()
    try:
        import yonetici_kalp
        yonetici_kalp.kalp_yaz(K / "yonetici-kalp.txt", ram(), 0, "YENİLE", "YENİLE")
    except Exception:
        pass
    betik = getattr(sys.modules["__main__"], "__file__", sys.argv[0])  # yonetici_gorev chdir yapar; __main__.__file__ mutlak yoldur
    os.execv(sys.executable, [sys.executable, betik, *sys.argv[1:]])


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


# RAM-1: ajan başına tahmini MB; RAM-BEKCI-3 (24 Eki 15:20, 4 canlı ajan ağacı × 4 örnek): kök claude.exe medyan 755 (+conhost/bash ≈50),
# ağaç toplamı medyan 1106 / en çok 1651 (ruflo 305'e çıkabilir); MCP başına: stalemap 82, chrome-devtools 83, ruflo 82, playwright ≈85, rea 32, premiere 64. render/blender ≈1500
AJAN_MB, MCP_MB, RENDER_MB = 800, {"playwright": 85, "chrome-devtools": 83, "premiere-pro": 64, "ruflo": 82, "stalemap": 82, "rea": 32}, 1500


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
    env.setdefault("MCP_TIMEOUT", "240000")  # RUFLO-BAG-1: yük altında ruflo soğuk başlangıcı ~165 sn; CC varsayılanı 30 sn → MCP 'failed', araçlar hiç gelmiyordu
    env.update(ajan_ram_bekci.TARAYICI_ENV)  # TARAYICI-KAPI-1: BROWSER=none, CI=1, OPEN_BROWSER=false → ajan alt süreçleri Opera açmaz
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
    try:  # BEYIN-CANLI-1: iş bitişi → 2. beyin olay günlüğü (kanıtlı iş · model · $ · KABUL/DUR)
        sys.path.insert(0, str(KOK / "tools")); import beyin_dusun
        beyin_dusun.is_olayi(ad, f"{model}-{efor}" if efor else model, usd, dk, ok, j)
    except Exception:
        pass
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


NIHAI_SATIR = "NİHAİ 31+32"


def gorev_yolu_satir(istem):
    """Ajan görev dosyasını yanlış klasörde aramasın: istem yolunu mutlak yola çevirip isteme satır olarak ekler."""
    return f"\n[görev dosyası] {(KOK / istem).resolve()} (mutlak yol; gorev/ değil, yazıldığı yer burası)"


def nihai_kapi(ad, metin, simdi=None):
    """NİHAİ-KAPI-1 başlama kapısı: görev metninde 'NİHAİ 31+32' satırı ve beyin bekçisi canlı (son olay ≤5 dk) değilse sebep döner (iş başlamaz), tamsa None.
    Eksik satırı yönetici eklemez (görev yazanın işi); sebep ajan-sira loguna çağıranca, beyne 'kapi' olayı + Desktop için beyin-alarm.txt'ye yazılır."""
    import beyin_dusun
    sebep = None
    if NIHAI_SATIR not in metin:
        sebep = f"görevde '{NIHAI_SATIR}' satırı yok"
    else:
        canli, s = beyin_dusun.bekci_canli(simdi)
        sebep = None if canli else s
    if sebep:
        beyin_dusun.olay("kapi", ad, f"BAŞLAMADI {ad}: {sebep}", True)
        beyin_dusun._yaz_bayt(beyin_dusun.ALARM, f"{time.strftime('%d %H:%M')} NİHAİ-KAPI: {ad} başlamadı — {sebep}\n")
    return sebep


ARA_ARALIK = 100  # sn; döngü 30 sn adımlı, 120 eşiği 2.0–2.6 dk veriyordu
YONETICI_OLAY = ("ara", "kapi", "is", "denetim", "maliyet", "kurtar")  # yöneticinin kendi olayları iş oturumunun beyin yazımı sayılmaz


def nihai_bitis(ad, t0, t1):
    """NİHAİ-KAPI-1 4b bitiş kapısı: iş penceresinde (t0..t1) beyne ≥1 olay/2 dk ve ruflo pattern-store izi yoksa eksik listesi döner + 'KISMI-NİHAİ' beyin hata olayı + Desktop alarmı.
    Not: olaylar iş adıyla etiketli değil; pencere içindeki tüm oturum olayları sayılır (eşzamanlı oturum varsa gevşek)."""
    import beyin_dusun
    olaylar, _ = beyin_dusun._olay_oku(0)
    pen = [o for o in olaylar if t0 <= o["t"] <= t1 and o["tur"] not in YONETICI_OLAY]
    dk, eksik = max((t1 - t0) / 60, 1), []
    if len(pen) < dk / 2:
        eksik.append(f"beyin olayı {len(pen)} < {dk / 2:.0f} (≥1/2 dk)")
    if not any("pattern-store" in o["arac"] or "pattern-store" in o["ozet"] for o in pen):
        eksik.append("ruflo pattern-store izi yok")
    if eksik:
        msg = f"KISMI-NİHAİ {ad}: " + "; ".join(eksik)
        beyin_dusun.olay("kapi", ad, msg, True)
        beyin_dusun._yaz_bayt(beyin_dusun.ALARM, f"{time.strftime('%d %H:%M')} {msg}\n")
    return eksik


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
    DEVAM.update(kurtar(kuyruk(), baslayan))  # d3: Desktop/yönetici kapanınca ölen işler yeniden sıraya
    devral(calisan, kuyruk())  # YONETICI-YENILE-2: yenilemeden önceki yöneticinin hâlâ koşan ajanları izlenmeye devam eder
    log(f"başladı · tavan {tavan()} · RAM eşiği %{esik()} · önceden başlamış {len(baslayan)} · dış çalışan {dis_calisan(set())}")
    ara_t, kapi_t, yarim_t = 0.0, {}, 0.0
    izle, son_degisen, yenile, yenile_t0 = izlenen_mtime(), {}, False, 0.0  # YONETICI-YENILE-1: kod değişince kendini yeniler; çalışanları yeni yönetici devralır (YENILE-2)
    while True:
        if time.time() - ara_t >= ARA_ARALIK:  # BEYIN-CANLI-1: çalışan her ajan için 2 dk'da bir ara olay + bekçi (sessiz ölüm yok)
            ara_t = time.time()
            try:
                sys.path.insert(0, str(KOK / "tools")); import beyin_dusun
                for ad_, v in list(calisan.items()):
                    beyin_dusun.ara_olay(ad_, (ara_t - v[1]) / 60)
                beyin_dusun.bekci(len(calisan))
            except Exception:
                pass
        ram_bekle(calisan)  # RAM-BEKCI-1: çalışan ajanların alt süreçleri (iş başlatma kapısı aşağıda ayrı)
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
                ram_kesti = ram_kesti_al(ad)  # RAM-BEKCI-2: bekçi kesti → basamak yükselmez, araç denetimi/devam turu yok; RAM < %85'te -b
                if ram_kesti and (yb := ram_yeniden(ad, istem, kosul, ef, mdl, bas, cwd)) and yb[0] not in tekrar:
                    yeniden.append(yb)
                    tekrar.add(yb[0])
                    log("YENİDEN", ad, f"RAM ile kesildi → {yb[0]} (RAM < %{RAM_YENIDEN}'te)")
                try:
                    if eksik_n := nihai_bitis(ad, t0, time.time()):
                        log("KISMI-NİHAİ", ad, "; ".join(eksik_n))
                except Exception as e:
                    log("nihai_bitis hata", repr(e)[:120])
                if bas is not None and not ok and not ram_kesti and ad not in tekrar and ad not in BUTCE_ASTI and bas + 1 < len(MERDIVEN):  # bütçe dolan iş üst modelle yeniden koşmaz
                    yeniden.append((ad + "-r", istem, kosul, None, None, bas + 1, cwd))
                    tekrar.add(ad + "-r")
                    log("YENİDEN", ad, "→ bir üst basamak", MERDIVEN[bas + 1])
                den = None if ram_kesti else zorunlu_arac.denetle(ad)  # ZORUNLU-ARAÇ-1: döküm sayımı; arac_eksik → aynı görev bir kez eksik araç ekiyle yeniden
                if den and den["durum"] != "ok":
                    log("DENETİM", ad, den["durum"], "eksik:", ", ".join(den["eksik"]))
                    try:
                        import beyin_dusun; beyin_dusun.olay("denetim", ad, f"{den['durum']} eksik: {', '.join(den['eksik'])}", True)  # BEYIN-CANLI-1
                    except Exception:
                        pass
                    yeni, dk = zorunlu_arac.devam(ad, den)  # ARAÇ-KAPI-1: üç işaretten biri → en fazla 2 devam turu (Haiku), sonra DUR
                    if zorunlu_arac.YENIDEN and dk == "devam" and yeni not in tekrar:
                        yeniden.append((yeni, zorunlu_arac.yeniden_istem(ad, istem, zorunlu_arac.eksik_liste(den), yeni), kosul, ef, mdl, bas or 0, cwd))  # asıl işin efor/modeli
                        tekrar.add(yeni)
                    elif dk == "dur":
                        log("DUR", ad, "2 devam turundan sonra hâlâ eksik:", ", ".join(zorunlu_arac.eksik_liste(den)))
                subprocess.Popen([sys.executable, str(KOK / "tools" / "beyin_kayit.py"), ad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)  # BEYIN-KAYIT-1: ikinci beyne yaz (arka plan, beklemez)
                del calisan[ad]
        try:  # ARKA-KALICI-1: ajanların yazdığı uzun iş istekleri burada (ajandan bağımsız) başlar
            arka_istek.isle(log=log)
        except Exception as e:
            log("arka-istek hata", repr(e)[:120])
        if time.time() - yarim_t >= 600:  # YARIM-BEKCI-1: 10 dk'da bir yarım iş taraması (H5/H6 otomatik düzelir, H1–H4 yalnız log + yarim.tsv)
            yarim_t = time.time()
            try:
                import yarim_bekci
                for s_ in yarim_bekci.calistir(K, KOK)[1]:
                    log(s_)
            except Exception as e:
                log("yarim_bekci hata", repr(e)[:120])
        karar, son_degisen, hatalar = yenile_karar(izle, son_degisen)  # YONETICI-YENILE-1: derleme hatası varsa yenileme yok, ALARM
        if karar == "alarm":
            yenile = False
            log("ALARM", "YENİLE yok · derleme hatası:", "; ".join(hatalar))
            try:
                import beyin_dusun; beyin_dusun.olay("yenile-alarm", "yonetici", f"kod değişti ama derlenmiyor: {'; '.join(hatalar)}"[:300], True)
            except Exception:
                pass
        elif karar == "yenile":
            yenile, yenile_t0 = True, yenile_t0 if yenile else time.time()
            log("YENİLE BEKLE", ", ".join(sorted(Path(f).name for f in son_degisen)), f"· çalışan {len(calisan)} (yeni yönetici devralır) · bekleyen deneme {len(yeniden)}")
        if yenile and yenile_hazir(yeniden, yenile_t0, time.time()):
            try:
                yenile_et(son_degisen)
            except OSError as e:  # execv başarısız: kilidi geri al, eski kodla sürdür
                yenile = False
                kilit_al()
                log("ALARM", "YENİLE execv hatası", repr(e)[:120])
        bekleyen = [y for y in yeniden if not y[0].endswith(("-a", "-a2"))] + [x for x in kuyruk() if x[0] not in baslayan] + [y for y in yeniden if y[0].endswith(("-a", "-a2"))]  # devam turları ana işlerin arkasında
        if yenile:  # kuyruktan yeni iş yok; bellekteki yeniden denemeler restart'ta kaybolmasın diye bitirilir
            bekleyen = list(yeniden)
        dis = dis_calisan(set(calisan))
        if not bekleyen and not calisan and not dis:  # 22 Eki (Ömer): kuyruk boşalınca ÇIKMA — sonradan eklenen işler başlamıyordu; bekle
            if "bos" not in uyari:
                log("kuyruk boş, bekleniyor (yeni satır gelince başlar)")
                uyari.add("bos")
            time.sleep(60)
            continue
        uyari.discard("bos")
        r = ram()
        if not DUR.exists() and not oyun_modu() and len(calisan) + dis < tavan() + (3 if r < esik() - 10 else 0) and r < esik() and time.time() - son >= ARA:  # RAM-1: RAM boşken tavan +3; asıl koruma aday başına tahmin kapısı
            for ad, istem, kosul, efor, model, bas, cwd in bekleyen:
                if not ram_yeniden_hazir(ad, r):  # RAM-BEKCI-2: RAM ile kesilen iş RAM < %85'e inene dek bekler
                    continue
                if ("k", ad) not in uyari:  # ZORUNLU-ARAÇ-1 d4: koşul görev dosyasının kendinde geçiyorsa erken başlar
                    uyari.add(("k", ad))
                    if u := zorunlu_arac.kosul_uyari(kosul, istem):
                        log("KOŞUL UYARI", ad, u)
                if not kosul_tamam(kosul):
                    continue
                hedef = cwd_hedef(cwd)
                if hedef is None:
                    if ad not in uyari:
                        log("cwd yok", ad, cwd)
                        uyari.add(ad)
                    continue
                if time.time() - kapi_t.get(ad, 0) < 120:  # NİHAİ-KAPI-1: kapalı iş 2 dk'da bir yeniden denetlenir (beyne/alarma tekrar yazmaz)
                    continue
                if sebep := nihai_kapi(ad, (KOK / istem).read_text(encoding="utf-8")):
                    kapi_t[ad] = time.time()
                    if (("n", ad, sebep)) not in uyari:
                        uyari.add(("n", ad, sebep))
                        log("KAPI BAŞLAMADI", ad, sebep)
                    continue
                kapi_t.pop(ad, None)
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
                metin = arac_onek(str(hedef) if cwd else None) + kural_ilgili(metin) + zorunlu_arac.blok(ad, metin) + ders_onek(metin) + ordu_onek() + ordu_on_ozet(ad, metin) + metin  # ZORUNLU-ARAÇ-1: ön uçuş
                try:  # MAKARA aktarım: kasadan ilgili 3-5 ders satırı (≤600 jeton); hata kuyruğu bozmaz
                    sys.path.insert(0, str(KOK / "tools")); import makara_ders; metin = makara_ders.onek(metin) + metin
                except Exception:
                    pass
                metin = on_ek_kur(model, metin)
                metin = ogren_blok((KOK / istem).read_text(encoding="utf-8")) + metin
                metin += (f"\n\n[bütçe] Hedef ${butce:.2f}: az oku, az dene, ücretsiz araç önce. Hedefi aşman gerekse bile işi YARIM BIRAKMA — "
                          "bitir, doğrula, raporla. Hedefi aştıysan raporda nedenini tek satır yaz.")
                metin += f"\n[ara kayıt] Uzun işte her parça sonunda commit ya da .kos/kopru/ara/{ad}.md ilerleme notu yaz; yönetici kesilirse iş buradan sürer."  # d4
                metin += gorev_yolu_satir(istem)  # NİHAİ-DÜZELT-2 C: görev dosyası MUTLAK yol
                try:
                    sys.path.insert(0, str(KOK / "tools")); import mcp_profil; metin += mcp_profil.codemode()  # CODE-MODE-AB-1: CC_CODEMODE=1
                except Exception:
                    pass
                kesik = DEVAM.pop(ad, None)  # d3: kurtarılan iş transkripti varsa aynı oturumdan sürer
                sid = kesik or str(uuid.uuid4())
                if kesik:
                    metin = DEVAM_ISTEM
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
                argv += ["--resume" if kesik else "--session-id", sid]
                p = subprocess.Popen(argv, cwd=str(hedef), stdin=subprocess.PIPE, stdout=fo, stderr=subprocess.STDOUT,
                                     env=env, creationflags=0x08000000)
                p.stdin.write(metin.encode("utf-8"))
                p.stdin.close()
                calisan[ad] = (p, time.time(), fo, efor, model, bas, istem, kosul, cwd, butce)
                baslayan.add(ad)
                yeniden = [y for y in yeniden if y[0] != ad]
                (CIKTI / f"{ad}.basladi").write_text(time.strftime("%H:%M:%S") + f" pid {p.pid} sid {sid}", encoding="utf-8")
                son = time.time()
                log("BAŞLAT", ad, model, efor or "-", "pid", p.pid, f"RAM %{r}", f"tahmin {tah} MB", "çalışan", len(calisan) + dis)
                break
        time.sleep(30)


if __name__ == "__main__":
    main()
