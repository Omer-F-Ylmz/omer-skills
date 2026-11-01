"""PAKET-3 (D1-A): 1 Kas'ta CC'ye kurulan SKILL satirlari -> claude.ai aile paketleri.
Adimlar: aday.tsv -> (canli ayni ad+icerik atla / farkli icerik <ad>-al) -> aile.tsv -> zip -> manifest.
Kullanim: python paket3.py aday|aile|uret|manifest   (cikti dist/paket-3)"""
import zlib, csv, io, pathlib, re, shutil, sys, collections

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import fark
from envanter import _fm
import paketle

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "dist/paket-3"
HOME = pathlib.Path.home() / ".claude"
TSV = [REPO / "docs/video-tarama/kurulum-gh-sonuc.tsv", REPO / "docs/video-tarama/kurulum-gh-sonuc-ek.tsv"]

# aile -> anahtar sozcukler (ad + aciklama, kucuk harf); sira = oncelik
AILE = [
    ("guvenlik", r"security|pentest|exploit|vuln|malware|reverse|hunt|owasp|\bxss|sqli|ssrf|secret|threat|forensic|offensive|\bctf|competition-|red-team|\bsast|\bdast|strix|auth-?bypass|phish|mitre"),
    ("frontend-ui", r"frontend|\bui\b|\bux\b|css|tailwind|react|vue|svelte|angular|nextjs|design|figma|layout|typograph|shadcn|storybook|web-?page|landing|accessib|component|bootstrap|gsap|scroll|glass|dither|background|shader|animation"),
    ("3d-blender", r"three|3d|blender|webgl|gltf|mesh|unity|godot|unreal|shader"),
    ("oyun", r"game|oyun|minecraft|level-design|npc|quest"),
    ("video", r"video|remotion|hyperframes|ffmpeg|reel|subtitle|caption|motion|clip|podcast|audio|music|tts|voice|sound|transcri|youtube|\byt-"),
    ("gorsel", r"image|illustration|logo|icon|photo|diagram|infographic|svg|poster|slide|deck|thumbnail|comic|art\b"),
    ("pazarlama-reklam", r"marketing|seo|\bads?\b|ad-|campaign|social|instagram|linkedin|twitter|newsletter|email|copywrit|brand|influenc|content|geo-|crm|outreach|sales|\bcro\b|viral"),
    ("bilim", r"bio|chem|genom|protein|scienc|scientific|physic|astro|clinical|drug|rna|dna|quantum|neuro|math|stat|paper|research-|literature|lab"),
    ("ml-ai", r"\bml\b|llm|machine-learning|torch|tensorflow|transformers|fine-?tun|embedding|rag\b|vector|model|agent-?(eval|memory)|prompt|mlops|inference|cuda|gpu|huggingface|diffusion"),
    ("mobil", r"mobile|android|ios\b|swift|flutter|expo|react-native|kotlin"),
    ("bulut-devops", r"aws|azure|gcp|cloud|docker|kubernetes|k8s|terraform|devops|helm|deploy|vercel|netlify|cloudflare|ci-?cd|github-actions|infra|observab|monitor|sentry|datadog|grafana|serverless"),
    ("veri-db", r"database|sql|postgres|mysql|mongo|redis|clickhouse|dbt|etl|pipeline|data-|warehouse|supabase|prisma|orm\b|migration|duckdb|pandas|polars|analytics"),
    ("backend-dotnet", r"dotnet|\.net|csharp|c#|backend|api|fastapi|django|flask|rails|spring|laravel|nestjs|express|golang|\bgo-|rust|java\b|python|node|graphql|grpc|microservice|ef-core"),
    ("test-qa", r"test|qa\b|tdd|e2e|playwright|cypress|vitest|jest|coverage|mutation|flaky|quality"),
    ("git-yayin", r"git\b|github|commit|\bpr\b|pull-request|release|changelog|merge|branch|ship|publish"),
    ("inceleme", r"review|audit|critique|lint|refactor|simplif|code-?quality"),
    ("surec-plan", r"plan|spec|prd|roadmap|brainstorm|workflow|process|sprint|agile|estimate|decision|adr|requirement|strategy"),
    ("ajan-arac", r"agent|mcp|skill|plugin|orchestrat|subagent|tool|hook|claude|codex|cli\b|automation|memory|context"),
    ("belge", r"doc|pdf|docx|xlsx|pptx|markdown|readme|wiki|notion|obsidian|writing|translate|office|report"),
    ("arastirma", r"research|search|scrape|crawl|browser|web-|osint|fetch|summariz|explore|knowledge"),
    ("verimlilik", r"productiv|todo|task|calendar|habit|focus|token|efficien|optimi|cost|performance|speed"),
    ("is-finans-hukuk", r"financ|legal|contract|invoice|account|tax|trading|invest|stock|crypto|payment|stripe|hr\b|hiring|compliance|gdpr"),
]
AILE_RE = [(a, re.compile(r, re.I)) for a, r in AILE]


def aday():
    rows, seen = [], set()
    for f in TSV:
        for x in csv.reader(io.StringIO(f.read_bytes().decode("utf-8")), delimiter="\t"):
            if len(x) > 4 and x[1] == "SKILL" and x[3] == "KURULDU" and x[2] not in seen:
                seen.add(x[2]); rows.append((x[2], str(HOME / "skills" / x[2]), x[0]))
    return rows


def yaz(p, rows, baslik):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / p, "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter="\t", lineterminator="\n"); w.writerow(baslik); w.writerows(rows)


def oku(p):
    with open(OUT / p, encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))[1:]


def adim_aday():
    sync = next(p for p in (HOME / "skills/synced").iterdir() if p.is_dir())
    ai = fark.claudeai(sync)
    cand = aday()
    yaz("aday.tsv", cand, ["ad", "kaynak", "repo"])
    atla, yeni = [], []
    for ad, yol, repo in cand:
        kar = ai.get(fark.anahtar(ad), [])
        if not kar:
            yeni.append((ad, yol, repo, "")); continue
        cci = fark.izler(pathlib.Path(yol), "SKILL.md")
        ayni = False
        for x in kar:
            aii = fark.izler(x["dizin"], x["ana"])
            ortak = [y for y in cci if y in aii]
            eksik = [y for y in cci if y not in aii and y != "@" and y.endswith(".md")] if "REFERANS.md" not in aii else []
            if not [y for y in ortak if len(cci[y] - aii[y]) >= fark.ESIK] and not eksik:
                ayni = True; break
        if ayni:
            atla.append((ad, x["kayit"]))
        else:
            yeni.append((ad, yol, repo, "al"))
    yaz("atlandi-ayni.tsv", atla, ["ad", "canli_kayit"])
    yaz("paketlenecek.tsv", yeni, ["ad", "kaynak", "repo", "sonek"])
    print(f"aday {len(cand)} atlandi-ayni {len(atla)} paketlenecek {len(yeni)} (al-sonek {sum(1 for y in yeni if y[3])})")


def sinifla(ad, ac):
    for a, r in AILE_RE:
        if r.search(ad) or r.search(ac):
            return a
    return ""


def adim_aile():
    out = []
    for ad, yol, repo, sonek in oku("paketlenecek.tsv"):
        ac = (_fm(pathlib.Path(yol, "SKILL.md").read_text(encoding="utf-8", errors="replace"))[1] or "")
        a = sinifla(ad, ac[:200])
        out.append((ad, yol, repo, sonek, a or "diger-genel", "kural" if a else "kalan"))
    yaz("aile.tsv", out, ["ad", "kaynak", "repo", "sonek", "aile", "yontem"])
    print(collections.Counter(x[4] for x in out).most_common())


KONU = {"frontend-ui": "frontend ui arayuz css react tasarim", "backend-dotnet": "backend api dotnet python go rust sunucu",
        "veri-db": "veritabani sql veri analiz pipeline", "test-qa": "test qa tdd e2e kalite", "guvenlik": "guvenlik pentest zafiyet malware tersine",
        "surec-plan": "plan spec surec sprint karar", "inceleme": "kod inceleme review audit refactor", "git-yayin": "git github pr release yayin",
        "ajan-arac": "ajan mcp skill plugin arac orkestrasyon", "belge": "belge pdf docx pptx xlsx markdown", "arastirma": "arastirma arama scrape tarayici",
        "verimlilik": "verimlilik gorev token maliyet performans", "video": "video ses muzik remotion ffmpeg altyazi", "3d-blender": "3d blender three webgl",
        "oyun": "oyun game tasarim motor", "gorsel": "gorsel gorsel-uretim logo diyagram slayt", "pazarlama-reklam": "pazarlama seo reklam sosyal medya icerik",
        "bilim": "bilim biyoloji kimya veri bilimsel", "ml-ai": "makine ogrenmesi llm model egitim", "mobil": "mobil android ios expo swift",
        "bulut-devops": "bulut devops docker kubernetes aws azure deploy", "is-finans-hukuk": "is finans hukuk muhasebe odeme", "diger-genel": "genel cesitli arac"}


def temizle(d):
    """Hazirlik kopyasinda gorunmez Unicode silinir, gizli anahtar deseni maskelenir (kaynak kurulum dokunulmaz)."""
    import zip_denetle as zd
    gz = re.compile(zd.GIZLI.pattern.decode() if isinstance(zd.GIZLI.pattern, bytes) else zd.GIZLI.pattern)
    for f in d.rglob("*"):
        if f.is_file() and f.suffix.lower() in (".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".sh", ".tsv"):
            t = f.read_text(encoding="utf-8", errors="replace")
            n = gz.sub("[GIZLI-MASKELI]", zd.GORUNMEZ.sub("", t))
            if n != t:
                f.write_text(n, encoding="utf-8", newline="")


def adim_uret():
    import zipfile
    stage = OUT / "stage"; zipd = OUT / "zip"
    for d in (stage, zipd):
        shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    fam = collections.defaultdict(list)
    for ad, yol, repo, sonek, a, _ in oku("aile.tsv"):
        dst = stage / a / (ad + ("-al" if sonek else ""))
        shutil.copytree(yol, dst, ignore=shutil.ignore_patterns(".git", "node_modules", "__pycache__"))
        temizle(dst)
        fam[a].append((ad + ("-al" if sonek else ""), dst))
    man, engel = [], []
    for a, lst in sorted(fam.items()):
        for ad, dst in list(lst):
            try:
                sk = paketle._buyuk_skill(dst)
                w = sum(len(zlib.compress(v.encode("utf-8"))) + 150 for v in sk[3].values())
                if 1 + len(sk[3]) > paketle.SINIR or 3000 + w > paketle.BUYUK_BOYUT:
                    raise ValueError(f"tek basina sigmiyor ({len(sk[3])} dosya, {w} bayt)")
            except Exception as e:
                engel.append((ad, a, str(e)[:120])); lst.remove((ad, dst))
        for zp, n in paketle.buyuk("al-" + a, KONU[a], [str(d) for _, d in lst], str(zipd)):
            with zipfile.ZipFile(zp) as z:
                for nm in z.namelist():
                    pass
            man.append((a, pathlib.Path(zp).name, n, [x for x, _ in lst]))
        print(a, len(lst), flush=True)
    yaz("engel.tsv", engel, ["ad", "aile", "neden"])
    import json
    (OUT / "uret.json").write_text(json.dumps([[a, z, n, l] for a, z, n, l in man], ensure_ascii=False), encoding="utf-8")


def adim_manifest():
    import json, zipfile
    man = json.loads((OUT / "uret.json").read_text(encoding="utf-8"))
    rows = []
    for a, z, n, l in man:
        with zipfile.ZipFile(OUT / "zip" / z) as zf:
            adlar = {m.split("/")[2] for m in zf.namelist() if m.count("/") >= 3 and m.split("/")[1] == "skills"}
        rows += [(s, z) for s in sorted(adlar)]
    yaz("manifest.tsv", rows, ["skill", "zip"])
    zips = sorted(p.name for p in (OUT / "zip").glob("*.zip"))
    for i in range(0, len(zips), 20):
        d = OUT / f"parti-{i // 20 + 1}"; shutil.rmtree(d, ignore_errors=True); d.mkdir()
        for z in zips[i:i + 20]:
            shutil.copy(OUT / "zip" / z, d / z)
    cov = {s for s, _ in rows} | {r[0] + ("-al" if r[3] else "") for r in oku("paketlenecek.tsv")} - {e[0] for e in oku("engel.tsv")}
    gercek = {s for s, _ in rows}
    eksik = [r[0] + ("-al" if r[3] else "") for r in oku("paketlenecek.tsv")]
    eksik = [x for x in eksik if x not in gercek and x not in {e[0] for e in oku("engel.tsv")}]
    print("zip", len(zips), "parti", -(-len(zips) // 20), "manifest", len(rows), "eksik", len(eksik), eksik[:10])


if __name__ == "__main__":
    {"aday": adim_aday, "aile": adim_aile, "uret": adim_uret, "manifest": adim_manifest}[sys.argv[1]]()
