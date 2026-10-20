"""ROUTER-1 (20 Eki) onay betiği — Ömer koşar. ~/.claude/settings.json env'inden CLAUDE_CODE_SUBAGENT_MODEL_FORCE'u kaldırır:
açıkken alt ajan tanımındaki `model:` yok sayılır (code.claude.com/docs/en/sub-agents), kademe tablosu alt ajanda işlemez.
python onay/router_1b_force.py --kuru   # plan (varsayılan; hiçbir şey yazmaz)
python onay/router_1b_force.py uygula   # settings.json'u ~/.claude/yedek/router1b-<zaman>.json'a yedekler, anahtarı siler
python onay/router_1b_force.py --geri   # son yedeği geri yazar
Değer basılmaz; yalnız anahtar adı. Etki yeni oturumda."""
import json, shutil, sys, time
from pathlib import Path

AYAR = Path.home() / ".claude" / "settings.json"
ANAHTAR = "CLAUDE_CODE_SUBAGENT_MODEL_FORCE"
SON = Path.home() / ".claude" / "yedek" / "router1b-son.json"


def oku():
    return json.loads(AYAR.read_text(encoding="utf-8"))


def kuru():
    print(f"{ANAHTAR}: {'var → silinecek' if ANAHTAR in oku().get('env', {}) else 'yok, iş yok'} ({AYAR})")


def uygula():
    d = oku()
    if ANAHTAR not in d.get("env", {}):
        return print("yok, iş yok")
    yedek = SON.parent / f"router1b-{time.strftime('%Y%m%d-%H%M%S')}.json"
    yedek.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(AYAR, yedek)
    del d["env"][ANAHTAR]
    AYAR.write_bytes((json.dumps(d, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    SON.write_text(json.dumps({"yedek": str(yedek)}), encoding="utf-8")
    print(f"silindi (yedek {yedek})")


def geri():
    shutil.copy2(json.loads(SON.read_text(encoding="utf-8"))["yedek"], AYAR)
    print("geri alındı")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    {"--kuru": kuru, "uygula": uygula, "--geri": geri}[k]()
