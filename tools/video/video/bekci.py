"""VİDEO-AKIL-1b-2a: bekçi. Paketteki aday-benzeri terimlerden raporun Adaylar'ında olmayanlar için tek kısa model çağrısı; evetler `kaynak: bekçi` satırıyla
Adaylar'a eklenir. Üretim hattına bağlı değil (karar ölçümden sonra)."""
import re

from . import tarama as tr
from .altin import eslesir

TAVAN = 60  # tek çağrıda sorulan en çok terim
SIS = ("Aday bekçisisin. Her terim bir video paketinden çıkarıldı. Terim videoda gösterilen/kullanılan/anlatılan bir araç, model, servis, kütüphane, font, "
       "skill, MCP, CLI ya da teknikse aday=true ve tur seç; genel kelime, yalnız reklamı yapılan ya da başka adayın parçasıysa aday=false ve neden yaz. "
       "Her terim için bir karar döndür. aday=true ise kanit: PAKET'ten birebir alıntı (en az 3 kelime, terimi içeren); aday=false ise kanit boş.")
SEMA = {"type": "object", "required": ["kararlar"], "additionalProperties": False, "properties": {"kararlar": {"type": "array", "items": {
    "type": "object", "required": ["terim", "aday", "tur", "neden", "kanit"], "additionalProperties": False,
    "properties": {"terim": {"type": "string"}, "aday": {"type": "boolean"}, "tur": {"type": "string", "enum": sorted(tr.TUR)}, "neden": {"type": "string"}, "kanit": {"type": "string"}}}}}}
FONT = r"\b[A-Z][a-z]+ (?:Sans|Serif|Grotesk|Mono|Display)\b"
ATLA = {"youtu.be", "youtube.com", "m.youtube.com"}
GENEL = {"html", "css", "dom", "api", "cpu", "gpu", "url", "json", "ui", "ux", "http", "https", "sql", "xml", "yaml", "pdf", "ram", "seo", "svg", "rest", "cli", "ide", "sdk", "ai", "llm"}  # genel terim: aday değil


def terimler(paket):
    """Saf: paket metninden aday-benzeri terimler (büyük harfli · tireli · CamelCase · .js/.ts · npm/pip/npx argümanı · font adı · link alan adı)."""
    t = paket.split("\n## Kareler")[0]
    t = "\n".join(s for s in t.splitlines() if not s.startswith(("#", "=")))
    out = set(re.findall(r"\b[A-Z]{6,}\b", t))  # ≤5 harfli hepsi-büyük kısaltma düşer
    out |= set(re.findall(r"\b[a-z]+(?:-[A-Za-z0-9]+)+\b", t))
    out |= set(re.findall(r"\b[A-Z][a-z]+(?:[A-Z][a-z0-9]+)+\b", t))
    out |= set(re.findall(r"\b[\w-]+\.(?:js|ts)\b", t))
    out |= {m for m in re.findall(r"(?:npm (?:i|install)|pip install|npx)\s+(?:-\S+\s+)*([\w@/.-]+)", t)}
    out |= set(re.findall(FONT, t))
    out |= {h for h in re.findall(r"https?://(?:www\.)?([^/\s?#]+)", t) if h not in ATLA}
    return {x for x in out if x.casefold() not in GENEL}


def kalan(rapor, terim):
    """Adaylar'daki herhangi bir adla eslesir olanlar düşer; sıralı, ≤ TAVAN."""
    ad = [r[0] for h, rows in tr.tablolar(tr.bolum(rapor, "Adaylar")) if h and h[0].casefold() == "ad" for r in rows if r]
    return sorted(x for x in terim if x.casefold() not in GENEL and not any(eslesir(x, a, []) for a in ad))[:TAVAN]


def _norm(x):
    return " ".join(x.casefold().split())


def kanitli(d, paket):
    """Saf: evet kararının kanıtı ≥ 3 kelime ve paketten birebir (boşluk/büyük-küçük harf esnek) mi."""
    k = _norm(d.get("kanit") or "")
    return len(k.split()) >= 3 and k in _norm(paket)


def bekci(rapor, paket, tas, model=None):
    """→ (yeni_rapor, {"cagri": 0|1, "eklenen": [terim], "usage", "usd"}). Kalan terim yoksa çağrı yok."""
    k = kalan(rapor, terimler(paket))
    if not k:
        return rapor, {"cagri": 0, "eklenen": [], "usage": {}, "usd": 0.0}
    y = tas(SIS, "TERİMLER:\n" + "\n".join(k), SEMA, **({"model": model} if model else {}))
    ek = [d for d in ((y.get("form") or {}).get("kararlar") or []) if d.get("aday") and d.get("terim") in k and kanitli(d, paket)]
    L = rapor.split("\n")
    i = next((n for n, s in enumerate(L) if s.startswith("## Adaylar")), None)
    if i is not None and ek:
        e = next((n for n in range(i + 1, len(L)) if L[n].startswith("## ")), len(L))
        j = max(n for n in range(i + 1, e) if L[n].startswith("|"))  # Adaylar tablosunun son satırı
        L[j + 1:j + 1] = [f"| {d['terim']} | yok | {d['tur']} | yok | {' '.join(d['neden'].replace('|', '/').split())} | yok | kaynak: bekçi |" for d in ek]
    return "\n".join(L), {"cagri": 1, "eklenen": [d["terim"] for d in ek], "usage": y.get("usage") or {}, "usd": y.get("usd")}
