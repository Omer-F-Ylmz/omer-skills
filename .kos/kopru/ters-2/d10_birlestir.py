"""d10: doğrulanmış taslakları hedef-d9.json'a birleştirir (şema: docs/ters/kapi/hedefler.json)."""
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from d10_dogrula import kontrol
from d10_taslak import HEDEF, J, KOK

AYIR = KOK / ".kos/kopru/ters-2/d9-js"
DLL = {
    "Jev": J / "Jev/bin/Debug/net10.0/Jev.dll",
    "Jev.Tests": J / "Jev.Tests/bin/Debug/net10.0/Jev.Tests.dll",
    "NativeAotFixture": KOK / ".kos/kopru/ters-2/d9-dn/nativeaot/bin/Debug/net8.0/NativeAotFixture.dll",
}
SORU = {ad: v[2] for ad, v in HEDEF.items()}
out = []
for i, ad in enumerate(HEDEF, 14):
    tur, kaynaklar, soru = HEDEF[ad]
    iyi, kotu = kontrol(ad)
    assert len(iyi) == 5 and not kotu, (ad, len(iyi), kotu)
    h = {"id": i, "ad": ad, "tur": tur, "yol": kaynaklar[0]}
    if tur == "js":
        d = AYIR / ad
        d.mkdir(parents=True, exist_ok=True)
        shutil.copy(kaynaklar[0], d / Path(kaynaklar[0]).name)
        h["rea_yol"] = str(d).replace("\\", "/")
    elif tur == "dotnet":
        h["derlenmis"] = str(DLL[ad]).replace("\\", "/")
        h["yol"] = str(Path(kaynaklar[0]).parent).replace("\\", "/")
        kaynaklar = kaynaklar + [h["derlenmis"]]
    else:
        h["sayfa"] = "/animasyon-atolyesi/tarifler/" + Path(kaynaklar[0]).name
    h["kaynaklar"] = kaynaklar
    h["sorular"] = soru
    h["maddeler"] = [{"madde": m["madde"], "kanit": m["kanit"]} for m in iyi]
    out.append(h)
Path(KOK / ".kos/kopru/ters-2/hedef-d9.json").write_text(json.dumps({"hedefler": out}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(out), "hedef yazıldı")
