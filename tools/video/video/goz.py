"""VİDEO-GÖZ-1b-1: GÖZ katmanı saf yardımcıları (ekran metni süzgeci · model karesi ölçeği · kare seçimi · yorum/URL · ad sözlüğü)."""
import re

from .altin import norm

OCR_GUVEN, OCR_BUTCE, MODEL_KENAR = 0.5, 3000, 768  # ayar · M1: RapidOCR skor eşiği · Ekran metni jeton bütçesi · modele giden kare uzun kenarı
URL_KOMUT = re.compile(r"https?://|www\.|\b[\w-]+\.(?:com|io|ai|dev|app|org|net|co|so|sh|gg|xyz|me|tr|tech|studio|design)\b"
                       r"|\b(?:npx|npm|pip|uvx?|claude|git|gh|curl|winget|brew)\b|--\w|`", re.I)
TERIM = re.compile(r"\b(?:[A-Z][a-z]+[A-Z]\w*|[A-Za-z]+\d[\w.]*|[A-Z]{3,}\w*)\b")  # CamelCase · harf+rakam · KISALTMA


def ocr_satirlar(sonuc, esik=OCR_GUVEN):
    """RapidOCR [(metin, skor, üst y)] → skoru ≥ esik satırlar, yukarıdan aşağı."""
    return [x.strip() for x, s, _ in sorted(sonuc, key=lambda r: r[2]) if s >= esik and x.strip()]


def _pencere(s):
    k = [norm(w) for w in re.findall(r"\w+", s.casefold())]
    return {"".join(k[i:i + n]) for n in range(1, 4) for i in range(len(k))}


def sozlukte(satir, sozluk):
    """Satırda sözlük adı geçiyor mu: norm ≤4 kelime sınırıyla, ≥5 alt dize (altin.gecer'in lev'siz hâli)."""
    d, p = norm(satir), None
    for a in sozluk:
        n = norm(a)
        if len(n) > 4 and n in d:
            return True
        if 0 < len(n) <= 4 and n in (p := p if p is not None else _pencere(satir)):
            return True
    return False


def oncelik(satir, sozluk, altyazi):
    if sozlukte(satir, sozluk):
        return 0
    if URL_KOMUT.search(satir):
        return 1
    return 2 if any(norm(t) not in altyazi for t in TERIM.findall(satir)) else 3


def ekran_metni(metin, altyazi, sozluk=(), butce=OCR_BUTCE, token=lambda s: len(s) // 4 + 1):
    """metin [(t, [satır])] → [(t, satır)] zaman sırasıyla. Aynı satır bir kez, altyazıda zaten geçen satır yok; bütçe aşılırsa
    öncelik sözlük > URL/komut > yeni teknik terim > diğer (eşitte erken zaman)."""
    alt, gor, aday = norm(altyazi), set(), []
    for t, ss in sorted(metin):
        for x in ss:
            if not (k := norm(x)) or k in gor or k in alt:
                continue
            gor.add(k)
            aday.append((oncelik(x, sozluk, alt), t, x))
    tut, top = [], 0
    for _, t, x in sorted(aday, key=lambda a: (a[0], a[1])):
        if top + token(x) <= butce:
            top += token(x)
            tut.append((t, x))
    return sorted(tut)


MODEL_KOK = "C:/Projeler/.tmp-video/models/rapidocr/"  # ayar · VIDEO_OCR_MODEL ile değişir


def rapid_yukle():
    """Gerçek RapidOCR (det/cls PP-OCR mobile + Latin PP-OCRv5 rec, yerel model, ağ yok) → yol → [(metin, skor, üst y)].
    Import/model hatası yükselir: cli._ocr Windows OCR'a düşer. ponytail: ı → i okunur (Latin sözlüğü); eşleşme norm'la."""
    import os
    from rapidocr import LangCls, LangDet, LangRec, ModelType, OCRVersion, RapidOCR
    k = (os.environ.get("VIDEO_OCR_MODEL") or MODEL_KOK).rstrip("/\\") + "/"
    dosya = {"Det.model_path": "ch_PP-OCRv5_det_mobile.onnx", "Cls.model_path": "ch_ppocr_mobile_v2.0_cls_mobile.onnx",
             "Rec.model_path": "latin_PP-OCRv5_rec_mobile.onnx", "Rec.rec_keys_path": "ppocrv5_latin_dict.txt"}
    if eksik := [f for f in dosya.values() if not os.path.isfile(k + f)]:
        raise FileNotFoundError(f"model yok: {', '.join(eksik)}")
    ocr = RapidOCR(params={"Global.model_root_dir": k, **{a: k + f for a, f in dosya.items()},
                           "Det.ocr_version": OCRVersion.PPOCRV5, "Det.lang_type": LangDet.CH, "Det.model_type": ModelType.MOBILE,
                           "Cls.ocr_version": OCRVersion.PPOCRV4, "Cls.lang_type": LangCls.CH, "Cls.model_type": ModelType.MOBILE,
                           "Rec.ocr_version": OCRVersion.PPOCRV5, "Rec.lang_type": LangRec.LATIN, "Rec.model_type": ModelType.MOBILE})

    def oku(yol):
        r = ocr(str(yol))
        return [(t, float(s), float(min(p[1] for p in b))) for t, s, b in
                zip(r.txts or (), r.scores or (), r.boxes if r.boxes is not None else ())]
    return oku


def olcek(w, h, kenar=MODEL_KENAR):
    """Modele giden kare: uzun kenar ≤ kenar (büyütme yok), iki kenar da 28'in katına aşağı yuvarlanır."""
    o = min(1, kenar / max(w, h))
    return int(w * o) // 28 * 28, int(h * o) // 28 * 28
