"""MOTOR-M2a: parti motoru çekirdeği — aşama 1 kuyruk · 2 paket · 3-4 hafif tarayıcı formu + doğrulama + rapor · 10 defter.
Durum .kos/<parti-id>/durum.json (her adımda atomik), defter .kos/<parti-id>/defter.jsonl (model çağrısı başına satır)."""
import json
import os
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from jev import cekirdek as c

from . import hafif
from . import metin as m
from . import tarama as tr

YENIDEN = {"bekliyor", "hata", "tavan"}
SHORT_GRUP, GIRDI_TAVAN = 8, 40_000  # parti-motoru.md: short grubu ≤8, çağrı girdisi ≤40k jeton
KARE_TK = 1_600  # ponytail: kare başına sabit jeton tahmini; gruplar sınırda kalırsa gerçek boyut (cli._kare_tk)
SISTEM = ("Video tarayıcısısın. Her VIDEO bloğu bir paket: künye, açıklama bağlantıları, altyazı segmentleri, kare listesi. "
          "Her video için formu Türkçe ve eksiksiz doldur; zorunlu alanlar boş olamaz. Zamanlar m:ss ve video süresi içinde "
          "(yalnız açıklamada geçiyorsa 'açıklama'). Açıklama bağlantılarının HER biri için karar ver (aday_mi + neden); erişilemeyende (ücretli topluluk, giriş gerekli) "
          "aday_mi false + erisilemez: <sebep>. "
          "Alıntı en fazla 15 kelime. Kareden okunan bilgide kaynak 'kare' (ekli görseller, sırası bloklardaki kare listesiyle aynı). "
          "Anahtar, şifre, token değeri yazma. Site/landing/frontend içerikli videoda site_ui doldur. Emin olmadığını belirsizliklere yaz. "
          "Gösterilen ya da söylenen her kurulum/terminal komutunu kurulum_komutlar'a yaz (komut · ne yapar · zaman · kaynak).")


OPS = {"karede_gorulen", "erisilemez", "alt_tur", "kullanim_kosullari", "ucretsiz_katman", "veri_gizliligi", "bizde_karsilik", "kurulum_komutlar"}  # M2c: opsiyonel alanlar


def _o(**alan):
    return {"type": "object", "required": [k for k in alan if k not in OPS], "additionalProperties": False, "properties": alan}


def _d(x):
    return {"type": "array", "items": x}


S = {"type": "string", "minLength": 1}
N = {"type": ["string", "null"]}
KAYNAK = {"type": "string", "enum": ["altyazı", "kare", "açıklama"]}
ZMN = {"type": "string", "minLength": 1, "description": "m:ss, video süresi içinde; yalnız açıklamadaysa 'açıklama'"}
KG = {"karede_gorulen": {"type": ["string", "null"], "description": "kare gönderildiyse zorunlu: karede tam olarak ne görülüyor"}}


def sema(ids):
    """Tarayıcı formu (motor-sema.md §1); tür listeleri rapor-denetle'ninkiyle aynı."""
    video = _o(id={"type": "string", "enum": list(ids)}, ozet=S, bolumler=_d(_o(zaman=ZMN, baslik=S)),
               adaylar=_d(_o(ad=S, tur={"type": "string", "enum": sorted(tr.TUR)}, ne=S, kanit_zamani=ZMN, kaynak=KAYNAK, kanit=S, repo_url=N, **KG)),
               aciklama_baglantilari=_d(_o(url=S, ne=S, aday_mi={"type": "boolean"}, neden=S, aday_adi=N, erisilemez=N)),
               site_ui=_d(_o(teknik=S, ne=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)),
               promptlar=_d(_o(metin=S, amac=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)),
               iddialar=_d(_o(iddia=S, kanit_zamani=ZMN, kaynak=KAYNAK, tur={"type": "string", "enum": sorted(tr.IDDIA_TUR)}, aday_adi=N, **KG)),
               kareden_okunanlar=_d(_o(kare=S, okunan=S)), belirsizlikler=_d(S),
                kurulum_komutlar=_d(_o(komut=S, ne_yapar=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)))
    return _o(videolar={"type": "array", "minItems": len(ids), "items": video})


def _denet(x, s, yol):
    t = s.get("type")
    if x is None:
        return [] if isinstance(t, list) and "null" in t else [f"{yol}: eksik"]
    if t == "object":
        if not isinstance(x, dict):
            return [f"{yol}: nesne değil"]
        return [f"{yol}.{k}: eksik" for k in s["required"] if k not in x] + \
            [h for k, a in s["properties"].items() if k in x for h in _denet(x[k], a, f"{yol}.{k}")]
    if t == "array":
        return [h for i, y in enumerate(x) for h in _denet(y, s["items"], f"{yol}[{i}]")] if isinstance(x, list) else [f"{yol}: dizi değil"]
    if t == "boolean":
        return [] if isinstance(x, bool) else [f"{yol}: bool değil"]
    if not isinstance(x, str):
        return [f"{yol}: metin değil"]
    if s.get("minLength") and not x.strip():
        return [f"{yol}: boş olamaz"]
    return [f"{yol}: '{x}' geçersiz ({', '.join(s['enum'])})"] if "enum" in s and x not in s["enum"] else []


def dogrula(form, paketler, ids):
    """→ {id: [hata]}; boş = hepsi geçti. Şema + her açıklama bağlantısına karar + üretilecek raporun rapor-denetle'si."""
    s = sema(ids)["properties"]["videolar"]["items"]
    gelen = {f.get("id"): f for f in (form or {}).get("videolar") or [] if isinstance(f, dict)}
    out = {}
    for v in ids:
        if (f := gelen.get(v)) is None:
            out[v] = [f"videolar: {v} formu yok"]
            continue
        h = _denet(f, s, v)
        if not h:
            kararli = {b["url"] for b in f["aciklama_baglantilari"]}
            h = [f"{v}.aciklama_baglantilari: karar yok: {u}" for u in paketler[v]["linkler"] if u not in kararli]
            if paketler[v]["kareler"] and hafif.GORSEL:  # M2c K5: kare gönderildiyse yalnız kare kaynaklı bulguda karede görülen zorunlu
                h += [f"{v}.{b}[{i}].karede_gorulen: kare gönderildi, karede görülen boş olamaz" for b in ("adaylar", "site_ui", "promptlar", "iddialar")
                      for i, x in enumerate(f[b]) if x.get("kaynak") == "kare" and not (x.get("karede_gorulen") or "").strip()]
            h += [f"{v} rapor: {x}" for x in tr.denetle(rapor_md(f, paketler[v], []), paketler[v]["sure"])]
        if h:
            out[v] = h
    return out


def _ks(x):
    z = re.search(r"(\d+):(\d{2})", str(x))
    return int(z[1]) * 60 + int(z[2]) if z else None


def paket_oku(yol):
    metin = Path(yol).read_text(encoding="utf-8")
    bas = metin.splitlines()[0][2:].split(" · ")
    sure = int(x[1]) if (x := re.search(r"· sure_sn (\d+)", metin)) else m.sn(re.search(r"· süre (\S+)", metin)[1])
    dil = re.search(r"· dil (\S+)", metin)
    satir = lambda b: [s.strip() for s in tr.bolum(metin, b).splitlines() if s.strip() and s.strip() != "yok"]
    return {"id": bas[0], "baslik": bas[1], "kanal": bas[2], "sure": sure, "dil": dil[1] if dil else "?", "metin": metin,
            "short": x[1] == "true" if (x := re.search(r"· short: (true|false)", metin)) else tr.short_mu(sure),
            "linkler": satir("Açıklama bağlantıları"), "kareler": [s.split(" · ")[0] for s in satir("Kareler")],
            "kare_zaman": [_ks(s.split(" · ")[1]) if " · " in s else None for s in satir("Kareler")]}  # ölçüm betikleri (olcum_m4/m4b)


def _h(x):
    return re.sub(r"\s+", " ", str(x)).replace("|", "/").strip()


def _kg(x):
    return f" (karede: {_h(x['karede_gorulen'])})" if x.get("karede_gorulen") else ""


def _nk(s):  # M4c: yalnız gösterim (test_m4 K1 testi); şema nasil/kutuphane istemez
    return f" — nasıl: {_h(s['nasil'])} · kütüphane: {_h(s['kutuphane'])}" if s.get("nasil") else ""


def rapor_md(f, pk, notlar):
    """Mevcut rapor biçimi (docs/video-tarama/*.md) koddan; prompt'lar Adaylar'a `prompt` satırı olarak girer."""
    L = [f"# {pk['baslik']}", "## Künye", f"{pk['baslik']} · {pk['kanal']} · süre: {m.ss(pk['sure'])} · {pk['dil']} · https://youtu.be/{pk['id']}",
         *notlar, "## Özet", _h(f["ozet"]), "## Bölümler", *([f"- {_h(b['zaman'])} {_h(b['baslik'])}" for b in f["bolumler"]] or ["- yok"]),
         "## Adaylar", "| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |", "|---|---|---|---|---|---|---|",
         *[f"| {_h(a['ad'])} | yok | {a['tur']} | {_h(a['repo_url'] or 'yok')} | {_h(a['ne'])} | {_h(a['kanit_zamani'])} | {_h(a['kanit'])}{_kg(a)} |" for a in f["adaylar"]],
         *[f"| {_h(p['amac'])} | yok | prompt | yok | {_h(p['metin'])} | {_h(p['kanit_zamani'])} | kaynak: {p['kaynak']} |" for p in f["promptlar"]],
         "## Açıklama bağlantıları",
         *([f"- {b['url']} — {_h(b['ne'])} · aday: {'evet (' + _h(b['aday_adi'] or '?') + ')' if b['aday_mi'] else 'hayır'} · {_h(b['neden'])}" + (f" · erişilemez: {_h(b['erisilemez'])}" if b.get('erisilemez') else "")
            for b in f["aciklama_baglantilari"]] or ["- yok"])]
    if f["site_ui"]:
        L += [f"## {tr.SITE_UI}", "| teknik | ne işe yarar | zaman | kaynak |", "|---|---|---|---|",
              *[f"| {_h(s['teknik'])} | {_h(s['ne'])}{_nk(s)}{_kg(s)} | {_h(s['kanit_zamani'])} | {s['kaynak']} |" for s in f["site_ui"]]]
    elif any(tr.SITE_UI in str(b) for b in f["belirsizlikler"]):  # M2f K1: tamam_eksik raporunda zorunlu bölüm EKSİK başlığıyla yazılır
        L += [f"## {tr.SITE_UI}", "- EKSİK: formda site/UI tekniği yok (kısmi kabul)"]
    if f.get("kurulum_komutlar"):  # M4 K1: altın setteki Kurulum/komutlar kategorisi
        L += ["## Kurulum/komutlar", "| komut | ne yapar | zaman | kaynak |", "|---|---|---|---|",
              *[f"| {_h(k['komut'])} | {_h(k['ne_yapar'])}{_kg(k)} | {_h(k['kanit_zamani'])} | {k['kaynak']} |" for k in f["kurulum_komutlar"]]]
    seg = sum(s.startswith("[") for s in tr.bolum(pk["metin"], "Segmentler").splitlines())
    L += ["## İddialar", "| iddia | zaman | tür |", "|---|---|---|", *[f"| {_h(i['iddia'])} | {_h(i['kanit_zamani'])} | {i['tur']} |" for i in f["iddialar"]],
          "## Kareden okunanlar", *([f"- {_h(k['kare'])}: {_h(k['okunan'])}" for k in f["kareden_okunanlar"]] or ["- yok"]),
          "## Belirsizlikler", *([f"- {_h(b)}" for b in f["belirsizlikler"]] or ["- yok"]),
          "## Atlanan segment oranı", f"0/{seg} (paket tam okuma, motor)"]
    return "\n".join(L) + "\n"


def gruplar(pk):
    """short'lar ≤8 ve ≤40k jetonluk gruplar; uzun video tek başına."""
    out = []
    for v, p in sorted(pk.items(), key=lambda x: not x[1]["short"]):  # M2b K0: short'lar kuyruk sırasından bağımsız
        tk = c.token(p["metin"]) + KARE_TK * len(p["kareler"])
        if p["short"] and out and out[-1][0] and len(out[-1][1]) < SHORT_GRUP and out[-1][2] + tk <= GIRDI_TAVAN:
            out[-1][1].append(v)
            out[-1][2] += tk
        else:
            out.append([p["short"], [v], tk])
    return [g[1] for g in out]


def site_mu(metin):
    """M2e K2: kuyruk notu ya da başlıkta site/UI · landing · prompt anatomisi → kare tavanı 12."""
    return bool(re.search(r"site|\bUI\b|landing|prompt anatomisi", metin or "", re.I))


def kare_sayisi(sure, site):
    """M2e K2: short ≤3 · uzun süre/2.5 dk (en az 4, en fazla 8) · site/UI en fazla 12 → (n, neden)."""
    if not sure:
        return 3, "süre bilinmiyor"
    if sure < tr.SHORT_SN:
        return 3, "short ≤3"
    return max(4, min(12 if site else 8, round(sure / 150))), f"{m.ss(sure)} / 2.5 dk · " + ("site/UI ≤12" if site else "4–8")


def kare_sigdir(pk):
    """M2e K2: uzun videonun çağrı girdisi ≤40k jeton; aşarsa kare düşürülür, rapora not."""
    for p in pk.values():
        tk = c.token(p["metin"])
        if not p["short"] and tk + KARE_TK * len(p["kareler"]) > GIRDI_TAVAN:
            n = max(0, (GIRDI_TAVAN - tk) // KARE_TK)
            p["kare_not"] = f"kareler: girdi ≤{GIRDI_TAVAN} jeton için {len(p['kareler'])}→{n}"
            p["kareler"] = p["kareler"][:n]


LISTE = ("bolumler", "adaylar", "aciklama_baglantilari", "site_ui", "promptlar", "iddialar", "kareden_okunanlar", "belirsizlikler")
AD = ("ad", "teknik", "amac", "iddia", "url", "kare", "baslik")


def kismi(f, hatalar, v):
    """M2e K1: geçmeyen alan 'EKSİK: <alan> (<sebep>)'; alan dışı hata Belirsizlikler'e. → (form, [[aday, alan, sebep]])
    ponytail: rapor düzeyi hata (süre dışı zaman vb.) satırda işaretlenmez, yalnız Belirsizlikler'de; rapor-denetle onu yine sayar."""
    f = json.loads(json.dumps(f))
    f.setdefault("ozet", "")
    for b in LISTE:
        f[b] = f.get(b) if isinstance(f.get(b), list) else []
    eksik, notlar = [], []
    for h in hatalar:
        x = re.match(rf"{re.escape(v)}\.(\w+)(?:\[(\d+)\])?(?:\.(\w+))?: (.+)", h)
        b, i, alan, sebep = x.groups() if x else (None, None, None, h.split(": ", 1)[-1])
        if b and i is None and alan is None and not isinstance(f.get(b), list):
            f[b] = f"EKSİK: {b} ({sebep})"
            eksik.append(["-", b, sebep])
        elif b and i is not None and alan and int(i) < len(f[b]) and isinstance(k := f[b][int(i)], dict):
            k[alan] = f"EKSİK: {alan} ({sebep})"
            eksik.append([next((str(k[a]) for a in AD if k.get(a) and not str(k[a]).startswith("EKSİK")), b), alan, sebep])
        else:
            notlar.append(f"EKSİK: {b or 'rapor'} ({sebep})")
            eksik.append(["-", b or "rapor", sebep])
    f["belirsizlikler"] += notlar
    return f, eksik


def _rapor_yaz(d, v, f, p, tdir, **ek):
    r = tdir / f"{d['tarih']}-{v}.md"
    r.parent.mkdir(parents=True, exist_ok=True)
    md = rapor_md(f, p, _notlar(d, p))
    r.write_bytes(md.encode("utf-8"))
    adaylar, ele = tr.ayikla(md)
    tr.kayit_ekle(tdir / "kayit.jsonl", [{"id": v, "tarih": d["tarih"], "rapor": r.name, "adaylar": adaylar, "ele": ele, "parti": d["parti"]}])
    d["videolar"][v]["tarama"].update(cikti=r.as_posix(), **ek)


def _kismi_kabul(pdir, d, v, p, tdir):
    """M2e K1: diskteki son form yeniden denetlenir, geçerli kısmıyla rapor → tamam_eksik; form yoksa False (form_red kalır)."""
    y = pdir / "form" / f"{v}.json"
    if not y.is_file():
        return False
    f, eksik = kismi(json.loads(y.read_text(encoding="utf-8")), dogrula({"videolar": [json.loads(y.read_text(encoding="utf-8"))]}, {v: p}, [v]).get(v, []), v)
    try:
        _rapor_yaz(d, v, f, p, tdir, durum="tamam_eksik" if eksik else "tamam", eksik=eksik, hata=None)
    except (KeyError, TypeError, AttributeError) as e:  # biçimi bozuk form rapora dökülemez: form_red kalır
        print(f"kısmi kabul: {v} rapor yazılamadı: {e}"[:200])
        return False
    return True


def _yaz(yol, d):
    d["guncelleme"] = datetime.now().isoformat(timespec="seconds")
    tmp = yol.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, yol)


def _defter(pdir):
    s = tr.kayit_oku(pdir / "defter.jsonl")
    return len(s), sum(x["usd"] for x in s), sum(x["girdi"] + x["onb_okuma"] + x["onb_yazma"] + x["cikti"] for x in s)


def _tavan(pdir, d):
    n, usd, _ = _defter(pdir)
    return n >= d["tavan"]["cagri"] or usd >= d["tavan"]["usd"]


def _istem(ids, pk, hatalar, temizle):
    s = "\n\n".join(f"=== VIDEO {v} · süre {m.ss(pk[v]['sure'])} · kare görseli {len(pk[v]['kareler']) if hafif.GORSEL else 0} ===\n"
                    f"{temizle(pk[v]['metin'])}" for v in ids)
    if hatalar:
        s += "\n\nÖNCEKİ FORM REDDEDİLDİ. Hatalar:\n" + "\n".join(f"- {x}" for v in ids for x in hatalar.get(v, [])) + \
             "\nBu videoların formunu düzeltip eksiksiz yeniden ver."
    return s


def _notlar(d, pk):
    k = len(pk["kareler"])
    return [f"motor: parti {d['parti']} · {d['model']} · hafif claude -p",
            "kareler: yok" if not k else f"kareler: görsel girdi ({k})" if hafif.GORSEL else f"kareler: metin açıklamasıyla ({k} kare görülmedi; açık kalem)",
            *([pk["kare_not"]] if pk.get("kare_not") else [])]


def _kos(pdir, d, onb, tdir, alt, temizle, cagir, env):
    yol = pdir / "durum.json"
    for v, s in d["videolar"].items():  # aşama 2: mevcut ozet/whisper/paket komutları (Jev 0: --istek-tavan 0)
        a = s["paket"]
        if a["durum"] == "tamam" or a["deneme"] >= 3:
            continue
        a["deneme"] += 1
        try:
            if not (onb / v / "paket.md").is_file():
                alt(["ozet", v])
                if not (onb / v / "segmentler.jsonl").is_file():
                    alt(["whisper", v])
                mt = json.loads((onb / v / "meta.json").read_text(encoding="utf-8")) if (onb / v / "meta.json").is_file() else {}
                n, neden = kare_sayisi(mt.get("duration") or 0, site_mu(f"{s.get('not', '')} {mt.get('title') or ''}"))  # M2e K2
                print(f"paket {v}: kare {n} ({neden})")
                alt(["paket", v, "--kare", str(n), "--istek-tavan", "0"])
            a.update(durum="tamam" if (onb / v / "paket.md").is_file() else "hata", cikti=(onb / v / "paket.md").as_posix())
        except Exception as e:  # tek videonun indirme hatası partiyi durdurmaz; devam yeniden dener
            a.update(durum="hata", hata=str(e)[:200])
        _yaz(yol, d)
    bek = [v for v, s in d["videolar"].items()
           if s["paket"]["durum"] == "tamam" and s["tarama"]["durum"] in YENIDEN and s["tarama"]["deneme"] < 3]
    pk = {v: paket_oku(onb / v / "paket.md") for v in bek}
    kare_sigdir(pk)
    for g in gruplar(pk):  # aşama 3-4
        for v in g:
            d["videolar"][v]["tarama"]["deneme"] += 1
        _yaz(yol, d)
        kalan, hatalar = list(g), {}
        for _ in range(3):  # ilk istek + en fazla 2 yeniden istek
            if _tavan(pdir, d):
                for v in bek:
                    if d["videolar"][v]["tarama"]["durum"] in YENIDEN and v in kalan and v in hatalar:  # M2e: formu geçmemiş video tavanda da form_red (sonra --kismi-kabul)
                        d["videolar"][v]["tarama"].update(durum="form_red", hata=hatalar[v][:5])
                    elif d["videolar"][v]["tarama"]["durum"] in YENIDEN:
                        d["videolar"][v]["tarama"]["durum"] = "tavan"
                d["durum"] = "tavan"
                _yaz(yol, d)
                print(f"parti: tavan aşıldı ({d['tavan']['cagri']} çağrı / ${d['tavan']['usd']}), motor durdu")
                return 3
            kareler = [k for v in kalan for k in pk[v]["kareler"] if Path(k).is_file()] if hafif.GORSEL else []
            try:
                y = cagir(SISTEM, _istem(kalan, pk, hatalar, temizle), sema(kalan), kareler=kareler, model=d["model"],
                          butce=min(d["butce"], d["tavan"]["usd"] - _defter(pdir)[1]), env=env)
            except Exception as e:  # M2b K0: çağrı ortası kesinti → durum hata; devam yalnız bu grubu yeniden çağırır
                y = {"hata": f"taşıyıcı: {e}"[:200]}
            hatalar = {} if y.get("hata") else dogrula(y.get("form"), pk, kalan)
            for f in (y.get("form") or {}).get("videolar") or []:  # M2e K1: son form diskte (kısmi kabul çağrısız)
                if isinstance(f, dict) and f.get("id") in kalan:
                    (pdir / "form").mkdir(exist_ok=True)
                    (pdir / "form" / f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")
            u = y.get("usage") or {}
            tr.kayit_ekle(pdir / "defter.jsonl", [{
                "zaman": datetime.now().isoformat(timespec="seconds"), "adim": "tarama", "videolar": kalan, "model": d["model"],
                "girdi": u.get("input_tokens", 0), "onb_okuma": u.get("cache_read_input_tokens", 0), "onb_yazma": u.get("cache_creation_input_tokens", 0),
                "cikti": u.get("output_tokens", 0), "sure": y.get("sure"), "usd": y.get("usd") or 0.0, "kare": len(kareler),
                "form": f"hata: {y['hata']}" if y.get("hata") else f"red {len(hatalar)}/{len(kalan)}" if hatalar else "gecti"}])
            if y.get("hata"):
                for v in kalan:
                    d["videolar"][v]["tarama"].update(durum="hata", hata=y["hata"][:200])
                kalan = []
                break
            for v in kalan:
                if v not in hatalar:
                    _rapor_yaz(d, v, next(f for f in y["form"]["videolar"] if f.get("id") == v), pk[v], tdir, durum="tamam", usage=u, grup=len(kalan), hata=None)
            kalan = [v for v in kalan if v in hatalar]
            _yaz(yol, d)
            if not kalan:
                break
        for v in kalan:  # M2e K1: 2 yeniden istekten sonra kısmi kabul; son form yoksa form_red
            if not _kismi_kabul(pdir, d, v, pk[v], tdir):
                d["videolar"][v]["tarama"].update(durum="form_red", hata=hatalar[v][:5])
        _yaz(yol, d)
    d["durum"] = "tamam" if all(s["tarama"]["durum"] in ("tamam", "tamam_eksik", "form_red") for s in d["videolar"].values()) else "yarim"
    _yaz(yol, d)
    return 0


def _ozet(pdir, d):
    n, usd, tk = _defter(pdir)
    say = lambda a: " · ".join(f"{k} {x}" for k, x in sorted(Counter(s[a]["durum"] for s in d["videolar"].values()).items()))
    taranan = sum(s["tarama"]["durum"] == "tamam" and not s["tarama"].get("ice_alindi") for s in d["videolar"].values())
    print(f"parti {d['parti']} · durum {d['durum']} · paket: {say('paket')} · tarama: {say('tarama')}")
    print(f"defter: {n} çağrı / tavan {d['tavan']['cagri']} · ${usd:.4f} / ${d['tavan']['usd']} · {tk} jeton"
          + (f" · taranan video başına {tk // taranan} jeton" if taranan else ""))
    for v, s in d["videolar"].items():
        t = s["tarama"]
        print(f"- {v} · paket {s['paket']['durum']} · tarama {t['durum']}" + (" (içe alındı)" if t.get("ice_alindi") else "")
              + (f" · {t['cikti']}" if t.get("cikti") else "") + (f" · {str(t['hata'])[:120]}" if t.get("hata") else ""))
    return 0


def parti(ns, ctx):
    from . import cli, uygula as uy  # döngüsel içe aktarma yok: yalnız varsayılanlar için
    kok = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK)
    tdir = ctx.get("tarama_dizin") or cli._tarama_dizin(ctx)
    alt = ctx.get("alt") or (lambda a: cli.main(a, env=ctx["env"], kos=ctx["kos"], gonder=ctx["gonder"], uyku=ctx["uyku"]))
    temizle = ctx.get("temizle") or (lambda s: cli._temizle(s, ctx["env"]))
    if ns.eylem == "kuyruk" and not ns.hedef:  # M2d K4: tek komut; varsayılan kuyruk
        ns.hedef = (kok / "docs" / "video-tarama" / "kuyruk.md").as_posix()
    if ns.eylem in ("baslat", "kuyruk"):
        tur, satirlar = tr.kuyruk_parti(Path(ns.hedef).read_bytes().decode("utf-8"))
        if not satirlar:
            print("parti: kuyrukta bekleyen video yok")
            return 1
        if (ns.short and tur != "short") or (ns.uzun and tur != "uzun"):
            print(f"parti: kuyruğun sıradaki partisi {tur}")
            return 2
        tarih = ns.tarih or date.today().isoformat()
        pid, i = f"{tarih}-{tur}", 1
        while (kok / ".kos" / pid).exists():
            i += 1
            pid = f"{tarih}-{tur}-{i}"
        (pdir := kok / ".kos" / pid).mkdir(parents=True)
        d = {"parti": pid, "tur": tur, "tarih": tarih, "model": ns.model, "butce": ns.butce, "kuyruk": Path(ns.hedef).as_posix(),
             "tavan": {"cagri": ns.cagri_tavan, "usd": ns.usd_tavan}, "durum": "calisiyor", "videolar": {}}
        for h in satirlar[:ns.en_fazla]:
            eski = sorted(Path(tdir).glob(f"*-{h[0]}.md"))  # mevcut rapor yeniden taranmaz
            adim = {"durum": "tamam", "deneme": 0, "cikti": eski[-1].as_posix(), "ice_alindi": True} if eski else {"durum": "bekliyor", "deneme": 0}
            d["videolar"][h[0]] = {"paket": dict(adim), "tarama": dict(adim), "not": " ".join(h[2:4])}  # M2e K2: site/UI kare tavanı
        _yaz(pdir / "durum.json", d)
        print(f"parti: {pid} · {tur} · {len(d['videolar'])} video · tavan {ns.cagri_tavan} çağrı / ${ns.usd_tavan}")
    else:
        pdir = kok / ".kos" / ns.hedef
        if not (pdir / "durum.json").is_file():
            print(f"parti yok: {pdir.as_posix()}")
            return 1
        d = json.loads((pdir / "durum.json").read_text(encoding="utf-8"))
        if ns.eylem == "durum":
            return _ozet(pdir, d)
        if getattr(ns, "cagri_ek", 0) or getattr(ns, "usd_ek", 0):  # M2b: tavan yalnız açıkça yükseltilir
            d["tavan"] = {"cagri": d["tavan"]["cagri"] + ns.cagri_ek, "usd": round(d["tavan"]["usd"] + ns.usd_ek, 4)}
        if ns.eylem == "akil" and getattr(ns, "yeniden", False):  # M2g K1: yalnız geliştirme karşılaştırması yeniden (kayıt satırlarına dokunmaz)
            from . import akil
            d.pop("gelistirme", None)
            akil.gelistir(pdir, d, kok, ctx)
            _yaz(pdir / "durum.json", d)
            print(f"panel: {akil.panel(pdir, d, kok).as_posix()} · geliştirme {len(d.get('gelistirme', []))} satır · bizde bilgi yok {len(d.get('bizde_yok', []))}")
            return 0
        if ns.eylem in ("akil", "kapat"):
            from . import akil
            return akil.akil(pdir, d, kok, Path(tdir), ctx, getattr(ns, "tum", False)) if ns.eylem == "akil" else akil.kapat(pdir, d, kok, ctx)
        if getattr(ns, "yeniden_tara", False):  # M2d: _temizle URL hatası sonrası — bitmiş videolar düzeltilmiş girdiyle yeniden taranır
            for s in d["videolar"].values():
                if s["tarama"]["durum"] in ("tamam", "tamam_eksik", "form_red", "tavan"):
                    s["tarama"].update(durum="bekliyor", deneme=0, hata=None)
        if getattr(ns, "form_red_yeniden", False):  # M2b K6: form_red → yeniden dene hakkı
            for s in d["videolar"].values():
                if s["tarama"]["durum"] == "form_red":
                    s["tarama"].update(durum="bekliyor", deneme=min(s["tarama"]["deneme"], 2))
        if getattr(ns, "kismi_kabul", False):  # M2e K1: form_red → diskteki son formdan tamam_eksik, çağrısız
            for v, s in d["videolar"].items():
                if s["tarama"]["durum"] == "form_red" and not _kismi_kabul(pdir, d, v, paket_oku(Path(ctx["kok"]) / v / "paket.md"), Path(tdir)):
                    print(f"kısmi kabul: {v} son form yok (M2e öncesi) — form_red kalır")
            _yaz(pdir / "durum.json", d)
            return _ozet(pdir, d)
        d["durum"] = "calisiyor"
    kos = lambda: _kos(pdir, d, Path(ctx["kok"]), Path(tdir), alt, temizle, ctx.get("cagir") or hafif.cagir, ctx["env"])
    rc = kos()
    if ns.eylem == "kuyruk" and rc == 0:  # M2d K4: form_red bir kez yeniden → akil → panelde dur
        red = [s for s in d["videolar"].values() if s["tarama"]["durum"] == "form_red"]
        for s in red:
            s["tarama"].update(durum="bekliyor", deneme=min(s["tarama"]["deneme"], 2))
        rc = kos() if red else rc
        from . import akil
        rc = rc or akil.akil(pdir, d, kok, Path(tdir), ctx)
        n, usd, _ = _defter(pdir)
        print(f"panel: docs/kurulumlar/parti/{d['parti']}/panel.md · defter {n} çağrı ${usd:.4f} · sonra: panel Ömer sütunu → video panel uygula → video parti kapat {d['parti']}")
    _ozet(pdir, d)
    return rc


def panel(ns, ctx):
    from . import akil
    return akil.panel_uygula(ns, ctx)
