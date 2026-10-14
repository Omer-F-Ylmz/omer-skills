"""VİDEO-KISA-TOKEN-1: kısa video (reel · short · carousel) hattı — Gemini izler, katalog önbelleği eler, Claude yalnız JSON okur.

izle: video + paket.md → ücretsiz Gemini → <cache>/<id>/gemini.json (şema SEMA). Claude bu adımda yok.
katalog: araç adı → kurulu sözlük (tarama.sozluk_kur) ya da ig-41 karar-birlesik.tsv; bilinen araç yalnız fark notu alır.
arastir: bilinmeyen GitHub reposu → gh api künye + README özeti (tools/ucuz_alt.py, Claude-dışı); repo başına önbellek.
oturum: ≥8 videonun gemini.json'u tek claude -p çağrısında (hafif.cagir, efor low) → kısa rapor (araç başı ≤4 satır).
"""
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import hafif
from . import tarama as tr

API = "https://generativelanguage.googleapis.com"
MODELLER = ("gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite")  # ücretsiz katman; ilki 429/404/5xx/zaman aşımı verirse sıradaki (14 Eki: iki flash birden 503, lite ayakta)
VIDEO_PARALEL = 4  # ücretsiz katman dakika sınırı: video başı 2 Gemini çağrısı
IZLE_ZAMAN = 90  # generateContent sn; asılı yanıtta sıradaki modele geç
IZLE_TUR, IZLE_BEKLE = 4, 30  # tüm modeller düşerse tur arası 30·tur sn
KOK = Path(__file__).resolve().parents[3]
KARAR = KOK / "docs" / "kurulumlar" / "ig-41" / "karar-birlesik.tsv"
ARASTIRMA = KOK / ".kos" / "kopru" / "video" / "kisa" / "arastirma"
PAKET_TAVAN = 12_000  # paket.md karakteri (Gemini'ye bağlam; ücretsiz)
SEMA = {"type": "OBJECT", "required": ["konusma_ozet", "ekran_metni", "araclar", "adlar", "teknikler", "linkler", "komutlar", "iddialar"], "properties": {
    "adlar": {"type": "ARRAY", "items": {"type": "STRING"}},
    "teknikler": {"type": "ARRAY", "items": {"type": "STRING"}},
    "konusma_ozet": {"type": "STRING"},
    "ekran_metni": {"type": "ARRAY", "items": {"type": "STRING"}},
    "araclar": {"type": "ARRAY", "items": {"type": "OBJECT", "required": ["ad", "ne_dedi", "zaman"], "properties": {
        "ad": {"type": "STRING"}, "ne_dedi": {"type": "STRING"}, "zaman": {"type": "STRING"}}}},
    "linkler": {"type": "ARRAY", "items": {"type": "STRING"}},
    "komutlar": {"type": "ARRAY", "items": {"type": "STRING"}},
    "iddialar": {"type": "ARRAY", "items": {"type": "STRING"}}}}
ISTEM = ("Bu kısa videoyu (ya da carousel slaytlarını) baştan sona izle; konuşmayı VE ekrandaki her yazıyı oku. Ekte paket.md var: açıklama, "
         "açıklama/yorum bağlantıları, otomatik transkript ve OCR; paket.md'yi baştan sona tara, orada geçen araçlar da listeye girer (yazımı oradan al, "
         "eksiklerini videodan tamamla). Türkçe yaz.\n"
         "- araclar: anılan ya da ekranda görünen HER araç, repo, kütüphane, model, skill, MCP, CLI, servis, site; adı ekrandaki yazımıyla "
         "(owner/repo görünüyorsa öyle). ne_dedi: videonun onun hakkında söylediği/gösterdiği (≤25 kelime). zaman: m:ss ya da 'açıklama'/'yorum'. "
         "Altyapıyı da ayrı satır yaz: dil (Python), paket yöneticisi (pip, npm, uv), platform (GitHub, Hugging Face), çerçeve (PyTorch, Transformers), "
         "lisans (Apache-2.0); anılan her model sürümünü ayrı (ör. Qwen3.5-0.8B, Llama). "
         "Eksik yazmaktansa fazla yaz, ama yalnız videoda/pakette gerçekten geçeni.\n"
         "- adlar: paket.md'de ve ekranda geçen HER özel adın tam listesi (araç, repo, model ve sürümü, kütüphane, platform, paket yöneticisi, lisans, "
         "adlandırılmış teknik); satır satır tara, tekrarsız.\n"
         "- teknikler: videonun anlattığı ya da adını koyduğu yöntem/teknikler (1–4 adet, 2–5 kelimelik Türkçe ad; ör. 'kuantizasyonla küçültme').\n"
         "- linkler: ekranda, konuşmada, açıklamada ya da yorumlarda geçen her URL/alan adı/GitHub yolu (aynen).\n"
         "- komutlar: ekranda görünen kurulum/terminal komutları aynen. ekran_metni: ekrandaki anlamlı yazılar (başlık, kod, istem) kısa.\n"
         "- iddialar: sayısal/karşılaştırmalı/özellik iddiaları, zamanıyla. Uydurma; göremediğini yazma.")


def anahtar(env=None):
    from .cli import _kullanici_env  # HKCU yedeği; değer basılmaz
    env = dict(os.environ if env is None else env)
    _kullanici_env(env)
    if not env.get("GEMINI_API_KEY"):
        raise SystemExit("kisa: GEMINI_API_KEY yok")
    return env["GEMINI_API_KEY"]


def _iste(url, key, govde=None, bas=None, ham=False, zaman=300):
    """Anahtar başlıkta (URL'de değil → hata metnine sızmaz)."""
    veri = govde if isinstance(govde, (bytes, type(None))) else json.dumps(govde).encode()
    r = urllib.request.Request(url, data=veri, headers={"x-goog-api-key": key, **({} if ham else {"Content-Type": "application/json"}), **(bas or {})})
    with urllib.request.urlopen(r, timeout=zaman) as y:
        return y if ham else json.load(y)


def yukle(yol, key):
    """Files API (resumable) → {fileData}; ACTIVE olana dek bekler (≤120 sn)."""
    yol, mime = Path(yol), mimetypes.guess_type(str(yol))[0] or "video/mp4"
    r = urllib.request.Request(f"{API}/upload/v1beta/files", data=json.dumps({"file": {"display_name": yol.name}}).encode(), headers={
        "x-goog-api-key": key, "Content-Type": "application/json", "X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start",
        "X-Goog-Upload-Header-Content-Length": str(yol.stat().st_size), "X-Goog-Upload-Header-Content-Type": mime})
    with urllib.request.urlopen(r, timeout=60) as y:
        hedef = y.headers["X-Goog-Upload-URL"]
    f = _iste(hedef, key, yol.read_bytes(), {"X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"})["file"]
    for _ in range(60):
        if f.get("state") != "PROCESSING":
            break
        time.sleep(2)
        f = _iste(f"{API}/v1beta/{f['name']}", key)
    if f.get("state") != "ACTIVE":
        raise RuntimeError(f"gemini dosya durumu {f.get('state')}")
    return {"fileData": {"fileUri": f["uri"], "mimeType": mime}}


def parcalar(d, medya, key):
    """Gemini girdisi: YouTube URL doğrudan · reel mp4 Files API · carousel görselleri satır içi + slayt videoları + paket.md (OCR dahil)."""
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    p = []
    if not d.name.startswith("ig-"):
        p.append({"fileData": {"fileUri": f"https://www.youtube.com/watch?v={d.name}"}})
    else:
        for ad in ["goz-video.mp4", *(meta.get("slayt_video") or [])]:
            if (medya / ad).is_file():
                p.append({**yukle(medya / ad, key), "videoMetadata": {"fps": 0.5}})
        gorsel = [medya / ad for ad in meta.get("gorseller") or [] if (medya / ad).is_file()]
        if not p and not gorsel:  # embed video vermediyse önbellek kareleri ekranın yerini tutar (video elenmez)
            gorsel = sorted((d / "kareler").glob("*.jpg"))[:12]
        for y in gorsel:
            p.append({"inlineData": {"mimeType": "image/jpeg", "data": __import__("base64").b64encode(y.read_bytes()).decode()}})
    paket = (d / "paket.md").read_text(encoding="utf-8")[:PAKET_TAVAN] if (d / "paket.md").is_file() else meta.get("description") or ""
    return p + [{"text": f"paket.md:\n{paket}\n\n{ISTEM}"}]


def izle(d, medya=None, env=None, yeniden=False):
    """→ (gemini.json içeriği, {model, sure, jeton}); önbellekte varsa çağrı yok."""
    d = Path(d)
    hedef = d / "gemini.json"
    if hedef.is_file() and not yeniden:
        return json.loads(hedef.read_text(encoding="utf-8")), {"onbellek": True}
    key, t = anahtar(env), time.monotonic()
    govde = {"contents": [{"parts": parcalar(d, Path(medya or d), key)}],
             "generationConfig": {"responseMimeType": "application/json", "responseSchema": SEMA, "temperature": 0.2,
                                  "mediaResolution": "MEDIA_RESOLUTION_LOW"}}  # ekran yazısı paket.md OCR'ında; düşük çözünürlük izlemeyi kısaltır
    j, iz = _uret(govde, key, t)
    var = {a["ad"].casefold() for a in j["araclar"]}  # lite araclar'da adları atlıyor; ayrı tam liste alanı yakalamayı artırır
    ek = [(a, "(yalnız adı geçiyor)") for a in j.pop("adlar", [])] + [(a, "(teknik)") for a in j.pop("teknikler", [])]
    ek += [(k, "(kurulum komutu)") for k in j.get("komutlar", []) if KURULUM.match(k)]
    for a, ne in ek:
        if a.casefold() not in var and not KOD.search(a):
            var.add(a.casefold())
            j["araclar"].append({"ad": a, "ne_dedi": ne, "zaman": "paket"})
    hedef.write_text(json.dumps({**j, "_iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
    return j, iz


KOD = re.compile(r"[<>{}=;]")  # kod parçası ad değil
KURULUM = re.compile(r"\s*(pip3?|pipx|uv|npm|pnpm|yarn|bun|brew|cargo|go|gem|winget)\s.*\b(install|add)\b")
METIN_ISTEM = ("Aşağıda bir kısa videonun paketi var (başlık, açıklama, konuşma metni, ekran OCR'ı, linkler). Videoda adı geçen TÜM araç, repo, uygulama, "
               "servis, model (sürümüyle), kütüphane, paket yöneticisi (pip, npm, uv…), programlama dili, platform ve lisans adlarını çıkar; yalnız bir kez "
               "ya da yalnız ekranda geçenler dahil. OCR bozuk yazımlarını tek doğru ada indir. Genel terimleri (API, JSON, HTTP, CSS), slash komutlarını, "
               "kişi adlarını, arayüz düğme/menü yazılarını ve sıradan kelimeleri alma. ADAYLAR katalogdan gelir ve pakette geçer: yalnız videoda gerçekten "
               "araç/ürün adı olarak kullanılanları al.")


def metin_gec(d, env=None, yeniden=False):
    """İkinci, yalnız-metin Gemini geçişi (recall): paket.md + katalog sözlüğü adayları → {adlar}; önbellek gemini-metin.json. Video izlemeye paralel koşabilir."""
    d = Path(d)
    hedef = d / "gemini-metin.json"
    if hedef.is_file() and not yeniden:
        return json.loads(hedef.read_text(encoding="utf-8"))
    key, t = anahtar(env), time.monotonic()
    aday = [a["ad"] for a in sozluk_tara(d, {})]
    metin = (d / "paket.md").read_text(encoding="utf-8")[:PAKET_TAVAN * 2]
    govde = {"contents": [{"parts": [{"text": f"{METIN_ISTEM}\n\nADAYLAR: {', '.join(aday) or 'yok'}\n\n{metin}"}]}],
             "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1,
                                  "responseSchema": {"type": "OBJECT", "required": ["adlar"], "properties": {"adlar": {"type": "ARRAY", "items": {"type": "STRING"}}}}}}
    j, iz = _uret(govde, key, t)
    j = {"adlar": [a for a in dict.fromkeys(j["adlar"]) if a.strip() and not KOD.search(a)], "aday": len(aday), "_iz": iz}
    hedef.write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    return j


def birlestir(g, m):
    """Metin geçişinin adlarını Gemini araçlarına tekrarsız ekler (yerinde)."""
    g["araclar"] = [a for a in g["araclar"] if not KOD.search(a["ad"])]  # eski önbellekteki kod parçaları da (DeV9 <script src=…>)
    var = {tr.normal(a["ad"]) for a in g["araclar"]}
    for a in m.get("adlar", []):
        if tr.normal(a) not in var:
            var.add(tr.normal(a))
            g["araclar"].append({"ad": a, "ne_dedi": "(metin geçişi: pakette adı geçiyor)", "zaman": "paket"})
    return g


def _uret(govde, key, t):
    """MODELLER sırasıyla generateContent → (JSON, iz)."""
    son = []
    for tur in range(IZLE_TUR):  # iki model birden 503 "high demand" verebiliyor (14 Eki) → bekle, baştan dene
        if tur:
            time.sleep(IZLE_BEKLE * tur)
        for m in MODELLER:
            try:
                y = _iste(f"{API}/v1beta/models/{m}:generateContent", key, govde, zaman=IZLE_ZAMAN)
                j = json.loads(y["candidates"][0]["content"]["parts"][0]["text"])
                return j, {"model": m, "sure": round(time.monotonic() - t, 1), "jeton": (y.get("usageMetadata") or {}).get("totalTokenCount")}
            except urllib.error.HTTPError as e:
                son.append(f"{m}: HTTP {e.code} {e.read()[:200]!r}")
                if e.code not in (404, 429, 500, 503):
                    raise RuntimeError(f"gemini: {' | '.join(son)}")
            except (TimeoutError, urllib.error.URLError) as e:
                son.append(f"{m}: bağlantı/zaman aşımı ({type(e).__name__})")
            except (KeyError, IndexError, ValueError) as e:
                son.append(f"{m}: yanıt ayrıştırılamadı ({type(e).__name__})")
    raise RuntimeError(f"gemini: {' | '.join(son)}")


def _kararlar():
    if not KARAR.is_file():
        return {}
    satir = [s.split("\t") for s in KARAR.read_text(encoding="utf-8").splitlines()]
    bas = satir[0]
    return {tr.normal(s[bas.index("kalem")]): f"{s[bas.index('karar')]} (ig-41)" for s in satir[1:] if len(s) == len(bas)}


def katalog(adlar, ev=None, kok=None, vid=""):
    """{ad: 'kurulu:<kaynak>' | '<karar> (ig-41)' | 'atlas:<kaynak>' | None}; None = bilinmeyen → tam araştırma.
    ATLAS envanterinde videonun kendi raporundan gelen satır sayılmaz."""
    sozluk, karar = tr.sozluk_kur(Path(ev or Path.home()), []), _kararlar()
    atlas = _tarama(kok)["ad"] if kok else {}
    out = {}
    for a in adlar:
        k = karar.get(tr.normal(a))
        e = None if k else tr.eslestir(a, sozluk)
        x = atlas.get(" ".join(_sozcuk(a)), [a, []])[1]
        x = [y for y in x if not (vid and vid[3:] in y)]
        out[a] = k or (f"kurulu:{e[1]}" if e else (f"atlas:{x[0]}" if x else None))
    return out


ENVANTER = KOK / ".claude" / "atlas" / "envanter.jsonl"
DF_TAVAN = 0.2  # ad, paketlerin bu oranından fazlasında geçiyorsa genel kelime (agent %48, claude %72); ≤%1 denemesinde lite aday dışı adları da (pip, npm, Llama) bıraktı
_sozcuk = lambda s: re.findall(r"[a-z0-9]+", s.casefold())


def _ngram(s):
    t = _sozcuk(s)
    return {" ".join(t[i:i + n]) for n in (1, 2, 3) for i in range(len(t) - n + 1)}


_TARAMA = {}


def _tarama(kok):
    """{ngram: [envanter adı, kaynak]} + belge sıklığı; süreç başına bir kez (1.9k paket.md ~birkaç sn)."""
    if "ad" not in _TARAMA:
        ad = {}
        if ENVANTER.is_file():
            for s in ENVANTER.read_text(encoding="utf-8").splitlines():
                j = json.loads(s)
                k = " ".join(_sozcuk(j.get("ad", "")))
                if k and k.count(" ") < 3 and (" " in k or len(k) >= 3) and not k.isdigit():
                    ad.setdefault(k, [j["ad"], []])[1].append(j.get("kaynak", ""))
        df = {}
        paketler = list(Path(kok).glob("*/paket.md"))
        for p in paketler:
            for g in _ngram(p.read_text(encoding="utf-8", errors="ignore")) & ad.keys():
                df[g] = df.get(g, 0) + 1
        _TARAMA.update(ad=ad, df=df, n=max(len(paketler), 1))
    return _TARAMA


def sozluk_tara(d, g):
    """Claude'suz recall: paket.md (konuşma+OCR+açıklama+linkler) içinde ATLAS envanterinin bildiği adlar → Gemini'nin atladıkları.
    Videonun kendi raporundan gelen envanter satırı sayılmaz (sızıntı); genel kelimeler belge sıklığıyla elenir."""
    p, vid = Path(d) / "paket.md", Path(d).name
    t = _tarama(Path(d).parent)
    if not p.is_file():
        return []
    var = {tr.normal(a["ad"]) for a in g.get("araclar", [])}
    out = []
    for k in sorted(_ngram(p.read_text(encoding="utf-8", errors="ignore")) & t["ad"].keys()):
        ad, kaynak = t["ad"][k]
        if all(vid[3:] in x for x in kaynak) or t["df"].get(k, 0) / t["n"] > DF_TAVAN or tr.normal(ad) in var:
            continue
        var.add(tr.normal(ad))
        out.append({"ad": ad, "ne_dedi": "(katalog sözlüğü: pakette adı geçiyor)", "zaman": "paket"})
    return out


def arastir(repo):
    """owner/repo → kısa künye (lisans · yıldız · son push · açıklama · README özeti). Claude yok; önbellek ARASTIRMA/<o_r>.json."""
    ARASTIRMA.mkdir(parents=True, exist_ok=True)
    yol = ARASTIRMA / (repo.replace("/", "_") + ".json")
    if yol.is_file():
        return json.loads(yol.read_text(encoding="utf-8"))
    def gh(*a):
        r = subprocess.run(["gh", "api", *a], capture_output=True, text=True, encoding="utf-8", timeout=60)
        return r.stdout if r.returncode == 0 else ""
    j = json.loads(gh(f"repos/{repo}") or "{}")
    k = {"repo": repo, "lisans": ((j.get("license") or {}).get("spdx_id")) or "yok", "yildiz": j.get("stargazers_count"),
         "push": (j.get("pushed_at") or "")[:10], "aciklama": j.get("description") or ""}
    readme = gh(f"repos/{repo}/readme", "-H", "Accept: application/vnd.github.raw")[:20_000]
    if readme:
        ham, ozet = ARASTIRMA / (yol.stem + "-readme.md"), ARASTIRMA / (yol.stem + "-ozet.md")
        ham.write_text(readme, encoding="utf-8")
        subprocess.run([sys.executable, str(KOK / "tools" / "ucuz_alt.py"), "README'yi 3 satırda özetle: ne yapar, nasıl kurulur, ne ister (anahtar/hesap/ağ).",
                        str(ozet), str(ham)], capture_output=True, timeout=400)
        k["readme"] = ozet.read_text(encoding="utf-8").strip()[:600] if ozet.is_file() else ""
    yol.write_text(json.dumps(k, ensure_ascii=False), encoding="utf-8")
    return k


def repo_bul(ad, metinler):
    """Araç → owner/repo: önce Gemini metnindeki github linki, yoksa gh arama ilk sonucu (doğrulanmamış; Claude karar verir)."""
    for u in metinler:
        m = re.search(r"github\.com/([\w.-]+/[\w.-]+)", u)
        if m and tr.normal(ad.split("/")[-1]) in tr.normal(m.group(1)):
            return m.group(1).removesuffix(".git"), "link"
    for _ in range(4):  # arama 30/dk; araç patlamasında (DeHMM 25) sessiz kayıp yerine sıfırlanmayı bekle
        r = subprocess.run(["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={ad} in:name", "-f", "per_page=1", "--jq", ".items[0].full_name"],
                           capture_output=True, text=True, encoding="utf-8", timeout=60)
        if r.returncode == 0 or "rate limit" not in (r.stderr or "").lower():
            break
        time.sleep(20)
    return (r.stdout.strip(), "gh arama, doğrulanmadı") if r.returncode == 0 and r.stdout.strip() else (None, None)


OTURUM_SISTEM = ("Kısa video değerlendiricisisin. Her VIDEO bloğu Gemini'nin videoyu izleyip çıkardığı JSON'dur (konuşma + ekran + açıklama/yorum linkleri) "
                 "ve her aracın katalog durumudur. Hiçbir video ve hiçbir araç elenmez. Her araç için: tur (skill·plugin·MCP·CLI·kütüphane·uygulama·servis·model·teknik·ipucu), "
                 "link (JSON'da varsa, yoksa boş), not ≤2 kısa cümle. Katalog 'kurulu'/'karar' diyorsa not yalnız FARK (yeni sürüm/özellik/iddia) ya da 'fark yok'; "
                 "'bilinmeyen' ise not = ne işe yarar + bizde ne işe yarar, arastirma künyesi varsa lisans/hesap şartını ekle. "
                 "ne_dedi '(metin geçişi…)' / '(yalnız adı geçiyor)' olan adlardan araç/ürün/model/dil/platform/lisans adı OLMAYANLARI (arayüz düğme/menü yazısı, "
                 "sıradan kelime, kişi adı, OCR bozuğu) yazma; gerçek araçların hepsi kalır. "
                 "linkler: videonun tüm linkleri aynen. Uydurma ekleme, JSON'da olmayan aracı yazma.")
OTURUM_SEMA = {"type": "object", "required": ["videolar"], "properties": {"videolar": {"type": "array", "items": {
    "type": "object", "required": ["id", "ozet", "araclar", "linkler"], "properties": {
        "id": {"type": "string"}, "ozet": {"type": "string"}, "linkler": {"type": "array", "items": {"type": "string"}},
        "araclar": {"type": "array", "items": {"type": "object", "required": ["ad", "tur", "link", "not"], "properties": {
            "ad": {"type": "string"}, "tur": {"type": "string"}, "link": {"type": "string"}, "not": {"type": "string"}}}}}}}}}


def blok(vid, g, kat, kunye):
    """Claude'a giden tek video bloğu: ham paket değil, Gemini JSON'u (ekran_metni kısaltılmış) + katalog + araştırma künyesi."""
    g = {k: v for k, v in g.items() if k != "_iz"}
    g["ekran_metni"] = [s[:160] for s in g.get("ekran_metni", [])[:12]]
    g["araclar"] = [{**a, "katalog": kat.get(a["ad"]) or "bilinmeyen", **({"arastirma": kunye[a["ad"]]} if a["ad"] in kunye else {})}
                    for a in g.get("araclar", [])]
    return f"VIDEO {vid}\n{json.dumps(g, ensure_ascii=False, separators=(',', ':'))}"


def oturum(bloklar, efor="low", env=None):
    """Tek claude -p (≥8 video önerilir; sabit sistem metni önbellekte) → hafif.cagir sonucu."""
    return hafif.cagir(OTURUM_SISTEM, "\n\n".join(bloklar), OTURUM_SEMA, efor=efor, env=env, butce=1.0)


def link_tamamla(x, kunye_link):
    """Linksiz araca karar dosyasındaki (ig-41, doğrulanmış) ya da videonun kendi linkinden bulunan repo adresi; Claude'suz.
    14 Eki d6: Laya 'KUR' bilinen sayıldığı için araştırılmadı → repo linki rapora hiç girmedi."""
    kl = {}
    if KARAR.is_file():
        satir = [s.split("\t") for s in KARAR.read_text(encoding="utf-8").splitlines()]
        bas = satir[0]
        kl = {tr.normal(s[bas.index("kalem")]): s[bas.index("link")] for s in satir[1:] if len(s) == len(bas) and s[bas.index("link")].startswith("http")}
    for a in x["araclar"]:
        if not a["link"]:
            a["link"] = kl.get(tr.normal(a["ad"])) or kunye_link.get(a["ad"], "")
    x["linkler"] = list(dict.fromkeys(x["linkler"] + [a["link"] for a in x["araclar"] if a["link"]]))


def paket_linkleri(d):
    """Açıklama/yorum linkleri paket.md'den regex'le (14 Eki: Gemini 21 linkten 3'ünü döndürdü; Claude'a kopyalatmak jeton yer)."""
    p = d / "paket.md"
    if not p.is_file():
        return []
    s = p.read_text(encoding="utf-8")
    gh = [f"https://github.com/{o}/{r}" for o, r in dict.fromkeys(GH_BASLIK.findall(s)) if _repo_var(f"{o}/{r}")][:8]
    return list(dict.fromkeys([x["url"] for x in tr.link_topla({"paket": s})] + gh))


GH_BASLIK = re.compile(r"^\[[\d:]+\]\s*([A-Za-z0-9][\w-]{0,38})(?:\s+/\s*|\s*/\s+)([\w.-]{2,100})\s*$", re.M)  # OCR'da GitHub repo başlığı "sahip / repo"


def _repo_var(r):
    """gh api ile repo gerçekten var mı (OCR tahmini doğrulanmadan link yazılmaz)."""
    y = subprocess.run(["gh", "api", f"repos/{r}", "--jq", ".full_name"], capture_output=True, text=True, encoding="utf-8", timeout=30)
    return y.returncode == 0 and y.stdout.strip().lower() == r.lower()


def calistir(ids, kok, cikti, efor="low", env=None):
    """Uçtan uca: her id için IG medyası (cikti/medya/<id>, hat indirir) → izle → katalog → bilinmeyene arastir → tek oturum → cikti/<id>.md.
    kok/<id>/meta.json (+ paket.md) önceden `video paket` ile hazır olmalı. → (iz, oturum sonucu)."""
    from . import instagram
    kok, cikti = Path(kok), Path(cikti)
    iz, bloklar, paket_link, kunye_link = {}, {}, {}, {}

    def isle(v, m, indir):
        with ThreadPoolExecutor(2) as ex:  # metin geçişi video izlemeyi beklemez
            fg, fm = ex.submit(izle, kok / v, m, env), ex.submit(metin_gec, kok / v, env)
            (g, gi), mg = fg.result(), fm.result()
        birlestir(g, mg)
        paket_link[v] = paket_linkleri(kok / v)
        kat = katalog([a["ad"] for a in g["araclar"]], kok=kok, vid=v)
        def kun(a):
            r, nasil = repo_bul(a["ad"], g["linkler"] + paket_link[v] + [a["ne_dedi"]])
            return a["ad"], ({**arastir(r), "bulunus": nasil} if r else None)
        t = time.monotonic()
        with ThreadPoolExecutor(6) as ex:  # gh + README özeti ağ bekler; seri DeHMM 30 araçta 43 sn
            kunye = {ad: k for ad, k in ex.map(kun, [a for a in g["araclar"] if not kat[a["ad"]]]) if k}
        kunye_link[v] = {ad: f"https://github.com/{k['repo']}" for ad, k in kunye.items() if k["bulunus"] == "link"}  # gh arama ilk sonucu doğrulanmadı → link yazılmaz
        iz[v] = {"indir": indir, "gemini": gi, "metin": mg["_iz"], "arastir": round(time.monotonic() - t, 1), "arac": len(kat), "bilinen": sum(1 for x in kat.values() if x)}
        bloklar[v] = blok(v, g, kat, kunye)
        print(v, iz[v], flush=True)

    t0, isler = time.monotonic(), []
    with ThreadPoolExecutor(VIDEO_PARALEL) as ex:  # indirme seri (aynı anda tek); Gemini yükleme/izleme sıradaki indirmeyle üst üste biner
        for v in ids:
            t, m = time.monotonic(), kok / v
            if v.startswith("ig-"):
                m = cikti / "medya" / v
                if not (m / "meta.json").is_file():
                    m.mkdir(parents=True, exist_ok=True)
                    instagram.getir(m)
            isler.append(ex.submit(isle, v, m, round(time.monotonic() - t, 1)))
        for f in isler:
            f.result()
    hazir = round(time.monotonic() - t0, 1)
    y = oturum([bloklar[v] for v in ids if v in bloklar], efor, env)
    y["hazir_sure"], y["duvar"] = hazir, round(time.monotonic() - t0, 1)
    for x in (y["form"] or {}).get("videolar", []):
        x["linkler"] = list(dict.fromkeys(x["linkler"] + paket_link.get(x["id"], [])))
        link_tamamla(x, kunye_link.get(x["id"], {}))
        (cikti / f"{x['id']}.md").write_text(rapor(x, f"gemini ({iz.get(x['id'], {}).get('gemini', {}).get('model', 'önbellek')}) + claude oturum"), encoding="utf-8")
    return iz, y


def rapor(v, kaynak):
    """Araç başı ≤4 satır markdown."""
    s = [f"# {v['id']} — kısa video", f"kaynak: {kaynak}", "", v["ozet"], "", "## Araçlar"]
    for a in v["araclar"]:
        s += [f"- **{a['ad']}** · {a['tur']}" + (f" · {a['link']}" if a["link"] else ""), f"  {a['not']}"]
    return "\n".join(s + ["", "## Linkler", *[f"- {u}" for u in v["linkler"]], ""])
