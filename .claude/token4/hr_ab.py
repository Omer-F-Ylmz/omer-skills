"""TOKEN-4 A2 kapı: Headroom HEADROOM_STABLE_BOUNDARY_BREAKPOINT A/B. İki taze vekil ayrı portta (A=0 kapalı, B varsayılan);
env yalnız vekil sürecinde, taban URL yalnız çocuğun --settings env'inde. Global ayar/kullanıcı ortamı/Headroom config değişmez.
Görev ≥20 bloklu mesaj üretir (22 paralel Read + 22 paralel Grep). Sıra A,B,A,B; bitince vekiller kapanır.
  python hr_ab.py [n=2]"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / "tools"))
import cc_profil

HR = Path(os.environ["LOCALAPPDATA"]) / "Headroom/headroom/runtime/venv/Scripts/headroom.exe"  # canlı 6768 ile aynı kurulum
DIZ = Path(__file__).parent
KOL = {"A": (6791, {"HEADROOM_STABLE_BOUNDARY_BREAKPOINT": "0"}), "B": (6792, {})}
DOSYA = sorted(p.relative_to(KOK).as_posix() for p in (KOK / "tools").glob("*.py"))[:22]
ISTEM = ("Araçları tam şu sırayla kullan, her adımı TEK yanıtta paralel çağrılarla yap:\n"
         f"1) Şu {len(DOSYA)} dosyanın her birini Read ile limit 8 oku (hepsi tek yanıtta): " + ", ".join(DOSYA) + "\n"
         "2) Aynı dosyaların her birinde Grep ile '^def ' desenini output_mode count ile say (hepsi tek yanıtta).\n"
         "3) En çok def'li 3 dosyayı Read ile offset 1 limit 40 oku (tek yanıtta).\n"
         "Sonra her dosya için tek satır yaz: yol · def sayısı · ilk satırdaki docstring'in 6 kelimelik özeti.")


def adimlar(sid):
    j = Path.home() / ".claude/projects/C--Projeler-omer-skills" / f"{sid}.jsonl"
    gor, s = set(), []
    for satir in j.open(encoding="utf-8", errors="replace") if j.is_file() else []:
        try: o = json.loads(satir)
        except ValueError: continue
        m = o.get("message")
        if o.get("type") == "assistant" and isinstance(m, dict) and isinstance(m.get("usage"), dict) and m.get("id") not in gor:
            gor.add(m["id"]); u = m["usage"]
            s.append((u.get("input_tokens") or 0, u.get("cache_creation_input_tokens") or 0, u.get("cache_read_input_tokens") or 0))
    return s


def kos(kol, port):
    a, e = cc_profil.kur("ajan", ek_ayar={"env": {"ANTHROPIC_BASE_URL": f"http://127.0.0.1:{port}"}}, gecici=DIZ / f"profil-{kol}")
    argv = [r"C:\Users\pc\.local\bin\claude.exe", "-p", "--output-format", "json", "--model", "opus",
            "--allowedTools", "Read,Grep", "--disable-slash-commands", *a]
    t = time.time()
    p = subprocess.run(argv, input=ISTEM.encode(), capture_output=True, cwd=str(KOK), env={**os.environ, **e},
                       creationflags=0x08000000, timeout=900)
    try: o = json.loads(p.stdout)
    except ValueError: return {"kol": kol, "rc": p.returncode, "hata": p.stdout[:200].decode("utf-8", "replace")}
    s = adimlar(o.get("session_id", ""))
    durma = sum(1 for g, cw, cr in s if cw == 0 and g >= 3000)
    agir = sum(g * 1 + cw * 1.25 + cr * 0.1 for g, cw, cr in s)
    return {"kol": kol, "sn": round(time.time() - t), "adim": len(s), "durma": durma, "g": sum(x[0] for x in s),
            "cw": sum(x[1] for x in s), "cr": sum(x[2] for x in s), "agirlikli": round(agir), "usd": o.get("total_cost_usd"),
            "sonuc": (o.get("result") or "")[:4000], "sid": o.get("session_id"), "adimlar": s}


def ram():
    import ctypes
    class M(ctypes.Structure): _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)); return m.yuk


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    # Desktop 22:20: vekiller TEK SEFERDE biri (ikisi aynı anda ~2 GB), yalnız RAM <%75 iken
    for kol in (sys.argv[1] if len(sys.argv) > 1 else "AB"):
        if ram() >= 75: sys.exit(f"RAM %{ram()} ≥75, dur")
        port, env = KOL[kol]
        v = subprocess.Popen([str(HR), "proxy", "--port", str(port), "--no-http2", "--no-rate-limit"],
                             env={**os.environ, **env}, stdout=open(DIZ / f"hr_ab_{kol}.log", "w"),
                             stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x08000000)
        try:
            for _ in range(60):
                try: urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2); break
                except Exception: time.sleep(2)
            else: sys.exit(f"vekil {port} açılmadı")
            r = kos(kol, port)
            with open(DIZ / "hr_ab.jsonl", "a", encoding="utf-8") as f: f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print({k: v for k, v in r.items() if k not in ("sonuc", "adimlar")}, flush=True)
        finally:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(v.pid)], capture_output=True, creationflags=0x08000000)
            print(f"vekil {kol} kapandı", flush=True)
