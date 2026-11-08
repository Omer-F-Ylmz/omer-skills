"""POSTIZ-KUR-1: sosyal-oto hazir/ klasörünü izleyip Postiz kuyruğuna koyar (Claude çağırmaz).
Kullanım (python -I):
  yayinci.py kontrol                 Postiz erişimi + bağlı hesaplar + eşleme eksikleri
  yayinci.py esle                    bağlı hesapları buyume/hesaplar.json tutamaçlarıyla gruba eşler -> hesap-esle.json
  yayinci.py calistir [--zamanla] [--kuru]   hazir/*/video.mp4 -> upload + post (varsayılan TASLAK/özel; --zamanla ET slotlarına planlar)
  yayinci.py dongu                   5 dk'da bir calistir (taslak modu)
Sır: POSTIZ_API_KEY ortamdan, yoksa WSL /opt/postiz/.env'den okunur; yazdırılmaz."""
import json, os, subprocess, sys, time, datetime as dt
from pathlib import Path
from zoneinfo import ZoneInfo
import requests

BU = Path(__file__).resolve().parent
KOK = BU.parent.parent
SOSYAL = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-oto")
API = os.environ.get("POSTIZ_API_URL", "http://127.0.0.1:4007/api/public/v1")
ESLE, DURUM, LOG = BU / "hesap-esle.json", BU / "durum.json", BU / "yayinci.log"
SLOT_ET = ["12:00", "17:00", "20:30"]  # grup başına günde 3 (ABD prime, ET)
PLAT = {"youtube": "youtube", "instagram": "instagram", "tiktok": "tiktok"}


def log(m, hata=False):
    LOG.open("a", encoding="utf-8").write(f"{dt.datetime.now():%F %T} {'HATA ' if hata else ''}{m}\n")
    print(m)
    if hata:  # 2. beyin
        subprocess.run([sys.executable, "-I", str(KOK / "tools" / "beyin_kayit.py"), "olay", "hata", f"POSTIZ yayinci: {m}"[:300], "--hata"], capture_output=True)


def anahtar():
    k = os.environ.get("POSTIZ_API_KEY")
    if k:
        return k
    o = subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "-e", "grep", "^POSTIZ_API_KEY=", "/opt/postiz/.env"], capture_output=True, text=True).stdout.strip()
    return o.split("=", 1)[1] if "=" in o else ""


_acik = []


def istek(yol, **kw):
    if not _acik:
        sys.path.insert(0, str(BU))
        import postiz_ac
        postiz_ac.ac()
        _acik.append(1)
    return requests.request(kw.pop("m", "GET"), API + yol, headers={"Authorization": anahtar()}, timeout=300, **kw)


def hesaplar():
    r = istek("/integrations")
    r.raise_for_status()
    return r.json()


def esle():
    tut = json.loads((SOSYAL / "buyume" / "hesaplar.json").read_text(encoding="utf-8"))
    sonuc = {g: {} for g in tut}
    for h in hesaplar():
        ad = f"{h.get('name','')} {h.get('profile','')}".lower().replace(" ", "")
        for g, t in tut.items():
            if any(v and v.lstrip("@").lower() in ad for v in t.values()):
                sonuc[g][h["identifier"].split("-")[0]] = h["id"]
    ESLE.write_text(json.dumps(sonuc, indent=1), encoding="utf-8")
    log(f"esle: {({g: sorted(v) for g, v in sonuc.items()})}")


def kontrol():
    try:
        hs = hesaplar()
    except Exception as e:
        return log(f"Postiz erişilemiyor: {e}", True)
    for h in hs:
        if h.get("disabled") or h.get("refreshNeeded"):
            log(f"hesap oturumu düştü/devre dışı: {h.get('identifier')} {h.get('name')}", True)
    log(f"bağlı hesap {len(hs)}; eşleme {'var' if ESLE.exists() else 'YOK (esle çalıştır)'}")


def sonraki_slot(grup, durum):
    et = ZoneInfo("America/New_York")
    now = dt.datetime.now(et)
    dolu = set(durum.get("slotlar", {}).get(grup, []))
    for gun in range(0, 14):
        for s in SLOT_ET:
            t = dt.datetime.combine((now + dt.timedelta(days=gun)).date(), dt.time.fromisoformat(s), et)
            if t > now + dt.timedelta(minutes=10) and t.isoformat() not in dolu:
                return t
    raise RuntimeError("14 günde boş slot yok")


def yayin(klasor, zamanla, kuru, esl, durum):
    meta = json.loads((klasor / "meta.json").read_text(encoding="utf-8"))
    grup = {"a": "free-ai-drop", "b": "curiosity-well"}.get(meta["grup"], meta["grup"])
    hed = esl.get(grup, {})
    if not hed:
        return log(f"{klasor.name}: {grup} için bağlı hesap yok, atlandı", True)
    t = sonraki_slot(grup, durum) if zamanla else dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
    pl, yazi = meta.get("platform", {}), (klasor / "metin.txt").read_text(encoding="utf-8") if (klasor / "metin.txt").exists() else ""
    posts = []
    if kuru:
        return log(f"[kuru] {klasor.name} -> {grup} {sorted(hed)} {'slot ' + t.isoformat() if zamanla else 'taslak'}")
    with open(klasor / "video.mp4", "rb") as f:
        up = istek("/upload", m="POST", files={"file": ("video.mp4", f, "video/mp4")})
    up.raise_for_status()
    med = {"id": up.json()["id"], "path": up.json()["path"]}
    for p, iid in hed.items():
        m = pl.get(p, {})
        baslik = (m.get("title") or meta.get("baslik") or "")[:90]
        govde = m.get("description") or m.get("caption") or meta.get("aciklama") or yazi
        ayar = {"youtube": {"__type": "youtube", "title": baslik[:100], "type": "private" if not zamanla else "public", "selfDeclaredMadeForKids": "no"},
                "tiktok": {"__type": "tiktok", "title": baslik, "privacy_level": "SELF_ONLY", "duet": False, "stitch": False, "comment": True, "autoAddMusic": "no",
                           "brand_content_toggle": False, "brand_organic_toggle": False, "video_made_with_ai": True, "content_posting_method": "UPLOAD"},
                "instagram": {"__type": "instagram", "post_type": "post"}}[p]
        posts.append({"integration": {"id": iid}, "value": [{"content": govde, "image": [med]}], "group": klasor.name, "settings": ayar})
    r = istek("/posts", m="POST", json={"type": "schedule" if zamanla else "draft", "date": t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"), "shortLink": False, "tags": [], "posts": posts})
    if r.status_code >= 300:
        return log(f"{klasor.name}: post {r.status_code} {r.text[:200]}", True)
    (klasor / "POSTIZ-KUYRUK.json").write_text(json.dumps({"mod": "zamanla" if zamanla else "taslak", "tarih": t.isoformat(), "kaynak": "yayinci"}), encoding="utf-8")
    if zamanla:
        durum.setdefault("slotlar", {}).setdefault(grup, []).append(t.isoformat())
        DURUM.write_text(json.dumps(durum), encoding="utf-8")
    log(f"{klasor.name}: kuyruğa alındı ({'zamanlı ' + t.isoformat() if zamanla else 'taslak'}), {len(posts)} platform")


def calistir(zamanla, kuru):
    esl = json.loads(ESLE.read_text(encoding="utf-8")) if ESLE.exists() else {}
    durum = json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else {}
    for k in sorted(SOSYAL.glob("out/*/hazir/*/video.mp4")):
        if not (k.parent / "POSTIZ-KUYRUK.json").exists() and (k.parent / "meta.json").exists():
            try:
                yayin(k.parent, zamanla, kuru, esl, durum)
            except Exception as e:
                log(f"{k.parent.name}: {type(e).__name__} {e}"[:250], True)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["kontrol"]:
        kontrol()
    elif a[:1] == ["esle"]:
        esle()
    elif a[:1] == ["calistir"]:
        calistir("--zamanla" in a, "--kuru" in a)
    elif a[:1] == ["dongu"]:
        while True:
            kontrol(); calistir(False, False); time.sleep(300)
    else:
        print(__doc__)
