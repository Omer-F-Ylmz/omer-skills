"""ATLAS-2 Opus kararı K3 (belge-sunum): K3 kartlarına karar + kosul; ATLAS-1 ve K1/K2 kararlı kartlara dokunmaz."""
import json, re
from collections import Counter
from pathlib import Path

VARSAYILAN = {  # departman-belge Adımlar 1–4 + biçim başına tek araç
    "departman-belge": "", "document-generate": "proje dokümanı", "example-skills:doc-coauthoring": "ortak yazım",
    "agent-skills:documentation-and-adrs": "karar kaydı (ADR)", "make-pdf": "markdown → PDF", "diagram": "diyagram",
    "claude-mem:wowerpoint": "sunum (HTML slayt)", "example-skills:docx": ".docx dosyası", "example-skills:pptx": ".pptx dosyası",
    "example-skills:xlsx": ".xlsx dosyası", "example-skills:pdf": "PDF okuma/birleştirme/form", "markitdown": "her biçim → markdown okuma",
    "humanizer": "AI izi temizliği", "writing-guidelines": "yazım kılavuzu", "document-release": "yayın sonrası doküman güncelle",
}
KULLANMA = {
    "gstack-make-pdf": "make-pdf'in gstack kopyası; kısa adı kullan",
    "gstack-document-generate": "document-generate'in gstack kopyası",
    "gstack-document-release": "document-release'in gstack kopyası",
    "gstack-diagram": "diagram'ın gstack kopyası",
    "claude-ads:ads-report": "reklam denetim raporu; belge-sunum değil (ad eşleşmesiyle kümeye girdi)",
}
OZEL = {
    "example-skills:web-artifacts-builder": "çok bileşenli claude.ai artifact (state/routing/shadcn); tek dosya HTML/JSX'te değil",
    "example-skills:theme-factory": "belge/slayt/artifact'a hazır tema giydirilecekse",
    "ecc:frontend-slides": "animasyonlu HTML slayt; wowerpoint yetmezse",
    "baoyu-slide-deck": "makale/metinden görsel slayt destesi gerekince",
    "excalidraw-diagram": "el çizimi görünümlü diyagram istenirse; varsayılan diagram",
    "dok-markitdown-donusum": "çok dosyalı toplu dönüşüm alt ajana verilecekse; tek dosyada markitdown",
    "stop-slop": "humanizer sonrası ikinci dil süzgeci gerekince",
}


def kosul(k):
    a = k["ad"]
    if a in OZEL:
        return OZEL[a]
    if a.startswith("adobe-for-creativity:"):
        return "Adobe bağlantısı açıksa ve Adobe çıktısı istenirse; yerel biçimde example-skills:*"
    if a.endswith("-paket"):
        return "kaynak paketi; asıl skill/ajan yetmezse tarif kaynağı"
    if a.startswith("phoenix-prd-pipeline:"):
        return "çok aşamalı PRD hattı gerekince; tek PRD'de pln-prd-yazar"
    if a.startswith(("sepia", "obsidian")):
        return "ilgili kasada/araçta çalışılıyorsa"
    return k.get("ne_zaman") or ""


yol = Path("docs/atlas/kart.jsonl")
K = {json.loads(s)["ad"] for s in open(".claude/atlas2/K3.jsonl", encoding="utf-8")}
L = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]
K -= {k["ad"] for k in L if k.get("karar") and k["ad"] not in VARSAYILAN}  # önceki karar korunur; belge varsayılanı üstüne yazar
for k in L:
    a = k["ad"]
    if a not in K:
        continue
    c = None if a in VARSAYILAN or a in KULLANMA else kosul(k)
    k["karar"] = "VARSAYILAN" if a in VARSAYILAN else "KULLANMA" if a in KULLANMA else "GEREKINCE"
    k["kosul"] = VARSAYILAN.get(a) or KULLANMA.get(a) or c
eksik = (set(VARSAYILAN) | set(KULLANMA) | set(OZEL)) - {k["ad"] for k in L if k["ad"] in K}
assert not eksik, eksik
yol.write_bytes(("\n".join(json.dumps(k, ensure_ascii=False) for k in L) + "\n").encode("utf-8"))
print(Counter(k["karar"] for k in L if k["ad"] in K))
