"""ATLAS-2 Opus kararı: K1 (video-icerik) + K2 (guvenlik-test) kartlarına karar + kosul; diğer kartlara dokunmaz."""
import json, re, subprocess
from collections import Counter
from pathlib import Path

VARSAYILAN = {
    # video: yerel hat (video CLI = indirme+kare+Gemini+rapor), alt ajan, ffmpeg
    "video": "", "video-cli": "", "video-tarama": "", "video-izle": "", "video-uygula": "",
    "video-tarayici": "", "aday-arastirici": "", "ffmpeg": "", "gemini-omni-flash-api": "",
    # güvenlik/test: site kapanış listesi
    "gitleaks": "", "semgrep": "", "sec-gitleaks-gecmis": "", "sec-semgrep-kural": "", "sec-guvenlik-baslik": "",
    "lighthouse-chrome-devtools": "", "qa-erisilebilirlik-testi": "", "qa-e2e-playwright": "",
}
KULLANMA = {
    "video-tarayici-haiku": "TOKEN-DENEME-2a deneme kolu; varsayılan video-tarayici",
}
OZEL = {
    "strix": "ZAP kurulu değilken yerel önizlemeye hızlı tarama (ZAP muadili); canlı/üçüncü taraf hedef yok",
    "sec-pentest-plani": "yalnız sahipli/izinli hedefte pentest planı; site kapanışında değil",
    "cso": "sürüm öncesi tek seferlik güvenlik görüşü; araç taramalarından sonra",
    "autoclip-paket": "uzun videodan otomatik kısa klip kesimi gerekince",
    "moneyprinter-paket": "stok görüntü + TTS ile tam otomatik kısa video denemesi; marka işi değil",
    "reel-plan": "reel/kısa video senaryo planı gerekince",
    "erisilebilirlik-paket": "kaynak paketi; qa-erisilebilirlik-testi yetmezse tarif kaynağı",
}


def kosul(k):
    a = k["ad"]
    if a in OZEL:
        return OZEL[a]
    if re.match(r"claude-ads:audit-", a):
        return None  # KULLANMA
    if a.endswith("-desktop"):
        return "claude.ai/Desktop kopyası; CC'de asıl CLI"
    if a.endswith("-paket"):
        return "kaynak paketi; asıl skill/ajan yetmezse tarif kaynağı"
    if a.startswith("hyperframes"):
        return "HTML/CSS ile video kompozisyonu gerekince (Remotion alternatifi); hyperframes:hyperframes yönlendirir"
    if a.startswith("remotion-"):
        return "Remotion ile render bu konu gerekince"
    if a.startswith("vid-"):
        return "kısa/uzun video yapım hattında bu adım gerekince"
    if "strix" in a:
        return "strix taraması gerekince (ZAP yokken); yalnız yerel/izinli hedef"
    return k.get("ne_zaman") or ""


yol = Path("docs/atlas/kart.jsonl")
K = {json.loads(s)["ad"] for f in ("K12", "K2ek") for s in open(f".claude/atlas2/{f}.jsonl", encoding="utf-8")}
eski = subprocess.run(["git", "show", "8b16d66c:docs/atlas/kart.jsonl"], capture_output=True, encoding="utf-8").stdout
K -= {k["ad"] for k in map(json.loads, eski.splitlines()) if k.get("karar")}  # ATLAS-1 kararı korunur
L = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()]
for k in L:
    a = k["ad"]
    if a not in K:
        continue
    c = None if a in VARSAYILAN or a in KULLANMA else kosul(k)
    k["karar"] = "VARSAYILAN" if a in VARSAYILAN else "KULLANMA" if a in KULLANMA or c is None else "GEREKINCE"
    k["kosul"] = VARSAYILAN.get(a) or KULLANMA.get(a) or c or "reklam hesap denetimi; güvenlik/test değil (ad eşleşmesiyle kümeye girdi)"
eksik = (set(VARSAYILAN) | set(KULLANMA) | set(OZEL)) - {k["ad"] for k in L if k["ad"] in K}
assert not eksik, eksik
yol.write_bytes(("\n".join(json.dumps(k, ensure_ascii=False) for k in L) + "\n").encode("utf-8"))
print(Counter(k["karar"] for k in L if k["ad"] in K))
