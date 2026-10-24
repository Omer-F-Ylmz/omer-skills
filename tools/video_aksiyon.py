"""VIDEO-AKSIYON-1: video/post'u anla -> arastir -> aksiyon plani. Claude jetonu 0 (agir is yerel + ucretsiz havuz).
video_derin.py'nin indir/asr/ocr/aciklama adimlarini yeniden kullanir; ustune zaman cizelgesi, yorum, repo/lisans arastirmasi, aksiyon plani ekler.
Kullanim: python tools/video_aksiyon.py <url> [--uygula]
Cikti: .kos/kopru/video/aksiyon/<kod>.md ; --uygula: KUR/UYGULA satirlari .kos/kopru/gorev/video-aksiyon-kuyruk.md'ye eklenir (silme yok)."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import video_derin as vd

KOK = vd.KOK
CIKTI = KOK / ".kos/kopru/video/aksiyon"
KUYRUK = KOK / ".kos/kopru/gorev/video-aksiyon-kuyruk.md"
GH_RE = re.compile(r"github\.com/([\w.-]+/[\w.-]+)", re.I)
SOSYAL = ("youtube.com", "youtu.be", "instagram.com", "tiktok.com", "x.com", "twitter.com", "facebook.com")
ELIMIZDE = ("gsap-skills, animasyon-scroll-paket, animasyon-atolyesi, scroll-craft, smooth-scroll, threejs-3d-paket, "
            "threejs-react-three-fiber, remotion-video-paket, hyperframes-paket, Blender headless, ffmpeg, 21st bilesenleri, "
            "ucretsiz model havuzu, REA/playwright MCP")
ISTEM = """"ozet" alaninin ICINE, 
 ile satirlara bolunmus, asagidaki 4 markdown basligini iceren metni yaz (ozet degil, plan).
Asagida bir videonun/postun incelemesi var (zaman cizelgesi, ekrandaki yazilar, sozler, bulunan repolar+lisans).
Gorev: Omer'in projeleri icin AKSIYON plani yaz. Yalniz su 4 basligi kullan, her biri 2-5 madde, her madde tek cumle, somut:
## KUR (araç/skill/MCP/CLI; varsayilan kurulur; lisans MIT/Apache degilse 'muadil veya teknigi yeniden yaz' yaz)
## UYGULA (hangi projeye, hangi adimla; videodaki teknigi nasil yaparız)
## ÖĞREN (taktik/ipucu; 2. beyine yazilacak)
## DAHA İYİSİ (elimizdekilerle nasil geciriz)
Elimizde: {elimizde}. Videodaki karakter/icerik kopyalanmaz, yalniz teknik ve arac tarafi. Incelemede olmayan arac uydurma.
Ek turkce aciklama, giris cumlesi yazma; yalniz 4 baslik."""


def kos(*a, timeout=600):
    return vd.kos(*a, timeout=timeout)


def indir(url, d):
    """video + info.json + (varsa) yorumlar; Instagram karuselinde gallery-dl ile tum gorseller."""
    gorseller = []
    if re.search(r"instagram\.com/p/", url) and shutil.which("gallery-dl"):
        g = d / "g"
        kos("gallery-dl", "-D", g, "--write-metadata", url, timeout=180)
        gorseller = sorted(p for p in g.glob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")) if g.exists() else []
    r = kos("yt-dlp", "-f", "wv[height>=360]+wa/worst[height>=360]/worst/best", "--no-playlist", "-o", d / "v.%(ext)s", url, "--write-info-json",
            "--write-comments", "--extractor-args", "youtube:max_comments=20,20,0,0", timeout=300)
    v = next((p for p in d.glob("v.*") if p.suffix != ".json"), None)
    return v, gorseller, r.stderr[-200:]


def zamanli_kareler(v, d, tavan=120):
    """sahne degisimi kareleri + her karenin saniyesi (showinfo pts_time)."""
    k = d / "k"
    k.mkdir(exist_ok=True)
    r = kos("ffmpeg", "-y", "-i", v, "-vf", "select=eq(n\\,0)+gt(scene\\,0.3),showinfo,scale=640:-1", "-fps_mode", "vfr", "-q:v", "4", k / "%04d.jpg")
    zam = [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    ks = sorted(k.glob("*.jpg"))
    if len(ks) < 2 or len(zam) != len(ks):
        shutil.rmtree(k)
        k.mkdir()
        kos("ffmpeg", "-y", "-i", v, "-vf", "fps=1,scale=640:-1", "-q:v", "4", k / "%04d.jpg")
        ks = sorted(k.glob("*.jpg"))
        zam = [float(i) for i in range(len(ks))]
    if len(ks) > tavan:
        adim = len(ks) / tavan
        idx = [int(i * adim) for i in range(tavan)]
        ks, zam = [ks[i] for i in idx], [zam[i] for i in idx]
    return ks, zam


def mmss(t):
    return f"{int(t) // 60:02d}:{int(t) % 60:02d}"


def cizelge(seg, ekran, zam_of, pencere=15):
    """pencere basina: ekranda ne yazıyor | ne söyleniyor."""
    kovalar = {}
    for e in ekran:
        b = int(zam_of.get(e["k"], 0) // pencere)
        kovalar.setdefault(b, {"ekran": [], "soz": []})["ekran"].append(e["t"])
    for s in seg:
        kovalar.setdefault(int(s["b"] // pencere), {"ekran": [], "soz": []})["soz"].append(s["t"])
    sat = []
    for b in sorted(kovalar):
        x = kovalar[b]
        sat.append(f"- [{mmss(b * pencere)}] ekran: {'; '.join(x['ekran'][:6])[:160] or '-'} | söz: {' '.join(x['soz'])[:240] or '-'}")
    return sat


def repo_bilgi(repo):
    r = kos("gh", "api", f"repos/{repo}", "--jq", "[.license.spdx_id,.stargazers_count,.pushed_at[:10],.description]|@json", timeout=30)
    try:
        lic, yildiz, son, acik = json.loads(r.stdout)
        return f"- {repo} · lisans {lic or 'YOK'} · {yildiz}★ · son {son} · {(acik or '')[:100]}"
    except (ValueError, TypeError):
        return f"- {repo} · gh doğrulanamadı (repo yok/özel olabilir)"


def calis(url, uygula):
    kod = vd.kod_of(url)
    d = Path(tempfile.mkdtemp(prefix="va_"))
    try:
        v, gorseller, hata = indir(url, d)
        if not v and not gorseller:
            return f"indirilemedi: {hata.strip().splitlines()[-1][:160] if hata.strip() else '?'}"
        meta, yorumlar = {}, []
        ij = next(d.glob("*.info.json"), None)
        if ij:
            j = json.loads(ij.read_text(encoding="utf-8"))
            meta = {"baslik": j.get("title"), "sure": j.get("duration"), "yukleyen": j.get("uploader"), "aciklama": (j.get("description") or "")[:1200]}
            yorumlar = [c.get("text", "")[:200] for c in sorted(j.get("comments") or [], key=lambda c: -(c.get("like_count") or 0))[:10]]
        dil, seg, ks, zam, kaynak = "", [], [], [], "video"
        if v:
            dil, seg = vd.asr(v, d)
            ks, zam = zamanli_kareler(v, d)
        if gorseller:
            kaynak = f"karusel ({len(gorseller)} görsel)"
            ks = list(gorseller) + ks
            zam = [0.0] * len(gorseller) + zam
        ekran = vd.ocr(ks)
        zam_of = {k.name: z for k, z in zip(ks, zam)}
        aciklama = vd.gemini_aciklama(ks) or vd.yerel_aciklama(ks)
        metin = "\n".join(e["t"] for e in ekran) + "\n" + " ".join(s["t"] for s in seg) + "\n" + meta.get("aciklama", "") + "\n" + "\n".join(yorumlar)
        repolar = sorted({m.strip(".,)").removesuffix(".git") for m in GH_RE.findall(metin)})[:8]
        linkler = sorted({m.strip(".,)") for m in vd.URL_RE.findall(metin) if not any(s in m for s in SOSYAL) and "github.com" not in m})[:15]
        komutlar = sorted({m.strip() for m in vd.KOMUT_RE.findall(metin)})[:10]
        bilgi = [repo_bilgi(r) for r in repolar]

        govde = [f"# video-aksiyon {kod}", f"url: {url} · kaynak: {kaynak} · dil: {dil or '-'} · kare: {len(ks)}",
                 f"başlık: {meta.get('baslik')} · {meta.get('yukleyen')} · {meta.get('sure')} sn", "",
                 "## Açıklama + yorumlar", (meta.get("aciklama") or "-")[:600], *[f"- yorum: {y}" for y in yorumlar[:5]], "",
                 "## Zaman çizelgesi", *cizelge(seg, ekran, zam_of), "",
                 "## Görsel anlam (kareler)", (aciklama or "-")[:1500], "",
                 "## Bulunan araç/repo/link", *(bilgi or ["- repo bulunamadı"]), *[f"- link: {x}" for x in linkler], *[f"- komut: {x}" for x in komutlar]]
        paket = "\n".join(govde)
        CIKTI.mkdir(parents=True, exist_ok=True)
        pk = d / "paket.md"
        pk.write_text(paket, encoding="utf-8")
        plan = d / "plan.md"
        r = subprocess.run([sys.executable, str(KOK / "tools/ucuz_alt.py"), "--tur", "ozet", ISTEM.format(elimizde=ELIMIZDE), str(plan), str(pk)],
                           capture_output=True, text=True, creationflags=vd.NW)
        plan_md = plan.read_text(encoding="utf-8") if plan.exists() and "## KUR" in plan.read_text(encoding="utf-8") else "## KUR\n- (havuz yanıt vermedi; el ile: yukarıdaki repo/komut satırlarına bak)\n## UYGULA\n- -\n## ÖĞREN\n- -\n## DAHA İYİSİ\n- -"
        kuyruk = []
        for blok in re.finditer(r"^## (KUR|UYGULA)[^\n]*\n((?:\s*[-*] .+\n?)+)", plan_md, re.M):
            for b in re.findall(r"^\s*[-*] (.+)$", blok.group(2), re.M):
                kuyruk.append(f"- [video-aksiyon {kod}] {blok.group(1)}: {b.strip()}")
        cikti = CIKTI / f"{kod}.md"
        cikti.write_text(paket + "\n\n# Aksiyon planı\n" + plan_md.strip() + "\n\n## Kuyruk önerisi\n" + "\n".join(kuyruk) + "\n", encoding="utf-8")
        if uygula and kuyruk:
            with KUYRUK.open("a", encoding="utf-8") as f:
                f.write("\n".join(kuyruk) + "\n")
        return f"{cikti} · seg={len(seg)} ocr={len(ekran)} repo={len(repolar)} kuyruk={len(kuyruk)}{' (kuyruğa eklendi)' if uygula and kuyruk else ''} · plan {'havuz' if r.returncode in (0, 3) else 'ŞABLON(havuz çıkış ' + str(r.returncode) + ')'}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def main():
    a = sys.argv[1:]
    uygula = "--uygula" in a
    urls = [x for x in a if not x.startswith("--")]
    if not urls:
        print(__doc__)
        return 2
    for u in urls:
        print(calis(u, uygula), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
