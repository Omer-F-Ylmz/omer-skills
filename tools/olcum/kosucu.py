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
BASLIK = "gorev\ttekrar\tinput\tcache_creation\tcache_read\toutput\tbaglam\ttur\tsure_sn\tusd\tarac_isabet\tkalite\tskill_n\tmcp_n\taraclar\thata"
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
    """stream-json satırları → {usage, usd, sure_ms, metin, araclar, init, hook, tur}. Anahtar/istem değeri taşımaz."""
    o = {"usage": {}, "usd": 0.0, "sure_ms": 0, "metin": "", "araclar": [], "init": {}, "hook": [], "tur": 0}
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
                    o["araclar"].append(ad)
        elif t == "result":
            o["usage"] = x.get("usage") or {}
            o["usd"] = x.get("total_cost_usd") or 0.0
            o["sure_ms"] = x.get("duration_ms") or 0
            o["metin"] = str(x.get("result") or "")
            o["tur"] = x.get("num_turns") or 0
    o["usage"] = o["usage"] or o.get("usage_ilk") or {}
    return o


def jeton(u):
    """(input, cache_creation, cache_read, output)"""
    return (u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0))


def kos(istem, ek=(), cwd=None, model=None, timeout=600, butce=3.0):
    """Tek `claude -p`. ANTHROPIC_BASE_URL (headroom vekili) alt süreçte kaldırılır — araçları gizliyor. Boş cwd yoksa geçici boş klasör."""
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_BASE_URL"}
    args = ["claude", "-p", istem, *ROTA, "--max-budget-usd", f"{butce:.2f}", *([] if not model else ["--model", model]), *ek]
    # claude'un yan süreçleri (MCP/hook) klasörü bir süre tutabiliyor → temizlik hatası koşuyu düşürmez
    with tempfile.TemporaryDirectory(prefix="olcum-", ignore_cleanup_errors=True) as bos:
        t = time.monotonic()
        try:
            r = subprocess.run(args, capture_output=True, encoding="utf-8", errors="replace", env=env, cwd=cwd or bos, timeout=timeout)
            out, rc, err = r.stdout, r.returncode, r.stderr
        except subprocess.TimeoutExpired as e:
            out, rc, err = (e.stdout or "") if isinstance(e.stdout, str) else "", -9, "timeout"
        sure = round(time.monotonic() - t, 1)
    o = ayristir(out)
    o["sure"], o["rc"], o["hata"] = sure, rc, (err or "").strip().replace("\t", " ").replace("\n", " ")[-200:] if rc else ""
    return o


def puanla(metin, rubrik):
    return min(10, sum(m["puan"] for m in rubrik if re.search(m["regex"], metin, re.I | re.S)))


def isabet(araclar, beklenen):
    """beklenen = [] → araç gerekmez (1); aksi halde beklenen adlardan biri kullanıldıysa 1 (önek eşleşmesi: 'Skill:' tüm skill'leri sayar)."""
    return 1 if not beklenen else int(any(a.startswith(b) for a in araclar for b in beklenen))


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


def kos_profil(ad, p, gorevler, tarih, tekrar):
    ek = profil_ek(p)
    yol = CIKTI / f"{tarih}-{ad}.tsv"
    for n in range(1, tekrar + 1):
        for g in gorevler:
            bekle = 0
            while bos_ram_gb() < RAM_ALT_GB and bekle < 1800:
                time.sleep(30); bekle += 30
            o = kos(g["istem"], ek, cwd=str(KOK) if g.get("cwd") == "repo" else None)
            init_yaz(CIKTI / f"{tarih}-{ad}-init.json", o["init"])
            metin_dir = CIKTI / f"{tarih}-{ad}"  # yanıt metni: LLM yargıç (jev) ile kolları karşılaştırmak için
            metin_dir.mkdir(exist_ok=True)
            (metin_dir / f"{g['id']}-{n}.md").write_text(o["metin"], encoding="utf-8")
            i, cc, cr, out = jeton(o["usage"])
            sn = len(o["init"].get("skills") or []) if o["init"] else 0
            mn = len(o["init"].get("mcp_servers") or []) if o["init"] else 0
            s = "\t".join(str(v) for v in (g["id"], n, i, cc, cr, out, i + cc + cr, o["tur"], o["sure"], round(o["usd"], 4),
                                           isabet(o["araclar"], g["arac"]), puanla(o["metin"], g["rubrik"]), sn, mn,
                                           ",".join(dict.fromkeys(o["araclar"])), o["hata"]))
            satir_yaz(yol, s)
            print(ad, s, flush=True)
    print("->", yol, flush=True)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profil", default="tam", help="virgüllü profil adları, sırayla koşar")
    p.add_argument("--gorev", help="virgüllü görev kimlikleri (varsayılan hepsi)")
    p.add_argument("--tavan", type=int, default=12, help="profil başına en fazla N görev")
    p.add_argument("--tekrar", type=int, default=1, help="görev başına tekrar")
    p.add_argument("--tarih", default=time.strftime("%Y-%m-%d"))
    p.add_argument("--arka", action="store_true", help="ayrık süreçte koş, hemen dön")
    p.add_argument("--bekle-pid", type=int, help="başlamadan önce bu sürecin bitmesini bekle (sıralı kuyruk)")
    ns = p.parse_args(argv)
    if ns.arka:
        arg = [a for a in (argv if argv is not None else sys.argv[1:]) if a != "--arka"]
        ARKA_LOG.parent.mkdir(parents=True, exist_ok=True)
        # her arka koşu kendi günlüğüne yazar: devralınan Windows tutamacı O_APPEND taşımaz, ortak dosyada satırlar ezilir
        yol_log = ARKA_LOG.with_name(f"olcum-arka-{ns.profil.replace(',', '+')}.log")
        log = open(yol_log, "a", encoding="utf-8")
        bayrak = 0x00000008 | 0x00000200 if os.name == "nt" else 0
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
        kos_profil(ad, profiller[ad], gorevler, ns.tarih, ns.tekrar)
    print(time.strftime("%H:%M:%S"), "bitti", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
