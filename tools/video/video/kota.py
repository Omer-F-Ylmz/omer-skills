"""VİDEO-3 V5: ortak günlük Gemini defteri + PerDay 429'da dur, kaldığı yerden sür.

kisa._uret 429 gövdesini 200 baytta kestiği için kota türü hata metninde görünmez (14 Eki d6);
toplu iş 429 görünce tek minik istekle yoklar, günlükse diğer modelleri denemeden durur.
"""
import json
import threading
import urllib.error
from datetime import date, datetime, timedelta, timezone

from . import kisa

DIZIN = kisa.KOK / ".kos" / "kopru" / "video"
_KILIT = threading.Lock()


def pt_tarih(simdi=None):
    """Gemini günlük kotası PT gece yarısı sıfırlanır → defter günü PT tarihi (tzdata yok, ABD yaz saati elle)."""
    u = simdi or datetime.now(timezone.utc)
    y = u.year
    mart = datetime(y, 3, 8 + (6 - date(y, 3, 8).weekday()) % 7, 10, tzinfo=timezone.utc)  # 2. pazar 02:00 PST
    kasim = datetime(y, 11, 1 + (6 - date(y, 11, 1).weekday()) % 7, 9, tzinfo=timezone.utc)  # 1. pazar 02:00 PDT
    return (u - timedelta(hours=7 if mart <= u < kasim else 8)).date().isoformat()


def _yol(tarih=None):
    return DIZIN / f"kota-{tarih or pt_tarih()}.json"


def oku(tarih=None):
    p = _yol(tarih)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"istek": {}, "tukendi": {}}


def _yaz(d, tarih=None):
    p = _yol(tarih)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def say(model, n=1, tarih=None):
    with _KILIT:
        d = oku(tarih)
        d["istek"][model] = d["istek"].get(model, 0) + n
        _yaz(d, tarih)


def sayan(uret):
    """kisa._uret biçimli (JSON, iz) dönen işlevi sarar; başarılı isteği modeline yazar (bağlama V4 hat'ta)."""
    def sar(*a, **k):
        j, iz = uret(*a, **k)
        say(iz["model"])
        return j, iz
    return sar


def cozumle(govde):
    """429 gövdesi → {gunluk, kota, limit, bekle}; ayrıştırılamazsa gunluk=False."""
    try:
        ayr = json.loads(govde).get("error", {}).get("details", [])
    except (ValueError, AttributeError):
        ayr = []
    v = next((x for d in ayr for x in d.get("violations", [])), {})
    bekle = next((d["retryDelay"] for d in ayr if "retryDelay" in d), "")
    kota = v.get("quotaId", "")
    return {"gunluk": "PerDay" in kota, "kota": kota, "limit": int(v["quotaValue"]) if v.get("quotaValue", "").isdigit() else None,
            "bekle": int(float(bekle.rstrip("s"))) if bekle else None}


def yokla(key, model, iste=kisa._iste):
    """Tek minik istek; açıksa {"gunluk": False}, 429 ise cozumle(tam gövde)."""
    try:
        iste(f"{kisa.API}/v1beta/models/{model}:generateContent", key,
             {"contents": [{"parts": [{"text": "1"}]}], "generationConfig": {"maxOutputTokens": 1}}, zaman=30)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return cozumle(e.read())
        raise
    say(model)
    return {"gunluk": False}


def tukendi(model, bilgi, tarih=None):
    with _KILIT:
        d = oku(tarih)
        d["tukendi"][model] = bilgi
        _yaz(d, tarih)


def acik_modeller(tarih=None):
    t = oku(tarih)["tukendi"]
    return tuple(m for m in kisa.MODELLER if m not in t)


def gun_bol(isler, istek_basi, gunluk):
    """Günlük istek tavanına göre işleri günlere böl (180 link ≈696 istek → ≥2 gün)."""
    n = max(1, gunluk // istek_basi)
    return [isler[i:i + n] for i in range(0, len(isler), n)]


def toplu(isler, is_, durum_yolu, key, yokla_=yokla):
    """Her işi sırayla koşar; biteni durum_yolu'na yazar (kaldığı yerden). PerDay 429 → dur.

    Hata veren iş elenmez: bitti'ye girmez, sonraki koşuda yeniden denenir.
    """
    durum = json.loads(durum_yolu.read_text(encoding="utf-8")) if durum_yolu.exists() else {"bitti": [], "hata": {}}

    def kaydet():
        durum_yolu.parent.mkdir(parents=True, exist_ok=True)
        durum_yolu.write_text(json.dumps(durum, ensure_ascii=False, indent=1), encoding="utf-8")

    for i in isler:
        if i in durum["bitti"]:
            continue
        if not acik_modeller():
            return {"dur": "gunluk", "kaldi": i, **durum}
        try:
            is_(i)
        except RuntimeError as e:
            durum["hata"][i] = str(e)[:300]
            kaydet()
            if "HTTP 429" in str(e):
                m = acik_modeller()[0]
                b = yokla_(key, m)
                if b["gunluk"]:
                    tukendi(m, b)  # PerDayPerProjectPerModel model başına ama zincirin hepsi aynı anda tükeniyor (14 Eki) → diğerlerini yakma
                    return {"dur": "gunluk", "kaldi": i, **durum}
            continue
        durum["bitti"].append(i)
        durum["hata"].pop(i, None)
        kaydet()
    return {"dur": "bitti", "kaldi": None, **durum}
