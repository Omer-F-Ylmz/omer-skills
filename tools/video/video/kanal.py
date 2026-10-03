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


def degerli(kok):
    """{video: [kaynak]}, {B2 sınıfı: [ad]} iki kayıttan; video alanı yoksa parti durum.json aday→video (-gelistirme eki atılır), o da yoksa _bagla."""
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
                if ad + not_ not in (kume := b2.setdefault(sinif, [])):
                    kume.append(ad + not_)
        for v in vids:
            kaynak = f"{k}:{ad}" + (f"@{p}" if p else "") + (" ortak" if len(vids) > 1 else "")
            if kaynak not in out.setdefault(v, []):
                out[v].append(kaynak)
    return out, b2


def videolar(ctx, kok):
    """İşlenmiş videolar (rapor dosyaları ∪ video-tarama kayıt) → {id: {tarih, kanal, channel_id, url}}; eski biçim rapor sayısı."""
    rd, vs, eski = kok / "docs/video-tarama", {}, 0
    for f in sorted(rd.glob("*.md")) if rd.is_dir() else []:
        if (m := RAPOR.match(f.name)) and not f.name.startswith("00-"):
            vs.setdefault(m[2], {"tarih": m[1] or ""})
            eski += "## İddialar" not in f.read_text(encoding="utf-8", errors="replace")
    for r in _jsonl(rd / "kayit.jsonl"):
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
    k = {}
    for v, t in vs.items():
        a = k.setdefault(t["channel_id"] or t["kanal"], {"kanal": t["kanal"], "channel_id": t["channel_id"], "url": t["url"], "n": 0, "d": 0, "son": ""})
        a["n"], a["d"], a["son"] = a["n"] + 1, a["d"] + (v in deg), max(a["son"], t["tarih"])
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
        md.append("| " + " | ".join(_hucre(x) for x in (a["kanal"], a["channel_id"], a["url"], a["n"], a["d"], a["son"], o, eski_omer.get(anahtar) or eski_omer.get(a["kanal"], ""))) + " |")
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


def _tarih(e):
    # ponytail: --extractor-args approximate_date flat modda yaklaşık upload_date verir; yoksa timestamp; yoksa "tarih yok"
    if u := e.get("upload_date"):
        return f"{u[:4]}-{u[4:6]}-{u[6:8]}"
    t = e.get("timestamp") or e.get("release_timestamp")
    return datetime.fromtimestamp(t, timezone.utc).date().isoformat() if t else "tarih yok"


def _istek(ctx, args, sayac):
    """Tek yt-dlp -J isteği: önceki istekten ≥BEKLE sn sonra; 429/403'te GERI kadar bekleyip en fazla 2 yeniden deneme. → json ya da None."""
    geri = False
    for bekle in (*GERI, None):
        if sayac[0] and not geri:  # geri çekilme beklemesi istekler arası beklemeyi zaten karşılar
            ctx["uyku"](BEKLE)
        sayac[0] += 1
        rc, out, err = ctx["kos"](args, timeout=180)
        if not rc:
            return json.loads(out)
        if bekle is None or not re.search(r"HTTP Error (429|403)", (err or b"").decode("utf-8", "replace")):
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
                             "--extractor-args", "youtubetab:approximate_date", f"https://www.youtube.com/channel/{cid}/{sekme}"], sayac)
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
    deg, b2 = degerli(KOK)
    et = [{"id": v, "kanal": t["kanal"], "channel_id": t["channel_id"], "degerli": v in deg, "kaynak": deg.get(v, []),
           "altyazi": any((ctx["kok"] / v).glob("altyazi*")) or (ctx["kok"] / v / "segmentler.jsonl").is_file()} for v, t in sorted(vs.items())]
    d, a = sum(x["degerli"] for x in et), sum(x["altyazi"] for x in et)
    ozet = {"toplam": len(et), "degerli": d, "degersiz": len(et) - d, "altyazi_onbellekte": a, "b2": {k: len(x) for k, x in b2.items()}, "b2_cozulemedi": b2.get("çözülemedi", []),
            "kural": "≥1 AL/UYARLA/DENE/KUR (karar ya da yargı); docs/video-tarama + docs/kurulumlar kayit.jsonl; iptal parti " + ",".join(sorted(IPTAL)) + " hariç"}
    yol = KOK / "docs/olcumler/kanal-etiket.json"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps({"ozet": ozet, "videolar": et}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"etiket: {len(et)} video · değerli {d} · değersiz {len(et) - d} · altyazı önbellekte {a} · B2 " + " · ".join(f"{k} {len(x)}" for k, x in b2.items()))
    return 0


def kanal(ns, ctx):
    if ns.eylem == "onay" and not ns.dosya:
        raise Hata("onay: dosya gerekli (docs/video-tarama/kanallar.md)")
    return {"liste": lambda: liste(ctx), "onay": lambda: onay(ns.dosya), "envanter": lambda: envanter(ctx, ns.kanal), "coz": lambda: coz(ctx, ns.tavan), "etiket": lambda: etiket(ctx)}[ns.eylem]()
