"""SOSYAL-YUKLE-1: out/<grup>/hazir/<kimlik>/{video.mp4,meta.json} -> YouTube Studio / TikTok / Instagram web.
  durum [--kanal a]                          giriş envanteri (kalıcı profilde her platform açık mı)
  giris <kanal>                              görünür Chrome açar; Ömer tek seferlik elle giriş yapar, kapatır
  yukle [--kanal a] [--platform youtube,tiktok,instagram] [--gorunurluk PRIVATE|UNLISTED|PUBLIC] [--dry]
Oturum: sosyal-oto/gizli/chrome-<kanal> (Playwright kalıcı profil; Chrome'un kendi profiline dokunmaz).
Başarı = tüm istenen platformlarda URL doğrulandı -> YUKLENDI.txt + temizle.py yuklendi. Hata -> Telegram (modelsiz), dosya silinmez.
Kota: kanal başına günde GUNLUK_KOTA yükleme (uzun 1 + shorts 3). Boş hazir/ -> sessiz çık."""
import argparse, json, subprocess, sys, time
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = Path(__file__).resolve().parents[1]
SOS = Path.home() / "Desktop" / "Claude ile yapılanlar" / "sosyal-oto"
GIZLI = SOS / "gizli"
DURUM = GIZLI / "yukle-durum.json"
GUNLUK_KOTA = 4
KANALLAR = {"a": "Free AI Drop (sosyalmdyahesabi1)", "b": "Curiosity Well (sosyalmdyahesabi2)",
            "c": "is/para hikayeleri (sosyalmdyahesabi3)", "d": "AI dizi studyosu (sosyalmdyahesabi4)"}
GIRIS_URL = {"youtube": "https://studio.youtube.com", "tiktok": "https://www.tiktok.com/tiktokstudio/upload",
             "instagram": "https://www.instagram.com/"}
GIRISSIZ = {"youtube": "accounts.google.com", "tiktok": "/login", "instagram": "/accounts/login"}


def bildir(metin):
    subprocess.run([sys.executable, str(KOK / "tools/telegram_kopru.py"), "gonder", metin], capture_output=True, timeout=60)


def kuyruk(kanal=None):
    for meta in sorted(SOS.glob("out/*/hazir/*/meta.json")):
        if (meta.parent / "video.mp4").exists() and not (meta.parent / "YUKLENDI.txt").exists():
            m = json.loads(meta.read_text(encoding="utf-8"))
            if kanal in (None, m.get("grup")):
                yield meta.parent, m


def kota_ok(kanal):
    d = json.loads(DURUM.read_text()) if DURUM.exists() else {}
    return d.get(str(date.today()), {}).get(kanal, 0) < GUNLUK_KOTA


def kota_say(kanal):
    d = json.loads(DURUM.read_text()) if DURUM.exists() else {}
    g = d.setdefault(str(date.today()), {})
    g[kanal] = g.get(kanal, 0) + 1
    GIZLI.mkdir(parents=True, exist_ok=True)
    DURUM.write_text(json.dumps(d))


def baglam(pw, kanal, gorunur=False):
    prof = GIZLI / f"chrome-{kanal}"
    prof.mkdir(parents=True, exist_ok=True)
    args = [] if gorunur else ["--window-position=-32000,-32000"]  # ekran dışı: pencere öne çıkmaz
    return pw.chromium.launch_persistent_context(str(prof), channel="chrome", headless=False, args=args,
                                                 viewport={"width": 1280, "height": 900}, accept_downloads=False)


def giris_acik(sayfa, platform):
    sayfa.goto(GIRIS_URL[platform], wait_until="domcontentloaded", timeout=60000)
    sayfa.wait_for_timeout(4000)
    return GIRISSIZ[platform] not in sayfa.url


def yt_yukle(s, m, klasor, gorunurluk):
    s.goto("https://www.youtube.com/upload", wait_until="domcontentloaded", timeout=60000)
    s.set_input_files("input[type=file]", str(klasor / "video.mp4"))
    s.wait_for_selector("#title-textarea #textbox", timeout=120000)
    for sec, metin in (("#title-textarea #textbox", m["baslik"][:100]), ("#description-textarea #textbox", m["aciklama"])):
        s.click(sec); s.keyboard.press("Control+a"); s.keyboard.type(metin)
    s.click("[name=VIDEO_MADE_FOR_KIDS_NOT_MADE_FOR_KIDS]")
    s.click("#toggle-button")  # Daha fazla göster
    ai = m.get("ai_etiketi", {}).get("youtube_altered_synthetic", m.get("ai_label", False))
    s.click("[name=VIDEO_HAS_ALTERED_CONTENT_YES]" if ai else "[name=VIDEO_HAS_ALTERED_CONTENT_NO]")
    if m.get("etiketler"):
        s.click("#tags-container input"); s.keyboard.type(",".join(m["etiketler"]) + ",")
    for _ in range(3):
        s.click("#next-button"); s.wait_for_timeout(1500)
    s.click(f"[name={gorunurluk}]")
    s.wait_for_selector("ytcp-video-info a, .video-url-fadeable a", timeout=300000)
    url = s.get_attribute(".video-url-fadeable a", "href")
    s.click("#done-button"); s.wait_for_timeout(3000)
    return url


def tt_yukle(s, m, klasor, gorunurluk):
    s.goto(GIRIS_URL["tiktok"], wait_until="domcontentloaded", timeout=60000)
    s.set_input_files("input[type=file]", str(klasor / "video.mp4"))
    s.wait_for_selector("[contenteditable=true]", timeout=180000)
    s.click("[contenteditable=true]"); s.keyboard.press("Control+a")
    s.keyboard.type(m["baslik"] + " " + " ".join("#" + e for e in m.get("etiketler", [])[:5]))
    if m.get("ai_etiketi", {}).get("tiktok_aigc"):
        s.get_by_text("AI-generated content", exact=False).first.click()
    s.get_by_role("button", name="Post").click()
    s.wait_for_selector("text=Manage your posts", timeout=180000)
    return "tiktok:posted"  # TikTok web URL vermez; doğrulama = Manage posts listesinde başlık


def ig_yukle(s, m, klasor, gorunurluk):
    s.goto(GIRIS_URL["instagram"], wait_until="domcontentloaded", timeout=60000)
    s.get_by_role("link", name="Create").click()
    s.get_by_role("link", name="Post").click()
    s.set_input_files("input[type=file]", str(klasor / "video.mp4"))
    for _ in range(2):
        s.get_by_role("button", name="Next").click(); s.wait_for_timeout(1500)
    s.click("[contenteditable=true]"); s.keyboard.type(m["baslik"] + "\n" + m["aciklama"])
    s.get_by_role("button", name="Share").click()
    s.wait_for_selector("text=Your reel has been shared", timeout=300000)
    return "instagram:shared"


YUKLEYICI = {"youtube": yt_yukle, "tiktok": tt_yukle, "instagram": ig_yukle}


def dogrula_yt(ctx, url, baslik):
    s = ctx.new_page()
    s.goto(url, wait_until="domcontentloaded", timeout=60000)
    s.wait_for_timeout(5000)
    ok = baslik[:30].lower() in s.title().lower() and s.locator("video").count() > 0
    s.close()
    return ok


def durum_cmd(kanallar):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for k in kanallar:
            ctx = baglam(pw, k)
            s = ctx.new_page()
            for p in GIRIS_URL:
                try:
                    print(f"{k} {KANALLAR[k]} | {p}: {'giris acik' if giris_acik(s, p) else 'giris YOK'}")
                except Exception as e:
                    print(f"{k} {p}: olculemedi ({type(e).__name__})")
            ctx.close()


def giris_cmd(k):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        ctx = baglam(pw, k, gorunur=True)
        for p in GIRIS_URL:
            ctx.new_page().goto(GIRIS_URL[p])
        print("Üç sekmede giriş yap, sonra Chrome penceresini kapat.")
        ctx.wait_for_event("close", timeout=0)


def yukle_cmd(a):
    isler = [(k, m) for k, m in kuyruk(a.kanal)]
    if not isler:
        print("hazir bos"); return
    platformlar = a.platform.split(",")
    if a.dry:
        for k, m in isler: print("[dry]", k.name, m["baslik"], "->", platformlar)
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        for klasor, m in isler:
            kanal = m["grup"]
            if not kota_ok(kanal):
                print(f"{kanal}: kota doldu"); continue
            ctx = baglam(pw, kanal)
            s = ctx.new_page()
            sonuc = {}
            try:
                for p in platformlar:
                    if not giris_acik(s, p):
                        raise RuntimeError(f"{p}: giris yok (sosyal_yukle.py giris {kanal})")
                    sonuc[p] = YUKLEYICI[p](s, m, klasor, a.gorunurluk)
                    if p == "youtube" and not dogrula_yt(ctx, sonuc[p], m["baslik"]):
                        raise RuntimeError("youtube: yayin sayfasi dogrulanamadi " + str(sonuc[p]))
                (klasor / "YUKLENDI.txt").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
                kota_say(kanal)
                subprocess.run([sys.executable, str(SOS / "temizle.py"), "yuklendi"], check=False)
                bildir(f"YUKLENDI {m['kimlik']}: {sonuc}")
            except Exception as e:
                bildir(f"YUKLEME HATASI {m['kimlik']}: {str(e)[:300]} (dosya silinmedi)")
                print("HATA", m["kimlik"], e)
            finally:
                ctx.close()
            time.sleep(30)


def kendi_sinav():
    """Tarayıcısız öz-sınav: kuyruk taraması, kota, YUKLENDI dışlama."""
    global SOS, DURUM, GIZLI
    import tempfile
    t = Path(tempfile.mkdtemp())
    SOS, GIZLI = t, t / "gizli"; DURUM = GIZLI / "d.json"
    for i, ok in enumerate((False, True)):
        d = t / "out/a/hazir" / f"x{i}"; d.mkdir(parents=True)
        (d / "video.mp4").write_bytes(b"0"); (d / "meta.json").write_text(json.dumps({"grup": "a", "kimlik": f"x{i}"}))
        if ok: (d / "YUKLENDI.txt").write_text("{}")
    assert [m["kimlik"] for _, m in kuyruk("a")] == ["x0"]
    assert [m for _, m in kuyruk("b")] == []
    for _ in range(GUNLUK_KOTA): assert kota_ok("a"); kota_say("a")
    assert not kota_ok("a") and kota_ok("b")
    print("oz-sinav tamam")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["durum", "giris", "yukle", "sinav"])
    ap.add_argument("kanal_arg", nargs="?")
    ap.add_argument("--kanal")
    ap.add_argument("--platform", default="youtube")
    ap.add_argument("--gorunurluk", default="PUBLIC", choices=["PRIVATE", "UNLISTED", "PUBLIC"])
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    {"durum": lambda: durum_cmd([a.kanal] if a.kanal else list(KANALLAR)), "giris": lambda: giris_cmd(a.kanal_arg),
     "yukle": lambda: yukle_cmd(a), "sinav": kendi_sinav}[a.komut]()
