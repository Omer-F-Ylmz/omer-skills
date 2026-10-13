"""İş 4 davranış kapısı: A canlı SessionStart, B yamalı kopya (--plugin-dir; canlı iki plugin yalnız bu alt süreçte kapalı).
Tek istem/kol (2 claude -p). Ölçü: araç sırası, ctx_* payı, Skill çağrısı. python kapi4.py > kapi4.out"""
import ctypes, importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
EV = Path.home() / ".claude"
spec = importlib.util.spec_from_file_location("is4", KOK / "onay" / "token_8_is4_uygula.py")
is4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(is4)

ISTEM = ("Bu repoda tools/ altındaki .py dosyalarının satır sayılarına göre en büyük 5 dosyayı ver; ayrıca son 40 commit "
         "mesajında en sık geçen 5 kelimeyi say. Hiçbir dosyayı değiştirme. Kısa yanıt ver.")
PLUGINLER = {"superpowers@claude-plugins-official": "plugins/cache/claude-plugins-official/superpowers/6.4.1",
             "context-mode@context-mode": "plugins/cache/context-mode/context-mode/1.0.169"}


def ram():  # omniroute1/pilot.py ile aynı
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def kos(kol, ek):
    if ram() >= 88:
        return {"kol": kol, "hata": "RAM>=88"}
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
    cmd = ["claude", "-p", ISTEM, "--output-format", "stream-json", "--verbose", "--max-turns", "15"] + ek
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, cwd=KOK, timeout=900)
    araclar, sonuc, init = [], {}, {}
    for s in r.stdout.splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        if o.get("subtype") == "init":
            init = {"plugin": [x.get("path", x.get("name")) for x in o.get("plugins", [])], "mcp": [x.get("name") for x in o.get("mcp_servers", [])]}
        if o.get("type") == "assistant":
            araclar += [c["name"] for c in o["message"]["content"] if c.get("type") == "tool_use"]
        if o.get("type") == "result":
            sonuc = {k: o.get(k) for k in ("num_turns", "is_error", "total_cost_usd")}
    ctx = sum("ctx_" in a for a in araclar)
    veri = sum(a in ("Bash", "Read", "Grep", "Glob") or "ctx_" in a for a in araclar)
    return {"kol": kol, "araclar": araclar, "ctx_payi": f"{ctx}/{veri}", "skill": araclar.count("Skill"), **sonuc, **init}


def main():
    tmp = Path(tempfile.mkdtemp(prefix="token8-kapi4-"))
    dizinler = []
    for anahtar, goreli in PLUGINLER.items():
        hedef = tmp / ".claude" / goreli
        shutil.copytree(EV / goreli, hedef, ignore=shutil.ignore_patterns(".git"))
        dizinler += ["--plugin-dir", str(hedef)]
    assert is4.main(["uygula"], tmp / ".claude") == 0
    kapat = json.dumps({"enabledPlugins": {k: False for k in PLUGINLER}})
    for kol, ek in (("A", []), ("B", dizinler + ["--settings", kapat])):
        print(json.dumps(kos(kol, ek), ensure_ascii=False), flush=True)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
