"""12b video-tarama: kayıt, eski rapor içe alma, ad sözlüğü, tekilleme, işaret, rapor denetimi."""
import json
import re
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

from jev import skill as sk

from . import metin as m

ESIK = 0.8
YERLESIK = ("Claude Code", "Claude Desktop", "claude.ai")
DIS = {"skill", "plugin", "mcp", "yerlesik"}  # kurulu ya da platformda var → ÇİFT
BOLUM = ("Künye", "Özet", "Bölümler", "Adaylar", "Kareden okunanlar", "Belirsizlikler", "Atlanan")
TUR = {"skill", "plugin", "MCP", "CLI", "teknik", "iş akışı"}
ALINTI_KELIME = 15
DOSYA = re.compile(r"(?:(\d{4}-\d\d-\d\d)-)?([\w-]{11})")
ZAMAN = re.compile(r"(?<![\d:.])(?:\d{1,2}:)?\d{1,2}:\d{2}(?![\d:])")
ALINTI = re.compile(r"[“\"]([^”\"\n]*)[”\"]")
MADDE = re.compile(r"^- (.+?) → (\S+)")


def normal(ad):
    return re.sub(r"[\W_]+", "", ad.casefold())


def _hucre(satir):
    return [x.strip() for x in satir.strip().strip("|").split("|")]


def tablolar(metin):
    """[(başlık hücreleri, [satır hücreleri])] — ayraç satırı (|---|) atlanır."""
    out, cur = [], None
    for s in metin.splitlines():
        if not s.lstrip().startswith("|"):
            cur = None
            continue
        h = _hucre(s)
        if cur is None:
            cur = (h, [])
            out.append(cur)
        elif not all(set(x) <= set("-: ") for x in h):
            cur[1].append(h)
    return out


def bolum(metin, ad):
    """`## ad…` başlığından bir sonraki `## `'e kadar."""
    b = re.search(rf"^## {re.escape(ad)}.*?$(.*?)(?=^## |\Z)", metin, re.M | re.S | re.I)
    return b.group(1) if b else ""


def ayikla(metin):
    """Eski ve yeni rapordan (adaylar, ele): ilk sütunu `ad` olan tablolar + `- ad → ETİKET` maddeleri."""
    adaylar, ele = [], []
    for bas, satirlar in tablolar(metin):
        if bas[0].casefold() != "ad":
            continue
        e = bas.index("etiket") if "etiket" in bas else None
        for h in satirlar:
            adaylar.append(h[0])
            if e is not None and e < len(h) and h[e].upper().startswith("ELE"):
                ele.append(h[0])
    for s in metin.splitlines():
        x = MADDE.match(s)
        if x:
            adaylar.append(x[1].strip())
            if x[2].upper().startswith("ELE"):
                ele.append(x[1].strip())
    return list(dict.fromkeys(a for a in adaylar if a)), list(dict.fromkeys(ele))


def rapor_id(yol):
    x = DOSYA.fullmatch(Path(yol).stem)
    # ponytail: "00-envanter" 11 krk'lık id biçiminde; iki rakam-tire-küçük harf kalıbı id sayılmaz
    if not x or re.fullmatch(r"\d\d-[a-z]+", Path(yol).stem):
        return None, None
    return x[2], x[1]


def ice_al(dizin):
    out = []
    for f in sorted(Path(dizin).glob("*.md")):
        v, tarih = rapor_id(f)
        if v is None:
            continue
        adaylar, ele = ayikla(f.read_text(encoding="utf-8"))
        tarih = tarih or date.fromtimestamp(f.stat().st_mtime).isoformat()
        out.append({"id": v, "tarih": tarih, "rapor": f.name, "adaylar": adaylar, "ele": ele})
    return out


def kayit_oku(yol):
    yol = Path(yol)
    return [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()] if yol.is_file() else []


def kayit_yaz(yol, girdiler):
    Path(yol).write_text("".join(json.dumps(g, ensure_ascii=False) + "\n" for g in girdiler), encoding="utf-8")


def ayir(ids, kayit, yeniden=False):
    """(taranacak, atlanan): kayıttaki id yalnız --yeniden ile yeniden taranır."""
    gorulen = {k["id"] for k in kayit}
    tara = [v for v in ids if yeniden or v not in gorulen]
    return tara, [v for v in ids if v not in tara]


def dalgalar(ids, n=3):
    """Alt ajan dalgaları: aynı anda en fazla n."""
    return [ids[i:i + n] for i in range(0, len(ids), n)]


def _json(yol):
    try:
        return json.loads(Path(yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sozluk_kur(ev, kayit):
    """[(ad, kaynak)]: yerleşik · skill katalogu · plugin · MCP (yalnız anahtar adları) · kayıt adayları · ELE."""
    ev = Path(ev)
    out = [(a, "yerlesik") for a in YERLESIK]
    out += [(ad, "skill") for ad, _ in sk.adaylar(ev)]
    out += [(k.partition("@")[0], "plugin") for k in ((_json(ev / ".claude" / "plugins" / "installed_plugins.json") or {}).get("plugins") or {})]
    cj = _json(ev / ".claude.json") or {}
    mcp = list(cj.get("mcpServers") or {}) + [a for p in (cj.get("projects") or {}).values() for a in (p.get("mcpServers") or {})]
    out += [(a, "mcp") for a in dict.fromkeys(mcp)]
    for k in kayit:
        ele = set(k.get("ele") or [])
        out += [(a, "ele" if a in ele else "kayit") for a in k.get("adaylar") or []]
    return list(dict.fromkeys(out))


def _parcalar(ad):
    return {normal(x) for x in (ad, ad.rsplit(":", 1)[-1], ad.rsplit("/", 1)[-1])} - {""}


def eslestir(ad, sozluk, esik=ESIK):
    """En yakın sözlük adı (ad, kaynak, skor) ya da None. Tam ad, `p:ad` ve `owner/repo`'nun son parçası karşılaştırılır."""
    aday, iyi = _parcalar(ad), (None, 0.0)
    for s_ad, kaynak in sozluk:
        for a in aday:
            for b in _parcalar(s_ad):
                sm = SequenceMatcher(None, a, b)
                if sm.real_quick_ratio() > iyi[1] and sm.quick_ratio() > iyi[1]:
                    r = sm.ratio()
                    if r > iyi[1]:
                        iyi = ((s_ad, kaynak), r)
    return (*iyi[0], round(iyi[1], 2)) if iyi[0] and iyi[1] >= esik else None


def tekille(adaylar):
    """Aynı ad (normalize) tek kayıt; videolar birleşir, ilk görülenin alanları kalır."""
    out = {}
    for x in adaylar:
        k = normal(x["ad"])
        if k not in out:
            out[k] = {**x, "ad": x["ad"].strip(), "videolar": []}
        if x.get("video") not in out[k]["videolar"]:
            out[k]["videolar"].append(x.get("video"))
    return list(out.values())


def isaret(es, cift, risk):
    """Eleme yok: yalnız işaret. es=(ad, kaynak, skor)|None; cift=Jev çift p; risk=izin riski 0-3."""
    if (es and es[1] in DIS) or (cift is not None and cift >= 0.5):
        return "ÇİFT"
    if es:
        return "ÖNCEDEN-GÖRÜLDÜ"
    if cift is None or risk is None or risk >= 2:
        return "BEKLE"
    return "UYGULA"


def aday_satirlari(metin):
    """Yeni rapordaki ADAYLAR tablosunun satırları."""
    t = tablolar(bolum(metin, "Adaylar"))
    return t[0][1] if t else []


def denetle(metin, sure=None):
    """Hata listesi (boşsa geçti): zorunlu bölümler · süre dışı zaman · aday alanları · alıntı ≤15 kelime."""
    h = []
    basliklar = [s[3:].strip().casefold() for s in metin.splitlines() if s.startswith("## ")]
    h += [f"bölüm eksik: ## {b}" for b in BOLUM if not any(x.startswith(b.casefold()) for x in basliklar)]
    if sure:
        h += [f"süre dışı zaman: {z} > {m.ss(sure)}" for z in ZAMAN.findall(metin) if m.sn(z) > sure]
    for s in aday_satirlari(metin):
        if len(s) != 7 or any(x in ("", "-") for x in s):
            h.append(f"boş alan: aday satırı {s[0] or '?'} (7 alan dolu olmalı: ad·sözlük·tür·link·ne işe yarar·zaman·kanıt)")
        elif s[2] not in TUR:
            h.append(f"tür geçersiz: {s[0]} → {s[2]} ({', '.join(sorted(TUR))})")
    h += [f"alıntı {len(a.split())} kelime > {ALINTI_KELIME}: {a[:40]}…" for a in ALINTI.findall(metin) if len(a.split()) > ALINTI_KELIME]
    return h
