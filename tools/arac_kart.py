"""BEYIN-ARAC-KART-1: kurulu araç kartları (≤150 jeton) + kasa dışı bölüm indeksi (SQLite FTS5) + canlı geçmiş/kombin/ders.
  python tools/arac_kart.py yenile [--ekle ad ...]   kartları + bölüm indeksini artımlı yeniler (kaynak hash değişen/kartsız araç)
  python tools/arac_kart.py bayat                    kaynağı değişmiş ya da kartsız kurulu araçlar
  python tools/arac_kart.py ozet                     sayım + alan doluluğu
Üç katman: kart docs/arac-kart/kart.jsonl · bölüm indeksi .kos/arac-kart/bolum.db (kasa dışı) · tam metin kaynağında (kartta yol + hash).
Girdi (yeniden kullanım): docs/katalog/yetenek.jsonl (envanter), docs/atlas/kart.jsonl (ne/ne_zaman/kanıt yolu), docs/katalog/ogrenim.jsonl,
.kos/kopru/ajan-sira/*.json (+ .zorunlu/.denetim) ve ajan-sira.log (canlı geçmiş), beyin-olay.jsonl (ders). Saf Python, 0 jeton."""
import hashlib
import json
import math
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home() / ".claude"
KART_TAVAN = 420  # ≈140 jeton (Türkçede ~3 karakter/jeton)
PARCA = 1500
KURULU = {"CC", "kurulu", "ikisi", "repo", "claude.ai"}
DUR_SATIR = re.compile(r"^\S+ DUR (\S+)")


def varsayilan():
    k = KOK / ".kos/kopru"
    return {"kok": KOK, "yetenek": KOK / "docs/katalog/yetenek.jsonl", "kart": KOK / "docs/arac-kart/kart.jsonl",
            "kombin": KOK / "docs/arac-kart/kombin.json", "db": KOK / ".kos/arac-kart/bolum.db", "sira": k / "ajan-sira",
            "log": k / "ajan-sira.log", "atlas": KOK / "docs/atlas/kart.jsonl", "ogrenim": KOK / "docs/katalog/ogrenim.jsonl",
            "olay": k / "beyin-olay.jsonl",
            "koklar": [EV / "skills", EV / "plugins/cache", EV / "agents", KOK / "skills", KOK / "agents"]}


def _cfg(c):
    b = {**varsayilan(), **(c or {})}
    if c and "kok" in c and "koklar" not in c:  # sahte kök (test): yalnız onu tara
        b["koklar"] = [c["kok"]]
    return b


def _jsonl(yol):
    if not yol or not Path(yol).exists():
        return []
    s = []
    for satir in Path(yol).read_text(encoding="utf8", errors="ignore").splitlines():
        try:
            s.append(json.loads(satir))
        except ValueError:
            pass
    return s


def temiz(s, n):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def frontmatter(md):
    m = re.match(r"---\s*\n(.*?)\n---\s*\n?", md, re.S)
    if not m:
        return {}, md
    d = {}
    for a in re.finditer(r"^(\w[\w-]*):\s*(.*?)(?=^\w[\w-]*:|\Z)", m.group(1), re.S | re.M):
        d[a.group(1)] = " ".join(a.group(2).strip().strip("\"'>|").split())
    return d, md[m.end():]


def bolumle(md):
    """Başlık bazlı parçalar [(başlık, metin)]; frontmatter 'açıklama' parçası; uzun parça PARCA'ya bölünür."""
    fm, govde = frontmatter(md)
    ps = [("açıklama", " ".join(f"{k}: {v}" for k, v in fm.items()))] if fm else []
    bas, tut = "giriş", []
    for satir in govde.splitlines():
        if re.match(r"#{1,3} \S", satir):
            if "".join(tut).strip():
                ps.append((bas, "\n".join(tut).strip()))
            bas, tut = satir.lstrip("# ").strip(), []
        else:
            tut.append(satir)
    if "".join(tut).strip() or not ps:
        ps.append((bas, "\n".join(tut).strip()))
    son = []
    for b, m in ps:
        for i in range(0, max(len(m), 1), PARCA):
            son.append((b if i == 0 else f"{b} ({i // PARCA + 1})", m[i:i + PARCA]))
    return son


def kaynak_hash(yol):
    return hashlib.sha256(Path(yol).read_bytes()).hexdigest()[:12]


def kaynaklari_tara(koklar):
    """ad(küçük harf) → SKILL.md / ajan .md yolu. Plugin cache dahil; ilk bulunan kazanır."""
    h = {}
    for kok in koklar:
        for d, dizinler, dosyalar in os.walk(kok):
            dizinler[:] = [x for x in dizinler if x not in (".git", "node_modules", "__pycache__")]
            for f in dosyalar:
                yol = Path(d) / f
                if f == "SKILL.md":
                    ad = yol.parent.name
                elif f.endswith(".md") and Path(d).name == "agents":
                    ad = yol.stem
                else:
                    continue
                h.setdefault(ad.lower(), yol)
    return h


def gecmis_hesapla(sira, log, esik_t=0):
    """Canlı geçmiş: iş başına KABUL (success ∧ hata yok ∧ DUR yok), maliyet, araç kullanımı (zorunlu − denetim.eksik); araç ve çift sayaçları."""
    dur = set()
    if log and Path(log).exists():
        for s in Path(log).read_text(encoding="utf8", errors="ignore").splitlines():
            if m := DUR_SATIR.match(s):
                dur.add(m.group(1))
    arac = defaultdict(lambda: {"n": 0, "kabul": 0, "usd": 0.0, "son": 0})
    partner, tarif, isler = defaultdict(Counter), defaultdict(Counter), []
    for f in sorted(Path(sira).glob("*.json")):
        if f.name.count(".") != 1 or f.stat().st_mtime < esik_t:
            continue
        ad = f.stem
        try:
            j = json.loads(f.read_text(encoding="utf8"))
            z = json.loads((Path(sira) / f"{ad}.zorunlu.json").read_text(encoding="utf8"))
            dn = json.loads((Path(sira) / f"{ad}.denetim.json").read_text(encoding="utf8"))
        except (OSError, ValueError):
            continue
        if not isinstance(j, dict) or not isinstance(z, dict) or not isinstance(dn, dict):
            continue
        kabul = j.get("subtype") == "success" and not j.get("is_error") and ad not in dur
        usd = float(j.get("total_cost_usd") or 0)
        eksik = {e.lower() for e in dn.get("eksik") or []}
        kul = sorted({(a.get("ad") or "").lower() for a in z.get("araclar") or [] if isinstance(a, dict)} - eksik - {""})
        isler.append({"ad": ad, "t": f.stat().st_mtime, "kabul": kabul, "usd": usd, "tur": z.get("tur"), "kapi": dn.get("durum"), "arac": kul})
        for a in kul:
            s = arac[a]
            s["n"] += 1
            s["kabul"] += kabul
            s["usd"] += usd
            s["son"] = max(s["son"], f.stat().st_mtime)
        if kabul:
            for a in kul:
                tarif[z.get("tur") or "diğer"][a] += 1
                for b in kul:
                    if a != b:
                        partner[a][b] += 1
    return {"isler": isler, "arac": dict(arac), "partner": partner, "tarif": tarif}


def _birlikte(ad, g, k=2):
    n = g["arac"]
    p = g["partner"].get(ad.lower(), {})
    sk = sorted(p, key=lambda b: (-p[b] / math.sqrt(n[ad.lower()]["n"] * n[b]["n"]), b))  # kosinüs: her işte gelen çekirdek araç öne geçmesin
    return sk[:k]


def dersler(ogrenim, olay, adlar):
    """araç adı → ≤2 kısa ders ('araclar' alanı ya da metinde geçen ad; kısa/genel adlar yalnız 'araclar' alanından)."""
    d = defaultdict(list)
    uygun = {a.lower() for a in adlar if len(a) >= 7 and re.search(r"[-:_]", a)}  # serbest metinde yalnız özgül (tireli) adlar; genel ad ("codex") gürültü getirir
    for o in _jsonl(ogrenim):
        isim = {x.strip().lower() for x in re.split(r"[,;]", str(o.get("araclar") or "")) if x.strip()}
        for a in isim & {x.lower() for x in adlar}:
            d[a].append(temiz(o.get("ne"), 110))
    for o in _jsonl(olay):
        if o.get("tur") in ("ders", "hata") and o.get("ozet") and o.get("tur") == "ders":
            for a in set(re.findall(r"[\w:-]+", str(o["ozet"]).lower())) & uygun:
                d[a].append(temiz(o["ozet"], 110))
    return {a: list(dict.fromkeys(v))[:2] for a, v in d.items()}


def _surum(yol, imza):
    m = re.search(r"[\\/](\d+\.\d+\.\d+)[\\/]", str(yol or ""))
    return m.group(1) if m else (imza or "-")


def _surum_etiket(v):
    v = str(v or "-")
    return ("v" if re.match(r"\d+\.\d+", v) else "#") + temiz(v, 8)  # sürüm yoksa kaynak/imza özeti '#' ile


def kart_metni(k):
    """Kasadaki ≤150 jeton kart satırı: öncelik sırasıyla sığan alanlar (kesik alan değil, sığmayan alan düşer)."""
    g = k.get("gecmis") or {}
    parcalar = [
        (f"{temiz(k['ad'], 40)} ({k['tur']})", True), (temiz(k.get("ne"), 95), True),
        ("ne zaman: " + temiz(k.get("ne_zaman"), 50), k.get("ne_zaman")), ("çağrı: " + temiz(k.get("cagri"), 45), k.get("cagri")),
        ("DEĞİL: " + temiz(k.get("degil"), 40), k.get("degil") not in (None, "", "-")),
        ("+" + ",".join(temiz(x, 16) for x in k.get("birlikte") or []), k.get("birlikte")),
        (f"geçmiş {g.get('kabul', 0)}/{g.get('n', 0)} ${(g.get('usd', 0) / g['n']) if g.get('n') else 0:.2f}/iş", g.get("n")),
        ("ders: " + temiz("; ".join(k.get("ders") or []), 55), k.get("ders")),
        ("≈" + ",".join(temiz(x, 16) for x in (k.get("esdeger") or [])[:2]), k.get("esdeger")),
        ("gç: " + temiz(k.get("gc"), 24), k.get("gc")), (temiz(k.get("maliyet"), 18), k.get("maliyet")),
        (f"{temiz(k.get('guven'), 18)} {_surum_etiket(k.get('surum'))}", k.get("guven")),
    ]
    s = ""
    for t, ok in parcalar:
        if ok and len(s) + len(t) + 3 <= KART_TAVAN:
            s += (" · " if s else "") + t
    return s


GC = {"skill": "görev bağlamı → talimat", "ajan": "istem → özet", "mcp": "araç şeması → JSON", "cli": "argüman → stdout",
      "arac": "betik argümanı → dosya/stdout", "plugin": "komut/skill demeti", "kutuphane": "import → API"}


def _degil(desc):
    m = re.search(r"((?:do not|don't|not for|never|NOT)\b[^.]{5,120})", desc or "", re.I)
    return temiz(m.group(1), 80) if m else "-"


def uret(satir, atlas, yol, gec, ders, aileler):
    ad, tur = satir["ad"], satir["tur"]
    ad0 = satir.get("ad0", ad)  # çakışan adlarda kart adı "ad [tür]"; geçmiş/atlas/ders ham adla aranır
    at = atlas.get(ad0) or atlas.get(ad0.split(":")[-1]) or {}
    p = yol if yol and Path(yol).exists() else None
    fm, md = (frontmatter(Path(p).read_text(encoding="utf8", errors="ignore")) if p else ({}, ""))
    desc = fm.get("description") or at.get("ne") or satir.get("is") or satir.get("metin") or ""
    bs = [b for b, _ in bolumle(Path(p).read_text(encoding="utf8", errors="ignore"))] if p else []
    nz = at.get("ne_zaman") if at.get("ne_zaman") not in (None, "", "bilinmiyor") else " · ".join(x for x in (satir.get("alan"), satir.get("asama")) if x)
    cak = at.get("cakisma") or ""
    if cak in ("yok", "bilinmiyor"):
        cak = ""
    if "Sınır:" in nz:  # atlas ne_zaman'ı "…Sınır: …" taşıyorsa ikinci yarı 'ne zaman DEĞİL'dir
        nz, sinir = nz.split("Sınır:", 1)
    else:
        sinir = ""
    eş = [a for a in aileler.get(ad0.split(":")[-1].lower(), []) if a != ad][:4]
    ga = gec["arac"].get(ad0.lower()) or {}
    return {
        "ad": ad, "tur": tur, "ne": temiz(desc, 140) if desc.strip() else f"{tur}: açıklama yok (kaynak: {satir.get('kaynak')})", "ne_zaman": temiz(nz, 80), "degil": temiz(sinir, 80) if sinir.strip() else _degil(desc),
        "gc": GC.get(tur, "-"), "cagri": temiz(satir.get("cagri"), 80), "birlikte": _birlikte(ad0, gec) if ad0.lower() in gec["arac"] else [],
        "esdeger": eş or ([x.strip() for x in cak.split(",")][:3] if cak and "\\" not in cak and "/" not in cak else []),
        "maliyet": (at.get("token") if at.get("token") not in (None, "bilinmiyor") else (f"~{len(md) // 4} jeton metin" if p else "süreç/ağ")),
        "guven": f"{satir.get('karar') or '-'}/{(satir.get('durum') or '-').split()[0]}", "surum": _surum(p, satir.get("imza")),
        "hash": kaynak_hash(p) if p else hashlib.sha256(f"{satir.get('metin')}{satir.get('cagri')}{satir.get('imza')}".encode()).hexdigest()[:12],
        "yol": str(p) if p else "", "tetik": satir.get("tetik") or "", "ba":temiz(" | ".join(bs[:12]), 160),
        "gecmis": {"n": ga.get("n", 0), "kabul": ga.get("kabul", 0), "usd": round(ga.get("usd", 0), 3)} if ga else {},
        "ders": ders.get(ad0.lower(), []), "etiket": "",  # etiket: tools/etiket_uret.py doldurur
    }


ONCELIK = ("skill", "ajan", "mcp", "cli", "arac", "plugin", "kutuphane")


def kurulu_satirlar(c):
    """Kurulu (motion-prompt/aday hariç) araçlar; farklı türde aynı ad → öncelikli tür sade ad, diğeri "ad [tür]" (kart kimliği tekil)."""
    gor, s = set(), []
    for o in _jsonl(c["yetenek"]):
        if o.get("tur") == "motion-prompt" or (o.get("durum") or "x").split()[0] not in KURULU or (o["tur"], o["ad"]) in gor:
            continue
        gor.add((o["tur"], o["ad"]))
        s.append(o)
    s.sort(key=lambda o: ONCELIK.index(o["tur"]) if o["tur"] in ONCELIK else 9)
    adlar = set()
    for o in s:
        o["ad0"] = o["ad"]
        if o["ad"] in adlar:
            o["ad"] = f"{o['ad']} [{o['tur']}]"
        adlar.add(o["ad"])
    return s


def _yol_bul(satir, atlas, taranan):
    ad0 = satir.get("ad0", satir["ad"])
    at = atlas.get(ad0) or atlas.get(ad0.split(":")[-1]) or {}
    kanit = re.sub(r":\d+(-\d+)?$", "", str(at.get("kanit") or ""))
    if kanit and Path(kanit).is_file() and kanit.lower().endswith(".md"):
        return Path(kanit)
    if satir["tur"] in ("skill", "ajan"):
        return taranan.get(ad0.split(":")[-1].lower())
    return None


def _db(yol):
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    b = sqlite3.connect(yol)
    b.execute("CREATE VIRTUAL TABLE IF NOT EXISTS b USING fts5(ad UNINDEXED, baslik, metin, tokenize='unicode61 remove_diacritics 2')")
    return b


def _bolum_yaz(b, k, satir):
    b.execute("DELETE FROM b WHERE ad = ?", (k["ad"],))
    if k["yol"]:
        ps = bolumle(Path(k["yol"]).read_text(encoding="utf8", errors="ignore"))
    else:
        ps = [("özet", f"{k['ne']} {satir.get('metin') or ''} {satir.get('cagri') or ''}")]
    b.executemany("INSERT INTO b(ad, baslik, metin) VALUES (?,?,?)", [(k["ad"], x, y) for x, y in ps])


def _kartlar(c):
    return {k["ad"]: k for k in _jsonl(c["kart"])}


def bayat(c):
    c = _cfg(c)
    atlas = {o["ad"]: o for o in _jsonl(c["atlas"]) if o.get("ad")}
    taranan = kaynaklari_tara(c["koklar"])
    var, b = _kartlar(c), []
    for s in kurulu_satirlar(c):
        k = var.get(s["ad"])
        yol = _yol_bul(s, atlas, taranan)
        if not k or (yol and k["hash"] != kaynak_hash(yol)) or (not yol and k["yol"]):
            b.append(s["ad"])
    return b


def yenile(c=None, yalniz=None):
    """Artımlı: yalnız bayat/kartsız (ya da `yalniz` verilen) araçlar yeniden üretilir; geçmiş/birlikte/ders her çağrıda tazelenir (ucuz)."""
    c = _cfg(c)
    atlas = {o["ad"]: o for o in _jsonl(c["atlas"]) if o.get("ad")}
    taranan = kaynaklari_tara(c["koklar"])
    satirlar = kurulu_satirlar(c)
    gec = gecmis_hesapla(c["sira"], c.get("log"))
    ders = dersler(c.get("ogrenim"), c.get("olay"), [s["ad"] for s in satirlar])
    aileler = defaultdict(list)
    for s in satirlar:
        aileler[s["ad0"].split(":")[-1].lower()].append(s["ad"])
    var, b, yeni, say = _kartlar(c), _db(c["db"]), [], Counter()
    for s in satirlar:
        yol = _yol_bul(s, atlas, taranan)
        k0 = var.get(s["ad"])
        degisti = not k0 or (yol and k0["hash"] != kaynak_hash(yol)) or (not yol and k0["yol"]) or (yalniz and s["ad"] in yalniz)
        if not degisti and yalniz is not None and s["ad"] not in yalniz:
            yeni.append(k0)
            continue
        k = uret(s, atlas, yol, gec, ders, aileler)
        k["etiket"] = (k0 or {}).get("etiket", "")  # yenilemede korunur
        if degisti or not k0:
            _bolum_yaz(b, k, s)
            say["yenilendi"] += 1
        yeni.append(k)
    b.commit()
    b.close()
    Path(c["kart"]).parent.mkdir(parents=True, exist_ok=True)
    Path(c["kart"]).write_text("\n".join(json.dumps(k, ensure_ascii=False) for k in yeni) + "\n", encoding="utf8")
    if c.get("kombin"):
        Path(c["kombin"]).write_text(json.dumps({t: [a for a, _ in sa.most_common(8)] for t, sa in gec["tarif"].items()}, ensure_ascii=False, indent=0), encoding="utf8")
    return {"kart": len(yeni), **say, "is": len(gec["isler"])}


def ozet(c=None):
    c = _cfg(c)
    ks = list(_kartlar(c).values())
    uz = [len(kart_metni(k)) for k in ks]
    alan = {f: sum(1 for k in ks if k.get(f) not in (None, "", "-", [], {})) for f in ("ne", "ne_zaman", "degil", "cagri", "birlikte", "esdeger", "maliyet", "guven", "surum", "gecmis", "ders", "yol")}
    return {"kart": len(ks), "kurulu": len(kurulu_satirlar(c)), "kart_max_karakter": max(uz or [0]), "alan_dolu": alan}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:] or ["ozet"]
    if a[0] == "yenile":
        ek = a[a.index("--ekle") + 1:] if "--ekle" in a else None
        print(json.dumps(yenile(yalniz=ek), ensure_ascii=False))
    elif a[0] == "bayat":
        b = bayat(None)
        print(len(b), b[:20])
    else:
        print(json.dumps(ozet(), ensure_ascii=False, indent=1))
