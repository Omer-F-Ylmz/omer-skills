"""ERTELE-2: aday C ayar dosyası — tüm skill'ler user-invocable-only (model listesinden çıkar, /ad kalır), çekirdek liste name-only; ajan reddi ertele_ayar.json'dan."""
import json, re, sys
from pathlib import Path
K = Path(__file__).parent; KOK = K.parents[1]
sat = (K / "context-A.txt").read_text(encoding="utf-8").splitlines()
i = sat.index("### Skills")
adlar = [m.group(1).strip() for s in sat[i:] if (m := re.match(r"\| (.+?) \| (User|Plugin|Project|Bundled|Managed)\b", s))]
CEKIRDEK = {a for a in adlar if a.split(":")[-1].startswith("departman-")} | {
    "is-akisi", "opus-akis", "plan-kur", "yetenek-getir", "beyin", "headroom-compress", "graphify", "jev",
    "commit", "simplify", "frontend-craft", "impeccable", "context7-cli", "find-docs", "playwright-cli", "markitdown", "loop", "review"}
ov = {a: ("name-only" if a in CEKIRDEK else "user-invocable-only") for a in adlar}
red = json.loads((KOK / "tools" / "ertele_ayar.json").read_text(encoding="utf-8"))
(K / "ayar-C.json").write_text(json.dumps({"skillOverrides": ov, **red}, ensure_ascii=False), encoding="utf-8")
print(len(adlar), "skill;", sum(v == "name-only" for v in ov.values()), "çekirdek;", len(red["permissions"]["deny"]), "ajan reddi")
