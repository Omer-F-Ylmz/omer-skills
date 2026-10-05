"""KANAL-1: işlenmiş videoların kanalları → liste · onay · envanter (yt-dlp flat, indirme yok) · etiketli veri. Model çağrısı yok."""
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
IPTAL = {"2026-10-01-uzun"}  # iptal edilen parti: satırları değer kaynağı sayılmaz
DEGERLI = ("AL", "UYARLA", "DENE", "KUR")
KARSI = ("RED", "ZATEN", "ERTELE", "ÖĞREN")  # karar sözcüğü bunlardan biriyse yargı değeri ezilir
ESIK = "takip: değerli ≥2 ve değerli/işlenen ≥0.5 · atla: değerli 0 ve işlenen ≥3 · bir-kez: diğer"
BEKLE = 2  # sn, aynı kanalda istekler arası
GERI = (30, 90)  # 429/403 → bekle + en fazla 2 yeniden deneme, sonra kanal yarım
RAPOR = re.compile(r"^(?:(\d{4}-\d{2}-\d{2})-)?([A-Za-z0-9_-]{11})\.md$")
BASLIK = ("kanal", "channel_id", "URL", "işlenen (n)", "değerli", "son işlenen", "öneri", "Ömer")


class Hata(Exception):
    pass


def _jsonl(yol):
    return [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()] if yol.is_file() else []


def _karar(r):
    w = re.split(r"[\s(:]", str(r.get("karar") or ""), maxsplit=1)[0]
    if w in DEGERLI:
        return w
    return None if w.upper() in KARSI else (r.get("yargi") if r.get("yargi") in DEGERLI else None)


def _aday_bolum(kok):
    """Raporların aday/karar bölümü (ya da başlıksız 'aday' tablosu) ilk sütunu → {slug: {video}}; düz metin taranmaz."""
    out, rd = {}, kok / "docs/video-tarama"
    for f in sorted(rd.glob("*.md")) if rd.is_dir() else []:
        if not (m := RAPOR.match(f.name)) or f.name.startswith("00-"):
            continue
        bolum = False
        for x in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if x.startswith("#"):
                bolum = bool(re.search(r"aday|karar", x, re.I))
            elif x.startswith("|"):
                h = tr.slug(x.strip("|").split("|")[0])
                if h == "aday":
                    bolum = True  # eski biçim: başlıksız aday tablosu
                elif bolum and h:
                    out.setdefault(h, set()).add(m[2])
    return out


def _bagla(kok, r, idx):
    """B2: (sınıf, videolar, not) — (a) aday dosyası video/kaynak alanı (b) rapor aday bölümü; >3 video aşırı eşleşme."""
    adlar = {a for x in (r.get("ad"), r.get("aday")) if x and (a := tr.slug(x)[:40])}
    vids = set()
    for a in adlar:
        y = kok / "docs/kurulumlar/adaylar" / f"{a}.md"
        for x in y.read_text(encoding="utf-8").splitlines() if y.is_file() else []:
            if x.startswith("video:"):
                vids |= set(re.findall(r"(?<![\w-])[\w-]{11}(?![\w-])", x[6:]))
            elif x.startswith("kaynak:"):
                vids |= set(re.findall(r"(?:v=|youtu\.be/)([\w-]{11})", x))
    if not vids:
        vids = set().union(*(v for k, v in idx.items() for a in adlar if k == a or k.startswith(a + "-")))
    if len(vids) > 3:
        return "çözülemedi", [], " (aşırı eşleşme)"
    if vids:
        return "video", sorted(vids), ""
    p = r.get("parti")
    return ("video-dışı" if p and not (kok / ".kos" / str(p) / "durum.json").is_file() else "çözülemedi"), [], ""


def degerli(kok, sayac=None):
    """{video: [kaynak]}, {B2 sınıfı: [ad]} iki kayıttan; video alanı yoksa parti durum.json aday→video (-gelistirme eki atılır), o da yoksa _bagla.
    sayac verilirse B2 sınıfı başına karar kaydı sayılır (aynı adın tekrar kayıtları dahil; liste tekil ad)."""
    out, durum, b2, idx = {}, {}, {}, None
    for r in _jsonl(kok / "docs/video-tarama/kayit.jsonl") + _jsonl(kok / "docs/kurulumlar/kayit.jsonl"):
        k, p, ad = _karar(r), r.get("parti"), str(r.get("ad") or "")
        if not k or p in IPTAL:
            continue
        if r.get("video"):
            vids = [r["video"]]
        else:
            if p not in durum:
                y = kok / ".kos" / str(p) / "durum.json"
                durum[p] = json.loads(y.read_text(encoding="utf-8")).get("adaylar", {}) if p and y.is_file() else {}
            vids = list(durum[p].get(ad.removesuffix("-gelistirme"), {}).get("videolar", {}))
            if not vids:
                idx = _aday_bolum(kok) if idx is None else idx
                sinif, vids, not_ = _bagla(kok, r, idx)
                if sayac is not None:
                    sayac[sinif] = sayac.get(sinif, 0) + 1
                if ad + not_ not in (kume := b2.setdefault(sinif, [])):
                    kume.append(ad + not_)
        for v in vids:
            kaynak = f"{k}:{ad}" + (f"@{p}" if p else "") + (" ortak" if len(vids) > 1 else "")
            if kaynak not in out.setdefault(v, []):
                out[v].append(kaynak)
    return out, b2


def _eski_hat(kok):
    """A1: yalnız tarihsiz (23 Eyl öncesi biçim) raporu olan videolar."""
    rd, t = kok / "docs/video-tarama", {}
    for f in rd.glob("*.md") if rd.is_dir() else []:
        if (m := RAPOR.match(f.name)) and not f.name.startswith("00-"):
            t[m[2]] = t.get(m[2], False) or bool(m[1])
    return {v for v, tarihli in t.items() if not tarihli}


def videolar(ctx, kok):
    """İşlenmiş videolar (rapor dosyaları ∪ video-tarama kayıt) → {id: {tarih, kanal, channel_id, url}}; eski biçim rapor sayısı."""
    rd, vs, eski = kok / "docs/video-tarama", {}, 0
    for f in sorted(rd.glob("*.md")) if rd.is_dir() else []:
        if (m := RAPOR.match(f.name)) and not f.name.startswith("00-"):
            vs.setdefault(m[2], {"tarih": m[1] or ""})
            eski += "## İddialar" not in f.read_text(encoding="utf-8", errors="replace")
    for r in _jsonl(rd / "kayit.jsonl"):
        m = RAPOR.match(r.get("rapor") or f"{r['id']}.md")
        if not m or m[2] != r["id"]:  # kaynak-*/kurulum-* satırları video değil
            continue
        t = vs.setdefault(r["id"], {"tarih": ""})
        t["tarih"] = max(t["tarih"], r.get("tarih") or "")
    kanal_ad = {r["video"]: r["kanal"] for r in _jsonl(kok / "docs/kurulumlar/kayit.jsonl") if r.get("video") and r.get("kanal")}
    vky = kok / ".kos/kanal/video-kanal.json"
    vk = json.loads(vky.read_text(encoding="utf-8")) if vky.is_file() else {}
    for v, t in vs.items():
        y = ctx["kok"] / v / "meta.json"
        m = vk.get(v, {}) | {k: x for k, x in (json.loads(y.read_text(encoding="utf-8")) if y.is_file() else {}).items() if x}  # önce meta, sonra video-kanal.json
        t |= {"kanal": m.get("channel") or kanal_ad.get(v) or "?", "channel_id": m.get("channel_id") or "", "url": m.get("channel_url") or ""}
    ad_id = {t["kanal"]: (t["channel_id"], t["url"]) for t in vs.values() if t["channel_id"]}
    for t in vs.values():  # kanaldan bir video çözüldüyse aynı adlı kimliksiz videolar da o kimliği alır
        if not t["channel_id"] and t["kanal"] in ad_id:
            t["channel_id"], t["url"] = ad_id[t["kanal"]]
    return vs, eski


def oneri(n, d):
    return "takip" if d >= 2 and d / n >= 0.5 else "atla" if d == 0 and n >= 3 else "bir-kez"


def _hucre(x):
    return str(x).replace("|", "\\|")


def _tablo(yol):
    """kanallar.md satırları → [{başlık: hücre}] (\\| kaçışı çözülür)."""
    out = []
    for x in yol.read_text(encoding="utf-8").splitlines():
        h = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", x.strip())[1:-1]]
        if len(h) == len(BASLIK) and h[0] != BASLIK[0] and not set(h[0]) <= set("-: "):
            out.append(dict(zip(BASLIK, h)))
    return out


def liste(ctx):
    vs, eski = videolar(ctx, KOK)
    deg, _ = degerli(KOK)
    eh = _eski_hat(KOK)
    k = {}
    for v, t in vs.items():
        a = k.setdefault(t["channel_id"] or t["kanal"], {"kanal": t["kanal"], "channel_id": t["channel_id"], "url": t["url"], "n": 0, "d": 0, "e": 0, "son": ""})
        a["n"], a["d"], a["e"], a["son"] = a["n"] + 1, a["d"] + (v in deg), a["e"] + (v in eh and v not in deg), max(a["son"], t["tarih"])
    yol = KOK / "docs/video-tarama/kanallar.md"
    eski_omer = {}  # ad ve kimlikle: coz sonrası anahtar ad → channel_id değişse de Ömer sütunu korunur
    for r in _tablo(yol) if yol.is_file() else []:
        if r["Ömer"]:
            eski_omer |= {r["kanal"]: r["Ömer"]} | ({r["channel_id"]: r["Ömer"]} if r["channel_id"] else {})
    md = [f"# Kanallar · {date.today()} · {len(k)} kanal · {len(vs)} işlenmiş video", "",
          f"Öneri eşikleri: {ESIK}. Değerli = ≥1 AL/UYARLA/DENE/KUR kararı (iki kayıt; -gelistirme dahil; iptal parti hariç).",
          "Ömer sütunu: takip · bir-kez · atla (boş satır işlenmez) → `video kanal onay docs/video-tarama/kanallar.md`.", "",
          "| " + " | ".join(BASLIK) + " |", "|" + "---|" * len(BASLIK)]
    sayac = {}
    for anahtar, a in sorted(k.items(), key=lambda x: (-x[1]["d"], -x[1]["n"], x[1]["kanal"])):
        o = oneri(a["n"], a["d"])
        sayac[o] = sayac.get(o, 0) + 1
        n = f"{a['n']} (eski {a['e']})" if a["e"] else a["n"]  # A1: eski k = etiketsiz (eski hat) video
        md.append("| " + " | ".join(_hucre(x) for x in (a["kanal"], a["channel_id"], a["url"], n, a["d"], a["son"], o, eski_omer.get(anahtar) or eski_omer.get(a["kanal"], ""))) + " |")
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(md) + "\n", encoding="utf-8")
    kimliksiz = sum(not a["channel_id"] for a in k.values())
    print(f"kanallar: {yol.relative_to(KOK).as_posix()} · {len(k)} kanal ({kimliksiz} kimliksiz) · " + " · ".join(f"{o} {sayac.get(o, 0)}" for o in ("takip", "bir-kez", "atla")))
    if eski:
        print(f"uyarı: eski biçim rapor ({eski}, '## İddialar' yok) — kanal/değer kayıt ve meta'dan okundu")
    return 0


def onay(dosya):
    yol = KOK / "docs/video-tarama/kanallar.json"
    j = json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}
    n = 0
    for r in _tablo(Path(dosya)):
        if not (o := r["Ömer"].lower()):
            continue
        if o not in ("takip", "bir-kez", "atla"):
            print(f"uyarı: {r['kanal']}: geçersiz '{r['Ömer']}' atlandı")
            continue
        j[r["channel_id"] or r["kanal"]] = {"kanal": r["kanal"], "channel_id": r["channel_id"], "url": r["URL"], "karar": o}
        n += 1
    yol.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"onay: {n} kanal → {yol.relative_to(KOK).as_posix()}")
    return 0


def takip_ekle(kok, vids, ctx, kuyruk=""):
    """A3 Ömer kuralı (3 Eki): işlenen videonun kanalı kanallar.json'da yoksa 'takip' eklenir, varsa değişmez.
    channel_id: meta.json → .kos/kanal/video-kanal.json → yoksa uyarı (ağ isteği yok). Kuyruk notunda `kaynak: kanal:<id>` → envanterden gelen, eklemez.
    KANAL-2b C1: notunda `takip: hayır` olan satır da eklemez."""
    envanterden = {tr._hucre(s)[0] for s in kuyruk.splitlines() if s.lstrip().startswith("|") and ("kaynak: kanal:" in s or "takip: hayır" in s)}
    yol, vky = kok / "docs/video-tarama/kanallar.json", kok / ".kos/kanal/video-kanal.json"
    j = json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}
    vk = json.loads(vky.read_text(encoding="utf-8")) if vky.is_file() else {}
    eklenen = []
    for v in vids:
        if v in envanterden:
            continue
        y = Path(ctx["kok"]) / v / "meta.json" if ctx.get("kok") else None
        m = json.loads(y.read_text(encoding="utf-8")) if y and y.is_file() else {}
        if not m.get("channel_id"):
            m = vk.get(v, {})
        if not (cid := m.get("channel_id")):
            print(f"uyarı: takip: {v} channel_id yok (meta · video-kanal.json) — eklenmedi")
            continue
        if cid in j or any(a.get("channel_id") == cid for a in j.values()):
            continue
        j[cid] = {"kanal": m.get("channel") or "?", "channel_id": cid, "url": m.get("channel_url") or "", "karar": "takip", "kaynak": "otomatik · Ömer kuralı 3 Eki"}
        eklenen.append(cid)
    if eklenen:
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"takip: {len(eklenen)} yeni kanal → kanallar.json ({' · '.join(eklenen)})")
    return eklenen


def _tarih(e):
    # ponytail: --extractor-args approximate_date flat modda yaklaşık upload_date verir; yoksa timestamp; yoksa "tarih yok"
    if u := e.get("upload_date"):
        return f"{u[:4]}-{u[4:6]}-{u[6:8]}"
    t = e.get("timestamp") or e.get("release_timestamp")
    return datetime.fromtimestamp(t, timezone.utc).date().isoformat() if t else "tarih yok"


def _istek(ctx, args, sayac, yok=None, hata=None):
    """Tek yt-dlp -J isteği: önceki istekten ≥BEKLE sn sonra; 429/403'te GERI kadar bekleyip en fazla 2 yeniden deneme. → json ya da None.
    Hata metni `yok` desenine uyarsa (sekme yok) {} döner, hata sayılmaz. A8: `hata` listesi verilirse None'da son hata satırı eklenir."""
    geri = False
    for bekle in (*GERI, None):
        if sayac[0] and not geri:  # geri çekilme beklemesi istekler arası beklemeyi zaten karşılar
            ctx["uyku"](BEKLE)
        sayac[0] += 1
        rc, out, err = ctx["kos"](args, timeout=180)
        if not rc:
            return json.loads(out)
        e = (err or b"").decode("utf-8", "replace")
        if yok and re.search(yok, e):
            return {}
        if bekle is None or not re.search(r"HTTP Error (429|403)", e):
            if hata is not None:
                hata.append(([s for s in e.splitlines() if s.strip()] or [f"rc {rc}"])[-1].strip().removeprefix("ERROR: "))
            return None
        ctx["uyku"](bekle)
        geri = True


def envanter(ctx, secili=None):
    from .cli import yt_url
    yol = KOK / "docs/video-tarama/kanallar.json"
    onayli = {k: a for k, a in (json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}).items()
              if a.get("karar") in ("takip", "bir-kez") and secili in (None, k, a.get("channel_id"))}
    if not onayli:
        raise Hata("onaylı kanal yok: önce `video kanal liste` → Ömer sütunu → `video kanal onay`")
    for k, a in onayli.items():
        cid = a.get("channel_id")
        if not cid:
            print(f"kimlik yok: {a['kanal']} — atlandı (kimlik çözme KANAL-2)")
            continue
        oy = KOK / ".kos/kanal" / f"{cid}.json"
        onb = json.loads(oy.read_text(encoding="utf-8")) if oy.is_file() else {"kanal": a["kanal"], "channel_id": cid, "videolar": {}}
        once, yarim, sayac = len(onb["videolar"]), False, [0]
        for sekme in ("videos", "shorts"):
            j = _istek(ctx, ["yt-dlp", "--flat-playlist", "--skip-download", "-J", "--no-warnings",
                             "--extractor-args", "youtubetab:approximate_date", f"https://www.youtube.com/channel/{cid}/{sekme}"], sayac,
                       rf"does not have a {sekme} tab")  # A4: shorts sekmesi yok → 0 short · C3: videos sekmesi yok (yalnız short kanal) → 0 uzun
            if j is None:
                yarim = True
                break
            for e in j.get("entries") or []:
                if e.get("id") and e["id"] not in onb["videolar"]:
                    onb["videolar"][e["id"]] = {"baslik": e.get("title"), "sure": e.get("duration"), "tarih": _tarih(e),
                                                "tur": "short" if sekme == "shorts" else "uzun", "url": yt_url(e["id"])}
        onb |= {"yarim": yarim, "guncelleme": datetime.now().isoformat(timespec="seconds")}
        oy.parent.mkdir(parents=True, exist_ok=True)
        oy.write_text(json.dumps(onb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{a['kanal']}: {len(onb['videolar'])} video · yeni {len(onb['videolar']) - once}" + (" · yarım (hata/hız sınırı)" if yarim else ""))
    return 0


def ekle(ctx, url):
    """KANAL-2b C2: kanal linki → channel_id (flat, tek öğe, indirme yok) → kanallar.json 'takip' (varsa değer korunur) → o kanalın envanteri."""
    if not url:
        raise Hata("ekle: kanal linki gerekli")
    j = _istek(ctx, ["yt-dlp", "--flat-playlist", "--skip-download", "-J", "--no-warnings", "-I", "1", url], [0])
    if not j or not (cid := j.get("channel_id")):
        raise Hata(f"ekle: channel_id çözülemedi: {url}")
    yol = KOK / "docs/video-tarama/kanallar.json"
    k = json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}
    if var := next((a for kk, a in k.items() if cid in (kk, a.get("channel_id"))), None):
        print(f"ekle: {var['kanal']} zaten listede ({var.get('karar')}) — değer korundu")
    else:
        k[cid] = {"kanal": j.get("channel") or "?", "channel_id": cid, "url": j.get("channel_url") or f"https://www.youtube.com/channel/{cid}",
                  "karar": "takip", "kaynak": "Ömer · kanal linki"}
        yol.parent.mkdir(parents=True, exist_ok=True)
        yol.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"ekle: {k[cid]['kanal']} ({cid}) → takip")
    ctx["uyku"](BEKLE)  # çözme isteği ile envanter isteği arası
    return envanter(ctx, cid)


def coz(ctx, tavan=100):
    """Kanalı '?' videolar + kimliksiz kanal başına 1 video → yt-dlp -J (indirme yok). meta.json varsa ona, yoksa .kos/kanal/video-kanal.json."""
    from .cli import yt_url
    vs, _ = videolar(ctx, KOK)
    hedef, gorulen = [], set()
    for v, t in sorted(vs.items()):
        if t["kanal"] == "?" or (not t["channel_id"] and t["kanal"] not in gorulen):
            hedef.append(v)
            gorulen.add(t["kanal"])
    vky = KOK / ".kos/kanal/video-kanal.json"
    vk = json.loads(vky.read_text(encoding="utf-8")) if vky.is_file() else {}
    sayac, ardisik, cozulen, durdu = [0], 0, [], ""
    for v in hedef:
        if sayac[0] >= tavan:
            durdu = f"tavan {tavan} istek"
            break
        j = _istek(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", yt_url(v)], sayac)
        if not j or not j.get("channel_id"):
            ardisik += 1
            if ardisik >= 3:
                durdu = "3 ardışık hata"
                break
            continue
        ardisik = 0
        alan = {k: j.get(k) for k in ("channel", "channel_id", "channel_url")}
        y = ctx["kok"] / v / "meta.json"
        if y.is_file():  # .video-cache klasörü yalnız varsa yazılır, açılmaz
            y.write_text(json.dumps(json.loads(y.read_text(encoding="utf-8")) | alan, ensure_ascii=False), encoding="utf-8")
        else:
            vk[v] = alan
        cozulen.append(alan["channel_id"])
    if vk:
        vky.parent.mkdir(parents=True, exist_ok=True)
        vky.write_text(json.dumps(vk, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"coz: hedef {len(hedef)} · çözülen video {len(cozulen)} · kanal {len(set(cozulen))} · çözülemedi {len(hedef) - len(cozulen)} · istek {sayac[0]}"
          + (f" · dur: {durdu}" if durdu else ""))
    return 0


def etiket(ctx):
    vs, _ = videolar(ctx, KOK)
    b2k = {}
    deg, b2 = degerli(KOK, b2k)
    eh = _eski_hat(KOK)
    et = [{"id": v, "kanal": t["kanal"], "channel_id": t["channel_id"], "degerli": v in deg,
           "sinif": "değerli" if v in deg else "etiketsiz (eski hat)" if v in eh else "değersiz", "kaynak": deg.get(v, []),
           "altyazi": any((ctx["kok"] / v).glob("altyazi*")) or (ctx["kok"] / v / "segmentler.jsonl").is_file()} for v, t in sorted(vs.items())]
    d, e, a = sum(x["degerli"] for x in et), sum(x["sinif"] == "etiketsiz (eski hat)" for x in et), sum(x["altyazi"] for x in et)
    ozet = {"toplam": len(et), "degerli": d, "degersiz": len(et) - d - e, "etiketsiz": e, "altyazi_onbellekte": a,
            "b2": {k: len(x) for k, x in b2.items()}, "b2_karar": b2k, "b2_cozulemedi": b2.get("çözülemedi", []),
            "kural": "≥1 AL/UYARLA/DENE/KUR (karar ya da yargı); docs/video-tarama + docs/kurulumlar kayit.jsonl; iptal parti " + ",".join(sorted(IPTAL))
            + " hariç · etiketsiz (eski hat): yalnız tarihsiz rapor ve karar yok"}
    yol = KOK / "docs/olcumler/kanal-etiket.json"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps({"ozet": ozet, "videolar": et}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"etiket: {len(et)} video · değerli {d} · değersiz {len(et) - d - e} · etiketsiz (eski hat) {e} · altyazı önbellekte {a} · B2 "
          + " · ".join(f"{k} {len(x)} ad/{b2k.get(k, 0)} karar" for k, x in b2.items()))
    return 0


def kanal(ns, ctx):
    if ns.eylem == "onay" and not ns.dosya:
        raise Hata("onay: dosya gerekli (docs/video-tarama/kanallar.md)")
    return {"liste": lambda: liste(ctx), "onay": lambda: onay(ns.dosya), "envanter": lambda: envanter(ctx, ns.kanal), "coz": lambda: coz(ctx, ns.tavan), "ekle": lambda: ekle(ctx, ns.dosya), "etiket": lambda: etiket(ctx)}[ns.eylem]()
