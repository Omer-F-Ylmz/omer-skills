"""DISK-TARA-2 aday ölçümü: bilinen kalemlerin bugünkü boyutu + .part/.incomplete + çoklu klon + atıl büyük model.
Yalnız okur; silme komutu TSV'ye yazılır, çalıştırılmaz."""
import os, sys, time, datetime
from concurrent.futures import ThreadPoolExecutor

OUT = r"C:\Projeler\omer-skills\.kos\kopru\rapor\disk-tara-2"
H = os.path.expanduser("~")
LA = os.environ["LOCALAPPDATA"]
TMP = os.environ["TEMP"]
NOW = time.time()
try:
    import ctypes
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)
except Exception:
    pass


def du(path, older=None):
    """(bayt, dosya, en yeni mtime). older: yalnız N günden eski dosyalar."""
    tot = n = 0
    newest = 0.0
    stack = [path]
    while stack:
        p = stack.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        if e.is_symlink() or e.stat(follow_symlinks=False).st_file_attributes & 0x400:
                            continue
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            st = e.stat(follow_symlinks=False)
                            if older and NOW - st.st_mtime < older * 86400:
                                continue
                            tot += st.st_size
                            n += 1
                            newest = max(newest, st.st_mtime)
                    except OSError:
                        pass
        except OSError:
            pass
    return tot, n, newest


def d(ts):
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else "-"


rows = []  # yol, bayt, kategori, mtime, yeniden, oneri


def add(path, kat, yeniden, oneri, older=None):
    if not os.path.exists(path):
        return
    b, n, m = du(path, older)
    rows.append((path, b, kat, d(m), yeniden, oneri))


Q = lambda p: p.replace("'", "''")
RD = lambda p: f"Remove-Item -LiteralPath '{Q(p)}' -Recurse -Force"

K = []  # (path, kat, yeniden, oneri)
K += [
    (LA + r"\NVIDIA\DXCache", "a-onbellek", "evet", RD(LA + r"\NVIDIA\DXCache\*")),
    (r"C:\ProgramData\NVIDIA Corporation\NV_Cache", "a-onbellek", "evet", RD(r"C:\ProgramData\NVIDIA Corporation\NV_Cache\*")),
    (LA + r"\NVIDIA\GLCache", "a-onbellek", "evet", RD(LA + r"\NVIDIA\GLCache\*")),
    (LA + r"\uv\cache", "a-onbellek", "evet", "uv cache clean"),
    (LA + r"\npm-cache", "a-onbellek", "evet", "npm cache clean --force"),
    (H + r"\.nuget\packages", "a-onbellek", "evet", "dotnet nuget locals all --clear"),
    (H + r"\.bun\install\cache", "a-onbellek", "evet", "bun pm cache rm"),
    (LA + r"\pip\cache", "a-onbellek", "evet", "pip cache purge"),
    (LA + r"\pnpm", "a-onbellek", "evet", RD(LA + r"\pnpm\store")),
    (H + r"\.codex\.tmp\marketplaces", "a-onbellek", "evet", RD(H + r"\.codex\.tmp\marketplaces")),
    (H + r"\.codex\.tmp", "a-onbellek", "evet", RD(H + r"\.codex\.tmp")),
    (LA + r"\CrashDumps", "a-onbellek", "evet", RD(LA + r"\CrashDumps\*")),
    (H + r"\.cache\huggingface", "a-onbellek", "evet (yeniden iner)", RD(H + r"\.cache\huggingface\hub")),
    (H + r"\.cache", "a-onbellek", "kısmen", "alt klasör bazında karar"),
    (LA + r"\Temp", "a-onbellek", "evet", "bkz. TEMP 7g+ satırı"),
    (LA + r"\Microsoft\Windows\INetCache", "a-onbellek", "evet", RD(LA + r"\Microsoft\Windows\INetCache\*")),
    (LA + r"\D3DSCache", "a-onbellek", "evet", RD(LA + r"\D3DSCache\*")),
    (LA + r"\Google\Chrome\User Data\Default\Cache", "a-onbellek", "evet", "Chrome kapalıyken " + RD(LA + r"\Google\Chrome\User Data\Default\Cache")),
    (LA + r"\Opera Software", "a-onbellek", "kısmen", "Opera kapalıyken alt Cache klasörleri"),
    (r"C:\Windows\SoftwareDistribution\Download", "a-onbellek", "evet", "Stop-Service wuauserv; " + RD(r"C:\Windows\SoftwareDistribution\Download\*")),
    (r"C:\Windows\Temp", "a-onbellek", "evet", RD(r"C:\Windows\Temp\*")),
    (r"C:\Program Files (x86)\Steam\steamapps\shadercache", "a-onbellek", "evet", RD(r"C:\Program Files (x86)\Steam\steamapps\shadercache\*")),
    (r"C:\Program Files (x86)\Steam\steamapps\downloading", "c-yarim", "evet", RD(r"C:\Program Files (x86)\Steam\steamapps\downloading\*")),
    (r"C:\Program Files (x86)\Steam\steamapps\temp", "c-yarim", "evet", RD(r"C:\Program Files (x86)\Steam\steamapps\temp\*")),
    (r"C:\Program Files\Epic Games\.egstore", "c-yarim", "evet", "Epic Launcher kapalıyken alt bps/Pending incele"),
    (r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests", "a-onbellek", "kısmen", "silme; yalnız boyut"),
    (r"C:\ProgramData\Epic\EpicGamesLauncher\VaultCache", "a-onbellek", "evet", RD(r"C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\*")),
    (LA + r"\EpicGamesLauncher\Saved\webcache", "a-onbellek", "evet", RD(LA + r"\EpicGamesLauncher\Saved\webcache*")),
    (r"C:\Riot Games\Riot Client\Logs", "a-onbellek", "evet", RD(r"C:\Riot Games\Riot Client\Logs")),
    (LA + r"\Riot Games\Riot Client\Data", "a-onbellek", "kısmen", "yalnız boyut"),
    (r"C:\Riot Games\Riot Client\UX\GPUCache", "a-onbellek", "evet", RD(r"C:\Riot Games\Riot Client\UX\GPUCache")),
    (r"C:\ProgramData\Package Cache", "a-onbellek", "kısmen", "yalnız boyut (kurulum önbelleği)"),
    (H + r"\.video-cache", "d-onay", "evet (yeniden üretilir, uzun)", "karar: " + RD(H + r"\.video-cache")),
    (H + r"\.tmp-video", "d-onay", "kısmen", "karar: ölçüm kanıtı arşivle"),
    (r"C:\Projeler\omer-skills\.kos\kurulum-tarama\klon","b-kopya", "evet", RD(r"C:\Projeler\omer-skills\.kos\kurulum-tarama\klon")),
    (r"C:\Projeler\omer-skills-wt", "b-kopya", "evet", "git worktree remove (tek tek)"),
    (r"C:\AI\indirilen", "d-onay", "kısmen", "karar: içeriği incele"),
    (r"C:\AI\ComfyUI\models", "d-onay", "evet (yeniden iner)", "karar: kullanılmayan alt klasör"),
    (H + r"\.ollama\models", "d-onay", "evet (ollama pull)", "ollama rm <model>"),
    (H + r"\.lmstudio\models", "d-onay", "evet", "LM Studio'dan model sil"),
    (r"C:\Windows\Prefetch", "a-onbellek", "evet", "silme önerilmez; yalnız boyut"),
    (r"C:\hiberfil.sys", "d-onay", "evet", "powercfg /h off"),
    (r"C:\pagefile.sys", "d-onay", "-", "dokunma; yalnız boyut"),
]
for p, k, y, o in K:
    if p.endswith("sys"):
        if os.path.exists(p):
            rows.append((p, os.stat(p).st_size, k, "-", y, o))
    else:
        add(p, k, y, o)

# %TEMP% 7 gün+
b, n, m = du(TMP, older=7)
rows.append((TMP + r"  (yalnız 7 gün+ dosyalar, %d dosya)" % n, b, "a-onbellek", d(m), "evet",
             f"Get-ChildItem -LiteralPath '{Q(TMP)}' -Recurse -File -Force | Where-Object LastWriteTime -lt (Get-Date).AddDays(-7) | Remove-Item -Force"))

# .part/.incomplete/.crdownload/.tmp >= 50 MB
roots = [r"C:\AI", H + r"\.cache", H + r"\.ollama", H + r"\.lmstudio", H + r"\Downloads", H + r"\Desktop",
         H + r"\.video-cache", H + r"\.tmp-video", r"C:\Projeler", LA + r"\Temp", LA + r"\uv", H + r"\AppData\Roaming"]
EXT = (".part", ".incomplete", ".crdownload", ".partial", ".download", ".aria2", ".tmp")
hits = []


def walk(root):
    out = []
    stack = [root]
    while stack:
        p = stack.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        if e.is_symlink() or e.stat(follow_symlinks=False).st_file_attributes & 0x400:
                            continue
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        elif e.name.lower().endswith(EXT):
                            st = e.stat(follow_symlinks=False)
                            if st.st_size >= 50 * 2**20:
                                out.append((e.path, st.st_size, st.st_mtime))
                    except OSError:
                        pass
        except OSError:
            pass
    return out


with ThreadPoolExecutor(8) as ex:
    for res in ex.map(walk, [r for r in roots if os.path.isdir(r)]):
        hits += res
for pth, sz, mt in sorted(hits, key=lambda x: -x[1])[:40]:
    rows.append((pth, sz, "c-yarim", d(mt), "evet" if "tmp" in pth.lower() else "kısmen",
                 f"Remove-Item -LiteralPath '{Q(pth)}' -Force"))

# aynı repo birden çok klon: .git içeren klasörler (derinlik ≤4), remote adına göre grupla
git_roots = [r"C:\Projeler", H + r"\Desktop", H, r"C:\AI", r"C:\Users\pc\Documents"]
clones = {}


def find_git(root, depth=4):
    stack = [(root, 0)]
    while stack:
        p, dep = stack.pop()
        try:
            with os.scandir(p) as it:
                names = []
                for e in it:
                    names.append(e.name)
                    if e.is_dir(follow_symlinks=False) and dep < depth and e.name not in (".git", "node_modules", "AppData", ".cache", ".nuget", "venv", ".venv", "Windows"):
                        stack.append((e.path, dep + 1))
                if ".git" in names:
                    url = ""
                    try:
                        cfg = open(os.path.join(p, ".git", "config"), encoding="utf-8", errors="ignore").read() if os.path.isdir(os.path.join(p, ".git")) else "worktree"
                        for ln in cfg.splitlines():
                            if ln.strip().startswith("url ="):
                                url = ln.split("=", 1)[1].strip()
                                break
                        if cfg == "worktree":
                            url = "worktree:" + os.path.basename(p)
                    except OSError:
                        pass
                    clones.setdefault(url or "?" + os.path.basename(p), []).append(p)
        except OSError:
            pass


for r in git_roots:
    if os.path.isdir(r):
        find_git(r, 4 if r != H else 2)
for url, ps in clones.items():
    if len(ps) > 1 and not url.startswith("worktree") and not url.startswith("?"):
        for p in ps[1:]:
            b, n, m = du(p)
            if b > 50 * 2**20:
                rows.append((p, b, "b-kopya", d(m), "evet (aynı repo: " + url.split("/")[-1] + ", asıl " + ps[0] + ")",
                             f"commitsiz değişiklik yoksa: {RD(p)}"))

# 60 gündür dokunulmamış büyük model dosyaları (>=1 GB)
MROOTS = [r"C:\AI", H + r"\.ollama", H + r"\.lmstudio", H + r"\.cache\huggingface"]
MEXT = (".safetensors", ".ckpt", ".gguf", ".pt", ".pth", ".bin", ".onnx", ".pkl")
big = []


def walkm(root):
    out = []
    stack = [root]
    while stack:
        p = stack.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        if e.is_symlink() or e.stat(follow_symlinks=False).st_file_attributes & 0x400:
                            continue
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            st = e.stat(follow_symlinks=False)
                            if st.st_size >= 2**30 and (e.name.lower().endswith(MEXT) or "sha256-" in e.name):
                                out.append((e.path, st.st_size, st.st_mtime, st.st_atime))
                    except OSError:
                        pass
        except OSError:
            pass
    return out


with ThreadPoolExecutor(4) as ex:
    for res in ex.map(walkm, [r for r in MROOTS if os.path.isdir(r)]):
        big += res
stale = [x for x in big if NOW - max(x[2], x[3]) > 60 * 86400]
for pth, sz, mt, at in sorted(stale, key=lambda x: -x[1])[:25]:
    rows.append((pth, sz, "d-onay", d(max(mt, at)), "evet (yeniden indirilir)", f"Remove-Item -LiteralPath '{Q(pth)}' -Force   # 60g+ dokunulmamış"))

with open(os.path.join(OUT, "ham-aday.tsv"), "w", encoding="utf-8") as f:
    f.write("yol\tGB\tkategori\tson_degisiklik\tyeniden_uretilebilir\toneri\n")
    for p, b, k, m, y, o in sorted(rows, key=lambda r: -r[1]):
        f.write(f"{p}\t{b/2**30:.2f}\t{k}\t{m}\t{y}\t{o}\n")
print("satir", len(rows), "model>=1GB", len(big), "stale", len(stale))
