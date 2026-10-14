"""VİDEO-3 V4 kuru koşu: link listesi → hangi hat (kisa / karusel / uzun), önbellek durumu, Gemini istek tahmini. İşleme YOK, ağ YOK.
Kullanım (tools/video .venv): python hat_plan.py <linkler.txt> [cikti.tsv]
Durum: rapor (kisa çıktısı var) · paket (paket.md hazır, yalnız Gemini+karar) · yeni (önce `video paket`, indirme + OCR = ağır python, tek seferde 1)."""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools" / "video"))
from video import cli, kisa  # noqa: E402

RAPOR = Path(__file__).resolve().parent / "kisa"  # cli kisa --cikti varsayılanı
ISTEK = 1 + 1 + len(kisa.ORNEK)  # izle + metin SABIT + ORNEK başına bir; yeniden deneme hariç


def tur(url):
    if "/p/" in url:
        return "karusel"  # tek görselli gönderi de bu yoldan (slayt = 1)
    if "instagram.com" in url or "/shorts/" in url:
        return "kisa"
    return "uzun"  # pencere sayısı paket.md boyuna bağlı → istek tahmini yok


def durum(v, kok=Path(cli.KOK), rapor=RAPOR):
    if (rapor / f"{v}.md").is_file():
        return "rapor"
    return "paket" if (kok / v / "paket.md").is_file() else "yeni"


def plan(linkler):
    return [(v, tur(u), durum(v), u) for u, v in dict.fromkeys((u, cli.m.vid(u)) for u in linkler)]


if __name__ == "__main__":
    assert [tur(u) for u in ("https://www.instagram.com/p/X/", "https://www.instagram.com/reel/X/",
                             "https://youtube.com/shorts/X", "https://youtu.be/X")] == ["karusel", "kisa", "kisa", "uzun"]
    p = plan(Path(sys.argv[1]).read_text(encoding="utf-8").split())
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text("id\ttur\tdurum\turl\n" + "".join("\t".join(s) + "\n" for s in p), encoding="utf-8")
    print(f"{len(p)} link · tür {dict(Counter(s[1] for s in p))} · durum {dict(Counter(s[2] for s in p))}")
    kalan = [s for s in p if s[2] != "rapor"]
    print(f"işlenecek {len(kalan)} · önce paket {sum(s[2] == 'yeni' for s in kalan)} · "
          f"Gemini ≈{ISTEK * sum(s[1] != 'uzun' for s in kalan)} istek (video başı {ISTEK}; model başı günlük kota ayrı, zincir {len(kisa.MODELLER)} model)")
