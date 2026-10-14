"""Tavan analizi: altında olup v3 havuzunda olmayan adlar nerede kaybolur (A ham listesi / süzgeç / hiç yok) ve varlık eşleşmesiyle kaç tanesi geri gelir."""
import json, re, sys
from collections import Counter
from pathlib import Path
WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / "tools"))
import katalog_ara as ka, plan_kur as pk
IS = [s.split("\t")[2] for s in (WT / "tests/fixtures/plan_kur2_isler.tsv").read_text(encoding="utf8").splitlines()[1:]]
PAKET = [[0, 1, 2], [3, 4], [5, 6]]
A = {str(r["paket"]): r["metin"] for r in map(json.loads, (WT / ".claude/plankur2/sonuc.jsonl").read_text(encoding="utf8").splitlines()) if r["kol"] == "A"}
kur = [o for o in pk.kayitlar() if ka.kurulu(o) and o["tur"] in ("skill", "ajan", "mcp", "cli")]
yer = Counter(); ornek = Counter(); n = 0; geri = 0; ek_say = []
for p, grup in enumerate(PAKET):
    parca = re.split(r"(?m)^#{1,4} .*?(?=\d)(\d+)", A[str(p)])
    for i in grup:
        metin = next((parca[j + 1] for j in range(1, len(parca) - 1, 2) if parca[j] == str(i + 1)), "")
        alt = {o["ad"] for o in kur if re.search(rf"(?<![\w-]){re.escape(o['ad'])}(?![\w-])", metin)}
        ham = {o["ad"] for o in ka.aday(IS[i])}
        kal, _, _ = ka.suz([o for o in ka.aday(IS[i]) if o["tur"] in ("skill", "ajan", "mcp", "cli")], ka.yigin(IS[i]))
        hav = {o["ad"] for o in kal} | {"ecc:code-reviewer", "ecc:security-reviewer"}
        vr = pk.varliklar(IS[i])
        ek = {o["ad"] for o in kur if pk.ad_sozcukleri(o["ad"]) & vr} - hav
        ek_say.append(len(ek))
        for a in alt - hav:
            y = "suzuldu" if a in ham else ("varlik" if a in ek else "yok")
            yer[y] += 1
            if y == "yok": ornek[a] += 1
        n += len(alt); geri += len(alt & (hav | ek))
print("altın", n, "havuz+inceleme tavanı", round((n - sum(yer.values())) / n, 2), "· +varlık tavanı", round(geri / n, 2), "· ek ad/iş", ek_say)
print("kayıp yeri", dict(yer))
print("yok (en sık)", ornek.most_common(25))
