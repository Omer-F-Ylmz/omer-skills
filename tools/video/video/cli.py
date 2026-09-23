"""video — kademeli izleme: ozet → sor/suz → kare → whisper. Ham altyazı ve kareler önbellekte (repo dışı), ajana kompakt çıktı.
Jev isteği yalnız suz/sor'da ve tavanlı; önbellek varsa ağa çıkılmaz."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from jev import cekirdek as c
from jev import skill as sk

from . import kur
from . import metin as m
from . import ogren as og
from . import tarama as tr
from . import uygula as uy

KOK = r"C:\Projeler\.video-cache"
TARAMA_DIZIN = Path(__file__).resolve().parents[3] / "docs" / "video-tarama"
LISTE_TAVAN, ALTYAZI_ES, SUZ_ES = 8, 4, 8
SOR_TOKEN, ADAY_KR = 2_500, 400
GENISLIK = 768
GERI_CEKIL, HIZ_DK = (20, 60), 15  # 429: iki tekrar, sonra kullanıcıya bekleme süresi
SURE = {"meta": 120, "altyazi": 120, "kesit": 120, "ffmpeg": 60, "ses": 900}
ARAC_Q = {"type": "noul", "instructions": "Bu video kesiti (state) bir araç, skill, MCP, CLI, teknik ya da iş akışı anlatıyor mu?",
          "criteria": {"true": "Somut bir araç/teknik/iş akışı anlatılıyor.", "false": "Sohbet, giriş, reklam, genel yorum; araç anlatımı yok."}}
EKRAN_Q = {"type": "noul", "instructions": "Kesitte anlatılan şey ekranda gösteriliyor mu (komut, ayar, arayüz)?",
           "criteria": {"true": "Konuşma ekrandaki komut/ayar/arayüze atıf yapıyor (şuraya tıklayın, burada görüyorsunuz…).",
                        "false": "Yalnız sözlü anlatım; ekrana bakmak gerekmiyor."}}
GORUNTU_Q = {"type": "noul", "instructions": "Bu soruyu (state) yanıtlamak için videonun görüntüsüne (ekran, komut, arayüz) bakmak gerekir mi?",
             "criteria": {"true": "Yanıt ekranda görünen ayrıntıya bağlı.", "false": "Altyazı metni yeterli."}}
SORULAR = {"arac": ARAC_Q, "ekran": EKRAN_Q}
ASAMA1 = "Kullanıcının sorusu (state) videonun hangi kesitinde yanıtlanıyor? Hiçbiri değilse 'hiçbiri'."
ASAMA2 = "Kullanıcının sorusu (state) şu video kesitinde yanıtlanıyor mu? Kesit metni criteria.true içinde."
WHISPER_KUR = "faster-whisper kurulu değil. Kur: uv tool install -e tools/video --with faster-whisper"


def kos(args, timeout=120, env=None):
    r = subprocess.run(args, capture_output=True, timeout=timeout, env=env)
    return r.returncode, r.stdout, r.stderr


class Hata(Exception):
    pass


class HizHata(Hata):
    pass


def _kos(ctx, args, timeout):
    try:
        rc, out, err = ctx["kos"](args, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise Hata(f"{args[0]}: zaman aşımı ({timeout} sn)") from None
    if rc:
        son = (err or b"").decode("utf-8", "replace").strip().splitlines()[-1:] or ["?"]
        raise Hata(f"{args[0]} rc={rc}: {son[0][:200]}")
    return out


def _yt(ctx, args, timeout, d):
    """yt-dlp; 429'da 20/60 sn geri çekilip en fazla 2 tekrar, yine 429 → HizHata. Her hatada yarım altyazı dosyası silinir."""
    for bekle in (*GERI_CEKIL, None):
        try:
            return _kos(ctx, args, timeout)
        except Hata as e:
            for yarim in d.glob("altyazi*"):
                yarim.unlink()
            if "HTTP Error 429" not in str(e):
                raise
            if bekle is None:
                raise HizHata(f"{d.name}: YouTube hız sınırı: {HIZ_DK} dk sonra yeniden dene") from None
            ctx["uyku"](bekle)


def _dizin(ctx, v):
    d = ctx["kok"] / v
    d.mkdir(parents=True, exist_ok=True)
    return d


def _oku(d):
    yol = d / "segmentler.jsonl"
    if not yol.is_file():
        raise Hata(f"önbellek yok: önce `video ozet {d.name}`")
    return [json.loads(x) for x in yol.read_text(encoding="utf-8").splitlines() if x.strip()]


def _yaz(d, seg):
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in seg), encoding="utf-8")


def _meta(ctx, d):
    yol = d / "meta.json"
    if yol.is_file():
        return json.loads(yol.read_text(encoding="utf-8"))
    j = json.loads(_yt(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", d.name], SURE["meta"], d))
    alan = ("id", "title", "language", "channel", "duration", "chapters", "description", "subtitles", "automatic_captions")
    meta = {k: j.get(k) for k in alan}
    for k in ("subtitles", "automatic_captions"):  # yalnız dil anahtarları; format URL'leri gereksiz
        meta[k] = {d_: [] for d_ in (meta[k] or {})}
    yol.write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    return meta


def _ozet_satir(d, meta, seg, kaynak):
    tam = sum(c.token(s["metin"]) for s in seg)
    linkler = json.loads((d / "linkler.json").read_text(encoding="utf-8")) if (d / "linkler.json").is_file() else []
    return [f"{d.name} · {(meta.get('title') or '?')[:80]} · {meta.get('channel') or '?'}",
            f"süre {m.ss(meta.get('duration') or 0)} · {len(seg)} segment · ~{tam} token ({kaynak}) · {len(meta.get('chapters') or [])} chapter",
            f"linkler: {len(linkler)} · yol: {d}"]


def _ozet_bir(ctx, v, dil):
    d = _dizin(ctx, v)
    if (d / "segmentler.jsonl").is_file():
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
        return 0, _ozet_satir(d, meta, _oku(d), "önbellek")
    meta = _meta(ctx, d)
    (d / "linkler.json").write_text(json.dumps(m.urller(meta.get("description")), ensure_ascii=False), encoding="utf-8")
    secim = m.dil_sec(meta, dil)
    if not secim:
        return 3, [f"{v} · {(meta.get('title') or '?')[:80]}", f"altyazı yok → `video --whisper {v}` (CPU, açık bayrakla)"]
    anahtar, tur = secim
    for eski in d.glob("altyazi*"):
        eski.unlink()
    _yt(ctx, ["yt-dlp", "--skip-download", "--no-warnings", "--write-subs" if tur == "elle" else "--write-auto-subs", "--sleep-subtitles", "2",
              "--sub-langs", anahtar, "--sub-format", "vtt", "-o", str(d / "altyazi.%(ext)s"), v], SURE["altyazi"], d)
    vtt = next(d.glob("altyazi*.vtt"), None)
    if vtt is None:
        return 3, [f"{v}: altyazı indirilemedi → `video --whisper {v}`"]
    seg = m.segmentle(m.vtt_ayristir(vtt.read_text(encoding="utf-8")), meta.get("chapters"), meta.get("duration"))
    _yaz(d, seg)
    return 0, _ozet_satir(d, meta, seg, f"{anahtar} {tur}")


def _idler(ctx, hedefler):
    """URL/id/playlist'ler → (id'ler ≤LISTE_TAVAN, kalan, playlist var mı)."""
    ids, liste = [], False
    for h in hedefler:
        v = m.vid(h)
        if v is None:
            liste = True
            j = json.loads(_kos(ctx, ["yt-dlp", "--flat-playlist", "-J", "--no-warnings", h], SURE["meta"]))
            ids += [e["id"] for e in j.get("entries") or [] if e.get("id")]
        else:
            ids.append(v)
    ids = list(dict.fromkeys(ids))
    return ids[:LISTE_TAVAN], max(len(ids) - LISTE_TAVAN, 0), liste


def ozet(ns, ctx):
    ids, kalan, liste = _idler(ctx, ns.hedef)

    def bir(x):
        try:
            return _ozet_bir(ctx, x, ns.dil)
        except HizHata as e:
            return 4, [str(e)]
        except Hata as e:
            return 1, [f"{x}: {e}"]

    with ThreadPoolExecutor(ALTYAZI_ES) as ex:
        sonuc = list(ex.map(bir, ids))
    for _, satir in sonuc:
        print("\n".join(satir))
    if liste or kalan:
        print(f"playlist: {len(ids)} işlendi, kalan {kalan} (tavan {LISTE_TAVAN})")
    return max(rc for rc, _ in sonuc) if sonuc else 1


def _gonder_tavanli(ctx, tavan):
    """Tüm iş parçacıklarının ortak HTTP sayacı: tavan kilitle, ağa çıkmadan önce."""
    kilit, sayac = threading.Lock(), [0]

    def gonder(*a, **k):
        with kilit:
            if sayac[0] >= tavan:
                raise c.TavanHata(f"istek tavanı: {tavan} HTTP isteği doldu (--istek-tavan)")
            sayac[0] += 1
        return (ctx["gonder"] or c.http_gonder)(*a, **k)

    return gonder, sayac


def _suz(ctx, d, sorular, istek_tavan):
    """Yalnız p'si eksik (segment, soru) çiftleri sorulur; önbellekte p varsa istek yok. → (seg, bantlar, istek, tavan)"""
    if not sorular or set(sorular) - set(SORULAR):
        raise Hata(f"--sorular: {','.join(SORULAR)} içinden")
    seg, b = _oku(d), c.bantlar_oku()
    sor = [s for s in seg if any(f"p_{k}" not in s for k in sorular)]
    tavan = istek_tavan if istek_tavan is not None else len(seg) + 10
    if len(sor) > tavan:
        raise Hata(f"istek tavanı: {len(sor)} segment sorulacak, tavan {tavan} (--istek-tavan)")
    gonder, sayac = _gonder_tavanli(ctx, tavan)

    def bir(s):
        q = {k: SORULAR[k] for k in sorular if f"p_{k}" not in s}
        t = c.Tasiyici(env=ctx["env"], en_fazla=1, gonder=gonder, istek_tavan=tavan)
        cv = t.yargila([f"[{m.ss(s['bas'])}-{m.ss(s['son'])}] {s['metin']}"], q)[0]
        for k in q if cv else ():
            s[f"p_{k}"] = cv[k]["noul"]

    try:
        with ThreadPoolExecutor(SUZ_ES) as ex:
            list(ex.map(bir, sor))
    finally:
        for s in seg:
            if "p_arac" in s:  # yalnız "hayır" yönünde kesin olan atlanır; belirsiz okunur
                s["atla"] = s["p_arac"] < 0.5 and c.kesinlik({"type": "noul", "noul": s["p_arac"]}) >= b["act"]
        _yaz(d, seg)
    return seg, b, sayac[0], tavan


def suz(ns, ctx):
    seg, b, istek, tavan = _suz(ctx, ctx["kok"] / ns.id, ns.sorular.split(","), ns.istek_tavan)
    oku = [s for s in seg if not s.get("atla")]
    ekran = sorted((s for s in oku if s.get("p_ekran", 0) >= b["flag"]), key=lambda s: -s["p_ekran"])[:8]
    print(f"okunacak {len(oku)} · atlanan {len(seg) - len(oku)} · ~{sum(c.token(s['metin']) for s in oku)} token")
    print("ekran adayı: " + (", ".join(f"{m.ss((s['bas'] + s['son']) / 2)} ({s['p_ekran']:.2f})" for s in ekran) or "yok"))
    print(f"istek: {istek} (tavan {tavan})")
    return 0


def _sor(ctx, v, soru, kac):
    """→ (satırlar [(y, bant, s, metin)], istek, görüntü p'si yalnız Act ise, yoksa None). Tam 2 Jev isteği."""
    seg, b = _oku(ctx["kok"] / v), c.bantlar_oku()
    t = c.Tasiyici(env=ctx["env"], en_fazla=2, gonder=ctx["gonder"], istek_tavan=2)
    aday = [(f"s{s['i']}", f"[{m.ss(s['bas'])}] {s['metin'][:ADAY_KR]}") for s in seg if not s.get("atla")]
    q1 = {f"d{i}": {"type": "choice", "instructions": ASAMA1, "criteria": {**dict(dl), sk.HICBIRI: "Hiçbir kesit yanıtlamıyor."}}
          for i, dl in enumerate(sk.dilimle(aday))}
    cv = t.yargila([soru], {**q1, "goruntu": GORUNTU_Q})[0] or {}
    olas = {}
    for k, y in cv.items():
        for a, p in (y.get("probabilities") or {}).items() if k != "goruntu" else ():
            olas[a] = max(p, olas.get(a, 0.0))
    olas.pop(sk.HICBIRI, None)
    ilk = [a for a, p in sorted(olas.items(), key=lambda x: -x[1]) if p >= sk.ESIK1][:sk.ILK1]
    idx = {f"s{s['i']}": s for s in seg}
    ilk = [a for a in ilk if a in idx]
    satirlar = []
    if ilk:
        q2 = {f"a{n}": {"type": "noul", "instructions": ASAMA2, "criteria": {"true": idx[a]["metin"][:6000], "false": "Bu kesit soruyu yanıtlamıyor."}}
              for n, a in enumerate(ilk)}
        cv2 = t.yargila([soru], q2)[0] or {}
        sirali = sorted(((cv2[f"a{n}"], idx[a]) for n, a in enumerate(ilk) if f"a{n}" in cv2), key=lambda x: -x[0]["noul"])[:kac]
        butce = SOR_TOKEN
        for y, s in sirali:
            pay = max(butce // max(len(sirali) - len(satirlar), 1), 0)
            metin = s["metin"].encode()[:pay * 4].decode(errors="ignore")
            butce -= c.token(metin)
            satirlar.append((y, c.bant(c.kesinlik(y), b), s, metin))
    g = cv.get("goruntu")
    return satirlar, t.istek, g["noul"] if g and g["noul"] >= 0.5 and c.bant(c.kesinlik(g), b) == "Act" else None


def _sor_yaz(satirlar, istek):
    for y, bant, s, metin in satirlar:
        print(f"[{m.ss(s['bas'])}-{m.ss(s['son'])}] p={y['noul']:.2f} {bant} | {metin}")
    if not satirlar:
        print("eşleşen kesit yok")
    print(f"istek: {istek}")


def sor(ns, ctx):
    satirlar, istek, g = _sor(ctx, ns.id, ns.soru, ns.k)
    _sor_yaz(satirlar, istek)
    if g is not None:
        zaman = ",".join(m.ss((s["bas"] + s["son"]) / 2) for _, _, s, _ in satirlar[:3]) or m.ss(0)
        print(f"video kare {ns.id} --t {zaman}  (görüntü gerekli, p={g:.2f})")
    return 0


def izle(ns, ctx):
    """Desktop için tek çağrı: ozet (önbellekli) + sor + görüntü Act ise en iyi segmentin ortasından tek kare. suz yok → Jev ≤2."""
    v = m.vid(ns.hedef)
    if v is None:
        raise Hata("izle: tek video URL'si ya da id gerekli")
    rc, satir = _ozet_bir(ctx, v, None)
    print("\n".join(satir))
    if rc:
        return rc
    satirlar, istek, g = _sor(ctx, v, ns.soru, ns.k)
    _sor_yaz(satirlar, istek)
    if g is not None and satirlar:
        t = (satirlar[0][2]["bas"] + satirlar[0][2]["son"]) / 2
        for _, yol in _kareler(ctx, ctx["kok"] / v, [t], 0, GENISLIK, 1):
            print(f"kare: {yol.as_posix()} · {m.ss(t)} · ~{_kare_tk(yol)[1]} token (görüntü gerekli, p={g:.2f})")
    return 0


def paket(ns, ctx):
    """Alt ajan girdisi tek dosya <önbellek>/<id>/paket.md: künye · chapter · linkler · sadeleştirilmiş segmentler · kare yolları.
    Kareler: yalnız ekran sorusu (p varsa istek yok) → ekran p'si en yüksek --kare zamanın tam-t karesi. Segment metni stdout'a yazılmaz."""
    d = ctx["kok"] / ns.id
    seg, _, istek, _ = _suz(ctx, d, ["ekran"], ns.istek_tavan)
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    dil = m.dil_sec(meta)
    zamanlar = sorted((s["bas"] + s["son"]) / 2 for s in sorted(seg, key=lambda s: -s.get("p_ekran", 0))[:ns.kare])
    kareler = _kareler(ctx, d, zamanlar, 0, GENISLIK, len(zamanlar)) if zamanlar else []
    md = [f"# {ns.id} · {meta.get('title')} · {meta.get('channel')} · süre {m.ss(meta.get('duration') or 0)} · dil {dil[0] if dil else '?'}"
          f" · https://youtu.be/{ns.id}",
          "## Chapter", *([f"{m.ss(c_['start_time'])} {c_.get('title')}" for c_ in meta.get("chapters") or []] or ["yok"]),
          "## Linkler", *(m.urller(meta.get("description")) or ["yok"]),
          "## Segmentler", *[f"[{m.ss(s['bas'])}] {x}" for s in seg if (x := m.sadelestir(s["metin"]))],
          "## Kareler", *([f"{yol.as_posix()} · {m.ss(t)}" for t, yol in kareler] or ["yok"])]
    yol = d / "paket.md"
    yol.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"paket: {yol.as_posix()} · kareler: {' '.join(y.as_posix() for _, y in kareler) or 'yok'} · segment {len(seg)} · kare {len(kareler)} · ~{c.token(yol.read_text(encoding='utf-8'))} token metin"
          f" + ~{sum(_kare_tk(y)[1] for _, y in kareler)} kare · istek {istek}")
    return 0


def _akis_url(ctx, d):
    """Doğrudan akış URL'si; akis.url önbelleğinde, URL'deki expire'a 5 dk kalana dek geçerli. URL hiçbir çıktıya yazılmaz."""
    yol = d / "akis.url"
    if yol.is_file():
        url = yol.read_text(encoding="utf-8").strip()
        e = re.search(r"[?&/]expire[=/](\d+)", url)
        if e and int(e.group(1)) - 300 > time.time():
            return url
    out = _kos(ctx, ["yt-dlp", "-g", "--no-warnings", "-f", "bv*[height<=720][vcodec!=none]/b", d.name], SURE["meta"])
    url = out.decode("utf-8", "replace").strip().splitlines()[0]
    yol.write_text(url, encoding="utf-8")
    return url


def _kare_uret(ctx, d, url, t, pencere, g):
    """Tek zaman: ffmpeg girişte atlar (-ss -i'den önce). Önce tam t karesi; pencere>0 ise [t-p, t+p] sahne değişimleri ek. Video dosyası yok."""
    olcek = f"scale='min({g},iw)':-2,format=yuvj420p"  # mjpeg sınırlı-aralık YUV'u reddeder
    kd = d / "kareler"
    kd.mkdir(exist_ok=True)
    ad = f"k{int(t):05d}"
    for eski in kd.glob(f"{ad}_*.jpg"):
        eski.unlink()
    giris = ["ffmpeg", "-v", "error", "-y", "-rw_timeout", "15000000"]
    cagri = [giris + ["-ss", f"{t:g}", "-i", url, "-vf", olcek, "-frames:v", "1", "-q:v", "4", str(kd / f"{ad}_0.jpg")]]  # tam t hep ilk
    if pencere > 0:
        cagri.append(giris + ["-ss", f"{max(0.0, t - pencere):g}", "-t", f"{2 * pencere:g}", "-i", url, "-vf", f"select='gt(scene,0.3)',{olcek}",
                              "-fps_mode", "vfr", "-frames:v", "2", "-q:v", "4", str(kd / f"{ad}_%d.jpg")])
    try:
        for a in cagri:
            _kos(ctx, a, SURE["kesit"])
    except Hata as e:
        raise Hata(f"{m.ss(t)}: " + re.sub(r"https?://\S*", "<akış-url>", str(e))) from None  # _kos 200 krk'da keser: URL parçası da gider
    kareler = sorted(kd.glob(f"{ad}_*.jpg"))
    return kareler[:1], kareler[1:]


def kare(ns, ctx):
    d = _dizin(ctx, ns.id)
    if ns.suzgecten:
        seg = [s for s in _oku(d) if not s.get("atla")]
        if not any("p_ekran" in s for s in seg):
            raise Hata(f"ekran p'si yok: önce `video suz {ns.id}`")
        en = sorted(seg, key=lambda s: -s.get("p_ekran", 0))[:ns.en_fazla]
        zamanlar = sorted((s["bas"] + s["son"]) / 2 for s in en)
    elif ns.t:
        zamanlar = [m.sn(x) for x in ns.t.split(",") if x.strip()]
    else:
        raise Hata("--t 12:30,14:05 ya da --suzgecten gerekli")
    zamanlar = zamanlar[:ns.en_fazla]
    toplam = 0
    tut = _kareler(ctx, d, zamanlar, ns.pencere, min(ns.genislik, GENISLIK), ns.en_fazla)
    for t, yol in tut:
        gy, tk = _kare_tk(yol)
        toplam += tk
        print(f"{yol} · {m.ss(t)} · {gy[0]}x{gy[1]} · ~{tk} token")
    print(f"{len(tut)} kare · tahmini görsel ~{toplam} token · {len(zamanlar)} aralık akıştan okundu (video dosyası yazılmadı)")
    return 0


def _kare_tk(yol):
    gy = m.jpeg_boyut(yol.read_bytes())
    return gy, gy[0] * gy[1] // 750


def _kareler(ctx, d, zamanlar, pencere, g, en_fazla):
    """[(t, yol)] zamana göre: önce merkez kareler, kalan pay sahne karelerine; aHash ile tekrar ayıklanır."""
    url = _akis_url(ctx, d)
    merkezler, sahneler = [], []
    for t in zamanlar:
        mk, sh = _kare_uret(ctx, d, url, t, pencere, g)
        merkezler += [(t, x) for x in mk]
        sahneler += [(t, x) for x in sh]
    tut, hashler = [], []
    for t, yol in merkezler + sahneler:  # önce merkez kareler, kalan pay sahne karelerine
        if not yol.is_file():
            continue
        h = m.ahash(_kos(ctx, ["ffmpeg", "-v", "error", "-i", str(yol), "-vf", "scale=8:8,format=gray", "-f", "rawvideo", "-"], SURE["ffmpeg"]))
        if len(tut) >= en_fazla or any(bin(h ^ x).count("1") <= 5 for x in hashler):
            yol.unlink()
            continue
        hashler.append(h)
        tut.append((t, yol))
    return sorted(tut)


def oku(ns, ctx):
    """Alt ajan girdisi: künye · chapter · linkler · segmentler. Varsayılan tam: 12b'de süzgeçli geri çağırma %74 (<%90).
    --suzgecli: yalnız suz'un okunacak dediği segmentler. Ana ajan context'ine girmez."""
    d = ctx["kok"] / ns.id
    seg, meta = _oku(d), json.loads((d / "meta.json").read_text(encoding="utf-8"))
    linkler = json.loads((d / "linkler.json").read_text(encoding="utf-8")) if (d / "linkler.json").is_file() else []
    oku_ = [s for s in seg if not s.get("atla")] if ns.suzgecli else seg
    print(f"{ns.id} · {meta.get('title')} · {meta.get('channel')} · süre {m.ss(meta.get('duration') or 0)} · atlanan {len(seg) - len(oku_)}/{len(seg)}")
    print("chapter: " + (" · ".join(f"{m.ss(c_['start_time'])} {c_.get('title')}" for c_ in meta.get("chapters") or []) or "yok"))
    print("linkler: " + (" ".join(linkler) or "yok"))
    for s in oku_:
        print(f"[{m.ss(s['bas'])}-{m.ss(s['son'])}] {s['metin']}")
    return 0


def _tarama_dizin(ctx):
    return Path(ctx["env"].get("VIDEO_TARAMA_DIZIN") or TARAMA_DIZIN)


def _ev(ctx):
    return Path(ctx["env"].get("VIDEO_EV") or Path.home())


def kayit(ns, ctx):
    d = _tarama_dizin(ctx)
    yol = d / "kayit.jsonl"
    eski = tr.kayit_oku(yol)
    if ns.ice_al:
        gorulen = {k["id"] for k in eski}
        yeni = [g for g in tr.ice_al(d) if g["id"] not in gorulen]
        tr.kayit_yaz(yol, eski + yeni)
        print(f"içe alındı: {len(yeni)} video · adsız {sum(not g['adaylar'] for g in yeni)} · "
              f"{sum(len(g['adaylar']) for g in yeni)} aday ({sum(len(g['ele']) for g in yeni)} ELE) · {yol}")
        return 0
    if not ns.hedef:
        raise Hata("hedef ya da --ice-al gerekli")
    ids, kalan, _ = _idler(ctx, ns.hedef)
    tara, atla = tr.ayir(ids, eski, ns.yeniden)
    print("tara: " + (" ".join(tara) or "-"))
    print(f"atlandı: {len(atla)}" + (f" ({' '.join(atla)})" if atla else "") + (f" · liste kalanı {kalan}" if kalan else ""))
    for i, dl in enumerate(tr.dalgalar(tara), 1):
        print(f"dalga {i}: {' '.join(dl)}")
    return 0


def adlar(ns, ctx):
    sozluk = tr.sozluk_kur(_ev(ctx), tr.kayit_oku(_tarama_dizin(ctx) / "kayit.jsonl"))
    yol = ctx["kok"] / "adlar.json"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(json.dumps(sozluk, ensure_ascii=False), encoding="utf-8")
    say = {}
    for _, k in sozluk:
        say[k] = say.get(k, 0) + 1
    print(f"{len(sozluk)} ad · " + " · ".join(f"{k} {n}" for k, n in sorted(say.items())) + f" · {yol}")
    for a in ns.eslestir or []:
        e = tr.eslestir(a, sozluk)
        print(f"{a} → " + (f"{e[0]} ({e[1]}, {e[2]:.2f})" if e else "eşleşme yok"))
    return 0


def _sure(ctx, yol, metin):
    """Önbellekteki meta.json süresi; yoksa künyedeki `süre: m:ss`."""
    v, _ = tr.rapor_id(yol)
    meta = ctx["kok"] / (v or "?") / "meta.json"
    if v and meta.is_file():
        return json.loads(meta.read_text(encoding="utf-8")).get("duration")
    k = re.search(r"süre:?\s*((?:\d+:)?\d+:\d\d)", tr.bolum(metin, "Künye"))
    return m.sn(k[1]) if k else None


def _sozluk_doldur(ctx, yol, metin):
    """Aday satırında sözlük hücresi `?` ise ad sözlüğüyle yerinde doldurulur (alt ajanın `adlar` turu yerine)."""
    if not any(len(s) > 1 and s[1] == "?" for s in tr.aday_satirlari(metin)):
        return metin
    sozluk = tr.sozluk_kur(_ev(ctx), tr.kayit_oku(_tarama_dizin(ctx) / "kayit.jsonl"))

    def yaz(x):
        e = tr.eslestir(x[1], sozluk)
        return f"| {x[1]} | " + (f"{e[0]} ({e[1]}, {e[2]:.2f})" if e else "yok") + " |"
    metin = re.sub(r"^\|\s*([^|\n]+?)\s*\|\s*\?\s*\|", yaz, metin, flags=re.M)
    Path(yol).write_text(metin, encoding="utf-8")
    return metin


def rapor_denetle(ns, ctx):
    metin = _sozluk_doldur(ctx, ns.rapor, Path(ns.rapor).read_text(encoding="utf-8"))
    sure = _sure(ctx, ns.rapor, metin)
    h = tr.denetle(metin, sure)
    for x in h:
        print(x)
    print(f"rapor-denetle: {'GEÇTİ' if not h else f'{len(h)} hata'}" + ("" if sure else " (süre bilinmiyor: zaman denetimi atlandı)"))
    return 1 if h else 0


def kurallar(ns, ctx):
    yollar, on = tr.kural_kaynaklari(ctx["env"], _ev(ctx)), ctx["kok"] / "kurallar.json"
    k = tr.kurallar(yollar, on)
    for y in yollar:
        kisa = tr.kural_kisa(y)
        print(f"{kisa} · " + (f"{sum(a.startswith(kisa + ':') for a, _ in k)} kural" if y.is_file() else "yok") + f" · {y}")
    print(f"{len(k)} kural · önbellek: {on}")
    return 0


def toplu(ns, ctx):
    from types import SimpleNamespace

    from jev import cli as jc
    d = _tarama_dizin(ctx)
    yol = d / "kayit.jsonl"
    raporlar, adaylar, gecen = [], [], set()
    for r in ns.raporlar:
        v, _ = tr.rapor_id(r)
        metin = Path(r).read_text(encoding="utf-8")
        if not tr.denetle(metin, _sure(ctx, r, metin)):  # kayda yalnız rapor-denetle'den geçen
            gecen.add(v)
        baslik = next((s[2:].strip() for s in metin.splitlines() if s.startswith("# ")), "?")
        satir = tr.aday_satirlari(metin)
        raporlar.append((v, Path(r), baslik, list(dict.fromkeys(s[0] for s in satir))))
        adaylar += [{"ad": s[0], "video": v, "tur": s[2] if len(s) > 2 else "?", "ne": s[4] if len(s) > 4 else ""} for s in satir]
    ids = {v for v, *_ in raporlar}
    kayit = tr.kayit_oku(yol)
    sozluk = tr.sozluk_kur(_ev(ctx), [k for k in kayit if k["id"] not in ids])
    tek = tr.tekille(adaylar)
    ip = [x for x in tek if x["tur"] in tr.KURAL_TUR]
    tavan = ns.istek_tavan or 2 * len(tek) + 2 + 2 * len(ip)
    jy, istek = {}, 0
    if ip:  # önce kural: kuralda olan ipucu ÇİFT, jev taramaya girmez
        kl = tr.kurallar(tr.kural_kaynaklari(ctx["env"], _ev(ctx)), ctx["kok"] / "kurallar.json")
        tk = c.Tasiyici(env=ctx["env"], en_fazla=2 * len(ip), gonder=ctx["gonder"], istek_tavan=min(tavan, 2 * len(ip)))
        for x in ip:
            x["kural"] = tr.kural_esle(tk, f"İPUCU: {x['ad']}\n{x['tur']}: {x['ne']}", kl)
        istek = tk.istek
    sor = [x for x in tek if not x.get("kural")]
    if sor:
        gecici = ctx["kok"] / "tarama-adaylar.json"
        gecici.parent.mkdir(parents=True, exist_ok=True)
        gecici.write_text(json.dumps([{"ad": x["ad"], "aciklama": f"{x['tur']}: {x['ne']}"} for x in sor], ensure_ascii=False), encoding="utf-8")
        t = c.Tasiyici(env=ctx["env"], en_fazla=2, gonder=ctx["gonder"], istek_tavan=tavan - istek)  # jev tarama ≤2 batch
        _, sat = jc.tarama(SimpleNamespace(dosya=str(gecici)), lambda: t, None)
        jy = {r[0]: (float(r[1]) if r[1] != "-" else None, float(r[2]) if r[2] != "-" else None) for r in sat}
        istek += t.istek
    bugun = time.strftime("%Y-%m-%d")
    for x in tek:
        x["es"] = tr.eslestir(x["ad"], sozluk)
        x["cift"], x["risk"] = jy.get(x["ad"], (None, None))
        x["isaret"] = "ÇİFT" if x.get("kural") else tr.isaret(x["es"], x["cift"], x["risk"])
        x["etiket"] = x["isaret"] + (f" (kural: {x['kural']})" if x.get("kural") else "")
    isr = {tr.normal(x["ad"]): x["etiket"] for x in tek}
    cikti = d / f"{bugun}-toplu.md"
    md = [f"# Video tarama toplu — {bugun}", "", f"{len(raporlar)} video · {len(tek)} tekil aday · Jev tarama isteği {istek}", "",
          "| aday | işaret | sözlük eşleşmesi | çift p | izin riski (0-3) | tür | videolar |", "|---|---|---|---|---|---|---|"]
    for x in tek:
        es = f"{x['es'][0]} ({x['es'][1]}, {x['es'][2]:.2f})" if x["es"] else "yok"
        md.append(f"| {x['ad']} | {x['etiket']} | {es} | {'-' if x['cift'] is None else x['cift']} | "
                  f"{'-' if x['risk'] is None else x['risk']} | {x['tur']} | {', '.join(x['videolar'])} |")
    md += ["", "## Raporlar"] + [f"- {v} · {b} · {r.name}" for v, r, b, _ in raporlar]
    cikti.write_text("\n".join(md) + "\n", encoding="utf-8")
    kayit = [k for k in kayit if k["id"] not in gecen] + [{"id": v, "tarih": bugun, "rapor": r.name, "adaylar": a, "ele": []}
                                                          for v, r, _, a in raporlar if v in gecen]
    tr.kayit_yaz(yol, kayit)
    for v, _, b, a in raporlar[:20]:
        print(f"{v} · {b[:50]} · {len(a)} aday: " + ", ".join(f"{x} [{isr[tr.normal(x)]}]" for x in a)[:300])
    say = {}
    for x in tek:
        say[x["isaret"]] = say.get(x["isaret"], 0) + 1
    print(f"{len(tek)} tekil aday · " + " · ".join(f"{k} {n}" for k, n in sorted(say.items())) + f" · Jev istek {istek}")
    print(f"rapor: {cikti} · kayıt: {len(kayit)} video" + (f" · kayda yazılmadı (rapor-denetle): {' '.join(sorted(ids - gecen))}" if ids - gecen else ""))
    return 0


def whisper(ns, ctx):
    d = _dizin(ctx, ns.id)
    if (d / "segmentler.jsonl").is_file():
        print(f"altyazı zaten var: {d / 'segmentler.jsonl'} (whisper gereksiz)")
        return 0
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(WHISPER_KUR)
        return 2
    meta = _meta(ctx, d)
    sure, tavan = meta.get("duration") or 0, ns.en_fazla_dk * 60
    args = ["yt-dlp", "--no-warnings", "-f", "ba/b", "-o", str(d / "ses.%(ext)s")]
    if not sure or sure > tavan:
        args += ["--download-sections", f"*0-{tavan}"]
    try:
        _kos(ctx, args + [ns.id], SURE["ses"])
        ses = next(d.glob("ses.*"), None)
        if ses is None:
            raise Hata("ses inmedi")
        parcalar, _ = WhisperModel(ns.model, device="cpu", compute_type="int8").transcribe(str(ses))
        satirlar = [(round(p.start, 3), p.text.strip()) for p in parcalar if p.text.strip()]
    finally:
        for s in d.glob("ses.*"):
            s.unlink()
    seg = m.segmentle(satirlar, meta.get("chapters"), min(sure, tavan) if sure else None)
    _yaz(d, seg)
    print("\n".join(_ozet_satir(d, meta, seg, f"whisper {ns.model}" + (f", ilk {ns.en_fazla_dk} dk" if not sure or sure > tavan else ""))))
    return 0


def temizle(ns, ctx):
    sinir, n = time.time() - ns.gun * 86400, 0
    for d in ctx["kok"].iterdir() if ctx["kok"].is_dir() else []:
        if d.is_dir() and d.stat().st_mtime < sinir:
            shutil.rmtree(d)
            n += 1
    print(f"{n} video klasörü silindi ({ns.gun} günden eski) · {ctx['kok']}")
    return 0


def main(argv=None, env=None, kos=kos, gonder=None, uyku=time.sleep):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--whisper"]:
        argv[0] = "whisper"
    p = argparse.ArgumentParser(prog="video", description=__doc__)
    alt = p.add_subparsers(dest="komut", required=True)
    x = alt.add_parser("ozet", help="meta · chapter · linkler · altyazı → segmentler.jsonl; video başına ≤6 satır")
    x.add_argument("hedef", nargs="+", help="URL, id ya da playlist (çoklu, ≤4 eşzamanlı)")
    x.add_argument("--dil", help="altyazı dili (varsayılan tr, sonra en)")
    x = alt.add_parser("suz", help="segment başına Jev: araç anlatımı mı · ekranda mı; kesin-hayır atlanır")
    x.add_argument("id")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M HTTP isteği (varsayılan segment+10)")
    x.add_argument("--sorular", default="arac,ekran", help="arac,ekran ya da yalnız biri; p'si olan sorulmaz")
    x = alt.add_parser("paket", help="alt ajan girdisi tek dosya: künye · chapter · linkler · sade segmentler · kareler (yalnız ekran sorusu)")
    x.add_argument("id")
    x.add_argument("--kare", type=int, default=6, help="en fazla N kare (ekran p'si en yüksek)")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M HTTP isteği (varsayılan segment+10)")
    x = alt.add_parser("izle", help="Desktop tek çağrı: ozet + sor + görüntü gerekirse tek kare (Jev ≤2)")
    x.add_argument("hedef")
    x.add_argument("soru")
    x.add_argument("-k", type=int, default=3)
    x = alt.add_parser("sor", help="soruya en ilgili k segment (2 Jev isteği)")
    x.add_argument("id")
    x.add_argument("soru")
    x.add_argument("-k", type=int, default=5)
    x = alt.add_parser("kare", help="akış URL'sinden giriş-atlamalı kare; video dosyası yazılmaz")
    x.add_argument("id")
    x.add_argument("--t", help="12:30,14:05")
    x.add_argument("--suzgecten", action="store_true", help="suz'un ekran p'si en yüksek zamanlar")
    x.add_argument("--pencere", type=float, default=8)
    x.add_argument("--genislik", type=int, default=GENISLIK)
    x.add_argument("--en-fazla", type=int, default=6)
    x = alt.add_parser("whisper", help="altyazı yoksa CPU transkript (faster-whisper)")
    x.add_argument("id")
    x.add_argument("--model", default="small")
    x.add_argument("--en-fazla-dk", type=int, default=20)
    x = alt.add_parser("oku", help="alt ajan girdisi: künye · chapter · linkler · segmentler (varsayılan tam)")
    x.add_argument("id")
    x.add_argument("--suzgecli", action="store_true", help="yalnız suz'un okunacak dediği segmentler (12b: geri çağırma %%74, varsayılan kapalı)")
    x = alt.add_parser("kayit", help="kayit.jsonl'deki id'leri atlar; tara · atlandı · ≤3'lük alt ajan dalgaları")
    x.add_argument("hedef", nargs="*")
    x.add_argument("--yeniden", action="store_true", help="kayıttakileri de tara")
    x.add_argument("--ice-al", action="store_true", help="docs/video-tarama/*.md eski raporlarından id + aday adları (bir kez)")
    x = alt.add_parser("adlar", help="ad sözlüğü: skill katalogu · plugin · MCP · kayıt · ELE → önbellek; --eslestir bulanık eşleşme")
    x.add_argument("--eslestir", nargs="+", metavar="AD")
    x = alt.add_parser("rapor-denetle", help="bölümler · süre içi zaman · aday alanları · alıntı ≤15 kelime")
    x.add_argument("rapor")
    x = alt.add_parser("toplu", help="raporların adaylarını tekiller, sözlük + jev tarama (≤2 batch) ile işaretler; toplu rapor + kayıt")
    x.add_argument("raporlar", nargs="+")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M Jev HTTP isteği (varsayılan 2·aday+2+2·ipucu)")
    alt.add_parser("kurallar", help="kural kaynakları (~/.claude/CLAUDE.md + repo süreç dokümanları ya da VIDEO_KURALLAR) → madde önbelleği (mtime)")
    x = alt.add_parser("katman", help="aday.md → T0 kural · T1 yalnız-md skill · T2 onay · RED; uygular, docs/kurulumlar/kayit.jsonl")
    x.add_argument("adaylar", nargs="+")
    x.add_argument("--yeniden", action="store_true", help="kayıttaki adları da değerlendir")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M Jev isteği (varsayılan 7·aday)")
    x = alt.add_parser("bizde", help="aday.md → jev skill (2 istek/aday); p≥act skill'ler ## Bizde durum'a")
    x.add_argument("adaylar", nargs="+")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M Jev isteği (varsayılan 2·aday)")
    x = alt.add_parser("kural-onay", help="bekleyen/kural-<slug>.md → omer-kurallar.md'ye madde (çiftse eklenmez); yalnız CC, köprüde yok")
    x.add_argument("slug")
    x = alt.add_parser("onay", help="bekleyen/<ad>.md yapılandırılmış adımlar → kur · duman · başarısızsa geri alma; yalnız CC, köprüde yok")
    x.add_argument("ad")
    x.add_argument("--kuru", action="store_true", help="hiçbir şey koşmaz, planı yazar")
    x = alt.add_parser("geri-al", help="kayıttaki geri_alma adımları + köprü girdisini çıkarır; yalnız CC")
    x.add_argument("ad")
    x = alt.add_parser("dene", help="docs/denemeler/<ad>.md → claude -p A/B (sonnet) + Jev kalite; yalnız CC")
    x.add_argument("ad")
    x.add_argument("--tavan", type=int, default=6, help="en fazla N claude -p (görev×2)")
    x.add_argument("--istek-tavan", type=int, default=12, metavar="M", help="en fazla M Jev isteği")
    alt.add_parser("durum", help="docs/durum.md: köprü katalogu · son kararlar · ölçüm bulguları · ELE (≤3k token, elle bölüm korunur)")
    x = alt.add_parser("bilgi", help="bilgi/ kartları: guven · bayatlama · iddia")
    x.add_argument("--bayat", action="store_true", help="yalnız bayatlamış (yeniden doğrula)")
    alt.add_parser("projeler", help="docs/projeler.md: proje CLAUDE.md'lerinden 1-2 satır özet (mtime'la yenilenir)")
    x = alt.add_parser("temizle", help="eski önbellek klasörlerini siler")
    x.add_argument("--gun", type=int, default=14)
    ns = p.parse_args(argv)
    env = os.environ if env is None else env
    ctx = {"env": env, "kos": kos, "gonder": gonder, "uyku": uyku, "kok": Path(env.get("VIDEO_CACHE") or KOK)}
    try:
        return {"ozet": ozet, "suz": suz, "sor": sor, "kare": kare, "whisper": whisper, "temizle": temizle, "kayit": kayit, "adlar": adlar, "oku": oku, "paket": paket, "izle": izle,
                "rapor-denetle": rapor_denetle, "toplu": toplu, "kurallar": kurallar, "katman": uy.katman, "projeler": uy.projeler,
                "bizde": uy.bizde, "kural-onay": uy.kural_onay, "onay": kur.onay, "geri-al": kur.geri_al, "dene": kur.dene, "durum": og.durum, "bilgi": og.bilgi}[ns.komut](ns, ctx)
    except HizHata as e:
        print(f"hata: {e}")
        return 4
    except (Hata, c.JevHata) as e:
        print(f"hata: {e}")
        return 1


def calistir():
    for akis in (sys.stdout, sys.stderr):
        akis.reconfigure(encoding="utf-8")
    sys.exit(main())
