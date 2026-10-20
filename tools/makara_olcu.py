"""MAKARA ölçüsü (haftalık): iş türü başına oturum sayısı ve oturum başı token, kapı ıskası, kabul edilen öneri, kasadan cevaplanan soru oranı
→ 90-log/makara-olcu-<hafta>.md. İş türü = ajan-sira dosya adının ilk harf öbeği. Model yok, Claude token 0.
Soru oranı `beyin ara` günlüğünden (.kos/makara/ara.log: ts<TAB>sonuç sayısı); günlük yoksa 'veri yok' yazılır."""
import json
import re
import time
from collections import defaultdict
from pathlib import Path

import makara_ders

KOK = makara_ders.KOK
M = KOK / ".kos/makara"


def hafta(t):
    return time.strftime("%G-W%V", time.localtime(t))


def topla(sira=makara_ders.SIRA):
    h = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))  # hafta → tür → [oturum, token, ıska]
    for p in Path(sira).glob("*.json"):
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:
            continue
        u = j.get("usage") or {}
        tok = sum(u.get(k) or 0 for k in ("input_tokens", "output_tokens", "cache_creation_input_tokens"))
        e = h[hafta(p.stat().st_mtime)][(re.match(r"[a-zçğıöşü]+", p.stem) or ["diger"])[0]]
        e[0] += 1; e[1] += tok; e[2] += bool(j.get("is_error") or "kapı GEÇMEDİ" in str(j.get("result"))[:400])
    return h


def soru_orani(w):
    y = M / "ara.log"
    if not y.exists():
        return None
    s = [l.split("\t") for l in y.read_text(encoding="utf-8").splitlines() if "\t" in l]
    s = [(float(a), int(b)) for a, b in s if hafta(float(a)) == w]
    return (sum(1 for _, n in s if n), len(s)) if s else None


def main():
    w, h = hafta(time.time()), topla()
    kum = [json.loads(p.read_text(encoding="utf-8")) for p in (M / "kum").glob("*.json")]
    kabul = sum(1 for r in kum if hafta(time.mktime(time.strptime(r["gun"], "%Y-%m-%d"))) == w)
    so = soru_orani(w)
    sat = [f"- {t}: {o} oturum · oturum başı {tok // max(o, 1):,} token · ıska {i}" for t, (o, tok, i) in sorted(h[w].items())]
    y = makara_ders.KASA / "90-log" / f"makara-olcu-{w}.md"
    y.write_bytes((f"---\ntur: olcu\nguncellenme: {time.strftime('%Y-%m-%d')}\netiket: [makara, olcu]\n---\n# makara ölçü {w}\n"
                   f"- kabul edilen öneri (kum havuzu): {kabul}\n- kasadan cevaplanan soru: {f'{so[0]}/{so[1]}' if so else 'veri yok (ara.log boş)'}\n## İş türü başına\n"
                   + ("\n".join(sat) or "bu hafta oturum yok") + "\n").encode("utf-8"))
    print(y)


if __name__ == "__main__":
    main()
