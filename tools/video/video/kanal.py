"""KANAL-1: işlenmiş videoların kanalları → liste · onay · envanter (yt-dlp flat, indirme yok) · etiketli veri. Model çağrısı yok."""
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
IPTAL = {"2026-10-01-uzun"}  # iptal edilen parti: satırları değer kaynağı sayılmaz
DEGERLI = ("AL", "UYARLA", "DENE")
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


def degerli(kok):
    """{video: [kaynak]} iki kayıttan; video alanı yoksa parti durum.json aday→video eşlemesi (-gelistirme eki atılır)."""
    out, durum, esz = {}, {}, 0
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
            esz += not vids
        for v in vids:
            kaynak = f"{k}:{ad}" + (f"@{p}" if p else "")
            if kaynak not in out.setdefault(v, []):
                out[v].append(kaynak)
    return out, esz


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
    for v, t in vs.items():
        y = ctx["kok"] / v / "meta.json"
        m = json.loads(y.read_text(encoding="utf-8")) if y.is_file() else {}
        t |= {"kanal": m.get("channel") or kanal_ad.get(v) or "?", "channel_id": m.get("channel_id") or "", "url": m.get("channel_url") or ""}
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
    eski_omer = {r["channel_id"] or r["kanal"]: r["Ömer"] for r in _tablo(yol)} if yol.is_file() else {}
    md = [f"# Kanallar · {date.today()} · {len(k)} kanal · {len(vs)} işlenmiş video", "",
          f"Öneri eşikleri: {ESIK}. Değerli = ≥1 AL/UYARLA/DENE kararı (iki kayıt; -gelistirme dahil; iptal parti hariç).",
          "Ömer sütunu: takip · bir-kez · atla (boş satır işlenmez) → `video kanal onay docs/video-tarama/kanallar.md`.", "",
          "| " + " | ".join(BASLIK) + " |", "|" + "---|" * len(BASLIK)]
    sayac = {}
    for anahtar, a in sorted(k.items(), key=lambda x: (-x[1]["d"], -x[1]["n"], x[1]["kanal"])):
        o = oneri(a["n"], a["d"])
        sayac[o] = sayac.get(o, 0) + 1
        md.append("| " + " | ".join(_hucre(x) for x in (a["kanal"], a["channel_id"], a["url"], a["n"], a["d"], a["son"], o, eski_omer.get(anahtar, ""))) + " |")
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
        once, yarim, istek, geri = len(onb["videolar"]), False, 0, False
        for sekme in ("videos", "shorts"):
            for bekle in (*GERI, None):
                if istek and not geri:  # geri çekilme beklemesi zaten istekler arası beklemeyi karşılar
                    ctx["uyku"](BEKLE)
                istek, geri = istek + 1, False
                rc, out, err = ctx["kos"](["yt-dlp", "--flat-playlist", "--skip-download", "-J", "--no-warnings",
                                           "--extractor-args", "youtubetab:approximate_date", f"https://www.youtube.com/channel/{cid}/{sekme}"], timeout=180)
                if not rc:
                    break
                e = (err or b"").decode("utf-8", "replace")
                if bekle is None or not re.search(r"HTTP Error (429|403)", e):
                    yarim = True
                    break
                ctx["uyku"](bekle)
                geri = True
            if yarim:
                break
            for e in json.loads(out).get("entries") or []:
                if e.get("id") and e["id"] not in onb["videolar"]:
                    onb["videolar"][e["id"]] = {"baslik": e.get("title"), "sure": e.get("duration"), "tarih": _tarih(e),
                                                "tur": "short" if sekme == "shorts" else "uzun", "url": yt_url(e["id"])}
        onb |= {"yarim": yarim, "guncelleme": datetime.now().isoformat(timespec="seconds")}
        oy.parent.mkdir(parents=True, exist_ok=True)
        oy.write_text(json.dumps(onb, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{a['kanal']}: {len(onb['videolar'])} video · yeni {len(onb['videolar']) - once}" + (" · yarım (hata/hız sınırı)" if yarim else ""))
    return 0


def etiket(ctx):
    vs, _ = videolar(ctx, KOK)
    deg, esz = degerli(KOK)
    et = [{"id": v, "kanal": t["kanal"], "channel_id": t["channel_id"], "degerli": v in deg, "kaynak": deg.get(v, []),
           "altyazi": any((ctx["kok"] / v).glob("altyazi*")) or (ctx["kok"] / v / "segmentler.jsonl").is_file()} for v, t in sorted(vs.items())]
    d, a = sum(x["degerli"] for x in et), sum(x["altyazi"] for x in et)
    ozet = {"toplam": len(et), "degerli": d, "degersiz": len(et) - d, "altyazi_onbellekte": a, "eslenmeyen_karar": esz,
            "kural": "≥1 AL/UYARLA/DENE (karar ya da yargı); docs/video-tarama + docs/kurulumlar kayit.jsonl; iptal parti " + ",".join(sorted(IPTAL)) + " hariç"}
    yol = KOK / "docs/olcumler/kanal-etiket.json"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps({"ozet": ozet, "videolar": et}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"etiket: {len(et)} video · değerli {d} · değersiz {len(et) - d} · altyazı önbellekte {a} · eşlenmeyen değerli karar {esz}")
    return 0


def kanal(ns, ctx):
    if ns.eylem == "onay" and not ns.dosya:
        raise Hata("onay: dosya gerekli (docs/video-tarama/kanallar.md)")
    return {"liste": lambda: liste(ctx), "onay": lambda: onay(ns.dosya), "envanter": lambda: envanter(ctx, ns.kanal), "etiket": lambda: etiket(ctx)}[ns.eylem]()
