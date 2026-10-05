"""23c K2: araştırıcıya tam sayfa/tam dosya girmez. getir: sayfa → ana metin (gezinme/altbilgi atılır) + bağlantılar, üst sınırlı ve önbellekli.
repo: gh api ile README ilk 120 satır · ağaç derinlik 2 · istenen dosyanın ≤200 satırı. on: ikisini .kos/<video>/<ad>/on.md'ye yazar."""
import hashlib
import json
import re
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

from . import tarama as tr
from .metin import sn

ATLA = {"script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"}
README, AGAC, DOSYA, BAGLANTI, PROMPT = 120, 80, 200, 30, 4000


class _Ayikla(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url, self.atla, self.ana, self.baslik_ic = url, 0, 0, False
        self.baslik, self.tum, self.anametin, self.linkler = "", [], [], []

    def handle_starttag(self, tag, attrs):
        if tag in ATLA:
            self.atla += 1
        elif tag in ("main", "article"):
            self.ana += 1
        elif tag == "title":
            self.baslik_ic = True
        elif tag == "a" and not self.atla and (h := dict(attrs).get("href")) and not h.startswith(("#", "javascript:", "mailto:")):
            self.linkler.append(urljoin(self.url, h))

    def handle_endtag(self, tag):
        if tag in ATLA:
            self.atla = max(0, self.atla - 1)
        elif tag in ("main", "article"):
            self.ana = max(0, self.ana - 1)
        elif tag == "title":
            self.baslik_ic = False

    def handle_data(self, data):
        if self.baslik_ic:
            self.baslik += data
        elif not self.atla and data.strip():
            (self.anametin if self.ana else self.tum).append(" ".join(data.split()))


_son = [0.0]
ACMA, ILGILI = ("github", "video", "sosyal"), ("github", "gist", "doküman", "ürün/marketplace", "video")  # github B3'te gh ile okunur · video → B ek kuyruk


def _al(url):
    time.sleep(max(0.0, _son[0] + 2 - time.monotonic()))  # plan: web istekleri arası ≥2 sn
    _son[0] = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 video-getir"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


class GetirHata(Exception):
    pass


def kes(metin, n):
    return metin if len(metin) <= n else metin[:n] + f"\n…(kesildi: {len(metin) - n} karakter)"


def kes_satir(satirlar, n):
    return satirlar[:n] + ([f"…(kesildi: {len(satirlar) - n} satır)"] if len(satirlar) > n else [])


def getir(url, n=6000, cache=None, al=_al):
    y = Path(cache) / f"{hashlib.sha1(f'{url}|{n}'.encode()).hexdigest()[:16]}.md" if cache else None
    if y and y.is_file():
        return y.read_text(encoding="utf-8")
    p = _Ayikla(url)
    try:
        p.feed(al(url))
    except urllib.error.URLError as e:  # HTTPError dahil: ham traceback yerine anlamlı hata
        raise GetirHata(f"getir {url}: {getattr(e, 'code', '') or ''} {getattr(e, 'reason', e)}".replace("  ", " ")) from None
    metin = "\n".join(p.anametin or p.tum)
    out = "\n".join([f"# {' '.join(p.baslik.split()) or url}", f"kaynak: {url}", "", kes(metin, n), "", "## Bağlantılar",
                     *kes_satir([f"- {x}" for x in dict.fromkeys(p.linkler)], BAGLANTI)]) + "\n"
    if y:
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_text(out, encoding="utf-8")
    return out


def derinlik1(linkler, kok, al=_al, hata=None):
    """B1: linkli sayfalardaki ilgili linkler (1 derinlik); sayfa <kok>/sayfa önbelleğinde → aynı URL bütün partilerde bir kez okunur.
    B2: açılamayan sayfa `hata`ya (url, sebep) olarak eklenir; paket düşmez."""
    gor, yeni = {x["url"] for x in linkler}, []
    for x in linkler:
        if x["sinif"] in ACMA:
            continue
        try:
            s = getir(x["url"], cache=Path(kok) / "sayfa", al=al)
        except (GetirHata, OSError, ValueError) as e:  # zaman aşımı / bozuk adres de erişilemedi
            if hata is not None:
                hata.append((x["url"], str(e).removeprefix(f"getir {x['url']}: ")))
            continue
        for b in tr.link_topla({f"sayfa {x['url']}": tr.bolum(s, "Bağlantılar")}):
            if b["sinif"] in ILGILI and b["url"] not in gor:
                gor.add(b["url"])
                yeni.append(b)
    return yeni


def _gh(kos, *args):
    rc, out, err = kos(["gh", "api", *args])
    if rc:
        raise RuntimeError(f"gh api {args[0]}: {(err or b'').decode('utf-8', 'replace').strip()[:200]}")
    return out.decode("utf-8", "replace").splitlines()


def repo(ad, dosya=None, satir=None, kos=None):
    if dosya:
        a, _, b = (satir or f"1-{DOSYA}").partition("-")
        a = max(1, int(a))
        b = int(b or a + DOSYA - 1)
        s = _gh(kos, f"repos/{ad}/contents/{dosya}", "-H", "Accept: application/vnd.github.raw")[a - 1:b]
        return "\n".join([f"# {ad}/{dosya} satır {a}-{a + min(len(s), DOSYA) - 1}", *kes_satir(s, DOSYA)]) + "\n"
    readme = _gh(kos, f"repos/{ad}/readme", "-H", "Accept: application/vnd.github.raw")
    agac = [x for x in _gh(kos, f"repos/{ad}/git/trees/HEAD?recursive=1", "--jq", ".tree[].path") if x.count("/") <= 1]
    return "\n".join([f"# {ad}", "## README", *kes_satir(readme, README), "", "## Ağaç (derinlik 2)", *kes_satir(agac, AGAC)]) + "\n"


YAPIMCI = {"surum": 3, "issue": 5, "discussion": 5}  # ayar · B3: en fazla N (sürüm notu · açık ve kapalı issue ayrı ayrı · discussion)
ARAMA = {"aralik": 2.1, "bekle_ust": 60}  # ayar · B3 eki: gh arama uçları dakikada 30 istek; oran sınırında tek bekleme (≤60 sn)
uyku, saat = time.sleep, time.monotonic  # testte sahte
_son_ara = [float("-inf")]


def _gh_ara(kos, *args):
    """B3 eki: arama çağrıları arası ≥ARAMA["aralik"] sn; oran sınırında Retry-After / X-RateLimit-Reset kadar (başlık yoksa
    üst sınır) BİR kez bekler, BİR kez yeniden dener; yine olmazsa _gh gibi RuntimeError (→ erisilemedi)."""
    for deneme in (0, 1):
        uyku(max(0.0, _son_ara[0] + ARAMA["aralik"] - saat()))
        rc, out, err = kos(["gh", "api", "-i", *args])
        _son_ara[0] = saat()
        t = out.decode("utf-8", "replace").replace("\r\n", "\n")
        bas, govde = t.partition("\n\n")[::2] if t.startswith("HTTP/") else ("", t)
        if not rc:
            return govde.splitlines()
        sebep = (err or b"").decode("utf-8", "replace").strip()
        if deneme or not re.search(r"rate limit|HTTP 429", bas + sebep, re.I):
            raise RuntimeError(f"gh api {args[0]}: {sebep[:200]}")
        ra, rs = (re.search(rf"^{h}:\s*(\d+)", bas, re.I | re.M) for h in ("retry-after", "x-ratelimit-reset"))
        bekle = int(ra[1]) if ra else (int(rs[1]) - time.time() if rs else ARAMA["bekle_ust"])
        uyku(min(ARAMA["bekle_ust"], max(0.0, bekle)))


def yapimci(ad, kos, hata):
    """B3: sürüm notları + en çok tepki alan açık/kapalı issue + discussion başlıkları (gh api). gh hatası (kota/oran sınırı dahil)
    adayı düşürmez: `hata`ya (istek, sebep) eklenir, bölümde 'erişilemedi' satırı olur."""
    n, out = YAPIMCI, ["## Yapımcı nasıl yaptı", "bilinen hata/sınırlama/şikâyet → kötü yan · yazarın önerdiği ayar/çözüm → onarım (kaynak linkiyle)"]
    gq = (f'query=query{{search(query:"repo:{ad} sort:reactions",type:DISCUSSION,first:{n["discussion"]})'
          '{nodes{... on Discussion{title url reactions{totalCount}}}}}')
    istek = [([f"repos/{ad}/releases?per_page={n['surum']}"],
              lambda j: [f"- {r['tag_name']} · {r['html_url']} · {' '.join((r.get('body') or '').split())[:300]}" for r in j]),
             *[(["search/issues", "-X", "GET", "-f", f"q=repo:{ad} is:issue is:{d}", "-f", "sort=reactions", "-f", f"per_page={n['issue']}"],
                lambda j, t=t: [f"- {t} · {i['title']} · tepki {i['reactions']['total_count']} · {i['html_url']}" for i in j["items"]])
               for d, t in (("open", "açık"), ("closed", "kapalı"))],
             (["graphql", "-f", gq], lambda j: [f"- discussion · {x['title']} · tepki {x['reactions']['totalCount']} · {x['url']}"
                                                for x in j["data"]["search"]["nodes"] if x])]
    for args, bic in istek:
        try:
            out += bic(json.loads("\n".join((_gh_ara if args[0] in ("search/issues", "graphql") else _gh)(kos, *args))))
        except Exception as e:  # kota/oran sınırı, 404, bozuk JSON → aday düşmez, sebep görünür
            lab = "gh api " + next((a[2:] for a in args if a.startswith("q=")), args[0])
            hata.append((lab, str(e)[:200]))
            out.append(f"- erişilemedi: {lab} ({str(e)[:200]})")
    return "\n".join(out) + "\n"


WEB = {"sorgu": 5, "sonuc": 3}  # ayar · B4: aday başına en fazla N sorgu · sorgu başına sonuç
SORGU = ("{ad} review", "{ad} vs alternatives comparison", "{ad} known issues problems", "{ad} alternative",
         "{ad} announcement blog post")  # inceleme · karşılaştırma · bilinen sorun · alternatif · yazarın duyuru/blog yazısı (B3'ten)
DUSUK = tr.KACAN_SOSYAL + ("reddit.com", "news.ycombinator.com", "stackoverflow.com", "stackexchange.com", "lobste.rs")  # forum/sosyal


def _sonuclar(t):
    """mcporter exa çıktısı: JSON (results/content) ya da 'Title: … / URL: …' metni → [(başlık, url)]."""
    try:
        j = json.loads(t)
    except ValueError:
        out, b = [], ""
        for s in t.splitlines():
            if s.startswith("Title:"):
                b = s[6:].strip()
            elif s.startswith("URL:"):
                out.append((b, s[4:].strip()))
        return out
    if isinstance(j, dict) and "content" in j:
        return _sonuclar("\n".join(c.get("text", "") for c in j["content"]))
    return [(x.get("title") or "", x["url"]) for x in (j.get("results", []) if isinstance(j, dict) else j) if x.get("url")]


def web_ara(ad, kos, hata):
    """B4: genel web araması (Agent Reach yolu: mcporter exa.web_search_exa), web istekleri arası ≥2 sn. Forum/sosyal 'düşük güven';
    aynı URL bir kez; sorgu hatası adayı düşürmez → `hata`ya (istek, sebep)."""
    out, gor = ["## Web araması", "inceleme · karşılaştırma · alternatif · bilinen sorun · yazarın duyuru/blog yazısı; forum/sosyal → düşük güven"], set()
    for q in (s.format(ad=ad) for s in SORGU[:WEB["sorgu"]]):
        uyku(max(0.0, _son[0] + 2 - saat()))  # plan: web istekleri arası ≥2 sn
        rc, o, err = kos(["mcporter", "call", "exa.web_search_exa", f"query={q}", f"numResults={WEB['sonuc']}"])
        _son[0] = saat()
        if rc:
            hata.append((f"web: {q}", (e := (err or b"").decode("utf-8", "replace").strip()[:200])))
            out.append(f"- erişilemedi: web: {q} ({e})")
            continue
        for b, u in _sonuclar(o.decode("utf-8", "replace"))[:WEB["sonuc"]]:
            if u not in gor:
                gor.add(u)
                h = urlparse(u).netloc.lower()
                dusuk = "forum" in h or any(h == s or h.endswith("." + s) for s in DUSUK)
                out.append(f"- {q} · {b} · {u}" + (" · düşük güven" if dusuk else ""))
    return "\n".join(out) + "\n"


def prompt_metni(rapor, seg):
    """24a K2: tarama raporu Adaylar'ında tür=prompt satırı → zamanından sonraki ilk `## Bölümler` zamanına kadar paket altyazısı (≤4000, kesildi)."""
    satir = [s for s in (tr.tablolar(tr.bolum(rapor, "Adaylar")) or [([], [])])[0][1] if len(s) >= 7 and s[2].casefold() == "prompt"]
    if not satir:
        return "## Prompt metni\nyok (raporda tür=prompt aday yok)\n"
    bol = sorted(sn(z) for z in tr.ZAMAN.findall(tr.bolum(rapor, "Bölümler")))
    segs = [json.loads(x) for x in Path(seg).read_text(encoding="utf-8").splitlines() if x.strip()] if seg and Path(seg).is_file() else []
    out = ["## Prompt metni", "kaynak: tarama raporu tür=prompt satırı + paket altyazısı; araştırıcı prompt aramaz, buradan okur"]
    for s in satir:
        t = sn(s[5]) if tr.ZAMAN.fullmatch(s[5]) else 0.0
        son = next((b for b in bol if b > t), float("inf"))
        metin = " ".join(" ".join(x["metin"]) if isinstance(x["metin"], list) else x["metin"] for x in segs if t <= x["bas"] < son)
        out += [f"### {s[0]} · {s[5]}", f"ekran: {s[6]}", kes(metin, PROMPT) if metin else "altyazı yok (paket segmentleri bulunamadı)", ""]
    return "\n".join(out)


def on(kok, video, ad, repo_ad=None, url=None, kos=None, cache=None, al=_al, rapor=None, seg=None, guvenlik=None, kapsam=None, web=False):
    """K4: araştırıcı bu dosyayla başlar; eksik kalırsa `video getir`/`video repo` ile tamamlar. 24a K2: rapor → prompt metni.
    24b K1: guvenlik → `## Güvenlik ön taraması` bölümü (araştırıcı klonlamaz, taramaz; buradan okur).
    B3: repo varsa `## Yapımcı nasıl yaptı`; gh hataları kapsam.json "erisilemedi"ye (B2 gibi, aynısı tekrar yazılmaz)."""
    from video.cli import _slug  # cli bu modülü içe aktarır; döngü yalnız çağrıda çözülür
    y = Path(kok) / ".kos" / video / _slug(ad) / "on.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    parca, hata = [f"# ön getirme: {ad} · video {video}"], []
    if repo_ad:
        parca.append(repo(repo_ad, kos=kos))
        parca.append(yapimci(repo_ad, kos, hata))
    if web:
        parca.append(web_ara(ad, kos, hata))
    if hata and kapsam and Path(kapsam).is_file():  # ponytail: kapsam.json yoksa (paketsiz video) hata yalnız on.md'de
        k = json.loads(Path(kapsam).read_text(encoding="utf-8"))
        k["erisilemedi"] = [*(e := k.get("erisilemedi", [])), *[list(h) for h in hata if list(h) not in e]]
        Path(kapsam).write_text(json.dumps(k, ensure_ascii=False), encoding="utf-8")
    if guvenlik:
        parca.append(guvenlik)
    if url:
        parca.append(getir(url, cache=cache, al=al))
    if rapor:
        parca.append(prompt_metni(Path(rapor).read_text(encoding="utf-8"), seg))
    y.write_text("\n".join(parca), encoding="utf-8")
    return y
