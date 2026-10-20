"""Tohum doğrulama: kaynak dosya var, satır aralıkta, yasak dosya yok, çok-notlu ≥2 kaynak, ajan-sira/SIRA sayısı."""
import json
import os
import re
from pathlib import Path

D = Path(__file__).parent
oku = lambda p: [json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]  # noqa: E731
yasak = {re.sub(r":\d+$", "", k.strip()).split("/")[-1] for q in oku(D.parent / "beyin2/sorular.jsonl") for k in q["kaynak"].split(";")}
for t in (2007, 2008):
    qs = oku(D / f"sorular-{t}.jsonl")
    sira, dosya, kotu = 0, set(), []
    for q in qs:
        ks = [k.strip() for k in q["kaynak"].split(";")]
        sira += any("ajan-sira" in k or "SIRA.md" in k for k in ks)
        if q.get("cok") and len(ks) < 2:
            kotu.append((q["id"], "cok-tek-kaynak"))
        for k in ks:
            m = re.match(r"(.+):(\d+)$", k.replace("\\", "/"))
            p = m and os.path.expanduser(m.group(1))
            if not m or not os.path.exists(p):
                kotu.append((q["id"], "yok", k))
                continue
            if int(m.group(2)) > len(Path(p).read_text(encoding="utf-8", errors="replace").split("\n")):
                kotu.append((q["id"], "satir", k))
            dosya.add(os.path.basename(p))
            if os.path.basename(p) in yasak:
                kotu.append((q["id"], "yasak", k))
    print(t, len(qs), "cok", sum(bool(q.get("cok")) for q in qs), "sira", sira, "dosya", len(dosya), "kotu", kotu)
