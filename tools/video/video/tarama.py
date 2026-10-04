"""12b video-tarama: kayıt, eski rapor içe alma, ad sözlüğü, tekilleme, işaret, rapor denetimi."""
import json
import os
import re
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path

from jev import skill as sk

from . import metin as m

ESIK = 0.8
YERLESIK = ("Claude Code", "Claude Desktop", "claude.ai")
DIS = {"skill", "plugin", "mcp", "yerlesik"}  # kurulu ya da platformda var → ÇİFT
BOLUM = ("Künye", "Özet", "Bölümler", "Adaylar", "İddialar", "Kareden okunanlar", "Belirsizlikler", "Atlanan")
IDDIA_TUR = {"sayısal", "özellik", "karşılaştırma", "öneri"}
TUR = {"skill", "plugin", "MCP", "CLI", "teknik", "iş akışı", "ipucu", "prompt"}
ALINTI_KELIME = 15
DOSYA = re.compile(r"(?:(\d{4}-\d\d-\d\d)-)?([\w-]{11})")
ZAMAN = re.compile(r"(?<![\d:.])(?:\d{1,2}:)?\d{1,2}:\d{2}(?![\d:])")
ALINTI = re.compile(r"[“\"]([^”\"\n]*)[”\"]")
MADDE = re.compile(r"^- (.+?) → (\S+)")
SITE_UI = "Site/UI teknikleri"  # 23 K5: frontend/site içerikli videoda zorunlu
FRONTEND = re.compile(r"\b(landing|web ?sitesi|website|frontend|css|tailwind|gsap|three\.?js|webgl|animasyon\w*|scroll\w*|kaydırma\w*|"
                      r"tipografi\w*|arayüz\w*|ui|figma|framer|hero|react|next\.js|lenis|grid)\b", re.I)


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


TR_ASCII = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")


def slug(ad):  # 24e-1 K1: dosya adı ASCII; Türkçe harf kabukta bozulmaz
    return re.sub(r"\W+", "-", ad.translate(TR_ASCII).casefold()).strip("-")


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


ICERIK = ("site/UI yapımı", "prompt/şablon paylaşımı", "token/verimlilik", "araç/skill tanıtımı", "iş akışı", "diğer")
KANIT = re.compile(r"lisans|ücret|login|ölç|zaten", re.I)  # 17 K4: RED gerekçesi kanıta bağlı mı (not metninde)
MADDE_ESKI = re.compile(r"^- (.+?) → (ZATEN VAR|[A-ZÇĞİÖŞÜ]{3,})\b\s*(.*)$")
# 1b: yalnız bilinen etiketler; `→ CLAUDE.md` / `→ DESIGN.md` / `→ API anahtarları` hedef dosya ya da adımdır, etiket değil
ETIKET_ESKI = {"ZATEN VAR", "ELE", "ELENDİ", "ADAY", "BİLGİ", "INFO", "KUR", "TETİKLEYİCİ", "ÇİFT", "DENE", "RED", "ÖĞREN", "UYARLA", "KURAL"}


def eski_kalemler(metin):
    """VİDEO-YENİDEN-1: eski rapor → [(ad, durum, etiket, not)]: `ad` başlıklı tablolar + `- ad → ETİKET (not)` maddeleri."""
    out = []
    for bas, satirlar in tablolar(metin):
        if bas[0].casefold() == "ad":
            out += [(h[0], (g := dict(zip(bas, h))).get("durum", ""), g.get("etiket", ""), g.get("not", "")) for h in satirlar if h[0]]
    for s in metin.splitlines():
        if (x := MADDE_ESKI.match(s)) and x[2] in ETIKET_ESKI:
            out.append((x[1].strip(), "", x[2], x[3].strip(" ()")))
    return out


def sahte_kalemler(metin):
    """1b: VİDEO-YENİDEN-1'in aday sandığı maddeler (bilinmeyen büyük harf etiket); silinmez, `sahte` işaretlenir."""
    return [x[1].strip() for s in metin.splitlines() if (x := MADDE_ESKI.match(s)) and x[2] not in ETIKET_ESKI]


def envanter_sozluk(envanter):
    """1b K1: departman envanteri (plugin · skill · MCP · CLI; `p:ad` önekli ve claude.ai senkron adlar dahil) → [(ad, "envanter:<tür>")]."""
    return [(e["ad"], f"envanter:{e['tur']}") for e in envanter]


def arac_esle(ad, envanter, sozluk):
    """1b K1: önce tam envanter, yoksa sözlük (yalnız DIS kaynak). Ad ` / ` ve virgülle parçalanır: `impeccable / front end ...`.
    Parça yalnız boşluksuz ad/takma addır (≥3 karakter); parantez içi açıklama (`Fable (Claude model…)`) eşleşmeye girmez."""
    ic, dis = re.findall(r"\(([^()]*)\)", ad), re.sub(r"\([^()]*\)", " ", ad)
    parca = [ad] + [p for p in (x.strip() for x in re.split(r"\s/\s|,", dis) + ic) if p and " " not in p and len(normal(p)) >= 3]
    for s in (envanter, [x for x in sozluk if x[1] in DIS]):
        if es := max((e for p in parca if (e := eslestir(p.strip(), s))), key=lambda e: e[2], default=None):
            return es
    return None


def yeni_karar(x):
    """Eski kalem → bugünkü karar (eleme yok). x: ad·durum·etiket·not·tur(araç|teknik|prompt|ipucu)·kural·es·ko·token·departman."""
    if x.get("kural") or x.get("es"):
        return "ZATEN VAR", f"eşleşme: {x.get('kural') or x['es'][0]}"
    if x["tur"] == "araç":
        if x["etiket"].upper().startswith("ELE"):
            if x.get("token") and not KANIT.search(x.get("not", "")):
                return "DENE", "K4: token etiketli, kanıtsız RED → DENE"
            return "RED", f"eski: {x.get('not') or x['etiket']}"
        return "DENE", f"eski {x['etiket'] or '?'}: araştırıcı gerekir"
    if x.get("ko") == "kural":
        return "KURAL", "davranış kuralı → bekleyen (ONAY)"
    if x.get("departman") == "frontend":
        return "UYARLA", "frontend teknik/prompt → web-sahne-desenleri / frontend-promptlar"
    return "ÖĞREN", "olgu → bilgi kartı adayı"


def celiski_mi(x):
    """Eski rapor ZATEN VAR/ÇİFT dedi, bugün hiçbir kaynakta eşleşme yok."""
    return x["durum"].startswith(("ZATEN VAR", "ÇİFT")) and not (x.get("kural") or x.get("es"))


def puan(v):
    """K3 yeniden izleme puanı: site/UI ×3 · prompt/şablon ×3 · DENE+UYARLA ×2 · token aday ×2 · kare zayıf ×1."""
    return 3 * (v["tur"] in ICERIK[:2]) + 2 * sum(k in ("DENE", "UYARLA") for k in v["kararlar"]) + 2 * v["token"] + int(v["kare_zayif"])


def rapor_id(yol):
    x = DOSYA.fullmatch(Path(yol).stem)
    # ponytail: "00-envanter" 11 krk'lık id biçiminde; iki rakam-tire-küçük harf kalıbı id sayılmaz
    if not x or re.fullmatch(r"\d\d-[a-z]+", Path(yol).stem):
        return None, None
    return x[2], x[1]


GH = re.compile(r"https?://(?:www\.)?github\.com/([\w.-]+)/([\w.-]+?)(?:\.git)?(?:/(?:tree|blob)/[^/\s]+/([^\s?#]*?))?/?(?:[?#]\S*)?$")
PAKET = re.compile(r"https?://(?:www\.)?(?:npmjs\.com/package|pypi\.org/project)/([@\w.-]+(?:/[\w.-]+)?)/?$")
SOSYAL = ("youtube.com", "youtu.be", "twitter.com", "x.com", "instagram.com", "linkedin.com", "discord.gg", "discord.com", "tiktok.com",
          "facebook.com", "patreon.com")


def kaynak_ayristir(url):
    """24e-2 K2: videosuz kaynak → {repo, alt, ad, id}; GitHub `tree|blob/<dal>/<alt yol>` alt klasörü korunur, web sayfası repo'suz."""
    from urllib.parse import urlparse
    g = GH.match(url.strip())
    if g:
        alt = (g[3] or "").strip("/")
        ad = slug((alt or g[2]).split("/")[-1])
        return {"repo": f"{g[1]}/{g[2]}", "alt": alt, "ad": ad, "id": f"kaynak-{ad}"}
    p = urlparse(url.strip())
    ad = slug(p.path.strip("/").split("/")[-1] or p.netloc)
    return {"repo": None, "alt": "", "ad": ad, "id": f"kaynak-{ad}"}


def aciklama_adaylari(metin, v):
    """24e-2 K1: `## Açıklama bağlantıları` → GitHub/paket bağlantısı aday (tür araç, repo dolu; kurulu kontrolü toplu sözlük eşleşmesinde),
    diğer site bağlantısı Site/UI referansı; sosyal ağ ve GitHub sponsors atlanır."""
    from urllib.parse import urlparse
    ad, ref = [], []
    for u in dict.fromkeys(re.findall(r"https?://[^\s|)>\]]+", bolum(metin, "Açıklama bağlantıları"))):
        g, p, h = GH.match(u), PAKET.match(u), urlparse(u).netloc.casefold().removeprefix("www.")
        if g and g[1] not in ("sponsors", "orgs"):
            ad.append({"ad": g[2], "video": v, "tur": "araç", "ne": u, "repo": f"{g[1]}/{g[2]}"})
        elif p:
            ad.append({"ad": p[1].split("/")[-1], "video": v, "tur": "araç", "ne": u, "repo": u})
        elif not g and not any(h == s or h.endswith("." + s) for s in SOSYAL):
            ref.append(u)
    return ad, ref


def rapor_videolari(metin, v):
    """24e-2 K3: karşılaştırmalı short raporu `videolar: a, b` → her id ayrı kayıt satırı."""
    x = re.search(r"(?m)^videolar:\s*(.+)$", metin)
    return list(dict.fromkeys([v, *re.findall(r"(?<![\w-])[A-Za-z0-9_-]{11}(?![\w-])", x[1] if x else "")]))


def _hucre(s):
    return [x.strip() for x in s.strip().strip("|").split("|")]


def kuyruk_parti(metin):
    """24e-2 K6: bekleyen video satırları sıra 1'den; ilk satırın türü partiyi belirler (short <2 dk ≤8 · uzun ≤3),
    notunda anılan ya da onu anan aynı türden bekleyen önce gelir. → (tür, [hücreler])"""
    sira, bek = 9, []
    for s in metin.splitlines():
        if x := re.match(r"###\s+Sıra\s+(\d+)", s):
            sira = int(x[1])
        h = _hucre(s)
        if s.lstrip().startswith("|") and len(h) == 5 and h[4] == "bekliyor" and re.fullmatch(r"\d+(?:\.\d+)?", h[1]):
            bek.append((sira, len(bek), h))
    bek = [h for *_, h in sorted(bek)]
    if not bek:
        return None, []
    kisa = float(bek[0][1]) < 2
    ayni = [h for h in bek if (float(h[1]) < 2) == kisa]
    bag = [h for h in ayni[1:] if h[0] in ayni[0][3] or ayni[0][0] in h[3]]
    parti = list({h[0]: h for h in [ayni[0], *bag, *ayni]}.values())
    return ("short", parti[:8]) if kisa else ("uzun", parti[:3])


def kuyruk_isle(metin, ids, sha):
    """24e-2 K6: id'si `ids`'te olan tablo satırının yalnız son (durum) hücresi `işlendi: <sha>` olur; satır sonu ve diğer baytlar aynı."""
    out = []
    for s in metin.splitlines(keepends=True):
        g = s.rstrip("\r\n")
        if g.lstrip().startswith("|") and _hucre(g)[0] in ids:
            i = g.rstrip().rstrip("|").rfind("|")
            s = f"{g[:i + 1]} işlendi: {sha} |{s[len(g):]}"
        out.append(s)
    return "".join(out)


def kuyruk_ekle(metin, satirlar, raporlu, muaf, baslik, gunluk=None):
    """KANAL-2b C4: (id, süre, başlık, not) satırları `baslik` altında `bekliyor` eklenir; kuyrukta bekleyen ya da
    tarihli raporu olan id atlanır, `muaf` yalnız rapor atlamasından kurtulur. Satır sonu dosyanınki. → (metin, {id: sebep})
    E1: 5. öğe metadata hata metniyse nota `meta hatası: …` eklenir ve `gunluk`a `id<TAB>hata` satırı yazılır."""
    nl = "\r\n" if "\r\n" in metin else "\n"
    bek = {_hucre(s)[0] for s in metin.splitlines() if s.lstrip().startswith("|") and _hucre(s)[-1] == "bekliyor"}
    atla, out = {}, []
    for v, sure, bas, n, *h in satirlar:
        if v in bek:
            atla[v] = "kuyrukta bekliyor"
        elif v in raporlu and v not in muaf:
            atla[v] = "tarihli rapor"
        else:
            bek.add(v)
            if h and h[0]:
                n = f"{n} · meta hatası: {h[0].replace('|', '/')}"
                if gunluk:
                    Path(gunluk).parent.mkdir(parents=True, exist_ok=True)
                    with open(gunluk, "a", encoding="utf-8") as f:
                        f.write(f"{v}\t{h[0]}\n")
            out.append(f"| {v} | {sure} | {bas} | {n} | bekliyor |")
    if not out:
        return metin, atla
    bas = [baslik, "", "| id | süre | başlık (kısa) | not | durum |", "|---|---|---|---|---|"]
    return metin + ("" if metin.endswith(nl) else nl) + nl + nl.join(bas + out) + nl, atla


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


def kayit_ekle(yol, girdiler):
    """23c K5: append-only; eski satırın baytı değişmez (sonda satır sonu yoksa önce o eklenir)."""
    yol = Path(yol)
    yol.parent.mkdir(parents=True, exist_ok=True)
    bas = "\n" if yol.is_file() and (b := yol.read_bytes()) and not b.endswith(b"\n") else ""
    with yol.open("a", encoding="utf-8", newline="\n") as f:
        f.write(bas + "".join(json.dumps(g, ensure_ascii=False) + "\n" for g in girdiler))


def bos_yol(y):
    """24b K3: günlük çıktı ezilmez — y varsa y-2, y-3 … ilk boş ad."""
    y, n = Path(y), 2
    x = y
    while x.exists():
        x, n = y.with_name(f"{y.stem}-{n}{y.suffix}"), n + 1
    return x


def kayit_son(kayit, anahtar="ad"):
    """Append-only okuma: anahtar başına satırlar sırayla birleşir (sonraki alan öncekini ezer)."""
    son = {}
    for k in kayit:
        son[k[anahtar]] = {**son.get(k[anahtar], {}), **k}
    return son


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
    t = tablolar(bolum(metin, "İddialar"))
    for s in t[0][1] if t else []:  # 17 K1: videodaki her somut iddia ayrı satır
        if len(s) != 3 or any(x in ("", "-") for x in s):
            h.append(f"boş alan: iddia satırı {s[0] or '?'} (3 alan dolu olmalı: iddia·zaman·tür)")
        elif s[2] not in IDDIA_TUR:
            h.append(f"iddia türü geçersiz: {s[0]} → {s[2]} ({', '.join(sorted(IDDIA_TUR))})")
    t = tablolar(bolum(metin, "İz"))
    if (sm := re.search(r"şema (\d+)", bolum(metin, "Künye"))) and int(sm[1]) >= 2 and not (t and t[0][1]):  # D1 (a): eski şema serbest
        h.append(f"bölüm eksik: ## İz (şema {sm[1]}: her bahis bir satır)")
    for s in t[0][1] if t else []:  # D1: her bahis bir satır; "zaten kurulu" sebep değil (29 Eyl: kurulu araç da aday)
        if len(s) != 4 or any(x in ("", "-") for x in s[:3]):
            h.append(f"İz boş alan: {s[1] if len(s) > 1 else '?'} (4 alan: kaynak·ne·bağlandığı·kanıt)")
        elif s[2].casefold().startswith("aday değil") and not IZ_SEBEP.fullmatch(s[2].split(":", 1)[-1].strip()):
            h.append(f"İz sebebi geçersiz: {s[1]} → {s[2]} (genel kavram · başka adayın parçası (hangisi) · sponsor/reklam · konu dışı)")
    h += [f"alıntı {len(a.split())} kelime > {ALINTI_KELIME}: {a[:40]}…" for a in ALINTI.findall(metin) if len(a.split()) > ALINTI_KELIME]
    return h + site_ui_denetle(metin)


IZ_SEBEP = re.compile(r"genel kavram|başka adayın parçası \(\S[^)]*\)|sponsor/reklam|konu dışı", re.I)
KACAN_URL = re.compile(r"https?://[^\s|)>\]]+")
KACAN_DESEN = [re.compile(r"(?<![\w./:-])[A-Za-z0-9][\w.-]*/[\w.-]*\w(?![\w/])"),  # owner/repo
               re.compile(r"\b(?:npx|uvx|pipx? install|npm i(?:nstall)?(?: -g)?|claude mcp add|/plugin install)\s+(?:-\S+\s+)*([\w@./-]+)"),
               re.compile(r"\b[A-Z][a-z]+[A-Z][A-Za-z]*\b")]  # büyük harfli ürün adı (OpenAI, ChatGPT)


def _kat_ad(s):
    """D2: OCR karışıklığı katlanır (1→i, 0→o), harf/rakam dışı atılır: OpenA1 · Open A I · openai aynı."""
    return re.sub(r"[\W_]", "", s.casefold().translate(str.maketrans("10", "io")))


ARAC_ISARET = {"skill", "skills", "plugin", "mcp", "cli", "extension", "agent", "server"}


def _ayirt(ad):
    """D2 (i): tire/rakam/nokta/iç büyük harf ya da ≥5 harf ve YAYGIN değil."""
    return bool(re.search(r"[-.\d]|[a-z][A-Z]", ad)) or (len(re.sub(r"[\W\d_]", "", ad)) >= 5 and ad.casefold() not in YAYGIN)


def _baglam(satir, s, e, once, sonra):
    """D2 (ii): komşu sözcük araç işareti · "/ad" ya da "ad/" (owner/repo) · kurulum komutu içinde."""
    return ((once or "").casefold() in ARAC_ISARET or (sonra or "").casefold() in ARAC_ISARET or "/" in satir[s - 1:s] + satir[e:e + 1]
            or any(m.start() <= s < m.end() for m in KACAN_DESEN[1].finditer(satir)))


def kacan(rapor, kaynaklar, sozluk, desen=KACAN_DESEN, zayif=None):
    """D2 çağrısız kaçak denetimi: [(kaynak, metin)] içindeki URL · owner/repo · kurulum komutu · büyük harfli ürün adı ve sözlük adları
    (1–3 ardışık sözcük katlanmış eşit; kısa adlar dahil) ## İz'de geçmiyorsa → [(kaynak, terim)] "KAÇAN?".
    zayif listesi verilirse ayırt edici olmayan ve araç bağlamı olmayan sözlük eşleşmeleri oraya (düşük güven) gider."""
    iz, sozluk, gorulen, k, zt_hepsi = _kat_ad(bolum(rapor, "İz")), {_kat_ad(x): x for x in sozluk}, set(), [], []
    for kaynak, metin in kaynaklar:
        terim, zt = KACAN_URL.findall(metin), []
        duz = KACAN_URL.sub(" ", metin)
        for satir in duz.splitlines():
            m = list(re.finditer(r"[\w.-]+", satir))
            w = [x.group() for x in m]
            for n in (1, 2, 3):
                for i in range(len(w) - n + 1):
                    if (j := _kat_ad("".join(w[i:i + n]))) in sozluk:
                        ad = sozluk[j]
                        guclu = zayif is None or _ayirt(ad) or _baglam(satir, m[i].start(), m[i + n - 1].end(),
                                                                       w[i - 1] if i else None, w[i + n] if i + n < len(w) else None)
                        (terim if guclu else zt).append(ad)
            if zayif is not None:  # "ad-skill" / "ad-mcp" tireli biçim
                terim += [sozluk[j] for x in w if "-" in x and x.rsplit("-", 1)[1].casefold() in ARAC_ISARET
                          and (j := _kat_ad(x.rsplit("-", 1)[0])) in sozluk]
        terim += [x for d in desen for x in d.findall(duz)]
        for t in terim:
            if (j := _kat_ad(t)) and j not in gorulen and j not in iz:
                gorulen.add(j)
                k.append((kaynak, t))
        zt_hepsi += [(kaynak, t) for t in zt]
    for q, t in zt_hepsi:  # engelleyen olan ya da İz'deki ad düşük güvende tekrar sayılmaz
        if (j := _kat_ad(t)) not in gorulen and j not in iz:
            gorulen.add(j)
            zayif.append((q, t))
    return k


# ayar · D2 (b): düşük güven adayı sayılmayan yaygın büyük harfli kelimeler (casefold)
YAYGIN = set("i a an the this that these those it its we you he she they my our your and or but so if then now here there what why how "
             "when where who okay ok yes no hello hi hey thanks today also just bir bu şu o ve ama için ile çok daha şimdi evet hayır "
             "tamam merhaba yani peki sonra burada design data docs do review taste standup debug video careful confidence".split())
BILINEN = Path("docs") / "video-tarama" / "bilinen-araclar.txt"


def kacan_sozluk(kok):
    """D2 (a): kurulu araçlar (envanter.json) + aday dosya adları + docs/video-tarama/bilinen-araclar.txt."""
    kok, ev = Path(kok), Path(kok) / "docs" / "departmanlar" / "envanter.json"
    b = kok / BILINEN
    return ([e["ad"] for e in ((_json(ev) or []) if ev.is_file() else [])] + [p.stem for p in (kok / "docs" / "kurulumlar" / "adaylar").glob("*.md")]
            + ([x.strip() for x in b.read_text(encoding="utf-8").splitlines() if x.strip()] if b.is_file() else []))


def bilinen_ekle(kok, adlar):
    """D2 (a): parti kapanışında yeni aday adları bilinen-araclar.txt'ye eklenir; büyük/küçük harf farkı tekrar sayılır."""
    b = Path(kok) / BILINEN
    L = [x.strip() for x in b.read_text(encoding="utf-8").splitlines() if x.strip()] if b.is_file() else []
    for a in adlar:
        if a.casefold() not in {x.casefold() for x in L}:
            L.append(a)
    b.write_text("".join(f"{x}\n" for x in L), encoding="utf-8")


def kacan_dusuk(rapor, kaynaklar, sozluk):
    """D2 (b) "KAÇAN? (düşük güven)": cümle başında olmayan, YAYGIN'da ve sözlükte olmayan, kaynaklarda ≥2 kez geçen büyük harfli
    tek kelime İz'de yoksa → [(ilk kaynak, kelime)]. Parti kapat'ı durdurmaz."""
    iz, soz, say, ilk = _kat_ad(bolum(rapor, "İz")), {_kat_ad(x) for x in sozluk}, {}, {}
    for kaynak, metin in kaynaklar:
        for satir in KACAN_URL.sub(" ", metin).splitlines():
            satir = re.sub(r"^\s*\[?\d+:\d+(?::\d+)?\]?\s*·?\s*", "", satir)  # [mm:ss] / mm:ss · öneki cümle başıdır
            for b in re.finditer(r"(?<![\w-])[A-ZÇĞİÖŞÜ][\w-]+", satir):
                if not re.search(r"(^|[.!?:]\s*)$", satir[:b.start()]):
                    w = b.group()
                    say[w] = say.get(w, 0) + 1
                    ilk.setdefault(w, kaynak)
    # iç büyük harfli tek kelime (LangGraph, ChatGPT) tek geçişte de; ≥2 şartı yalnız düz Büyük-harfli kelimeye
    return [(ilk[w], w) for w, n in say.items() if (n >= 2 or re.search(r"[a-z][A-Z]", w)) and w.casefold() not in YAYGIN
            and (j := _kat_ad(w)) not in soz and j not in iz]


def kacan_video(rapor, paket, sozluk):
    """D2 kancalama: paket.md (Açıklama bağlantıları · Segmentler · Ekran metni) + yanındaki ocr-gurultu.txt → (engelleyen, düşük güven).
    Engelleyen = URL · owner/repo · kurulum komutu · sözlük; büyük harfli ürün adı yalnız düşük güvende."""
    p = Path(paket)
    md = p.read_text(encoding="utf-8") if p.is_file() else ""
    g = p.parent / "ocr-gurultu.txt"
    k = [("paket", "\n".join(bolum(md, b) for b in ("Açıklama bağlantıları", "Segmentler", "Ekran metni")))]
    k += [("gürültü", g.read_text(encoding="utf-8"))] if g.is_file() else []
    zayif = []
    eng = kacan(rapor, k, sozluk, KACAN_DESEN[:2], zayif)
    return eng, kacan_dusuk(rapor, k, sozluk) + zayif


def frontend_mu(metin):
    """Künye + Özet + Adaylar'da ≥2 farklı site/UI anahtar kelimesi."""
    return len({x.casefold() for x in FRONTEND.findall(" ".join(bolum(metin, b) for b in ("Künye", "Özet", "Adaylar")))}) >= 2


def uyarilar(metin):
    """M2f K1: başlığı olan ama EKSİK/boş Site/UI bölümü hata değil uyarı (tamam_eksik raporu)."""
    var = any(s[3:].strip().casefold().startswith(SITE_UI.casefold()) for s in metin.splitlines() if s.startswith("## "))
    t = tablolar(bolum(metin, SITE_UI)) if var else []
    return [f"uyarı: ## {SITE_UI} EKSİK ({(bolum(metin, SITE_UI).strip() or 'boş')[:120]})"] if var and not (t and t[0][1]) else []


def site_ui_denetle(metin):
    """23 K5: teknik · kanıt (m:ss) · kütüphane/araç (ekranda/kanıtta yoksa 'tahmin: …') · bizde."""
    if not frontend_mu(metin):
        return []
    t = tablolar(bolum(metin, SITE_UI))
    if not t or not t[0][1]:
        return [] if uyarilar(metin) else [f"bölüm eksik: ## {SITE_UI}"]
    h, oku = [], bolum(metin, "Kareden okunanlar").casefold()
    for s in t[0][1]:
        if len(s) != 4 or any(x in ("", "-") for x in (s[0], s[1], s[3])):
            h.append(f"boş alan: teknik satırı {s[0] or '?'} (teknik·kanıt·kütüphane/araç·bizde)")
        elif s[3] in ("altyazı", "kare", "açıklama"):  # M2e K1: motor biçimi (teknik·ne·zaman·kaynak); açıklama kaynaklı kalemde zaman beklenmez
            if s[3] != "açıklama" and not ZAMAN.search(s[2]):
                h.append(f"kanıt zamansız: {s[0]} (m:ss + kare yolu ya da altyazı)")
        elif not ZAMAN.search(s[1]):
            h.append(f"kanıt zamansız: {s[0]} (m:ss + kare yolu ya da altyazı)")
        elif s[2] not in ("", "-") and not s[2].casefold().startswith("tahmin") and s[2].casefold() not in oku + s[1].casefold():
            h.append(f"kütüphane kanıtsız: {s[0]} → {s[2]} (ekranda/açıklamada yoksa 'tahmin: …')")
    return h


# --- 12f: ipucu/iş akışı adaylar kural kaynaklarıyla karşılaştırılır ---

KURAL_TUR = {"ipucu", "iş akışı"}
KURAL_ASAMA1 = "Videodaki ipucu (state) aşağıdaki çalışma kurallarından hangisinde zaten var? Hiçbirinde yoksa 'hiçbiri'."
KURAL_ASAMA2 = "Videodaki ipucu (state) şu kuralda zaten var mı, aynı davranışı mı istiyor? Kural: {k}"
KAVRAM = {"model": ("sonnet", "haiku", "opus", "fable", "ucuz model", "model:"), "altajan": ("subagent", "sub-agent", "alt ajan", "alt-ajan"),
          "kural-dosyasi": ("claude.md", "bellek", "memory", "skill"), "kanit": ("kanıt", "doğrula", "verify"), "baglam": ("context", "bağlam", "token"),
          "soru": ("sormadan", "soru sor", "onay iste"), "kisa": ("kısa", "sade", "token-verimli"), "geri-bildirim": ("geri bildirim", "gerekçe", "feedback")}
DESTEK_ESIK = 0.4  # 23 K3: aşama 1 seçimiyle ≥2 ortak kavram varsa aşama 2 eşiği
KURAL_SATIR = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+(.+)")


def kural_kaynaklari(env, ev):
    """VIDEO_KURALLAR (os.pathsep ayrımlı) ya da ~/.claude/CLAUDE.md + repo dışındaki omer-kurallar.md.
    Not dokümanları ve bellek dosyaları kaynak değil: aşama 1'i gürültüyle dolduruyor, yanlış pozitif veriyor (12f canlı ölçüm)."""
    if env.get("VIDEO_KURALLAR"):
        return [Path(y) for y in env["VIDEO_KURALLAR"].split(os.pathsep) if y]
    return [Path(ev) / ".claude" / "CLAUDE.md", Path(__file__).resolve().parents[4] / "omer-kurallar.md"]


def kural_kisa(yol):
    return Path(yol).stem


def kural_parcala(yol):
    """[[dosya:satır, metin]]: madde satırları ve ≥20 karakterlik düz satırlar; başlık, tablo, alıntı, kod bloğu atlanır."""
    kisa, out, kod = kural_kisa(yol), [], False
    satir = yol.read_text(encoding="utf-8").splitlines()
    on = satir.index("---", 1) + 1 if satir[:1] == ["---"] and "---" in satir[1:] else 0  # frontmatter atlanır
    for i, s in enumerate(satir[on:], on + 1):
        if s.lstrip().startswith("```"):
            kod = not kod
            continue
        if kod or not s.strip() or s.lstrip().startswith(("#", "|", ">", "---")):
            continue
        x = KURAL_SATIR.match(s)
        metin = (x[1] if x else s).replace("**", "").strip()
        if x or len(metin) >= 20:
            out.append([f"{kisa}:{i}", metin[:300]])
    return out


def kurallar(yollar, onbellek):
    """[(kısaltma, metin)]; dosyanın mtime'ı önbellektekiyle aynıysa yeniden okunmaz, olmayan dosya atlanır."""
    try:
        eski = json.loads(Path(onbellek).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        eski = {}
    yeni, out = {}, []
    for y in yollar:
        try:
            mt = y.stat().st_mtime_ns
        except OSError:
            continue
        v = eski.get(str(y))
        if not v or v["mtime"] != mt:
            v = {"mtime": mt, "kurallar": kural_parcala(y)}
        yeni[str(y)] = v
        out += [tuple(k) for k in v["kurallar"]]
    if yeni != eski:
        Path(onbellek).parent.mkdir(parents=True, exist_ok=True)
        Path(onbellek).write_text(json.dumps(yeni, ensure_ascii=False), encoding="utf-8")
    return out


def kural_esle(t, state, kurallar, a1=KURAL_ASAMA1, a2=KURAL_ASAMA2):
    """Aşama 1: dilim başına choice + hiçbiri (tek istek) → birinci seçim; aşama 2: o kurala noul (tek istek).
    p≥0.5 ise kuralın kısaltması, değilse ya da birinci seçim 'hiçbiri'yse None. Aday başına ≤2 istek.
    Bant aranmaz: 12f tanısında doğru kural aşama 2'de Flag'de kalıyordu (.84/.78). 15: a1/a2 ile kart çifti ve çelişki de sorulur."""
    if not (ilk := en_yakin(t, state, kurallar, a1)):
        return None
    y = (t.yargila([state], {"k": {"type": "noul", "instructions": a2.format(k=dict(kurallar).get(ilk, ilk))}})[0] or {}).get("k")
    esik = DESTEK_ESIK if len(kavramlar(state) & kavramlar(dict(kurallar).get(ilk, ""))) >= 2 else 0.5
    return ilk if y and y["noul"] >= esik else None


def kavramlar(metin):
    """Normalleştirilmiş kavram kümesi (ör. Sonnet/Haiku/ucuz model → model)."""
    s = metin.casefold()
    return {k for k, ws in KAVRAM.items() if any(w in s for w in ws)}


def kural_regresyon(t, fix, kurallar):
    """23 K3: bilinen çiftler ÇİFT, bilinen yanlış pozitifler (kendi kuralı eklenerek) ÇİFT değil. Aday başına ≤2 istek."""
    r = {"bulunan": [], "kacan": [], "yp": []}
    for x in fix["cift"]:
        e = kural_esle(t, x["state"], kurallar)
        r["bulunan" if e in x["beklenen"] else "kacan"].append(f"{x['ad']} → {e}")
    for x in fix["degil"]:
        if e := kural_esle(t, x["state"], kurallar + [tuple(x["kural"])]):
            r["yp"].append(f"{x['ad']} → {e}")
    return r


def en_yakin(t, state, kurallar, a1=KURAL_ASAMA1):
    """Aşama 1: dilim başına choice + hiçbiri (tek istek) → birinci seçimin etiketi ya da None."""
    if not kurallar:
        return None
    s1 = {f"d{i}": {"type": "choice", "instructions": a1,
                    "criteria": {**dict(d), sk.HICBIRI: "Bu ipucu listedeki hiçbir kuralda yok."}}
          for i, d in enumerate(sk.dilimle(kurallar))}
    olas = {}
    for y in (t.yargila([state], s1)[0] or {}).values():
        for a, p in (y.get("probabilities") or {}).items():
            olas[a] = max(p, olas.get(a, 0.0))
    ilk = min(olas.items(), key=lambda x: (-x[1], x[0]), default=(sk.HICBIRI, 0))[0]
    return None if ilk == sk.HICBIRI else ilk


SHORT_SN = 120  # M2b K0: short tek tanım — kuyruk.md (<2 dk) · paket künyesi · parti gruplama
IPUCU = re.compile(r"github|\brepo|https?://|\blink|\bprompt", re.I)  # DERİNLİK-1 R4: short altyazısında geçerse kare tavanı 8


def short_mu(sn):
    return 0 < (sn or 0) < SHORT_SN
