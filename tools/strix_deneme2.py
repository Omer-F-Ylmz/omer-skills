"""STRIX-2 (28 Eki): Docker aç → RAM <=%89 bekle (2 dk'da bir, en çok 40 dk) → strix quick (OpenRouter :free, timeout 9000 sn).
Çıktı .kos/kopru/arka/strix2-strix.log'a akar (anahtar değeri yazılmaz). Bitişte 'BITIS'/'ENGEL' basar."""
import ctypes, functools, http.server, os, socketserver, subprocess, sys, threading, time, winreg
sys.stdout.reconfigure(encoding="utf-8")
SITE = r"C:\Users\pc\Desktop\Claude ile yapılanlar\parfum-yaris\parfum-desktop"
DOCKER_BIN = r"C:\Program Files\Docker\Docker\resources\bin"
CLI = DOCKER_BIN + r"\docker.exe"
LOG = r"C:\Projeler\omer-skills\.kos\kopru\arka\strix2-strix.log"
TAVAN, TIMEOUT = 89, 9000


def ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def docker_hazir():
    return subprocess.run([CLI, "version", "--format", "{{.Server.Version}}"], capture_output=True, timeout=30, creationflags=0x08000000).returncode == 0


def kullanici(ad):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ad)[0]
    except OSError:
        return os.environ.get(ad, "")


if not docker_hazir():
    subprocess.Popen([r"C:\Program Files\Docker\Docker\Docker Desktop.exe"], creationflags=0x00000008 | 0x00000200)
    print("docker başlatıldı", flush=True)
bas = time.time()
while True:
    r, d = ram(), docker_hazir()
    print(f"{time.strftime('%H:%M:%S')} ram=%{r} docker={d}", flush=True)
    if r <= TAVAN and d:
        break
    if time.time() - bas > 2400:
        print(f"ENGEL: 40 dk'da RAM<=%{TAVAN} ve docker hazır olmadı (son ram=%{r}, docker={d})", flush=True)
        sys.exit(1)
    time.sleep(120)

H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=SITE)
H.log_message = lambda *a: None
srv = socketserver.TCPServer(("0.0.0.0", 4180), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ)
env["PATH"] = DOCKER_BIN + ";" + env.get("PATH", "")
env["STRIX_LLM"] = "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
env["LLM_API_KEY"] = env["OPENROUTER_API_KEY"] = kullanici("OPENROUTER_API_KEY")
print("anahtar var:", bool(env["LLM_API_KEY"]), "strix başlıyor", flush=True)
try:
    with open(LOG, "w", encoding="utf-8", errors="replace") as f:
        try:
            rc = subprocess.run(["strix", "-n", "-m", "quick", "-t", "http://host.docker.internal:4180"], env=env, stdout=f, stderr=subprocess.STDOUT, timeout=TIMEOUT, creationflags=0x08000000).returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
    print("strix çıkış", rc, flush=True)
finally:
    srv.shutdown()
print("BITIS", flush=True)
