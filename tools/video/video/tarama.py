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


def eski_kalemler(metin):
    """VİDEO-YENİDEN-1: eski rapor → [(ad, durum, etiket, not)]: `ad` başlıklı tablolar + `- ad → ETİKET (not)` maddeleri."""
    out = []
    for bas, satirlar in tablolar(metin):
        if bas[0].casefold() == "ad":
            out += [(h[0], (g := dict(zip(bas, h))).get("durum", ""), g.get("etiket", ""), g.get("not", "")) for h in satirlar if h[0]]
    for s in metin.splitlines():
        if x := MADDE_ESKI.match(s):
            out.append((x[1].strip(), "", x[2], x[3].strip(" ()")))
    return out


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
    h += [f"alıntı {len(a.split())} kelime > {ALINTI_KELIME}: {a[:40]}…" for a in ALINTI.findall(metin) if len(a.split()) > ALINTI_KELIME]
    return h + site_ui_denetle(metin)


def frontend_mu(metin):
    """Künye + Özet + Adaylar'da ≥2 farklı site/UI anahtar kelimesi."""
    return len({x.casefold() for x in FRONTEND.findall(" ".join(bolum(metin, b) for b in ("Künye", "Özet", "Adaylar")))}) >= 2


def site_ui_denetle(metin):
    """23 K5: teknik · kanıt (m:ss) · kütüphane/araç (ekranda/kanıtta yoksa 'tahmin: …') · bizde."""
    if not frontend_mu(metin):
        return []
    t = tablolar(bolum(metin, SITE_UI))
    if not t or not t[0][1]:
        return [f"bölüm eksik: ## {SITE_UI}"]
    h, oku = [], bolum(metin, "Kareden okunanlar").casefold()
    for s in t[0][1]:
        if len(s) != 4 or any(x in ("", "-") for x in (s[0], s[1], s[3])):
            h.append(f"boş alan: teknik satırı {s[0] or '?'} (teknik·kanıt·kütüphane/araç·bizde)")
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
