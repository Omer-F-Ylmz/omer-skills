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
from pathlib import Path

from . import hafif
from . import tarama as tr

API = "https://generativelanguage.googleapis.com"
MODELLER = ("gemini-3.5-flash", "gemini-3.8-flash")  # ücretsiz katman; ilki 429/404/5xx verirse sıradaki
KOK = Path(__file__).resolve().parents[3]
KARAR = KOK / "docs" / "kurulumlar" / "ig-41" / "karar-birlesik.tsv"
ARASTIRMA = KOK / ".kos" / "kopru" / "video" / "kisa" / "arastirma"
PAKET_TAVAN = 12_000  # paket.md karakteri (Gemini'ye bağlam; ücretsiz)
SEMA = {"type": "OBJECT", "required": ["konusma_ozet", "ekran_metni", "araclar", "linkler", "komutlar", "iddialar"], "properties": {
    "konusma_ozet": {"type": "STRING"},
    "ekran_metni": {"type": "ARRAY", "items": {"type": "STRING"}},
    "araclar": {"type": "ARRAY", "items": {"type": "OBJECT", "required": ["ad", "ne_dedi", "zaman"], "properties": {
        "ad": {"type": "STRING"}, "ne_dedi": {"type": "STRING"}, "zaman": {"type": "STRING"}}}},
    "linkler": {"type": "ARRAY", "items": {"type": "STRING"}},
    "komutlar": {"type": "ARRAY", "items": {"type": "STRING"}},
    "iddialar": {"type": "ARRAY", "items": {"type": "STRING"}}}}
ISTEM = ("Bu kısa videoyu (ya da carousel slaytlarını) baştan sona izle; konuşmayı VE ekrandaki her yazıyı oku. Ekte paket.md var: açıklama, "
         "açıklama/yorum bağlantıları, otomatik transkript ve OCR (yazım için kullan, eksiklerini videodan tamamla). Türkçe yaz.\n"
         "- araclar: anılan ya da ekranda görünen HER araç, repo, kütüphane, model, skill, MCP, CLI, servis, site; adı ekrandaki yazımıyla "
         "(owner/repo görünüyorsa öyle). ne_dedi: videonun onun hakkında söylediği/gösterdiği (≤25 kelime). zaman: m:ss ya da 'açıklama'/'yorum'.\n"
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
                p.append(yukle(medya / ad, key))
        for ad in meta.get("gorseller") or []:
            if (medya / ad).is_file():
                p.append({"inlineData": {"mimeType": "image/jpeg", "data": __import__("base64").b64encode((medya / ad).read_bytes()).decode()}})
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
             "generationConfig": {"responseMimeType": "application/json", "responseSchema": SEMA, "temperature": 0.2}}
    son = []
    for m in MODELLER:
        try:
            y = _iste(f"{API}/v1beta/models/{m}:generateContent", key, govde)
            j = json.loads(y["candidates"][0]["content"]["parts"][0]["text"])
            iz = {"model": m, "sure": round(time.monotonic() - t, 1), "jeton": (y.get("usageMetadata") or {}).get("totalTokenCount")}
            hedef.write_text(json.dumps({**j, "_iz": iz}, ensure_ascii=False, indent=1), encoding="utf-8")
            return j, iz
        except urllib.error.HTTPError as e:
            son.append(f"{m}: HTTP {e.code} {e.read()[:200]!r}")
            if e.code not in (404, 429, 500, 503):
                break
        except (KeyError, IndexError, ValueError) as e:
            son.append(f"{m}: yanıt ayrıştırılamadı ({type(e).__name__})")
    raise RuntimeError(f"gemini: {' | '.join(son)}")


def _kararlar():
    if not KARAR.is_file():
        return {}
    satir = [s.split("\t") for s in KARAR.read_text(encoding="utf-8").splitlines()]
    bas = satir[0]
    return {tr.normal(s[bas.index("kalem")]): f"{s[bas.index('karar')]} (ig-41)" for s in satir[1:] if len(s) == len(bas)}


def katalog(adlar, ev=None):
    """{ad: 'kurulu:<kaynak>' | '<karar> (ig-41)' | None}; None = bilinmeyen → tam araştırma."""
    sozluk, karar = tr.sozluk_kur(Path(ev or Path.home()), []), _kararlar()
    out = {}
    for a in adlar:
        k = karar.get(tr.normal(a))
        e = None if k else tr.eslestir(a, sozluk)
        out[a] = k or (f"kurulu:{e[1]}" if e else None)
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
    r = subprocess.run(["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={ad} in:name", "-f", "per_page=1", "--jq", ".items[0].full_name"],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    return (r.stdout.strip(), "gh arama, doğrulanmadı") if r.returncode == 0 and r.stdout.strip() else (None, None)


OTURUM_SISTEM = ("Kısa video değerlendiricisisin. Her VIDEO bloğu Gemini'nin videoyu izleyip çıkardığı JSON'dur (konuşma + ekran + açıklama/yorum linkleri) "
                 "ve her aracın katalog durumudur. Hiçbir video ve hiçbir araç elenmez. Her araç için: tur (skill·plugin·MCP·CLI·kütüphane·uygulama·servis·model·teknik·ipucu), "
                 "link (JSON'da varsa, yoksa boş), not ≤2 kısa cümle. Katalog 'kurulu'/'karar' diyorsa not yalnız FARK (yeni sürüm/özellik/iddia) ya da 'fark yok'; "
                 "'bilinmeyen' ise not = ne işe yarar + bizde ne işe yarar, arastirma künyesi varsa lisans/hesap şartını ekle. "
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


def calistir(ids, kok, cikti, efor="low", env=None):
    """Uçtan uca: her id için IG medyası (cikti/medya/<id>, hat indirir) → izle → katalog → bilinmeyene arastir → tek oturum → cikti/<id>.md.
    kok/<id>/meta.json (+ paket.md) önceden `video paket` ile hazır olmalı. → (iz, oturum sonucu)."""
    from . import instagram
    kok, cikti = Path(kok), Path(cikti)
    iz, bloklar = {}, []
    for v in ids:
        t, m = time.monotonic(), kok / v
        if v.startswith("ig-"):
            m = cikti / "medya" / v
            if not (m / "meta.json").is_file():
                m.mkdir(parents=True, exist_ok=True)
                instagram.getir(m)
        indir = round(time.monotonic() - t, 1)
        g, gi = izle(kok / v, m, env)
        kat = katalog([a["ad"] for a in g["araclar"]])
        kunye, t = {}, time.monotonic()
        for a in g["araclar"]:
            if not kat[a["ad"]]:
                r, nasil = repo_bul(a["ad"], g["linkler"] + [a["ne_dedi"]])
                if r:
                    kunye[a["ad"]] = {**arastir(r), "bulunus": nasil}
        iz[v] = {"indir": indir, "gemini": gi, "arastir": round(time.monotonic() - t, 1), "arac": len(kat), "bilinen": sum(1 for x in kat.values() if x)}
        bloklar.append(blok(v, g, kat, kunye))
        print(v, iz[v], flush=True)
    y = oturum(bloklar, efor, env)
    for x in (y["form"] or {}).get("videolar", []):
        (cikti / f"{x['id']}.md").write_text(rapor(x, f"gemini ({iz.get(x['id'], {}).get('gemini', {}).get('model', 'önbellek')}) + claude oturum"), encoding="utf-8")
    return iz, y


def rapor(v, kaynak):
    """Araç başı ≤4 satır markdown."""
    s = [f"# {v['id']} — kısa video", f"kaynak: {kaynak}", "", v["ozet"], "", "## Araçlar"]
    for a in v["araclar"]:
        s += [f"- **{a['ad']}** · {a['tur']}" + (f" · {a['link']}" if a["link"] else ""), f"  {a['not']}"]
    return "\n".join(s + ["", "## Linkler", *[f"- {u}" for u in v["linkler"]], ""])
