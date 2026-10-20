"""KURULUM-V1 d2: effortless'tan alınan mekanizma = modele göre sabit effort (settings.json modelSettings). Eklenti kurulmaz.
  python onay/kurulum_v1_effortless.py          # kuru: ne yazılacağını gösterir, dosyaya dokunmaz
  python onay/kurulum_v1_effortless.py --kuru   # yedek alıp modelSettings'e ekler
  python onay/kurulum_v1_effortless.py --geri   # yedeği geri koyar (ayar sonradan değiştiyse reddeder)
Hedef: ~/.claude/settings.json (ENV KURULUM_V1_AYAR ile değişir). Yazımı yalnız bu betik --kuru ile Desktop'ta çalıştırılınca olur."""
import json
import os
import sys
from pathlib import Path

HEDEF = Path(os.environ.get("KURULUM_V1_AYAR", Path.home() / ".claude/settings.json"))
YEDEK = HEDEF.with_name(HEDEF.name + ".kurulum_v1_effortless.bak")
MODEL, SEVIYE = "claude-sonnet-5-5", "high"


def yeni(ham):
    nl = "\r\n" if "\r\n" in ham else "\n"  # satır sonu stilini koru (write_text CRLF tuzağı)
    j = json.loads(ham)
    j.setdefault("modelSettings", {}).setdefault(MODEL, {})["effortLevel"] = SEVIYE
    return json.dumps(j, ensure_ascii=False, indent=2).replace("\n", nl) + (nl if ham.endswith("\n") else "")


def uygula(mod):
    ham = HEDEF.read_bytes().decode("utf-8")  # read_text satır sonunu çevirir
    if mod == "--geri":
        if not YEDEK.exists():
            return "yedek yok"
        if HEDEF.read_bytes() != yeni(YEDEK.read_bytes().decode("utf-8")).encode("utf-8"):
            return "ayar sonradan değişmiş: geri alma reddedildi"
        HEDEF.write_bytes(YEDEK.read_bytes())
        return "geri alındı"
    hedef = yeni(ham)
    if mod != "--kuru":
        return "kuru: " + MODEL + ".effortLevel=" + SEVIYE + (" (zaten var)" if hedef == ham else "")
    if hedef == ham:
        return "zaten uygulanmış"
    YEDEK.write_bytes(HEDEF.read_bytes())
    HEDEF.write_bytes(hedef.encode("utf-8"))
    return "uygulandı: " + MODEL + ".effortLevel=" + SEVIYE


if __name__ == "__main__":
    print(uygula(sys.argv[1] if len(sys.argv) > 1 else ""))
