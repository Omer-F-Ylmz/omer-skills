"""VİDEO-GÖZ-1b-1: GÖZ katmanı saf yardımcıları (ekran metni süzgeci · model karesi ölçeği · kare seçimi · yorum/URL · ad sözlüğü)."""
import heapq
import re
from difflib import SequenceMatcher
from pathlib import Path

from . import metin as m
from .altin import lev, norm, url_norm

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


def _bilgi(s):
    """1b-1S S1: satırın bilgi birimleri — ≥3 harfli kelimeler (norm) ve ardışık kelime çiftleri."""
    k = [n for w in re.findall(r"\w+", s) if (n := norm(w))]
    return {w for w in k if len(w) >= 3} | {f"{a} {b}" for a, b in zip(k, k[1:])}


def ekran_metni(metin, altyazi, sozluk=(), butce=OCR_BUTCE, token=lambda s: len(s) // 4 + 1):
    """metin [(t, [satır])] → [(t, satır)] zaman sırasıyla. altyazı = paketin başka bölümlerinde yazan metin (1b-1S S1). Satır yalnız
    yeni bilgi getiriyorsa (tutulan ekran metninde ve altyazıda olmayan ≥1 kelime ya da çift) tutulur; öncelik sözlük > URL/komut >
    yeni teknik terim > diğer; düzey içinde açgözlü: kalanlardan yeni bilgi/token en büyük olan (eşitte erken zaman), kazancı 0 düşer,
    bütçeye sığmayan atlanır (DEVAM-4)."""
    alt, gor, aday = norm(altyazi), set(), []
    for t, ss in sorted(metin):
        for x in ss:
            if not (k := norm(x)) or k in gor:
                continue
            gor.add(k)
            aday.append((oncelik(x, sozluk, alt), t, x))
    bil, tut, top = _bilgi(altyazi), [], 0
    for p in sorted({a[0] for a in aday}):  # DEVAM-4: düzey içinde lazy greedy — kazanç yalnız azalır, yığındaki değer üst sınır
        yig = [(-len(_bilgi(x) - bil) / token(x), t, x) for q, t, x in aday if q == p]
        heapq.heapify(yig)
        while yig:
            k, t, x = heapq.heappop(yig)
            if not (g := len(_bilgi(x) - bil)):
                continue
            if -g / token(x) > k:
                heapq.heappush(yig, (-g / token(x), t, x))
            elif top + token(x) <= butce:
                top += token(x)
                bil |= _bilgi(x)
                tut.append((t, x))
    return sorted(tut)


SAHNE_HAM, OCR_DEGISIM, OCR_GUVENLIK, MODEL_UST = 5, 0.15, 900, 6  # ayar · M2: sahne Hamming > · OCR metin değişimi ≥ · 1b-1R R4: OCR güvenlik tavanı sn (kesim kare sayısıyla) · model karesi
AD = re.compile(r"\b[A-Z][\w.+-]{2,}|(?:https?://|www\.)\S+|\b[\w-]+\.(?:com|io|ai|dev|app|org|net|co|so|sh|gg|xyz|me|tr|tech|studio|design)\b\S*")


def fps(sure):
    return 0.5 if sure >= 600 else 1


def sahneler(hashler, f):
    """Aşama 1: [dHash] (fps f, zaman sırası) → [(t, Hamming)]; son tutulan kareye Hamming > SAHNE_HAM olan an sahne, ilk kare hep (64)."""
    out, son = [], None
    for i, h in enumerate(hashler):
        if (d := 64 if son is None else bin(h ^ son).count("1")) > SAHNE_HAM:
            out.append((round(i / f, 1), d))
            son = h
    return out


TAVAN_SURUM = "sahne+dk12/800"  # önbellek anahtarı: tavanın sayısı değil formülü
YOGUN_SURUM, YOGUN_UST = "url±2/120", 120  # DEVAM-4: URL'li karenin komşuları, tavan dışı ek kare üst sınırı
URL_BENZER = re.compile(r"https?://|www\.|[a-z0-9-]+\.(?:ai|com|io|dev|app|sh|so|org|net|co)\b", re.I)


def url_benzer(x):
    return bool(URL_BENZER.search(x))


def yogun_zaman(okunmus, url_t, sure, ust=YOGUN_UST):
    """DEVAM-4: URL benzeri satırlı karelerin t-2..t+2 sn komşuları; okunmuş ve [0, süre] dışı atlanır, URL zaman sırasıyla en çok ust, sıralı."""
    gor, ek = set(okunmus), []
    for t in sorted(url_t):
        for k in (t - 2, t - 1, t + 1, t + 2):
            if 0 <= k <= sure and k not in gor and len(ek) < ust:
                gor.add(k)
                ek.append(k)
    return sorted(ek)


def tavan_ocr(sure, n_sahne):
    """1b-1T T3: OCR kare tavanı = atım öncesi sahne sayısı + dk×12, en çok 800 — 5 sn tabanı (dk×12) hep sığar, aralık yalnız 800'de büyür."""
    return min(800, n_sahne + int(sure / 60 * 12))


def sahne_sec(sahne, tavan):
    """Tavan aşılırsa en az değişen (düşük Hamming) sahneler atılır; zaman sırası korunur."""
    return sorted(sorted(sahne, key=lambda s: -s[1])[:tavan])


TABAN_SN = (5, 10, 15, 20)  # ayar · 1b-1T S4: A tam karede buluyor → 5 sn · 1b-1R R3: periyodik taban aralıkları sn (tavan aşılırsa büyür)


def kare_sec(sahne, sure, f, tavan, taban=TABAN_SN):
    """1b-1R R3: sahneler + periyodik taban — sahne olmayan her `a` sn'ye bir kare (fark 0). Tavan aşılırsa aralık 5→10→15→20 büyür,
    sahneler korunur; 20 sn'de de aşılırsa en düşük Hamming'li sahneler atılır (sahne_sec). Zaman sıralı.
    ponytail: taban kareleri atılmadan önceki sahnelere göre; uzun boşluk kalırsa sahne atımı sonrası yeniden hesap."""
    for a in taban:
        uc = [t for t, _ in sahne] + [sure]
        per = [(round((b + a * k) * f) / f, 0) for b, c in zip(uc, uc[1:]) for k in range(1, int((c - b) / a) + 1) if b + a * k < c]
        if len(sahne) + len(per) <= tavan:
            break
    else:
        sahne = sahne_sec(sahne, max(tavan - len(per), 1))
    return sorted(sahne + per)


def kapsam_sira(n):
    """1b-1R R4: OCR sırası kapsamaya göre — eşit aralıklı seyrek geçiş, sonra boşluklar (8 → 0,4,2,6,1,3,5,7); kesilirse kayıp videoya yayılır."""
    s, sira, gor = 1 << max(n - 1, 0).bit_length(), [], set()
    while s:
        yeni = [i for i in range(0, n, s) if i not in gor]
        sira += yeni
        gor.update(yeni)
        s //= 2
    return sira


def ocr_sec(okunan, esik=OCR_DEGISIM):
    """Aşama 2: [(t, satırlar)] zaman sırasıyla → son tutulan metne göre değişim (1 - benzerlik) ≥ esik olanlar; metinsiz kare yok."""
    tut, son = [], ""
    for t, s in okunan:
        if (k := "\n".join(s).casefold()) and 1 - SequenceMatcher(None, son, k, autojunk=False).ratio() >= esik:
            tut.append((t, s))
            son = k
    return tut


def butce(sure):
    return min(5000, max(1500, int(sure / 60 * 300)))  # 1b-1S: dk×200→300 (bütçe-attı; toplam token ≤49465)


def model_sec(okunan, altyazi, isaret, n=MODEL_UST):
    """Modele ≤n kare (sahne varsa en az min(n, sahne)): önce en çok yeni ad/URL getiren (altyazıda ve önceki karelerde yok), sonra segment
    işaretine ≤5 sn yakın, sonra zaman."""
    alt, gor, puan = norm(altyazi), set(), []
    for t, s in sorted(okunan):
        yeni = {k for x in s for z in AD.findall(x) if (k := norm(z)) and k not in alt} - gor
        gor |= yeni
        puan.append((-len(yeni), not any(abs(t - i) <= 5 for i in isaret), t))
    return sorted(t for *_, t in sorted(puan)[:n])


YORUM_SATIR = re.compile(r"https?://|www\.|\b(?:npx|pip|uvx?|git)\b|`|\b\d{1,2}:\d{2}\b", re.I)
URL_BUL = re.compile(r"(?:https?://)?(?:localhost:\d+|(?:[\w-]+\.)+(?:com|io|ai|dev|app|org|net|co|so|sh|gg|xyz|me|tr|tech|studio|design|no)\b)"
                     r"(?:/[^\s)\]>,'\"]*)?", re.I)


TIRELI = re.compile(r"\b[^\W\d_]+(?:-[^\W\d_]+)+\b")  # 1b-1S S3: cut-and-extend


def _yorum_oncelikli(x, sozluk):
    return bool(YORUM_SATIR.search(x) or sozlukte(x, sozluk) or TERIM.search(x) or TIRELI.search(x))


def aciklama_duz(aciklama, butce=600, token=lambda s: len(s) // 4 + 1):
    """DEVAM-1: açıklama düz metni; URL ve chapter (zaman damgalı) satırları çıkar (başka bölümde var), boş satırlar tekil, ≤ butce tk (taşan satırlar atılır)."""
    out, top = [], 0
    for x in (x.strip() for x in (aciklama or "").splitlines()):
        if not x or re.search(r"https?://", x) or re.match(r"^\W*(?:\d{1,2}:)?\d{1,2}:\d{2}\b", x):
            continue
        if top + token(x) > butce:
            break
        out.append(x)
        top += token(x)
    return out


def yorum_sec(ham, sozluk=(), butce=1500, token=lambda s: len(s) // 4 + 1):
    """M4: sabit ve kanal sahibi yorumu tam (satırlar ' / '), diğerlerinden yalnız link/kod/komut/zaman damgası/sözlük adı/TERIM/tireli
    terim taşıyan satır; öncelik sabit > sahip > diğer (yt-dlp top sırası), ≤ butce. 1b-1S S3b: sabit/sahip yorumu kalan bütçeyi aşarsa
    atılmaz, satırlarına bölünür — önce öncelikli satırlar, kalan bütçe sırayla; seçilenler özgün sırada."""
    out, top = [], 0
    for k in ("pinned", "sahip"):
        for h in ham:
            if not h.get(k) or (k == "sahip" and h.get("pinned")):
                continue
            on, sat = f"[{'sabit' if k == 'pinned' else 'sahip'}] ", [x.strip() for x in h["text"].splitlines() if x.strip()]
            if token(on + " / ".join(sat)) > butce - top:
                sec = set()
                for n in sorted(range(len(sat)), key=lambda n: not _yorum_oncelikli(sat[n], sozluk)):
                    if token(on + " / ".join(sat[i] for i in sorted(sec | {n}))) <= butce - top:
                        sec.add(n)
                sat = [sat[i] for i in sorted(sec)]
            if sat:
                out.append(x := on + " / ".join(sat))
                top += token(x)
    for x in [x.strip() for h in ham if not (h.get("pinned") or h.get("sahip")) for x in h["text"].splitlines()
              if x.strip() and _yorum_oncelikli(x, sozluk)]:
        if top + token(x) <= butce:
            top += token(x)
            out.append(x)
    return out


def urller_bul(kaynaklar):
    """M4: [(kaynak, t, metin)] → [(url, kaynak, ilk t)] tekil (url_norm), zamana göre; konuşmadaki 'dot/nokta' noktaya çevrilir."""
    ilk = {}
    for k, t, x in kaynaklar:
        for u in URL_BUL.findall(re.sub(r"\s+(?:dot|nokta)\s+", ".", x, flags=re.I)):
            if (a := url_norm(u := u.rstrip(".,;:"))) not in ilk or t < ilk[a][2]:
                ilk[a] = (u, k, t)
    return sorted(ilk.values(), key=lambda v: v[2])


def sozluk_oku(yol):
    """M5: sozluk.txt 'kanonik | alias, alias' (# yorum, boş satır atlanır) → [(kanonik, [alias])]; dosya yoksa []."""
    y = Path(yol)
    return [(k.strip(), [x.strip() for x in a.split(",") if x.strip()]) for s in (y.read_text(encoding="utf-8").splitlines() if y.is_file() else [])
            if s.strip() and not s.lstrip().startswith("#") for k, _, a in [s.partition("|")]]


def sozluk_adlari(sz):
    return [x for k, a in sz for x in (k, *a)]


def eslesmeler(kaynaklar, sz):
    """M5: [(kaynak, t, metin)] → [(kanonik, kaynak, ilk t, bulanık biçim | None)] zamana göre. Kesin: norm ≤4 kelime sınırı, ≥5 alt dize;
    kesin yoksa yalnız ses kaynağında bulanık öneri (ilk harf aynı, lev ≤1; ≥8 harfte ≤2). Metin değişmez, yalnız eşleme satırı."""
    adlar, ilk = [(k, [n for a in (k, *al) if (n := norm(a))]) for k, al in sz], {}
    for kay, t, x in sorted(kaynaklar, key=lambda q: q[1]):
        d, p = norm(x), _pencere(x)
        for k, ns in adlar:
            if k in ilk:
                continue
            if any(n in p if len(n) <= 4 else n in d for n in ns):
                ilk[k] = (k, kay, t, None)
            elif kay == "ses" and (w := next((w for n in ns if len(n) >= 5 for w in p if w[:1] == n[:1] and abs(len(w) - len(n)) <= 2
                                              and lev(w, n) <= (2 if len(n) >= 8 else 1)), None)):
                ilk[k] = (k, kay, t, w)
    return sorted(ilk.values(), key=lambda v: v[2])


def eslesme_satirlari(es):
    return [f"{k} · {kay} · {m.ss(t) if kay in ('ekran', 'ses') else '-'}" + (f" · bulanık: {w}" if w else "") for k, kay, t, w in es]


def groq_prompt(sz, metin, sinir=224, tk=lambda s: len(s) // 4 + 1):
    """M3: Groq/Whisper prompt'u — altın-hariç sözlüğün kanonik adları; metinde (açıklama/ekran) geçenler önce (geçiş sırasıyla),
    sonra sözlük sırası; ', ' ile ≤ sinir jeton."""
    d = norm(metin)
    yer = {k: min((i for a in (k, *al) if len(n := norm(a)) > 2 and (i := d.find(n)) >= 0), default=-1) for k, al in sz}
    out = ""
    for k in [*sorted((k for k in yer if yer[k] >= 0), key=yer.get), *(k for k in yer if yer[k] < 0)]:
        if tk(y := f"{out}, {k}" if out else k) > sinir:
            break
        out = y
    return out


def parca_plani(sure, bayt, sinir=24_000_000):
    """M3: 16 kHz mono FLAC ≤ sinir bayt parçalar → [(başlangıç sn, süre sn)] (eşit süre)."""
    n = -(-bayt // sinir)
    uz = -(-int(sure) // n) if n > 1 else sure
    return [(i * uz, uz) for i in range(n)]


def birlestir(parcalar):
    """M3: [(offset, Groq segments)] → [(t, metin)]; boş metin atılır."""
    return [(round(offset + x["start"], 3), x["text"].strip()) for offset, ss in parcalar for x in ss if x["text"].strip()]


MODEL_KOK = "C:/Projeler/.tmp-video/models/rapidocr/"  # ayar · VIDEO_OCR_MODEL ile değişir
MODEL_DOSYA = {"Det.model_path": "ch_PP-OCRv5_det_mobile.onnx", "Cls.model_path": "ch_ppocr_mobile_v2.0_cls_mobile.onnx",
               "Rec.model_path": "latin_PP-OCRv5_rec_mobile.onnx", "Rec.rec_keys_path": "ppocrv5_latin_dict.txt"}  # gitleaks:allow (dosya adı) · 1b-1R R1: OCR önbellek anahtarında
OCR_CIHAZ = "dml"  # ayar · 1b-1R R4: dml | cpu — 20 kare DML 0,245 vs CPU 1,585 sn/kare (6,5×) → dml


def rapid_yukle(cihaz=None):
    """Gerçek RapidOCR (det/cls PP-OCR mobile + Latin PP-OCRv5 rec, yerel model, ağ yok) → yol → [(metin, skor, üst y)].
    Import/model hatası yükselir: cli._ocr Windows OCR'a düşer. ponytail: ı → i okunur (Latin sözlüğü); eşleşme norm'la."""
    import os
    from rapidocr import LangCls, LangDet, LangRec, ModelType, OCRVersion, RapidOCR
    k = (os.environ.get("VIDEO_OCR_MODEL") or MODEL_KOK).rstrip("/\\") + "/"
    if eksik := [f for f in MODEL_DOSYA.values() if not os.path.isfile(k + f)]:
        raise FileNotFoundError(f"model yok: {', '.join(eksik)}")
    cihaz = cihaz or OCR_CIHAZ
    if cihaz == "dml":  # R4: DirectML yalnız sağlayıcı varsa; 1b-1S S5: yoksa cpu, künyede "cpu (dml yok)" (kur.sh override'ı düşmüş olabilir)
        import onnxruntime
        cihaz = "dml" if "DmlExecutionProvider" in onnxruntime.get_available_providers() else "cpu (dml yok)"
    ocr = RapidOCR(params={"Global.model_root_dir": k, "EngineConfig.onnxruntime.use_dml": cihaz == "dml", **{a: k + f for a, f in MODEL_DOSYA.items()},
                           "Det.ocr_version": OCRVersion.PPOCRV5, "Det.lang_type": LangDet.CH, "Det.model_type": ModelType.MOBILE,
                           "Cls.ocr_version": OCRVersion.PPOCRV4, "Cls.lang_type": LangCls.CH, "Cls.model_type": ModelType.MOBILE,
                           "Rec.ocr_version": OCRVersion.PPOCRV5, "Rec.lang_type": LangRec.LATIN, "Rec.model_type": ModelType.MOBILE})

    def oku(yol):
        r = ocr(str(yol))
        return [(t, float(s), float(min(p[1] for p in b))) for t, s, b in
                zip(r.txts or (), r.scores or (), r.boxes if r.boxes is not None else ())]
    oku.cihaz = cihaz
    return oku


def olcek(w, h, kenar=MODEL_KENAR):
    """Modele giden kare: uzun kenar ≤ kenar (büyütme yok), iki kenar da 28'in katına aşağı yuvarlanır."""
    o = min(1, kenar / max(w, h))
    return int(w * o) // 28 * 28, int(h * o) // 28 * 28
