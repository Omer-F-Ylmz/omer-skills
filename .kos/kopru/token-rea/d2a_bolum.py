"""d2a: köprü ajan profilinde hook enjeksiyonunu blok blok sayar (1 claude -p + count_tokens). Yalnız etiket + sayı yazar.
  python d2a_bolum.py"""
import json, re, sys
import taban as t

import os, pathlib
G = t.BU / "d2a_govde.json"
if G.exists():
    d = json.load(open(G, encoding="utf-8")); t.GOVDE, t.BASLIK = d["g"], d["b"]
else:
    t.GOVDE, t.BASLIK = t.kur_baslik(); json.dump({"g": t.GOVDE, "b": t.BASLIK}, open(G, "w", encoding="utf-8"))
bloklar = []
for m in t.GOVDE["messages"]:
    parca = m["content"] if isinstance(m["content"], list) else [{"text": m["content"]}]
    for c in parca:
        metin = c.get("text", "")
        # system-reminder / başlık sınırlarında böl
        for p in re.split(r"(?=<system-reminder>|SessionStart[^\n]{0,40}hook|<context_window_protection>|<EXTREMELY_IMPORTANT>|# Work state|# \[omer-skills\] recent|Codebase map|\n# Ponytail|\n# Environment)", metin):
            if p.strip():
                bloklar.append(p)
cikti = [{"etiket": re.sub(r"\s+", " ", b[:70]), "karakter": len(b), "token": t.tok(b)} for b in bloklar]
json.dump(cikti, open(t.BU / "d2a_bolum.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for c in sorted(cikti, key=lambda x: -x["token"]):
    print(c["token"], c["karakter"], c["etiket"])
print("toplam", sum(c["token"] for c in cikti), "count_tokens", t.SAYAC["say"])
