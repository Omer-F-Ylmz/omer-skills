"""ARAC-KAPI-1B: 3 ücretsiz eleştirmen (tasarımcı · kullanıcı · performans) ekran/metin çıktısını eleştirir.
Görsel işlerde kabul kapısından önce koşulur; tam metin <cikti.json>'a yazılır, stdout'a yalnız rol başına ~120 karakter (Claude ≤200 jeton/çağrı).
Yalnız tools/ucuz_alt.coz (ücretsiz zincir, ücretli modele yükselmez) kullanılır.
  python tools/elestirmen.py <ekran.md|ekran.png> <cikti.json>
Çıkış: 0 en az bir eleştirmen yanıtladı · 5 hiçbir ücretsiz yol yanıtlamadı (bekle, yeniden dene)."""
import json
import sys
from pathlib import Path

ROLLER = {
    "tasarimci": "tasarimci olarak eleştir: hiyerarşi, boşluk, tipografi, renk uyumu; en çok düzelen 3 öneri",
    "kullanici": "kullanici olarak eleştir: ne anlaşılmıyor, nerede takılırım, eylem çağrısı net mi; en çok düzelen 3 öneri",
    "performans": "performans olarak eleştir: ağır görsel/metin, gereksiz öğe, yükleme ve akıcılık; en çok düzelen 3 öneri",
}
GORSEL = {".png", ".jpg", ".jpeg", ".webp"}
KISA = 120


def elestir(dosya, coz):
    """[{rol, oneri | None, model}] — ücretsiz yol yanıtlamayan rol oneri=None (sessizce uydurulmaz)."""
    gorsel = Path(dosya).suffix.lower() in GORSEL
    out = []
    for rol, istem in ROLLER.items():
        o, model, *_ = coz("gorsel" if gorsel else "ozet", istem, [] if gorsel else [dosya], (), dosya if gorsel else None)
        oneri = (o.get("hukum") if gorsel else o.get("ozet")) if o else None
        out.append({"rol": rol, "oneri": oneri, "model": model})
    return out


def main(argv, coz=None):
    if coz is None:
        import ucuz_alt
        coz = ucuz_alt.coz
    dosya, cikti = argv
    r = elestir(dosya, coz)
    Path(cikti).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    for x in r:
        print(f"{x['rol']}: {(x['oneri'] or 'YOK (bekle)')[:KISA]}")
    return 0 if any(x["oneri"] for x in r) else 5


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
