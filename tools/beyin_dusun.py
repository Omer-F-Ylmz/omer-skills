"""BEYIN-DUSUN-1: düşünen 2. beyin, sonsuz öğrenme döngüsü (Claude jetonu 0; yalnız ücretsiz havuz).
  kanca  → CC kancası (stdin JSON): her araç çağrısı/istek/hata beyin-olay.jsonl'e (betik, 0 jeton)
  tur    → 2 dk'da bir TOPLU hafif tur: son 2 dk olayları TEK istekte, sağlayıcılar sırayla, kota %80'de sıradakine; olay yoksa atlar.
           Boşta (30 dk+) ya da her 2 saatte derin tur: iki model ailesi, kanıtla, elenen düzelt, Obsidian'a yaz
  kart   → "bugünün içgörüleri" kartı (kural kartıyla birlikte yazılır: kural_uret.uret)
  durum  → sayılar (öneri durumları, kota, besleme jetonu/iş)
Öneri yaşamı: taslak → (2 farklı aile ya da 2 tur) deneniyor → kanitlandi | elendi → duzelt ≤3 kez → kalici-elendi.
Kural değiştiren öneri ASLA otomatik: onay-bekliyor (Ömer'e sorulur). Besleme: ders_dongu.onek aynı blokta ≤2 madde (satirlar)."""
import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools/ogrenme"))
import atomik_yaz  # noqa: E402  Windows'ta WinError 5'e karşı yeniden deneme
import ders  # noqa: E402  sır süzgeci + kök eşleme

KOP = KOK / ".kos/kopru"
OLAY, DURUM, KOTA, ONERI, BESLEME = (KOP / n for n in ("beyin-olay.jsonl", "beyin-durum.json", "beyin-kota.json", "beyin-oneri.jsonl", "beyin-besleme.jsonl"))
KILIT, KART, ONAY, IS_KAYDI = KOP / "beyin-kilit", KOP / "icgoru-kart.md", KOP / "onay-bekliyor.md", KOP / "is-kaydi.tsv"
ALARM, OZET, DESKTOP, ETKI = (KOP / n for n in ("beyin-alarm.txt", "beyin-ozet.md", "beyin-desktop.jsonl", "beyin-etki.jsonl"))
TEKRAR, IMZA, KONTROL = (KOP / n for n in ("beyin-tekrar.jsonl", "beyin-hata-imza.json", "beyin-kontrol.md"))  # BEYIN-GERI-1
GOREV = "omer-beyin-dusun"  # onay/beyin_dusun.py zamanlanmış görevi (2 dk)
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
ICGORU, ONERILER = KASA / "20-icgoru", KASA / "10-kararlar/oneriler.md"
SIRA = ["gemini", "groq", "nvidia", "mistral", "cloudflare", "openrouter"]
LIMIT = None  # sağlayıcı günlük istek sınırı; None → havuz ENT'sinden (bkz. _limit)
ESIK, RAM_ESIK, MAX_DENEME, ISTEM_TAVAN = 0.8, 80, 3, 3500
OLLAMA_MODEL = "gemma4:12b"  # yerel yedek: hiçbir ücretsiz sağlayıcı kalmadıysa aç-işle-kapat
HATA_RE = re.compile(r"Traceback \(most|exit code [1-9]|\bFAILED\b|rc=[1-9]")
KURAL_RE = re.compile(r"\bK\d+[a-z-]*\b|CLAUDE\.md|Kurallar\.md|kural\w* (kaldır|değiştir|gevşet|sil)|nihai kural", re.I)
JSON_ISTEM = ('Yalnız JSON liste ver (en fazla {n} madde, yoksa []): [{{"tur":"hata|ucuz|hiz|kalite|arac|ram|akis","oneri":"tek kısa emir cümlesi, ≤80 karakter",'
              '"tetik":"hangi işte geçerli, 3-6 anahtar sözcük","kural":false}}]; "kural" = öneri Ömer\'in nihai kurallarını/CLAUDE.md\'yi değiştiriyorsa true.\n')
ISTEM_HAFIF = ("Aşağıda bir yazılım ajanının son 2 dakikadaki araç olayları var. Bunlardan 'bu nasıl daha hatasız / ucuz / hızlı / kaliteli yapılır' "
               "diye düşün; yalnız olaylarda KANIT olan genellenebilir öneri ver.\n" + JSON_ISTEM.format(n=3) + "Olaylar:\n")
ISTEM_DERIN = ("Aşağıda son saatlerin beyin notları, raporlar, iş kaydı ($/kalite), dersler, denetim satırları var. Yaptığımız HER ŞEY için "
               "daha hatasız / ucuz / hızlı / kaliteli yolu düşün: tekrar eden hata kalıbı → tek kural, en ucuz+kaliteli kombin, bir ajanın çözümünün "
               "başka iş türüne uyumu, eksik araç kullanımı, bir sonraki işte denenecek fikir. Yalnız kanıtlı olanı yaz.\n" + JSON_ISTEM.format(n=5) + "Kaynak:\n")
ISTEM_KOCLUK = ("Aşağıda bir ajanın işinin sonucu ve denetim satırı var. Deneyimli bir koç gibi TEK cümle yaz: 'Ben olsam ...' ile başla, bu iş türünde bir sonraki "
                "ajanın daha hatasız/ucuz/hızlı yapması için somut yöntem öner (≤140 karakter, yalnız kanıtlı çıkarım, genel öğüt yok).\nİş: ")
ISTEM_CELISKI = ("Tek kelime yanıtla: ÇELİŞİR ya da ÇELİŞMEZ. Yeni ders aşağıdaki mevcut kurallardan birine aykırı bir davranış mı öneriyor?\n"
                 "Kurallar:\n{k}\nYeni ders: {m} (tetik: {t})\n")
ISTEM_DUZELT = ('Şu öneri denendi ve kötüleştirdi. Neden kötüleştiğini düşün, düzeltilmiş halini ver. Yalnız JSON: {{"oneri":"≤80 karakter emir cümlesi","tetik":"3-6 sözcük"}}\n'
                'Öneri: {m}\nTetik: {t}\nKötüleşme: {s}\nÖnceki denemeler: {g}\n')


# ---- topla (0 jeton) ----
KAYNAK = {"istek": "cc-kanca", "arac": "cc-kanca", "durak": "cc-kanca", "ara": "kopru-ajani", "is": "kopru-ajani", "denetim": "kopru-ajani", "kapi": "kopru-ajani",
          "kurtar": "kopru-ajani", "maliyet": "kopru-ajani", "desktop": "desktop"}  # tur → olay kaynağı (kanca alt ajandaysa alt-ajan)
def olay(tur, arac="", ozet="", hata=False, kaynak=""):
    ozet = " ".join(str(ozet).split())[:200]
    if ders.sir_var(f"{arac} {ozet}"):
        return False
    kaynak = kaynak or KAYNAK.get(tur.split("-")[0], "beyin")
    OLAY.parent.mkdir(parents=True, exist_ok=True)
    with OLAY.open("ab") as f:  # satır başına tek yazım: paralel kancalar birbirini bozmaz
        f.write((json.dumps({"t": round(time.time(), 1), "tur": tur, "arac": arac, "ozet": ozet, "hata": bool(hata), "kaynak": kaynak}, ensure_ascii=False) + "\n").encode("utf-8"))
    if hata:
        _hata_izle(arac, ozet, kaynak)
    return True


# ---- BEYIN-GERI-1: hata tekrar ölçümü (sürekli) ----
def _kok(metin):
    """Türkçe harfleri ASCII'ye katla, 5 harf kök: 'parfüm'/'parfum' aynı terim."""
    return ders.kelimeler(metin.translate(str.maketrans("ğüşıöçĞÜŞİÖÇ", "gusiocGUSIOC")))


def _imza(arac, ozet):
    return " ".join(re.sub(r"\d+", "#", f"{arac} {ozet}".lower()).split())[:60]


def _kacirilan_ders(imza):
    """İmzaya en çok uyan (≥2 ortak kök) kural/kanıtlı/deneniyor ders metni; yoksa ''."""
    a, en = set(_kok(imza)), (0, "")
    for o in oneri_oku():
        if o["durum"] in ("kural", "kanitlandi", "deneniyor"):
            n = len(a & set(_kok(o["tetik"] + " " + o["metin"])))
            if n >= 2 and n > en[0]:
                en = (n, o["metin"])
    return en[1]


def _hata_izle(arac, ozet, kaynak):
    """Aynı hata imzası ikinci kez: kaynağı (iş/ajan) + kaçırılan ders beyin-tekrar.jsonl'e. Kanca asla bozulmaz."""
    try:
        imza = _imza(arac, ozet)
        goruldu = _json(IMZA, {})
        if imza in goruldu:
            with TEKRAR.open("ab") as f:
                f.write((json.dumps({"t": round(time.time(), 1), "imza": imza, "kaynak": kaynak, "onceki_kaynak": goruldu[imza],
                                     "ders": _kacirilan_ders(imza)}, ensure_ascii=False) + "\n").encode("utf-8"))
        else:
            goruldu[imza] = kaynak
            if len(goruldu) > 3000:
                goruldu = dict(list(goruldu.items())[-2000:])
            _yaz_bayt(IMZA, json.dumps(goruldu, ensure_ascii=False))
    except Exception:
        pass


def _tekrarlar(gun=7):
    if not TEKRAR.exists():
        return []
    l = [json.loads(s) for s in TEKRAR.read_text(encoding="utf-8").splitlines() if s.strip()]
    return [x for x in l if x["t"] >= time.time() - gun * 86400]


def kanca(g):
    e, ti, r = g.get("hook_event_name", ""), g.get("tool_input") or {}, g.get("tool_response")
    if e == "UserPromptSubmit":
        olay("istek", "", g.get("prompt", "")[:150])
    elif e in ("PostToolUse", "PostToolUseFailure"):
        ozet = next((str(ti[k]) for k in ("command", "file_path", "pattern", "description", "prompt", "url") if ti.get(k)), "")
        hata = e == "PostToolUseFailure" or (isinstance(r, dict) and bool(r.get("is_error") or r.get("interrupted"))) or bool(HATA_RE.search(str(r)[:600]))
        olay("arac", g.get("tool_name", ""), ozet, hata, "alt-ajan" if g.get("agent_id") else "")
    elif e in ("Stop", "SubagentStop", "SessionEnd"):
        olay("durak", "", e)


def is_olayi(ad, model, usd, dk, ok, j):
    """BEYIN-CANLI-1: biten köprü işi → 'is' olayı (iş · model · $ · süre · KABUL/DUR · tur · kalite satırı); pahalıysa nedeniyle 'maliyet' olayı."""
    u, tur_say = j.get("usage") or {}, j.get("num_turns", 0)
    kalite = re.search(r"(?im)^[^\n]*kalite[^\n]*", j.get("result") or "")
    olay("is", ad, f"{ad} · {model} · ${usd:.2f} · {dk:.0f} dk · {'KABUL' if ok else 'DUR'} · {tur_say} tur · {j.get('subtype') or '-'}"
         + (f" · {kalite.group(0).strip()[:60]}" if kalite else ""), not ok)
    if usd > 0.5:  # hedef $0.50/iş (sert değil): neden pahalı → öneri/ders için
        okuma, girdi = u.get("cache_read_input_tokens", 0), u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
        neden = [n for n, c in (("çok tur", tur_say > 30), ("büyük bağlam okuma", girdi and okuma / girdi > 0.9 and girdi > 5000), ("uzun bekleme", dk > 15)) if c]
        olay("maliyet", ad, f"pahalı iş {ad}: ${usd:.2f}, {tur_say} tur, {dk:.0f} dk; neden: {', '.join(neden) or 'belirsiz'}")


def ara_olay(ad, dk):
    olay("ara", ad, f"{ad} çalışıyor, {dk:.0f}. dakika")


def _baslat():
    """Zamanlanmış görevi hemen koştur (pencere yok)."""
    subprocess.run(["schtasks", "/Run", "/TN", GOREV], capture_output=True, creationflags=0x08000000)


def bekci(calisan_say, simdi=None):
    """Sessiz ölüm olmasın: çalışan ajan varken son 5 dk'da olay yoksa ya da döngü 6 dk'dır tur atmadıysa → beyin-alarm.txt; döngü ölüyse görevi yeniden başlatır."""
    simdi, sorun = simdi or time.time(), []
    tur_t = _json(DURUM, {}).get("tur_t")
    if tur_t is not None and simdi - tur_t > 360:
        sorun.append(f"döngü ölü: son tur {(simdi - tur_t) / 60:.0f} dk önce")
        _baslat()
    if calisan_say:
        olaylar, _ = _olay_oku(0)
        son = olaylar[-1]["t"] if olaylar else 0
        if simdi - son > 300:
            sorun.append(f"olay yok: {calisan_say} ajan çalışırken son olay {(simdi - son) / 60:.0f} dk önce")
    if not sorun:
        if ALARM.exists() and simdi - ALARM.stat().st_mtime > 600:  # sorun geçti; Desktop'un görmesi için alarm 10 dk kalır
            ALARM.unlink(missing_ok=True)
        return "ok"
    _yaz_bayt(ALARM, f"{time.strftime('%d %H:%M')} " + " · ".join(sorun) + "\n")
    return "alarm"


def bekci_canli(simdi=None):
    """NİHAİ-KAPI-1: (canlı?, sebep). Canlı = beyin döngüsü ≤6 dk'da tur attı VE son olay ≤5 dk ('kapi' olayları sayılmaz); ölüyse görevi yeniden başlatır."""
    simdi = simdi or time.time()
    tur_t = _json(DURUM, {}).get("tur_t")
    if tur_t is None or simdi - tur_t > 360:
        _baslat()
        return False, "bekçi ölü: döngü " + ("hiç tur atmadı" if tur_t is None else f"{(simdi - tur_t) / 60:.0f} dk önce son tur attı")
    olaylar, _ = _olay_oku(0)
    son = max((o["t"] for o in olaylar if o["tur"] != "kapi"), default=0)
    if simdi - son > 300:
        return False, f"son beyin olayı {(simdi - son) / 60:.0f} dk önce (>5 dk)"
    return True, ""


def bekci_yokla(simdi=None):
    """NİHAİ-KAPI-1 CC SessionStart: beyin döngüsü ölüyse (tur_t >6 dk ya da yok) yeniden başlatır, oturuma uyarı satırı döner; canlıysa ''."""
    tur_t = _json(DURUM, {}).get("tur_t")
    if tur_t is not None and (simdi or time.time()) - tur_t <= 360:
        return ""
    _baslat()
    return "UYARI (NİHAİ 31+32): beyin bekçisi ölüydü, yeniden başlatıldı; olayları elle yazma, birkaç dk sonra `beyin_dusun.py durum` bak.\n"


def desktop_al():
    """beyin-desktop.jsonl'daki yeni Desktop notları → olay günlüğü (satır ofseti DURUM'da)."""
    if not DESKTOP.exists():
        return 0
    d, satir = _json(DURUM, {}), DESKTOP.read_text(encoding="utf-8", errors="replace").splitlines()
    yeni = satir[d.get("desk_ofset", 0):]
    for s in yeni:
        try:
            x = json.loads(s)
        except ValueError:
            continue
        olay("desktop-" + str(x.get("tur", "not")), "desktop", f"{x.get('ozet', '')} → {x.get('ders', '')}", x.get("tur") == "hata")
    _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "desk_ofset": len(satir)}))
    return len(yeni)


def _olay_oku(ofset):
    if not OLAY.exists():
        return [], ofset
    with OLAY.open("rb") as f:
        f.seek(ofset)
        ham = f.read()
    bitis = ham.rfind(b"\n") + 1  # yarım son satır sonraki tura
    out = []
    for s in ham[:bitis].decode("utf-8", "replace").splitlines():
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if isinstance(x, dict) and x.get("tur"):  # beyin_kayit.py gibi şemasız satırlar döngüyü çökertmesin
            o = {"t": 0, "arac": "", "ozet": "", "hata": False, **x}
            if not isinstance(o["t"], (int, float)):  # beyin_kayit.py tarih dizgisi yazabilir; sayıya zorla (döngü TypeError ile ölmesin)
                o["t"] = 0
            out.append(o)
    return out, ofset + bitis


def _ozet_olay(olaylar):
    c, hatalar = Counter(o["arac"] or o["tur"] for o in olaylar), [o for o in olaylar if o["hata"]]
    satir = [f"{len(olaylar)} olay; araç: " + ", ".join(f"{k}×{v}" for k, v in c.most_common(8)), f"hata: {len(hatalar)}"]
    satir += [f"HATA {o['arac']}: {o['ozet'][:120]}" for o in hatalar[:8]]
    satir += [f"istek: {o['ozet'][:120]}" for o in olaylar if o["tur"] == "istek"][-5:]
    satir += [f"{o['arac']}: {o['ozet'][:100]}" for o in olaylar if o["tur"] == "arac" and not o["hata"]][-12:]
    return "\n".join(satir)[:ISTEM_TAVAN]


# ---- durum / kota ----
def _json(yol, varsayilan):
    try:
        return json.loads(yol.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return varsayilan


def _yaz_bayt(yol, metin):
    atomik_yaz.yaz_bayt(yol, metin.encode("utf-8"))  # CRLF'siz


def _kota():
    bugun = time.strftime("%Y-%m-%d", time.gmtime())
    k = _json(KOTA, {})
    return k if k.get("gun") == bugun else {"gun": bugun, "p": {}}


def _kota_ekle(prov, jeton=0):
    k = _kota(); v = k["p"].setdefault(prov, [0, 0])
    v[0] += 1; v[1] += jeton; k["son"] = prov
    _yaz_bayt(KOTA, json.dumps(k))


def _limit(prov):
    if LIMIT is not None:
        return LIMIT.get(prov, 0)
    import ucretsiz_havuz as h
    kova = {}
    for e in h.ENT:
        if e.prov == prov and h.Z in e.turler:
            kova[e.kova or h.ad(e)] = e.rpd
    return sum(kova.values())


def siradaki(haric=()):
    """Sıralı dağıtım: son kullanılandan sonraki sağlayıcı; günlük istek sınırının %80'ine gelen atlanır; hepsi doluysa None."""
    k = _kota(); i = SIRA.index(k["son"]) + 1 if k.get("son") in SIRA else 0
    for p in SIRA[i:] + SIRA[:i]:
        if p not in haric and k["p"].get(p, [0])[0] < ESIK * _limit(p):
            return p
    return None


def _ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in "abcdefg"]
    m = M(); m.l = ctypes.sizeof(M)
    try:
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    except (AttributeError, OSError):
        return 0
    return m.yuk


def _havuz(tur, istem, **kw):
    sys.path.insert(0, str(KOK / "tools"))
    import nihai_ozet, ucretsiz_havuz
    return ucretsiz_havuz.cagir(tur, nihai_ozet.OZET + istem, **kw)  # NİHAİ-KAPI-1


def _aile(kaynak):
    import ucretsiz_havuz as h
    return next((e.aile for e in h.ENT if h.ad(e) == kaynak), (kaynak or "").split("/")[0])


def _ollama(istem, max_tokens):
    """Yerel Ollama: sunucu kapalıysa aç, işle, kapat (RAM sonra serbest). Yanıt yoksa None.
    YEREL-KAPALI (Ömer 23 Eki 18:03): .kos/yerel-model.kapali varken yerel model hiç açılmaz; bulut ücretsiz havuz kullanılır."""
    import urllib.request
    if (KOK / ".kos" / "yerel-model.kapali").exists():
        return None

    def uc(yol, veri=None, zaman=5):
        r = urllib.request.Request("http://127.0.0.1:11434" + yol, data=json.dumps(veri).encode() if veri else None, headers={"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(r, timeout=zaman))
    proc = None
    try:
        try:
            uc("/api/tags", zaman=2)
        except OSError:
            proc = subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
            for _ in range(30):
                time.sleep(1)
                try:
                    uc("/api/tags", zaman=2); break
                except OSError:
                    pass
        y = uc("/api/chat", {"model": OLLAMA_MODEL, "stream": False, "think": False, "keep_alive": 0, "messages": [{"role": "user", "content": istem}],
                             "options": {"num_ctx": 8192, "num_predict": max_tokens}}, zaman=180)
        return (y.get("message") or {}).get("content") or None
    except (OSError, ValueError, KeyError):
        return None
    finally:
        if proc:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True, creationflags=0x08000000)


def _sor(tur, istem, max_tokens, zaman=60, rotasyon=True, **kw):
    """→ (metin, kaynak). rotasyon: sağlayıcılar sırayla (hafif tur); değilse havuz seçer (derin tur). Her deneme kotaya yazılır. Claude'a düşmez (haiku_tavan=0)."""
    denenen = set()
    while True:
        p = siradaki(denenen) if rotasyon else None
        if rotasyon and p is None:  # sıradaki sağlayıcılar dolu → önce tüm bulut havuzu (havuz kendisi seçer), yerel Ollama en son ve yalnız kapalı bayrağı yoksa
            y, k, _ = _havuz(tur, istem, max_tokens=max_tokens, zaman=zaman, **kw)
            if y:
                return y, k
            y = _ollama(istem, max_tokens) if _ram() < RAM_ESIK else None
            return (y, "ollama/yerel") if y else (None, None)
        y, k, _ = _havuz(tur, istem, max_tokens=max_tokens, zaman=zaman, **({"saglayici": p} if p else {}), **kw)
        _kota_ekle(p or (k or "?/?").split("/")[0], len(istem) // 3 + max_tokens)
        if y or not rotasyon:
            return y, k
        denenen.add(p)


def _liste(metin):
    try:
        j = json.loads(metin[metin.index("["):metin.rindex("]") + 1])
    except ValueError:
        return []
    return [x for x in j if isinstance(x, dict)] if isinstance(j, list) else []


# ---- öneri deposu ----
def oneri_oku():
    return [json.loads(s) for s in ONERI.read_text(encoding="utf-8").splitlines() if s.strip()] if ONERI.exists() else []


def _oneri_yaz(liste):
    _yaz_bayt(ONERI, "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in liste))


def _kurallar():
    """Mevcut kural satırları: Kurallar.md (Obsidian) + kalıcılaşmış (durum=kural) dersler."""
    kf = KASA / "10-kararlar/Kurallar.md"
    satir = [s.strip() for s in kf.read_text(encoding="utf-8", errors="replace").splitlines() if len(s.strip()) > 20] if kf.exists() else []
    return satir + [x["metin"] for x in oneri_oku() if x["durum"] == "kural"]


def celiski(metin, tetik):
    """→ çelişen kural satırı | ''. Kural eşleştirme (≥2 ortak kök, en çok 3 aday) sonra ücretsiz model: ÇELİŞİR/ÇELİŞMEZ."""
    a = set(ders.kelimeler(metin + " " + tetik))
    aday = sorted(((len(a & set(ders.kelimeler(k))), k) for k in _kurallar()), reverse=True)
    aday = [k for n, k in aday[:3] if n >= 2]
    if not aday:
        return ""
    y, _ = _sor("ozet", ISTEM_CELISKI.format(k="\n".join("- " + k[:200] for k in aday), m=metin, t=tetik), 20)
    return aday[0] if y and re.search(r"ÇELİŞİR", y.upper()) and "ÇELİŞMEZ" not in y.upper() else ""


def oneri_ekle(o, kaynak):
    """→ ('yeni'|'destek'|'ret', öneri). Benzer öneri birleşir; farklı 2 aile ya da kaynak → deneniyor (kural değiştiren hariç)."""
    metin, tetik = str(o.get("oneri", "")).strip()[:90], str(o.get("tetik", "")).strip()[:80]
    if len(metin) < 8 or ders.sir_var(metin + " " + tetik):
        return "ret", None
    kural = bool(o.get("kural")) or bool(KURAL_RE.search(metin))
    liste, anahtar = oneri_oku(), set(ders.kelimeler(metin + " " + tetik))
    for x in liste:
        b = set(ders.kelimeler(x["metin"] + " " + x["tetik"]))
        if anahtar and len(anahtar & b) / len(anahtar | b) >= 0.6:
            if x["durum"] == "kalici-elendi":
                return "ret", x
            x["destek"] += 1
            x["kural"] = x["kural"] or kural
            if kaynak not in x["kaynaklar"]:
                x["kaynaklar"].append(kaynak)
            if x["durum"] == "taslak" and len({_aile(s) for s in x["kaynaklar"]}) >= 2:
                x["durum"] = "onay-bekliyor" if x["kural"] else "deneniyor"
            _oneri_yaz(liste)
            return "destek", x
    cakisan = celiski(metin, tetik)
    if cakisan:
        olay("celiski", kaynak, f"çelişki: '{metin[:60]}' ↔ '{cakisan[:60]}'")
        return "ret", None
    yeni = {"id": hashlib.sha1(metin.encode()).hexdigest()[:6], "metin": metin, "tetik": tetik, "tur": str(o.get("tur", ""))[:12], "kural": kural,
            "durum": "taslak", "destek": 1, "kaynaklar": [kaynak], "olusma": time.time(), "deneme": 0, "sebep": "", "gecmis": []}
    _oneri_yaz(liste + [yeni])
    return "yeni", yeni


def _is_oku():
    """[(epoch, usd, hata)] — is-kaydi.tsv; hata = sonuc success/rc0 dışı."""
    if not IS_KAYDI.exists():
        return []
    out = []
    for s in IS_KAYDI.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        c = s.split("\t")
        try:
            out.append((time.mktime(time.strptime(c[0], "%Y-%m-%d %H:%M")), float(c[6]), c[7] not in ("success", "rc0")))
        except (ValueError, IndexError):
            pass
    return sorted(out)


def _ort(rows):
    return sum(r[1] for r in rows) / len(rows), sum(r[2] for r in rows) / len(rows)


def _etki_yaz(x):
    with ETKI.open("ab") as f:
        f.write((json.dumps(x, ensure_ascii=False) + "\n").encode("utf-8"))


def kanitla(min_n=3):
    """Önerinin beslendiği işler (besleme anından sonraki ilk iş satırı) ↔ diğer işler: $ ve hata oranı. İyileşti → kanitlandi, kötüleşti → elendi (kural ise geri-cekildi); her karar etki defterine."""
    rows, besleme, liste = _is_oku(), [json.loads(s) for s in BESLEME.read_text(encoding="utf-8").splitlines() if s.strip()] if BESLEME.exists() else [], oneri_oku()
    for o in liste:
        if o["durum"] not in ("deneniyor", "kanitlandi", "kural"):
            continue
        bagli = set()
        for t in sorted(x["t"] for x in besleme if o["id"] in x["ids"] and x["t"] >= o["olusma"]):
            i = next((i for i, r in enumerate(rows) if t < r[0] <= t + 10800 and i not in bagli), None)
            if i is not None:
                bagli.add(i)
        w, wo = [rows[i] for i in sorted(bagli)], [r for i, r in enumerate(rows) if i not in bagli and r[0] >= o["olusma"]]
        if len(w) < min_n or len(wo) < min_n:
            continue
        (uw, hw), (uo, ho) = _ort(w), _ort(wo)
        ozet = f"önerili {len(w)} iş ${uw:.2f} hata %{hw * 100:.0f}; diğer {len(wo)} iş ${uo:.2f} hata %{ho * 100:.0f}"
        kotu = hw > ho or uw > 1.25 * uo
        _etki_yaz({"t": time.time(), "id": o["id"], "metin": o["metin"], "is": len(w), "usd_ile": round(uw, 2), "usd_siz": round(uo, 2),
                   "hata_ile": round(hw, 2), "hata_siz": round(ho, 2), "karar": "geri" if kotu and o["durum"] == "kural" else "elendi" if kotu else "kal"})
        if kotu and o["durum"] == "kural":  # BEYIN-CANLI-1b: kurala dönmüş ders zarar verdi → otomatik geri çek, nedeni beyne
            o["durum"], o["sebep"] = "geri-cekildi", ozet
            olay("geri-cekildi", o["id"], f"geri çekildi '{o['metin'][:60]}': {ozet}", True)
        elif kotu:
            o["durum"], o["sebep"] = "elendi", ozet
        elif o["durum"] == "deneniyor" and hw <= ho and uw <= 1.1 * uo and (hw < ho or uw < uo):
            o["durum"], o["sebep"] = "kanitlandi", ozet
    _oneri_yaz(liste)


def duzelt():
    """Elenen çöpe gitmez: neden kötüleştiği düşünülür, düzeltilmiş hali yeni taslak; ≤3 yeniden deneme sonra kalici-elendi."""
    liste = oneri_oku()
    for o in liste:
        if o["durum"] != "elendi":
            continue
        if o["deneme"] >= MAX_DENEME:
            o["durum"] = "kalici-elendi"; continue
        y, k = _sor("ozet", ISTEM_DUZELT.format(m=o["metin"], t=o["tetik"], s=o["sebep"], g=" | ".join(g["metin"] for g in o["gecmis"]) or "-"), 300)
        try:
            j = json.loads(y[y.index("{"):y.rindex("}") + 1]) if y else {}
        except ValueError:
            j = {}
        m = str(j.get("oneri", "")).strip()[:90]
        if len(m) < 8 or ders.sir_var(m):
            continue
        o["gecmis"].append({"metin": o["metin"], "sebep": o["sebep"]})
        o.update(metin=m, tetik=str(j.get("tetik", o["tetik"]))[:80], durum="taslak", deneme=o["deneme"] + 1, kaynaklar=[k], destek=1, olusma=time.time())
    _oneri_yaz(liste)


# ---- koçluk ($0: notu ücretsiz model üretir; Desktop yalnız kaçırdığını ekler) ----
def kocluk_ekle(hedef, metin, kaynak):
    """Koçluk notu → öneri deposu (tur=kocluk, ikinci aileyi beklemez: deneniyor). Etkisi kanitla ile ölçülür."""
    d, x = oneri_ekle({"tur": "kocluk", "oneri": metin, "tetik": hedef, "kural": False}, kaynak)
    if x and x["durum"] == "taslak":
        liste = oneri_oku()
        for o in liste:
            if o["id"] == x["id"]:
                o["durum"], o["tur"] = "deneniyor", "kocluk"
        _oneri_yaz(liste)
    return d


def kocluk_uret(ad, sonuc):
    """Biten işin sonuç/denetim satırından 'ben olsam' notu (ücretsiz model, Claude yok) → olay tur=kocluk, kaynak=ucretsiz."""
    y, k = _sor("ozet", ISTEM_KOCLUK + f"{ad}: {sonuc}"[:900], 120)
    y = " ".join((y or "").split())[:160]
    if len(y) < 15:
        return False
    return olay("kocluk", f"ucretsiz:{k}", y)


def kocluk_isle(en_cok=2):
    """Yeni biten işler ('is' olayı) + denetim satırları → kocluk_uret; ofset DURUM'da (koc_t)."""
    d = _json(DURUM, {})
    olaylar, _ = _olay_oku(0)
    yeni = [o for o in olaylar if o["tur"] == "is" and o["t"] > d.get("koc_t", 0)]
    for o in sorted(yeni, key=lambda o: not o["hata"])[:en_cok]:
        den = " | ".join(x["ozet"] for x in olaylar if x["tur"] == "denetim" and x["arac"] == o["arac"])
        kocluk_uret(o["arac"], o["ozet"] + (" · " + den if den else ""))
    if yeni:
        _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "koc_t": max(o["t"] for o in yeni)}))
    return len(yeni)


def kocluk_oku():
    """beyin-desktop.jsonl'daki tur=kocluk satırları → koçluk önerisi (kaynak desktop); ofset DURUM'da."""
    if not DESKTOP.exists():
        return 0
    d, satir = _json(DURUM, {}), DESKTOP.read_text(encoding="utf-8", errors="replace").splitlines()
    n = 0
    for s in satir[d.get("koc_ofset", 0):]:
        try:
            x = json.loads(s)
        except ValueError:
            continue
        if isinstance(x, dict) and x.get("tur") == "kocluk":
            kocluk_ekle(str(x.get("hedef", "")) + " " + str(x.get("ders", "")), str(x.get("ozet", "")) or str(x.get("ders", "")) or str(x.get("not", "")), "desktop/kocluk")
            n += 1
    _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "koc_ofset": len(satir)}))
    return n


# ---- yaz ----
def yaz_icgoru(yeniler, baslik):
    if not yeniler:
        return
    ICGORU.mkdir(parents=True, exist_ok=True)
    p = ICGORU / (time.strftime("%Y-%m-%d") + ".md")
    ek = f"\n## {time.strftime('%H:%M')} {baslik}\n" + "".join(f"- [{x['id']}] ({x['durum']}) {x['metin']} — {x['tetik']} · {x['kaynaklar'][0]}\n" for x in yeniler)
    p.write_bytes((p.read_bytes() if p.exists() else f"# İçgörüler {p.stem}\n".encode("utf-8")) + ek.encode("utf-8"))


def yaz_oneriler():
    liste, bolum = oneri_oku(), []
    for d in ("onay-bekliyor", "kanitlandi", "deneniyor", "taslak", "elendi", "kalici-elendi"):
        sec = [x for x in liste if x["durum"] == d]
        if sec:
            bolum.append(f"## {d} ({len(sec)})\n" + "".join(f"- [{x['id']}] {x['metin']} — {x['tetik']} · destek {x['destek']} · deneme {x['deneme']}"
                                                          + (f" · {x['sebep']}" if x["sebep"] else "") + "\n" for x in sec))
    _yaz_bayt(ONERILER, "# Öneriler (beyin-dusun, otomatik; elle düzenleme)\n\n" + "\n".join(bolum))
    bekleyen = [x for x in liste if x["durum"] == "onay-bekliyor"]
    _yaz_bayt(ONAY, "# Onay bekliyor (Ömer'in kurallarını değiştirir; otomatik uygulanmaz)\n\n" + "".join(f"- [{x['id']}] {x['metin']} ({x['tetik']})\n" for x in bekleyen))


def kurala_cevir(min_destek=3):
    """BEYIN-CANLI-1: destek ≥3 ve çelişki yoksa (kötüleşip düzeltilmiş değil, elenmiş benzeri yok) öneri 'kural' olur. Ömer'in kurallarını değiştirenler (kural=True) onay bekler."""
    liste, n = oneri_oku(), 0
    elenen = [set(ders.kelimeler(x["metin"] + " " + x["tetik"])) for x in liste if x["durum"] in ("elendi", "kalici-elendi")]
    for o in liste:
        if o["durum"] not in ("taslak", "deneniyor", "kanitlandi") or o["kural"] or o["destek"] < min_destek or o["gecmis"]:
            continue
        a = set(ders.kelimeler(o["metin"] + " " + o["tetik"]))
        if any(a and len(a & e) / len(a | e) >= 0.4 for e in elenen):
            continue
        o["durum"], n = "kural", n + 1
    if n:
        _oneri_yaz(liste)
    return n


def gosterge(liste, olaylar):
    """ÖĞRENME-2 canlı gösterge (tek satır): bugün olay · yeni ders · kurala dönen · geri çekilen · $ 7 gün eğilimi · tekrar eden hata oranı (7 gün)."""
    simdi, gun = time.time(), 86400
    bugun = time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d"))
    rows = _is_oku()
    son7, onceki7 = [r for r in rows if r[0] >= simdi - 7 * gun], [r for r in rows if simdi - 14 * gun <= r[0] < simdi - 7 * gun]
    egilim = f"${_ort(son7)[0]:.2f} (önceki 7g " + (f"${_ort(onceki7)[0]:.2f})" if onceki7 else "-)") if son7 else "-"
    hatalar = [o["ozet"][:60] for o in olaylar if o["hata"] and o["t"] >= simdi - 7 * gun]
    tekrar = f"%{100 * (len(hatalar) - len(set(hatalar))) / len(hatalar):.0f}" if hatalar else "-"
    return (f"GÖSTERGE: bugün {sum(o['t'] >= bugun for o in olaylar)} olay · yeni ders {sum(x['olusma'] >= bugun for x in liste)} · "
            f"kurala dönen {sum(x['durum'] == 'kural' for x in liste)} · geri çekilen {sum(x['durum'] in ('elendi', 'kalici-elendi') for x in liste)} · "
            f"iş başı $ 7g {egilim} · tekrar eden hata {tekrar} ({len(hatalar)} hata) · canlı tekrar {len(_tekrarlar())}")


def tekillestir(metinler, esik=0.4, en_az=3):
    """Anlamsal tekilleştirme (0 jeton): kök kümesi örtüşmesi ≥esik ve ≥en_az ortak kök → aynı kural. [(ilk metin, sayı)], sıra korunur."""
    gruplar = []  # [metin, say, kök kümesi (birleşim)]
    for m in metinler:
        a = set(_kok(m))
        for g in gruplar:
            ort = len(a & g[2])
            if ort >= en_az and a and ort / min(len(a), len(g[2])) >= esik:
                g[1], g[2] = g[1] + 1, g[2] | a
                break
        else:
            gruplar.append([m, 1, a])
    return [(g[0], g[1]) for g in gruplar]


def _kural_satirlari(liste, durumlar, n):
    uyan = sorted((x for x in liste if x["durum"] in durumlar), key=lambda x: -x["destek"])
    return [f"{m[:100]}" + (f" (×{s})" if s > 1 else "") for m, s in tekillestir([x["metin"] for x in uyan])[:n]]


def ozet_yaz():
    """Desktop her kontrolde, CC SessionStart'ta okur: ≤20 satır (alarm · kurallar · kanıtlı içgörüler · son maliyet dersleri · iş başı ortalama $)."""
    liste, olaylar, satir = oneri_oku(), _olay_oku(0)[0], []
    if ALARM.exists():
        satir.append("ALARM: " + ALARM.read_text(encoding="utf-8").strip()[:150])
    son = [o["t"] for o in olaylar][-1:] or [0]
    satir.append(f"BEYİN ÖZETİ {time.strftime('%d %H:%M')} · son olay {(time.time() - son[0]) / 60:.0f} dk önce · toplam olay {len(olaylar)}")
    kurallar = _kural_satirlari(liste, ("kural",), 6)
    satir += ["KURAL: " + k for k in kurallar]
    satir += ["KANITLI: " + k for k in _kural_satirlari(liste, ("kanitlandi",), 4)]
    satir += ["MALİYET: " + o["ozet"][:120] for o in [o for o in olaylar if o["tur"] == "maliyet"][-3:]]
    rows = _is_oku()[-20:]
    if rows:
        u, h = _ort(rows)
        satir.append(f"İŞ BAŞI ORT: son {len(rows)} iş ${u:.2f}, hata %{h * 100:.0f} (hedef $0.50)")
    tek = _tekrarlar()[-1:]
    kont = [s for s in satir[:2] if s.startswith(("ALARM", "BEYİN"))] + ["KURAL: " + k for k in kurallar[:4]]
    if tek:
        satir.append(f"TEKRAR HATA: {tek[0]['imza'][:60]} ← {tek[0]['kaynak']}; kaçırılan ders: {tek[0]['ders'][:60] or '(yok)'}")
        kont.append(satir[-1])
    satir.append(gosterge(liste, olaylar))
    _yaz_bayt(OZET, "\n".join(satir[:20]) + "\n")
    _yaz_bayt(KONTROL, "KONTROL BAŞINDA OKU (beyin geri okuma)\n" + "\n".join(kont + [satir[-1]])[:1500] + "\n")  # Desktop: kısa dosya


def geri_oku(gorev, ad="", tavan=2400):
    """BEYIN-GERI-1: işin başına enjekte edilecek blok (0 jeton, ücretsiz): beyin-özet + göreve uyan kanıtlı ders + Obsidian 50-dersler/90-log
    eşleşmeleri (≥3 ortak kök, dosya başına en uygun satır) + uyan tekrar-hata. Hiçbiri yoksa ''."""
    parca = []
    if OZET.exists():
        parca.append("\n".join(OZET.read_text(encoding="utf-8", errors="replace").splitlines()[:20])[:1200])
    s = satirlar(gorev)
    if s:
        parca.append("İlgili ders:\n" + s)
    sorgu, bulunan = set(_kok(f"{gorev[:600]} {ad}")), []
    for alt, en_cok in (("50-dersler", 300), ("90-log", 12)):
        d = KASA / alt
        dosyalar = sorted(d.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:en_cok] if d.exists() else []
        for p in dosyalar:
            try:
                satirlar_ = [x.strip() for x in p.read_text(encoding="utf-8", errors="replace").splitlines() if len(x.strip()) > 15][:80]
            except OSError:
                continue
            ort = len(sorgu & set(_kok(p.stem + " " + " ".join(satirlar_))))
            if ort >= 3:
                en = max(satirlar_, key=lambda x: len(sorgu & set(_kok(x))), default="")
                bulunan.append((ort, f"- {alt}/{p.name}: {en.lstrip('#- ').strip()[:140]}"))
    if bulunan:
        parca.append("Geçmiş dersler/hatalar:\n" + "\n".join(x for _, x in sorted(bulunan, reverse=True)[:3]))
    tek = [t for t in reversed(_tekrarlar(30)) if len(sorgu & set(_kok(t["imza"]))) >= 2][:2]
    if tek:
        parca.append("Tekrar eden hata:\n" + "\n".join(f"- {t['imza']} → {t['ders'] or 'ders yok'}" for t in tek))
    return ("[BEYİN GERİ OKUMA]\n" + "\n".join(parca))[:tavan] + "\n" if parca else ""


def kart_metin():
    k = sorted((x for x in oneri_oku() if x["durum"] == "kanitlandi" and not x["kural"]), key=lambda x: -x["destek"])[:3]
    return ("BUGÜNÜN İÇGÖRÜLERİ (kanıtlı): " + " · ".join(x["metin"] for x in k))[:400] + "\n" if k else ""


# ---- besle ----
def satirlar(gorev):
    """Göreve uyan (≥2 ortak kelime-kökü) kanıtlı ≤2 madde, madde başına tek kısa emir; uyan yoksa ''. deneniyor olanlar işlerin yarısına (A/B kanıtı)."""
    if os.environ.get("BEYIN_DUSUN"):
        return ""
    try:
        with BESLEME.with_suffix(".say").open("ab") as f:
            f.write(b".")  # iş sayacı: jeton/iş ortalaması için
        sorgu, ab = set(ders.kelimeler(gorev[:600])), int(hashlib.sha1(gorev[:600].encode()).hexdigest()[:2], 16) % 2
        aday = []
        for o in oneri_oku():
            koc = o["tur"] == "kocluk"
            if o["durum"] not in ("kural", "kanitlandi", "deneniyor") or o["kural"] or (o["durum"] == "deneniyor" and ab and not koc):
                continue
            ortak = len(sorgu & set(ders.kelimeler(o["tetik"] + " " + o["metin"])))
            if ortak >= 2:
                aday.append((3 if koc else {"kural": 2, "kanitlandi": 1}.get(o["durum"], 0), ortak, o["destek"], o))
        sec = [a[3] for a in sorted(aday, key=lambda a: a[:3], reverse=True)[:2]]
        if not sec:
            return ""
        blok = "\n".join(f"- {'KOÇLUK: ' if o['tur'] == 'kocluk' else ''}{o['metin'][:80]}" for o in sec)
        with BESLEME.open("ab") as f:
            f.write((json.dumps({"t": time.time(), "ids": [o["id"] for o in sec], "jeton": len(blok) // 3}) + "\n").encode("utf-8"))
        return blok
    except Exception:
        return ""


# ---- düşün ----
def tur():
    """Hafif tur → 'atla' (olay yok) | 'kota-dolu' (Ollama da yok/RAM yüksek) | 'havuz-yok' | 'ok'. Başarısızlıkta ofset ilerlemez (olaylar kaybolmaz)."""
    d = _json(DURUM, {})
    olaylar, ofset = _olay_oku(d.get("ofset", 0))
    if not olaylar:
        return "atla"
    y, k = _sor("ozet", ISTEM_HAFIF + _ozet_olay(olaylar), 700)
    if k is None:
        return "kota-dolu"
    if not y:
        return "havuz-yok"
    yeniler = [x for o in _liste(y) for s, x in [oneri_ekle(o, k)] if s == "yeni"]
    yaz_icgoru(yeniler, "hafif tur")
    yaz_oneriler()
    _yaz_bayt(DURUM, json.dumps({**d, "ofset": ofset, "olay_say": d.get("olay_say", 0) + len(olaylar)}))
    return "ok"


def _derin_kaynak():
    """Son 6 saatin beyin notları + raporlar + iş kaydı + dersler + DENETİM satırları (betik okur, jeton yok), ≤9000 karakter."""
    sinir, parca = time.time() - 6 * 3600, []
    for kl, n, kes in ((KASA / "40-projeler", 4, 300), (KASA / "50-dersler", 4, 300), (KOP / "rapor", 5, 500)):
        for p in sorted((q for q in kl.glob("*.md") if q.stat().st_mtime > sinir), key=lambda q: -q.stat().st_mtime)[:n] if kl.is_dir() else []:
            parca.append(f"[{kl.name}/{p.name}] " + " ".join(p.read_text(encoding="utf-8", errors="replace").split())[:kes])
            parca += [s.strip()[:200] for s in p.read_text(encoding="utf-8", errors="replace").splitlines() if "DENETİM" in s][:2]
    rows = _is_oku()[-40:]
    if rows:
        u, h = _ort(rows)
        parca.append(f"[is-kaydi son {len(rows)} iş] ort ${u:.2f}, hata %{h * 100:.0f}")
    dersler = KOK / "tools/dersler.jsonl"
    if dersler.exists():
        for s in dersler.read_text(encoding="utf-8").splitlines()[-8:]:
            x = json.loads(s); parca.append(f"[ders] {x['tetik']} → {x['dogru']}")
    olaylar, _ = _olay_oku(0)
    if olaylar:
        parca.append("[olay günlüğü] " + _ozet_olay(olaylar[-300:])[:1500])
    return "\n".join(parca)[:9000]


def ders_isle():
    """DERS-DONGU-1: RED/DUR satırlarından ücretsiz havuzla ders üret (tools/ders_dongu.py). → yeni ders sayısı."""
    sys.path.insert(0, str(KOK / "tools"))
    import ders_dongu
    return ders_dongu.dongu()


def derin():
    """Derin tur: iki model ailesi; uyuşan → deneniyor, uyuşmayan taslak. Sonra kanıtla, elenen düzelt, Obsidian/kart yaz."""
    try:
        ders_isle()
    except Exception as e:  # ders havuzu kilitli/çökük olsa da derin tur sürer
        olay("hata", "ders_dongu", f"ders döngüsü düştü: {e}", True, "beyin-dusun")
    istem = ISTEM_DERIN + _derin_kaynak()
    y1, k1 = _sor("hakem", istem, 1500, 120, rotasyon=False)
    if not y1:
        return "havuz-yok"
    y2, k2 = _sor("hakem", istem, 1500, 120, rotasyon=False, haric_aile=_aile(k1))
    yeniler = [x for y, k in ((y1, k1), (y2, k2)) if y for o in _liste(y) for s, x in [oneri_ekle(o, k)] if s == "yeni"]
    kanitla(); duzelt()
    yaz_icgoru(yeniler, "derin tur"); yaz_oneriler(); KART.write_bytes(kart_metin().encode("utf-8"))
    _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "derin_t": time.time(), "olay_say": 0}))
    return "ok"


def _kilit_al():
    try:
        os.close(os.open(KILIT, os.O_CREAT | os.O_EXCL))
        return True
    except FileExistsError:
        if time.time() - KILIT.stat().st_mtime > 600:  # bayat (tek döngü ≤10 dk)
            KILIT.unlink(missing_ok=True)
        return False


def calis():
    """Zamanlanmış görevin girişi (2 dk): hafif tur; derin tur 2 saatte bir ya da boşta (olay var, 30 dk geçti). Tek süreç (kilit)."""
    os.environ["BEYIN_DUSUN"] = "1"  # kendi çağrılarımıza içgörü beslenmesin
    if not _kilit_al():
        return "mesgul"
    try:
        desktop_al(); kocluk_oku()
        r = tur(); kocluk_isle() if r == "ok" else None
        d = _json(DURUM, {}); gec = time.time() - d.get("derin_t", 0)
        if r != "bekle" and (gec >= 7200 or (r == "atla" and gec >= 1800 and d.get("olay_say", 0) > 0)):
            r += "+derin:" + derin()
        if r != "bekle":
            kurala_cevir(); yaz_oneriler()
        ozet_yaz()
        _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "tur_t": time.time()}))
        return r
    except Exception as e:  # sessiz ölüm yok: alarm + tur_t ilerler (bekçi "ölü" saymasın, Desktop alarmı okur)
        _yaz_bayt(ALARM, f"{time.strftime('%d %H:%M')} döngü hatası: {type(e).__name__}: {str(e)[:120]}\n")
        _yaz_bayt(DURUM, json.dumps({**_json(DURUM, {}), "tur_t": time.time()}))
        return "hata"
    finally:
        KILIT.unlink(missing_ok=True)


def durum():
    sayi, b = Counter(x["durum"] for x in oneri_oku()), [json.loads(s) for s in BESLEME.read_text(encoding="utf-8").splitlines() if s.strip()] if BESLEME.exists() else []
    is_say = BESLEME.with_suffix(".say").stat().st_size if BESLEME.with_suffix(".say").exists() else 0
    return {"oneri": dict(sayi), "tur_t": _json(DURUM, {}).get("tur_t"), "kota": _kota().get("p"), "besleme_is": is_say, "beslenen_is": len(b), "jeton_is_ort": round(sum(x["jeton"] for x in b) / is_say, 1) if is_say else 0}


if __name__ == "__main__":
    if sys.stdout:  # pythonw (zamanlanmış görev): stdout yok
        sys.stdout.reconfigure(encoding="utf-8")
    else:
        sys.stdout = open(os.devnull, "w")
    kmt = sys.argv[1] if len(sys.argv) > 1 else ""
    if kmt == "kanca":
        try:
            kanca(json.load(sys.stdin))
        except Exception:
            pass  # kanca asla oturumu bozmaz
    elif kmt == "tur":
        print(calis())
    elif kmt == "derin":
        os.environ["BEYIN_DUSUN"] = "1"; print(derin())
    elif kmt == "ozet":  # CC SessionStart kancası: stdout oturum bağlamına girer
        print(bekci_yokla() + (OZET.read_text(encoding="utf-8") if OZET.exists() else ""))
    elif kmt == "geri":  # cc-kopru ajan aracı: görev stdin'den, blok stdout'a
        print(geri_oku(sys.stdin.read(), sys.argv[2] if len(sys.argv) > 2 else ""), end="")
    elif kmt == "kart":
        print(kart_metin() or "(kanıtlı içgörü yok)")
    elif kmt == "durum":
        print(json.dumps(durum(), ensure_ascii=False))
    else:
        print(__doc__)
