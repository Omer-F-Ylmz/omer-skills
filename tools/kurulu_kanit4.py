"""KANIT-3: ana-liste.tsv'de durum=KURULU-KANITSIZ kalemler icin gercek kanit uretir (kurulum yapmaz, yan etkili komut calistirmaz).
Yontem: skill/komut/ajan -> .md frontmatter + ad eslesmesi; plugin -> installed_plugins.json + installPath; mcp -> yapilandirmada kayitli + komut cozumu;
cli -> yalniz --version (guvenlik: yalniz --version; husky/lefthook yasak); klon -> git HEAD + dosya; site/yontem/prompt/varlik -> kayit satiri + kaynak (HTTP 200 / dosya yolu).
Kullanim: python -I tools/kurulu_kanit4.py [--yaz] | --dogrula N   (cikti: tmp/kanit3_sonuc.tsv; --yaz ana-liste + kurulu-kanit.tsv gunceller, yedek alir)"""
import csv, glob, json, os, random, re, shutil, subprocess, sys, time, urllib.request, collections
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

K = Path(r"C:\Projeler\omer-skills"); V = K / "docs/video-tarama"; HOME = Path.home(); CL = HOME / ".claude"
ARAC = HOME / "Desktop/Claude ile yapılanlar/araclar"
csv.field_size_limit(10**9)
NW = 0x08000000
GENEL = {"core", "cli", "app", "sdk", "server", "main", "docs", "skills", "plugin", "plugins", "web", "api", "mcp", "tools", "agent", "agents", "code", "test", "demo"}
YASAK_EXE = {"husky", "lefthook", "pre-commit", "git-lfs"}
SADECE_VERSION = re.compile(r"nmap|sqlmap|metasploit|msf|nuclei|burp|hydra|john|hashcat|ffuf|strix|semgrep|gitleaks|trivy|nikto|wpscan|aircrack|impacket|bloodhound|mimikatz|ghidra|radare|frida", re.I)

def n(s): return re.sub(r"[^a-z0-9]", "", str(s).lower())
def anahtar(ad):
    ad = str(ad).strip(); ks = {n(ad)}
    if "/" in ad: ks.add(n(ad.rstrip("/").split("/")[-1]))
    for o, r in re.findall(r"github\.com/([\w.-]+)/([\w.-]+)", ad): ks.add(n(r.removesuffix(".git")))
    if "__" in ad: ks.add(n(ad.split("__", 1)[1]))
    return [k for k in ks if len(k) >= 3 and k not in GENEL]
def run(a, t=25):
    try:
        r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=t, stdin=subprocess.DEVNULL, creationflags=NW)
        return r.returncode, (r.stdout + r.stderr).strip()
    except Exception as e: return -1, type(e).__name__

def fm(f):
    """SKILL.md/komut/ajan frontmatter: (ad, None) ya da (None, neden)."""
    try: t = Path(f).read_text(encoding="utf-8", errors="ignore")[:4000]
    except Exception: return None, "dosya-okunamadi"
    t = t.lstrip("\ufeff")
    if not t.startswith("---"): return None, "frontmatter-yok"
    kapan = re.search(r"^---\s*$", t[3:], re.M)
    if not kapan: return None, "frontmatter-kapanmamis"
    blok = t[3:3 + kapan.start()]
    m = re.search(r"^name:\s*['\"]?([^\n'\"]+)", blok, re.M)
    if not re.search(r"^description:", blok, re.M) and not m: return None, "frontmatter-bos"
    return (m.group(1).strip() if m else Path(f).parent.name if Path(f).name.lower() == "skill.md" else Path(f).stem), None

SK = {}; PL = {}; MC = {}; KL = {}
def sk_ekle(key, p): SK.setdefault(key, []).append(str(p))
def indeks():
    for d in os.scandir(CL / "skills"):
        if d.is_dir() or d.is_symlink():
            for nm in ("SKILL.md", "skill.md"):
                p = Path(d.path) / nm
                if p.exists(): sk_ekle(n(d.name), p); break
    for d in glob.glob(str(CL / "commands/*.md")) + glob.glob(str(CL / "agents/*.md")): sk_ekle(n(Path(d).stem), d)
    C = str(CL / "plugins/cache")
    for pat in ("*/*/*/skills/*/SKILL.md", "*/*/*/*/skills/*/SKILL.md", "*/*/*/commands/*.md", "*/*/*/agents/*.md"):
        for p in glob.glob(C + "/" + pat):
            q = Path(p); sk_ekle(n(q.parent.name if q.name == "SKILL.md" else q.stem), q)
    ip = json.loads((CL / "plugins/installed_plugins.json").read_text(encoding="utf-8")).get("plugins", {})
    for key, v in ip.items():
        for k in {n(key.split("@")[0]), n(key)}: PL.setdefault(k, (key, v[0].get("installPath", "")))
    def mcp_ekle(src, d):
        for nm, c in (d or {}).items():
            if isinstance(c, dict): MC.setdefault(n(nm), (src, nm, c.get("command") or c.get("url") or ""))
    for src in ("~/.claude.json", "settings.json"):
        p = HOME / ".claude.json" if src.startswith("~") else CL / src
        try: d = json.loads(p.read_text(encoding="utf-8"))
        except Exception: continue
        mcp_ekle(src, d.get("mcpServers"))
        for pr in (d.get("projects") or {}).values(): mcp_ekle(src, pr.get("mcpServers"))
    for p in glob.glob(C + "/*/*/*/.mcp.json"):
        try: d = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception: continue
        mcp_ekle("plugin:" + Path(p).parts[-4], d.get("mcpServers", d))
    if ARAC.exists():
        for d1 in ARAC.iterdir():
            if d1.is_dir():
                for k in anahtar(d1.name): KL.setdefault(k, d1)
                for d2 in d1.iterdir():
                    if d2.is_dir():
                        for k in anahtar(d2.name): KL.setdefault(k, d2)
try: AUTH = json.loads((CL / "mcp-needs-auth-cache.json").read_text(encoding="utf-8"))
except Exception: AUTH = {}
YONTEM = {}
def yontem_oku():
    for f, kol in ((K / "docs/envanter/kayit-yontem-prompt.tsv", "kalem"), (K / "docs/envanter/varlik-siniflari.tsv", None)):
        if not f.exists(): continue
        rd = csv.DictReader(open(f, encoding="utf-8-sig", errors="replace", newline=""), delimiter="\t")
        for r in rd:
            ad = r.get(kol or "kalem") or r.get("ad") or next(iter(r.values()), "")
            for k in anahtar(ad): YONTEM.setdefault(k, f.name)

def exe_bul(ad):
    adlar = []
    for v in (str(ad).strip().lstrip("/.").lower(), re.sub(r"\s+", "-", str(ad).strip().lstrip("/.").lower()), n(ad)):
        for w in (v, re.sub(r"-?cli$", "", v)):
            if w and re.fullmatch(r"[a-z0-9][a-z0-9._-]{1,40}", w) and w not in adlar: adlar.append(w)
    for w in adlar:
        if w in YASAK_EXE or w in GENEL: continue
        e = shutil.which(w)
        if e and Path(e).stem.lower() not in YASAK_EXE: return w, e
    return None, None

def url_kontrol(u):
    u = u.strip().split("|")[0].strip()
    if not re.match(r"https?://", u): return None
    for met in ("HEAD", "GET"):
        try:
            rq = urllib.request.Request(u, method=met, headers={"User-Agent": "Mozilla/5.0 (kanit-3 link check)"})
            with urllib.request.urlopen(rq, timeout=15) as r:
                if r.status == 200: return f"HTTP 200 {u[:70]}"
        except urllib.error.HTTPError as e:
            if met == "GET": return f"HTTP{e.code}:{u[:60]}"
        except Exception as e:
            if met == "GET": return f"HATA:{type(e).__name__}:{u[:60]}"
    return None

def coz(r):
    """(sonuc, tur, ayrinti, neden_kodu)"""
    kalem, tur, link = r["kalem"], r["tur"], r["repo_link"]
    keys = anahtar(kalem) + [n(kalem)]
    keys = list(dict.fromkeys(k for k in keys if k))
    # 1) skill / komut / ajan
    hata = None
    for k in keys:
        for p in SK.get(k, [])[:4]:
            ad, h = fm(p)
            if ad: return "KANIT", "skill", f"{Path(p).parent.name if Path(p).name.lower()=='skill.md' else Path(p).name} frontmatter ok name={ad[:40]} ({Path(p).as_posix()[-70:]})", ""
            hata = h
    # 2) plugin
    for k in keys:
        if k in PL:
            key, ip = PL[k]
            if ip and Path(ip).exists() and any(Path(ip).iterdir()): 
                pj = Path(ip) / ".claude-plugin/plugin.json"
                ok = ""
                try: ok = " plugin.json ok" if pj.exists() and json.loads(pj.read_text(encoding="utf-8")) else ""
                except Exception: pass
                return "KANIT", "plugin", f"installed_plugins.json:{key} installPath var{ok}", ""
    # 3) mcp
    for k in keys:
        if k in MC:
            src, nm, cmd = MC[k]
            c0 = str(cmd).split(" ")[0]
            cozulen = c0.startswith("http") or bool(shutil.which(c0)) or Path(c0).exists()
            if cozulen: return "KANIT", "mcp", f"{src} mcpServers.{nm} kayitli; komut/url cozuldu ({Path(c0).name[:30] if not c0.startswith('http') else 'http'})", ""
            hata = "mcp-komut-cozulemedi"
    if any(k in AUTH or any(k == n(a) for a in AUTH) for k in keys): return "KANITSIZ", "baglayici", "claude.ai baglayicisi mcp-needs-auth-cache'te; yetki bekliyor (kimlik dogrulamasiz listelenemez)", "BAGLAYICI-YETKI"
    # 4) cli (yalniz --version)
    ad, exe = exe_bul(kalem)
    if exe:
        args = [("--version",)] if SADECE_VERSION.search(ad) else [("--version",), ("-V",), ("--help",)]
        for a in args:
            c, o = run([exe, *a], 25)
            if c == 0 and o: return "KANIT", "cli", f"{Path(exe).name} {a[0]} exit0: {o.splitlines()[0][:60]}", ""
    # 5) klon
    for k in keys:
        d = KL.get(k)
        if d:
            c, o = run(["git", "-C", str(d), "rev-parse", "--short", "HEAD"], 15)
            ic = sum(1 for _ in zip(range(3), d.iterdir()))
            if ic and (c == 0 or (d / "package.json").exists() or (d / "pyproject.toml").exists() or (d / "README.md").exists()):
                return "KANIT", "klon", f"dizin {d.name} git HEAD {o[:8] if c==0 else '-'} dosya var", ""
    # 6) site / link
    for u in (link, kalem):
        if u and re.match(r"https?://", u.strip()):
            s = url_kontrol(u)
            if s and s.startswith("HTTP 200"): return "KANIT", "baglanti", s + (" +kayit satiri" if any(k in YONTEM for k in keys) else ""), ""
            if s: return "KANITSIZ", "baglanti", s, "LINK-ULASILAMADI"
    # 7) kayit satiri (yontem/prompt/varlik/ui)
    for k in keys:
        if k in YONTEM and tur in ("yontem", "prompt", "varlik", "ui-kutuphane", "kutuphane"):
            return "KANITSIZ", "kayit", f"kayit satiri var ({YONTEM[k]}); kaynak URL/dosya yolu yok", "KAYNAK-LINK-YOK"
    if hata: return "KANITSIZ", "?", f"eslesme var ama kanit uretilemedi ({hata})", "BOZUK-KAYIT"
    return "KANITSIZ", "?", f"tur={tur}: eslesen skill/plugin/mcp/cli/klon/link yok", "ESLESME-YOK"

def main():
    t0 = time.time(); indeks(); yontem_oku()
    rows = list(csv.DictReader(open(V / "ana-liste.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))
    hedef = [r for r in rows if r["durum"] == "KURULU-KANITSIZ"]
    if "--dogrula" in sys.argv:
        N = int(sys.argv[sys.argv.index("--dogrula") + 1]); eski = {r["kalem"]: r for r in csv.DictReader(open(K / "tmp/kanit3_sonuc.tsv", encoding="utf-8", newline=""), delimiter="\t")}
        kanitlar = [r for r in eski.values() if r["sonuc"] == "KANIT"]; random.seed(7); ornek = random.sample(kanitlar, N)
        by = {r["kalem"]: r for r in rows}
        with ThreadPoolExecutor(6) as ex: yeni = list(ex.map(lambda e: coz(by[e["kalem"]]) if e["kalem"] in by else ("KANITSIZ",), ornek))
        ok = sum(1 for y in yeni if y[0] == "KANIT"); print(f"dogrulama: {ok}/{N} tekrarlandi (%{100*ok//N})")
        for e, y in zip(ornek, yeni):
            if y[0] != "KANIT": print("TEKRARLANMADI", e["kalem"], y)
        return
    with ThreadPoolExecutor(6) as ex: out = list(ex.map(coz, hedef))
    (K / "tmp").mkdir(exist_ok=True)
    with open(K / "tmp/kanit3_sonuc.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n"); w.writerow(["kalem", "sinif", "sonuc", "tur", "ayrinti", "neden_kodu"])
        for r, o in zip(hedef, out): w.writerow([r["kalem"], r["tur"], o[0], o[1], o[2], o[3]])
    print(len(hedef), "satir", round(time.time() - t0), "sn", collections.Counter(o[0] for o in out))
    print(collections.Counter(o[1] for o in out if o[0] == "KANIT")); print(collections.Counter(o[3] for o in out if o[0] != "KANIT"))
    if "--yaz" in sys.argv: yaz(rows, hedef, out)

def yaz(rows, hedef, out):
    ts = time.strftime("%m%d-%H%M")
    shutil.copy2(V / "ana-liste.tsv", V / f"ana-liste.tsv.yedek-kanit3-{ts}")
    shutil.copy2(V / "kurulu-kanit.tsv", V / f"kurulu-kanit.tsv.oncesi-kanit3-{ts}")
    res = {r["kalem"]: o for r, o in zip(hedef, out)}
    for r in rows:
        o = res.get(r["kalem"]) if r["durum"] == "KURULU-KANITSIZ" else None
        if not o: continue
        if o[0] == "KANIT": r["durum"] = "CALISIYOR"; r["neden_kanit"] = f"KANIT-3 {o[1]}: {o[2]}"
        else: r["durum"] = "KANITSIZ-" + o[3]; r["neden_kanit"] = "KANIT-3: " + o[2]
    with open(V / "ana-liste.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), delimiter="\t", lineterminator="\n"); w.writeheader(); w.writerows(rows)
    eski = list(csv.reader(open(V / "kurulu-kanit.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))
    yeni_k = {r["kalem"] for r in hedef}
    with open(V / "kurulu-kanit.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n"); w.writerow(eski[0])
        w.writerows(x for x in eski[1:] if x and x[0] not in yeni_k)
        for r, o in zip(hedef, out): w.writerow([r["kalem"], r["tur"], "KANIT3", o[0], o[1], o[2] if o[0] == "KANIT" else o[3] + ": " + o[2]])
    print("yazildi; yedekler", ts)

if __name__ == "__main__": main()
