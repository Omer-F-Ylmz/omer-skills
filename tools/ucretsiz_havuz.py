"""UCRETSIZ-HAVUZ-1: bütün ücretsiz model kaynakları tek havuzda. OmniRoute yalnız bir halka; tek kapı değil.
Kullanım (kütüphane): cagir(tur, istem, aile=, haric_aile=, dogrula=, haiku_tavan=, etiket=) -> (metin|None, kaynak, log)
CLI: envanter | durum | tekrar | serve [port]   (serve: OpenAI uyumlu yerel uç, claude-mem mem-yedek için; ertelenen işleri de 30 sn'de bir dener)
Kurallar: 429/5xx/zaman aşımı → BEKLEME YOK, sıradaki sağlayıcı; düşen halka soğuma sonra tek deneme (ardışık hatada süre katlanır);
yük dağıtımı = kullanım/ağırlık en düşük sağlayıcı önce; son halka Haiku yalnız çağıranın haiku_tavan'ı kadar. Anahtar değeri hiçbir yere yazılmaz."""
import json, os, re, subprocess, sys, threading, time, urllib.error, urllib.request
from collections import namedtuple
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DIZIN = KOK / ".kos/kopru/ucretsiz"
DURUM = DIZIN / "durum.json"
NW = 0x08000000  # CREATE_NO_WINDOW
KILIT = threading.Lock()
sys.path.insert(0, str(Path(__file__).parent))

# sağlayıcı: (uç, anahtar kaynağı, ağırlık = yük payı). github anahtarı `gh auth token`, omni ucuz_alt.anahtar.
SAG = {"gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", "GEMINI_API_KEY", 3),
       "groq": ("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY", 2),
       "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY", 2),
       "github": ("https://models.github.ai/inference/chat/completions", "gh", 1.5),
       "omniroute": ("http://127.0.0.1:20128/v1/chat/completions", "omni", 0.5),
       # UCRETSIZ-HAVUZ-2: anahtar kullanıcı ortamında yoksa halka sessizce atlanır (bekliyor); {AD} uçtaki ortam değişkeniyle dolar
       "mistral": ("https://api.mistral.ai/v1/chat/completions", "MISTRAL_API_KEY", 1.5),
       "cloudflare": ("https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/v1/chat/completions", "CLOUDFLARE_API_KEY", 1),
       "nvidia": ("https://integrate.api.nvidia.com/v1/chat/completions", "NVIDIA_API_KEY", 1),
       "sambanova": ("https://api.sambanova.ai/v1/chat/completions", "SAMBANOVA_API_KEY", 0.5),
       "ollama": ("https://ollama.com/v1/chat/completions", "OLLAMA_API_KEY", 0.5)}
DUSUNME = {"gemini", "groq", "openrouter", "omniroute", "ollama"}  # reasoning_effort bilen uçlar; diğerleri bilinmeyen alanı 400/422 yapabilir
E = namedtuple("E", "prov model aile kova rpm tpm rpd baglam turler")
Z, H, Y, U = "ozet", "hakem", "yazim", "uzun"
# Sınırlar muhafazakâr belge/ölçüm değerleri (envanter.tsv); gerçek 429 gelirse soğuma devreye girer. baglam = jeton.
# kova: openrouter :free hesap başına ortak; diğerlerinde model başına.
ENT = [E("gemini", "gemini-3.1-flash-lite", "google", None, 10, 200_000, 200, 900_000, (Z, H, U)),
       E("gemini", "gemini-3.5-flash-lite", "google", None, 10, 200_000, 200, 900_000, (Z, H, U)),
       E("gemini", "gemini-3.6-flash", "google", None, 5, 200_000, 100, 900_000, (H, Y, U)),
       E("gemini", "gemini-3.8-flash", "google", None, 5, 200_000, 100, 900_000, (H, Y, U)),
       E("groq", "openai/gpt-oss-120b", "openai", None, 25, 7000, 800, 5500, (Z, H, Y)),
       E("groq", "openai/gpt-oss-20b", "openai", None, 25, 7000, 800, 5500, (Z, H, Y)),
       E("groq", "qwen/qwen3.8-27b", "alibaba", None, 25, 6000, 800, 4500, (Z, H, Y)),
       E("openrouter", "nvidia/nemotron-3-super-120b-a12b:free", "nvidia", "openrouter", 18, 10**6, 900, 200_000, (Z, H, Y, U)),
       E("openrouter", "google/gemma-4-31b-it:free", "google", "openrouter", 18, 10**6, 900, 100_000, (Z, H, Y)),
       E("openrouter", "minimax/minimax-m3.1-flash:free", "minimax", "openrouter", 18, 10**6, 900, 100_000, (Z, H, Y)),
       E("openrouter", "nvidia/nemotron-3-ultra-550b-a55b:free", "nvidia", "openrouter", 18, 10**6, 900, 100_000, (H, Y)),
       E("github", "openai/gpt-4.1-mini", "openai", None, 10, 7000, 120, 5500, ()),  # KAPALI: models.github.ai her yola 200 + gövde "OK" (20 Eki); düzelince türleri aç
       E("omniroute", "cc-ucuz-free", "karma", None, 15, 10**6, 100, 100_000, (Z, H, Y, U)),
       # 20 Eki canlı: mistral 429 (hız sınırı, kendini toparlarsa açılır) · cloudflare 200 · ollama "Free usage limit" 429; sınırlar acilabilir.md'deki belge değerlerinin muhafazakârı; ilk 429'da soğuma devreye girer
       E("mistral", "mistral-small-latest", "mistral", None, 30, 100_000, 1000, 100_000, (Z, H, Y, U)),
       E("mistral", "ministral-8b-latest", "mistral", None, 30, 100_000, 1000, 100_000, (Z, H, Y)),  # HAVUZ-3: mistral-small/medium 429 (1300), large 403 tier; ministral 200
       E("cloudflare", "@cf/meta/llama-3.3-70b-instruct-fp8-fast", "meta", None, 60, 20_000, 150, 20_000, (Z, H, Y)),
       E("nvidia", "openai/gpt-oss-20b", "openai", None, 30, 100_000, 1000, 100_000, (Z, H, Y)),  # HAVUZ-3: 200 (2 sn); llama-3.3 410, nemotron-nano 404, deepseek-v4.1-flash/gemma-4 zaman aşımı
       E("nvidia", "nvidia/nemotron-3-ultra-550b-a55b", "nvidia", None, 30, 100_000, 1000, 100_000, (H, Y)),  # ORDU d8: 200 (1 sn); nemotron-3-super-120b/nano-3-30b/llama-3.1-nemotron-ultra-253b listede ama 404, 3.5-lightning/3.5-super-vl 200 boş içerik (düşünme jetonu)
       E("nvidia", "nvidia/nemotron-3.5-lightning-30b-a3b", "nvidia", None, 30, 100_000, 1000, 100_000, (H, Y)),  # ORDU d9: 200 dolu içerik (max_tokens 8000; ~300 düşünme jetonu); max_tokens ≤1500 ile boş kalabilir
       E("nvidia", "google/gemma-4-31b-it", "google", None, 30, 100_000, 1000, 100_000, ()),  # KAPALI: llama-3.3 410, mistral-large/nemotron-70b 404, gemma/deepseek 60 sn zaman aşımı (20 Eki)
       E("sambanova", "gpt-oss-120b", "openai", None, 20, 20_000, 20, 60_000, ()),  # KAPALI: 402 PAYMENT_METHOD_REQUIRED (ücretsiz bakiye yok, 20 Eki); Llama-3.3 yoğunluktan 429
       E("ollama", "gpt-oss:120b", "openai", None, 6, 100_000, 100, 100_000, (Z, H, Y))]
ad = lambda e: f"{e.prov}/{e.model}"  # noqa: E731
ERT, SONUC = DIZIN / "ertelenen.jsonl", DIZIN / "ertelenen-sonuc.jsonl"
SERT = re.compile(r"free usage limit|per ?day|tokens per day|\btpd\b|daily|günlük", re.I)


class Hata(Exception):
    def __init__(self, kod, mesaj, bekle=None):
        super().__init__(f"{kod} {mesaj}"); self.kod, self.mesaj, self.bekle = kod, mesaj, bekle


_ANAHTAR = {}


def _anahtar(kaynak):
    if kaynak in _ANAHTAR:
        return _ANAHTAR[kaynak]
    v = None
    if kaynak == "gh":
        v = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, creationflags=NW).stdout.strip()
    elif kaynak == "omni":
        import ucuz_alt
        v = ucuz_alt.anahtar()
    else:
        v = os.environ.get(kaynak)
        if not v:
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                    v = winreg.QueryValueEx(k, kaynak)[0]
            except (ImportError, OSError):  # ImportError: Linux (Actions runner), anahtar yalnız ortam değişkeninden
                pass
    _ANAHTAR[kaynak] = v or None
    return _ANAHTAR[kaynak]


def _url(prov):
    """Uç adresi; {ORTAM_DEĞİŞKENİ} dolar, değişken yoksa None (halka atlanır)."""
    u = SAG[prov][0]
    for n in re.findall(r"\{(\w+)\}", u):
        if not _anahtar(n):
            return None
        u = u.replace("{" + n + "}", _anahtar(n))
    return u


def _gizle(s):
    for v in _ANAHTAR.values():
        if v and len(v) > 8:
            s = s.replace(v, "***")
    return s


def _omni_serbest():
    import ucuz_alt
    return ucuz_alt.ucretsiz("omni", ucuz_alt.COMBO)  # combo üyelerinin hepsi :free değilse ücretliye düşebilir


def _durum():
    try:
        return json.loads(DURUM.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _yaz(d):  # shortcut: süreçler arası kilit yok, son yazan kazanır (sayaç hafif eksik kalabilir); sık paralel süreçte dosya kilidi ekle
    DIZIN.mkdir(parents=True, exist_ok=True)
    t = DURUM.with_suffix(".tmp"); t.write_text(json.dumps(d), encoding="utf-8"); os.replace(t, DURUM)


def _oran(e, hata):
    """Aile başına [istek, boş/hatalı] sayacı (d10); _sec yalnız sıralamada kullanır, aileyi çıkarmaz."""
    with KILIT:
        d = _durum(); v = d.setdefault("oran", {}).setdefault(e.aile, [0, 0]); v[0] += 1; v[1] += bool(hata); _yaz(d)


def _hata_oranu(d, aile):
    n, h = d.get("oran", {}).get(aile, [0, 0])
    return round(h / n * 5) if n >= 5 else 0  # 5'ten az örnekte yok sayılır; 0.2'lik basamak, yük dengesi basamak içinde kalır


def _say(d, k, bugun):
    v = d.get("say", {}).get(k)
    return v[1] if v and v[0] == bugun else 0


def _sec(tur, tahmin, aile, haric, denenen, rezerv=None):
    """Uygun halkaların en az yüklüsünü seçer ve kotasını hemen rezerve eder (paralel iş parçacıkları aşmasın)."""
    with KILIT:
        d = _durum(); now = time.time(); bugun = time.strftime("%Y-%m-%d", time.gmtime())
        for k in ("say", "soguma", "dk", "son", "ardisik"):
            d.setdefault(k, {})
        uygun = []
        for e in ENT:
            if tur not in e.turler or ad(e) in denenen or tahmin > e.baglam or (aile and e.aile != aile) or e.aile == haric:
                continue
            if d["soguma"].get(ad(e), 0) > now or d["soguma"].get("p:" + e.prov, 0) > now:
                continue
            kova = e.kova or ad(e)
            dk = [x for x in d["dk"].get(kova, []) if x[0] > now - 60]; d["dk"][kova] = dk
            if len(dk) >= e.rpm or sum(x[1] for x in dk) + (rezerv or tahmin) > e.tpm or _say(d, kova, bugun) >= e.rpd:  # çıktı tavanı tam dolmaz: dakika kovası yarım max_tokens sayar
                continue
            if not _anahtar(SAG[e.prov][1]) or not _url(e.prov) or (e.prov == "omniroute" and not _omni_serbest()):
                continue
            uygun.append((_hata_oranu(d, e.aile), _say(d, "p:" + e.prov, bugun) / SAG[e.prov][2], _say(d, ad(e), bugun), d["son"].get(ad(e), 0), e))
        if not uygun:
            return None
        son = d.get("sec", [])[-20:]  # son 20 seçimde yarıyı aşan sağlayıcı, alternatif varken atlanır (kapı: hiçbir sağlayıcı >%50)
        if len({u[-1].prov for u in uygun}) > 1:
            uygun = [u for u in uygun if son.count(u[-1].prov) * 2 < len(son)] or uygun
        e = min(uygun, key=lambda x: x[:-1])[-1]
        d["sec"] = son + [e.prov]
        d["dk"][e.kova or ad(e)].append([now, rezerv or tahmin]); d["son"][ad(e)] = now
        for k in {ad(e), e.kova or ad(e), "p:" + e.prov}:
            d["say"][k] = [bugun, _say(d, k, bugun) + 1]
        _yaz(d)
        return e


def _dus(e, h):
    """Hataya göre soğuma; süre bitince halka bir kez denenir, yine düşerse süre katlanır."""
    with KILIT:
        d = _durum(); now = time.time()
        for k in ("soguma", "ardisik"):
            d.setdefault(k, {})
        n = d["ardisik"][ad(e)] = d["ardisik"].get(ad(e), 0) + 1
        if h.kod == 429:
            gunluk = SERT.search(h.mesaj) or (h.bekle or 0) > 900
            sure = 14400 if gunluk else min(h.bekle or 60, 900) * min(n, 4)  # OpenRouter "per-day" 429'u model başına geçici (20 Eki ölçüm): 4 saat değil
        elif h.kod in (401, 402, 403):
            d["soguma"]["p:" + e.prov] = now + 3600; _yaz(d); return  # anahtar/izin sorunu: sağlayıcının hepsi
        elif h.kod in (400, 404):
            sure = 3600
        elif h.kod == 413:
            sure = 600
        elif h.kod == 0:  # boş/kesik yanıt: yumuşak
            sure = 30
        else:
            sure = 120 * min(n, 4)
        d["soguma"][ad(e)] = now + sure; _yaz(d)


def _basari(e):
    with KILIT:
        d = _durum(); d.setdefault("ardisik", {})[ad(e)] = 0; _yaz(d)


def _istek(e, istem, max_tokens, zaman):
    url, kaynak = _url(e.prov), SAG[e.prov][1]
    g = {"model": e.model, "messages": [{"role": "user", "content": istem}], "max_tokens": max_tokens}
    if e.prov in DUSUNME and "gemma" not in e.model:
        g["reasoning_effort"] = "low"  # düşünme jetonu çıktıyı yemesin
    q = urllib.request.Request(url, json.dumps(g).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8",
                                                            "Authorization": "Bearer " + _anahtar(kaynak)})
    try:
        with urllib.request.urlopen(q, timeout=zaman) as f:
            j = json.load(f)
    except urllib.error.HTTPError as x:
        ra = x.headers.get("retry-after")
        raise Hata(x.code, _gizle(x.read()[:300].decode("utf-8", "replace")), int(ra) if ra and ra.isdigit() else None)
    if j.get("error"):  # "429 ama 200": gövdede hata
        er = j["error"] if isinstance(j["error"], dict) else {"message": j["error"]}
        raise Hata(er["code"] if isinstance(er.get("code"), int) else 502, _gizle(str(er)[:300]))
    try:
        c = j["choices"][0]; y = c["message"].get("content")
    except (KeyError, IndexError, TypeError, AttributeError):
        raise Hata(502, "choices yok")
    if not isinstance(y, str) or not y.strip():
        raise Hata(0, "boş yanıt")
    if c.get("finish_reason") == "length":
        raise Hata(0, "kesik yanıt")
    return y.strip()


def _haiku(istem):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    DIZIN.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--output-format", "json", "--max-turns", "1", "--tools", "",
                        "--setting-sources", ""], input=istem, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       timeout=150, creationflags=NW, cwd=DIZIN, env=env)
    j = json.loads(p.stdout)
    if j.get("is_error") or not (j.get("result") or "").strip():
        raise Hata(0, "haiku " + str(j.get("result"))[:80])
    if len(j["result"]) < 200 and re.search(r"(?i)usage limit|limit reached|resets? (at|in)", j["result"]):  # plan limiti düz metin gelir, yanıt sayılmasın
        raise Hata(429, "haiku plan limiti")
    return j["result"].strip()


def cagir(tur, istem, *, max_tokens=3000, aile=None, haric_aile=None, dogrula=None, haiku_tavan=0, etiket=None, zaman=90, ertele=None, zor=False, sablon=None):
    """(metin | None, 'saglayici/model', log). dogrula(metin) -> None | ret nedeni (ret → sıradaki halka, soğuma yok).
    ertele=<iş kimliği>: hiçbir halka (Haiku dahil) yanıtlamazsa iş ertelenen.jsonl'e yazılır, log'a 'ertelendi' düşer.
    AJAN-AKIS-1: iş-akışı çekirdeği (tools/ajan_cekirdek.md) HER çağrıda istemin başına eklenir; zor=True ayrıca zor-iş bölümünü ekler.
    sablon=<tür>: egitim-1 damıtma şablonu (tools/ogret/sarmal.py) + ornek-<tür>.md istemin başına eklenir."""
    ham = istem
    if sablon:
        from ogret.sarmal import onek
        istem = onek(sablon, zor) + istem
    else:
        import ajan_cekirdek
        import ders_dongu  # DERS-DONGU-1: çekirdekten sonra ≤5 ders (≤150 jeton); ders yok → ''
        istem = ajan_cekirdek.onek(zor) + ders_dongu.onek(ham) + istem
    tahmin, log, denenen = len(istem) // 3 + max_tokens, [], set()
    while (e := _sec(tur, tahmin, aile, haric_aile, denenen, len(istem) // 3 + max_tokens // 2)):
        denenen.add(ad(e))
        try:
            y = _istek(e, istem, max_tokens, zaman)
        except Hata as h:
            _dus(e, h); _oran(e, True); log.append(f"{ad(e)}:{h.kod}"); continue
        except (OSError, ValueError) as x:  # zaman aşımı, bağlantı, bozuk gövde
            _dus(e, Hata(599, type(x).__name__)); _oran(e, True); log.append(f"{ad(e)}:{type(x).__name__}"); continue
        neden = dogrula(y) if dogrula else None
        if neden:
            log.append(f"{ad(e)}:{neden}"); continue
        _basari(e); _oran(e, False)
        return y, ad(e), log
    if haiku_tavan > 0 and aile in (None, "anthropic") and haric_aile != "anthropic":
        with KILIT:  # sayaç etiket başına ve GÜNLÜK sıfırlanır (havuz-1: kalıcı sayaç ilk koşuda dolup sonra Haiku'yu hep kapattı)
            d = _durum(); k = etiket or tur; bugun = time.strftime("%Y-%m-%d", time.gmtime()); v = d.setdefault("haiku", {}).get(k); n = v[1] if isinstance(v, list) and v[0] == bugun else 0
            if n < haiku_tavan:
                d["haiku"][k] = [bugun, n + 1]; _yaz(d)
            else:
                n = None
        if n is not None:
            try:
                y = _haiku(istem)
                neden = dogrula(y) if dogrula else None
                if not neden:
                    return y, "haiku/claude-haiku-5-5", log
                log.append(f"haiku:{neden}")
            except (Hata, OSError, ValueError, subprocess.SubprocessError) as x:
                log.append(f"haiku:{type(x).__name__}")
    if ertele:
        _ertele(ertele, dict(tur=tur, istem=ham, max_tokens=max_tokens, aile=aile, haric_aile=haric_aile, haiku_tavan=haiku_tavan, etiket=etiket, zaman=zaman, zor=zor))
        log.append("ertelendi")
    return None, None, log


def _ertele(ad, is_):
    """Sonuçsuz iş hata değil: ertelenen.jsonl'e yazılır, en yakın soğuma bitiminde tekrar() dener."""
    now = time.time(); t = [v for v in _durum().get("soguma", {}).values() if v > now]
    DIZIN.mkdir(parents=True, exist_ok=True)
    with KILIT, ERT.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"id": ad, "hazir": min(t) if t else now + 60, **is_}, ensure_ascii=False) + "\n")


def tekrar():
    """Zamanı gelen ertelenen işleri dener → ertelenen-sonuc.jsonl; olmayanlar yeni zamanla kuyrukta kalır. (biten, kalan)
    shortcut: dogrula (çağrı fonksiyonu) kuyruğa yazılamaz, tekrar doğrulamasız; sonucu tüketen kendi doğrulamasını yapar."""
    ara = ERT.with_suffix(".isleniyor")
    try:
        os.replace(ERT, ara)  # atomik devral: bu sırada gelen yeni satırlar yeni ERT'ye yazılır
    except OSError:
        return 0, 0
    biten, kalan = 0, []
    for s in ara.read_text(encoding="utf-8").splitlines():
        if not s.strip():
            continue
        i = json.loads(s)
        if i["hazir"] <= time.time() and not i["id"].startswith("makara:"):  # makara kayıtlarını gece betiği alır
            y, k, _ = cagir(i["tur"], i["istem"], **{a: i[a] for a in ("max_tokens", "aile", "haric_aile", "haiku_tavan", "etiket", "zaman")})
            if y:
                with SONUC.open("a", encoding="utf-8") as f:
                    f.write(json.dumps({"id": i["id"], "metin": y, "kaynak": k}, ensure_ascii=False) + "\n")
                biten += 1; continue
            i["hazir"] = min([v for v in _durum().get("soguma", {}).values() if v > time.time()] or [time.time() + 60])
        kalan.append(i)
    ara.unlink()
    if kalan:
        with ERT.open("a", encoding="utf-8") as f:
            f.write("".join(json.dumps(i, ensure_ascii=False) + "\n" for i in kalan))
    return biten, len(kalan)


def iki_aile(tur, istem, **kw):
    """Hakem: iki ayrı aileden birer yanıt [(metin, kaynak, aile)]; ikinci aile ilkinden farklı olmak zorunda."""
    a, k1, _ = cagir(tur, istem, **kw)
    if a is None:
        return []
    f1 = next((e.aile for e in ENT if ad(e) == k1), "anthropic")
    b, k2, _ = cagir(tur, istem, **{**kw, "haric_aile": f1})
    return [(a, k1, f1)] + ([(b, k2, next((e.aile for e in ENT if ad(e) == k2), "anthropic"))] if b else [])


def envanter():
    """Her halka için 1 canlı Türkçe çağrı + model listesi sayısı → envanter.tsv (anahtar değeri yok)."""
    satir = ["saglayici\tmodel\taile\tanahtar\thttp\tgecikme_sn\tmodel_sayisi\trpm\ttpm\trpd\tturkce\tnot"]
    sayi = {}
    for p, (_, kaynak, _) in SAG.items():
        a, url = _anahtar(kaynak), _url(p)
        try:
            if not a or not url:
                raise Hata(-1, "anahtar yok")
            r = urllib.request.Request(url.rsplit("/chat/completions", 1)[0] + "/models", headers={"Authorization": "Bearer " + a, "User-Agent": "curl/8"})
            sayi[p] = len(json.load(urllib.request.urlopen(r, timeout=30)).get("data", []))
        except Exception as x:
            sayi[p] = f"liste:{type(x).__name__}"
    for e in ENT:
        t0 = time.time(); kod, tr, nt = 200, "-", ""
        try:
            if not _anahtar(SAG[e.prov][1]) or not _url(e.prov):
                raise Hata(-1, "anahtar yok")
            y = _istek(e, "Türkiye'nin başkenti neresidir? Tek cümleyle, Türkçe karakterlerle (ş, ğ, ı) yanıtla.", 400, 60)
            tr = "iyi" if "Ankara" in y and re.search(r"[şğıçöü]", y) else "zayıf"; nt = y[:60].replace("\t", " ").replace("\n", " ")
        except Hata as h:
            kod, nt = h.kod, h.mesaj[:80].replace("\t", " ").replace("\n", " ")
        except (OSError, ValueError) as x:
            kod, nt = 599, type(x).__name__
        satir.append("\t".join(map(str, [e.prov, e.model, e.aile, "var" if _anahtar(SAG[e.prov][1]) else "yok", kod, round(time.time() - t0, 1),
                                         sayi[e.prov], e.rpm, e.tpm, e.rpd, tr, nt])))
    DIZIN.mkdir(parents=True, exist_ok=True)
    (DIZIN / "envanter.tsv").write_text("\n".join(satir) + "\n", encoding="utf-8")
    print("\n".join(satir))


def serve(port):
    """OpenAI uyumlu yerel uç: claude-mem openai-compatible yedeği buraya bağlanır (model adı yok sayılır, tür ozet)."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Is(BaseHTTPRequestHandler):
        def do_POST(self):
            g = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))) or b"{}")
            istem = "\n\n".join(m["content"] if isinstance(m["content"], str) else str(m["content"]) for m in g.get("messages", []))
            y, k, log = cagir("ozet", istem, max_tokens=min(int(g.get("max_tokens") or 3000), 4000), haiku_tavan=0, etiket="serve")
            kod, govde = (200, {"object": "chat.completion", "model": k, "choices": [{"index": 0, "finish_reason": "stop",
                                                                                        "message": {"role": "assistant", "content": y}}]}) if y else (
                503, {"error": {"message": "havuz boş: " + ",".join(log)[:300], "code": 503}})
            b = json.dumps(govde).encode()
            self.send_response(kod); self.send_header("content-type", "application/json"); self.send_header("content-length", str(len(b)))
            self.end_headers(); self.wfile.write(b)

        def log_message(self, *a):
            pass
    def dongu():  # ertelenen işleri soğuma bitince yeniden dene
        while True:
            time.sleep(30)
            try:
                tekrar()
            except Exception:
                pass
    threading.Thread(target=dongu, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", port), Is).serve_forever()


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "durum"
    if c == "envanter":
        envanter()
    elif c == "tekrar":
        print(tekrar())
    elif c == "serve":
        serve(int(sys.argv[2]) if len(sys.argv) > 2 else 20190)
    else:
        print(json.dumps({k: v for k, v in _durum().items() if k in ("say", "soguma", "haiku")}, indent=1))
