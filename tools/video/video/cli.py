"""video — kademeli izleme: ozet → sor/suz → kare → whisper. Ham altyazı ve kareler önbellekte (repo dışı), ajana kompakt çıktı.
Jev isteği yalnız suz/sor'da ve tavanlı; önbellek varsa ağa çıkılmaz."""
import argparse
import difflib
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

from . import altin as au
from . import departman as dp
from . import getir as gt
from . import kanal as kn
from . import kur
from . import metin as m
from . import ogren as og
from . import parti as pt
from . import tarama as tr
from . import uygula as uy

KOK = r"C:\Projeler\.video-cache"
TARAMA_DIZIN = Path(__file__).resolve().parents[3] / "docs" / "video-tarama"
LISTE_TAVAN, ALTYAZI_ES, SUZ_ES = 8, 4, 8
SOR_TOKEN, ADAY_KR = 2_500, 400
GENISLIK = 768
GERI_CEKIL, HIZ_DK = (20, 60), 15  # 429: iki tekrar, sonra kullanıcıya bekleme süresi
SURE = {"meta": 120, "altyazi": 120, "kesit": 120, "ffmpeg": 60, "ses": 900, "sahne": 1800, "ocr": 600}
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
WHISPER_PARCA = 1200  # ayar · C1: whisper parça boyu (sn); yarıda kalırsa kaldığı parçadan sürer


def kos(args, timeout=120, env=None):
    args = [shutil.which(args[0]) or args[0], *args[1:]]  # MÜKEMMEL-7: Windows'ta npm .cmd sarmalayıcısı (mcporter.cmd) uzantısız bulunmaz
    r = subprocess.run(args, capture_output=True, timeout=timeout, env=env)
    return r.returncode, r.stdout, r.stderr


class Hata(Exception):
    pass


class HizHata(Hata):
    pass


def yt_url(vid):
    """yt-dlp'ye kimlik hiç çıplak verilmez: tireli kimlik (-_S3KD0ZIfI) seçenek sanılır."""
    return vid if vid.startswith(("http://", "https://")) else f"https://www.youtube.com/watch?v={vid}"


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
    j = json.loads(_yt(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", yt_url(d.name)], SURE["meta"], d))
    alan = ("id", "title", "language", "channel", "channel_id", "channel_url", "duration", "chapters", "description", "subtitles", "automatic_captions")
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
              "--sub-langs", anahtar, "--sub-format", "vtt", "-o", str(d / "altyazi.%(ext)s"), yt_url(v)], SURE["altyazi"], d)
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


SHORT_SN, SHORT_KARE, IPUCU_KARE = 120, 3, 8  # 24e-2 K3: kuyruk.md short (<2 dk) → kare ≤3 · DERİNLİK-1 R4: altyazıda repo/link/prompt → ≤8


def kare_tavan(sure, n, metin=""):
    return min(n, IPUCU_KARE if tr.IPUCU.search(metin) else SHORT_KARE) if 0 < sure < SHORT_SN else n


ISARET = re.compile(r"\b(?:ekran|screen|repo|github|link|url|https?://|komut|command|terminal|prompt|ayar|setting|config)", re.I)  # C2: altyazıda ekrana/repoya/linke/komuta/prompta/ayara işaret
SAHNE_ESIK = 0.3
OCR_PS = Path(__file__).with_name("ocr.ps1")
MONTAJ_SN = 5  # ayar · C5: bu pencerede ≥3 sahne kesimi → hızlı kurgu (montaj)
OCR_BENZER, DHASH_SAHNE = 0.9, 10  # ayar · O11 (3): katlanmış OCR metni benzerliği ≥ → tekrar · aynı sahnede dHash Hamming ≤ → tekrar
ADAY_UST = 150  # ayar · O11 (5): paket aday kare üst sınırı (merkez + işaret + tüm sahneler); aşan sahneler skor sırasıyla "aday tavanı"
OCR_AZ, OCR_KISA, OCR_KOD, OCR_GUVEN = 40, 12, 0.3, 0.7  # C3: <40 krk şema/görsel · satır ort. <12 krk arayüz · kod satırı
# ≥%30 · anlamlı oran <0.7 → kare modele · uzun videoda her 60 sn'ye bir sahne adayı (en az 2×kare)
PAKET_BUTCE = 40_000  # ayar · C4: video başına paket jetonu (segment metni + modele giden kareler; parti GIRDI_TAVAN ile aynı); aşan kare "incelenmedi"
KOMUT = re.compile(r"https?://|www\.|\b(?:npx|npm|pip|uvx?|claude|git|gh|curl|winget|brew)\b|--\w", re.I)
TEKNIK = re.compile(KOMUT.pattern + r"|\b[\w.-]+/[\w.-]+|^\s*/\w", re.I)
KOD = re.compile(r"[{};]|=>|==|\w\(|^\s*(?:def|function|import|from|const|let|var|class|return)\b")
TR_HARF = re.compile(r"[çğışöüÇĞİŞÖÜ]")
KATLA = str.maketrans("şıİüöçğŞÜÖÇĞ", "siIuocgSUOCG")
OCR_TR_IPUCU = {"ve", "bir", "icin", "ile", "bu", "da", "de", "olarak", "gibi", "ama", "veya", "cok", "daha", "su", "ne"}  # ayar · katlanmış
OCR_YAYGIN = OCR_TR_IPUCU | {"the", "to", "how", "what", "and", "for", "with", "you", "your", "this", "that", "will", "can", "not", "see", "use",
                             "run", "new"}  # ayar · gürültü: ≥5 harfli kelime yoksa satır bunlardan birini taşımalı


def _kat(s):
    """C3 düzeltme: aksan katlanır (ş→s ı→i İ→I ü→u ö→o ç→c ğ→g), harf büyüklüğü yok sayılır."""
    return s.translate(KATLA).lower()


def _ocr_gurultu(s):
    """C3 düzeltme: anlamlı kelime yok (≥5 harf ya da OCR_YAYGIN) ya da anlamsız oranı > 1 - OCR_GUVEN → pakete yazılmaz; komut/URL ve kod
    satırı korunur. ponytail: sözlük yok; kısa gerçek satır ("Save", "kith add") ayırt edilemez, yaygın listesi ayarda."""
    if KOMUT.search(s) or KOD.search(s):
        return False
    return not any(len(w) >= 5 or _kat(w) in OCR_YAYGIN for w in re.findall(r"[^\W\d_]+", s)) or m.anlamsiz_oran(s) > 1 - OCR_GUVEN


def _ocr_birlestir(tr_, en):
    """C3: tr ve en satırları ([metin, x0, y0, x1, y1]) kutu örtüşmesiyle eşlenir. URL/komut/kod → en, Türkçe ipucu kelimesi → tr, aksan
    katlanınca aynı → en (O10: "üşer" → user), Türkçe harf → tr, değilse anlamlı
    oranı yüksek olan (Windows OCR güven puanı vermez: vekil m.anlamsiz_oran; eşitte en). Eşsiz satır olduğu gibi; sıra yukarıdan aşağı."""
    ortus = lambda a, b: a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]  # noqa: E731
    kalan, cikti = list(en), []
    for a in tr_:
        b = next((b for b in kalan if ortus(a, b)), None)
        if b is None:
            cikti.append((a[2], a[0]))
            continue
        kalan.remove(b)
        x, y = a[0], b[0]
        s = (y if TEKNIK.search(x) or TEKNIK.search(y) else x if OCR_TR_IPUCU & set(re.findall(r"\w+", _kat(x)))
             else y if _kat(x) == _kat(y) else x if TR_HARF.search(x) else x if m.anlamsiz_oran(x) < m.anlamsiz_oran(y) else y)
        cikti.append((a[2], s))
    cikti += [(b[2], b[0]) for b in kalan]
    return [re.sub(r" [—–] ", " -- ", s) if TEKNIK.search(s) else s for _, s in sorted(cikti, key=lambda c: c[0])]  # OCR "--"yu "—" okur


def _ocr_model(satirlar):
    """C3: OCR anlamlandıramadı mı → kare modele gider: az metin (şema/görsel) · kısa satırlar (arayüz) · kod · anlamsız."""
    metin = " ".join(satirlar)
    n = len(re.sub(r"\s", "", metin))
    return (n < OCR_AZ or n / len(satirlar) < OCR_KISA or sum(bool(KOD.search(s)) for s in satirlar) >= OCR_KOD * len(satirlar)
            or m.anlamsiz_oran(metin) > 1 - OCR_GUVEN)


def _ocr(ctx, yollar):
    """C3: tüm kareler tek PowerShell çağrısında (ocr.ps1, Windows.Media.Ocr tr + en) → {dosya adı: birleşik satırlar}."""
    out = _kos(ctx, ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(OCR_PS), *map(str, yollar)], SURE["ocr"])
    return {ad: _ocr_birlestir(k.get("tr") or [], k.get("en") or []) for ad, k in json.loads(out.decode("utf-8") or "{}").items()}


def _yorumlar(ctx, d):
    """DERİNLİK-1 R4: sabitlenmiş/yazar yorumlarındaki bağlantılar (en fazla 20 yorum, indirme yok; yorumlar.json). → (bağlantılar, kapsam durumu)"""
    yol = d / "yorumlar.json"
    j = json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}
    if j.get("durum") != "✓":
        ctx["uyku"](2)  # meta isteğinin ardından beklemesiz istek yok
        try:  # _yt değil: hata yolunda altyazı dosyası silinmesin
            js = json.loads(_kos(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", "--write-comments", "--extractor-args",
                                       "youtube:max_comments=20,20,0,0;comment_sort=top", yt_url(d.name)], SURE["meta"]))
            j = {"durum": "✓", "yorumlar": [x.get("text") or "" for x in js.get("comments") or [] if x.get("is_pinned") or x.get("author_is_uploader")]}
        except Exception as e:  # sessiz dönüş yok: sebep Kapsam'da
            j = {"durum": f"yorum alınamadı ({' '.join(str(e).split())[:80]})", "yorumlar": []}
        yol.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    return list(dict.fromkeys(u for t in j["yorumlar"] for u in m.urller(t))), j["durum"]


def _bagli_video(ctx, v, bl, ky):
    """B ek: açıklama/yorum/sayfa'daki video linki kuyrukta (her durumda) yoksa 'bağlantılı video (<v>)' notuyla eklenir; kanal takibi yok."""
    metin = ky.read_bytes().decode("utf-8")
    var = {tr._hucre(s)[0] for s in metin.splitlines() if s.lstrip().startswith("|")}
    ids = [g[1] for x in bl if x["sinif"] == "video" and any(k.split()[0] in ("açıklama", "yorum", "sayfa") for k in x["kaynak"])
           and (g := m.ID.search(x["url"])) and g[1] and g[1] not in var and g[1] != v]
    sat, sayac = [], [0]
    for i in dict.fromkeys(ids):
        j = kn._istek(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", f"https://youtu.be/{i}"], sayac) or {}
        sat.append((i, round((j.get("duration") or 0) / 60, 1), str(j.get("title") or "?")[:40].replace("|", "/"), f"bağlantılı video ({v})",
                    "" if j else "yt-dlp -J başarısız"))
    if sat:
        ky.write_bytes(tr.kuyruk_ekle(metin, sat, set(), set(), "## Bağlantılı videolar")[0].encode("utf-8"))


def paket(ns, ctx):
    """Alt ajan girdisi tek dosya <önbellek>/<id>/paket.md: künye · chapter · linkler · sadeleştirilmiş segmentler · kare yolları.
    Kareler: yalnız ekran sorusu (p varsa istek yok) → ekran p'si en yüksek --kare zamanın tam-t karesi. Segment metni stdout'a yazılmaz."""
    from .parti import PAKET_ADIMLARI  # cli parti'yi içe alır: döngüsel, yerel
    d = ctx["kok"] / ns.id
    seg, _, istek, _ = _suz(ctx, d, ["ekran"], ns.istek_tavan) if ns.istek_tavan != 0 else (_oku(d) if (d / "segmentler.jsonl").is_file() else [], None, 0, None)  # M2a: tavan 0 → Jev yok, kareler segment sırasıyla
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    dil = m.dil_sec(meta)
    ns.kare = kare_tavan(meta.get("duration") or 0, ns.kare, " ".join(str(s.get("metin")) for s in seg))
    yalniz = ns.kare_yalniz or not seg  # M8 K2 (ii): altyazı yok ya da whisper çıktısı anlamsız → kare-yalnız paket
    seg = [] if yalniz else seg
    km = next((j[ns.id] for f in sorted(ctx["kok"].glob("kuyruk-meta-*.json"), reverse=True)
               if ns.id in (j := json.loads(f.read_text(encoding="utf-8")))), {})  # 24e-2 K1: Desktop kuyruk-meta önce
    lk = km.get("linkler") or m.urller(km.get("aciklama") or meta.get("description"))
    lk = m.urller(lk) if isinstance(lk, str) else lk
    ak = lk or []
    lk = list(dict.fromkeys([*ak, *(yk := _yorumlar(ctx, d)[0])]))  # DERİNLİK-1 R4: yorum bağlantıları kaynağa; durum yorumlar.json → parti Kapsam
    ky = d / "kapsam.json"
    if ns.incelenmedi:  # C4 ikinci geçiş: yalnız tavan/bütçe yüzünden incelenmeyen anlar; ilk paket paket-1.md'de kalır
        zamanlar, isaret = [t for t, _ in (json.loads(ky.read_text(encoding="utf-8"))["incelenmedi"] if ky.is_file() else [])], []
        if not zamanlar:
            print(f"paket: {ns.id} incelenmedi an yok")
            return 0
        if not (d / "paket-1.md").is_file():
            (d / "paket.md").replace(d / "paket-1.md")
    else:
        zamanlar = sorted((s["bas"] + s["son"]) / 2 for s in sorted(seg, key=lambda s: -s.get("p_ekran", 0))[:ns.kare])
        if (yalniz or 0 < (meta.get("duration") or 0) < SHORT_SN) and len(zamanlar) < ns.kare:  # M8 K5: short çoğunlukla tek segment → 1 kare; süreye yay
            zamanlar = [round(meta["duration"] * (i + 0.5) / ns.kare, 1) for i in range(ns.kare)]
        isaret = [(s["bas"] + s["son"]) / 2 for s in seg if ISARET.search(str(s.get("metin")))]
    ocr, gor = {}, set()
    taban = "\n".join([*(str(s.get("metin")) for s in seg), *(lk or [])])  # O11: OCR _kareler'de eklenir; ponytail: künye/chapter satırları sayılmaz
    try:
        kareler, kare_yok = (_kareler(ctx, d, [*isaret, *zamanlar], 0, GENISLIK, ns.model_tavan or ns.kare, not ns.incelenmedi, isaret, meta.get("duration") or 0, ocr, taban)
                             if zamanlar else []), None
    except Hata as e:  # M9 K2: taze adresle de kare yok → paket düşmez; altyazı + açıklama + bağlantılar kalır
        kareler, kare_yok = [], f"kare yok: {' '.join(str(e).split())}"[:200]
    bl, hata = tr.link_topla({  # B1: dört kaynak, sınıflı
        "açıklama": "\n".join(ak), "yorum": "\n".join(yk), "ocr": "\n".join(x for _, s in ocr.get("metin", []) for x in s),
        "altyazı": "\n".join(str(s.get("metin")) for s in seg)}), []
    yeni = gt.derinlik1(bl, ctx["kok"], al=ctx["al"], hata=hata)  # B2: 1 derinlik; okuyucu ctx'ten (testte sahte)
    (d / "baglantilar.json").write_text(json.dumps(bl + yeni, ensure_ascii=False, indent=1), encoding="utf-8")
    if ns.kuyruk and Path(ns.kuyruk).is_file():
        _bagli_video(ctx, ns.id, bl + yeni, Path(ns.kuyruk))
    md = [f"# {ns.id} · {meta.get('title')} · {meta.get('channel')} · süre {m.ss(meta.get('duration') or 0)} · sure_sn {int(meta.get('duration') or 0)} · short: {str(km['short'] if 'short' in km else tr.short_mu(meta.get('duration') or 0)).lower()} · dil {dil[0] if dil else '?'}"
          f" · https://youtu.be/{ns.id}",
          "## Chapter", *([f"{m.ss(c_['start_time'])} {c_.get('title')}" for c_ in meta.get("chapters") or []] or ["yok"]),
          "## Açıklama bağlantıları", *(lk or ["yok"]),
          *(["## Bağlantılı sayfalar", *[f"{x['url']} ({x['kaynak'][0]})" for x in yeni]] if yeni else []),  # erişilemeyen → kapsam.json (Ömer, O21)
          "## Segmentler", *(["altyazı yok: kare-yalnız — kanıt kaynağı kare/açıklama; altyazı kanıtı beklenmez"] if yalniz else []), *[f"[{m.ss(s['bas'])}] {x}" for s in seg if (x := m.sadelestir(s["metin"]))],
          *(["## Ekran metni (OCR)", *e] if (e := [f"[{m.ss(t)}] {x}" for t, s in sorted(ocr.get("metin", [])) for x in s if not (x in gor or gor.add(x))]
                                                or [x for x in [ocr.get("durum", "✓")] if x != "✓"]) else []),  # aynı satır bir kez; boşsa bölüm yok
          *(["## İncelenmedi", *i] if (i := [f"[{m.ss(t)}] {sebep}" for t, sebep in sorted(ocr.get("incelenmedi", []))]) else []),
          "## Kareler", *([f"{yol.as_posix()} · {m.ss(t)}" for t, yol in kareler] or [kare_yok or "yok"])]
    yol = d / "paket.md"
    yol.write_text("\n".join(md) + "\n", encoding="utf-8")
    if ocr.get("gurultu_satir"):  # O11 (4): atılan gürültü satırları denetim için
        (d / "ocr-gurultu.txt").write_text("".join(f"{m.ss(t)} · {x}\n" for t, x in sorted(ocr["gurultu_satir"], key=lambda g: g[0])), encoding="utf-8")
    sj = json.loads((d / "sahne.json").read_text(encoding="utf-8")) if (d / "sahne.json").is_file() else {"durum": "sahne ?"}
    inc = sorted(ocr.get("incelenmedi", []))
    ky.write_text(json.dumps({"izleme": f"{'kare-yalnız' if yalniz else f'segment {len(seg)}'} · "  # C4 Kapsam satırı → parti durum.json → panel
                                        f"{f'sahne {len(sj['sahneler'])}' if sj.get('durum') == '✓' else sj.get('durum')} · seçilen {ocr.get('secilen', 0)} · "
                                        f"OCR {len(ocr.get('metin', []))} · model {len(kareler)} · incelenmedi {len(inc)} · OCR gürültü {ocr.get('gurultu', 0)}{f" · tekrar (montaj) {n}" if (n := ocr.get('montaj')) else ''}", "incelenmedi": inc, "erisilemedi": hata,
                              "adimlar": list(PAKET_ADIMLARI)}, ensure_ascii=False), encoding="utf-8")  # MÜKEMMEL-5a damga
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
    out = _kos(ctx, ["yt-dlp", "-g", "--no-warnings", "-f", "bv*[height<=720][vcodec!=none]/b", yt_url(d.name)], SURE["meta"])
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


def _sahneler(ctx, d, n):
    """C2: tüm videoda sahne değişimleri (yalnız anahtar kareler, 160 px; video yazılmaz) → skoru en yüksek n zaman.
    sahne.json önbellek; hata durumu kayıtlı (sessiz dönüş yok) ve sonraki koşuda yeniden denenir."""
    yol = d / "sahne.json"
    j = json.loads(yol.read_text(encoding="utf-8")) if yol.is_file() else {}
    if j.get("durum") != "✓":
        try:  # ponytail: tüm akış okunur (uzun videoda bant genişliği); ağır gelirse düşük çözünürlüklü -f ile ayrı -g
            out = _kos(ctx, ["ffmpeg", "-v", "error", "-rw_timeout", "15000000", "-skip_frame", "nokey", "-i", _akis_url(ctx, d), "-an", "-vf",
                             f"scale=160:-2,select='gt(scene,{SAHNE_ESIK})',metadata=print:file=-", "-fps_mode", "vfr", "-f", "null", os.devnull], SURE["sahne"])
            j = {"durum": "✓", "sahneler": [[float(t), float(s)] for t, s in re.findall(rb"pts_time:([\d.]+)\s+lavfi\.scene_score=([\d.]+)", out)]}
        except Hata as e:
            j = {"durum": f"sahne alınamadı ({re.sub(r'https?://\S*', '<akış-url>', ' '.join(str(e).split()))[:80]})", "sahneler": []}
        yol.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    return [t for t, _ in sorted(j["sahneler"], key=lambda x: -x[1])[:n]]


def _kareler(ctx, d, zamanlar, pencere, g, en_fazla, sahne=False, oncelik=(), sure=0, ocr=None, taban=None):
    """[(t, yol)] zamana göre. sahne: tüm videonun sahne değişimleri de aday (C2, paket). Sıra: oncelik (altyazı işaret anı) → merkez
    kareler → pencere sahne kareleri; grup içinde OCR karakter sayısı. Tekrar (O11): katlanmış OCR metni ≥ OCR_BENZER benzer → uzun olan
    kalır; dHash ≤5 ya da aynı sahnede ≤ DHASH_SAHNE → bir kez (ikisi de metinliyse hash bakılmaz).
    ocr (dict, C3 paket): adaylar OCR'lanır → ocr {durum, metin [(t, satırlar)], incelenmedi [(t, sebep)]}; OCR'ın anlamlandırdığı kare
    modele gitmez (silinir), en_fazla yalnız modele giden kareleri sayar. taban (C4, O11): paket metni; taban + OCR metni + modele giden
    kareler pt.girdi_tk ile PAKET_BUTCE'yi aşarsa kare "incelenmedi"."""
    zamanlar, kesilen = list({int(t): t for t in zamanlar}.values()), []  # aynı saniye bir kez: _kare_uret aynı adlı kareyi siler
    if sahne:  # O11 (5): her sahne aday; ADAY_UST'u aşan sahneler (skor sırasıyla sondakiler) "aday tavanı"
        sh = list({int(t): t for t in _sahneler(ctx, d, None) if int(t) not in {int(x) for x in zamanlar}}.values())  # aynı saniyede iki sahne → bir kez
        zamanlar, kesilen = [*zamanlar, *sh[:max(0, ADAY_UST - len(zamanlar))]], sh[max(0, ADAY_UST - len(zamanlar)):]
    try:
        uretilen = [(t, _kare_uret(ctx, d, _akis_url(ctx, d), t, pencere, g)) for t in zamanlar]
    except Hata:  # M9 K1: 403 / akış URL hatası → önbellek silinir, taze -g ile bir kez yeniden
        (d / "akis.url").unlink(missing_ok=True)
        url = _akis_url(ctx, d)
        uretilen = [(t, _kare_uret(ctx, d, url, t, pencere, g)) for t in zamanlar]
    on = {int(t) for t in oncelik}
    aday = [(int(t) not in on, 0, t, x) for t, (mk, _) in uretilen for x in mk] + [(True, 1, t, x) for t, (_, sh) in uretilen for x in sh]
    aday = list({a[3]: a for a in aday if a[3].is_file()}.values())  # aynı yol bir kez (canlı hata: çift aday → ikinci unlink çöktü)
    o, metin = ({} if ocr is None else ocr), {}
    o.update(metin=[], incelenmedi=[(t, "aday tavanı") for t in kesilen], secilen=0, gurultu=0, gurultu_satir=[], montaj=0)
    if ocr is not None and aday:
        try:
            metin, o["durum"] = _ocr(ctx, [a[3] for a in aday]), "✓"
        except (Hata, ValueError) as e:  # OCR yok → kareler eskisi gibi hepsi modele (sebep pakette)
            o["durum"] = f"OCR yok ({' '.join(str(e).split())[:80]})"
    temiz, katlar, tekrar = {}, [], set()
    for a in aday:  # C3 düzeltme: gürültü satırı pakete yazılmaz, model kararına da girmez (O11: tekrar ayıklamadan önce, tüm adaylar)
        s = metin.get(a[3].name) or []
        temiz[a[3].name] = [x for x in s if not _ocr_gurultu(x)]
        o["gurultu"] += len(s) - len(temiz[a[3].name])
        o["gurultu_satir"] += [(a[2], x) for x in s if x not in temiz[a[3].name]]  # O11 (4): paket ocr-gurultu.txt
    for a in sorted(aday, key=lambda a: -len(_kat("\n".join(temiz[a[3].name])))):  # O11 (3a): metni uzun olan kalır
        if not (k := _kat("\n".join(temiz[a[3].name]))):
            continue
        if any((sm := difflib.SequenceMatcher(None, k, x, autojunk=False)).real_quick_ratio() >= OCR_BENZER and sm.quick_ratio() >= OCR_BENZER
               and sm.ratio() >= OCR_BENZER for x in katlar):
            tekrar.add(a[3].name)
            a[3].unlink(missing_ok=True)
        else:
            katlar.append(k)
    sj = json.loads((d / "sahne.json").read_text(encoding="utf-8")) if (d / "sahne.json").is_file() else {}
    kesim = [x for x, _ in sj["sahneler"]] if sj.get("durum") == "✓" else None  # O11 (3b): sahne ✓ değilse aynı sahne bilinmez → yalnız ≤5
    model, hashler = [], []
    for *_, t, yol in sorted(aday, key=lambda a: (a[0], a[1], -len(re.sub(r"\s", "", "".join(temiz[a[3].name]))))):
        if yol.name in tekrar:
            continue
        s = temiz[yol.name]
        h = m.dhash(_kos(ctx, ["ffmpeg", "-v", "error", "-i", str(yol), "-vf", "scale=9:8,format=gray", "-f", "rawvideo", "-"], SURE["ffmpeg"]))
        if any(not (s and sx) and ((f := bin(h ^ x).count("1")) <= 5 or f <= DHASH_SAHNE and kesim is not None
                                   and not any(min(t, tx) < k <= max(t, tx) for k in kesim)) for x, tx, sx in hashler):  # ikisi metinli → metin karar verdi
            yol.unlink(missing_ok=True)
            continue
        hashler.append((h, t, s))
        o["secilen"] += 1
        if s:
            o["metin"].append((t, s))
        if yol.name in metin and not _ocr_model(s):  # OCR anlamlandırdı: metin pakette, kare modele gitmez
            yol.unlink(missing_ok=True)
        else:
            model.append((t, yol))
    if kesim:  # C5: 5 sn içinde ≥3 kesim → montaj; kümeden modele en çok OCR metni (eşitse sahne skoru) taşıyan ≤2 kare
        skor, bas = {int(x): s for x, s in sj["sahneler"]}, []
        for k in sorted(kesim):
            if (not bas or k >= bas[-1] + MONTAJ_SN) and sum(k <= x < k + MONTAJ_SN for x in kesim) >= 3:
                bas.append(k)
        for b in bas:
            kume = sorted((f for f in model if b <= f[0] < b + MONTAJ_SN),
                          key=lambda f: (-len(re.sub(r"\s", "", "".join(temiz[f[1].name]))), -skor.get(int(f[0]), 0)))
            for f in kume[2:]:
                model.remove(f)
                f[1].unlink(missing_ok=True)
                o["montaj"] += 1
    tut, yazi = [], "\n".join([taban or "", *(x for _, s in o["metin"] for x in s)])  # O11: bütçe OCR dahil tam metinle (pt.girdi_tk)
    for t, yol in model:
        if len(tut) >= en_fazla:
            o["incelenmedi"].append((t, f"kare tavanı {en_fazla}"))
            yol.unlink(missing_ok=True)
        elif taban is not None and pt.girdi_tk(yazi, [*(y for _, y in tut), yol]) > PAKET_BUTCE:
            o["incelenmedi"].append((t, "jeton bütçesi"))
            yol.unlink(missing_ok=True)
        else:
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
        tr.kayit_ekle(yol, yeni)
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


OR_URL = "https://openrouter.ai/api/v1/chat/completions"


def _temizle(metin, env):
    """TOKEN-DENEME-2a: OpenRouter'a yalnız paket/altyazı gider — anahtar/token env değerleri ve mutlak yerel yollar çıkarılır."""
    for ad, deger in env.items():
        if re.search(r"KEY|TOKEN|SECRET|PASS", ad, re.I) and len(deger or "") >= 8:
            metin = metin.replace(deger, "[gizli]")
    return re.sub(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|(?<![\w.:/])/(?:[a-z]|home|Users|tmp)/|~[\\/])[^\s|)\]>\"'`]*", "[yol]", metin)


def tara(ns, ctx):
    """TOKEN-DENEME-2a K1: sonnet/haiku → Agent satırı (ana ajan çağırır); openrouter:<model> → aynı talimat + paket (vision ise ≤6 kare) OpenRouter'a, rapor + denetim."""
    import base64
    import time
    from datetime import date
    kol, pk = ns.kol, ctx["kok"] / ns.id / "paket.md"
    if kol not in ("sonnet", "haiku") and not kol.startswith("openrouter:"):
        print("kol: sonnet | haiku | openrouter:<model>")
        return 2
    if not pk.is_file():
        print(f"paket yok: {pk.as_posix()} (önce: video paket <url>)")
        return 1
    paket_md = pk.read_text(encoding="utf-8")
    kareler = list(dict.fromkeys(re.findall(r"\S+\.jpg", paket_md)))
    ad = re.sub(r"[^a-z0-9]+", "-", kol.lower()).strip("-")
    rapor = f"docs/video-tarama/{ns.tarih or date.today()}-{ns.id}.md" if kol == "sonnet" else f"docs/denemeler/ucuz-tarayici/{ad}/{ns.id}.md"
    if not kol.startswith("openrouter:"):
        print(f"ajan: video-tarayici{'-haiku' if kol == 'haiku' else ''} · id: {ns.id} · paket: {pk.as_posix()} · kareler: {' '.join(kareler) or '-'} · rapor: {rapor}")
        return 0
    if not (anahtar := ctx["env"].get("OPENROUTER_API_KEY")):
        print("OPENROUTER_API_KEY yok")
        return 1
    talimat = (kur._kok(ctx) / ".claude" / "agents" / "video-tarayici.md").read_text(encoding="utf-8").split("---", 2)[-1]
    sistem = talimat + "\nAraç yok: dosya okuyamaz/yazamaz, komut koşamazsın. Raporu yalnız markdown olarak döndür (rapor-denetle ana tarafta koşar)."
    ekler = [{"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(Path(k).read_bytes()).decode()}}
             for k in kareler[:min(ns.kare, 6)] if Path(k).is_file()]  # base64 filtrelenmez: yalnız metin parçaları _temizle'den geçer
    govde = {"model": kol.split(":", 1)[1], "usage": {"include": True},
             "messages": [{"role": "system", "content": _temizle(sistem, ctx["env"])},
                          {"role": "user", "content": [{"type": "text", "text": _temizle(paket_md, ctx["env"])}] + ekler}]}
    t = c.Tasiyici(env=ctx["env"], gonder=ctx["gonder"], uyu=ctx["uyku"] or time.sleep, istek_tavan=2, tekrar=1)  # jev taşıyıcısı: tekrar + istek tavanı
    t.b = {"ad": "OpenRouter", "url": OR_URL}
    y = t._istek(govde, {"Authorization": f"Bearer {anahtar}", "Content-Type": "application/json"})
    md, u = y["choices"][0]["message"]["content"] or "", y.get("usage") or {}
    (r := kur._kok(ctx) / rapor).parent.mkdir(parents=True, exist_ok=True)
    r.write_text(md.strip() + "\n", encoding="utf-8")
    h = tr.denetle(md)
    print(f"tara: {rapor} · kol: {kol} · token: {u.get('prompt_tokens', 0)}+{u.get('completion_tokens', 0)} · ${u.get('cost') or 0:.4f} · istek: {t.istek} · kare: {len(ekler)} · denetim: {'GEÇTİ' if not h else f'{len(h)} hata'}")
    return 0


def rapor_denetle(ns, ctx):
    if (ham := Path(ns.rapor).read_text(encoding="utf-8")).startswith("# Deneme:"):  # 24e-2 K5: deneme şeması (takas tablosu)
        for x in (h := og.deneme_denetle(ham)):
            print(x)
        print("rapor-denetle (deneme): " + ("GEÇTİ" if not h else f"{len(h)} hata"))
        return 1 if h else 0
    if tr.bolum(ham := Path(ns.rapor).read_text(encoding="utf-8"), "Özellikler").strip() or uy.prompt_mu(ham) or "arastirma" in uy.alanlar(ham):  # 24c K1  # 20b-devam K6 · 23c K7: aday raporu
        yarim = "yarım" in uy.alanlar(ham).get("arastirma", "")  # 24a K1: tur tavanı; geçerli ama işaretli, katman DENE vermez
        for x in (h := uy.mekanizma_denetle(ham) + uy.anatomi_denetle(ham)):
            print(("yarım: " if yarim else "") + x)
        print("rapor-denetle (aday): " + (f"GEÇTİ (araştırma yarım, işaretli; {len(h)} eksik)" if yarim else "GEÇTİ" if not h else f"{len(h)} hata"))
        return 1 if h and not yarim else 0
    if {"ad", "tur"} <= uy.alanlar(ham).keys():  # 24e-1 K5: T0 aday dosyası video raporu değil
        for x in (h := uy.t0_denetle(ham)):
            print(x)
        print("rapor-denetle (T0): " + ("GEÇTİ" if not h else f"{len(h)} hata"))
        return 1 if h else 0
    metin = _sozluk_doldur(ctx, ns.rapor, Path(ns.rapor).read_text(encoding="utf-8"))
    sure = _sure(ctx, ns.rapor, metin)
    eksik = sum("EKSİK:" in s for s in metin.splitlines())  # M2e K1: kısmi kabul işareti geçerli ama uyarılı
    h = tr.denetle("\n".join(s for s in metin.splitlines() if "EKSİK:" not in s), sure)
    for x in tr.uyarilar(metin):  # M2f K1: uyarı sayılmaz
        print(x)
    if eksik:
        print(f"uyarı: {eksik} EKSİK alan (kısmi kabul, işaretli)")
    for x in h:
        print(x)
    print(f"rapor-denetle: {'GEÇTİ' if not h else f'{len(h)} hata'}" + ("" if sure else " (süre bilinmiyor: zaman denetimi atlandı)"))
    return 1 if h else 0


def t0_regresyon(ns, ctx):
    """24c K2/K4: tests/fixture/t0-tur.json → T0 türü (≥ n-1 doğru) + prompt/kural ZATEN VAR (hepsi). Canlı Jev: T0 ≤2·n, zaten ≤3·m."""
    fix = json.loads((Path(__file__).resolve().parents[1] / "tests" / "fixture" / "t0-tur.json").read_text(encoding="utf-8"))
    t = c.Tasiyici(env=ctx["env"], en_fazla=2 * len(fix["t0"]), gonder=ctx["gonder"], istek_tavan=2 * len(fix["t0"]))
    d = 0
    for x in fix["t0"]:
        g = uy.t0_tur(t, x["ad"], {"kural": x["kural"]})
        d += g == x["tur"]
        print(f"{'+' if g == x['tur'] else '-'} {x['ad']}: {g} (beklenen {x['tur']})")
    kok, z = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK), 0
    tz = c.Tasiyici(env=ctx["env"], en_fazla=3 * len(fix["zaten"]), gonder=ctx["gonder"], istek_tavan=3 * len(fix["zaten"]))
    for x in fix["zaten"]:
        e = uy.prompt_zaten(tz, f"{x['ad']}: {x['kalip']}", uy.zaten_liste(kok, ctx["env"], x.get("haric")))  # kalıbın kendi adayı hariç (katmandaki gibi)
        ok = bool(e and x["kaynak"] in e[0] and e[1] >= uy.ZATEN_ESIK)  # 24d: 0.4–0.6 olası tekrar, ZATEN VAR sayılmaz
        z += ok
        print(f"{'+' if ok else '-'} zaten {x['ad']}: {e}")
    print(f"t0-regresyon: T0 {d}/{len(fix['t0'])} (Jev {t.istek}) · zaten {z}/{len(fix['zaten'])} (Jev {tz.istek})")
    return 0 if d >= len(fix["t0"]) - 1 and z == len(fix["zaten"]) else 1


def kural_regresyon(ns, ctx):
    fix = json.loads((Path(__file__).resolve().parents[1] / "tests" / "fixture" / "kural-cifti.json").read_text(encoding="utf-8"))
    kl = tr.kurallar(tr.kural_kaynaklari(ctx["env"], _ev(ctx)), ctx["kok"] / "kurallar.json")
    t = c.Tasiyici(env=ctx["env"], en_fazla=2 * (len(fix["cift"]) + len(fix["degil"])), gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    r = tr.kural_regresyon(t, fix, kl)
    print(f"kural-regresyon: çift {len(r['bulunan'])}/{len(fix['cift'])} · yanlış pozitif {len(r['yp'])} · Jev istek {t.istek} (tavan {ns.istek_tavan})")
    for x in r["kacan"] + r["yp"]:
        print(f"- {x}")
    return 1 if r["kacan"] or r["yp"] else 0


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
    raporlar, adaylar, gecen, refs, ek = [], [], set(), [], {}
    for r in ns.raporlar:
        v, _ = tr.rapor_id(r)
        metin = Path(r).read_text(encoding="utf-8")
        if not tr.denetle(metin, _sure(ctx, r, metin)):  # kayda yalnız rapor-denetle'den geçen
            gecen.add(v)
        baslik = next((s[2:].strip() for s in metin.splitlines() if s.startswith("# ")), "?")
        satir = tr.aday_satirlari(metin)
        ac, ref = tr.aciklama_adaylari(metin, v)  # 24e-2 K1: kurulu kontrolü aşağıdaki sözlük eşleşmesinde
        adaylar += ac
        refs += [(v, u) for u in ref]
        ek[v] = tr.rapor_videolari(metin, v)  # 24e-2 K3
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
    cikti = tr.bos_yol(d / f"{bugun}-toplu.md")  # 24b K3: aynı gün ikinci koşu ezmez
    md = [f"# Video tarama toplu — {bugun}", "", f"{len(raporlar)} video · {len(tek)} tekil aday · Jev tarama isteği {istek}", "",
          "| aday | işaret | sözlük eşleşmesi | çift p | izin riski (0-3) | tür | videolar |", "|---|---|---|---|---|---|---|"]
    for x in tek:
        es = f"{x['es'][0]} ({x['es'][1]}, {x['es'][2]:.2f})" if x["es"] else "yok"
        md.append(f"| {x['ad']} | {x['etiket']} | {es} | {'-' if x['cift'] is None else x['cift']} | "
                  f"{'-' if x['risk'] is None else x['risk']} | {x['tur']} | {', '.join(x['videolar'])} |")
    md += ["", "## Açıklama bağlantıları"] + [f"- aday {x['ad']} · repo {x['repo']} · {x['video']}" for x in adaylar if x.get("repo")] + [f"- referans (Site/UI) {u} · {v}" for v, u in refs] if refs or any(x.get("repo") for x in adaylar) else []
    md += ["", "## Raporlar"] + [f"- {v} · {b} · {r.name}" for v, r, b, _ in raporlar]
    cikti.write_text("\n".join(md) + "\n", encoding="utf-8")
    tr.kayit_ekle(yol, [{"id": x, "tarih": bugun, "rapor": r.name, "adaylar": a, "ele": []} for v, r, _, a in raporlar if v in gecen for x in ek[v]])  # 23c: yalnız ekler
    from .kanal import takip_ekle  # KANAL-2a A3: parti dışı yol (video-tarama → toplu) da Ömer kuralına bağlı
    takip_ekle(yol.parents[2], [x for v, *_ in raporlar if v in gecen for x in ek[v]], ctx)
    kayit = tr.kayit_son(tr.kayit_oku(yol), "id")
    for v, _, b, a in raporlar[:20]:
        print(f"{v} · {b[:50]} · {len(a)} aday: " + ", ".join(f"{x} [{isr[tr.normal(x)]}]" for x in a)[:300])
    say = {}
    for x in tek:
        say[x["isaret"]] = say.get(x["isaret"], 0) + 1
    print(f"{len(tek)} tekil aday · " + " · ".join(f"{k} {n}" for k, n in sorted(say.items())) + f" · Jev istek {istek}")
    print(f"rapor: {cikti} · kayıt: {len(kayit)} video" + (f" · kayda yazılmadı (rapor-denetle): {' '.join(sorted(ids - gecen))}" if ids - gecen else ""))
    return 0


ARAC_TUR = {"araç": "kurulabilir skill, plugin, MCP, CLI, uygulama, kütüphane ya da hizmet",
            "teknik": "tasarım, kod, animasyon ya da mimari tekniği", "prompt": "prompt ya da şablon kalıbı",
            "ipucu": "iş akışı ya da kullanım ipucu"}


def _slug(ad):
    return tr.slug(ad)[:40]


def _top(y, k):
    pr = ((y or {}).get(k) or {}).get("probabilities") or {}
    return max(pr, key=pr.get) if pr else "?"


def _kural_bekleyen(bk, x, etiket):
    """24a K3: t0 biçimi (başlık + ad · madde · kaynak) — `alanlar()` başlık satırını atlar, `video kural-onay` madde/kaynak okur."""
    bk.mkdir(parents=True, exist_ok=True)
    y = bk / f"kural-{_slug(x['ad'])}.md"
    y.write_text(f"# ONAY kural {_slug(x['ad'])}\nad: {x['ad']}\nmadde: {x['ad']}{' — ' + x['not'] if x['not'] else ''}\nkaynak: {x['video']} ({etiket})\n",
                 encoding="utf-8")
    return y


def yeniden(ns, ctx):
    """VİDEO-YENİDEN-1: eski (≤--son, etiketsiz) raporların kalemleri bugünkü hattan; izleme · araştırıcı · claude -p yok.
    Jev: video içerik türü (1 batch) · kalem tür/kural-olgu/token/departman (batch) · araç olmayana kural_esle (≤2/kalem, tavanlı)."""
    from collections import Counter
    d, kok, bugun = _tarama_dizin(ctx), Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK), time.strftime("%Y-%m-%d")
    kayit = tr.kayit_oku(d / "kayit.jsonl")
    env_ = {h[0]: h for _, rs in tr.tablolar((d / "00-envanter.md").read_text(encoding="utf-8")) for h in rs} if (d / "00-envanter.md").is_file() else {}
    vids, kal = [], []
    # 1b: --yalniz <dosya> (satır: id<TAB>ad) → yalnız o kalemler; video türü ve kalan kararlar önceki yeniden satırından
    yal = {tuple(s.split("\t", 1)) for s in Path(ns.yalniz).read_text(encoding="utf-8").splitlines() if "\t" in s} if ns.yalniz else None
    onceki = tr.kayit_son([k for k in kayit if str(k.get("etiket", "")).startswith("yeniden:")], "id")
    for k in kayit:
        if k["tarih"] > ns.son or k.get("etiket") or k["id"] == "JfmAm3sxCSc" or (yal is not None and k["id"] not in {i for i, _ in yal}):
            continue
        m_ = (d / k["rapor"]).read_text(encoding="utf-8")
        e = env_.get(k["id"])
        ka = re.search(r"^kanal:\s*([^·\n]+)", m_, re.M)
        v = {"id": k["id"], "baslik": e[1] if e else next((s[2:].strip() for s in m_.splitlines() if s.startswith("# ")), "?"),
             "kanal": e[2] if e else (ka[1].strip() if ka else "?"), "tarih": e[4] if e and len(e) > 4 else k["tarih"],
             "kare_zayif": "Kareden okunanlar" not in m_ or "yalnız ekranda" in m_,
             "ozet": next((s for s in m_.splitlines() if s.startswith("ana iddia:")), m_[:300])}
        v["kalem"] = [{"ad": a, "durum": du, "etiket": et, "not": no, "video": k["id"]} for a, du, et, no in tr.eski_kalemler(m_)]
        if yal is not None:
            v["kalem"] = [x for x in v["kalem"] if (k["id"], x["ad"]) in yal]
            v["sahte"] = [{"ad": a, "durum": "", "etiket": "", "not": "", "video": k["id"], "karar": "SAHTE", "gerekce": "sahte aday: → hedef dosya/adım, etiket değil",
                           "celiski": False, "token": False} for a in tr.sahte_kalemler(m_) if (k["id"], a) in yal]
            v["tur"] = onceki[k["id"]]["tur"]
        vids.append(v)
        kal += v["kalem"]
    t = c.Tasiyici(env=ctx["env"], en_fazla=10 ** 5, gonder=ctx["gonder"], istek_tavan=ns.istek_tavan)
    soru = {"tur": {"type": "choice", "instructions": "Bu YouTube videosunun (state: başlık · özet · kalemler) ana içerik türü hangisi?",
                    "criteria": {x: x for x in tr.ICERIK}}}
    for v, y in zip(vids, t.yargila([f"{v['baslik']}\n{v['ozet']}\nkalemler: {', '.join(x['ad'] for x in v['kalem'])}" for v in vids], soru) if yal is None else []):
        v["tur"] = _top(y, "tur")
    sk_ = {"tur": {"type": "choice", "instructions": "Videodan çıkan bu kalem (state) ne?", "criteria": ARAC_TUR},
           "ko": {"type": "choice", "instructions": og.TUR_SORU, "criteria": og.TUR_OLCUT},
           "token": {"type": "noul", "instructions": "Bu kalem (state) token, context ya da model maliyeti tasarrufu hakkında mı?"}, **dp.soru()}
    for x, y in zip(kal, t.yargila([f"{x['ad']} · eski: {x['durum']} {x['etiket']} · {x['not']}" for x in kal], sk_)):
        x["tur"], x["ko"], x["departman"] = _top(y, "tur"), _top(y, "ko"), dp.sec(y or {})[0]
        x["token"] = ((y or {}).get("token") or {}).get("noul", 0) >= 0.5
    ev = _ev(ctx)
    sozluk, envanter = tr.sozluk_kur(ev, []), tr.envanter_sozluk(tr._json(kok / "docs" / "departmanlar" / "envanter.json") or [])
    kl = tr.kurallar(tr.kural_kaynaklari(ctx["env"], ev) + [kok / "skills" / "web-sahne-desenleri" / "SKILL.md", kok / "docs" / "departmanlar" / "frontend-promptlar.md"],
                     ctx["kok"] / "kurallar-yeniden.json")
    for x in kal:
        x["es"], x["kural"] = tr.arac_esle(x["ad"], envanter, sozluk), None
        if x["tur"] != "araç" and not x["es"]:
            if t.istek + 2 > ns.istek_tavan:
                x["sorulmadi"] = True
            else:
                x["kural"] = tr.kural_esle(t, f"İPUCU: {x['ad']}\n{x['tur']}: {x['not']}", kl)
        x["karar"], x["gerekce"] = ("SORULMADI", "istek tavanı") if x.get("sorulmadi") else tr.yeni_karar(x)
        x["celiski"] = not x.get("sorulmadi") and tr.celiski_mi(x)
    if yal is not None:
        return _yeniden_duzelt(vids, kal, onceki, t, ns, d, kok, bugun)
    for v in vids:
        v["puan"] = tr.puan({"tur": v["tur"], "kararlar": [x["karar"] for x in v["kalem"]], "token": sum(x["token"] for x in v["kalem"]), "kare_zayif": v["kare_zayif"]})
    # çıktı
    h = lambda s: str(s).replace("|", "/")  # noqa: E731
    ilk = sorted(vids, key=lambda v: (-v["puan"], v["id"]))[:15]
    L = [f"# Yeniden değerlendirme {bugun} — {len(vids)} eski video, {len(kal)} kalem", "",
         f"izleme 0 · araştırıcı 0 · claude -p 0 · Jev istek {t.istek} (tavan {ns.istek_tavan}) · kaynak: eski raporlar + 00-envanter.md", "",
         "## İçerik türü dağılımı", *[f"- {a}: {n}" for a, n in Counter(v["tur"] for v in vids).most_common()], "",
         "## Eski → yeni karar", *[f"- {a} → {b}: {n}" for (a, b), n in sorted(Counter((x["etiket"] or "?", x["karar"]) for x in kal).items(), key=lambda z: -z[1])], "",
         "## Yeni karar dağılımı", *[f"- {a}: {n}" for a, n in Counter(x["karar"] for x in kal).most_common()], ""]
    for kr in ("DENE", "UYARLA", "ÖĞREN"):
        L += [f"## {kr}", "| ad | video | tür | departman | token | gerekçe |", "|---|---|---|---|---|---|",
              *[f"| {h(x['ad'])} | {x['video']} | {x['tur']} | {x['departman']} | {'mekanizma-adayı' if x['token'] else ''} | {h(x['gerekce'])} |" for x in kal if x["karar"] == kr], ""]
    L += ["## ÇELİŞKİ (eski ZATEN VAR/ÇİFT, bugün eşleşme yok)", *([f"- {x['ad']} ({x['video']}): eski {x['durum']} · bugün {x['karar']}" for x in kal if x["celiski"]] or ["- yok"]), "",
          "## Kural önerileri (ONAY: `video kural-onay <slug> --kapsam ...`)", *([f"- kural-{_slug(x['ad'])}: {x['ad']} ({x['video']})" for x in kal if x["karar"] == "KURAL"] or ["- yok"]), "",
          "## Envanter (K1)", "| id | başlık | kanal | tarih | kalem | eski işaretler | tür | puan |", "|---|---|---|---|---|---|---|---|",
          *[f"| {v['id']} | {h(v['baslik'])} | {h(v['kanal'])} | {v['tarih']} | {len(v['kalem'])} | {h(' '.join(f'{a}:{n}' for a, n in Counter(x['etiket'] or '?' for x in v['kalem']).items()))} | {v['tur']} | {v['puan']} |" for v in vids], "",
          "## Tam yeniden izleme — ilk 15 (K3, KOŞULMAZ)", "puan = site/UI×3 + prompt/şablon×3 + (DENE+UYARLA)×2 + token kalem×2 + kare zayıf×1; JfmAm3sxCSc hariç", "",
          "| id | başlık | puan | gerekçe |", "|---|---|---|---|",
          *[f"| {v['id']} | {h(v['baslik'])} | {v['puan']} | {v['tur']} · DENE+UYARLA {sum(x['karar'] in ('DENE', 'UYARLA') for x in v['kalem'])} · token {sum(x['token'] for x in v['kalem'])} · kare zayıf {int(v['kare_zayif'])} |" for v in ilk], "",
          "parti 1 (8): `/video-uygula " + " ".join(f"https://youtu.be/{v['id']}" for v in ilk[:8]) + "` (video kayit --yeniden; etiket yeniden:tam; eski satır ezilmez)",
          "parti 2 (7): `/video-uygula " + " ".join(f"https://youtu.be/{v['id']}" for v in ilk[8:]) + "` (aynı)", ""]
    cikti = tr.bos_yol(kok / "docs" / "kurulumlar" / "yeniden" / f"{bugun}-toplu.md")  # 24b K3
    cikti.parent.mkdir(parents=True, exist_ok=True)
    cikti.write_text("\n".join(L), encoding="utf-8")
    bk = kok / "docs" / "kurulumlar" / "bekleyen"
    for x in kal:
        if x["karar"] == "KURAL":
            _kural_bekleyen(bk, x, f"yeniden:{bugun}")
    tr.kayit_ekle(d / "kayit.jsonl", [{"id": v["id"], "tarih": bugun, "rapor": f"../kurulumlar/yeniden/{cikti.name}", "adaylar": [x["ad"] for x in v["kalem"]], "ele": [],
                                        "etiket": f"yeniden:{bugun}", "tur": v["tur"], "puan": v["puan"], "kararlar": {x["ad"]: x["karar"] for x in v["kalem"]}} for v in vids])
    print(f"{cikti} · {len(vids)} video · {len(kal)} kalem · Jev istek {t.istek}/{ns.istek_tavan}")
    return 0

def _yeniden_duzelt(vids, kal, onceki, t, ns, d, kok, bugun):
    """1b: --yalniz sonucu → önceki yeniden raporuna '## Düzeltme (1b)' eki + kayıt satırı (etiket önceki+'b', append-only).
    Puan Δ = 2·(DENE+UYARLA farkı); token sınıfı değişmedi varsayılır (aynı soru, aynı kalem)."""
    from collections import Counter
    DU, h = ("DENE", "UYARLA"), (lambda s: str(s).replace("|", "/"))
    ch, satir, sahte = [], [], [x for v in vids for x in v["sahte"]]
    for v in vids:
        o, yeni = onceki[v["id"]], {x["ad"]: x for x in v["kalem"] + v["sahte"]}
        ch += [(o["kararlar"].get(a, "?"), x["karar"], x) for a, x in yeni.items()]
        satir.append({"id": v["id"], "tarih": bugun, "rapor": o["rapor"], "adaylar": o["adaylar"], "ele": [], "etiket": o["etiket"] + "b", "tur": v["tur"],
                      "puan": o["puan"] + 2 * sum((x["karar"] in DU) - (o["kararlar"].get(a) in DU) for a, x in yeni.items()),
                      "kararlar": {**o["kararlar"], **{a: x["karar"] for a, x in yeni.items()}}, "sahte": [x["ad"] for x in v["sahte"]]})
    son = {**onceki, **{s["id"]: s for s in satir}}
    sira = lambda z: [i for i, _ in sorted(((i, r) for i, r in z.items() if "puan" in r), key=lambda p: (-p[1]["puan"], p[0]))[:15]]  # noqa: E731
    eski15, yeni15 = sira(onceki), sira(son)
    dene = sum(k == "DENE" for i in yeni15 for k in son[i]["kararlar"].values())
    L = ["", f"## Düzeltme (1b) — {bugun}", "",
         f"`video yeniden --yalniz`: {len(kal)} kalem Jev'e soruldu + {len(sahte)} sahte işaretlendi · izleme 0 · araştırıcı 0 · claude -p 0 · "
         f"Jev istek {t.istek} (tavan {ns.istek_tavan}) · etiket {satir[0]['etiket'] if satir else '-'} · araç eşleştirme: tam departman envanteri, yoksa sözlük", "",
         "### Eski → yeni (yeniden koşulanlar)", *[f"- {a} → {b}: {n}" for (a, b), n in Counter((a, b) for a, b, _ in ch).most_common()], "",
         "### Değişen kararlar", "| ad | video | eski | yeni | gerekçe |", "|---|---|---|---|---|",
         *[f"| {h(x['ad'][:90])} | {x['video']} | {a} | {b} | {h(x['gerekce'])} |" for a, b, x in ch if a != b and b != "SAHTE"], "",
         f"### Sahte aday: {len(sahte)} (işaretli `sahte`, silinmedi; `- madde → CLAUDE.md / DESIGN.md / API …` hedefi etiket sanılmıştı)",
         *[f"- {x['video']}: {h(x['ad'][:90])} (eski {a})" for a, b, x in ch if b == "SAHTE"], "",
         "### İlk 15 (1b puanı)", "| id | eski puan | yeni puan | durum |", "|---|---|---|---|",
         *[f"| {i} | {onceki[i]['puan']} | {son[i]['puan']} | {'yeni giren' if i not in eski15 else ''} |" for i in yeni15],
         *([f"- çıkan: {i} ({onceki[i]['puan']} → {son[i]['puan']})" for i in eski15 if i not in yeni15] or ["- liste değişmedi"]), "",
         "### Maliyet (1b)", "- tarayıcı: 15 × ~75k = ~1.13M token (değişmedi)",
         f"- araştırıcı: ilk 15'te DENE {dene} × ~30k = ~{dene * 0.03:.2f}M token (önceki varsayım 15 × 2 = 30 aday)", ""]
    with (kok / "docs" / "kurulumlar" / "yeniden" / Path(satir[0]["rapor"] if satir else "yok.md").name).open("a", encoding="utf-8") as f:
        f.write("\n".join(L))
    bk = kok / "docs" / "kurulumlar" / "bekleyen"
    for x in kal:
        if x["karar"] == "KURAL" and not (bk / f"kural-{_slug(x['ad'])}.md").exists():
            _kural_bekleyen(bk, x, f"yeniden:{bugun}b")
    tr.kayit_ekle(d / "kayit.jsonl", satir)
    print(f"düzeltme: {len(kal)} kalem · sahte {len(sahte)} · {len(satir)} video · Jev istek {t.istek}/{ns.istek_tavan} · ilk 15 {'aynı' if eski15 == yeni15 else 'değişti'}")
    return 0


def getir_(ns, ctx):
    print(gt.getir(ns.url, ns.n, ctx["kok"] / "getir"), end="")
    return 0


def repo_(ns, ctx):
    print(gt.repo(ns.ad, ns.dosya, ns.satir, ctx["kos"]), end="")
    return 0


def kaynak(ns, ctx):
    """24e-2 K2: videosuz kaynak (GitHub repo/alt klasör ya da web sayfası) → kayıt (id kaynak-<slug>, yalnız ekler) → kurulu kontrolü +
    ön getirme (`on_`: iskelet + güvenlik ön taraması) → docs/kurulumlar/kaynak-<slug>.md. Araştırıcı ve katman ana ajanda."""
    import time
    from types import SimpleNamespace
    kok = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK)
    k, ky = tr.kaynak_ayristir(ns.url), _tarama_dizin(ctx) / "kayit.jsonl"
    if k["id"] not in {x.get("id") for x in tr.kayit_oku(ky)}:
        tr.kayit_ekle(ky, [{"id": k["id"], "tarih": time.strftime("%Y-%m-%d"), "rapor": f"kaynak-{k['ad']}.md", "adaylar": [k["ad"]], "ele": [], "url": ns.url}])
    rc = on_(SimpleNamespace(video=k["id"], aday=k["ad"], repo=k["repo"], tur=ns.tur, url=None if k["repo"] else ns.url, rapor=None), ctx)
    r = kok / "docs" / "kurulumlar" / f"kaynak-{k['ad']}.md"
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text(f"# {k['id']}\n\nurl: {ns.url}\nrepo: {k['repo'] or 'yok'}\nalt_yol: {k['alt'] or 'yok'}\ntur: {ns.tur}\n\n## Sonraki\n"
                 f"- aday-arastirici: docs/kurulumlar/adaylar/{k['ad']}.md (alt yol {k['alt'] or 'kök'}) → `video katman docs/kurulumlar/adaylar/{k['ad']}.md`\n",
                 encoding="utf-8")
    print(f"kaynak: {k['id']} · repo {k['repo'] or 'yok'} · alt {k['alt'] or 'yok'} · on rc {rc} · {r.as_posix()}")
    return rc


def kuyruk(ns, ctx):
    """24e-2 K6: kuyruk.md → sıradaki parti önerisi; --isle id,… --commit sha → yalnız o satırların durum sütunu (CRLF korunur)."""
    y = Path(ns.dosya) if ns.dosya else Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK) / "docs" / "video-tarama" / "kuyruk.md"
    metin = y.read_bytes().decode("utf-8")
    if ns.eylem == "yenile":  # A8: dk/başlığı "?" satırlar yt-dlp -J ile; başarısızsa "?" kalır, nota "meta hatası: <sebep>" (bir kez)
        out, sayac, n, t = [], [0], 0, 0
        for s in metin.splitlines(keepends=True):
            g = s.rstrip("\r\n")
            h = tr._hucre(g)
            if g.lstrip().startswith("|") and len(h) == 5 and "?" in h[1:3] and re.fullmatch(r"[\w-]{11}", h[0]):
                hata, t = [], t + 1
                j = kn._istek(ctx, ["yt-dlp", "-J", "--skip-download", "--no-warnings", f"https://youtu.be/{h[0]}"], sayac, hata=hata)
                if j:
                    h[1] = str(round(j["duration"] / 60, 1)) if j.get("duration") else h[1]
                    h[2] = str(j.get("title") or h[2])[:40].replace("|", "/")
                    n += 1
                elif (nt := f"meta hatası: {(hata or ['?'])[0][:80].replace('|', '/')}") not in h[3]:
                    h[3] = f"{h[3]} · {nt}" if h[3] else nt
                s = f"| {' | '.join(h)} |{s[len(g):]}"
            out.append(s)
        y.write_bytes("".join(out).encode("utf-8"))
        print(f"kuyruk: yenilendi {n}/{t} satır ({sayac[0]} istek)")
        return 0
    if ns.isle:
        if not ns.commit:
            print("kuyruk: --isle için --commit gerekli")
            return 2
        y.write_bytes(tr.kuyruk_isle(metin, set(ns.isle.split(",")), ns.commit).encode("utf-8"))
        print(f"kuyruk: işlendi: {ns.commit} · {ns.isle}")
        return 0
    tur, parti = tr.kuyruk_parti(metin)
    print(f"kuyruk: sıradaki parti ({tur or 'yok'}, {len(parti)}/{8 if tur == 'short' else 3})")
    for h in parti:
        print(f"- {h[0]} · {h[1]} dk · {h[2]} · https://youtu.be/{h[0]} · not: {h[3]}")
    if parti:
        print(f"işlenince: video kuyruk --isle {','.join(h[0] for h in parti)} --commit <sha>")
    return 0


def on_(ns, ctx):
    kok = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK)
    if ns.tur in tr.KURAL_TUR | {"teknik"}:  # parti-d: ipucu/teknik iskelete girmez, T0 (katman) yolundan geçer
        print(f"on: {ns.aday} · tür {ns.tur} → iskelet yok, T0'dan geçer")
        return 2
    if es := tr.arac_esle(ns.aday, tr.envanter_sozluk(tr._json(kok / "docs" / "departmanlar" / "envanter.json") or []), []):  # parti-d: kurulu → on/klon yok
        uy.bizdeki_mekanizma(ctx, kok, ns.video, ns.aday, es[0])  # B5: bizdeki kopya
        print(f"on: kurulu ({es[0]}) → ZATEN VAR, araştırıcı yok · aday: {uy.iskelet(kok, ns.video, ns.aday, ns.tur, ns.repo, None, kurulu=es[0])}")
        return 0
    g = uy.on_tarama(ctx, ns.repo) if ns.repo else None
    r = ns.rapor if not ns.rapor or Path(ns.rapor).is_file() else kok / "docs" / "video-tarama" / ns.rapor  # DEVAM-4: çıplak ad → tarama dizini
    m = uy.mekanizma(ctx, ctx["kok"] / "repo" / ns.repo.replace("/", "__") if ns.repo else None, ns.repo or ns.aday)  # B5: on_tarama klonu
    y = gt.on(kok, ns.video, ns.aday, ns.repo, ns.url, ctx["kos"], ctx["kok"] / "getir", rapor=r, seg=ctx["kok"] / ns.video / "segmentler.jsonl", guvenlik=(g or "") + m,
                 kapsam=ctx["kok"] / ns.video / "kapsam.json", web=True, tur=ns.tur)
    a = uy.iskelet(kok, ns.video, ns.aday, ns.tur, ns.repo, y, g)  # 24c K1: araştırıcıdan önce, var olanı ezmez
    print(f"on: {y} · ~{c.token(y.read_text(encoding='utf-8'))} token · aday: {a}")
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
    sure, tavan = meta.get("duration") or 0, ns.en_fazla_dk * 60 or None  # C1: --en-fazla-dk 0 → süre sınırı yok
    kes = tavan and (not sure or sure > tavan)
    boy, yarim = (min(sure, tavan) if tavan else sure) if sure else 0, d / "whisper.json"
    parca = json.loads(yarim.read_text(encoding="utf-8"))["parca"] if yarim.is_file() else []  # C1: yarıda kalan → kaldığı parçadan
    ses = next(d.glob("ses.*"), None) if parca else None
    if ses is None:
        parca = []
        _kos(ctx, ["yt-dlp", "--no-warnings", "-f", "ba/b", "-o", str(d / "ses.%(ext)s"), *(["--download-sections", f"*0-{tavan}"] if kes else []),
                   yt_url(ns.id)], SURE["ses"])
        if (ses := next(d.glob("ses.*"), None)) is None:
            raise Hata("ses inmedi")
    model = WhisperModel(ns.model, device="cpu", compute_type="int8")
    for bas in range(len(parca) * WHISPER_PARCA, boy or 1, WHISPER_PARCA):  # süre bilinmiyorsa tek parça
        k = {"clip_timestamps": [bas, min(bas + WHISPER_PARCA, boy)]} if boy else {}
        parca.append([(round(p.start, 3), p.text.strip()) for p in model.transcribe(str(ses), **k)[0] if p.text.strip()])
        yarim.write_text(json.dumps({"parca": parca}, ensure_ascii=False), encoding="utf-8")
    for s in [*d.glob("ses.*"), yarim]:  # ponytail: yarıda kalan ses diskte kalır; bitince silinir
        s.unlink()
    seg = m.segmentle([tuple(x) for p in parca for x in p], meta.get("chapters"), boy or None)
    _yaz(d, seg)
    print("\n".join(_ozet_satir(d, meta, seg, f"whisper {ns.model}" + (f", ilk {ns.en_fazla_dk} dk" if kes else ""))))
    return 0


def temizle(ns, ctx):
    sinir, n = time.time() - ns.gun * 86400, 0
    for d in ctx["kok"].iterdir() if ctx["kok"].is_dir() else []:
        if d.is_dir() and d.stat().st_mtime < sinir:
            shutil.rmtree(d)
            n += 1
    print(f"{n} video klasörü silindi ({ns.gun} günden eski) · {ctx['kok']}")
    return 0


def altin(ns, ctx):  # VİDEO-GÖZ-1a K4: rapor.md altın JSON'a karşı (salt okur)
    f, s = (au.kapsam, au.kapsam_satirlar) if ns.eylem == "kapsam" else (au.puan, au.satirlar)
    for x in s(f(Path(ns.rapor).read_text(encoding="utf-8"), json.loads(Path(ns.altin).read_text(encoding="utf-8")))):
        print(x)
    return 0


def main(argv=None, env=None, kos=kos, gonder=None, uyku=time.sleep, al=None):
    argv = [a.rstrip("\r") for a in (sys.argv[1:] if argv is None else argv)]  # 24e-1 K2: CRLF listeden gelen yol
    if argv[:1] == ["--whisper"]:
        argv[0] = "whisper"
    argv = ["\0" + a if re.fullmatch(r"-\w[\w-]{9}", a, re.A) else a for a in argv]  # M8 K1: tireli kimlik (-_S3KD0ZIfI) argparse'ta seçenek sanılmasın
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
    x.add_argument("--model-tavan", type=int, help="O11 (5): modele giden en fazla M kare (varsayılan --kare); --kare aday tabanı kalır")
    x.add_argument("--kare-yalniz", action="store_true", help="M8 K2: segmentleri yok say (whisper çıktısı anlamsız) → kare-yalnız paket")
    x.add_argument("--incelenmedi", action="store_true", help="C4 ikinci geçiş: yalnız kapsam.json'daki incelenmedi anlar (ilk paket → paket-1.md)")
    x.add_argument("--kuyruk", metavar="MD", help="B ek: açıklama/yorum/sayfa video linkleri bu kuyruğa (yoksa); verilmezse kuyruğa dokunulmaz")
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
    x.add_argument("adaylar", nargs="+", type=str.strip)
    x.add_argument("--yeniden", action="store_true", help="kayıttaki adları da değerlendir")
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M Jev isteği (varsayılan 7·aday)")
    x = alt.add_parser("bizde", help="aday.md → jev skill (2 istek/aday); p≥act skill'ler ## Bizde durum'a")
    x.add_argument("adaylar", nargs="+", type=str.strip)
    x.add_argument("--istek-tavan", type=int, metavar="M", help="en fazla M Jev isteği (varsayılan 2·aday)")
    x = alt.add_parser("kural-onay", help="bekleyen/kural-<slug>.md → omer-kurallar.md'ye madde (çiftse eklenmez); yalnız CC, köprüde yok")
    x.add_argument("slug")
    x.add_argument("--kapsam", required=True, help="23c: maddenin geçerli olduğu kapsam (ör. 'site/UI yapım promptlarında'); kapsamsız onay yok")
    x = alt.add_parser("yeniden", help="VİDEO-YENİDEN-1: eski raporların kalemleri bugünkü hattan (izleme/araştırıcı/claude -p yok) → docs/kurulumlar/yeniden/<tarih>-toplu.md")
    x.add_argument("--son", default="2026-09-18", help="bu tarihe kadarki etiketsiz kayıt satırları")
    x.add_argument("--istek-tavan", type=int, default=600)
    x.add_argument("--yalniz", metavar="DOSYA", help="1b: yalnız bu kalemler (satır: id<TAB>ad); etiket önceki+'b', rapora '## Düzeltme (1b)' eki")
    x = alt.add_parser("getir", help="23c K2: sayfa → ana metin (gezinme/altbilgi atılır) başlık + ilk N karakter + bağlantılar; önbellek getir/")
    x.add_argument("url")
    x.add_argument("--n", type=int, default=6000)
    x = alt.add_parser("repo", help="23c K2: gh api → README ilk 120 satır · ağaç derinlik 2 · --dosya yalnız --satir a-b (≤200)")
    x.add_argument("ad", help="sahip/ad")
    x.add_argument("--dosya")
    x.add_argument("--satir", metavar="a-b")
    x = alt.add_parser("kaynak", help="24e-2 K2: videosuz kaynak (GitHub repo/alt klasör · web sayfası) → kayıt + kurulu kontrolü + on; rapor docs/kurulumlar/kaynak-<slug>.md")
    x.add_argument("url")
    x.add_argument("--tur", default="araç")
    x = alt.add_parser("kuyruk", help="24e-2 K6: kuyruk.md sıradaki parti önerisi; --isle id,… --commit sha yalnız durum sütununu yazar")
    x.add_argument("eylem", nargs="?", choices=["yenile"], help="A8: dk/başlığı '?' satırları metadata ile yeniden doldur")
    x.add_argument("--dosya")
    x.add_argument("--isle")
    x.add_argument("--commit")
    x = alt.add_parser("on", help="23c K4: aday ön getirme → <kök>/.kos/<video>/<aday>/on.md (repo özeti + site özeti); 24b K1: --repo → sığ klon + SkillSpector ön taraması")
    x.add_argument("video")
    x.add_argument("aday")
    x.add_argument("--repo")
    x.add_argument("--tur", help="24c K1: hat iskeletinin tür alanı (skill · plugin · MCP · CLI · prompt …)")
    x.add_argument("--url")
    x.add_argument("--rapor", help="24a K2: tarama raporu; tür=prompt satırının zamanından paket altyazısıyla prompt metni (≤4000) on.md'ye")
    x = alt.add_parser("onay", help="bekleyen/<ad>.md yapılandırılmış adımlar → kur · duman · başarısızsa geri alma; yalnız CC, köprüde yok")
    x.add_argument("ad")
    x.add_argument("--kuru", action="store_true", help="hiçbir şey koşmaz, planı yazar")
    x = alt.add_parser("koru", help="20b: ~/.claude parmak izi; --al önce, sonra `-- komut` koşup karşılaştırır; fark → geri yükle + rc 1 (DUR)")
    x.add_argument("--al", action="store_true", help="parmak izi + yedek al (docs/denemeler/.kos/caveman/)")
    x.add_argument("--agsiz", action="store_true", help="komutun env'inde API anahtarı yok, BASE_URL ölü port")
    x.add_argument("arg", nargs=argparse.REMAINDER, metavar="-- komut")
    x = alt.add_parser("geri-al", help="kayıttaki geri_alma adımları + köprü girdisini çıkarır; yalnız CC")
    x.add_argument("ad")
    x = alt.add_parser("dene", help="docs/denemeler/<ad>.md → claude -p kollar (sonnet, kol başına 2 koşu, karışık sıra): görev başarısı + Jev kalite; karar sıcak maliyetle; yalnız CC")
    x.add_argument("ad")
    x.add_argument("--tavan", type=int, default=24, help="en fazla N claude -p (görev × kol × 2)")
    x.add_argument("--gorevler", type=lambda s: s if re.fullmatch(r"[\w-]+", s) else int("x"), metavar="SET", help="docs/denemeler/gorevler-<SET>/ (örn. okuma)")
    x.add_argument("--istek-tavan", type=int, default=30, metavar="M", help="en fazla M Jev isteği")
    x = alt.add_parser("uret", help="docs/uyarlamalar/<ad>.md → taslak denetimi (tavan · tetik · 8-gram · KAYNAK.md) → dene → bekleyen/zip ya da bilgi kartı; yalnız CC")
    x.add_argument("ad")
    x.add_argument("--tavan", type=int, default=24, help="en fazla N claude -p (görev × kol × 2)")
    x.add_argument("--istek-tavan", type=int, default=30, metavar="M", help="en fazla M Jev isteği")
    x.add_argument("--tur", type=int, metavar="N", help="23b AYRIŞTIR onarım turu (0 ilk ölçüm, en fazla 2); tur ≤12, toplam ≤24 claude -p")
    x = alt.add_parser("karar", help="23b: SOR bekleyen → Ömer'in AL|RED kararı (dene yeniden koşmaz); yalnız CC")
    x.add_argument("ad")
    x.add_argument("secim", choices=["AL", "RED", "ERTELE"])
    alt.add_parser("takas-geri", help="23b K9/K11: deneme sonuçları takas tablosuyla yeniden + mekanizma kaydı + ayrıştırma adayı (claude -p 0, Jev 0)")
    alt.add_parser("durum", help="docs/durum.md: köprü katalogu · son kararlar · ölçüm bulguları · ELE (≤3k token, elle bölüm korunur)")
    x = alt.add_parser("bilgi", help="bilgi/ kartları: guven · bayatlama · iddia")
    x.add_argument("--bayat", action="store_true", help="yalnız bayatlamış (yeniden doğrula)")
    x = alt.add_parser("brief", help="uygula raporu → Desktop ikinci görüş girdisi ≤60 satır: özellik kararları · iddialar · linkler")
    x.add_argument("rapor")
    x = alt.add_parser("departman", help="19: aktif skill/plugin/MCP/köprü CLI → Jev choice → docs/departmanlar/ (elle.json kazanır, hash önbellek)")
    x.add_argument("--yeniden", action="store_true", help="önbelleği yok say (elle.json yine kazanır)")
    x.add_argument("--istek-tavan", type=int, default=450, metavar="M", help="en fazla M Jev isteği")
    alt.add_parser("projeler", help="docs/projeler.md: proje CLAUDE.md'lerinden 1-2 satır özet (mtime'la yenilenir)")
    alt.add_parser("ajan-denetle", help="23 K1: SKILL.md/ajan tanımlarındaki her subagent_type → .claude/agents'ta var · model sonnet · tools dar")
    alt.add_parser("t0-regresyon", help="24c K2/K4: tests/fixture/t0-tur.json → T0 türü ≥7/8 + prompt/kural ZATEN VAR 2/2 (canlı Jev ≤16 + ≤6)")
    x = alt.add_parser("kural-regresyon", help="23 K3: tests/fixture/kural-cifti.json → bilinen çiftler ÇİFT, yanlış pozitif değil (canlı Jev)")
    x.add_argument("--istek-tavan", type=int, default=40, metavar="M", help="en fazla M Jev isteği")
    x = alt.add_parser("departman-geri", help="23 K2: kayit.jsonl'de departmansız karar kayıtları → departman + katalog 'Videodan gelen'")
    x.add_argument("--istek-tavan", type=int, default=30, metavar="M", help="en fazla M Jev isteği")
    x = alt.add_parser("altin", help="VİDEO-GÖZ-1a: rapor.md'yi altın JSON'a karşı puanlar (LLM yok)")
    x.add_argument("eylem", choices=["puan", "kapsam"])  # 1b-1 M0: kapsam rapor yerine paket.md alır
    x.add_argument("rapor")
    x.add_argument("altin")
    x = alt.add_parser("teknik", help="23 K5: rapor Site/UI teknikleri → ÖĞREN kartı (frontend) ya da UYARLA bekleyen; frontend katalog ## Teknikler")
    x.add_argument("raporlar", nargs="+")
    x = alt.add_parser("temizle", help="eski önbellek klasörlerini siler")
    x.add_argument("--gun", type=int, default=14)
    x = alt.add_parser("tara", help="tarayıcı kolu: sonnet/haiku ajan satırı · openrouter:<model> rapor (TOKEN-DENEME-2a)")
    x.add_argument("id")
    x.add_argument("--kol", required=True, help="sonnet | haiku | openrouter:<model>")
    x.add_argument("--kare", type=int, default=0, help="openrouter vision: gönderilecek kare (≤6; short ≤3)")
    x.add_argument("--tarih")
    x = alt.add_parser("parti", help="MOTOR-M2a: kuyruk → paket → hafif claude -p tarayıcı formu → rapor + kayıt; .kos/<parti-id>/durum.json + defter.jsonl")
    x.add_argument("eylem", choices=["baslat", "kuyruk", "link", "devam", "durum", "akil", "kapat", "iptal", "denetim-isle"])
    x.add_argument("--kayit", metavar="JSONL", help="MÜKEMMEL-7c U10: rapor kaydı (varsayılan tarama dizini kayit.jsonl)")
    x.add_argument("--neden", help="iptal: M12 K3 — iptal nedeni (zorunlu)")
    x.add_argument("hedef", nargs="?", help="baslat/kuyruk: kuyruk.md (varsayılan docs/video-tarama/kuyruk.md) · devam/durum: parti-id")
    x.add_argument("--en-fazla", type=int, default=8, metavar="N")
    g = x.add_mutually_exclusive_group()
    g.add_argument("--short", action="store_true")
    g.add_argument("--uzun", action="store_true")
    x.add_argument("--model", default=pt.hafif.MODEL)
    x.add_argument("--cagri-tavan", type=int, default=12, help="parti başında sabit model çağrısı tavanı")
    x.add_argument("--usd-tavan", type=float, default=1.0, help="parti başında sabit $ tavanı (CLI total_cost_usd)")
    x.add_argument("--cagri-tavan-max", type=int, default=30, help="M6 K3: dinamik tavan genişlemesinin parti başı çağrı üst sınırı")
    x.add_argument("--usd-tavan-max", type=float, default=2.0, help="M6 K3: dinamik tavan genişlemesinin parti başı $ üst sınırı")
    x.add_argument("--butce", type=float, default=0.5, help="çağrı başı --max-budget-usd")
    x.add_argument("--tarih")
    x.add_argument("--tum", action="store_true", help="akil: tüm kayıt genelinde birleştir")
    x.add_argument("--form-red-yeniden", action="store_true", help="devam: form_red videolara yeniden deneme hakkı")
    x.add_argument("--kismi-kabul", action="store_true", help="devam: M2e — form_red videoları diskteki son formdan tamam_eksik (çağrısız)")
    x.add_argument("--ikinci-goz", choices=("luna", "yok"), default="yok", help="M5: Sonnet sonrası luna ikinci göz (M5b: varsayılan yok — kaliteyi düşürdü)")
    x.add_argument("--yeniden-tara", action="store_true", help="devam: M2d — tamam/form_red/tavan videoları düzeltilmiş girdiyle yeniden tara")
    x.add_argument("--paket-yeniden", action="store_true", help="devam --yeniden-tara ile: DERİNLİK-1 R4b — paket R4 ile yeniden kurulur (yorum + kare; ozet yok)")
    x.add_argument("--incelenmedi", action="store_true", help="devam: C4 — incelenmedi anı kalan videolar ikinci geçişte (paket --incelenmedi + yeniden tarama)")
    x.add_argument("--yeniden", action="store_true", help="akil: M2g K1 — geliştirme karşılaştırması yeniden (yalnız gelistir + panel)")
    x.add_argument("--cagri-ek", type=int, default=0, help="devam/akil/kapat: çağrı tavanını açıkça yükselt")
    x.add_argument("--a-yolu", action="store_true", help="devam: V10 rotasını bırak, A taşıyıcısıyla tara (OmniRoute yokken açık seçim)")
    x.add_argument("--usd-ek", type=float, default=0.0, help="devam/akil/kapat: $ tavanını açıkça yükselt")
    x = alt.add_parser("kanal", help="KANAL-1: liste → docs/video-tarama/kanallar.md · onay <md> → kanallar.json · envanter (onaylı, flat, indirme yok) · etiket → docs/olcumler/kanal-etiket.json")
    x.add_argument("eylem", choices=["liste", "onay", "envanter", "etiket", "coz", "ekle"])
    x.add_argument("--tavan", type=int, default=100, help="coz: en fazla yt-dlp isteği")
    x.add_argument("dosya", nargs="?")
    x.add_argument("--kanal", help="envanter: yalnız bu channel_id")
    x = alt.add_parser("panel", help="MOTOR-M2b: panel.md Ömer sütunu (AL/RED/ERTELE) → video karar; boş satır dokunulmaz")
    x.add_argument("eylem", choices=["uygula"])
    x.add_argument("panel")
    ns = p.parse_args(argv)
    geri = lambda x: x[1:] if isinstance(x, str) and x[:1] == "\0" else x  # noqa: E731
    vars(ns).update({k: [geri(y) for y in x] if isinstance(x, list) else geri(x) for k, x in vars(ns).items()})
    env = os.environ if env is None else env
    ctx = {"env": env, "kos": kos, "gonder": gonder, "uyku": uyku, "kok": Path(env.get("VIDEO_CACHE") or KOK), "al": al or gt._al,  # B2: sayfa okuyucu
           "gh": lambda a: json.loads(subprocess.run(["gh", *a], capture_output=True, text=True, encoding="utf-8", check=True).stdout)}  # DERİNLİK-1 R3
    try:
        return {"ozet": ozet, "suz": suz, "sor": sor, "kare": kare, "whisper": whisper, "temizle": temizle, "kayit": kayit, "adlar": adlar, "oku": oku, "paket": paket, "izle": izle,
                "rapor-denetle": rapor_denetle, "altin": altin, "tara": tara, "toplu": toplu, "kaynak": kaynak, "kuyruk": kuyruk, "kurallar": kurallar, "katman": uy.katman, "projeler": uy.projeler,
                "bizde": uy.bizde, "kural-onay": uy.kural_onay, "onay": kur.onay, "koru": kur.koru, "geri-al": kur.geri_al, "dene": kur.dene, "uret": kur.uret, "karar": kur.karar_isle, "takas-geri": kur.takas_geri, "durum": og.durum, "bilgi": og.bilgi, "brief": uy.brief, "departman": dp.departman,
                "ajan-denetle": uy.ajan_denetle, "kural-regresyon": kural_regresyon, "t0-regresyon": t0_regresyon, "departman-geri": uy.departman_geri, "teknik": uy.teknik,
                "getir": getir_, "repo": repo_, "on": on_, "yeniden": yeniden, "parti": pt.parti, "panel": pt.panel, "kanal": kn.kanal}[ns.komut](ns, ctx)
    except HizHata as e:
        print(f"hata: {e}")
        return 4
    except (Hata, c.JevHata, gt.GetirHata, kn.Hata) as e:
        print(f"hata: {e}")
        return 1


def calistir():
    for akis in (sys.stdout, sys.stderr):
        akis.reconfigure(encoding="utf-8")
    sys.exit(main())
