"""KATEGORI-KAPSAM adim 2-3: docs/envanter/kapsam-ek.tsv satirlarini 23+1 kategoriye ayirir
(ad-onceligi kurallari -> aciklama metni -> kategori_sinifla.siniflandir) -> docs/envanter/kapsam-kategori.tsv
ve kategori.tsv'de OLMAYAN adlari ona EKLER (silme yok, tekrar yok). Denetim -> .kos/kopru/arka/kategori-kapsam-denetim.json
  python tools/kapsam_sinifla.py [--kuru] [--yeniden]   (--yeniden: onceki 'kapsam:' satirlarini kategori.tsv'den cikarip yeniden ekler)"""
import csv
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import kategori_sinifla as S  # noqa: E402

csv.field_size_limit(10**9)
EK = KOK / "docs/envanter/kapsam-ek.tsv"
KAT = KOK / "docs/envanter/kategori.tsv"
KAPSAM_KAT = KOK / "docs/envanter/kapsam-kategori.tsv"
DENETIM = KOK / ".kos/kopru/arka/kategori-kapsam-denetim.json"
BASLIK = ["ad", "tur", "yol", "birincil", "ikincil", "cok_yonlu", "guven", "yontem", "gerekce"]
TUR_ESLE = {"skill": "skill", "ajan": "ajan", "plugin": "plugin", "mcp": "mcp", "claude-ai-baglayici": "baglayici",
            "uygulama-windows": "uygulama", "uygulama-kurulum": "uygulama", "uygulama-kisayol": "uygulama", "cli": "cli",
            "uv-arac": "cli", "model-ollama": "model", "model-hf": "model", "comfyui-eklenti": "eklenti",
            "editor-eklenti": "eklenti", "chrome-eklenti": "eklenti", "blender-eklenti": "eklenti", "npm-paket": "cli",
            "pip-paket": "kalem", "repo": "klon", "plugin-pazaryeri": "plugin", "kanca": "betik", "komut": "betik",
            "betik": "betik", "skill-zip": "skill"}
ONEK = re.compile(r"^(?:davila7|elainesmithburkel-code|elainesmithburkel|jk|y23|nousresearch|garrytan|mukul975|ootto|hkuds|baoyu|"
                  r"calesthio|agricidaniel|czlonkowski|nateherkai|paperclipai|anthropics|anthropic-skills|cli-anything|cloudai-x|"
                  r"dsh|openclaw|pbakaus|thesmokedev|xbtlin|emilkowalski|nextlevelbuilder|jimliu|digitalsamba|trycompai|"
                  r"vercel-labs|ecc|octo|sepia)[-:]+", re.I)
# ad-tabanli oncelik kurallari (ilk eslesen kazanir)
ONCELIK = [
    ("guvenlik", r"ssl|crypt|bandit|minisign|gitleaks|semgrep|secret|jwt|oauth|vuln|pentest|fullscan|\bhunt|truststore|certifi|keyring|owasp|exploit|malware|forensic|red.?team|sast|competition-|h-mmer|security"),
    ("3d-blender", r"blender|\b3d\b|threejs|three-js|gltf|hunyuan3d|trellis"),
    ("video", r"video|openscreen|caption|subtitle|ffmpeg|\breel|remotion|hyperframes|motion|animasyon|youtube|\byt-|\bclip|podcast"),
    ("backend-dotnet", r"\.net|dotnet|csharp|aspnet|ef.?core|nuget"),
    ("belge", r"acrobat|\bpdf|docx|pptx|xlsx|writing|prose|humaniz|slides|markdown|readme"),
    ("is-finans-hukuk", r"payment|invoice|\bhr\b|hr-|thesis|financ|legal|contract|accounting|\btax|salary|recruit|hiring|crm|sales|stripe"),
    ("pazarlama-reklam", r"marketing|brand|\bseo|\bads?\b|content-plan|next-content|campaign|social|copywrit|newsletter|geo-|-global$"),
    ("bulut-devops", r"\bcdk\b|terraform|cloud|docker|kubern|\bk8s|helm|\baws\b|azure|gcp|ci-cd|devops|vercel|netlify|railway|render-"),
    ("veri-db", r"database|\bdb\b|dbos|\bsql|postgres|mysql|redis|mongo|duckdb|\betl\b|dataset|pandas|polars"),
    ("ml-ai", r"umap|torch|sklearn|scikit|transformers|embedding|\bllm\b|diffusion|onnx|tensorflow|huggingface|\bgguf|ollama"),
    ("frontend-ui", r"design.?md|design-system|\bui-|-ui\b|\bcss\b|tailwind|react|\bvue\b|svelte|frontend|animation-performance|interface|better-(?:ui|layout|colors|typography|interface)"),
    ("arastirma", r"research|learn-codebase|literature|arxiv|scholar|wiki|knowledge|search"),
    ("test-qa", r"hypothesis|pytest|\btest|reproduce|\bqa\b|coverage|playwright|cypress|selenium"),
    ("verimlilik", r"thrifty|token|context|memory|\bcost|budget|productivity|chief-of-staff|todo"),
    ("ajan-arac", r"ajan-getir|\bmcp\b|\bagent|plugin|paket$"),
    ("surec-plan", r"plan|roadmap|\bspec\b|\bprd\b|requirements|decision|gsd"),
    ("diger-genel", r"^yarn|pyinstaller|windows sdk|\bsdk\b|redistributable|runtime|visual c\+\+|driver|updater|installer|git for windows|node\.?js|\bnpm\b|\bpip\b|setuptools|wheel"),
]
ONCELIK = [(k, re.compile(v, re.I)) for k, v in ONCELIK]


def temiz_ad(ad):
    a = ad.split("/")[-1]
    a = re.sub(r"@[\w.\-]+$", "", a)
    a = re.sub(r"\.(exe|cmd)$", "", a, flags=re.I)
    return ONEK.sub("", a) or a


def aciklama(yol):
    """skill zip / SKILL.md / README / package.json'dan ilk ~400 karakter aciklama (salt okuma)."""
    try:
        p = Path(yol)
        if yol.lower().endswith(".zip") and p.is_file():
            with zipfile.ZipFile(p) as z:
                for n in z.namelist():
                    if n.upper().endswith("SKILL.MD"):
                        m = re.search(r"description:\s*(.+)", z.read(n)[:3000].decode("utf-8", "ignore"))
                        return m.group(1)[:400] if m else ""
        elif p.is_dir():
            for n in ("SKILL.md", "README.md", "readme.md", "package.json", "pyproject.toml"):
                f = p / n
                if f.is_file():
                    t = f.read_text(encoding="utf-8", errors="ignore")[:1500]
                    m = re.search(r"description\W+([^\n]{10,300})", t)
                    return m.group(1) if m else re.sub(r"[#*`>\-]+", " ", t)[:400]
    except Exception:  # noqa: BLE001
        pass
    return ""


def sinifla(r, tur):
    t = temiz_ad(r["ad"])
    k = S.katla(t)
    for kat, rx in ONCELIK:
        if rx.search(k):
            return kat, "", "orta", "kapsam-kural", f"ad~{kat}"
    ozet = f"{r['tur']} {r['kaynak_yer']} {aciklama(r['yol'])}"
    return S.siniflandir(t, tur, ozet, r["tur"], r["yol"], "")


def norm(ad):
    return S._norm(ad)


def yer_etiketi(yer):
    k = yer.split(" (")[0]
    if k.startswith("pip:"):
        p = Path(k[4:]).parts
        return "pip:" + (p[-4] if len(p) >= 4 else k)
    return k


def oku_kat():
    with open(KAT, encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t"))


def main(kuru=False, yeniden=False):
    if yeniden:  # onceki kapsam eklemelerini kategori.tsv'den cikar (yalniz 'kapsam:' yolu olan satirlar)
        kat0 = oku_kat()
        with open(KAT, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(kat0[0])
            w.writerows(x for x in kat0[1:] if len(x) > 2 and not x[2].startswith("kapsam:"))
    with open(EK, encoding="utf-8", newline="") as f:
        ek = list(csv.DictReader(f, delimiter="\t"))
    rows = []
    for r in ek:
        tur = TUR_ESLE.get(r["tur"], "klon" if r["tur"] == "repo" else "kalem")
        b, ik, g, y, ge = sinifla(r, tur)
        cy = S.cok_yonlu(r["ad"], r["yol"], r["tur"])
        rows.append([r["ad"], tur, f"kapsam:{r['kaynak_yer']}:{r['yol']}", b, ",".join(ik), ",".join(cy), g, y, ge])
    gor, tekil = set(), []
    for x in rows:
        if tuple(x[:3]) not in gor:
            gor.add(tuple(x[:3]))
            tekil.append(x)
    with open(KAPSAM_KAT, "w", encoding="utf-8", newline="\n") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(BASLIK)
        w.writerows(tekil)
    kat = oku_kat()
    var_ad = {norm(x[0]) for x in kat[1:] if x}
    eklenecek, say, eklenen_ad = [], defaultdict(lambda: [0, 0, 0]), set()
    for x, r in zip(rows, ek):
        yer = yer_etiketi(r["kaynak_yer"])
        say[yer][0] += 1
        n = norm(x[0])
        if n in var_ad:
            say[yer][1] += 1
        else:
            say[yer][2] += 1
            if n not in eklenen_ad:
                eklenen_ad.add(n)
                eklenecek.append(x)
    if eklenecek and not kuru:
        with open(KAT, "a", encoding="utf-8", newline="") as f:
            csv.writer(f, delimiter="\t", lineterminator="\n").writerows(eklenecek)
    kat2 = oku_kat() if not kuru else kat
    ad2 = {norm(x[0]) for x in kat2[1:] if x}
    eksik = [r["ad"] for r in ek if norm(r["ad"]) not in ad2]
    out = {"ek_satir": len(ek), "kapsam_kategori_tekil": len(tekil), "kategori_tsv_onceki": len(kat) - 1,
           "eklenen": 0 if kuru else len(eklenecek), "ekleme_adayi": len(eklenecek), "kategori_tsv_sonraki": len(kat2) - 1,
           "eksik": len(eksik), "eksik_ornek": eksik[:20],
           "yer": {k: {"toplam": v[0], "zaten_var": v[1], "eklendi_veya_tekil": v[2]} for k, v in sorted(say.items(), key=lambda t: -t[1][0])},
           "kategori_dagilimi_ek": dict(Counter(x[3] for x in tekil).most_common())}
    DENETIM.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print({k: out[k] for k in ("ek_satir", "kapsam_kategori_tekil", "kategori_tsv_onceki", "eklenen", "kategori_tsv_sonraki", "eksik")})


if __name__ == "__main__":
    main("--kuru" in sys.argv, "--yeniden" in sys.argv)
