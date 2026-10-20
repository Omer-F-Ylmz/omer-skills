"""mem2: claude-mem arama, worker'siz doğrudan salt-okur FTS5 (observations_fts, bm25, başlık ağırlıklı).
Kullanım: python -I -S mem2.py "<soru>" [--k 5] [--proje omer-skills]
Çıktı: "#ID tarih T başlık ~jeton" satırları; ayrıntı için get_observations([ID])."""
import os
import re
import sqlite3
import sys

DB = os.path.expanduser("~/.claude-mem/claude-mem.db")
SEMBOL = {"bugfix": "●", "feature": "◆", "refactor": "↻", "change": "✓", "discovery": "○", "decision": "⚖"}


def kelimeler(s):
    k = [w for w in re.findall(r"\w+", s.lower()) if len(w) > 2]
    return list(dict.fromkeys(k))


AGIRLIK = (5, 2, 5, 0, 3, 3)  # title, subtitle, narrative, text, facts, concepts; eğitim tohumu 20102402 taramasından


AD = os.path.dirname(os.path.abspath(__file__))
ONBELLEK = os.path.join(AD, "mem2_genis.json")


def genislet(sorular):
    """Havuzla (Claude yok) her soru için EN+TR ilgili arama sözcükleri; önbellekli. Havuz yoksa/başarısızsa boş liste."""
    import json
    try:
        ob = json.load(open(ONBELLEK, encoding="utf-8"))
    except (OSError, ValueError):
        ob = {}
    eksik = [s for s in dict.fromkeys(sorular) if s not in ob]
    if eksik:
        try:
            sys.path.insert(0, os.path.join(AD, "..", "..", "..", "tools"))
            import ucretsiz_havuz as H
            ist = ("Her numaralı soru bir geliştirici iş günlüğünde (İngilizce başlıklar, Türkçe/İngilizce anlatı) bir kaydı arıyor. Her soru için kayıtta geçmesi "
                   "muhtemel en çok 6 ilgili anahtar sözcük yaz (İngilizce ve Türkçe karışık, eş anlamlılar dahil). Çıktı: soru başına bir satır, sözcükler boşlukla, numarasız.\n"
                   + "\n".join("%d. %s" % (k + 1, s) for k, s in enumerate(eksik)))
            y, _, _ = H.cagir("ozet", ist, max_tokens=1200, haiku_tavan=0, etiket="mem2-genis",
                              dogrula=lambda m: None if len([l for l in m.strip().splitlines() if l.strip()]) == len(eksik) else "satır sayısı")
            if y:
                for s, l in zip(eksik, [l for l in y.strip().splitlines() if l.strip()]):
                    ob[s] = kelimeler(l.lstrip("0123456789.) "))
                json.dump(ob, open(ONBELLEK, "w", encoding="utf-8"), ensure_ascii=False)
        except Exception:  # noqa: BLE001
            pass
    return [ob.get(s, []) for s in sorular]


def ara(soru, k=5, proje=None, ag=AGIRLIK, ek=()):
    w = list(dict.fromkeys(kelimeler(soru) + list(ek)))
    if not w:
        return []
    c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True, timeout=5)
    q = " OR ".join('"%s"' % x.replace('"', "") for x in w)
    sql = ("SELECT o.id, o.created_at, o.type, o.title, length(o.narrative)/4 FROM observations_fts f "
           "JOIN observations o ON o.id=f.rowid WHERE observations_fts MATCH ? "
           + ("AND o.project=? " if proje else "") + "ORDER BY bm25(observations_fts, %s) LIMIT ?" % ",".join(map(str, ag)))
    return c.execute(sql, (q, *([proje] if proje else []), k)).fetchall()


def ara2(soru, k=5, proje=None, ek=()):
    """İki aşamalı: önce özgün OR; ilk k'da ek sözcük çakışması yoksa ek sözcükleri birleştir."""
    ilk = ara(soru, k, proje)
    ekler = [x for x in ek if x not in kelimeler(soru)]
    if not ekler or not ilk:
        return ilk or ara(soru, k, proje, ek=ek)
    c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True, timeout=5)
    for i, *_ in ilk:
        m = " ".join(x or "" for x in c.execute("SELECT title, narrative FROM observations WHERE id=?", (i,)).fetchone()).lower()
        if any(x in m for x in ekler):
            return ilk
    return ara(soru, k, proje, ek=ek)


def bicim(rows):
    return "\n".join("#%d %s %s %s ~%d" % (i, d[5:16].replace("T", " "), SEMBOL.get(t, "?"), (b or "").strip("* ")[:110], n or 0)
                     for i, d, t, b, n in rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    k = int(a[a.index("--k") + 1]) if "--k" in a else 5
    p = a[a.index("--proje") + 1] if "--proje" in a else None
    sys.stdout.reconfigure(encoding="utf-8")
    ek = genislet([a[0]])[0] if "--genis" in a else ()
    print(bicim(ara2(a[0], k, p, ek=ek) if ek else ara(a[0], k, p)) or "sonuç yok")
