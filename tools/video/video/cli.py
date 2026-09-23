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

from . import metin as m

KOK = r"C:\Projeler\.video-cache"
LISTE_TAVAN, ALTYAZI_ES, SUZ_ES = 8, 4, 8
SOR_TOKEN, ADAY_KR = 2_500, 400
GENISLIK = 768
SURE = {"meta": 120, "altyazi": 120, "kesit": 120, "ffmpeg": 60, "ses": 900}
ARAC_Q = {"type": "noul", "instructions": "Bu video kesiti (state) bir araç, skill, MCP, CLI, teknik ya da iş akışı anlatıyor mu?",
          "criteria": {"true": "Somut bir araç/teknik/iş akışı anlatılıyor.", "false": "Sohbet, giriş, reklam, genel yorum; araç anlatımı yok."}}
EKRAN_Q = {"type": "noul", "instructions": "Kesitte anlatılan şey ekranda gösteriliyor mu (komut, ayar, arayüz)?",
           "criteria": {"true": "Konuşma ekrandaki komut/ayar/arayüze atıf yapıyor (şuraya tıklayın, burada görüyorsunuz…).",
                        "false": "Yalnız sözlü anlatım; ekrana bakmak gerekmiyor."}}
GORUNTU_Q = {"type": "noul", "instructions": "Bu soruyu (state) yanıtlamak için videonun görüntüsüne (ekran, komut, arayüz) bakmak gerekir mi?",
             "criteria": {"true": "Yanıt ekranda görünen ayrıntıya bağlı.", "false": "Altyazı metni yeterli."}}
ASAMA1 = "Kullanıcının sorusu (state) videonun hangi kesitinde yanıtlanıyor? Hiçbiri değilse 'hiçbiri'."
ASAMA2 = "Kullanıcının sorusu (state) şu video kesitinde yanıtlanıyor mu? Kesit metni criteria.true içinde."
WHISPER_KUR = "faster-whisper kurulu değil. Kur: uv tool install -e tools/video --with faster-whisper"


def kos(args, timeout=120):
    r = subprocess.run(args, capture_output=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


class Hata(Exception):
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
    j = json.loads(_kos(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", d.name], SURE["meta"]))
    alan = ("id", "title", "channel", "duration", "chapters", "description", "subtitles", "automatic_captions")
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
    for eski in d.glob("altyazi*.vtt"):
        eski.unlink()
    _kos(ctx, ["yt-dlp", "--skip-download", "--no-warnings", "--write-subs" if tur == "elle" else "--write-auto-subs",
               "--sub-langs", anahtar, "--sub-format", "vtt", "-o", str(d / "altyazi.%(ext)s"), v], SURE["altyazi"])
    vtt = next(d.glob("altyazi*.vtt"), None)
    if vtt is None:
        return 3, [f"{v}: altyazı indirilemedi → `video --whisper {v}`"]
    seg = m.segmentle(m.vtt_ayristir(vtt.read_text(encoding="utf-8")), meta.get("chapters"), meta.get("duration"))
    _yaz(d, seg)
    return 0, _ozet_satir(d, meta, seg, f"{anahtar} {tur}")


def ozet(ns, ctx):
    v = m.vid(ns.hedef)
    ids, kalan = [v], 0
    if v is None:
        j = json.loads(_kos(ctx, ["yt-dlp", "--flat-playlist", "-J", "--no-warnings", ns.hedef], SURE["meta"]))
        hepsi = [e["id"] for e in j.get("entries") or [] if e.get("id")]
        ids, kalan = hepsi[:LISTE_TAVAN], max(len(hepsi) - LISTE_TAVAN, 0)

    def bir(x):
        try:
            return _ozet_bir(ctx, x, ns.dil)
        except Hata as e:
            return 1, [f"{x}: {e}"]

    with ThreadPoolExecutor(ALTYAZI_ES) as ex:
        sonuc = list(ex.map(bir, ids))
    for _, satir in sonuc:
        print("\n".join(satir))
    if v is None:
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


def suz(ns, ctx):
    d = ctx["kok"] / ns.id
    seg, b = _oku(d), c.bantlar_oku()
    sor = [s for s in seg if "p_arac" not in s]
    tavan = ns.istek_tavan if ns.istek_tavan is not None else len(seg) + 10
    if len(sor) > tavan:
        raise Hata(f"istek tavanı: {len(sor)} segment sorulacak, tavan {tavan} (--istek-tavan)")
    gonder, sayac = _gonder_tavanli(ctx, tavan)
    q = {"arac": ARAC_Q, "ekran": EKRAN_Q}

    def bir(s):
        t = c.Tasiyici(env=ctx["env"], en_fazla=1, gonder=gonder, istek_tavan=tavan)
        cv = t.yargila([f"[{m.ss(s['bas'])}-{m.ss(s['son'])}] {s['metin']}"], q)[0]
        if cv:
            s["p_arac"], s["p_ekran"] = cv["arac"]["noul"], cv["ekran"]["noul"]

    try:
        with ThreadPoolExecutor(SUZ_ES) as ex:
            list(ex.map(bir, sor))
    finally:
        for s in seg:
            if "p_arac" in s:  # yalnız "hayır" yönünde kesin olan atlanır; belirsiz okunur
                s["atla"] = s["p_arac"] < 0.5 and c.kesinlik({"type": "noul", "noul": s["p_arac"]}) >= b["act"]
        _yaz(d, seg)
    oku = [s for s in seg if not s.get("atla")]
    ekran = sorted((s for s in oku if s.get("p_ekran", 0) >= b["flag"]), key=lambda s: -s["p_ekran"])[:8]
    print(f"okunacak {len(oku)} · atlanan {len(seg) - len(oku)} · ~{sum(c.token(s['metin']) for s in oku)} token")
    print("ekran adayı: " + (", ".join(f"{m.ss((s['bas'] + s['son']) / 2)} ({s['p_ekran']:.2f})" for s in ekran) or "yok"))
    print(f"istek: {sayac[0]} (tavan {tavan})")
    return 0


def sor(ns, ctx):
    d = ctx["kok"] / ns.id
    seg, b = _oku(d), c.bantlar_oku()
    t = c.Tasiyici(env=ctx["env"], en_fazla=2, gonder=ctx["gonder"], istek_tavan=2)
    aday = [(f"s{s['i']}", f"[{m.ss(s['bas'])}] {s['metin'][:ADAY_KR]}") for s in seg if not s.get("atla")]
    q1 = {f"d{i}": {"type": "choice", "instructions": ASAMA1, "criteria": {**dict(dl), sk.HICBIRI: "Hiçbir kesit yanıtlamıyor."}}
          for i, dl in enumerate(sk.dilimle(aday))}
    cv = t.yargila([ns.soru], {**q1, "goruntu": GORUNTU_Q})[0] or {}
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
        cv2 = t.yargila([ns.soru], q2)[0] or {}
        sirali = sorted(((cv2[f"a{n}"], idx[a]) for n, a in enumerate(ilk) if f"a{n}" in cv2), key=lambda x: -x[0]["noul"])[:ns.k]
        butce = SOR_TOKEN
        for y, s in sirali:
            pay = max(butce // max(len(sirali) - len(satirlar), 1), 0)
            metin = s["metin"].encode()[:pay * 4].decode(errors="ignore")
            butce -= c.token(metin)
            satirlar.append(s)
            print(f"[{m.ss(s['bas'])}-{m.ss(s['son'])}] p={y['noul']:.2f} {c.bant(c.kesinlik(y), b)} | {metin}")
    if not satirlar:
        print("eşleşen kesit yok")
    g = cv.get("goruntu")
    print(f"istek: {t.istek}")
    if g and g["noul"] >= 0.5 and c.bant(c.kesinlik(g), b) == "Act":
        zaman = ",".join(m.ss((s["bas"] + s["son"]) / 2) for s in satirlar[:3]) or m.ss(0)
        print(f"video kare {ns.id} --t {zaman}  (görüntü gerekli, p={g['noul']:.2f})")
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
    """Tek zaman: ffmpeg girişte atlar (-ss -i'den önce), yalnız [t-p, t+p] okunur; ilk kare + sahne değişimleri. Video dosyası yok."""
    olcek = f"scale='min({g},iw)':-2,format=yuvj420p"  # mjpeg sınırlı-aralık YUV'u reddeder
    kd = d / "kareler"
    kd.mkdir(exist_ok=True)
    ad = f"k{int(t):05d}"
    for eski in kd.glob(f"{ad}_*.jpg"):
        eski.unlink()
    giris = ["ffmpeg", "-v", "error", "-y", "-rw_timeout", "15000000"]
    if pencere > 0:
        giris += ["-ss", f"{max(0.0, t - pencere):g}", "-t", f"{2 * pencere:g}", "-i", url,
                  "-vf", f"select='eq(n,0)+gt(scene,0.3)',{olcek}", "-fps_mode", "vfr", "-frames:v", "3"]
    else:
        giris += ["-ss", f"{t:g}", "-i", url, "-vf", olcek, "-frames:v", "1"]
    try:
        _kos(ctx, giris + ["-q:v", "4", str(kd / f"{ad}_%d.jpg")], SURE["kesit"])
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
    g = min(ns.genislik, GENISLIK)
    url = _akis_url(ctx, d)
    merkezler, sahneler = [], []
    for t in zamanlar:
        mk, sh = _kare_uret(ctx, d, url, t, ns.pencere, g)
        merkezler += [(t, x) for x in mk]
        sahneler += [(t, x) for x in sh]
    tut, hashler = [], []
    for t, yol in merkezler + sahneler:  # önce merkez kareler, kalan pay sahne karelerine
        if not yol.is_file():
            continue
        h = m.ahash(_kos(ctx, ["ffmpeg", "-v", "error", "-i", str(yol), "-vf", "scale=8:8,format=gray", "-f", "rawvideo", "-"], SURE["ffmpeg"]))
        if len(tut) >= ns.en_fazla or any(bin(h ^ x).count("1") <= 5 for x in hashler):
            yol.unlink()
            continue
        hashler.append(h)
        tut.append((t, yol))
    toplam = 0
    for t, yol in sorted(tut):
        gy = m.jpeg_boyut(yol.read_bytes())
        tk = gy[0] * gy[1] // 750
        toplam += tk
        print(f"{yol} · {m.ss(t)} · {gy[0]}x{gy[1]} · ~{tk} token")
    print(f"{len(tut)} kare · tahmini görsel ~{toplam} token · {len(zamanlar)} aralık akıştan okundu (video dosyası yazılmadı)")
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


def main(argv=None, env=None, kos=kos, gonder=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["--whisper"]:
        argv[0] = "whisper"
    p = argparse.ArgumentParser(prog="video", description=__doc__)
    alt = p.add_subparsers(dest="komut", required=True)
    x = alt.add_parser("ozet", help="meta · chapter · linkler · altyazı → segmentler.jsonl; video başına ≤6 satır")
    x.add_argument("hedef", help="URL, id ya da playlist")
    x.add_argument("--dil", help="altyazı dili (varsayılan tr, sonra en)")
    x = alt.add_parser("suz", help="segment başına Jev: araç anlatımı mı · ekranda mı; kesin-hayır atlanır")
    x.add_argument("id")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M HTTP isteği (varsayılan segment+10)")
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
    x = alt.add_parser("temizle", help="eski önbellek klasörlerini siler")
    x.add_argument("--gun", type=int, default=14)
    ns = p.parse_args(argv)
    env = os.environ if env is None else env
    ctx = {"env": env, "kos": kos, "gonder": gonder, "kok": Path(env.get("VIDEO_CACHE") or KOK)}
    try:
        return {"ozet": ozet, "suz": suz, "sor": sor, "kare": kare, "whisper": whisper, "temizle": temizle}[ns.komut](ns, ctx)
    except (Hata, c.JevHata) as e:
        print(f"hata: {e}")
        return 1


def calistir():
    for akis in (sys.stdout, sys.stderr):
        akis.reconfigure(encoding="utf-8")
    sys.exit(main())
