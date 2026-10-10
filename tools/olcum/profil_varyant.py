"""KÜTÜPHANE-4: profil varyantı üretir — taban profil (tam = boş, ya da bir profil json'u) + env SLASH_COMMAND_TOOL_CHAR_BUDGET.
  python tools/olcum/profil_varyant.py <cikti_adi> <butce> [taban_json]
settings.json'a dokunmaz; yalnız tools/olcum/<cikti_adi>.json yazar."""
import json
import sys
from pathlib import Path

D = Path(__file__).resolve().parent


def uret(ad, butce, taban=None):
    d = json.loads((D / taban).read_text(encoding="utf-8")) if taban else {}
    d.setdefault("env", {})["SLASH_COMMAND_TOOL_CHAR_BUDGET"] = str(int(butce))
    (D / f"{ad}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return D / f"{ad}.json"


if __name__ == "__main__":
    a = sys.argv[1:]
    print(uret(a[0], a[1], a[2] if len(a) > 2 else None))
