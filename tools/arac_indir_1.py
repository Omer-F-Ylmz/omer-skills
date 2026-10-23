"""ARAC-INDIR-1: _arac.tsv kurulu-olmayanlari tekillestir, gh ile cozumle, clone --depth 1, gitleaks+semgrep say. Kurma/calistirma yok."""
import csv, json, os, re, subprocess, sys, shutil
from concurrent.futures import ThreadPoolExecutor

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAPOR = os.path.join(KOK, ".kos", "kopru", "rapor")
HEDEF = r"C:\AI\indirilen"
CIKTI = os.path.join(RAPOR, "arac-indir-1.tsv")
BUYUK_KB = 500 * 1024
ES = {"whisper": "faster-whisper", "yt-dp": "yt-dlp"}  # islevsel es (kurulu-es)
ALIAS = {"skils": "vercel-labs/skills", "claude-men": "thedotmack/claude-mem", "cavem": "JuliusBrussee/caveman", "caveman@caveman": "JuliusBrussee/caveman",
         "cc-usage": "ryoppippi/ccusage", "codebur": "getagentseal/codeburn", "codebura": "getagentseal/codeburn", "codeburm": "getagentseal/codeburn",
         "codeburs": "getagentseal/codeburn", "open-webui": "open-webui/open-webui", "lamafactory": "hiyouga/LLaMA-Factory", "taste-skil": "Leonxlnx/taste-skill",
         "ui-ux-pro-max-": "nextlevelbuilder/ui-ux-pro-max-skill", "agent-tars/cli": "bytedance/UI-TARS-desktop", "hummingbot.gi": "hummingbot/hummingbot",
         "shadcnglatest": "shadcn-ui/ui", "diffsynth-": "modelscope/DiffSynth-Studio", "everything-claude-code@everything-claude-code": "affaan-m/everything-claude-code",
         "apify/actors-ncp-server": "apify/actors-mcp-server", "apify/actorsmcp-server": "apify/actors-mcp-server", "apify/tap/mcpc": "apify/mcpc",
         "create-video": "remotion-dev/remotion", "create-videoptatest": "remotion-dev/remotion", "daude-video": "remotion-dev/remotion"}
ENV = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1", GIT_TERMINAL_PROMPT="0")


def calis(cmd, zaman=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=zaman, env=ENV, encoding="utf-8", errors="replace")
        return r.returncode, r.stdout
    except Exception as e:
        return 99, str(e)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def gh_goruntule(aday):
    rc, o = calis(["gh", "repo", "view", aday, "--json", "nameWithOwner,stargazerCount,diskUsage,isFork,isArchived"], 40)
    return json.loads(o) if rc == 0 else None


def coz(satir):
    adaylar = [a for a in ([ALIAS[satir["ad"]]] if satir["ad"] in ALIAS else []) + satir["ham"].split("|") if a]
    for a in adaylar:
        if a.count("/") == 1:
            d = gh_goruntule(a)
            if d:
                return d, "gh-aday"
    ad = satir["ad"]
    rc, o = calis(["gh", "search", "repos", ad, "--limit", "5", "--json", "fullName,stargazersCount"], 40)
    if rc == 0:
        for d in sorted(json.loads(o or "[]"), key=lambda x: -x["stargazersCount"]):
            if norm(d["fullName"].split("/")[1]) == norm(ad) and d["stargazersCount"] >= 50:
                v = gh_goruntule(d["fullName"])
                if v:
                    return v, "gh-arama(tahmin)"
    return None, ""


def tara(yol):
    sayi = {}
    rc, o = calis(["gitleaks", "detect", "--no-git", "-s", yol, "--report-format", "json", "--report-path", "-", "--exit-code", "0", "--no-banner"], 300)
    try:
        sayi["gl"] = len(json.loads(o)) if o.strip().startswith("[") else 0
    except Exception:
        sayi["gl"] = "?"
    rc, o = calis(["semgrep", "--config", "auto", "--severity", "ERROR", "--json", "--quiet", yol], 600)
    try:
        sayi["sg"] = len(json.loads(o)["results"])
    except Exception:
        sayi["sg"] = "?"
    return f"gitleaks={sayi['gl']};semgrep_ERROR={sayi['sg']}"


def isle(g):
    d, kaynak = g["d"], g["kaynak"]
    ad = d["nameWithOwner"]
    boyut = f"{d['diskUsage']//1024}MB"
    if d["diskUsage"] > BUYUK_KB:
        return [ad, "github:" + ad, "buyuk-ertelendi", boyut, "-", g["video"]]
    yol = os.path.join(HEDEF, ad.replace("/", "__"))
    if not os.path.isdir(yol):
        rc, o = calis(["git", "clone", "--depth", "1", "--no-tags", "-c", "core.symlinks=false", f"https://github.com/{ad}.git", yol], 600)
        if rc != 0:
            return [ad, "github:" + ad, "indirilemedi", boyut, o.strip()[-80:], g["video"]]
    return [ad, f"github:{ad} ({kaynak})", "indirildi", boyut, tara(yol), g["video"]]


def main():
    os.makedirs(HEDEF, exist_ok=True)
    envanter = ""
    for f in os.listdir(RAPOR):
        if f.startswith("_inv_"):
            envanter += open(os.path.join(RAPOR, f), encoding="utf-8", errors="replace").read().lower()
    with open(os.path.join(RAPOR, "_arac.tsv"), encoding="utf-8") as f:
        satirlar = [r for r in csv.DictReader(f, delimiter="\t") if r["durum"] != "KURULU"]
    print("ham satir", len(satirlar), flush=True)
    with ThreadPoolExecutor(8) as ex:
        sonuc = list(ex.map(coz, satirlar))
    tekil, cikti = {}, []
    for s, (d, kaynak) in zip(satirlar, sonuc):
        v = s["ornek_video"].strip("[]").replace("'", "")
        if d is None:
            es = ES.get(s["ad"])
            if es and es in envanter:
                cikti.append([s["ad"], "-", f"kurulu-es({es})", "-", "-", v])
            else:
                cikti.append([s["ad"], "-", "bulunamadi", "-", "-", v])
            continue
        k = d["nameWithOwner"].lower()
        if k in tekil:
            tekil[k]["video"] += "," + v
        else:
            tekil[k] = {"d": d, "kaynak": kaynak, "video": v}
    print("tekil repo", len(tekil), flush=True)
    with ThreadPoolExecutor(4) as ex:
        cikti += list(ex.map(isle, tekil.values()))
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["ad", "kaynak", "durum", "boyut", "tarama", "video"])
        w.writerows(cikti)
    print("bitti", len(cikti))


if __name__ == "__main__":
    main()
