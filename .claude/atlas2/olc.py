"""ATLAS-2 alt küme seçim ölçümü: python olc.py <set_ad> <id,id,...> (zor set id'leri z: önekiyle). Tek claude -p (toplu, sonra kolu)."""
import json, sys
from pathlib import Path
D = Path(__file__).resolve().parents[2] / "tools" / "secim"
sys.path.insert(0, str(D))
import secim_olc  # noqa: E402
ana = {g["id"]: g for g in json.loads((D / "secim_gorevler.json").read_text(encoding="utf-8"))}
zor = {g["id"]: g for g in json.loads((D / "secim_gorevler_zor.json").read_text(encoding="utf-8"))}
gorev = [zor[i[2:]] if i.startswith("z:") else ana[i] for i in sys.argv[2].split(",")]  # ayrıştırıcı yalnız Sxx: zor id'si seçili ana id'lerle çakışmamalı
assert len({g["id"] for g in gorev}) == len(gorev), "id çakışması"
print(secim_olc.toplu("sonra", 1, gorev=gorev, set_ad=sys.argv[1]))
print("BITTI")
