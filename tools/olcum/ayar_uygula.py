"""KÜTÜPHANE-4: ölçülmüş bir profili ~/.claude/settings.json'a birleştirir (yalnız skillOverrides + env; başka anahtara dokunmaz).
  python tools/olcum/ayar_uygula.py profil-nameonly-75k.json      # yedek al + birleştir
  python tools/olcum/ayar_uygula.py --geri                        # son yedekten döner
Kurallar: mevcut skillOverrides değeri ezilmez (yalnız eksik anahtar eklenir); env'de profildeki anahtar yazılır.
Yedek: settings.json.bak-k4-<zaman>; en son yedek yolu settings.json.bak-k4-son dosyasında."""
import json
import shutil
import sys
import time
from pathlib import Path

AYAR = Path.home() / ".claude" / "settings.json"
SON = AYAR.with_name("settings.json.bak-k4-son")
D = Path(__file__).resolve().parent


def birlestir(ayar, profil):
    so = ayar.setdefault("skillOverrides", {})
    eklenen = 0
    for k, v in (profil.get("skillOverrides") or {}).items():
        if k not in so:
            so[k] = v
            eklenen += 1
    env = ayar.setdefault("env", {})
    degisen = {k: (env.get(k), v) for k, v in (profil.get("env") or {}).items() if env.get(k) != v}
    env.update(profil.get("env") or {})
    return eklenen, degisen


def main(a):
    if a and a[0] == "--geri":
        y = Path(SON.read_text(encoding="utf-8").strip())
        shutil.copy2(y, AYAR)
        print("geri alındı:", y)
        return 0
    profil = json.loads((D / a[0]).read_text(encoding="utf-8"))
    ham = AYAR.read_text(encoding="utf-8")
    ayar = json.loads(ham)
    yedek = AYAR.with_name(f"settings.json.bak-k4-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(AYAR, yedek)
    SON.write_text(str(yedek), encoding="utf-8")
    once = len(ayar.get("skillOverrides") or {})
    eklenen, degisen = birlestir(ayar, profil)
    AYAR.write_text(json.dumps(ayar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(AYAR.read_text(encoding="utf-8"))
    print(f"yedek {yedek.name} · skillOverrides {once} -> {len(ayar['skillOverrides'])} (+{eklenen}) · env değişen {degisen}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
