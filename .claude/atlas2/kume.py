"""ATLAS-2 küme süzgeci: K1 video-icerik, K2 guvenlik-test; kurulu (CC ya da claude.ai) öğeler."""
import json, re, sys
from pathlib import Path
KOK = Path(__file__).resolve().parents[2]
K1 = re.compile(r"video|clip|klip|remotion|hyperframe|moneyprinter|reel|shorts?\b|ffmpeg|altyazi|subtitle|vid-|kisa-video", re.I)
K2 = re.compile(r"guvenlik|security|secur|gitleaks|semgrep|opengrep|audit|osv|lighthouse|\baxe\b|a11y|playwright|strix|pentest|owasp|vuln|secret|sast|header|careful|guard|agentshield|e2e", re.I)
K3 = re.compile(r"docx|pptx|xlsx|pdf|slide|sunum|artifact|excel|powerpoint|wowerpoint|diagram", re.I)
def alanlar(r):
    a = r["alan"]
    return a if isinstance(a, list) else a.split(",")
def kume(r, rx, alan):
    if r["tur"] in ("video-aday", "site-inceleme") or not (r["cc"] or r["claude_ai"]):
        return False
    return bool(rx.search(r["ad"])) or alan in alanlar(r)
if __name__ == "__main__":
    rs = [json.loads(s) for s in (KOK / ".claude/atlas/envanter.jsonl").open(encoding="utf-8")]
    hazir = {json.loads(s)["ad"] for s in (KOK / "docs/atlas/kart.jsonl").open(encoding="utf-8")}
    for ad, rx, alan in (("K1", K1, "video"), ("K2", K2, "guvenlik"), ("K3", K3, "belge")):
        k = [r for r in rs if kume(r, rx, alan)]
        yeni = [r for r in k if r["ad"] not in hazir]
        print(ad, len(k), "kartsız", len(yeni), {t: sum(r["tur"] == t for r in k) for t in {r["tur"] for r in k}})
        (KOK / f".claude/atlas2/{ad}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in k), encoding="utf-8")
