"""23c K2: araştırıcıya tam sayfa/tam dosya girmez. getir: sayfa → ana metin (gezinme/altbilgi atılır) + bağlantılar, üst sınırlı ve önbellekli.
repo: gh api ile README ilk 120 satır · ağaç derinlik 2 · istenen dosyanın ≤200 satırı. on: ikisini .kos/<video>/<ad>/on.md'ye yazar."""
import hashlib
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ATLA = {"script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "form"}
README, AGAC, DOSYA, BAGLANTI = 120, 80, 200, 30


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


def _al(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 video-getir"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def kes(metin, n):
    return metin if len(metin) <= n else metin[:n] + f"\n…(kesildi: {len(metin) - n} karakter)"


def kes_satir(satirlar, n):
    return satirlar[:n] + ([f"…(kesildi: {len(satirlar) - n} satır)"] if len(satirlar) > n else [])


def getir(url, n=6000, cache=None, al=_al):
    y = Path(cache) / f"{hashlib.sha1(f'{url}|{n}'.encode()).hexdigest()[:16]}.md" if cache else None
    if y and y.is_file():
        return y.read_text(encoding="utf-8")
    p = _Ayikla(url)
    p.feed(al(url))
    metin = "\n".join(p.anametin or p.tum)
    out = "\n".join([f"# {' '.join(p.baslik.split()) or url}", f"kaynak: {url}", "", kes(metin, n), "", "## Bağlantılar",
                     *kes_satir([f"- {x}" for x in dict.fromkeys(p.linkler)], BAGLANTI)]) + "\n"
    if y:
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_text(out, encoding="utf-8")
    return out


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


def on(kok, video, ad, repo_ad=None, url=None, kos=None, cache=None, al=_al):
    """K4: araştırıcı bu dosyayla başlar; eksik kalırsa `video getir`/`video repo` ile tamamlar."""
    y = Path(kok) / ".kos" / video / ad / "on.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    parca = [f"# ön getirme: {ad} · video {video}"]
    if repo_ad:
        parca.append(repo(repo_ad, kos=kos))
    if url:
        parca.append(getir(url, cache=cache, al=al))
    y.write_text("\n".join(parca), encoding="utf-8")
    return y
