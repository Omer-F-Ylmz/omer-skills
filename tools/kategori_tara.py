"""K36-GENISLET-1: NİHAİ 36(A) kategori 14-27 kaynak okuyucuları + seçim sıralaması.
  python tools/kategori_tara.py --sirala     # dizin.tsv + kart.jsonl -> .kos/kopru/kaynak-dizin/sirali.tsv + sirali-ozet.md
envanter_tara.py bu modülü içe alır: dosya_kaynaklari() (mtime önbellekli, artan) ve sistem_satirlari() (6 saatte bir).
Satır = (tür, ad, yol, özet, etiket); etiket 'kNN' ile başlar. GİZLİLİK: hesaplar yalnız ad, anahtar/şifre değeri okunmaz."""
import ctypes
import json
import math
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envanter_tara as E  # noqa: E402

KOK, MASA, DIZIN, ATLA, EL = E.KOK, E.MASA, E.DIZIN, E.ATLA, E.EL
KOPRU = KOK / ".kos" / "kopru"
OBS = MASA / "Obsidian"
GENEL = Path("C:/Projeler/omer-kurallar.md")
HESAPLAR = ("Figma Stitch claude-design 21st Miro Canva Higgsfield Vercel Netlify Supabase Cloudflare GitHub Sketchfab HuggingFace fal.ai Modal Apify "
            "Firecrawl Composio Oxylabs Telegram-botu Meta-Ads Google-Workspace Google-Drive OneDrive Notion Slack Linear Atlassian OpenAI-Codex Adobe "
            "Epic-Fab Unity Roblox claude.ai Tripo Meshy Brave OmniRoute Gemini Groq OpenRouter GitHub-Models").split()


def _satir(tur, ad, yol, ozet, etiket):
    return (tur, ad[:60], str(yol).replace(EL, "/"), re.sub(r"\s+", " ", str(ozet))[:110], etiket)


def _md(tur, etiket, kok=KOK, uzun=3000):
    def uret(f):
        try:
            t = f.read_text(encoding="utf-8", errors="replace")[:uzun]
        except OSError:
            return []
        try:
            yol = f.relative_to(kok)
        except ValueError:
            yol = f
        return [_satir(tur, f.stem, yol, E.ozet_md(t), etiket)]
    return uret


def _tsv(tur, etiket, ad_k, ozet_k, yol_on):
    def uret(f):
        out = []
        for s in f.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
            k = s.split("\t")
            if len(k) > max(ad_k, ozet_k) and k[ad_k].strip():
                out.append(_satir(tur, k[ad_k], f"{yol_on}:{k[ad_k]}", " · ".join(k[i] for i in ozet_k if i < len(k) and k[i]) if isinstance(ozet_k, tuple) else k[ozet_k], etiket))
        return out
    return uret


def _py(f):
    try:
        t = f.read_text(encoding="utf-8", errors="replace")[:900]
    except OSError:
        return []
    m = re.search(r'"""\s*(.+)', t) or re.search(r"^#\s*(.+)", t, re.M)
    return [_satir("betik", f.stem, f.relative_to(KOK), m.group(1) if m else "betik", "k15 betik " + f.parent.name)]


def _usta(f):
    out = []
    for s in f.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(s)
        except ValueError:
            continue
        ku = d.get("kullanim") or [""]
        out.append(_satir("kart", d.get("ad", "?"), "usta:" + d.get("ad", "?"), f"{ku[0][:60]} · kombin {', '.join(d.get('kombin') or [])[:40]}", "k16 usta-karti " + str(d.get("tur", ""))))
    return out


def _kombin(f):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError:
        return []
    return [_satir("kombin", k, f"kombin:{k}", json.dumps(v, ensure_ascii=False), "k16 kombin") for k, v in d.items()]


def _altin(f):
    out = []
    for s in f.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if isinstance(d, dict) and d.get("is"):
            out.append(_satir("altin", d["is"], f"altin:{f.stem}:{d['is']}", "seçim: " + ", ".join(d.get("secim") or [])[:100], "k16 altin-ornek"))
    return out


def _satirlar(etiket, tur, ad_oneki=""):
    """Satır satır belge (bekleyen-linkler, Kararlar, kurallar): başlık/madde/tablo satırı = 1 kayıt."""
    def uret(f):
        out = []
        for i, s in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = s.strip()
            if len(s) < 12 or s.startswith(("|---", "```", "---")):
                continue
            out.append(_satir(tur, ad_oneki + re.sub(r"^[#|\-*\s\d.]+", "", s)[:48], f"{f.name}#L{i}", s.strip("|#- "), etiket))
        return out
    return uret


def _suz(uret, rx):
    """Satır üreticisinin çıktısını özetinde rx geçenlere indirger."""
    return lambda f: [r[:2] + ("kalite:" + r[2],) + r[3:] for r in uret(f) if re.search(rx, r[3] + r[1], re.I)]


def _json_anahtar(etiket, tur):
    def uret(f):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except ValueError:
            return []
        return [_satir(tur, k, f"{f.name}:{k}", f"{f.name} kaydı", etiket) for k in (d if isinstance(d, dict) else [])]
    return uret


def dosya_kaynaklari():
    r = []
    ekle = lambda dosyalar, uret: r.extend((f, uret) for f in dosyalar if f.exists())
    vt = KOK / "docs/video-tarama"
    ekle([vt / "ana-liste.tsv"], lambda f: [_satir("liste", s[0], f"ana-liste:{s[0]}", f"{s[4]} · {s[1]} · {s[5][:50]} · {s[2]}", f"k14 ana-liste {s[1]} {s[4]}") for s in (l.split("\t") for l in f.read_text(encoding="utf-8", errors="replace").splitlines()[1:]) if len(s) > 5 and s[0]])
    ekle([vt / "ana-liste-ozellik.tsv"], _tsv("liste", "k14 ozellik", 0, 1, "ana-liste-ozellik"))
    ekle(sorted((vt / "yapilis").glob("*.md")), _md("liste", "k14 yapilis"))
    ekle(sorted((KOK / "tools").glob("*.py")) + sorted(KOPRU.glob("*.py")), _py)
    ekle([KOK / "docs/usta-kart/usta.jsonl"], _usta)
    ekle([KOK / "docs/katalog/yetenek.jsonl"], lambda f: [_satir("katalog", d["ad"], "katalog:" + d["ad"], d.get("metin", d.get("cagri", "")), "k1 katalog " + str(d.get("tur", ""))) for d in (json.loads(s) for s in f.read_text(encoding="utf-8", errors="replace").splitlines() if s.startswith("{")) if d.get("ad")])
    ekle([KOK / "docs/arac-kart/kombin.json"], _kombin)
    ekle(sorted((KOPRU / "altin-ornek").glob("*.jsonl")) + sorted((KOK / ".secim").rglob("*.jsonl")), _altin)
    for d, e in ((KOPRU / "rapor", "k17 rapor"), (KOK / "devir", "k17 devir"), (KOPRU / "devir", "k17 devir"), (KOPRU / "arka", "k17 arka")):
        ekle([f for f in sorted(d.rglob("*.md")) if "ucretsiz" not in f.name and not ATLA & set(f.parts) and "site-packages" not in f.parts][:900], _md("rapor", e))
    ekle(sorted(KOPRU.glob("rapor/*ucretsiz*.md")) + sorted(KOPRU.glob("rapor/hesapli*.md")) + sorted((KOK / "docs/kaynak-tarama").glob("*.md")), _md("kota", "k19 ucretsiz-kota arastirma"))
    ekle([KOPRU / "ucretsiz/envanter.tsv"], _tsv("kota", "k19 ucretsiz-havuz", 1, (0, 2, 3, 7, 8, 9), "ucretsiz-havuz"))
    ekle([KOPRU / "ucretsiz/modeller.json"], _json_anahtar("k19 ucretsiz-havuz saglayici", "kota"))
    ekle([vt / "bekleyen-linkler.md"], _satirlar("k24 istek-havuzu", "istek"))
    ekle(sorted((KOK / "docs").glob("*istek*.md")) + sorted((KOK / "docs").glob("*fikir*.md")) + sorted(OBS.rglob("fikir*.md")) + sorted(OBS.rglob("*istek*.md")), _md("istek", "k24 fikir-istek"))
    ekle([KOK / "docs/hesap-kuyrugu.md", KOK / "docs/claude-ai-baglayici.md"], _satirlar("k25 hesap-adi", "hesap"))
    k27, k23 = _satirlar("k27 karar-defteri", "karar"), _suz(_satirlar("k23 kalite-referans geri-bildirim", "kalite", "ölçek "), r"İLİK|ilik-v4|müthiş|puan ölçe|50.55|beğenmedi|reddet|geri bildirim")
    ekle([OBS / "10-kararlar/Kararlar.md", OBS / "10-kararlar/Kurallar.md", GENEL], lambda f: k27(f) + k23(f))  # aynı dosya iki üretici: önbellek anahtarı dosya olduğundan tek üretici
    ekle(sorted(OBS.glob("10-kararlar/*.md"))[:200] + sorted((KOK / "docs").glob("devir-*.md")), _md("karar", "k27 karar-devir", OBS))
    mem = Path.home() / ".claude/projects/C--Projeler-omer-skills/memory"
    ekle(sorted(mem.glob("*.md")), _md("kalite", "k23 k18 cc-hafiza geri-bildirim", mem))
    ekle(sorted((KOK / "docs/olcumler").glob("altin/*.md")), _md("kalite", "k23 kalite-referans"))
    ekle([KOK / "docs/claude-mem.md"], _md("gecmis", "k18 claude-mem"))
    ekle(sorted((KOK / "docs/tasarim").glob("*.md")), _md("tasarim", "k21 tasarim-sistemi"))
    return r


def _gorev_zamanlayici():
    out = []
    for s in E.calis(["schtasks", "/query", "/fo", "csv", "/nh"], 30).splitlines():
        k = s.strip('"').split('","')
        if k and "omer" in k[0].lower():
            out.append(_satir("betik", k[0].split("\\")[-1], "gorev:" + k[0], f"Görev Zamanlayıcı · {k[-1] if len(k) > 2 else ''}", "k15 gorev-zamanlayici"))
    return out


def _model_dosyalari():
    out = []
    ext = {".safetensors", ".gguf", ".ckpt", ".pth", ".pt", ".onnx", ".bin", ".sft"}
    ai = Path("C:/AI")
    if ai.exists():
        for p in sorted(ai.iterdir()):
            out.append(_satir("model", p.name, "model-agirlik:" + str(p), "C:\\AI klasörü", "k20 model-klasoru"))
    for kok in sorted(ai.glob("ComfyUI*/models")) if ai.exists() else []:
        for yol, dirs, files in os.walk(kok):
            dirs[:] = [d for d in dirs if d not in ATLA and not d.startswith(".")]
            for f in files:
                if Path(f).suffix.lower() in ext:
                    try:
                        gb = (Path(yol) / f).stat().st_size / 2 ** 30
                    except OSError:
                        continue
                    out.append(_satir("model", f, f"model-agirlik:{Path(yol) / f}", f"{Path(yol).name} · {gb:.2f} GB · {kok.parent.name}", "k20 model-agirligi " + Path(yol).name))
    hf = Path.home() / ".cache/huggingface/hub"
    for p in sorted(hf.glob("models--*")) if hf.exists() else []:
        out.append(_satir("model", p.name[8:], "model-agirlik:hf:" + p.name, "HF önbelleği", "k20 model-agirligi hf"))
    return out


def _tasarim_test():
    out = []
    kokler = [KOK] + ([p for p in MASA.iterdir() if p.is_dir() and p.name not in ATLA] if MASA.exists() else [])
    test_ad = re.compile(r"(\.spec\.|\.test\.|^test_|playwright\.config|(^|[-_.])(axe|zap|e2e)([-_.]|$)|gitleaks|semgrep)", re.I)
    for p in kokler:
        sayac = 0
        for yol, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in ATLA and not d.startswith(".") and d not in {"_arsiv", "tmp", "docs", "dist"}]
            if len(Path(yol).relative_to(p).parts) >= 4:
                dirs[:] = []
            for f in files:
                if f.upper().startswith("DESIGN") and f.lower().endswith(".md"):
                    out.append(_satir("tasarim", f"{p.name}/{f}", Path(yol) / f, E.ozet_md((Path(yol) / f).read_text(encoding="utf-8", errors="replace")[:2500]), "k21 DESIGN.md " + p.name))
                elif sayac < 12 and test_ad.search(f) and Path(f).suffix in {".py", ".ts", ".js", ".mjs", ".cs", ".toml", ".json", ".yml"}:
                    sayac += 1
                    out.append(_satir("test", f, Path(yol) / f, f"{p.name} test/kanıt düzeni", "k22 test-duzeni " + p.name))
    return out


def _donanim():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("y", ctypes.c_ulong)] + [(n, ctypes.c_ulonglong) for n in "tp ap tv av ex".split()]
    m = M()
    m.l = ctypes.sizeof(M)
    ram = ""
    try:
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        ram = f"RAM {m.tp / 2 ** 30:.0f} GB (yük %{m.y})"
    except Exception:
        pass
    gpu = E.calis(["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader"], 15).strip()
    du = shutil.disk_usage("C:/")
    d = "k26 donanim"
    return [_satir("donanim", "GPU", "donanim:gpu", gpu or "RTX 4070 Ti 12 GB (sm_89: INT8/FP8 var, NVFP4 yok)", d),
            _satir("donanim", "RAM", "donanim:ram", ram or "RAM 34 GB", d),
            _satir("donanim", "Disk C:", "donanim:disk", f"boş {du.free / 2 ** 30:.0f} GB / {du.total / 2 ** 30:.0f} GB (taban 30 GB)", d),
            _satir("donanim", "Tavanlar", "donanim:tavan", "VRAM ≤%80, RAM ≤%89, C: boş ≥30 GB (indirmede 60 GB hedef)", d)]


def _gecmis():
    out = []
    kok = Path.home() / ".claude/projects"
    for p in sorted(kok.iterdir()) if kok.exists() else []:
        if p.is_dir():
            js = list(p.glob("*.jsonl"))
            if js:
                son = time.strftime("%Y-%m-%d", time.localtime(max(f.stat().st_mtime for f in js)))
                out.append(_satir("gecmis", p.name.replace("C--", "")[:60], "cc-oturum:" + p.name, f"{len(js)} oturum transkripti · son {son}", "k18 cc-oturum"))
    return out


def _skill_dizinleri():
    """Kurulu skill dizinleri (repo skills/ + ~/.claude/skills): kart.jsonl'de olmayan dn-*/fe-* gibi aileler dahil."""
    out = []
    for kok in (KOK / "skills", Path.home() / ".claude/skills"):
        for p in sorted(kok.iterdir()) if kok.exists() else []:
            f = p / "SKILL.md"
            if f.exists():
                m = re.search(r"^description:\s*(.+)", f.read_text(encoding="utf-8", errors="replace")[:1500], re.M)
                out.append(_satir("skill", p.name, f"skill-dizin:{p.name}", m.group(1) if m else "skill", "k1 skill-dizini"))
    return out


def sistem_satirlari():
    out = []
    for f in (_skill_dizinleri, _gorev_zamanlayici, _model_dosyalari, _tasarim_test, _donanim, _gecmis):
        try:
            out += f()
        except Exception as e:  # tek kaynak düşse diğerleri girer
            out.append(_satir("hata", f.__name__, "tarama-hata:" + f.__name__, repr(e)[:100], "k0 tarama-hatasi"))
    out += [_satir("hesap", h, "hesap-adi:" + h, "hesap/bağlayıcı adı (kural 36(A)9; değer asla okunmaz)", "k25 hesap-adi") for h in HESAPLAR]
    return out


# ---- SIRALAMA: her kalem -> kategori no + iş türü etiketleri + kanıt + usta kartı + son kullanım -> seçim puanı ----
HARITA = {"site": {4, 5, 6, 14, 16, 21, 22, 23}, "gorsel-video-ses-3d": {9, 10, 14, 19, 20, 23, 26}, "kurulum": {1, 14, 15, 17, 20, 27},
          "kod": {1, 7, 15, 18, 22}, "otomasyon": {9, 13, 15, 19, 25}, "arastirma": {2, 3, 8, 14, 19}}
HER_ISTE = {12, 16, 17, 24, 27}
IS_TURU = {  # iş türü <- dizin satırındaki sözcükler (duz() sonrası)
    "site": r"site|web|landing|frontend|\bui\b|\bux\b|css|tasarim|design|react|next|tailwind|gsap|scroll|figma|sablon|bilesen|shader",
    "gorsel-video-ses-3d": r"video|gorsel|image|\bses\b|audio|3d|blender|render|animasyon|logo|ffmpeg|remotion|comfy|model-agirlik|tts|whisper|glb|comfyui|diffusion|flux",
    "kurulum": r"kurulum|install|setup|\bkur\b|npm|\bcli\b|pip |uygulama|eklenti",
    "kod": r"\bkod\b|\bapi\b|backend|dotnet|python|\btest|sql|\bgit\b|refactor|typescript|betik|semgrep|gitleaks",
    "otomasyon": r"otomasyon|\bbot\b|n8n|zapier|schedule|cron|sosyal|instagram|telegram|workflow|mcp|gorev",
    "arastirma": r"arastir|research|scrape|crawl|search|rapor|analiz|dokuman|paper|arxiv|kaynak|inceleme",
}
KAT_ETIKET = [("ucretsiz-havuz", 13), ("video yontem", 2), ("kaynak-kutuphane", 3), ("tasarim-katalog", 4), ("site inceleme", 4), ("site kart", 4), ("yer-imi", 4),
              ("sablon", 5), ("gecmis-proje", 6), ("2.beyin obsidian", 8), ("github repo", 9), ("claude code marketplace", 9), ("steam oyun", 10), ("epic oyun", 10)]
KAT_TUR = {"klon": 3, "sablon": 5, "proje": 6, "varlik": 6, "baglayici": 9, "mcp": 1, "uygulama": 10, "eklenti": 10, "arac": 10, "model": 20}
KAT_YONTEM = {"ders": 7, "mekanizma": 7, "uyarlama": 7, "roast": 7, "kutuphane": 7}
TOKEN = re.compile(r"[a-z0-9][a-z0-9._-]{3,}")
KANIT = re.compile(r"calisiyor|calisti|smoke|gecti|olculdu|kanit|bitti|kurulu\b|dogrulandi", re.I)


def kat_no(tur, etiket):
    m = re.match(r"k(\d+)", etiket)
    if m:
        return int(m.group(1))
    for k, n in KAT_ETIKET:
        if k in etiket:
            return n
    if tur == "yontem":
        return next((n for k, n in KAT_YONTEM.items() if etiket.startswith(k)), 7)
    return KAT_TUR.get(tur, 0)


def is_turleri(metin):
    d = E.duz(metin)
    return [t for t, rx in IS_TURU.items() if re.search(rx, d)]


def _tokenlar():
    """rapor/devir/arka metninden: kanıt satırı token'ları, her token'ın son anılma zamanı, altın seçim adları, usta kartı adları."""
    kanit, son = set(), {}
    for d in (KOPRU / "rapor", KOPRU / "devir", KOPRU / "arka", KOK / "devir"):
        for f in d.rglob("*.md") if d.exists() else []:
            mt = f.stat().st_mtime
            for s in f.read_text(encoding="utf-8", errors="replace").splitlines():
                tk = TOKEN.findall(E.duz(s))
                if tk and KANIT.search(E.duz(s)):
                    kanit.update(tk)
                for t in tk:
                    if son.get(t, 0) < mt:
                        son[t] = mt
    altin = set()
    for f in list((KOPRU / "altin-ornek").glob("*.jsonl")) + list((KOK / ".secim").rglob("*.jsonl")):
        for s in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                altin.update(E.duz(x) for x in (json.loads(s).get("secim") or []))
            except (ValueError, AttributeError):
                pass
    usta = set()
    for s in (KOK / "docs/usta-kart/usta.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            a = E.duz(json.loads(s).get("ad", ""))
        except ValueError:
            continue
        usta.update({a, a.split(":")[-1]})
    return kanit, son, altin, usta


def slug(ad):
    return re.sub(r"[^a-z0-9]+", "-", E.duz(ad)).strip("-")


def sirala():
    kanit, son, altin, usta = _tokenlar()
    liste = KOK / "docs/video-tarama/ana-liste.tsv"
    al_usta = set()
    for s in liste.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        k = s.split("\t")
        if len(k) > 6 and k[6].strip().lower() == "var":
            al_usta.add(slug(k[0]))
    kayit = [r.split("\t") for r in (DIZIN / "dizin.tsv").read_text(encoding="utf-8").splitlines()[1:] if r.count("\t") == 4]
    for s in (KOK / "docs/arac-kart/kart.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            d = json.loads(s)
        except ValueError:
            continue
        kayit.append([d.get("tur", "skill"), d.get("ad", "?"), "kart:" + d.get("ad", "?"), str(d.get("ne", ""))[:110], "k1 arac-karti"])
    simdi = time.time()
    out = []
    for tur, ad, yol, ozet, etiket in kayit:
        sl = slug(ad)
        a_kisa = E.duz(ad).split(":")[-1]
        cal = int(bool(re.match(r"(KURULU|CALISIYOR|ÇALIŞIYOR)", ozet)) or (sl in kanit and len(sl) >= 4))
        us = int(E.duz(ad) in usta or a_kisa in usta or sl in al_usta or tur == "kart")
        al = int(E.duz(ad) in altin or a_kisa in altin)
        mt = son.get(sl, 0)
        gun = (simdi - mt) / 86400 if mt else 999
        puan = 3 * cal + 2 * us + 3 * al + (2 if gun <= 7 else 1 if gun <= 30 else 0) + int(mt > 0)
        out.append((kat_no(tur, etiket), ",".join(is_turleri(f"{ad} {ozet} {etiket}")) or "-", cal, us, al, time.strftime("%Y-%m-%d", time.localtime(mt)) if mt else "", puan, tur, ad, yol, ozet))
    out.sort(key=lambda r: (r[0], -r[6], r[8].lower()))
    (DIZIN / "sirali.tsv").write_text("kat\tis_turu\tcalisiyor\tusta\taltin\tson_kullanim\tpuan\ttur\tad\tyol\n" + "\n".join("\t".join(str(x).replace("\t", " ") for x in r) for r in out) + "\n", encoding="utf-8")
    ozet = ["# Sıralı kaynak dizini (K36-GENISLET-1) — kategori başına özet", "", "kat · kalem · çalışıyor-kanıtlı · usta kartlı · altın · en yüksek 5 (puan)"]
    for k in range(0, 28):
        g = [r for r in out if r[0] == k]
        if g:
            ozet.append(f"- {k}: {len(g)} · {sum(r[2] for r in g)} · {sum(r[3] for r in g)} · {sum(r[4] for r in g)} · " + "; ".join(f"{r[8][:28]} ({r[6]})" for r in g[:5]))
    (DIZIN / "sirali-ozet.md").write_text("\n".join(ozet) + "\n", encoding="utf-8")
    return out


_SIRALI = {}


def bonus_fonksiyonu(is_):
    """kaynak_ara için: satır -> sıralama bonusu (seçim puanı + iş türünün SEÇİM HARİTASI kategorisinde olma)."""
    if not _SIRALI:
        p = DIZIN / "sirali.tsv"
        if p.exists():
            for s in p.read_text(encoding="utf-8").splitlines()[1:]:
                k = s.split("\t")
                if len(k) == 11:
                    _SIRALI[re.sub(r"^https?://(www\.)?|/$", "", k[9]).lower()] = (int(k[0]), int(k[6]))
    d = E.duz(is_)
    kat = set(HER_ISTE)
    for t, rx in IS_TURU.items():
        if re.search(rx, d):
            kat |= HARITA[t]

    def bonus(r):
        v = _SIRALI.get(re.sub(r"^https?://(www\.)?|/$", "", r[2]).lower())
        return 0 if not v else 0.2 * v[1] + (1.0 if v[0] in kat else 0)
    return bonus


KAT_AD = {1: "kurulu araç", 2: "video yöntem", 3: "kaynak-kütüphane/klon", 4: "site listesi", 5: "şablon", 6: "geçmiş proje", 7: "omer-skills arşiv", 8: "2. beyin",
          9: "hesap/bağlayıcı", 10: "uygulama", 12: "ölçüm", 13: "ücretsiz havuz", 14: "ana-liste", 15: "betik/hat", 16: "usta kartı/altın", 17: "rapor/devir", 18: "oturum geçmişi",
          19: "kota/araştırma", 20: "model ağırlığı", 21: "tasarım sistemi", 22: "test düzeni", 23: "kalite çıtası", 24: "istek havuzu", 25: "hesap adı", 26: "donanım", 27: "karar"}
DUR = {"icin", "yap", "bir", "ile", "yeni", "yaz", "uret"}
_SR = []


def _sr():
    if not _SR:
        for s in (DIZIN / "sirali.tsv").read_text(encoding="utf-8").splitlines()[1:]:
            k = s.split("	")
            if len(k) == 11:
                _SR.append((int(k[0]), k[1], int(k[2]), int(k[3]), int(k[4]), int(k[6]), k[8], E.duz(f"{k[8]} {k[10]} {k[9]}"), E.duz(k[8])))
    return _SR


def kok_sozcukler(is_):
    w = [x for x in E.kelimeler(is_) if x not in DUR]
    for k, ek in E.SINONIM.items():  # kaynak_ara ile aynı iş türü genişletmesi
        if any(x.startswith(k) for x in w):
            w += [e for e in ek.split() if e not in w]
    return [(x[:5] if len(x) > 6 else x) for x in w]


def kategori_siralama(is_, n_harita=2, n_diger=1):
    """İş için kategori başına en ilgili kalemler: ilgi = sorgu kökü eşleşmesi (ad ×2) + seçim puanı·0.3. {kat: (toplam, kanıtlı, [(skor, ad)])}"""
    w = kok_sozcukler(is_)
    d = E.duz(is_)
    harita = set(HER_ISTE)
    for t, rx in IS_TURU.items():
        if re.search(rx, d):
            harita |= HARITA[t]
    sr = _sr()
    agirlik = {x: math.log(1 + len(sr) / (sum(1 for r in sr if x in r[7]) or 1)) for x in w}  # IDF: nadir sözcük ağır
    sonuc = {}
    for k, it, cal, us, al, puan, ad, metin, adk in sr:
        if k <= 0:
            continue
        s = sonuc.setdefault(k, [0, 0, []])
        s[0] += 1
        s[1] += cal or us or al
        z = sum(agirlik[x] * (2 if x in adk else 1) for x in w if x in metin)
        if z and not re.fullmatch(r"[\w-]{11}", ad):
            s[2].append((z + 0.3 * puan, ad))
    cikti = {}
    for k, (n, kan, l) in sonuc.items():
        l.sort(key=lambda x: -x[0])
        gor, uniq = set(), []
        for z, ad in l:
            if ad.lower() not in gor:
                gor.add(ad.lower())
                uniq.append((z, ad))
        cikti[k] = (n, kan, uniq[:(n_harita if k in harita else n_diger)], k in harita)
    return cikti


def kategori_ozeti(is_):
    """birlestir() için: SEÇİM HARİTASI kategorileri önce (3'er kalem), kalan kategoriler 1'er kalem; hiçbir kategori eksik kalmaz."""
    c = kategori_siralama(is_)
    sat = [f"## kategori haritası (NİHAİ 36: {len(c)} kategori; haritadakiler önce) — tam sıra: .kos/kopru/kaynak-dizin/sirali.tsv"]
    for h in (True, False):
        for k in sorted(c):
            n, kan, l, hm = c[k]
            if hm == h:
                sat.append(f"k{k} {KAT_AD.get(k, '')} ({n}/{kan}✓): " + (" · ".join(a[:26] for _, a in l) if l else "eşleşme yok"))
    return sat


if __name__ == "__main__":
    if "--sirala" in sys.argv:
        o = sirala()
        print(len(o), "kalem sıralandı")
