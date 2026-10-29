"""VIDEO-IZLE-KUR-1 tur 2 (a): v2-uyarla.tsv (UYARLA/AL 238 satir) baslik+gerekce+kanit metninden arac/repo/skill/MCP adlarini
ucretsiz modelle cikarir (Claude jetonu 0). Kaldigi yerden devam eder. Kullanim: python -I -X utf8 video_izle_kur_1_v2arac.py
Cikti: video-izle-kur-1/v2-arac.jsonl {"id", "durum", "araclar": [{"ad","tur","repo_veya_url"}]}"""
import csv, json, re, sys
from pathlib import Path

K = Path(r"C:/Projeler/omer-skills")
sys.path.insert(0, str(K / "tools"))
from ucretsiz_havuz import cagir

D = K / ".kos/kopru/ogren/video-izle-kur-1"
OUT = D / "v2-arac.jsonl"
bitti = {d["id"] for d in map(json.loads, open(OUT, encoding="utf-8")) if d["durum"] == "ok"} if OUT.exists() else set()
ISTEM = """Asagidaki video ozetinde ADI GECEN kurulabilir araclari listele: GitHub repo, CLI, Claude Code skill/plugin, MCP sunucusu,
kutuphane, web sitesi/servis. YALNIZ metinde adi gecenleri yaz (uydurma yok); genel kavram (ornek "AI", "Claude Code" kendisi) yazma.
JSON yaz: {{"araclar": [{{"ad": "...", "tur": "repo|cli|skill|plugin|mcp|kutuphane|site", "repo_veya_url": "metinde varsa, yoksa bos"}}]}}
Hic yoksa {{"araclar": []}}. Yalniz JSON.
---
BASLIK: {b}
GEREKCE: {g}
KANIT: {k}"""


def dogrula(t):
    m = re.search(r"\{.*\}", t or "", re.S)
    try:
        assert isinstance(json.loads(m.group(0))["araclar"], list)
    except Exception:
        return "json degil"


for r in csv.DictReader(open(D / "v2-uyarla.tsv", encoding="utf-8"), delimiter="\t"):
    if r["id"] in bitti:
        continue
    t, kaynak, _ = cagir("ozet", ISTEM.format(b=r["başlık"], g=r["gerekçe"], k=r["kanıt"]), max_tokens=600, dogrula=dogrula, etiket="video-izle-kur-1-v2")
    rec = {"id": r["id"], "link": r["link"], "durum": "ok" if t else "model-yok", "kaynak": kaynak,
           "araclar": json.loads(re.search(r"\{.*\}", t, re.S).group(0))["araclar"] if t else []}
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(r["id"], rec["durum"], len(rec["araclar"]), kaynak, flush=True)
print("BITTI")
