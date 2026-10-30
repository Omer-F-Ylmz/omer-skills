"""Sosyal medya herkese açık sayaç ölçümü (0 token, model/anahtar yok). YT/TikTok/IG, günlük.
Kullanım: python tools/sosyal_olcum.py [olc | kural | ozet]
  olc   : hesaplar.json'daki her hesabın takipçi + son videolarının sayaçlarını çekip olcum.jsonl'e ekler
  kural : ilk ~48 saat performansından kanca/konu ağırlıklarını hesaplar -> agirlik.json
  ozet  : Telegram 'durum' için kısa metin (telegram_kopru.ozet ekler)
hesaplar.json: {"free-ai-drop": {"yt": "@freeaidrop", "tt": "freeaidrop", "ig": "freeaidrop"}, ...}  (boş/eksik alan atlanır)
Veri dizini: Desktop\\Claude ile yapılanlar\\sosyal-oto\\buyume\\"""
import json, os, re, statistics, subprocess, sys, time
from pathlib import Path

DIZ = Path.home() / "Desktop" / "Claude ile yapılanlar" / "sosyal-oto" / "buyume"
HESAP, OLCUM, AGIRLIK = DIZ / "hesaplar.json", DIZ / "olcum.jsonl", DIZ / "agirlik.json"
URL = {"yt": "https://www.youtube.com/{}/shorts"}
SAAT = 3600
MARKA = {"a": "free-ai-drop", "b": "curiosity-well"}  # hat.py grup -> hesaplar.json marka


def _yt_dlp(url, n=15):
    p = subprocess.run(["yt-dlp", "-J", "--flat-playlist", "--playlist-end", str(n), "--no-warnings", url],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180, env=os.environ.copy(), creationflags=0x08000000 if sys.platform == "win32" else 0)
    if p.returncode or not p.stdout.strip():
        return None, (p.stderr.strip().splitlines() or ["çıktı yok"])[-1][:160]
    return json.loads(p.stdout), None


def _sayi(t):
    """'96,482,343' / '686M' / '1.2K' -> int"""
    t = t.replace(",", "")
    k = {"K": 1e3, "M": 1e6, "B": 1e9}.get(t[-1:].upper())
    return int(float(t[:-1]) * k) if k else int(float(t))


def _web(platform, kimlik):
    """TikTok/IG: düz HTTP bot duvarına çarpar; başsız Chrome ile profil sayfasından takipçi (hesap düzeyi; video listesi yok)."""
    from playwright.sync_api import sync_playwright
    url, desen = (f"https://www.tiktok.com/@{kimlik}", r'followerCount"\s*:\s*"?(\d+)') if platform == "tt" else                  (f"https://www.instagram.com/{kimlik}/", r"([\d.,]+[KMB]?) Followers")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome", headless=True)
            try:
                pg = b.new_page(locale="en-US")
                pg.goto(url, timeout=40000, wait_until="domcontentloaded")
                pg.wait_for_timeout(4000)
                m = re.search(desen, pg.content())
            finally:
                b.close()
    except Exception as e:
        return None, f"{platform} sayfası açılamadı: {type(e).__name__}"
    return ({"takipci": _sayi(m.group(1)), "videolar": []}, None) if m else (None, f"{platform} takipçi sayısı sayfada yok (giriş duvarı/hesap yok)")


def olc_hesap(platform, kimlik):
    if platform in ("tt", "ig"):
        return _web(platform, kimlik)
    d, hata = _yt_dlp(URL[platform].format(kimlik))
    if hata and "shorts tab" in hata:  # henüz Shorts yok: takipçi için videolar sekmesi
        d, hata = _yt_dlp(URL[platform].format(kimlik).replace("/shorts", "/videos"))
    if hata and "does not have a" in hata:  # kanal var ama henüz video yok
        return {"takipci": None, "videolar": []}, None
    if hata:
        return None, hata
    v = [{"id": e.get("id"), "baslik": e.get("title") or "", "izlenme": e.get("view_count"), "begeni": e.get("like_count"),
          "yorum": e.get("comment_count")} for e in d.get("entries", [])]
    return {"takipci": d.get("channel_follower_count") or d.get("playlist_count"), "videolar": v}, None


def olc():
    if not HESAP.exists():
        print(f"hesaplar.json yok: {HESAP} (hesaplar açılınca doldurulur)"); return 0
    DIZ.mkdir(parents=True, exist_ok=True)
    ts, satir, hatalar = int(time.time()), [], []
    for marka, h in json.loads(HESAP.read_text(encoding="utf-8")).items():
        for plat, kimlik in h.items():
            if not kimlik:
                continue
            s, hata = olc_hesap(plat, kimlik)
            if hata:
                hatalar.append(f"{marka}/{plat}: {hata}"); continue
            satir.append({"ts": ts, "marka": marka, "plat": plat, "takipci": s["takipci"], "videolar": s["videolar"]})
    with OLCUM.open("a", encoding="utf-8", newline="\n") as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in satir)
    print(f"yazılan hesap: {len(satir)}; ölçülemedi: {len(hatalar)}")
    for h in hatalar:
        print(" -", h)
    return 0


# ---- kural tablosu ----
# oran = videonun ~48. saat izlenmesi / aynı hesabın önceki videolarının 48s medyanı
KURAL = [(2.0, 1.5), (1.0, 1.1), (0.5, 1.0), (0.2, 0.6), (0.0, 0.3)]  # (alt sınır, çarpan)
TAVAN, TABAN, MIN_VIDEO = 3.0, 0.2, 3


def kural_carpan(oran):
    return next(c for sinir, c in KURAL if oran >= sinir)


def izlenme_48s(snapshotlar, ilk_ts):
    """[(ts, izlenme)] içinden yayından 36-72 saat sonrasına düşen ve 48 saate en yakın olanı."""
    aday = [(abs((t - ilk_ts) / SAAT - 48), v) for t, v in snapshotlar if 36 <= (t - ilk_ts) / SAAT <= 72 and v is not None]
    return min(aday)[1] if aday else None


def agirlik_hesapla(olcumler, etiket):
    """olcumler: jsonl satırları; etiket: {(marka, video_id): {"kanca_tip":..,"konu_tip":..}} -> {tip: ağırlık}"""
    gor = {}  # (marka, plat, id) -> [(ts, izlenme)], ilk görülme = yayın zamanı yaklaşığı
    for o in olcumler:
        for v in o["videolar"]:
            gor.setdefault((o["marka"], o["plat"], v["id"]), []).append((o["ts"], v["izlenme"]))
    v48 = {k: izlenme_48s(s, min(t for t, _ in s)) for k, s in gor.items()}
    sonuc = {}
    for marka in {k[0] for k in v48}:
        degerler = [v for k, v in v48.items() if k[0] == marka and v is not None]
        if len(degerler) < MIN_VIDEO:
            continue
        taban = statistics.median(degerler)
        for k, v in v48.items():
            if k[0] != marka or v is None or taban <= 0:
                continue
            e = etiket.get((marka, k[2]), {})
            for alan in ("kanca_tip", "konu_tip"):
                tip = e.get(alan)
                if tip:
                    a = sonuc.setdefault(marka, {}).setdefault(f"{alan}:{tip}", 1.0)
                    sonuc[marka][f"{alan}:{tip}"] = min(TAVAN, max(TABAN, a * kural_carpan(v / taban)))
    return sonuc


def kanca_tip(hook):
    """Kanca metninden tip: soru / liste (sayı ile başlar) / uyari (stop, never, don't) / iddia."""
    h = (hook or "").strip().lower()
    if h.endswith("?"):
        return "soru"
    if re.match(r"\d", h):
        return "liste"
    if re.match(r"(stop|never|don't|dont|quit|avoid)\b", h):
        return "uyari"
    return "iddia"


def _etiketler():
    e = {}
    for m in (DIZ.parent / "out").glob("*/*/meta.json"):
        j = json.loads(m.read_text(encoding="utf-8"))
        for marka_id in (j.get("yayin_id") or {}).values():
            e[(MARKA.get(j.get("grup"), j.get("grup")), marka_id)] = j
    return e


def kural():
    if not OLCUM.exists():
        print("olcum.jsonl yok"); return 0
    o = [json.loads(s) for s in OLCUM.read_text(encoding="utf-8").splitlines() if s.strip()]
    a = agirlik_hesapla(o, _etiketler())
    AGIRLIK.write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"agirlik.json: {sum(len(v) for v in a.values())} tip"); return 0


def ozet():
    if not OLCUM.exists():
        return "SOSYAL: ölçüm yok"
    son = {}
    for s in OLCUM.read_text(encoding="utf-8").splitlines():
        if s.strip():
            j = json.loads(s); son[(j["marka"], j["plat"])] = j
    if not son:
        return "SOSYAL: ölçüm yok"
    return "SOSYAL " + " · ".join(f"{m}/{p}: {'?' if j['takipci'] is None else j['takipci']} takip, {sum(v['izlenme'] or 0 for v in j['videolar'])} izl, {time.strftime('%d %b', time.localtime(j['ts']))}"
                                  for (m, p), j in sorted(son.items()))


if __name__ == "__main__":
    sys.stdout and sys.stdout.reconfigure(encoding="utf-8")  # pythonw: stdout yok
    k = sys.argv[1] if len(sys.argv) > 1 else "olc"
    sys.exit({"olc": olc, "kural": kural, "ozet": lambda: print(ozet()) or 0}[k]())
