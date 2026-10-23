"""ÖĞRENME-2 uyku-zamanı yansıtma ($0): son 24 saatin olaylarını özetler, ücretsiz model varsa tek ders cümlesi ekler.
Çıktı: Obsidian 20-icgoru/<tarih>.md (günlük not) + .kos/kopru/yama-oneri.md (SKILL.md/kural YAMA ÖNERİSİ, uygulanmaz).
Claude çağrısı yok: ücretsiz havuz yoksa yalnız deterministik özet yazılır."""
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(KOK / "tools"))
import beyin_dusun as b  # noqa: E402

YAMA = KOK / ".kos/kopru/yama-oneri.md"


def ozet_metni(olaylar):
    hatalar = [o for o in olaylar if o["hata"]]
    satir = [f"{len(olaylar)} olay (son 24 sa) · {len(hatalar)} hata"]
    satir += [f"- hata: {o['arac'] or o['tur']}: {o['ozet'][:120]}" for o in hatalar[:3]]
    satir += [f"- maliyet: {o['ozet'][:120]}" for o in [o for o in olaylar if o["tur"] == "maliyet"][-3:]]
    return "\n".join(satir)


def yansit(olaylar, sor=b._sor):
    metin = ozet_metni(olaylar)
    if not olaylar:
        return metin
    istem = "Aşağıdaki iş olaylarından TEK satır ders yaz: ne pahalıydı ya da hata verdi, bir sonraki işte nasıl önlenir. Yalnız cümle.\n" + metin
    try:
        ders, _ = sor("ozet", istem, 200)  # geçerli tur: ozet/hakem/yazim/uzun; "hafif" hiçbir halkayla eşleşmiyordu → DERS hep boştu
    except Exception:
        ders = None
    return metin + (f"\nDERS: {ders.strip()}" if ders and ders.strip() else "")


def yaz(metin, gunluk, yama):
    for yol, icerik in ((gunluk, metin), (yama, metin)):
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(icerik + "\n", encoding="utf-8")


def main():
    simdi = time.time()
    olaylar = [o for o in b._olay_oku(0)[0] if o["t"] >= simdi - 86400]
    gunluk = b.ICGORU / f"{time.strftime('%Y-%m-%d')}-yansitma.md"
    yaz(yansit(olaylar), gunluk, YAMA)
    print(f"yansıtma: {len(olaylar)} olay → {gunluk}")


if __name__ == "__main__":
    main()
