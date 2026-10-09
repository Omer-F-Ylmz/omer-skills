"""MOTOR-M2a: parti motoru çekirdeği — aşama 1 kuyruk · 2 paket · 3-4 hafif tarayıcı formu + doğrulama + rapor · 10 defter.
Durum .kos/<parti-id>/durum.json (her adımda atomik), defter .kos/<parti-id>/defter.jsonl (model çağrısı başına satır)."""
import io
import json
import os
from contextlib import contextmanager, redirect_stdout
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from importlib.util import find_spec
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from jev import cekirdek as c

from . import hafif
from . import metin as m
from . import ikinci_goz as ig
from . import tarama as tr
from . import yonlendir as yon

IG_TAVAN = {"or_usd": .10, "jev": 150, "yargic": 8}  # M5: parti başına ikinci göz tavanları (OpenRouter $ · Jev durum · yargıç çağrı)
YENIDEN = {"bekliyor", "hata", "tavan", "yeniden"}
GECICI, SON_TUR_SN = re.compile(r"boş yanıt|HTTP (429|5\d\d)\b|zaman aşımı|timed? ?out", re.I), 60  # MÜKEMMEL-8a: geçici hata A'ya gitmez, parti sonunda bir tur
gecici = lambda h: bool(GECICI.search(h or ""))
ERISILEMEZ = ((r"members[- ]only|Join this channel|channel's members", "üyelere özel"), (r"Private video", "özel video"),
              (r"Video unavailable|has been removed|\bremoved\b", "kaldırılmış / yok"), (r"Sign in to confirm your age", "yaş doğrulaması"))  # ONARIM-3: kalıcı; 403 değil


def erisilemez(cikti):
    """yt-dlp çıktısında kalıcı erişim hatası → kısa sebep, yoksa None."""
    return next((s for k, s in ERISILEMEZ if re.search(k, cikti or "", re.I)), None)


YAZ = threading.RLock()  # YT1 3: kayit.jsonl · defter.jsonl · durum.json yazımı ve d değişiklikleri; ponytail: tek global kilit; darboğaz olursa dosya başına kilit
CAGIR = threading.Semaphore(6)  # YT1 3: eşzamanlı model çağrısı


@contextmanager
def asama(kimlik, ad):
    """YT1 3: aşama zamanlaması stderr'e (paket.md'ye değil): [aşama] <id> <ad> başla <iso> · bitti <iso> <sn>."""
    t0, an = time.monotonic(), lambda: datetime.now().isoformat(timespec="seconds")
    print(f"[aşama] {kimlik} {ad} başla {an()}", file=sys.stderr, flush=True)
    try:
        yield
    finally:
        print(f"[aşama] {kimlik} {ad} bitti {an()} {time.monotonic() - t0:.1f}", file=sys.stderr, flush=True)


class _Yon:
    """YT1 3: sys.stdout vekili — _yakala() iş parçacığı başına yakalar (redirect_stdout süreç geneli)."""

    def __init__(self, asil):
        self.asil, self.yer = asil, threading.local()

    def write(self, x):
        return (b if (b := getattr(self.yer, "b", None)) is not None else self.asil).write(x)

    def __getattr__(self, a):
        return getattr(self.asil, a)


@contextmanager
def _yakala():
    if not isinstance(y := sys.stdout, _Yon):
        with redirect_stdout(io.StringIO()) as b:
            yield b
        return
    y.yer.b = b = io.StringIO()
    try:
        yield b
    finally:
        y.yer.b = None
BUTCE_YOK = "tavan: yeniden istek bütçesi yok"  # M5b K2
YONLENDIRME = {"tarama": {"yontem": "ikili", "modeller": ["claude-sonnet-5-5", "claude-haiku-5-5"]}}  # 1b-2a KAPANIŞ: yeni parti tarama kurgu 2 (sonnet + haiku claude -p, birlestir) · geri alma: bu satır {} ya da durum.json'dan "yonlendirme" silinir
# geri alma (V10): YONLENDIRME = {"tarama": {"saglayici": "omniroute", "model": "openrouter/google/gemini-3.5-flash-lite", "yontem": "V10"}}  # DERİNLİK-KAPANIŞ-1
SHORT_GRUP, GIRDI_TAVAN = 8, 40_000  # parti-motoru.md: short grubu ≤8, çağrı girdisi ≤40k jeton
BOZUK_ESIK = 0.25  # ayar · C1: anlamsız kelime oranı bunu aşan altyazı bozuk → whisper
KARE_UST = 60  # ayar · C4 (O11): uzun videoda modele giden kare güvenlik üst sınırı; asıl sınır cli.PAKET_BUTCE (Ömer onayı: tavan 20 → bütçe)
WHISPER_RAM_GB, WHISPER_HIZ = 6, 0.5  # ayar · C1: whisper öncesi en az boş RAM · tahmini işlem sn / ses sn (ponytail: kaba, CPU small int8; ölçümle güncellenir)
AGIR = re.compile(r"^(?:blender|genshinimpact|yuanshen|zenlesszonezero|starrail|client-win64-shipping|testhost)\.exe\b|pytest|dotnet\S* test",
                  re.I | re.M)  # ayar · C1 ağır süreç: Blender · oyun (tam süreç adı; blender-mcp sayılmaz) · tam suit (komut satırı)
KARE_TK = 1_600  # O11: yalnız dosyası okunamayan kare için; asıl hesap girdi_tk (gerçek boyut, cli._kare_tk)
SISTEM = ("Video tarayıcısısın. Her VIDEO bloğu bir paket: künye, açıklama bağlantıları, altyazı segmentleri, kare listesi. "
          "Her video için formu Türkçe ve eksiksiz doldur; zorunlu alanlar boş olamaz. Zamanlar m:ss ve video süresi içinde "
          "(yalnız açıklamada geçiyorsa 'açıklama'). Açıklama bağlantılarının HER biri için karar ver (aday_mi + neden); erişilemeyende (ücretli topluluk, giriş gerekli) "
          "aday_mi false + erisilemez: <sebep>. "
          "Alıntı en fazla 15 kelime. Kareden okunan bilgide kaynak 'kare' (ekli görseller, sırası bloklardaki kare listesiyle aynı). "
          "Anahtar, şifre, token değeri yazma. Site/landing/frontend içerikli videoda site_ui doldur. Emin olmadığını belirsizliklere yaz. "
          "Gösterilen ya da söylenen her kurulum/terminal komutunu kurulum_komutlar'a yaz (komut · ne yapar · zaman · kaynak). "
          "iz (D1, şema 2): videoda anılan HER şey (konuşma m:ss · kare m:ss · açıklama · yorum · linkli sayfa) bir satır — baglandigi: aday adı ya da "
          "'aday değil: <sebep>'; sebep yalnız genel kavram · başka adayın parçası (<aday>) · sponsor/reklam · konu dışı. 'zaten kurulu' sebep değil: kurulu araç da aday. "
          # 1b-2a: eksiksiz aday + yeni alanlar + link sınıfı
          "Adaylar: paketin HERHANGİ bir yerinde (altyazı · ekran metni · açıklama · yorumlar · linkli sayfalar) adı geçen VE videoda gösterilen/kullanılan/anlatılan her "
          "araç, model, servis, kütüphane, font, skill, MCP, CLI ve teknik; yalnız reklamı yapılan aday değil; adı ekranda yazıldığı gibi yaz. "
          "is_akisi: videoda yapılan işin adımları sırasıyla, her adımda kullanılan araçlarla. promptlar: videoda yazılan ya da okunan promptlar (amac=konu, metin=özet ya da metin). "
          "urller: ekranda görünen, söylenen, açıklamada ya da yorumda geçen HER URL (zaman, kaynak, aday). "
          "Bağlantı sinif: 'sponsor' yalnız açık ifadeyle (\"sponsorluğunda\", \"sponsored by\", \"#ad\", ücretli ortaklık); yönlendirme parametresi ya da indirim kodu varsa 'affiliate'; diğerleri 'diğer'. "
          "Bağlantının alan adı videoda kullanılan/anlatılan bir aracı adlandırıyorsa aday_mi true ve o araç adaylar'da olmalı. "
          # 1b-2a tur 2: genel kurallar
          "Dil: is_akisi.adim, promptlar.amac ve metin, site_ui.teknik ve ne Türkçe yazılır; promptlar.metin promptun Türkçe özetidir (ne istediği ve kısıtları), birebir alıntı değil. "
          "İş akışı ayrıntısı: her ayrı eylem kendi adımıdır; kontrol, düzeltme, yeniden deneme, test, dışa aktarma ve yayın da adımdır; 10 dakikalık videoda genelde 10-15 adım olur; her adım kullandığı araçları adlandırır. "
          "Adaylar ayrıca şunları kapsar: font aileleri, CSS, 3B ya da gölgelendirici (GPU) teknikleri, sunucunun içinde çalıştığı ana yapay zekâ aracı ya da modeli (apaçık olsa bile), "
          "araç olarak kullanılan her servis ya da site, her skill/eklenti; ad ekranda göründüğü gibi yazılır. "
          "site_ui: kurulan sayfada görünen her arayüz, animasyon ya da yerleşim tekniği ayrı satırdır; Türkçe ad ve ardından parantez içinde yaygın İngilizce terim yazılır. "
          "Bağlantı aday_mi: referans ya da ilham sayfası (portfolyo, pin, galeri, demo site) aday_mi false; yalnız izleyicinin kullanabileceği araç ya da servis bağlantısı true. "
          "Kare gönderildiyse karede_gorulen her zaman doldurulur. "
          # 1b-2a DEVAM-3: genel kurallar
          "Adaylar.ad kısa kanonik addır (en çok 4 kelime, ekranda göründüğü gibi yazılır); açıklama ayrı alanına yazılır. "
          "Yalnız bir menüde ya da listede görünen, videoda kullanılmayan öğeler Adaylar'a değil Belirsizlikler'e yazılır. "
          "Görsel efekt ve etkileşim tarifleri Site/UI'ye yazılır; Adaylar'a teknik yalnız özel adı varsa girer. "
          "Sohbet arayüzüne yazılan /slash komutlar Kurulum/komutlar'a yazılır.")
YOKLA = yon.omni_yokla  # O78: devam öncesi OmniRoute ön kontrolü (testte conftest None)
BASLAT = lambda: subprocess.Popen("omniroute serve --no-open --daemon", shell=True,  # MÜKEMMEL-2c: pencere açılmaz
                                  creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
BEKLE = time.sleep


def _omni_baslat(model, env, h, pdir):
    """MÜKEMMEL-2c (K6 gözetimsiz koşu): OmniRoute'u bir kez başlat, ≤ 90 s yokla; kalkmazsa son hata metni."""
    t0 = time.monotonic()
    try:
        BASLAT()
    except OSError:
        return h
    for _ in range(30):
        BEKLE(3)
        if not (h := YOKLA(model, env)):
            sure = round(time.monotonic() - t0)
            print(f"OmniRoute kendiliğinden başlatıldı ({sure} s)")
            # MÜKEMMEL-2d: gözetimsiz koşuda kalıcı iz; _defter çağrı saymaz
            tr.kayit_ekle(pdir / "defter.jsonl", [{"zaman": datetime.now().isoformat(timespec="seconds"), "adim": "omniroute_baslat",
                                                  "model": model, "usd": 0, "sure_s": sure}])
            return None
    return h


OPS = {"karede_gorulen", "erisilemez", "alt_tur", "kullanim_kosullari", "ucretsiz_katman", "veri_gizliligi", "bizde_karsilik", "kurulum_komutlar", "lisans_kaynak", "kotu_yanlar", "guclendirme", "iz", "urller", "is_akisi", "sinif"}  # M2c: opsiyonel alanlar · D1 (b): iz yoksa eski form (şema 1)


def _o(**alan):
    return {"type": "object", "required": [k for k in alan if k not in OPS], "additionalProperties": False, "properties": alan}


def _d(x):
    return {"type": "array", "items": x}


S = {"type": "string", "minLength": 1}
N = {"type": ["string", "null"]}
KAYNAK = {"type": "string", "enum": ["altyazı", "kare", "açıklama"]}
ZMN = {"type": "string", "minLength": 1, "description": "m:ss, video süresi içinde; yalnız açıklamadaysa 'açıklama'"}
KG = {"karede_gorulen": {"type": ["string", "null"], "description": "kare gönderildiyse zorunlu: karede tam olarak ne görülüyor"}}


def sema(ids, iz=False):
    """Tarayıcı formu (motor-sema.md §1); tür listeleri rapor-denetle'ninkiyle aynı. iz=True: modele giden şemada İz zorunlu (D1 b)."""
    video = _o(id={"type": "string", "enum": list(ids)}, ozet=S, bolumler=_d(_o(zaman=ZMN, baslik=S)),
               adaylar=_d(_o(ad=S, tur={"type": "string", "enum": sorted(tr.TUR)}, ne=S, kanit_zamani=ZMN, kaynak=KAYNAK, kanit=S, repo_url=N, **KG)),
               aciklama_baglantilari=_d(_o(url=S, ne=S, aday_mi={"type": "boolean"}, neden=S, aday_adi=N, erisilemez=N, sinif={"type": "string", "enum": ["sponsor", "affiliate", "diğer"]})),
               urller=_d(_o(url=S, zaman=ZMN, kaynak={"type": "string", "enum": ["ekran", "ses", "açıklama", "yorum"]}, aday={"type": "boolean"})),  # 1b-2a
               is_akisi=_d(_o(adim=S, araclar=_d(S))),  # 1b-2a: liste sırası = adım sırası
               site_ui=_d(_o(teknik=S, ne=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)),
               promptlar=_d(_o(metin=S, amac=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)),
               iddialar=_d(_o(iddia=S, kanit_zamani=ZMN, kaynak=KAYNAK, tur={"type": "string", "enum": sorted(tr.IDDIA_TUR)}, aday_adi=N, **KG)),
               kareden_okunanlar=_d(_o(kare=S, okunan=S)), belirsizlikler=_d(S),
                kurulum_komutlar=_d(_o(komut=S, ne_yapar=S, kanit_zamani=ZMN, kaynak=KAYNAK, **KG)),
               iz=_d(_o(kaynak=S, ne=S, baglandigi=S, kanit=S)))
    if iz:
        video["required"].append("iz")
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


def _anlamli(yol):
    """M8 K2: köşeli etiket ([Music]) ve ♪ dışında ≥3 kelime → anlamlı. ponytail: kelime sayısı sezgisi; konu yargısı gerekirse Jev."""
    if not yol.is_file():
        return False
    metin = " ".join(json.loads(s).get("metin", "") for s in yol.read_text(encoding="utf-8").splitlines() if s.strip())
    return len(re.findall(r"\w{2,}", re.sub(r"\[[^\]]*\]|♪", " ", metin))) >= 3


def _bozuk_oran(yol):
    """C1: segmentlerin anlamsız kelime oranı (m.anlamsiz_oran)."""
    return m.anlamsiz_oran(" ".join(json.loads(s).get("metin", "") for s in yol.read_text(encoding="utf-8").splitlines() if s.strip()))


def _bos_ram_gb():
    import ctypes

    class Bellek(ctypes.Structure):
        _fields_ = [("boy", ctypes.c_ulong), ("yuk", ctypes.c_ulong), *((x, ctypes.c_ulonglong) for x in ("top", "bos", "a", "b", "c", "d", "e"))]
    b = Bellek(boy=ctypes.sizeof(Bellek))
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(b))
    return b.bos / 2 ** 30


def _surecler():
    """Süreç adı + komut satırı (tam suit pytest'i ancak komut satırından görünür)."""
    return subprocess.run(["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_Process | % { $_.Name + ' ' + $_.CommandLine }"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout


def _whisper_engel():
    """C1 koruma: boş RAM < WHISPER_RAM_GB ya da ağır süreç (AGIR) → sebep; yoksa None."""
    if (gb := _bos_ram_gb()) < WHISPER_RAM_GB:
        return f"boş RAM {gb:.1f} GB < {WHISPER_RAM_GB}"
    return f"ağır süreç: {a.group(0)}" if (a := AGIR.search(_surecler())) else None


def _sure(sn):
    return f"{round(sn / 60)} dk" if sn >= 60 else f"{round(sn)} sn"


def _konusma(d, mt, alt):
    """C1: konuşma kaynağı → kapsam etiketi. Temiz altyazıya dokunulmaz; yoksa ya da bozuksa (> BOZUK_ESIK) whisper, süre sınırsız,
    korumalı (_whisper_engel). Bozuk altyazı segmentler.altyazi.jsonl'e alınır; whisper segment üretmezse geri konur."""
    sg = d / "segmentler.jsonl"
    if sg.is_file() and (o := _bozuk_oran(sg)) <= BOZUK_ESIK:
        return "altyazı"
    neden = f"altyazı bozuk %{round(o * 100)}" if sg.is_file() else "altyazı yok"
    if not find_spec("faster_whisper"):
        return f"{neden}; whisper kurulu değil"
    if engel := _whisper_engel():
        return f"{neden}; whisper atlandı ({engel})"
    yedek = sg.replace(d / "segmentler.altyazi.jsonl") if sg.is_file() else None
    t0, hata = time.monotonic(), ""
    try:
        alt(["whisper", "--en-fazla-dk", "0", "--", d.name])
    except (Exception, SystemExit) as e:  # M9 K6: whisper istisnası → kare-yalnız yol, hata değil; yarım parçalar whisper.json'da
        hata = f" · yarıda ({type(e).__name__}: {e})"[:120]
        print(f"paket {d.name}: whisper istisnası ({type(e).__name__}: {e}) → {'altyazı' if yedek else 'kare-yalnız'}")
    if yedek and not sg.is_file():
        yedek.replace(sg)
    return f"whisper ({neden}) · tahmini {_sure((mt.get('duration') or 0) * WHISPER_HIZ)} · gerçek {_sure(time.monotonic() - t0)}{hata}"


def paket_oku(yol):
    metin = Path(yol).read_text(encoding="utf-8")
    bas = metin.splitlines()[0][2:].split(" · ")
    sure = int(x[1]) if (x := re.search(r"· sure_sn (\d+)", metin)) else m.sn(re.search(r"· süre (\S+)", metin)[1])
    dil = re.search(r"· dil (\S+)", metin)
    satir = lambda b: [s.strip() for s in tr.bolum(metin, b).splitlines() if s.strip() and s.strip() != "yok" and not s.startswith("kare yok: ")]
    url = re.search(r" · (https?://\S+) · altyazı ", metin.splitlines()[0])  # VİDEO-PLATFORM-1: künye adresi (eski paket: yok → youtu.be)
    return {"kare_not": next((s for s in metin.splitlines() if s.startswith("kare yok: ")), None), "id": bas[0], "url": url[1] if url else None, "baslik": bas[1], "kanal": bas[2], "sure": sure, "dil": dil[1] if dil else "?", "metin": metin,
            "short": x[1] == "true" if (x := re.search(r"· short: (true|false)", metin)) else tr.short_mu(sure),
            "kare_yalniz": "altyazı yok: kare-yalnız" in metin, "linkler": satir("Açıklama bağlantıları"), "kareler": [s.split(" · ")[0] for s in satir("Kareler")],
            "kare_zaman": [_ks(s.split(" · ")[1]) if " · " in s else None for s in satir("Kareler")]}  # ölçüm betikleri (olcum_m4/m4b)


def _h(x):
    return re.sub(r"\s+", " ", str(x)).replace("|", "/").strip()


def _kg(x):
    if not (k := x.get("karede_gorulen")):
        return ""
    return f" (karede: kanıttan) {_h(k)}" if x.get("kaynak") == "kare" and k == x.get("kanit") else f" (karede: {_h(k)})"


def kanittan(form):
    """ONARIM 2 KARAR: kaynak=kare satırında karede_gorulen boş, kanit doluysa karede_gorulen = kanit (raporda '(karede: kanıttan) …'). Yerinde; disk yazımından önce."""
    for f in (form or {}).get("videolar") or []:
        for b in ("adaylar", "site_ui", "promptlar", "iddialar") if isinstance(f, dict) else ():
            for x in f.get(b) or []:
                if isinstance(x, dict) and x.get("kaynak") == "kare" and not (x.get("karede_gorulen") or "").strip() and (x.get("kanit") or "").strip():
                    x["karede_gorulen"] = x["kanit"]
    return form


def _nk(s):  # M4c: yalnız gösterim (test_m4 K1 testi); şema nasil/kutuphane istemez
    return f" — nasıl: {_h(s['nasil'])} · kütüphane: {_h(s['kutuphane'])}" if s.get("nasil") else ""


AFFILIATE = re.compile(r"[?&]via=|[?&]ref=|utm_medium=affiliate|partnerlinks|indirim kodu|discount code|promo code|coupon code", re.I)  # 1b-2a


def _sinif(b):
    """1b-2a: modelin açık 'sponsor' beyanı korunur (affiliate ezmez); aksi halde affiliate regex url+ne üzerinde, yoksa model değeri ya da 'diğer'."""
    return b["sinif"] if b.get("sinif") == "sponsor" else "affiliate" if AFFILIATE.search(f"{b['url']} {b['ne']}") else b.get("sinif") or "diğer"


def rapor_md(f, pk, notlar):
    """Mevcut rapor biçimi (docs/video-tarama/*.md) koddan; prompt'lar Adaylar'a `prompt` satırı olarak girer."""
    L = [f"# {pk['baslik']}", "## Künye", f"{pk['baslik']} · {pk['kanal']} · süre: {m.ss(pk['sure'])} · {pk['dil']} · {pk.get('url') or f'https://youtu.be/{pk["id"]}'}"
         + (f" · platform: instagram · tür: {'reel' if '/reel/' in (pk.get('url') or '') else 'görsel gönderi'} · yorum: girişsiz alınamıyor" if pk["id"].startswith("ig-") else "")  # SMOKE-DÜZELT B2
         + (" · şema 2" if f.get("iz") is not None else ""),
         *notlar, "## Özet", _h(f["ozet"]), "## Bölümler", *([f"- {_h(b['zaman'])} {_h(b['baslik'])}" for b in f["bolumler"]] or ["- yok"]),
         "## Adaylar", "| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |", "|---|---|---|---|---|---|---|",
         *[f"| {_h(a['ad'])} | yok | {a['tur']} | {_h(a['repo_url'] or 'yok')} | {_h(a['ne'])} | {_h(a['kanit_zamani'])} | {_h(a['kanit'])}{_kg(a)} |" for a in f["adaylar"]],
         *[f"| {_h(p['amac'])} | yok | prompt | yok | {_h(p['metin'])} | {_h(p['kanit_zamani'])} | kaynak: {p['kaynak']} |" for p in f["promptlar"]],
         "## Açıklama bağlantıları",
         *([f"- {b['url']} — {_h(b['ne'])} · aday: {'evet (' + _h(b['aday_adi'] or '?') + ')' if b['aday_mi'] else 'hayır'} · {_h(b['neden'])} · sınıf: {_sinif(b)}" + (f" · erişilemez: {_h(b['erisilemez'])}" if b.get('erisilemez') else "")
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
          *(["## İz", "| kaynak | ne | bağlandığı | kanıt |", "|---|---|---|---|",
             *[f"| {_h(z['kaynak'])} | {_h(z['ne'])} | {_h(z['baglandigi'])} | {_h(z['kanit'])} |" for z in f["iz"]]] if f.get("iz") is not None else []),
          "## Kareden okunanlar", *([f"- {_h(k['kare'])}: {_h(k['okunan'])}" for k in f["kareden_okunanlar"]] or ["- yok"]),
          "## Belirsizlikler", *([f"- {_h(b)}" for b in f["belirsizlikler"]] or ["- yok"]),
          "## Atlanan segment oranı", f"0/{seg} (paket tam okuma, motor)"]
    L += ["## URL'ler", *(["| url | zaman | kaynak | aday |", "|---|---|---|---|", *[f"| {_h(u['url'])} | {_h(u['zaman'])} | {u['kaynak']} | {'evet' if u['aday'] else 'hayır'} |" for u in f["urller"]]] if f.get("urller") else ["- yok"]),
          "## İş akışı", *([f"- {i}. adım — {_h(a['adim'])} — araçlar: {', '.join(map(_h, a['araclar'])) or 'yok'}" for i, a in enumerate(f["is_akisi"], 1)] if f.get("is_akisi") else ["- yok"]),
          "## Promptlar", *([f"- {_h(p['amac'])} — {_h(p['metin'])}" for p in f["promptlar"]] or ["- yok"])]  # 1b-2a: mevcut bölümlerin sonuna eklenir
    return "\n".join(L) + "\n"


def gruplar(pk):
    """short'lar ≤8 ve ≤40k jetonluk gruplar; uzun video tek başına."""
    out = []
    for v, p in sorted(pk.items(), key=lambda x: not x[1]["short"]):  # M2b K0: short'lar kuyruk sırasından bağımsız
        tk = girdi_tk(p["metin"], p["kareler"])
        if p["short"] and out and out[-1][0] and len(out[-1][1]) < SHORT_GRUP and out[-1][2] + tk <= GIRDI_TAVAN:
            out[-1][1].append(v)
            out[-1][2] += tk
        else:
            out.append([p["short"], [v], tk])
    return [g[1] for g in out]


def site_mu(metin):
    """M2e K2: kuyruk notu ya da başlıkta site/UI · landing · prompt anatomisi → kare tavanı 12."""
    return bool(re.search(r"site|\bUI\b|landing|prompt anatomisi", metin or "", re.I))


def kare_sayisi(sure, site, ipucu=False):
    """M2e K2: short ≤3 · uzun süre/2.5 dk (en az 4, en fazla 8) · site/UI en fazla 12 → (n, neden)."""
    if not sure:
        return 3, "süre bilinmiyor"
    if sure < tr.SHORT_SN:
        return (8, "short ipucu ≤8") if ipucu else (3, "short ≤3")  # DERİNLİK-1 R4
    return max(4, min(12 if site else 8, round(sure / 150))), f"{m.ss(sure)} / 2.5 dk · " + ("site/UI ≤12" if site else "4–8")


def model_kare(n, sure):
    """C4 (Ömer onayı O10/O11: tavan → bütçe): uzun videoda modele giden kare KARE_UST (60) güvenlik üst sınırı, asıl sınır cli.PAKET_BUTCE.
    Short/süresiz değişmez, açık büyük n korunur."""
    return n if sure < tr.SHORT_SN else max(n, KARE_UST)


def incelenmedi_isaretle(d, onb):
    """C4 devam --incelenmedi: kapsam.json'da incelenmedi anı kalan video → paket ikinci geçiş (ozet yok) + yeniden tarama (rapor -incelenmedi)."""
    for v, s in d["videolar"].items():
        if (kj := Path(onb) / v / "kapsam.json").is_file() and json.loads(kj.read_text(encoding="utf-8"))["incelenmedi"]:
            s["paket"].update(durum="bekliyor", deneme=0, hata=None, yeniden=True, incelenmedi=True)
            s["tarama"].update(durum="bekliyor", deneme=0, hata=None, ice_alindi=None, gecis=2)


def girdi_tk(metin, kareler):
    """C4 (O11): paket bütçesi (cli.PAKET_BUTCE) ve kare_sigdir (GIRDI_TAVAN) aynı hesap — tam metin + gerçek kare jetonu (cli._kare_tk);
    dosyası olmayan kare KARE_TK sayılır."""
    from .cli import _kare_tk  # cli parti'yi içe alır: döngüsel, yerel
    return c.token(metin) + sum(_kare_tk(Path(k))[1] if Path(k).is_file() else KARE_TK for k in kareler)


def kare_sigdir(pk, onb=None):
    """M2e K2: uzun videonun çağrı girdisi ≤40k jeton; aşarsa kare düşürülür, rapora not. C4 (O10): onb verilirse düşen anlar
    kapsam.json incelenmedi'ye "girdi tavanı" ile (ikinci geçiş görür), izleme sayısı güncellenir."""
    for v, p in pk.items():
        if not p["short"] and girdi_tk(p["metin"], p["kareler"]) > GIRDI_TAVAN:
            n = len(p["kareler"])
            while n and girdi_tk(p["metin"], p["kareler"][:n]) > GIRDI_TAVAN:
                n -= 1
            p["kare_not"] = f"kareler: girdi ≤{GIRDI_TAVAN} jeton için {len(p['kareler'])}→{n}"
            if onb and (kj := Path(onb) / v / "kapsam.json").is_file():
                k = json.loads(kj.read_text(encoding="utf-8"))
                k["incelenmedi"] = sorted([*k["incelenmedi"], *(x for t in p["kare_zaman"][n:] if (x := [t, "girdi tavanı"]) not in k["incelenmedi"])])
                k["izleme"] = re.sub(r"model \d+ · incelenmedi \d+", f"model {n} · incelenmedi {len(k['incelenmedi'])}", k["izleme"])
                kj.write_text(json.dumps(k, ensure_ascii=False), encoding="utf-8")
            p["kareler"] = p["kareler"][:n]


LISTE = ("bolumler", "adaylar", "aciklama_baglantilari", "site_ui", "promptlar", "iddialar", "kareden_okunanlar", "belirsizlikler", "urller", "is_akisi")
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


def kanit_suz(f, paket):
    """1b-2a DEVAM-4: adı paket metninde `gecer` kuralıyla bulunmayan aday Adaylar'da kalır, kanıt hücresine 'kanıt: kare' (kaynak kare) ya da 'kanıt: yok' notu eklenir. LLM yok."""
    from .altin import gecer, norm
    kel = [norm(w) for w in re.findall(r"\w+", paket.casefold())]
    pencere = {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))}
    duz, f = norm(paket), json.loads(json.dumps(f))
    for a in f.get("adaylar") or []:
        if isinstance(a, dict) and isinstance(a.get("ad"), str) and not gecer(a["ad"], duz, pencere):
            a["kanit"] = f"{a.get('kanit') or ''} · kanıt: {'kare' if a.get('kaynak') == 'kare' else 'yok'}".lstrip(" ·")
    return f


def birlestir(a, b):
    """1b-2a KAPANIŞ: a birincil; adaylar gecer ile iki yönde tekil, url/komut url_norm/norm birleşimi (a'nın sınıfı kalır), kalan alanlar a'dan, a'da yoksa b'den."""
    from .altin import gecer, norm, url_norm
    f = json.loads(json.dumps(a))
    def gec(x, y):
        kel = [norm(w) for w in re.findall(r"\w+", y.casefold())]
        return gecer(x, norm(y), {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))})
    var = lambda x, L: any(gec(x["ad"], y["ad"]) or gec(y["ad"], x["ad"]) for y in L)
    f["adaylar"] = f.get("adaylar", []) + [x for x in b.get("adaylar", []) if not var(x, f.get("adaylar", []))]
    for k, anah, nm in (("urller", "url", url_norm), ("kurulum_komutlar", "komut", norm), ("aciklama_baglantilari", "url", url_norm)):
        gor = {nm(x[anah]) for x in f.get(k) or []}
        f[k] = (f.get(k) or []) + [x for x in b.get(k) or [] if nm(x[anah]) not in gor]
    for k in ("is_akisi", "promptlar", "site_ui", "iz", "iddialar"):
        if not f.get(k) and b.get(k):
            f[k] = b[k]
    return f


def _rapor_yaz(d, v, f, p, tdir, ikinci=None, **ek):
    f = kanit_suz(f, p["metin"])
    r =tdir / f"{d['tarih']}-{v}{'-incelenmedi' if d['videolar'][v]['tarama'].get('gecis') == 2 else ''}.md"  # C4: ilk rapor ezilmez
    r.parent.mkdir(parents=True, exist_ok=True)
    md = rapor_md(f, p, _notlar(d, p) + ([k] if (k := d["videolar"][v]["tarama"].get("kunye")) else [])) + (ig.ek_md(ikinci) if ikinci else "")
    r.write_bytes(md.encode("utf-8"))
    adaylar, ele = tr.ayikla(md)
    tr.kayit_ekle(Path(d.get("kayit") or tdir / "kayit.jsonl"), [{"id": v, "tarih": d["tarih"], "rapor": r.name, "adaylar": adaylar, "ele": ele, "parti": d["parti"], "konu": tr.konu_etiketle(md + p["metin"])}])  # YT1 2: rapor md + paket metni
    d["videolar"][v]["tarama"].update(cikti=r.as_posix(), **ek)


def _kismi_kabul(pdir, d, v, p, tdir):
    """M2e K1: diskteki son form yeniden denetlenir, geçerli kısmıyla rapor → tamam_eksik; form yoksa False (form_red kalır)."""
    y = pdir / "form" / f"{v}.json"
    if not y.is_file():
        return False
    form = kanittan({"videolar": [json.loads(y.read_text(encoding="utf-8"))]})  # ONARIM 2: yedek kural; disk ve rapor tutarlı
    y.write_text(json.dumps(form["videolar"][0], ensure_ascii=False, indent=1), encoding="utf-8")
    f, eksik = kismi(form["videolar"][0], dogrula(form, {v: p}, [v]).get(v, []), v)
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
    for i in range(5):  # M10 K1: antivirüs/dizinleyici geçici kilidi (WinError 5) → 50…800 ms bekleyip yeniden dene
        try:
            return os.replace(tmp, yol)
        except PermissionError:
            if i == 4:
                raise SystemExit(f"durum yazılamadı (dosya kilitli): {yol} — eski durum sağlam, kilit kalkınca `devam` ile sürdür")
            time.sleep(0.05 * 2 ** i)


def _maliyet(y):
    """F1 eki: defter usd alanı — taşıyıcı usd None dönerse (fiyat bilinmiyor) 0 yazılmaz."""
    return {"usd": None, "maliyet": "bilinmiyor"} if "usd" in y and y["usd"] is None else {"usd": y.get("usd") or 0.0}


PAKET_ADIMLARI = ("yorum", "baglanti", "sahne", "ocr")  # MÜKEMMEL-5a: paket hattı adım damgası (cli.paket yazar); yeni adım → eski paketler eksik


def eksik_adim(d):
    """MÜKEMMEL-5a: <önbellek>/<id>/kapsam.json damgasında olmayan paket adımları (damgasız ya da kapsam.json yok → hepsi)."""
    k = Path(d) / "kapsam.json"
    s = set(json.loads(k.read_text(encoding="utf-8")).get("adimlar", ())) if k.is_file() else set()
    return [x for x in PAKET_ADIMLARI if x not in s]


def _defter(pdir):
    s = [x for x in tr.kayit_oku(pdir / "defter.jsonl") if not x.get("adim", "").startswith(("ikinci_goz", "tavan", "omniroute_baslat", "paket_yenilendi"))]  # M5: ikinci göz ayrı tavanda · M6 K3: tavan satırı çağrı değil
    # F1 eki: usd None (maliyet bilinmiyor) $ tavanına girmez; çağrı tavanı sınırlar
    return sum(x.get("cagri", 1) for x in s), sum(x["usd"] or 0 for x in s), sum(x["girdi"] + x["onb_okuma"] + x["onb_yazma"] + x["cikti"] for x in s)


def _tavan(pdir, d):
    n, usd, _ = _defter(pdir)
    return n >= d["tavan"]["cagri"] or usd >= d["tavan"]["usd"]


def _ig_defter(pdir):
    s = tr.kayit_oku(pdir / "defter.jsonl")
    a = lambda k: [x for x in s if x.get("adim") == f"ikinci_goz_{k}"]
    return {"luna": len(a("luna")), "or_usd": sum(x["usd"] for x in a("luna")), "jev": sum(x.get("durum", 0) for x in a("jev")),
            "yargic": len(a("yargic")), "yargic_usd": sum(x["usd"] for x in a("yargic"))}


def _jev(env):
    def yargila(durumlar, q):
        return c.Tasiyici(env=env, en_fazla=len(c.parcala(durumlar)) + 1, istek_tavan=len(durumlar) + 10).yargila(durumlar, q)
    return yargila


def _kilitli_ekle(yol, s):
    with YAZ:
        tr.kayit_ekle(yol, [s])


def _ikinci(pdir, d, v, f, p, temizle, env, ikinci):
    """M5: Sonnet formu geçtikten sonra ikinci göz; her hata notla biter, video düşmez."""
    if not ikinci or ikinci.get("kapali"):
        return f, ({"not": [f"ikinci göz KAPALI: {ikinci['kapali']}"]} if ikinci else None)
    g = _ig_defter(pdir)
    kalan = {k: IG_TAVAN[k] - g[k] for k in IG_TAVAN}
    kareler = [k for k in p["kareler"] if Path(k).is_file()] if hafif.GORSEL else []
    luna = lambda butce: ikinci["luna"](SISTEM, _istem([v], {v: p}, {}, temizle), sema([v], iz=True), kareler=kareler, model=ig.LUNA, butce=butce, env=env)
    try:
        return ig.uygula(v, f, p, luna, ikinci["jev"], ikinci["yargic"], env, kalan, lambda x: dogrula({"videolar": [x]}, {v: p}, [v]).get(v),
                         lambda s: _kilitli_ekle(pdir / "defter.jsonl", s))
    except Exception as e:  # beklenmeyen hata: Sonnet sonucu aynen
        return f, {"not": [f"ikinci göz: hata ({e})"[:200] + " — Sonnet sonucu"]}


def _usage_topla(ys):
    """Sayısal usage alanlarının toplamı; iç içe alanlar (claude -p "cache_creation": {...}) toplanmaz."""
    ks = dict.fromkeys(a for y in ys for a, s in (y.get("usage") or {}).items() if isinstance(s, (int, float)))
    return {a: sum((y.get("usage") or {}).get(a, 0) for y in ys) for a in ks}


def _tara_v10(kalan, pk, hatalar, temizle, d, pdir, tdir, env, cagir, model):
    """DERİNLİK-KAPANIŞ-1: yonlendirme tarama "yontem": "V10" → video başı yon.tara_v10 (örnek tdir/ornek-v10.json). tara_v10 hatasında video aynı
    adımda A taşıyıcısıyla (cagir, d["model"]) taranır → geri_donus; usd ve cagri toplam, video düşmez.
    DERİNLİK-KAPANIŞ-2: ön tahmin (yon.tahmin_v10) kalan $'ı aşarsa çağrı 0, video "tavan" listesinde (A V10'dan pahalı; A'ya gitmez)."""
    ys, fs, notlar, tv, gc = [], [], [], [], {}
    for v in kalan:
        kr = [k for k in pk[v]["kareler"] if Path(k).is_file()] if hafif.GORSEL else []
        g = (SISTEM, _istem([v], pk, hatalar, temizle), sema([v], iz=True), kr)
        kalan_usd = d["tavan"]["usd"] - _defter(pdir)[1] - sum(y.get("usd") or 0 for y in ys)
        t = yon.tahmin_v10(g, model, Path(tdir) / "ornek-v10.json") if model in yon.FIYAT else 0.0
        if t > kalan_usd:
            tv.append(v)
            ys.append({"form": None, "usd": 0.0, "cagri": 0, "hata": f"tavan: ön tahmin ${t:.4f} > kalan ${kalan_usd:.4f}"})
            continue
        y = yon.tara_v10(g, env, model, ornek=Path(tdir) / "ornek-v10.json")
        ys.append(y)
        if y.get("hata") and gecici(y["hata"]):  # MÜKEMMEL-8a: yeniden denemelerden sonra da geçici → A yok, video "yeniden"
            gc[v] = y["hata"][:200]
        elif y.get("hata"):
            notlar.append(f"{v}: {y['hata']}")
            y = cagir(*g[:3], kareler=kr, model=d["model"], butce=min(d["butce"], kalan_usd - (y.get("usd") or 0)), env=env)
            ys.append(y)
        fs += [f for f in (y.get("form") or {}).get("videolar") or [] if isinstance(f, dict)]
    us = [y.get("usd") for y in ys]
    return {"form": {"videolar": fs} if fs else None, "usage": _usage_topla(ys),
            "usd": None if None in us else sum(us), "sure": round(sum(y.get("sure") or 0 for y in ys), 1), "cagri": sum(y.get("cagri", 1) for y in ys),
            "hata": None if fs else next((y["hata"] for y in reversed(ys) if y.get("hata")), "form yok"),
            "model": d["model"] if notlar else model, **({"geri_donus": " · ".join(notlar)[:120]} if notlar else {}), **({"tavan": tv} if tv else {}), **({"gecici": gc} if gc else {})}


def _tara_ikili(kalan, pk, hatalar, temizle, d, pdir, env, cagir, modeller):
    """1b-2a KAPANIŞ: kurgu 2 — video başı her model için bir claude -p (≤2 çağrı, yeniden istek yok); iki form → birlestir (modeller[0] birincil),
    tek kol hata → öbür kol tek başına + künye "tek kol: <model> <hata>", iki kol hata → o video formsuz (form_red yolu). Künye d["videolar"][v]["tarama"]["kunye"].
    YT1 3: iki kol eşzamanlı (2'li havuz, CAGIR kapısı); sonuçlar model listesi sırasıyla toplanır → birlestir(a, b) değişmez. Kol bütçesi video başına bir kez
    hesaplanır (ilk kolun harcaması ikinciden düşülmez). İki kol da geçici hata (429/5xx/zaman aşımı) verdiyse video "gecici" → parti sonunda bir tur."""
    ys, fs, gc = [], [], {}
    for v in kalan:
        kr = [k for k in pk[v]["kareler"] if Path(k).is_file()] if hafif.GORSEL else []
        istem = _istem([v], pk, hatalar, temizle)
        with YAZ:
            butce = min(d["butce"], d["tavan"]["usd"] - _defter(pdir)[1] - sum(x.get("usd") or 0 for x in ys))

        def kol(mdl, v=v, kr=kr, istem=istem, butce=butce):
            with CAGIR, asama(v, "model"):
                return cagir(SISTEM, istem, sema([v], iz=True), kareler=kr, model=mdl, butce=butce, env=env)
        with ThreadPoolExecutor(len(modeller)) as ex:
            yy = [f.result() for f in [ex.submit(kol, mdl) for mdl in modeller]]
        kolf, kun = [], []
        for mdl, y in zip(modeller, yy):
            ys.append(y)
            f = next((x for x in (y.get("form") or {}).get("videolar") or [] if isinstance(x, dict)), None)
            if y.get("hata") or f is None:
                kun.append(f"tek kol: {mdl} {y.get('hata') or 'form yok'}"[:200])
            else:
                kolf.append(f)
                (pdir / "form").mkdir(exist_ok=True)  # ONARIM 2: kol başı ham form (birleşik form/<id>.json ayrı yazılır)
                (pdir / "form" / f"{v}.{mdl.split('-')[1]}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")
                kun.append(f"{mdl}: {y.get('model') or mdl} · {sum((y.get('usage') or {}).get(a, 0) for a in ('input_tokens', 'cache_read_input_tokens', 'cache_creation_input_tokens', 'output_tokens'))} tk")
        if kolf:
            fs.append(birlestir(*kolf) if len(kolf) == 2 else kolf[0])
        elif any(gecici(y.get("hata")) for y in yy):
            gc[v] = next(y["hata"] for y in yy if gecici(y.get("hata")))[:200]
        with YAZ:
            d["videolar"][v]["tarama"]["kunye"] = " · ".join(kun)
    us = [y.get("usd") for y in ys]
    return {"form": {"videolar": fs} if fs else None, "usage": _usage_topla(ys),
            "usd": None if None in us else sum(us), "sure": round(sum(y.get("sure") or 0 for y in ys), 1), "cagri": len(ys),
            "hata": None if fs else next((y["hata"] for y in reversed(ys) if y.get("hata")), "form yok"), "model": "+".join(modeller), **({"gecici": gc} if gc else {})}


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
            *([pk["kare_not"]] if pk.get("kare_not") else []), *(["altyazı yok: kare-yalnız"] if pk.get("kare_yalniz") else [])]


def _kos(pdir, d, onb, tdir, alt, temizle, cagir, env, ikinci=None, kuyruk=None, tur=0, paralel=1, yalniz_paket=False):
    """YT1 3: ikili yolda her video tek iş (paketle → tara → rapor), `paralel` iş eşzamanlı, aşama bariyeri yok. Diğer yollar (V10/A) eskisi gibi art arda:
    önce tüm paketler, sonra gruplar. d / durum / defter / kayit yazımları ve d değişiklikleri tek global YAZ kilidi altında. yalniz_paket: tarama yok."""
    yol = pdir / "durum.json"
    ikili = ((d.get("yonlendirme") or {}).get("tarama") or {}).get("yontem") == "ikili"  # 1b-2a KAPANIŞ
    dur = threading.Event()  # YT1 3: RAM yetersiz → başlamamış işler atlanır, parti durur
    asil = sys.stdout
    if not isinstance(asil, _Yon):  # redirect_stdout süreç geneli: paralelde iş parçacıkları birbirinin çıktısını yakalar → iş parçacığı başına vekil
        sys.stdout = _Yon(asil)

    def paketle(v, s):  # aşama 2: mevcut ozet/whisper/paket komutları (Jev 0: --istek-tavan 0)
        a = s["paket"]
        with YAZ:
            if a["durum"] in ("tamam", "erisilemez") or a["deneme"] >= 3:
                return
            a["deneme"] += 1
        try:
            with YAZ:
                yeniden = a.pop("yeniden", False)  # DERİNLİK-1 R4b: --paket-yeniden → ozet atlanır, paket R4 ile yeniden kurulur
                ince = a.pop("incelenmedi", False)  # C4 ikinci geçiş
            if not yeniden and (onb / v / "paket.md").is_file() and (eksik := eksik_adim(onb / v)):  # MÜKEMMEL-5a: bayat paket → model 0 yeniden kurulum
                with YAZ:
                    tr.kayit_ekle(pdir / "defter.jsonl", [{"zaman": datetime.now().isoformat(timespec="seconds"), "adim": "paket_yenilendi", "video": v,
                                                           "not": f"paket yenilendi (eksik: {', '.join(eksik)})"}])
                yeniden = True
            if yeniden or not (onb / v / "paket.md").is_file():
                if not yeniden:
                    with _yakala() as b:
                        alt(["ozet", "--", v])
                    print(b.getvalue(), end="")
                    if sb := erisilemez(b.getvalue()):  # ONARIM-3: kalıcı erişim hatası → yeniden denenmez, rapor yok
                        with YAZ:
                            a.update(durum="erisilemez", hata=f"erişilemez: {sb}")
                            tr.kayit_ekle(Path(d.get("kayit") or tdir / "kayit.jsonl"), [{"id": v, "tarih": d["tarih"], "parti": d["parti"],
                                                                                          "etiket": "erisilemez", "not": f"erişilemez: {sb}"}])
                            _yaz(yol, d)
                        return
                mt = json.loads((onb / v / "meta.json").read_text(encoding="utf-8")) if (onb / v / "meta.json").is_file() else {}
                kons = "instagram: altyazı yok; reel → Groq (paket)" if v.startswith("ig-") else _konusma(onb / v, mt, alt)  # C1 · VİDEO-PLATFORM-1: IG'de whisper/yt-dlp yok (M8 K2 (i) ≤5 dk sınırı kalktı)
                with YAZ:
                    s["konusma"] = kons
                yalniz = not _anlamli(onb / v / "segmentler.jsonl")  # M8 K2 (ii): altyazı yok / whisper boş ya da yalnız müzik → kare-yalnız
                n, neden = kare_sayisi(mt.get("duration") or 0, site_mu(f"{s.get('not', '')} {mt.get('title') or ''}"),
                                       (sg := onb / v / "segmentler.jsonl").is_file() and bool(tr.IPUCU.search(sg.read_text(encoding="utf-8"))))  # M2e K2 · DERİNLİK-1 R4
                mk = model_kare(n, mt.get("duration") or 0)  # C4 · O11 (5): n aday tabanı, mk model tavanı
                with _yakala() as b:  # M9 K3: alt komutun "hata:" iletisi sebep olur
                    rc = alt(["paket", "--kare", str(n), "--model-tavan", str(mk), "--istek-tavan", "0", *(["--kare-yalniz"] if yalniz else []), *(["--incelenmedi"] if ince else []),
                              *(["--kuyruk", kuyruk] if kuyruk else []), "--", v])  # B ek: bağlantılı video kuyruğa
                print(b.getvalue(), end="")
                kn = int(km[1]) if (km := re.search(r"· kare (\d+)", b.getvalue())) else n  # O78: paketin gönderdiği gerçek kare
                print(f"paket {v}: kare {kn} (aday tabanı {n}: {neden} · model tavanı {mk}, sınır {'model tavanı' if kn >= mk else 'jeton bütçesi'})")
                if not (onb / v / "paket.md").is_file():
                    from .cli import Hata  # cli parti'yi içe alır: döngüsel, yerel
                    raise Hata(next((s[6:] for s in reversed(b.getvalue().splitlines()) if s.startswith("hata: ")), f"paket çıkış {rc}, paket.md yok"))
            with YAZ:
                a.update(durum="tamam", cikti=(onb / v / "paket.md").as_posix())
                if (yj := onb / v / "yorumlar.json").is_file():  # DERİNLİK-1 R4: Kapsam yorum alanı
                    s["yorum"] = json.loads(yj.read_text(encoding="utf-8"))["durum"]
                if (kj := onb / v / "kapsam.json").is_file():  # C4: Kapsam izleme alanı
                    s["izleme"] = json.loads(kj.read_text(encoding="utf-8"))["izleme"]
        except (Exception, SystemExit) as e:  # tek videonun indirme hatası partiyi durdurmaz; devam yeniden dener
            with YAZ:
                a.update(durum="hata", hata=f"{type(e).__name__}: {f'çıkış {e.code}' if isinstance(e, SystemExit) else e}"[:200])
            if "RAM yetersiz" in str(e):
                dur.set()
        with YAZ:
            _yaz(yol, d)

    def bekleyen(vs):
        with YAZ:
            bek = [v for v in vs if (s := d["videolar"][v])["paket"]["durum"] == "tamam"
                   and (s["tarama"]["durum"] == "yeniden" if tur else s["tarama"]["durum"] in YENIDEN) and s["tarama"]["deneme"] < 3]
        pk = {v: paket_oku(onb / v / "paket.md") for v in bek}
        kare_sigdir(pk, onb)
        with YAZ:
            for v in pk:  # C4 (O10): girdi tavanı izleme'yi değiştirmiş olabilir
                if (kj := onb / v / "kapsam.json").is_file():
                    d["videolar"][v]["izleme"] = json.loads(kj.read_text(encoding="utf-8"))["izleme"]
        return bek, pk

    def tara(g, pk, bek):  # aşama 3-4: tek grup; 3 → tavan, motor durur
        with YAZ:
            for v in g:
                d["videolar"][v]["tarama"]["deneme"] += 1
            _yaz(yol, d)
        kalan, hatalar, onceki = list(g), {}, 0.0
        for _ in range(1 if ikili else 3):  # ilk istek + en fazla 2 yeniden istek · ikili: yeniden istek yok (video ≤2 çağrı)
            with YAZ:
                if _tavan(pdir, d):  # ponytail: paralelde denetim çağrıdan önce; en çok `paralel` iş tavanı birer çağrı aşabilir
                    for v in bek:
                        if d["videolar"][v]["tarama"]["durum"] in YENIDEN and v in kalan and v in hatalar:  # M2e: formu geçmemiş video tavanda da form_red (sonra --kismi-kabul)
                            d["videolar"][v]["tarama"].update(durum="form_red", hata=hatalar[v][:5])
                        elif d["videolar"][v]["tarama"]["durum"] in YENIDEN:
                            d["videolar"][v]["tarama"]["durum"] = "tavan"
                    d["durum"] = "tavan"
                    _yaz(yol, d)
                    print(f"parti: tavan aşıldı ({d['tavan']['cagri']} çağrı / ${d['tavan']['usd']}), motor durdu")
                    return 3
                if hatalar and d["tavan"]["usd"] - _defter(pdir)[1] < onceki:  # M5b K2: kalan $ son istekten (tahmin) az → yeniden istek yok, form_red
                    for v in kalan:
                        d["videolar"][v]["tarama"].update(durum="form_red", hata=[BUTCE_YOK, *hatalar[v][:4]])
                    kalan = []
                    break
                kareler = [k for v in kalan for k in pk[v]["kareler"] if Path(k).is_file()] if hafif.GORSEL else []
                c, model = (None, None) if ikili else yon.sec(d, "tarama", cagir, env)  # F1: adım başı yönlendirme; tanımsızsa bugünkü · ikili: sağlayıcı yok
                v10 = ((d.get("yonlendirme") or {}).get("tarama") or {}).get("yontem") == "V10"  # DERİNLİK-KAPANIŞ-1
            try:  # model çağrısı kilitsiz: asıl bekleme burada
                y = _tara_ikili(kalan, pk, hatalar, temizle, d, pdir, env, cagir, d["yonlendirme"]["tarama"]["modeller"]) if ikili else \
                    _tara_v10(kalan, pk, hatalar, temizle, d, pdir, tdir, env, cagir, model) if v10 else c(SISTEM, _istem(kalan, pk, hatalar, temizle), sema(kalan, iz=True), kareler=kareler, model=model,
                          butce=min(d["butce"], d["tavan"]["usd"] - _defter(pdir)[1]), env=env)
            except Exception as e:  # M2b K0: çağrı ortası kesinti → durum hata; devam yalnız bu grubu yeniden çağırır
                y = {"hata": f"taşıyıcı: {e}"[:200]}
            tv = y.get("tavan") or []  # DERİNLİK-KAPANIŞ-2: ön tahmini kalan $'ı aşan video tavanda kalır (YENIDEN)
            ig_ = {}
            kanittan(y.get("form"))
            with YAZ:
                hatalar = {} if y.get("hata") else dogrula(y.get("form"), pk, [v for v in kalan if v not in tv])
            for f in (y.get("form") or {}).get("videolar") or []:  # M2e K1: son form diskte (kısmi kabul çağrısız)
                if isinstance(f, dict) and f.get("id") in kalan:
                    (pdir / "form").mkdir(exist_ok=True)
                    (pdir / "form" / f"{f['id']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1), encoding="utf-8")
            u = y.get("usage") or {}
            with YAZ:
                tr.kayit_ekle(pdir / "defter.jsonl", [{
                    "zaman": datetime.now().isoformat(timespec="seconds"), "adim": "tarama", "videolar": kalan, "model": y.get("model") or model,
                    "girdi": u.get("input_tokens", 0), "onb_okuma": u.get("cache_read_input_tokens", 0), "onb_yazma": u.get("cache_creation_input_tokens", 0),
                    "cikti": u.get("output_tokens", 0), "sure": y.get("sure"), **_maliyet(y), "kare": len(kareler), **{x: y[x] for x in ("cagri", "geri_donus", "gecici") if y.get(x) is not None},
                    "form": f"hata: {y['hata']}" if y.get("hata") else f"red {len(hatalar)}/{len(kalan)}" if hatalar else "gecti"}])
                onceki = y.get("usd") or 0.0
                for v in tv:
                    d["videolar"][v]["tarama"]["durum"] = "tavan"
                for v, h in (y.get("gecici") or {}).items():  # MÜKEMMEL-8a
                    d["videolar"][v]["tarama"].update(durum="yeniden", hata=h)
                kalan = [v for v in kalan if v not in tv and v not in (y.get("gecici") or {})]
                if y.get("hata"):
                    for v in kalan:  # M5b K2: bütçe hatası "hata" değil form_red (yeniden başlatılabilir)
                        d["videolar"][v]["tarama"].update(**({"durum": "form_red", "hata": [BUTCE_YOK, y["hata"][:200]]} if "max_budget" in y["hata"]
                                                             else {"durum": "hata", "hata": y["hata"][:200]}))
                    kalan = []
                    break
                gecen = [v for v in kalan if v not in hatalar]
            for v in gecen:  # ikinci göz ağ çağrısı yapabilir: kilitsiz
                ig_[v] = _ikinci(pdir, d, v, next(f for f in y["form"]["videolar"] if f.get("id") == v), pk[v], temizle, env, ikinci)
            with YAZ:
                for v, (f, e) in ig_.items():
                    _rapor_yaz(d, v, f, pk[v], tdir, ikinci=e, durum="tamam", usage=u, grup=len(kalan), hata=None, **({"ikinci_goz": ig.ozet(e)} if e else {}))
                kalan = [v for v in kalan if v in hatalar]
                _yaz(yol, d)
            if not kalan:
                break
        with YAZ:
            for v in kalan:  # M2e K1: 2 yeniden istekten sonra kısmi kabul; son form yoksa form_red
                if not _kismi_kabul(pdir, d, v, pk[v], tdir):
                    d["videolar"][v]["tarama"].update(durum="form_red", hata=hatalar[v][:5])
            _yaz(yol, d)
        return 0

    def is_(v):  # YT1 3: ikili iş = bir videonun paketle → tara hattı
        if dur.is_set():
            return 0
        paketle(v, d["videolar"][v])
        if yalniz_paket or dur.is_set():
            return 0
        bek, pk = bekleyen([v])
        return next((rc for g in gruplar(pk) if (rc := tara(g, pk, bek)) == 3), 0)

    try:
        if ikili:
            ex = ThreadPoolExecutor(max(1, paralel))
            try:
                if 3 in [f.result() for f in [ex.submit(is_, v) for v in list(d["videolar"])]]:
                    return 3
            finally:
                ex.shutdown(cancel_futures=True)  # kesinti / tavan: bekleyen işler başlamaz
        else:
            for v, s in d["videolar"].items():
                paketle(v, s)
            if not yalniz_paket:
                bek, pk = bekleyen(list(d["videolar"]))
                for g in gruplar(pk):  # aşama 3-4
                    if tara(g, pk, bek) == 3:
                        return 3
    finally:
        if isinstance(sys.stdout, _Yon) and sys.stdout is not asil:
            sys.stdout = asil
    if dur.is_set():
        d["durum"] = "yarim"
        _yaz(yol, d)
        print("parti: DUR — RAM yetersiz (10 ardışık düşük ölçüm); başlamamış videolar bekliyor, boşalınca `devam`")
        return 6
    if not tur and any(s["tarama"]["durum"] == "yeniden" for s in d["videolar"].values()):  # MÜKEMMEL-8a: parti sonu, ≥60 s sonra bir tur daha
        BEKLE(SON_TUR_SN)
        return _kos(pdir, d, onb, tdir, alt, temizle, cagir, env, ikinci, kuyruk, tur=1, paralel=paralel, yalniz_paket=yalniz_paket)
    if tur and ikili:  # YT1 3: ikinci turdan sonra hâlâ geçici hata → o video hata, diğerleri tamam
        for s in d["videolar"].values():
            if s["tarama"]["durum"] == "yeniden":
                s["tarama"]["durum"] = "hata"
    d["durum"] = "tamam" if all(s["tarama"]["durum"] in ("tamam", "tamam_eksik", "form_red") or s["paket"]["durum"] == "erisilemez" for s in d["videolar"].values()) else "yarim"
    _yaz(yol, d)
    return 0


def _ozet(pdir, d):
    rc = _ozet_govde(pdir, d)
    h = [f"{v} ({a}: {s[a].get('hata') or '?'})" for v, s in d["videolar"].items() for a in ("paket", "tarama") if s[a]["durum"] in ("hata", "yeniden")]
    if h:  # M8 K3: hatalı videolar özetin sonunda · MÜKEMMEL-8a: "yeniden" de
        print("hatalı videolar: " + " · ".join(h))
    if (df := pdir / "defter.jsonl").is_file() and (gd := [x["geri_donus"] for x in map(json.loads, df.read_text(encoding="utf-8").splitlines()) if x.get("geri_donus")]):
        print("geri dönüş: " + " · ".join(gd))  # MÜKEMMEL-8a: kalıcı hata → A
    return rc


def _ozet_govde(pdir, d):
    n, usd, tk = _defter(pdir)
    say = lambda a: " · ".join(f"{k} {x}" for k, x in sorted(Counter(s[a]["durum"] for s in d["videolar"].values()).items()))
    taranan = sum(s["tarama"]["durum"] in ("tamam", "tamam_eksik") and not s["tarama"].get("ice_alindi") for s in d["videolar"].values())
    print(f"parti {d['parti']} · durum {d['durum']} · paket: {say('paket')} · tarama: {say('tarama')}")
    print(f"defter: {n} çağrı / tavan {d['tavan']['cagri']} · ${usd:.4f} / ${d['tavan']['usd']} · {tk} jeton"
          + (f" · taranan video başına {tk // taranan} jeton" if taranan else ""))
    g = _ig_defter(pdir)
    if d.get("ikinci_goz_kapali"):
        print(f"ikinci göz KAPALI: {d['ikinci_goz_kapali']}")
    elif g["luna"] or g["jev"] or g["yargic"]:
        s = [x["tarama"].get("ikinci_goz") or {} for x in d["videolar"].values()]
        print(f"ikinci göz: eklenen {sum(x.get('eklenen', 0) for x in s)} · doğrulanamadı {sum(x.get('dogrulanamadi', 0) for x in s)} · "
              f"OpenRouter ${g['or_usd']:.4f} / ${IG_TAVAN['or_usd']} ({g['luna']} çağrı) · Jev {g['jev']} / {IG_TAVAN['jev']} durum · "
              f"yargıç {g['yargic']} / {IG_TAVAN['yargic']} çağrı ${g['yargic_usd']:.4f}")
    for v, s in d["videolar"].items():
        t = s["tarama"]
        print(f"- {v} · paket {s['paket']['durum']} · tarama {t['durum']}" + (" (içe alındı)" if t.get("ice_alindi") else "")
              + (f" · {t['cikti']}" if t.get("cikti") else "") + (f" · {str(t['hata'])[:120]}" if t.get("hata") else ""))
    return 0


def _acik(kok):
    """M12 K2: kapanmamış (kapandi/iptal değil) partilerdeki video → parti."""
    acik = {}
    for j in sorted((Path(kok) / ".kos").glob("*/durum.json")):
        d = json.loads(j.read_text(encoding="utf-8"))
        if "parti" in d and d.get("durum") not in ("kapandi", "iptal"):
            acik.update({v: d["parti"] for v in d.get("videolar", {})})
    return acik


def _ikili_mi(ns):
    return not getattr(ns, "a_yolu", False) and ((YONLENDIRME or {}).get("tarama") or {}).get("yontem") == "ikili"


def parti(ns, ctx):
    from . import cli, uygula as uy  # döngüsel içe aktarma yok: yalnız varsayılanlar için
    kok = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or uy.KOK)
    tdir = ctx.get("tarama_dizin") or cli._tarama_dizin(ctx)
    alt = ctx.get("alt") or (lambda a: cli.main(a, env=ctx["env"], kos=ctx["kos"], gonder=ctx["gonder"], uyku=ctx["uyku"], ocr=ctx.get("rapid")))  # YT1 3e: parti alt-komutları RapidOCR yükleyicisini de alır (yoksa göz yolu hiç koşmuyordu)
    temizle = ctx.get("temizle") or (lambda s: cli._temizle(s, ctx["env"]))
    if ns.eylem == "link":  # MÜKEMMEL-7c U1: tek link → geçici tek satırlık kuyruk → baslat (V10) → toplu; gerçek kuyruk.md'ye dokunulmaz
        v, onb = m.vid(ns.hedef), Path(ctx["kok"])  # VİDEO-PLATFORM-1 karar 6: tek kimlik yardımcısı (YouTube 11 tam · IG ig-<kod>)
        if not v:
            from .cli import Hata  # cli parti'yi içe alır: döngüsel, yerel
            raise Hata(f"link: kimlik çözülemedi: {ns.hedef}")
        if not (onb / v / "meta.json").is_file():
            alt(["ozet", "--", v])
        mt = json.loads((onb / v / "meta.json").read_text(encoding="utf-8"))
        (ky := kok / ".kos" / f"link-{v}.md").parent.mkdir(parents=True, exist_ok=True)
        ky.write_text("| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n| " + " | ".join(
            [v, str(round((mt.get("duration") or 0) / 60, 1)), str(mt.get("title") or "?")[:40].replace("|", "/"), "/video-uygula", "bekliyor"]) + " |\n", encoding="utf-8")
        ns.eylem, ns.hedef, ns.tekrar = "baslat", ky.as_posix(), True  # KUYRUK-HEDEF: açık istekte raporlu video yeniden alınır
        if rc := parti(ns, ctx):
            return rc
        d = next(x for j in sorted((kok / ".kos").glob("*/durum.json"), key=lambda j: j.stat().st_mtime, reverse=True)
                 if (x := json.loads(j.read_text(encoding="utf-8"))).get("kuyruk") == ky.as_posix())
        if not (rap := [s["tarama"]["cikti"] for s in d["videolar"].values() if s["tarama"].get("cikti")]):
            print(f"link: rapor yok — video parti devam {d['parti']}")
            return 5
        rc = alt(["toplu", *rap])
        d["durum"] = "kapandi"  # 7d: link partisi panel beklemez; açık kalırsa aynı videonun ikinci link'i _acik ile atlanır
        _yaz(kok / ".kos" / d["parti"] / "durum.json", d)
        return rc
    if ns.eylem in ("baslat", "kuyruk") and not ns.hedef:  # M2d K4: tek komut; varsayılan kuyruk · KÜÇÜK-1 K3: baslat da
        ns.hedef = (kok / "docs" / "video-tarama" / "kuyruk.md").as_posix()
    if ns.eylem in ("baslat", "kuyruk"):
        metin, acik = Path(ns.hedef).read_bytes().decode("utf-8"), _acik(kok)  # M12 K2: kapanmamış partideki video ikinci partiye alınmaz
        metin, raporlu = (metin, []) if getattr(ns, "tekrar", False) else tr.kuyruk_raporlu(metin, Path(getattr(ns, "kayit", None) or Path(tdir) / "kayit.jsonl"), tdir, acik)
        if raporlu:  # KUYRUK-HEDEF: raporlu video partiye alınmaz, kuyrukta `raporlu` olur; link (tekrar) ve açık parti hariç
            Path(ns.hedef).write_bytes(metin.encode("utf-8"))
            print(f"kuyruk: {len(raporlu)} satır raporlu (atlandı)")
        tur, satirlar = tr.kuyruk_parti(metin, kapsiz=_ikili_mi(ns))  # YT1 3: ikili yolda 3/8 sınırı yok, --en-fazla geçerli
        if not satirlar:
            print("parti: kuyrukta bekleyen video yok")
            return 1
        if (ns.short and tur != "short") or (ns.uzun and tur != "uzun"):
            print(f"parti: kuyruğun sıradaki partisi {tur}")
            return 2
        secilen = [h for h in satirlar if h[0] not in acik][:ns.en_fazla]
        if atla := sorted({acik[h[0]] for h in satirlar if h[0] in acik}):
            print(f"açık parti: {' · '.join(atla)} — önce: video parti kapat {atla[0]}" + (" (videoları atlandı)" if secilen else ""))
        if not secilen:
            return 3
        tarih = ns.tarih or date.today().isoformat()
        pid, i = f"{tarih}-{tur}", 1
        while (kok / ".kos" / pid).exists():
            i += 1
            pid = f"{tarih}-{tur}-{i}"
        (pdir := kok / ".kos" / pid).mkdir(parents=True)
        d = {"parti": pid, "tur": tur, "tarih": tarih, "model": ns.model, "butce": ns.butce, "kuyruk": Path(ns.hedef).as_posix(),
             "tavan": {"cagri": ns.cagri_tavan, "usd": ns.usd_tavan, "cagri_max": getattr(ns, "cagri_tavan_max", 30), "usd_max": getattr(ns, "usd_tavan_max", 2.0)}, "durum": "calisiyor", "videolar": {},
             **({"kayit": ns.kayit} if getattr(ns, "kayit", None) else {}),  # MÜKEMMEL-7c U10: varsayılan tarama dizini kayit.jsonl
             **({"yonlendirme": YONLENDIRME} if YONLENDIRME else {})}  # O78: anahtar yoksa da V10; eksik anahtar devam'da DUR
        for h in secilen:
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
        if ns.eylem == "iptal":  # M12 K3: durum + neden; dosya silinmez, panel uygulanmaz
            if not getattr(ns, "neden", None):
                print("parti iptal: --neden zorunlu")
                return 2
            d.update(durum="iptal", neden=ns.neden)
            _yaz(pdir / "durum.json", d)
            print(f"parti {d['parti']}: iptal · neden: {ns.neden} · dosyalar yerinde")
            return 0
        if d.get("durum") == "iptal" and ns.eylem != "durum":
            print(f"parti {d['parti']} iptal ({d.get('neden')}) — işlem yok")
            return 1
        if ns.eylem == "durum":
            return _ozet(pdir, d)
        if ns.eylem == "denetim-isle":  # E2
            from . import akil
            return akil.denetim_isle(d, kok)
        if getattr(ns, "cagri_ek", 0) or getattr(ns, "usd_ek", 0):  # M2b: tavan yalnız açıkça yükseltilir
            d["tavan"].update(cagri=d["tavan"]["cagri"] + ns.cagri_ek, usd=round(d["tavan"]["usd"] + ns.usd_ek, 4))  # ONARIM: cagri_max/usd_max/genis korunur
        if ns.eylem == "akil" and getattr(ns, "yeniden", False):  # DERİNLİK-1 R6: araştırma dahil yeniden (R1–R5); kurulu envanterden, Ömer hücreleri panelde korunur
            for a in d.get("adaylar", {}).values():
                for x in ("durum", "deneme", "hata", "repo_arama", "guncellik"):
                    a.pop(x, None)
            d.pop("gelistirme", None)
        if ns.eylem in ("akil", "kapat"):
            from . import akil
            return akil.akil(pdir, d, kok, Path(tdir), ctx, getattr(ns, "tum", False)) if ns.eylem == "akil" else akil.kapat(pdir, d, kok, ctx)
        if getattr(ns, "yeniden_tara", False):  # M2d: _temizle URL hatası sonrası — bitmiş videolar düzeltilmiş girdiyle yeniden taranır
            for s in d["videolar"].values():
                if s["tarama"]["durum"] in ("tamam", "tamam_eksik", "form_red", "tavan"):
                    s["tarama"].update(durum="bekliyor", deneme=0, hata=None, ice_alindi=None)
                    if getattr(ns, "paket_yeniden", False):  # DERİNLİK-1 R4b: bayraksız eski davranış
                        s["paket"].update(durum="bekliyor", deneme=0, hata=None, yeniden=True)
                        s["tarama"].pop("gecis", None)  # C4: tam paket → asıl rapor adı
        if getattr(ns, "incelenmedi", False):  # C4
            incelenmedi_isaretle(d, ctx["kok"])
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
    d["ikinci_goz"] = getattr(ns, "ikinci_goz", None) or d.get("ikinci_goz") or "luna"  # M5
    luna = ctx.get("luna") or (ig.or_cagir(ig.LUNA, ctx["env"]) if ctx["env"].get("OPENROUTER_API_KEY") else None)
    d["ikinci_goz_kapali"] = "--ikinci-goz yok" if d["ikinci_goz"] == "yok" else None if luna else "OPENROUTER_API_KEY yok"
    ikinci = {"kapali": d["ikinci_goz_kapali"], "luna": luna, "jev": ctx.get("jev") or _jev(ctx["env"]), "yargic": ctx.get("cagir") or hafif.cagir}
    n_par = max(1, getattr(ns, "paralel", 1) or 1)
    kos = lambda: _kos(pdir, d, Path(ctx["kok"]), Path(tdir), alt, temizle, ctx.get("cagir") or hafif.cagir, ctx["env"], ikinci,
                       d.get("kuyruk"), paralel=n_par, yalniz_paket=getattr(ns, "yalniz_paket", False))  # MÜKEMMEL-7c U10: bağlantılı video partiye verilen kuyruğa
    rota = (d.get("yonlendirme") or {}).get("tarama") or {}
    if getattr(ns, "a_yolu", False):  # O78: A taşıyıcısı yalnız açık bayrakla
        d.pop("yonlendirme", None)
    elif rota.get("saglayici") == "omniroute" and (h := YOKLA(rota.get("model"), ctx["env"])) and not (
            h.startswith("OmniRoute yok") and ctx["env"].get("OMNIROUTE_KEY")
            and not (h := _omni_baslat(rota.get("model"), ctx["env"], h, pdir))):
        print(f"DUR: OmniRoute/anahtar yok ({h})")  # O78: sessiz A düşüşü yok, çağrı 0
        return 4
    cli.INDIR_ARA = (5, 15) if n_par > 1 else None  # YT1 3: indirme başlangıçları arası rastgele boşluk yalnız paralelde
    try:
        rc = kos()
    finally:
        cli.INDIR_ARA = None
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
