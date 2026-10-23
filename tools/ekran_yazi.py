"""Ekran altyazısı: videonun alt-orta şeridini sık aralıkla OCR'lar, gömülü altyazıyı zaman damgalı satır olaylarına çevirir.

Gömülü altyazıyı videoyu yapan insan yazmıştır: ASR için ikinci kanıt. Aynı satır her karede tekrarlandığı için olay = satırın ilk görüldüğü an.
Kullanım: python tools/ekran_yazi.py <video.mp4> [cikti.json]   (venv-ocr: CUDA OCR)
"""
import difflib
import json
import re
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

FPS = 3
SERIT = "crop=iw:ih*0.5:0:ih*0.4,scale=720:-1"  # alt-orta yarım: reels altyazısı burada, ekran kaydı arayüzü büyük ölçüde dışarıda
_TR = str.maketrans("çğıöşüâî", "cgiosuai")


def kat(s):
    """Türkçe katlama: OCR'ın düşürdüğü aksanlar eşitlenir (görünmez = gorunmez); noktalama gider."""
    s = s.replace("İ", "i").replace("I", "ı").lower().translate(_TR)
    return re.sub(r"[^a-z0-9]+", "", s)


def serit_ocr(video, d):
    """[(t_sn, [satır, ...])]; satır = OCR metni (güven > 0.7, ≥3 karakter)."""
    import video_derin as vd  # CUDA DLL PATH'i + ortak OCR motoru
    k = Path(d) / "s"
    shutil.rmtree(k, ignore_errors=True)
    k.mkdir(parents=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(video), "-vf", f"fps={FPS},{SERIT}", "-q:v", "3", str(k / "%04d.jpg")], capture_output=True)
    m = vd.ocr_motor()
    out = []
    for i, f in enumerate(sorted(k.glob("*.jpg"))):
        res, _ = m(str(f))
        sat = sorted(((r[0][0][1], r[1].strip()) for r in res or [] if float(r[2]) > 0.7 and len(r[1].strip()) >= 3))
        out.append((round(i / FPS, 2), [t for _, t in sat]))
    return out


def olaylar(kareler, kalici=0.5):
    """Kare satırlarından altyazı olayları [(t, metin)]. Karelerin yarısından fazlasında duran satır (başlık, filigran) atılır;
    benzer satır (≥0.8) son 12 olayda varsa yenisi sayılmaz, öncekinin uzamışı (önek) ise onu günceller."""
    n = max(len(kareler), 1)
    sayac = {}
    for _, sat in kareler:
        for s in {kat(x) for x in sat}:
            sayac[s] = sayac.get(s, 0) + 1
    ol = []
    for t, sat in kareler:
        for s in sat:
            ks = kat(s)
            if not ks or sayac[ks] / n > kalici:
                continue
            son = ol[-12:]
            if any(difflib.SequenceMatcher(None, ks, kat(m)).ratio() >= 0.8 for _, m in son):
                for j in range(len(ol) - len(son), len(ol)):
                    ek = kat(ol[j][1])
                    if ks.startswith(ek) and len(ks) > len(ek):
                        ol[j] = (ol[j][0], s)
                continue
            ol.append((t, s))
    return ol


def var_mi(olay_listesi, min_olay=6):
    """Videoda gömülü altyazı var mı: yeterince çok farklı kısa satır."""
    return len(olay_listesi) >= min_olay


if __name__ == "__main__":
    d = tempfile.mkdtemp(prefix="ey_")
    try:
        kare = serit_ocr(sys.argv[1], d)
        ol = olaylar(kare)
        veri = {"kareler": kare, "olaylar": ol}
        if len(sys.argv) > 2:
            Path(sys.argv[2]).write_text(json.dumps(veri, ensure_ascii=False), encoding="utf-8")
        print(len(kare), "kare", len(ol), "olay")
    finally:
        shutil.rmtree(d, ignore_errors=True)
