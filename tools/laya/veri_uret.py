"""Laya ince ayar verisi: ajan-sira.tsv + ajan-sira.log + ajan-sira/*.json + ig-41/ig-42 tsv -> veri/{model,tur,konu}_{train,test}.csv.

model: istem metni -> haiku|sonnet|opus (tsv model= > log BAŞLAT > json modelUsage; başarılı koşular; istem başına çoğunluk).
tur:   istem metni -> iş türü (anahtar sözcük zayıf etiketi; on-söz 1 listesi).
konu:  ig-42 video başlığı+gerekçe / ig-41 site açıklaması -> konu (anahtar sözcük zayıf etiketi).
Ayrım %80/20, istem dosyası bazında (aynı istem iki tarafa düşmez).
"""
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

KOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KOPRU = os.path.join(KOK, ".kos", "kopru")
CIKTI = os.path.join(os.path.dirname(__file__), "veri")
UZUNLUK = 1500

TURLER = {
    "site-3d": ["three.js", "webgl", "3d", "landing", "frontend", "css", "tailwind", "vitrin", "html"],
    "video": ["video", "reel", "ffmpeg", "kare", "instagram", "transkript", "altyazı"],
    "guvenlik": ["güvenlik", "security", "skillspector", "kvkk", "zafiyet", "cve", "lisans", "secret"],
    "belge": ["belge", "rapor", "docx", "pdf", "doküman", "readme", "özet"],
    "logo": ["logo", "marka", "svg", "ikon"],
    "render": ["blender", "render", "glb", "gltf", "mesh", "sahne"],
}


def tur_etiketi(metin):
    m = metin.lower()
    puan = {t: sum(len(re.findall(re.escape(k), m)) for k in ks) for t, ks in TURLER.items()}
    en, say = max(puan.items(), key=lambda kv: kv[1])
    return en if say >= 2 else "diger"


KONULAR = {
    "ai-model": ["model", "llm", "gpt", "gemini", "nvidia", "api key", "openrouter", "qwen", "deepseek", "llama", "ollama", "yapay zeka"],
    "kodlama-ajan": ["claude", "skill", "mcp", "agent", "ajan", "cursor", "codex", "prompt", "token", "context", "kod"],
    "tasarim-ui": ["design", "tasarım", "ui", "ux", "css", "tailwind", "figma", "landing", "website", "frontend", "animasyon", "3d", "three.js"],
    "video-medya": ["video", "reel", "edit", "ffmpeg", "remotion", "capcut", "image", "görsel", "photo", "logo", "music"],
    "otomasyon": ["n8n", "automation", "otomasyon", "scrap", "workflow", "zapier", "bot", "crawl"],
    "guvenlik": ["security", "güvenlik", "hack", "vulnerab", "privacy", "malware", "gizlilik"],
}


def konu_etiketi(metin):
    m = metin.lower()
    puan = {t: sum(len(re.findall(r"(?<![a-zçğıöşü])" + re.escape(k), m)) for k in ks) for t, ks in KONULAR.items()}
    en, say = max(puan.items(), key=lambda kv: kv[1])
    return en if say >= 1 else "diger"


def model_kisa(ad):
    return next((m for m in ("haiku", "sonnet", "opus") if m in ad), None)


def json_modeli(yol):
    try:
        mu = json.load(open(yol, encoding="utf-8")).get("modelUsage") or {}
    except (OSError, ValueError):
        return None
    return model_kisa(max(mu, key=lambda k: mu[k].get("costUSD", 0))) if mu else None


def taraf(yol):
    return "test" if int(hashlib.md5(yol.encode()).hexdigest(), 16) % 5 == 0 else "train"


def main():
    satirlar = list(csv.reader(open(os.path.join(KOPRU, "ajan-sira.tsv"), encoding="utf-8"), delimiter="\t"))[1:]
    oylar = defaultdict(Counter)
    log_model = {}
    for x in open(os.path.join(KOPRU, "ajan-sira.log"), encoding="utf-8", errors="replace"):
        m = re.search(r"BAŞLAT (\S+) (haiku|sonnet|opus)", x)
        if m:
            log_model[m.group(1)] = m.group(2)
    metin = {}
    for r in satirlar:
        if len(r) < 2 or not os.path.exists(os.path.join(KOK, r[1])):
            continue
        yol = r[1]
        metin[yol] = open(os.path.join(KOK, yol), encoding="utf-8", errors="replace").read()[:UZUNLUK]
        j = os.path.join(KOPRU, "ajan-sira", r[0] + ".json")
        basarili = True
        if os.path.getsize(j) if os.path.exists(j) else 0:
            try:
                basarili = not json.load(open(j, encoding="utf-8")).get("is_error")
            except ValueError:
                pass
        model = next((x[6:] for x in r[2:] if x.startswith("model=")), None) or log_model.get(r[0]) or json_modeli(j)
        if model and basarili:
            oylar[yol][model] += 1
    os.makedirs(CIKTI, exist_ok=True)
    sayim = Counter()
    gorev = os.path.join(KOPRU, "gorev")
    tur_metin = dict(metin)
    for ad in os.listdir(gorev):
        yol = os.path.relpath(os.path.join(gorev, ad), KOK).replace(os.sep, "/")
        if ad.endswith(".md") and yol not in tur_metin:
            tur_metin[yol] = open(os.path.join(gorev, ad), encoding="utf-8", errors="replace").read()[:UZUNLUK]
    konu_metin = {}
    for r in csv.reader(open(os.path.join(KOPRU, "ogren", "video-764-v2.tsv"), encoding="utf-8"), delimiter="	"):
        if len(r) > 5 and r[0] != "id":
            konu_metin["ig-42:" + r[0]] = f"{r[2]}. {r[5]}"
    for r in csv.reader(open(os.path.join(KOPRU, "ig-41-frontend-siteler.tsv"), encoding="utf-8"), delimiter="	"):
        if len(r) > 2:
            konu_metin["ig-41:" + r[1]] = f"{r[1]}. {r[2]}"
    for ad, kume, etiket in (("model", metin, lambda y: oylar[y].most_common(1)[0][0] if oylar.get(y) else None),
                             ("tur", tur_metin, lambda y: tur_etiketi(tur_metin[y])),
                             ("konu", konu_metin, lambda y: konu_etiketi(konu_metin[y]))):
        dosya = {t: csv.writer(open(os.path.join(CIKTI, f"{ad}_{t}.csv"), "w", newline="", encoding="utf-8"))
                 for t in ("train", "test")}
        for w in dosya.values():
            w.writerow(["text", "label"])
        for yol in sorted(kume):
            e = etiket(yol)
            if e:
                dosya[taraf(yol)].writerow([re.sub(r"\s+", " ", kume[yol]), e])
                sayim[(ad, taraf(yol), e)] += 1
    for k in sorted(sayim):
        print(*k, sayim[k])


if __name__ == "__main__":
    sys.exit(main())
