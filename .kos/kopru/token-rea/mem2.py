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


def ara(soru, k=5, proje=None, ag=AGIRLIK):
    w = kelimeler(soru)
    if not w:
        return []
    c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True, timeout=5)
    q = " OR ".join('"%s"' % x.replace('"', "") for x in w)
    sql = ("SELECT o.id, o.created_at, o.type, o.title, length(o.narrative)/4 FROM observations_fts f "
           "JOIN observations o ON o.id=f.rowid WHERE observations_fts MATCH ? "
           + ("AND o.project=? " if proje else "") + "ORDER BY bm25(observations_fts, %s) LIMIT ?" % ",".join(map(str, ag)))
    return c.execute(sql, (q, *([proje] if proje else []), k)).fetchall()


def bicim(rows):
    return "\n".join("#%d %s %s %s ~%d" % (i, d[5:16].replace("T", " "), SEMBOL.get(t, "?"), (b or "").strip("* ")[:110], n or 0)
                     for i, d, t, b, n in rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    k = int(a[a.index("--k") + 1]) if "--k" in a else 5
    p = a[a.index("--proje") + 1] if "--proje" in a else None
    sys.stdout.reconfigure(encoding="utf-8")
    print(bicim(ara(a[0], k, p)) or "sonuç yok")
