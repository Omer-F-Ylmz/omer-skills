"""KATEGORI-KAPSAM adim 1: indirilen/kurulan her seyin yerlerini tarar -> docs/envanter/kapsam-ek.tsv
Sutunlar: ad, tur, yol, kaynak_yer, boyut_mb. Salt okuma; yalniz iki cikti dosyasi yazar (tsv + yer sayilari json).
GIZLILIK: .env / ~/.claude.json / kimlik dosyalari OKUNMAZ; claude.ai baglayicilari ve hesaplar yalniz repodaki
docs/envanter/envanter.tsv (tur=baglayici) satirlarindan ad olarak alinir."""
import csv
import json
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
HOME = Path.home()
APPDATA = Path(os.environ.get("APPDATA") or HOME / "AppData/Roaming")
LOCAL = Path(os.environ.get("LOCALAPPDATA") or HOME / "AppData/Local")
CIKTI = KOK / "docs/envanter/kapsam-ek.tsv"
SAYI = KOK / ".kos/kopru/arka/kategori-kapsam-yer-sayilari.json"
ROWS = []
CAPPED = []
ATLA_ADLAR = {".git", "node_modules", "__pycache__", "site-packages", "AppData", ".cache", "python_embeded"}


def ekle(ad, tur, yol, yer, boyut=None):
    ROWS.append((str(ad), tur, str(yol), yer, boyut))


def dirsize(p, sure=12.0):
    p = Path(p)
    try:
        if p.is_file():
            return round(p.stat().st_size / 1048576, 2)
    except OSError:
        return 0.0
    t0, top, yig = time.time(), 0, [str(p)]
    while yig:
        if time.time() - t0 > sure:
            CAPPED.append(str(p))
            break
        d = yig.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            yig.append(e.path)
                        else:
                            top += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return round(top / 1048576, 2)


def tur_dosya_klasor(c):
    if c.is_dir():
        return "repo" if (c / ".git").exists() else "klasor"
    return {".exe": "uygulama-kurulum", ".msi": "uygulama-kurulum", ".zip": "arsiv", ".7z": "arsiv", ".gguf": "model",
            ".safetensors": "model", ".ckpt": "model", ".pt": "model", ".mp4": "medya", ".png": "medya", ".jpg": "medya",
            ".pdf": "belge", ".md": "belge", ".json": "veri", ".tsv": "veri", ".py": "betik"}.get(c.suffix.lower(), "dosya")


def cocuklar(kok, yer, tur_fn):
    kok = Path(kok)
    if kok.is_dir():
        for c in sorted(kok.iterdir()):
            ekle(c.name, tur_fn(c), c, yer)


def calistir(cmd, sure=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=sure, encoding="utf-8", errors="replace",
                           shell=isinstance(cmd, str), env=dict(os.environ))
        return r.stdout
    except Exception:  # noqa: BLE001
        return ""


def projeler():
    kok = Path(r"C:\Projeler")
    for c in sorted(kok.iterdir()):
        ekle(c.name, tur_dosya_klasor(c), c, r"C:\Projeler\*" if c.is_dir() else r"C:\Projeler\(kök dosyalar)")
    sabit = {"_araclar", "araclar", "dis", "uygulamalar", "omer-kutuphaneler", "base-indir", "hermes-kaynak", "_v2x_dl",
             "egolite", "_tara", "_derle", "rea", "autoharness", "gsd-core-omer"}
    for c in sorted(kok.iterdir()):
        if not c.is_dir() or c.name.startswith("omer-skills"):
            continue
        if c.name.startswith(".") or c.name.startswith(("_tmp", "_gecici", "_t30")):
            continue  # onbellek/gecici/uretilmis medya: kurulum degil; ust klasor satiri yine yazilir
        repo_mu = any((c / x).exists() for x in (".git", "package.json", "pyproject.toml"))
        if c.name in sabit or not repo_mu:
            for a in sorted(c.iterdir()):
                if not a.name.startswith(".") and a.name not in ATLA_ADLAR:
                    ekle(f"{c.name}/{a.name}", tur_dosya_klasor(a), a, rf"C:\Projeler\{c.name}\*")


def masaustu():
    masa = HOME / "Desktop"
    for k in sorted(masa.iterdir()):
        if k.name.lower().startswith("claude ile") and k.is_dir():
            ekle(k.name, "klasor", k, "Desktop")
            for c in sorted(k.iterdir()):
                if c.name.startswith("."):
                    continue
                ekle(f"{k.name}/{c.name}", tur_dosya_klasor(c), c, r"Desktop\Claude ile yapılanlar\*")
                n = c.name.lower()
                if c.is_dir() and (n in {"araclar", "araçlar", "projeler", "indir"} or n.startswith("ana-liste")
                                   or n.startswith("blenderolcum")):
                    for a in sorted(c.iterdir()):
                        if not a.name.startswith("."):
                            ekle(f"{c.name}/{a.name}", tur_dosya_klasor(a), a, rf"Desktop\Claude ile yapılanlar\{c.name}\*")
        else:
            ekle(k.name, tur_dosya_klasor(k), k, r"Desktop\(diğer)")
            if k.is_dir() and k.name.lower() in {"araclar", "araçlar"}:
                for a in sorted(k.iterdir()):
                    ekle(f"{k.name}/{a.name}", tur_dosya_klasor(a), a, rf"Desktop\{k.name}\*")
    ortak = Path(r"C:\Users\Public\Desktop")
    if ortak.is_dir():
        for c in ortak.iterdir():
            ekle(c.name, "uygulama-kisayol", c, r"Public\Desktop")


def basit_yerler():
    cocuklar(r"C:\AI", r"C:\AI\*", tur_dosya_klasor)
    cocuklar(HOME / "Downloads", r"Downloads\*", tur_dosya_klasor)
    cocuklar(HOME / ".local/bin", r"~/.local/bin", lambda c: "cli")


def npm_global():
    kok = APPDATA / "npm/node_modules"
    if kok.is_dir():
        for c in sorted(kok.iterdir()):
            if c.name.startswith("@") and c.is_dir():
                for a in sorted(c.iterdir()):
                    ekle(f"{c.name}/{a.name}", "npm-paket", a, r"%APPDATA%\npm")
            elif not c.name.startswith("."):
                ekle(c.name, "npm-paket", c, r"%APPDATA%\npm")
    for c in sorted((APPDATA / "npm").glob("*.cmd")):
        ekle(c.stem, "cli", c, r"%APPDATA%\npm\bin")


def venvler():
    """Sinirli kesif (derin os.walk bu diskte cok yavas): kök/ + kök/*/ + .venv|venv|env cocuklari."""
    bulunan = []
    for tab in (Path(r"C:\Projeler"), Path(r"C:\AI")):
        if not tab.is_dir():
            continue
        for d1 in tab.iterdir():
            if not d1.is_dir() or d1.name in ATLA_ADLAR:
                continue
            adaylar = [d1] + [d1 / x for x in (".venv", "venv", "env")]
            try:
                adaylar += [d2 for d2 in d1.iterdir() if d2.is_dir() and d2.name not in ATLA_ADLAR]
            except OSError:
                pass
            for d in adaylar:
                exe = d / "Scripts/python.exe"
                if (d / "pyvenv.cfg").exists() and exe.exists():
                    bulunan.append(exe)
    return list(dict.fromkeys(bulunan))


def uv_pip():
    for s in calistir("uv tool list", 60).splitlines():
        m = re.match(r"^([A-Za-z0-9_.\-]+)\s+v?([\w.\-+]+)\s*$", s)
        if m:
            ekle(m.group(1), "uv-arac", f"uv tool:{m.group(1)}=={m.group(2)}", "uv tool list")
        elif s.startswith("- "):
            ekle(s[2:].strip(), "cli", "uv tool exe", "uv tool list")
    pys = [p for p in (LOCAL / f"Programs/Python/Python3{v}/python.exe" for v in (11, 12, 13)) if p.exists()]
    pys += venvler()
    pys = list(dict.fromkeys(pys))

    def liste(py):
        o = calistir([str(py), "-m", "pip", "list", "--format=json", "--disable-pip-version-check"], 90)
        try:
            return py, json.loads(o)
        except Exception:  # noqa: BLE001
            return py, []

    with ThreadPoolExecutor(6) as ex:
        for py, paketler in ex.map(liste, pys):
            for p in paketler:
                ekle(p["name"], "pip-paket", f"{py} ({p['version']})", "pip:" + str(py))
    return [str(p) for p in pys]


def modeller():
    for s in calistir("ollama list", 30).splitlines()[1:]:
        k = s.split()
        if k:
            m = re.search(r"([\d.]+)\s*(GB|MB)", s)
            mb = round(float(m.group(1)) * (1024 if m.group(2) == "GB" else 1), 2) if m else None
            ekle(k[0], "model-ollama", "ollama:" + k[0], "ollama list", mb)
    hf = HOME / ".cache/huggingface/hub"
    if hf.is_dir():
        for c in sorted(hf.iterdir()):
            if c.name.startswith(("models--", "datasets--", "spaces--")):
                ekle(c.name.split("--", 1)[1].replace("--", "/"), "model-hf", c, "HuggingFace önbelleği")
    comfy = []
    for tab in (Path(r"C:\AI"), Path(r"C:\Projeler"), HOME / "Desktop" / "Claude ile yapılanlar", HOME / "Documents"):
        if not tab.is_dir():
            continue
        for d1 in tab.iterdir():
            if not d1.is_dir():
                continue
            aday = [d1]
            if d1.name not in ATLA_ADLAR:
                try:
                    aday += [x for x in d1.iterdir() if x.is_dir()]
                except OSError:
                    pass
            comfy += [d for d in aday if (d / "custom_nodes").is_dir() and (d / "models").is_dir()]
    for c in comfy:
        for a in sorted((c / "custom_nodes").iterdir()):
            if a.is_dir() and a.name != "__pycache__":
                ekle(a.name, "comfyui-eklenti", a, f"ComfyUI custom_nodes ({c})")
        for kat in sorted((c / "models").iterdir()):
            if kat.is_dir():
                for dp, dn, fn in os.walk(kat):
                    for f in fn:
                        if f.lower().endswith((".safetensors", ".ckpt", ".pt", ".pth", ".gguf", ".bin", ".onnx", ".sft")):
                            ekle(f, f"model-comfyui/{kat.name}", Path(dp) / f, f"ComfyUI models ({c})")
    return [str(c) for c in comfy]


def winget():
    """Kurulu Windows uygulamalari: Uninstall kayit defteri (winget list bu makinede takiliyor); yalniz DisplayName."""
    import winreg
    gor = set()
    pre = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    wow = "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"
    for hive, yol, yer in ((winreg.HKEY_LOCAL_MACHINE, pre, "Uninstall HKLM"),
                           (winreg.HKEY_LOCAL_MACHINE, wow, "Uninstall HKLM-WOW64"),
                           (winreg.HKEY_CURRENT_USER, pre, "Uninstall HKCU")):
        try:
            k = winreg.OpenKey(hive, yol)
        except OSError:
            continue
        for i in range(winreg.QueryInfoKey(k)[0]):
            try:
                ad = winreg.QueryValueEx(winreg.OpenKey(k, winreg.EnumKey(k, i)), "DisplayName")[0]
            except OSError:
                continue
            if ad and ad not in gor:
                gor.add(ad)
                ekle(ad, "uygulama-windows", ad, yer)


def eklentiler():
    for kok, yer in ((HOME / ".vscode/extensions", "VS Code eklentileri"), (HOME / ".cursor/extensions", "Cursor eklentileri")):
        if kok.is_dir():
            for c in sorted(kok.iterdir()):
                if c.is_dir() and not c.name.startswith("."):
                    ekle(re.sub(r"-\d[\w.\-]*$", "", c.name), "editor-eklenti", c, yer)
    cr = LOCAL / "Google/Chrome/User Data"
    if cr.is_dir():
        for prof in cr.iterdir():
            ex = prof / "Extensions"
            if not ex.is_dir():
                continue
            for idd in ex.iterdir():
                ad = idd.name
                try:
                    v = sorted(idd.iterdir())[-1]
                    m = json.loads((v / "manifest.json").read_text(encoding="utf-8-sig", errors="replace"))
                    ad = m.get("name", ad)
                    if ad.startswith("__MSG_"):
                        anahtar = ad[6:-2].lower()
                        for loc in ("en", "en_US", m.get("default_locale", "en")):
                            lf = v / "_locales" / loc / "messages.json"
                            if lf.exists():
                                mm = json.loads(lf.read_text(encoding="utf-8-sig", errors="replace"))
                                ad = next((val["message"] for k2, val in mm.items() if k2.lower() == anahtar), ad)
                                break
                except Exception:  # noqa: BLE001
                    pass
                ekle(f"{ad} [{idd.name}]", "chrome-eklenti", idd, f"Chrome eklentileri ({prof.name})")
    bl = APPDATA / "Blender Foundation/Blender"
    if bl.is_dir():
        for sur in bl.iterdir():
            ad = sur / "scripts/addons"
            if ad.is_dir():
                for c in sorted(ad.iterdir()):
                    if c.name != "__pycache__":
                        ekle(c.stem, "blender-eklenti", c, f"Blender eklentileri ({sur.name})")
            eks = sur / "extensions"
            for e in eks.glob("*/*") if eks.is_dir() else []:
                if e.is_dir():
                    ekle(e.name, "blender-eklenti", e, f"Blender extensions ({sur.name})")


def claude_alani():
    cl = HOME / ".claude"
    for alt, tur in (("skills", "skill"), ("agents", "ajan"), ("commands", "komut"), ("hooks", "kanca")):
        d = cl / alt
        if d.is_dir():
            for c in sorted(d.iterdir()):
                if not c.name.startswith("."):
                    ekle(c.stem if c.is_file() else c.name, tur, c, f"~/.claude/{alt}")
    for dosya, tur, yer in (("plugins/installed_plugins.json", "plugin", "~/.claude/plugins (kurulu)"),
                            ("plugins/known_marketplaces.json", "plugin-pazaryeri", "~/.claude/plugins (marketplace)")):
        p = cl / dosya
        if p.exists():
            try:
                j = json.loads(p.read_text(encoding="utf-8"))
                for k in (j.get("plugins") or j):
                    ekle(k, tur, p, yer)
            except Exception:  # noqa: BLE001
                pass
    st = cl / "settings.json"
    if st.exists():
        try:
            j = json.loads(st.read_text(encoding="utf-8"))
            for k in (j.get("enabledPlugins") or {}):
                ekle(k, "plugin", st, "~/.claude/settings.json enabledPlugins")
            for k in (j.get("mcpServers") or {}):
                ekle(k, "mcp", st, "~/.claude/settings.json mcpServers")
        except Exception:  # noqa: BLE001
            pass
    dc = APPDATA / "Claude/claude_desktop_config.json"
    if dc.exists():
        try:
            for k in (json.loads(dc.read_text(encoding="utf-8")).get("mcpServers") or {}):
                ekle(k, "mcp", dc, "Claude Desktop config MCP")
        except Exception:  # noqa: BLE001
            pass
    dist = KOK / "dist"
    if dist.is_dir():
        for c in sorted(dist.rglob("*.zip")):
            ekle(c.stem, "skill-zip", c, r"omer-skills\dist (claude.ai yükleme)")


def hesaplar():
    """claude.ai baglayicilari + hesap/servis adlari: yalniz repodaki envanter.tsv (tur=baglayici) ad sutunu."""
    p = KOK / "docs/envanter/envanter.tsv"
    with open(p, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r.get("tur") == "baglayici":
                ekle(r["ad"], "claude-ai-baglayici", p, "claude.ai bağlayıcıları / hesaplar (yalnız ad; envanter.tsv)")


def main():
    t0 = time.time()
    sayi = {}
    for ad, fn in (("projeler", projeler), ("masaustu", masaustu), ("basit", basit_yerler), ("npm", npm_global),
                   ("uv_pip", uv_pip), ("modeller", modeller), ("winget", winget), ("eklentiler", eklentiler),
                   ("claude", claude_alani), ("hesaplar", hesaplar)):
        n0 = len(ROWS)
        try:
            ek = fn()
        except Exception as e:  # noqa: BLE001
            ek = f"HATA {type(e).__name__}: {str(e)[:120]}"
        sayi[ad] = {"satir": len(ROWS) - n0, "not": ek}
        print(ad, len(ROWS) - n0, f"{time.time() - t0:.0f}s", flush=True)
    hedef = {}
    for i, r in enumerate(ROWS):
        if r[4] is None and os.path.isabs(r[2]) and os.path.exists(r[2]) and r[1] not in {
                "pip-paket", "mcp", "plugin", "plugin-pazaryeri", "claude-ai-baglayici"}:
            hedef.setdefault(r[2], []).append(i)
    with ThreadPoolExecutor(16) as ex:
        for yol, mb in zip(hedef, ex.map(dirsize, hedef)):
            for i in hedef[yol]:
                ROWS[i] = ROWS[i][:4] + (mb,)
    gor, cikti = set(), []
    for r in ROWS:
        if r[:4] not in gor:
            gor.add(r[:4])
            cikti.append(r)
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        f.write("ad\ttur\tyol\tkaynak_yer\tboyut_mb\n")
        for r in cikti:
            f.write("\t".join(re.sub(r"[\t\r\n]+", " ", str(x)) if x is not None else "" for x in r) + "\n")
    yer = {}
    for r in cikti:
        k = r[3] if r[1] == "pip-paket" else r[3].split(" (")[0]
        yer[k] = yer.get(k, 0) + 1
    SAYI.write_text(json.dumps({"adimlar": sayi, "yer_basina": yer, "toplam": len(cikti), "boyut_sinirli": CAPPED[:50],
                                "sure_s": round(time.time() - t0)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("TOPLAM", len(cikti), "capped", len(CAPPED))


if __name__ == "__main__":
    main()
