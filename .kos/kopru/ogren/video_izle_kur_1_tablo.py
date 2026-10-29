"""VIDEO-IZLE-KUR-1: kurulacaklar son tablosu -> video-izle-kur-1/kurulacaklar.tsv (kalem, tür, kaynak, kurulum yolu, güvenlik notu).
Girdi: envanter.tsv KURULACAK + v2-arac.jsonl yeni adlar (kurulu olmayanlar) + tur1-cikar.jsonl komut + tarama/skill-kur sonuçları.
Yeniden koşulabilir (v2 çıkarma sürerken de). Kullanim: python -I video_izle_kur_1_tablo.py
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
K = Path(r"C:/Projeler/omer-skills")
H = Path.home() / ".claude"
D = K / ".kos/kopru/ogren/video-izle-kur-1"
IND = Path(r"C:/AI/indirilen")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# kurulu kanıtı: video_izle_kur_1_envanter.py ile aynı kaynaklar
kur = {norm(p.name) for p in (H / "skills").iterdir()} | {norm(p.parent.name) for p in (H / "skills").glob("*/*/SKILL.md")}
kur |= {norm(k.split("@")[0]) for k in json.load(open(H / "plugins/installed_plugins.json", encoding="utf-8")).get("plugins", {})}
klon = {norm(p.name.split("__", 1)[-1]) for p in IND.iterdir()}
metin = norm((K / "docs/video-tarama/00-kurulu.txt").read_text(encoding="utf-8", errors="ignore")
             + (D / "kurulu-ek.txt").read_text(encoding="utf-8", errors="ignore")
             + (K / "docs/kaynak-kutuphane/envanter.tsv").read_text(encoding="utf-8", errors="ignore"))


def kurulu_mu(ad, repo):
    adlar = [x for x in [norm(ad), norm(repo.split("/")[-1]) if "/" in repo else ""] if len(x) >= 5]
    for a in adlar:
        if a in kur:
            return "KURULU"
        if a in klon:
            return "KLONLU"
        if len(a) >= 6 and a in metin:
            return "KURULU"
    return ""


env = list(csv.DictReader(open(D / "envanter.tsv", encoding="utf-8"), delimiter="\t"))
bilinen = {norm(r["ad"]) for r in env} | {norm(r["repo"].split("/")[-1]) for r in env if "/" in r["repo"]}
cikar = {}
for s in open(D / "tur1-cikar.jsonl", encoding="utf-8"):
    d = json.loads(s)
    if d.get("durum") == "ok":
        cikar[norm(d["ad"])] = d
tara = {}
for s in open(IND / "video-izle-kur-1/sonuc.tsv", encoding="utf-8"):
    f = s.rstrip("\n").split("\t")
    if len(f) >= 7:
        tara[norm(f[1].split("/")[-1])] = f"SS HIGH {f[3]}/{f[4]} · gitleaks {f[5]} · semgrep {f[6]}"
skl = defaultdict(set)
for r in csv.DictReader(open(D / "skill-kur.tsv", encoding="utf-8"), delimiter="\t"):
    skl[norm(r["ad"])].add(r["durum"].split(":")[0] + (f" (SS HIGH {r['ss_high']}, gitleaks {r['gitleaks']})" if r["durum"].startswith("BEKLE") else ""))
OZEL = {  # EK 7 önlemleri (Ömer 13:36)
    "pentagi": "docker compose; yalnız 127.0.0.1, port dışa kapalı, yalnız kendi hedeflerimize; kullan-kapat; CVE-2026-14784 düzeltmesi çıkınca güncelle",
    "tradingagents": "uv venv + pip; LLM anahtarı ücretsiz Groq/OpenRouter/NVIDIA/Mistral; borsa-botu notu",
    "xtool": "WSL2 içinde; Apple ID girişi Ömer'e bırakılır",
    "freetoken": "install.sh YOK; ayrı venv'e `uv pip install \"freetoken[accel]\"` (~2 GiB, GPU ≤%80, kullan-kapat)",
}


def yol(tur, repo, ad):
    k = norm(repo.split("/")[-1]) if "/" in repo else norm(ad)
    if k in OZEL:
        return OZEL[k]
    t = (tur or "").lower()
    if not repo or "/" not in repo:
        return "repo/URL bulunacak (web ara) → sonra türüne göre"
    if "skill" in t:
        return "video_izle_kur_1_skill_kur.py (klon → SkillSpector+gitleaks → ~/.claude/skills + dist zip)"
    if "plugin" in t:
        return f"/plugin marketplace add {repo} (CC) + Desktop zip"
    if "mcp" in t:
        return "claude mcp add (CC) + Desktop MCP yapılandırması"
    return "klon → tarama → README kurulum (uv/npm/docker; ağır servis kullan-kapat)"


out = []
for r in env:
    if r["durum"] != "KURULACAK":
        continue
    k, rk = norm(r["ad"]), norm(r["repo"].split("/")[-1]) if "/" in r["repo"] else ""
    c = cikar.get(k, {})
    g = tara.get(rk) or "; ".join(sorted(skl.get(k, []))) or "tarama yok"
    komut = c.get("kurulum_komutu", "")
    out.append({"kalem": r["ad"], "tür": r["tür"], "kaynak": r["repo"] or c.get("repo_veya_url", ""), "köken": "envanter",
                "kurulum_yolu": yol(r["tür"], r["repo"], r["ad"]) + (f" · videodaki komut: {komut[:120]}" if komut and komut != "yok" else ""),
                "güvenlik": g, "eski_kanıt": r["kanıt"][:80]})
# v2 çıkarmasındaki yeni adlar
yeni, vid, tur, url = Counter(), defaultdict(list), {}, {}
for s in open(D / "v2-arac.jsonl", encoding="utf-8"):
    d = json.loads(s)
    for a in d.get("araclar", []):
        k = norm(a.get("ad"))
        if len(k) < 3 or k in bilinen:
            continue
        yeni[k] += 1
        vid[k].append(d["link"])
        tur.setdefault(k, (a.get("ad"), a.get("tur", "")))
        if a.get("repo_veya_url"):
            url[k] = a["repo_veya_url"]
v2kur = Counter()
for k, n in yeni.most_common():
    ad, t = tur[k]
    repo = re.sub(r"^https?://github\.com/", "", url.get(k, "")).strip("/")
    durum = kurulu_mu(ad, repo)
    v2kur[durum or "KURULACAK"] += 1
    if durum:
        continue
    out.append({"kalem": ad, "tür": t, "kaynak": url.get(k, "") or vid[k][0], "köken": f"v2 ({n} video)",
                "kurulum_yolu": yol(t, repo, ad), "güvenlik": "tarama yok", "eski_kanıt": ""})
with open(D / "kurulacaklar.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter="\t")
    w.writeheader()
    w.writerows(out)
print("satir", len(out), Counter(o["köken"].split(" ")[0] for o in out), "v2 yeni ad", dict(v2kur),
      "tarama var", sum(o["güvenlik"] != "tarama yok" for o in out), "repo yok", sum(o["kurulum_yolu"].startswith("repo/URL") for o in out))
