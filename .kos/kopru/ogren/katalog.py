"""ÖĞREN-0: kurulu/indirilmiş her kalemin mekanik kataloğu (LLM okuması yok).
  python katalog.py            -> katalog.jsonl + ozet.md (bu klasöre)
  python katalog.py --cli-yok  -> CLI sürüm yoklaması atlanır
Ortam değişkeni / MCP env değeri hiçbir yerde okunmaz ya da yazılmaz."""
import csv, hashlib, json, os, re, shutil, subprocess, sys, zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
EV = Path.home()
REPO = Path(__file__).resolve().parents[3]
PROJELER = REPO.parent
ATLA = {".git", "node_modules", ".venv", "venv", "__pycache__", ".next", "dist", "build", "target"}

KATEGORI = [  # sıra = eşitlikte öncelik; kısa sözcükler \b ile
    ("3d", r"\b3d\b|blender|three\.?js|\bmesh|\bglb\b|gltf|\br3f\b|webgl|shader"),
    ("oyun-mod", r"\bgame|\boyun|\bmods?\b|minecraft|unity|godot|roblox|unreal"),
    ("güvenlik", r"secur|güvenlik|vulnerab|pentest|owasp|\bsecret|semgrep|\bcve|exploit|malware|zafiyet"),
    ("token", r"\btoken|context window|bağlam|sıkıştır|compress|headroom|\brtk\b|\bcache|önbellek|jeton"),
    ("video-medya", r"video|youtube|\baudio|\bses\b|\bimage|görsel|ffmpeg|\bgif|\bmedia|music|podcast|transcri|remotion|\bfoto|\btts\b|speech"),
    ("backend-dotnet", r"dotnet|\.net\b|\bc#|csharp|asp\.?net|backend|\bapi\b|ef core|\bserver\b|sunucu|azure"),
    ("veri-db", r"database|\bsql|postgres|\bdb\b|\bveri\b|\bdata\b|sqlite|mongo|supabase|analytics|\bcsv\b|excel"),
    ("test-qa", r"\btest|\bqa\b|playwright|\be2e\b|\btdd\b|\blint|coverage|assert|kalite"),
    ("pazarlama", r"marketing|pazarlama|\bseo\b|\bsales|\bads\b|\bbrand|social|linkedin|\bemail|campaign|growth|instagram"),
    ("bilim", r"scien|bilim|\bmath|biolog|chemi|physic|\bpaper|bioinf|statistic|genom|protein"),
    ("frontend-tasarım", r"frontend|\bui\b|\bux\b|\bcss|tailwind|design|tasarım|react|component|animat|gsap|typograph|\bfont|figma|landing|\bsite\b|\bweb"),
    ("belge", r"\bdocs?\b|\bpdf|docx|pptx|xlsx|belge|rapor|report|markdown|slide|sunum|\bwrit|yazı"),
    ("araştırma", r"research|araştır|search|arama|scrap|crawl|\bfetch|brows"),
    ("ajan-orkestrasyon", r"\bagent|\bajan|subagent|orchestr|workflow|\bmcp\b|plugin|\bskill|\bhook|claude|prompt|\bllm|swarm"),
]
KAT_RE = [(k, re.compile(p, re.I)) for k, p in KATEGORI]


def kategori(metin):
    puan = [(len(r.findall(metin)), -i, k) for i, (k, r) in enumerate(KAT_RE)]
    best = max(puan)
    return best[2] if best[0] else "diğer"


def tek_satir(s, n=200):
    return re.sub(r"\s+", " ", s or "").strip()[:n]


def frontmatter(metin):
    """name/description: --- bloğundan mekanik; yoksa ilk düz cümle."""
    ad = acik = ""
    m = re.match(r"^﻿?---\s*\n(.*?)\n---", metin, re.S)
    if m:
        satirlar = m.group(1).splitlines()
        for i, s in enumerate(satirlar):
            if s.startswith("name:"):
                ad = s[5:].strip().strip("'\"")
            elif s.startswith("description:"):
                v = s[12:].strip()
                if v in ("|", ">", "|-", ">-", ""):  # çok satırlı blok
                    v = " ".join(x.strip() for x in satirlar[i + 1:] if x.startswith((" ", "\t")))
                acik = v.strip("'\"")
        govde = metin[m.end():]
    else:
        govde = metin
    return ad, tek_satir(acik) or ilk_cumle(govde)


def ilk_cumle(metin):
    for s in metin.splitlines():
        s = s.strip()
        if not s or s.startswith(("#", "<", "!", "[!", "|", "```", "---", ">")):
            continue
        return tek_satir(re.split(r"(?<=[.!?])\s", s)[0])
    return ""


def readme_baslik(metin):
    for s in metin.splitlines():
        if s.startswith("# "):
            return tek_satir(s[2:], 120)
    return ""


def oku(p):
    try:
        b = p.read_bytes()
    except OSError:
        return None
    return b


def kalem(tur, kaynak, yol, ad, acik="", veri=None, **ek):
    d = {"ad": ad, "tur": tur, "kaynak": kaynak, "yol": str(yol), "aciklama": tek_satir(acik),
         "satir": 0, "bayt": 0, "token_tahmin": 0, "_sha": ""}
    if veri is not None:
        d["satir"] = veri.count(b"\n") + 1
        d["bayt"] = len(veri)
        d["token_tahmin"] = round(len(veri) / 3.5)
        d["_sha"] = hashlib.sha1(veri.replace(b"\r\n", b"\n")).hexdigest()[:8]
    d.update(ek)
    return d


def md_kalem(tur, kaynak, p, varsayilan_ad):
    veri = oku(p)
    if veri is None:
        return None
    ad, acik = frontmatter(veri.decode("utf-8", "replace"))
    return kalem(tur, kaynak, p, ad or varsayilan_ad, acik, veri)


# ---------- toplayıcılar ----------
def skill_klasoru(kok, kaynak, tur="skill"):
    out = []
    if not kok.is_dir():
        return out
    for d in sorted(kok.iterdir()):
        sk = d / "SKILL.md"
        if sk.is_file():
            k = md_kalem(tur, kaynak, sk, d.name)
            k and out.append(k)
    return out


def md_klasoru(kok, kaynak, tur):
    if not kok.is_dir():
        return []
    return [k for p in sorted(kok.rglob("*.md")) if (k := md_kalem(tur, kaynak, p, p.stem))]


def hook_json(p, kaynak):
    out = []
    try:
        h = json.loads(p.read_text(encoding="utf-8")).get("hooks", {})
    except (OSError, ValueError, AttributeError):
        return out
    for olay, liste in h.items():
        for grup in liste or []:
            for hk in grup.get("hooks", []):
                komut = hk.get("command", "") or hk.get("type", "")
                # yalnız yürütücü + betik adı: diğer argümanlarda gizli değer olabilir
                kisa = " ".join(Path(x.strip("'\"")).name for x in komut.split()[:3]
                                if x is komut.split()[0] or re.search(r"\.(py|m?js|cjs|ps1|sh|ts)['\"]?$", x))
                out.append(kalem("hook", kaynak, p, f"{olay}:{grup.get('matcher', '*')}", kisa))
    return out


def mcp_sozluk(sunucular, kaynak, yol):
    out = []
    for ad, cfg in (sunucular or {}).items():
        komut = cfg.get("command") or cfg.get("url") or cfg.get("type", "")
        if cfg.get("url"):
            komut = re.sub(r"[?#].*", "", komut)  # sorgu dizgesinde anahtar olabilir
        else:
            komut = Path(komut).name
        out.append(kalem("mcp", kaynak, yol, ad, komut))
    return out


def plugin_topla(ev):
    out = []
    kayit = ev / ".claude/plugins/installed_plugins.json"
    try:
        eklentiler = json.loads(kayit.read_text(encoding="utf-8"))["plugins"]
    except (OSError, ValueError, KeyError):
        return out
    for anahtar, kurulumlar in sorted(eklentiler.items()):
        for kur in kurulumlar[:1]:
            kok = Path(kur["installPath"])
            src = f"plugin:{anahtar}"
            pj = next((p for p in (kok / ".claude-plugin/plugin.json", kok / "plugin.json") if p.is_file()), None)
            acik, veri = "", None
            if pj:
                veri = oku(pj)
                try:
                    acik = json.loads(veri).get("description", "")
                except ValueError:
                    pass
            out.append(kalem("plugin", "plugins", kok, anahtar.split("@")[0], acik, veri))
            out += skill_klasoru(kok / "skills", src)
            out += md_klasoru(kok / "commands", src, "komut")
            out += md_klasoru(kok / "agents", src, "agent")
            out += hook_json(kok / "hooks/hooks.json", src)
            mj = kok / ".mcp.json"
            if mj.is_file():
                try:
                    j = json.loads(mj.read_text(encoding="utf-8"))
                    out += mcp_sozluk(j.get("mcpServers", j), src, mj)
                except ValueError:
                    pass
    return out


def cc_topla(ev):
    c = ev / ".claude"
    out = skill_klasoru(c / "skills", "cc-skills")
    out += md_klasoru(c / "agents", "cc-agents", "agent")
    out += md_klasoru(c / "commands", "cc-commands", "komut")
    if (c / "hooks").is_dir():
        out += [kalem("hook", "cc-hooks", p, p.name, "", oku(p)) for p in sorted((c / "hooks").iterdir()) if p.is_file()]
    out += hook_json(c / "settings.json", "cc-settings")
    out += plugin_topla(ev)
    # claude.ai senkron kopyaları (CC'de /skill bunlara çözülür)
    for sk in sorted((c / "plugins/synced").rglob("SKILL.md")) if (c / "plugins/synced").is_dir() else []:
        k = md_kalem("skill", "claude.ai-synced", sk, sk.parent.name)
        k and out.append(k)
    try:
        cj = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
        out += mcp_sozluk(cj.get("mcpServers"), "cc-user-mcp", ev / ".claude.json")
        for proj, pv in cj.get("projects", {}).items():
            out += mcp_sozluk(pv.get("mcpServers"), f"cc-proje-mcp:{Path(proj).name}", ev / ".claude.json")
    except (OSError, ValueError):
        pass
    return out


def repo_topla(repo):
    out = skill_klasoru(repo / "skills", "omer-skills")
    for p in sorted((repo / "tools").iterdir()) if (repo / "tools").is_dir() else []:
        if p.name in ATLA:
            continue
        ana = p if p.is_file() else next((p / n for n in ("README.md", "SKILL.md", "main.py", "__init__.py") if (p / n).is_file()), None)
        veri = oku(ana) if ana else None
        acik = ""
        if veri is not None:
            m = re.search(rb'^\s*(?:"""|#|//)\s*(.+)', veri, re.M)
            acik = m.group(1).decode("utf-8", "replace") if m else ""
        out.append(kalem("cli", "omer-skills/tools", p, p.stem if p.is_file() else p.name, acik, veri))
    # dist zipleri: zip içindeki her SKILL.md ayrı satır
    for z in sorted((repo / "dist").glob("*/*.zip")):
        try:
            with zipfile.ZipFile(z) as zf:
                for n in zf.namelist():
                    if n.endswith("SKILL.md"):
                        veri = zf.read(n)
                        ad, acik = frontmatter(veri.decode("utf-8", "replace"))
                        parca = n.split("/")
                        out.append(kalem("skill", f"dist:{z.parent.name}", f"{z}!{n}",
                                         ad or (parca[-2] if len(parca) > 1 else z.stem), acik, veri, paket=z.stem))
        except (zipfile.BadZipFile, OSError):
            pass
    return out


def claudeai_topla(repo, gorulen):
    """claudeai_adlar.json: claude.ai'ye yüklü adlar; dist/synced'te zaten satırı olmayanlar ad-yalnız satır."""
    out = []
    try:
        j = json.loads((repo / ".kos/kopru/claudeai_adlar.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    for alan in ("giris", "paket_uyesi"):
        for ad in j.get(alan, []):
            if norm(ad) not in gorulen:
                gorulen.add(norm(ad))
                out.append(kalem("skill", f"claude.ai-kayit:{alan}", ".kos/kopru/claudeai_adlar.json", ad))
    return out


def dizin_olc(kok, tavan=200_000):
    dosya = bayt = 0
    for yol, dirs, files in os.walk(kok):
        dirs[:] = [d for d in dirs if d not in ATLA]
        for f in files:
            try:
                bayt += os.path.getsize(os.path.join(yol, f))
            except OSError:
                pass
            dosya += 1
        if dosya > tavan:  # shortcut: dev ağaçta sayım kesilir, gerekirse tavanı yükselt
            break
    return dosya, bayt


def klon_kalemi(d, kaynak):
    readme = next((d / n for n in ("README.md", "readme.md", "README.MD", "README") if (d / n).is_file()), None)
    lisans = next((p.name for p in d.iterdir() if p.is_file() and re.match(r"(licen[cs]e|copying)", p.name, re.I)), "")
    veri = oku(readme) if readme else None
    metin = veri.decode("utf-8", "replace") if veri else ""
    dosya, bayt = dizin_olc(d)
    acik = " · ".join(x for x in (readme_baslik(metin), ilk_cumle(metin)) if x)
    k = kalem("repo", kaynak, d, d.name, acik, veri, lisans=lisans, dosya=dosya, dizin_bayt=bayt)
    return k


def klonlar_topla(projeler, repo):
    out = []
    for ust in sorted(projeler.iterdir()):
        if not ust.is_dir() or ust.name.startswith("omer-skills"):
            continue
        if ust.name.startswith(".tmp") or ust.name in ("dis", "uygulamalar"):
            alt = [d for d in sorted(ust.iterdir()) if d.is_dir()]
            out += [klon_kalemi(d, f"indirme:{ust.name}") for d in alt]
        else:
            out.append(klon_kalemi(ust, "projeler"))
    # raf: omer-kutuphaneler tablosundaki kütüphaneler
    sk = repo / "skills/omer-kutuphaneler/SKILL.md"
    if sk.is_file():
        bolum = ""
        for s in sk.read_text(encoding="utf-8").splitlines():
            if s.startswith("## "):
                bolum = s[3:].strip()
            m = re.match(r"\|\s*\**([^|*]+?)\**\s*\|\s*([^|]+)\|", s)
            if m and bolum.startswith("Kütüphane") and not set(m.group(1)) <= set("-: ") and m.group(1) != "kütüphane":
                out.append(kalem("repo", "raf:omer-kutuphaneler", sk, m.group(1).strip(), m.group(2)))
    return out


def cli_topla(repo, yokla=True):
    adlar = {"ollama", "yt-dlp", "tesseract", "magick", "blender", "comfyui", "ffprobe", "ffmpeg", "git", "gh",
             "node", "npm", "python", "uv", "dotnet", "rtk", "graphify", "jev", "headroom", "claude", "docker",
             "playwright", "bun", "pnpm", "semgrep", "whisper"}
    try:
        izinli = json.loads((repo / "tools/cc-kopru/kopru.json").read_text(encoding="utf-8")).get("izinli", {})
        adlar |= {a for a in izinli if not a.startswith("_")}  # _not* açıklama anahtarı
    except (OSError, ValueError):
        pass
    out = []
    for ad in sorted(adlar):
        yol = shutil.which(ad)
        if not yol:
            out.append(kalem("cli", "cli:yok", "", ad, "PATH'te yok"))
            continue
        surum = ""
        if yokla:
            arg = ["-b", "--version"] if ad == "blender" else (["-version"] if ad.startswith("ff") else ["--version"])
            try:
                r = subprocess.run([yol, *arg], capture_output=True, text=True, timeout=20, encoding="utf-8",
                                   errors="replace", stdin=subprocess.DEVNULL,
                                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                surum = next((s for s in (r.stdout + r.stderr).splitlines() if s.strip()), "")
            except (OSError, subprocess.TimeoutExpired):
                surum = "sürüm alınamadı"
        out.append(kalem("cli", "cli:path", yol, ad, surum))
    return out


def model_topla(json_yol):
    try:
        modeller = json.loads(Path(json_yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for m in modeller:
        cap = m.get("capabilities") or {}
        yet = ["metin"] + (["görsel"] if cap.get("vision") else []) + \
              (["ses"] if re.search(r"audio|whisper|tts|speech|omni", m["id"], re.I) else [])
        acik = f"{m.get('owned_by')} · {'+'.join(yet)} · ctx {m.get('context_length')}" + (" · :free" if ":free" in m["id"] else "")
        out.append(kalem("model", f"omniroute:{m.get('owned_by')}", json_yol, m["id"], acik,
                         saglayici=m.get("owned_by"), yetenek=yet, free=":free" in m["id"]))
    return out


def desktop_topla(cfg):
    try:
        j = json.loads(Path(cfg).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return mcp_sozluk(j.get("mcpServers"), "desktop-mcp", cfg)


def video_topla(repo):
    out = []
    ad_dir = repo / "docs/kurulumlar/adaylar"
    if ad_dir.is_dir():
        out += [k for p in sorted(ad_dir.glob("*.md")) if (k := md_kalem("aday", "video:adaylar", p, p.stem))]
    tsv = repo / "docs/kurulumlar/kacan-karar.tsv"
    if tsv.is_file():
        son = {}
        with tsv.open(encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                son[r["terim"]] = r["karar"]
        for terim, karar in sorted(son.items()):
            if karar != "kapat":  # kapat = genel terim; yalnız ozet sayımına girer
                out.append(kalem("aday", "video:kacan-karar", tsv, terim, f"karar={karar}"))
        out.append({"_kapat": sum(1 for v in son.values() if v == "kapat")})
    return out


# ---------- birleştirme ----------
def norm(ad):
    return re.sub(r"(-claudeai|-claude-ai)$", "", (ad or "").strip().lower())


def grup_anahtar(k):
    # hook adı olay:matcher'dır; aynı olay farklı betik kopya sayılmaz
    return k["tur"], norm(k["ad"]) + ("|" + k["aciklama"] if k["tur"] == "hook" else "")


def zenginlestir(kalemler, atlas_adlar):
    sha_say = Counter(k["_sha"] for k in kalemler if k["_sha"])
    ad_kay = defaultdict(set)
    for k in kalemler:
        ad_kay[grup_anahtar(k)].add(k["kaynak"])
    for i, k in enumerate(kalemler, 1):
        k["id"] = f"k{i:05d}"
        k["atlasta"] = norm(k["ad"]) in atlas_adlar
        if k["_sha"] and sha_say[k["_sha"]] > 1:
            k["kopya_grubu"] = f"h:{k['_sha']}"
        elif len(ad_kay[grup_anahtar(k)]) > 1:
            k["kopya_grubu"] = f"ad:{norm(k['ad'])}"
        else:
            k["kopya_grubu"] = ""
        # model: yalnız id; kaynak hiç girmez ("video:", "plugin:" önekleri sınıfı bozuyordu)
        k["kategori_tahmin"] = kategori(k["ad"] if k["tur"] == "model" else f"{k['ad']} {k['aciklama']}")
    return kalemler


def topla(ev, repo, projeler, omni_json, desktop_cfg, cli=True):
    kalemler = cc_topla(ev) + repo_topla(repo)
    gorulen = {norm(k["ad"]) for k in kalemler if k["tur"] == "skill"}
    kalemler += claudeai_topla(repo, gorulen)
    kalemler += klonlar_topla(projeler, repo) if projeler.is_dir() else []
    kalemler += cli_topla(repo, cli)
    kalemler += model_topla(omni_json) + desktop_topla(desktop_cfg)
    for pj in sorted(projeler.glob("*/.mcp.json")) + sorted(projeler.glob("*/*/.mcp.json")):
        try:
            j = json.loads(pj.read_text(encoding="utf-8"))
            kalemler += mcp_sozluk(j.get("mcpServers", {}), f"proje-mcp:{pj.parent.name}", pj)
        except (OSError, ValueError):
            pass
    kalemler += video_topla(repo)
    kapat = sum(k.pop("_kapat") for k in kalemler if "_kapat" in k)
    kalemler = [k for k in kalemler if "ad" in k]
    atlas = set()
    kart = repo / "docs/atlas/kart.jsonl"
    if kart.is_file():
        atlas = {norm(json.loads(s).get("ad")) for s in kart.read_text(encoding="utf-8").splitlines() if s.strip()}
    return zenginlestir(kalemler, atlas), kapat


ALAN_SIRA = ["id", "ad", "tur", "kaynak", "yol", "aciklama", "satir", "bayt", "token_tahmin", "atlasta",
             "kopya_grubu", "kategori_tahmin"]


def yaz_jsonl(kalemler, p):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for k in kalemler:
            d = {a: k[a] for a in ALAN_SIRA}
            d.update({a: v for a, v in k.items() if a not in d and not a.startswith("_")})
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def ozet(kalemler, kapat):
    """ozet.md metni (≤60 satır)."""
    kurulu = [k for k in kalemler if k["tur"] not in ("aday", "model") and k["kaynak"] != "cli:yok"]
    turler = sorted({k["tur"] for k in kalemler})
    kat = [x for x, _ in KATEGORI] + ["diğer"]
    tk = Counter((k["tur"], k["kategori_tahmin"]) for k in kalemler)
    L = ["# ÖĞREN-0 katalog özeti (mekanik; LLM okuması 0)", "",
         f"Toplam {len(kalemler)} kalem · kurulu/indirilmiş {len(kurulu)} · aday {sum(k['tur']=='aday' for k in kalemler)}"
         f" (+{kapat} 'kapat' genel terim, satıra alınmadı) · model {sum(k['tur']=='model' for k in kalemler)}",
         f"Toplam token tahmini (ana dosya bayt/3.5): tümü {sum(k['token_tahmin'] for k in kalemler):,} · kurulu {sum(k['token_tahmin'] for k in kurulu):,}",
         f"Atlasta OLMAYAN kurulu kalem: {sum(not k['atlasta'] for k in kurulu)} / {len(kurulu)}", "",
         "## Tür × kategori", "| tür | " + " | ".join(t for t in turler) + " |", "|---" * (len(turler) + 1) + "|"]
    for c in kat:
        L.append(f"| {c} | " + " | ".join(str(tk[(t, c)] or "") for t in turler) + " |")
    L.append("| **toplam** | " + " | ".join(str(sum(k['tur'] == t for k in kalemler)) for t in turler) + " |")
    gruplar = Counter(k["kopya_grubu"] for k in kalemler if k["kopya_grubu"])
    tekil = {}
    for k in kurulu:  # kopyalar bir kez sayılır
        tekil.setdefault(k["kopya_grubu"] or k["id"], k)
    L += ["", f"## Kopya grupları: {len(gruplar)} grup, {sum(gruplar.values())} satır · tekil kurulu {len(tekil)}",
          "En kalabalık: " + ", ".join(f"{g}×{n}" for g, n in gruplar.most_common(8)), "",
          "## En büyük 20 kalem (token_tahmin; kopyalar tek)"]
    buyuk = [f"{k['token_tahmin']:,} {k['tur']} {k['ad']} ({k['kaynak']})"
             for k in sorted(tekil.values(), key=lambda k: -k["token_tahmin"])[:20]]
    L += ["- " + " · ".join(buyuk[i:i + 2]) for i in range(0, 20, 2)]
    okuma = Counter()
    adet = Counter()
    for k in tekil.values():
        okuma[k["kategori_tahmin"]] += k["token_tahmin"]
        adet[k["kategori_tahmin"]] += 1
    L += ["", "## ÖĞREN-1..N önerilen sıra (token önce — Ömer isteği; sonra tekil kurulu kalem sayısı)"]
    oncelik = ["token"] + sorted((c for c in kat if c != "token"), key=lambda c: (c == "diğer", -adet[c]))
    for i, c in enumerate(oncelik, 1):
        L.append(f"{i}. {c} — {adet[c]} kalem · ~{okuma[c]:,} token")
    return "\n".join(L[:60]) + "\n"


def main():
    burasi = Path(__file__).resolve().parent
    kalemler, kapat = topla(EV, REPO, PROJELER, REPO / ".kos/kopru/envanter/omni_models_api.json",
                            EV / "AppData/Roaming/Claude/claude_desktop_config.json", cli="--cli-yok" not in sys.argv)
    yaz_jsonl(kalemler, burasi / "katalog.jsonl")
    (burasi / "ozet.md").write_bytes(ozet(kalemler, kapat).encode("utf-8"))
    c = Counter(k["tur"] for k in kalemler)
    print(len(kalemler), dict(c))


if __name__ == "__main__":
    main()
