"""STRIX ilk deneme (Docker kuruldu, 27 Eki): parfum-desktop statik sitesini yerel sunucuda açar, strix'i ücretsiz modelle (argv[1]) kısa kipte koşar.
Anahtar değeri yazılmaz; yalnız bu sürecin ortamına GEMINI_API_KEY'den aktarılır."""
import functools, http.server, os, socketserver, subprocess, sys, threading, winreg
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SITE = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\parfum-yaris\parfum-desktop")
def kullanici(ad):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ad)[0]
    except OSError:
        return os.environ.get(ad, "")
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(SITE))
H.log_message = lambda *a: None
srv = socketserver.TCPServer(("0.0.0.0", 4180), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
env = dict(os.environ)
env["PATH"] = r"C:\Program Files\Docker\Docker\resources\bin;" + env.get("PATH", "")
# F1: sağlayıcı argv[1] (gemini | openrouter | groq); anahtar değeri yazılmaz
SAG = {"gemini": ("gemini/gemini-3.5-flash", "GEMINI_API_KEY"),
       "openrouter": ("openrouter/nvidia/nemotron-3-ultra-550b-a55b:free", "OPENROUTER_API_KEY"),
       "groq": ("groq/openai/gpt-oss-120b", "GROQ_API_KEY")}
model, anahtar = SAG[sys.argv[1] if len(sys.argv) > 1 else "gemini"]
env["STRIX_LLM"] = model
env["LLM_API_KEY"] = kullanici(anahtar)
env[anahtar] = env["LLM_API_KEY"]
print("anahtar var:", bool(env["LLM_API_KEY"]))
try:
    r = subprocess.run(["strix", "-n", "-m", "quick", "-t", "http://host.docker.internal:4180"], env=env,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1500, creationflags=0x08000000)
    print("strix çıkış", r.returncode)
    print(((r.stdout or "") + (r.stderr or ""))[-2500:])
finally:
    srv.shutdown()
print("BITIS")
