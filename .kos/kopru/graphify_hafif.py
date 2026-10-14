"""graphify sarmalayıcısı: python graphify_hafif.py [kök] [--tam] [ek graphify update bayrağı...]
Varsayılan ARTIMLI: grafın built_at_commit'inden bu yana git'te değişen + çalışma ağacında değişen/yeni dosyalar
graphify'ın kendi _rebuild_code(changed_paths=...) yoluyla (git hook'unun yolu) yeniden çıkarılır. --tam → `graphify update .`.
RAM ≥%85 (artımlı) / ≥%75 (tam) ya da başka graphify koşuyorsa çalışmaz; tek örnek kilidi; tepe RSS (süreç ağacı toplamı) + süre basar.
Hafifliğin asıl kaynağı kökteki .graphifyignore (GRAPHIFY-RAM-1, 14 Eki: dışlanmadan önce graph.json 337 MB → ~3.5 GB RAM)."""
import os, re, subprocess, sys, time
import psutil

GPY = os.path.expandvars(r"%APPDATA%\uv\tools\graphifyy\Scripts\python.exe")
arg = sys.argv[1:]
kok = next((a for a in arg if not a.startswith("--")), r"C:\Projeler\omer-skills")
arg = [a for a in arg if a != kok]
tam = "--tam" in arg
arg = [a for a in arg if a != "--tam"]
kilit = os.path.join(kok, "graphify-out", ".hafif.kilit")
if any("graphify" in " ".join(p.info["cmdline"] or []) and "graphify_hafif" not in " ".join(p.info["cmdline"] or [])
       for p in psutil.process_iter(["cmdline"]) if p.pid != os.getpid()):
    sys.exit("başka graphify süreci var, başlatılmadı")


def degisen():  # None → artımlı mümkün değil (graf yok / commit bilinmiyor)
    g = os.path.join(kok, "graphify-out", "graph.json")
    if not os.path.exists(g):
        return None
    with open(g, "rb") as f:
        f.seek(max(0, os.path.getsize(g) - 300))
        m = re.search(rb'"built_at_commit":"([0-9a-f]{40})"', f.read())
    if not m:
        return None
    git = lambda *a: subprocess.run(["git", *a], cwd=kok, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    d = git("diff", "--name-only", m.group(1).decode()) + git("ls-files", "-m", "-o", "--exclude-standard")
    return sorted(set(d))


d = None if tam else degisen()
esik = 75 if d is None else 85  # Desktop 14 Eki 22:06: artımlı ~332 MB → %85; tam ~1.5 GB → %75
ram = psutil.virtual_memory().percent
if ram >= esik:
    sys.exit(f"RAM %{ram:.0f} ≥ %{esik}, graphify başlatılmadı")
try:
    fd = os.open(kilit, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
except FileExistsError:
    sys.exit(f"kilit var: {kilit} (eski koşu öldüyse sil)")
try:
    os.write(fd, str(os.getpid()).encode()); os.close(fd)
    bas = time.time()
    if d is None:
        komut, girdi = ["graphify", "update", ".", *arg], None
    else:
        # GRAPHIFY-ULTRA-1 G2: _rebuild_code (48 sn/829 MB) yerine graphify_hizli (3.8 sn/332 MB); süzgeç orada
        komut = [GPY, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphify_hizli.py"), kok]
        girdi = subprocess.PIPE
    p = subprocess.Popen(komut, cwd=kok, stdin=girdi or subprocess.DEVNULL, creationflags=0x08000000)  # CREATE_NO_WINDOW
    if girdi:
        p.stdin.write("\n".join(d).encode()); p.stdin.close()
    ana, tepe = psutil.Process(p.pid), 0
    while p.poll() is None:
        try:
            tepe = max(tepe, sum(s.memory_info().rss for s in [ana, *ana.children(recursive=True)]))
        except psutil.Error:
            pass
        time.sleep(0.3)
    kip = "tam" if d is None else f"artımlı {len(d)} dosya"
    print(f"graphify_hafif: {kip} · rc {p.returncode} · tepe RSS {tepe / 1e6:.0f} MB · {time.time() - bas:.1f} sn")
    if p.returncode == 0:  # G3: graf değişti → harita tazelenir
        subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphify_harita.py"), kok])
    sys.exit(p.returncode)
finally:
    os.remove(kilit)
