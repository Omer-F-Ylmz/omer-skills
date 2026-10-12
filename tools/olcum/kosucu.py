"""KÜTÜPHANE-3a/4: ölçüm koşucusu. Sabit görev setini (gorevler.json) `claude -p` ile koşar, gerçek usage + süre +
doğru-araç isabeti + rubrik puanını docs/kutuphane/olcum/<tarih>-<profil>.tsv'ye SATIR SATIR ekler (yarıda kesilen koşu kaybolmaz).
  python tools/olcum/kosucu.py --profil tam[,nameonly] [--gorev G01,G05] [--tavan 12] [--tekrar 1] [--arka]
Profiller profiller.json'da: "ek" = ek `claude` argümanları, "settings" = tools/olcum'a göreli --settings dosyası.
Ayar/env değiştirmez. --arka: ayrık süreçte koşar, günlük .kos/kopru/olcum-arka.log; her çağrı öncesi boş RAM ≥ 6 GB beklenir.
Puan: rubrikteki her madde {"puan": n, "regex": "..."} yanıt metninde eşleşirse n eklenir (toplam 10)."""
import argparse
import ctypes
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DIZIN = Path(__file__).resolve().parent
KOK = DIZIN.parents[1]
CIKTI = KOK / "docs" / "kutuphane" / "olcum"
ARKA_LOG = KOK / ".kos" / "kopru" / "olcum-arka.log"
ROTA = ["--output-format", "stream-json", "--verbose", "--include-hook-events", "--no-session-persistence"]
BASLIK = "gorev\ttekrar\tinput\tcache_creation\tcache_read\toutput\tbaglam\ttur\tsure_sn\tusd\tarac_isabet\tkalite\tskill_n\tmcp_n\taraclar\thata\tjev\tjev_guven"
RAM_ALT_GB = 6.0


def bos_ram_gb():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("y", ctypes.c_ulong), ("t", ctypes.c_ulonglong), ("a", ctypes.c_ulonglong),
                    ("tp", ctypes.c_ulonglong), ("ap", ctypes.c_ulonglong), ("tv", ctypes.c_ulonglong), ("av", ctypes.c_ulonglong),
                    ("e", ctypes.c_ulonglong)]
    try:
        m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        return m.a / 2**30
    except (AttributeError, OSError):
        return 99.0


def pid_canli(pid):
    if os.name == "nt":
        h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
        if not h:
            return False
        kod = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(kod))
        ctypes.windll.kernel32.CloseHandle(h)
        return kod.value == 259
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def ayristir(stdout):
    """stream-json satırları → {usage, usd, sure_ms, metin, araclar, okunan, girdi, init, hook, tur}. Anahtar/istem değeri taşımaz."""
    o = {"usage": {}, "usd": 0.0, "sure_ms": 0, "metin": "", "araclar": [], "okunan": [], "girdi": [], "init": {}, "hook": [], "tur": 0}
    for s in (stdout or "").splitlines():
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if not isinstance(x, dict):
            continue
        t, st = x.get("type"), x.get("subtype")
        if t == "system" and st == "init":
            o["init"] = {k: x.get(k) for k in ("tools", "mcp_servers", "slash_commands", "agents", "skills", "plugins", "model") if k in x}
        elif t == "system" and st and st.startswith("hook"):
            o["hook"].append({k: x.get(k) for k in ("subtype", "hook_name", "hook_event", "exit_code") if k in x})
        elif t == "assistant":
            u = (x.get("message") or {}).get("usage") or {}
            if u and not o["usage"]:
                o["usage_ilk"] = o.get("usage_ilk") or u
            for b in (x.get("message") or {}).get("content") or []:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    ad = b.get("name") or ""
                    if ad == "Skill":
                        ad = "Skill:" + str((b.get("input") or {}).get("skill") or (b.get("input") or {}).get("command") or "")
                    elif ad in ("Task", "Agent"):
                        ad = "Agent:" + str((b.get("input") or {}).get("subagent_type") or "")
                    elif ad == "Read":  # hangi references bölümü okundu: vekil değil kanıt
                        o["okunan"].append(str((b.get("input") or {}).get("file_path") or "").replace("\\", "/"))
                    o["araclar"].append(ad)
                    g = b.get("input") or {}  # dosyaya yazılan/koşturulan çıktı da rubriğe girer (yalnız son metin değil)
                    o["girdi"].extend(str(g[k]) for k in ("content", "new_string", "command") if g.get(k))
        elif t == "result":
            o["usage"] = x.get("usage") or {}
            o["usd"] = x.get("total_cost_usd") or 0.0
            o["sure_ms"] = x.get("duration_ms") or 0
            # Arka plan Agent'ı akışta birden çok result üretir, sonuncusu boş (num_turns 0) → yanıtı ezmesin
            o["metin"] = str(x.get("result") or "") or o["metin"]
            o["tur"] = x.get("num_turns") or o["tur"]
            o["model"] = x.get("modelUsage") or {}
    o["usage"] = o["usage"] or o.get("usage_ilk") or {}
    return o


def jeton(u):
    """(input, cache_creation, cache_read, output)"""
    return (u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))


PENCERESIZ = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW: pencere açılmaz, torunlar (MCP/hook) bu gizli konsolu devralır


def is_olustur():
    """Windows Job Object (KILL_ON_JOB_CLOSE): kapanınca içindeki bütün torun ağacı ölür. Windows dışında None."""
    if os.name != "nt":
        return None
    k = ctypes.windll.kernel32
    k.CreateJobObjectW.restype = ctypes.c_void_p
    k.AssignProcessToJobObject.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    k.SetInformationJobObject.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_ulong]
    k.CloseHandle.argtypes = [ctypes.c_void_p]
    is_ = k.CreateJobObjectW(None, None)

    class Temel(ctypes.Structure):
        _fields_ = [("a", ctypes.c_int64), ("b", ctypes.c_int64), ("LimitFlags", ctypes.c_ulong), ("c", ctypes.c_size_t),
                    ("d", ctypes.c_size_t), ("e", ctypes.c_ulong), ("f", ctypes.c_size_t), ("g", ctypes.c_ulong), ("h", ctypes.c_ulong)]

    class Sinir(ctypes.Structure):
        _fields_ = [("Temel", Temel), ("io", ctypes.c_uint64 * 6), ("i", ctypes.c_size_t * 4)]

    s = Sinir()
    s.Temel.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if not k.SetInformationJobObject(is_, 9, ctypes.byref(s), ctypes.sizeof(s)):  # JobObjectExtendedLimitInformation
        k.CloseHandle(is_)
        return None
    return is_


def is_ata(is_, pr):
    if is_:
        ctypes.windll.kernel32.AssignProcessToJobObject(is_, ctypes.c_void_p(int(pr._handle)))


def is_kapat(is_):
    if is_:
        ctypes.windll.kernel32.CloseHandle(is_)


def calistir(args, env, cwd, timeout):
    """subprocess.run yerine: claude işe atanır, bitişte/timeout'ta iş kapanır → torunlar (remotion studio vb.) ölür. → (stdout, rc, stderr)"""
    is_ = is_olustur()
    pr = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace", env=env, cwd=cwd,
                          creationflags=PENCERESIZ)
    is_ata(is_, pr)  # ponytail: atamadan önce doğan torunlar işte değil; supur() onları yakalar
    try:
        out, err = pr.communicate(timeout=timeout)
        return out, pr.returncode, err
    except subprocess.TimeoutExpired:
        pr.kill()
        is_kapat(is_)
        is_ = None
        out, _ = pr.communicate()
        return out or "", -9, "timeout"
    finally:
        is_kapat(is_)


def supur(ad):
    """Emniyet: komut satırında geçici dizin adı (olcum-xxxx) geçen kalan süreçleri PID ile sonlandır. Ad ile öldürme yok."""
    if os.name != "nt" or not ad:
        return
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -ne $PID -and $_.CommandLine -and $_.CommandLine.Contains('%s') } "
          "| ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" % ad.replace("'", ""))
    try:  # emniyet süpürmesi: cihaz donmasında zaman aşımı koşuyu düşürmez
        subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps], capture_output=True, creationflags=PENCERESIZ, timeout=60)
    except subprocess.TimeoutExpired:
        pass


def kos(istem, ek=(), cwd=None, model=None, timeout=600, butce=3.0):
    """Tek `claude -p`. ANTHROPIC_BASE_URL (headroom vekili) alt süreçte kaldırılır — araçları gizliyor. Boş cwd yoksa geçici boş klasör.
    BROWSER=none: Remotion/Vite vb. tarayıcı/pencere açmaz."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    env["BROWSER"] = "none"
    args = ["claude", "-p", istem, *ROTA, "--max-budget-usd", f"{butce:.2f}", *([] if not model else ["--model", model]), *ek]
    # claude'un yan süreçleri (MCP/hook) klasörü bir süre tutabiliyor → temizlik hatası koşuyu düşürmez
    with tempfile.TemporaryDirectory(prefix="olcum-", ignore_cleanup_errors=True) as bos:
        t = time.monotonic()
        out, rc, err = calistir(args, env, cwd or bos, timeout)
        supur(Path(bos).name)
        sure = round(time.monotonic() - t, 1)
    o = ayristir(out)
    o["sure"], o["rc"], o["hata"] = sure, rc, (err or "").strip().replace("\t", " ").replace("\n", " ")[-200:] if rc else ""
    return o


def puanla(metin, rubrik):
    """Regex rubriği; Windows yol ayırıcısı `\\` olan yanıt `/` bekleyen kalıpla da eşleşir (A01–A03: 5 yerine 10)."""
    duz = metin.replace("\\", "/")
    return min(10, sum(m["puan"] for m in rubrik
                       if re.search(m["regex"], metin, re.I | re.S) or re.search(m["regex"], duz, re.I | re.S)))


def isabet(araclar, beklenen):
    """beklenen = [] → araç gerekmez (1); aksi halde beklenen adlardan biri kullanıldıysa 1 (önek eşleşmesi: 'Skill:' tüm skill'leri sayar).
    Skill ad alanı yok sayılır: 'Skill:anthropic-skills:blender-oturum' 'Skill:blender' ile de eşleşir (claude.ai senkron kopyası)."""
    adlar = [x for a in araclar for x in (a, "Skill:" + a.rsplit(":", 1)[-1]) if a.startswith("Skill:") or x == a]
    return 1 if not beklenen else int(any(a.startswith(b) for a in adlar for b in beklenen))


def profil_ek(p):
    ek = list(p.get("ek") or [])
    if p.get("settings"):
        ek += ["--settings", str((DIZIN / p["settings"]).resolve())]
    return ek


def satir_yaz(yol, satir):
    yeni = not yol.exists()
    with yol.open("a", encoding="utf-8") as f:
        if yeni:
            f.write(BASLIK + "\n")
        f.write(satir + "\n")


def init_yaz(yol, init):
    """Profilin gerçekten uygulandığını gösteren ad listeleri (değer/anahtar yok)."""
    if yol.exists() or not init:
        return
    oz = {}
    for k, v in init.items():
        if k == "tools" and isinstance(v, list):  # araç adları (mcp__netlify__…) gitleaks yanlış alarmı üretiyor → yalnız sayı
            oz[k] = {"toplam": len(v), "mcp": sum(1 for x in v if str(x).startswith("mcp__"))}
        elif isinstance(v, list):
            oz[k] = [x.get("name") if isinstance(x, dict) else x for x in v]
        else:
            oz[k] = v
    yol.write_text(json.dumps(oz, ensure_ascii=False, indent=1), encoding="utf-8")


def jev_doldur(yol, metin_dir, en_fazla=2, tasiyici=None):
    """JEV-1: koşu sonu tek jev_batch → TSV jev/jev_guven (regex rubrik 10'da doyuyor, jev ayırır). Jev erişilemezse TSV aynen kalır."""
    import jev_yargic
    try:
        k = jev_yargic.veri([metin_dir])
        if tasiyici is None:
            sys.path.insert(0, str(DIZIN.parent / "jev"))
            from jev.cekirdek import Tasiyici
            tasiyici = Tasiyici(en_fazla=en_fazla, istek_tavan=len(k) + 10)
        jev_yargic.tsv_doldur(yol, jev_yargic.jev_puanla(k, tasiyici))
        print("jev:", len(k), "yanıt puanlandı", flush=True)
    except Exception as e:  # noqa: BLE001 — jev yardımcı; ölçüm asla düşmez
        print("jev atlandı:", type(e).__name__, flush=True)


def kos_profil(ad, p, gorevler, tarih, tekrar, jev=True):
    ek = profil_ek(p)
    yol = CIKTI / f"{tarih}-{ad}.tsv"
    metin_dir = CIKTI / f"{tarih}-{ad}"  # yanıt metni: LLM yargıç (jev) ile kolları karşılaştırmak için
    for n in range(1, tekrar + 1):
        for g in gorevler:
            bekle = 0
            while bos_ram_gb() < RAM_ALT_GB and bekle < 1800:
                time.sleep(30); bekle += 30
            o = kos(g["istem"], ek, cwd=str(KOK) if g.get("cwd") == "repo" else None)
            init_yaz(CIKTI / f"{tarih}-{ad}-init.json", o["init"])
            metin_dir.mkdir(exist_ok=True)
            (metin_dir / f"{g['id']}-{n}.md").write_text(o["metin"], encoding="utf-8")
            i, cc, cr, out = jeton(o["usage"])
            sn = len(o["init"].get("skills") or []) if o["init"] else 0
            mn = len(o["init"].get("mcp_servers") or []) if o["init"] else 0
            s = "\t".join(str(v) for v in (g["id"], n, i, cc, cr, out, i + cc + cr, o["tur"], o["sure"], round(o["usd"], 4),
                                           isabet(o["araclar"], g["arac"]), puanla("\n".join([o["metin"], *o["girdi"]]), g["rubrik"]), sn, mn,
                                           ",".join(dict.fromkeys(o["araclar"])), o["hata"]))
            satir_yaz(yol, s)
            print(ad, s, flush=True)
    if jev and yol.exists():
        jev_doldur(yol, metin_dir)
    print("->", yol, flush=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profil", default="tam", help="virgüllü profil adları, sırayla koşar")
    p.add_argument("--gorev", help="virgüllü görev kimlikleri (varsayılan hepsi)")
    p.add_argument("--tavan", type=int, default=12, help="profil başına en fazla N görev")
    p.add_argument("--tekrar", type=int, default=1, help="görev başına tekrar")
    p.add_argument("--tarih", default=time.strftime("%Y-%m-%d"))
    p.add_argument("--jevsiz", action="store_true", help="koşu sonu jev puanlamasını atla (varsayılan: tek jev_batch)")
    p.add_argument("--arka", action="store_true", help="ayrık süreçte koş, hemen dön")
    p.add_argument("--bekle-pid", type=int, help="başlamadan önce bu sürecin bitmesini bekle (sıralı kuyruk)")
    ns = p.parse_args(argv)
    if ns.arka:
        arg = [a for a in (argv if argv is not None else sys.argv[1:]) if a != "--arka"]
        ARKA_LOG.parent.mkdir(parents=True, exist_ok=True)
        # her arka koşu kendi günlüğüne yazar: devralınan Windows tutamacı O_APPEND taşımaz, ortak dosyada satırlar ezilir
        yol_log = ARKA_LOG.with_name(f"olcum-arka-{ns.profil.replace(',', '+')}.log")
        log = open(yol_log, "a", encoding="utf-8")
        bayrak = (PENCERESIZ | 0x00000200) if os.name == "nt" else 0  # DETACHED (konsolsuz) üst süreç → claude.exe yeni konsol açıyor, Windows Terminal öne getiriyordu
        pr = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), *arg], stdout=log, stderr=subprocess.STDOUT,
                              stdin=subprocess.DEVNULL, cwd=str(KOK), creationflags=bayrak, close_fds=True)
        print(f"arka pid {pr.pid} · günlük {yol_log}")
        return 0
    profiller = json.loads((DIZIN / "profiller.json").read_text(encoding="utf-8"))
    if ns.bekle_pid:
        while pid_canli(ns.bekle_pid):
            time.sleep(20)
    gorevler = json.loads((DIZIN / "gorevler.json").read_text(encoding="utf-8"))
    if ns.gorev:
        gorevler = [g for g in gorevler if g["id"] in ns.gorev.split(",")]
    gorevler = gorevler[:ns.tavan]
    CIKTI.mkdir(parents=True, exist_ok=True)
    print(time.strftime("%H:%M:%S"), "başla", ns.profil, len(gorevler), "görev ×", ns.tekrar, flush=True)
    for ad in ns.profil.split(","):
        kos_profil(ad, profiller[ad], gorevler, ns.tarih, ns.tekrar, jev=not ns.jevsiz)
    print(time.strftime("%H:%M:%S"), "bitti", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
