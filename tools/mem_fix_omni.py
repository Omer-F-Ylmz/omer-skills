"""MEM-FIX-1: OmniRoute'ta claude-mem combo'sunu listele/kur. Anahtar değeri basılmaz.
Kullanım: mem_fix_omni.py liste | kur | ayar
"""
import json
import os
import sys
import urllib.request
import winreg

URL = "http://127.0.0.1:20128"
COMBO = "mem-yedek"
# Sıra (MEM-FIX-3): OpenRouter YALNIZ :free > yerel ollama > Groq EN SON (TPM 8000 → 413, combo 413'te sonraki halkaya düşmüyor; TPD 200k). Gemini claude-mem'de ayrı (hız sınırlı) birincil.
ZINCIR = ["openrouter/nvidia/nemotron-3.5-lightning:free", "ollama/qwen3.5:4b", "groq/openai/gpt-oss-20b"]


def serbest_mi(model):
    """OpenRouter hesabında kredi var: :free olmayan OpenRouter adı reddedilir."""
    return not model.startswith("openrouter/") or model.endswith(":free")


def anahtar():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


def istek(yol, govde=None, yontem=None):
    r = urllib.request.Request(
        URL + yol,
        data=None if govde is None else json.dumps(govde).encode(),
        method=yontem or ("POST" if govde is not None else "GET"),
        headers={"Authorization": "Bearer " + anahtar(), "Content-Type": "application/json", "User-Agent": "omer-skills/1.0"},
    )
    with urllib.request.urlopen(r, timeout=30) as f:
        return json.load(f)


def ayar_goster(yol="~/.claude-mem/settings.json"):
    """Değer basmaz: CLAUDE_MEM_* anahtar adı + var/yok (SIR KURALI)."""
    a = json.load(open(os.path.expanduser(yol), encoding="utf-8"))
    return {k: ("var" if a[k] not in ("", None) else "yok") for k in sorted(a) if k.startswith("CLAUDE_MEM_") and any(s in k for s in ("PROVIDER", "KEY", "MODEL", "BASE_URL", "RATE"))}


if __name__ == "__main__":
    if sys.argv[1] == "ayarbak":
        for k, v in ayar_goster().items():
            print(k, v)
    if sys.argv[1] == "liste":
        c = istek("/api/combos")
        for x in c.get("combos", c) if isinstance(c, dict) else c:
            print(x.get("name"), x.get("strategy"), json.dumps(x.get("models"))[:300])
        m = istek("/v1/models")
        print("modeller:", sorted({d["id"].split("/")[0] for d in m["data"]}))
        print("ollama:", [d["id"] for d in m["data"] if d["id"].startswith("ollama")][:6])
        print("groq20b:", [d["id"] for d in m["data"] if "gpt-oss-20b" in d["id"]][:4])
        print("free:", [d["id"] for d in m["data"] if d["id"].endswith(":free")][:8])

    if sys.argv[1] == "kur":
        bos = [m for m in ZINCIR if not serbest_mi(m)]
        if bos:
            sys.exit("ücretli OpenRouter modeli reddedildi: " + ",".join(bos))
        import subprocess
        e = dict(os.environ, OMNIROUTE_API_KEY=anahtar())
        print(subprocess.run(["omniroute", "combo", "create", COMBO, "--strategy", "priority", "--models", ",".join(ZINCIR)],
                             env=e, capture_output=True, text=True, shell=True).stdout[-300:])
    if sys.argv[1] == "ayar":
        # kalıcı claude-mem ayarı: Gemini birincil kalır, kota dolunca OmniRoute combo'su
        yol = os.path.expanduser("~/.claude-mem/settings.json")
        a = json.load(open(yol, encoding="utf-8"))
        a.update({
            "CLAUDE_MEM_QUOTA_FALLBACK_PROVIDER": "openai-compatible",
            "CLAUDE_MEM_OPENAI_COMPAT_BASE_URL": URL + "/v1",
            "CLAUDE_MEM_OPENAI_COMPAT_MODEL": COMBO,
            "CLAUDE_MEM_OPENAI_COMPAT_API_KEY": anahtar(),
        })
        with open(yol, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(a, indent=2, ensure_ascii=False) + "\n")
        print("ayar yazıldı (anahtar gizli)")
