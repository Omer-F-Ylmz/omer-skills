"""CLIProxyAPI duman testi: Claude-dışı sağlayıcılar, anahtarlar ortam DEĞİŞKENİNDEN okunur.

Geçici config üretir (anahtar değeri yalnız bu dosyada, iş bitince silinir), sunucuyu
127.0.0.1:8317'de başlatır, tek ücretsiz model isteği atar, KENDİ pid'ini kapatır.
Kullanım: python tools/cliproxy_dene.py
"""
import json, os, subprocess, sys, time, urllib.request
from pathlib import Path

DIR = Path("C:/Users/pc/tools-cliproxy")
EXE = DIR / "bin" / "cli-proxy-api.exe"
CFG = DIR / "config.gecici.yaml"
LOCAL_KEY = "sk-local-gecici-dene"
UA = {"User-Agent": "curl/8.5.0"}  # Groq Python-urllib UA'sını 1010 ile reddeder

# (ad, base-url, anahtar değişkeni, model)
SAGLAYICILAR = [
    ("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-20b"),
    ("openrouter", "https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "liquid/lfm-2.5-2.6b:free"),
    ("mistral", "https://api.mistral.ai/v1", "MISTRAL_API_KEY", "mistral-small-latest"),
    ("nvidia", "https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY", "meta/llama-3.1-8b-instruct"),
]


def config_yaz():
    satirlar = [
        "config-version: 8", "server:", '  host: "127.0.0.1"', "  port: 8317",
        "access:", "  api-keys:", f'    - "{LOCAL_KEY}"',
        "api-keys:", "  openai-compatibility:",
    ]
    ad_var = []
    for ad, url, var, model in SAGLAYICILAR:
        if not os.environ.get(var):
            continue
        satirlar += [
            f'    - name: "{ad}"', f'      prefix: "{ad}"', f'      base-url: "{url}"',
            "      keys:", f'        - api-key: "{os.environ[var]}"',
            "      models:", f'        - name: "{model}"', f'          alias: "{model}"',
        ]
        ad_var.append((ad, var, model))
    CFG.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    return ad_var


def istek(ad, model):
    govde = json.dumps({"model": f"{ad}/{model}", "max_tokens": 128,
                        "messages": [{"role": "user", "content": "Say ok"}]}).encode()
    r = urllib.request.Request("http://127.0.0.1:8317/v1/chat/completions", govde,
                               {"Authorization": f"Bearer {LOCAL_KEY}", "Content-Type": "application/json", **UA})
    try:
        with urllib.request.urlopen(r, timeout=60) as y:
            return y.status, json.loads(y.read())["choices"][0]["message"]["content"][:20]
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:120].decode("utf-8", "replace")
    except Exception as e:
        return 0, repr(e)[:120]


def main():
    ad_var = config_yaz()
    print("yapılandırılan:", [f"{a}({v})" for a, v, _ in ad_var])
    p = subprocess.Popen([str(EXE), "-config", str(CFG)], stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, creationflags=0x08000000)  # CREATE_NO_WINDOW
    try:
        time.sleep(4)
        for ad, _, model in ad_var:
            print(ad, *istek(ad, model))
    finally:
        p.kill()
        p.wait()
        CFG.unlink(missing_ok=True)
        print("sunucu kapandı pid", p.pid, "gecici config silindi")


if __name__ == "__main__":
    sys.exit(main())
