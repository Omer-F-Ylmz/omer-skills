"""mem_anahtar: claude-mem için TR<->EN anahtar sözcük yan dizini (kaynak koda dokunmaz). Claude çağrısı yok (yalnız ücretsiz havuz, sözlük için bir kez).
  sozluk [tavan]   korpus sözcüklerinin karşı dil karşılıklarını havuzla çıkarır (mem_sozluk.json, kaldığı yerden; tavan = en çok havuz çağrısı)
  kur | guncelle  yan dizin ~/.claude-mem/anahtar.db (kur sıfırdan, guncelle yalnız yeni gözlemler; DB salt-okur açılır)
  ara "<soru>"    mem2 biçiminde çıktı (kw+st kanalı eklenmiş bm25)
Dizin: FTS5(title,subtitle,narrative,facts,concepts,kw,st); kw = gözlem sözcüklerinin karşı dil karşılıkları (5 harfe kırpık), st = kendi sözcüklerinin 5 harfe kırpık hali (ek/çekim toleransı)."""
import collections
import json
import os
import re
import sqlite3
import sys

AD = os.path.dirname(os.path.abspath(__file__))
DB = os.path.expanduser("~/.claude-mem/claude-mem.db")
YAN = os.path.expanduser("~/.claude-mem/anahtar.db")
SOZLUK = os.path.join(AD, "mem_sozluk.json")
KES = 5
AG = (5, 2, 5, 3, 3)  # mem2.AGIRLIK ile aynı sıra (text yok)
KW_AG, ST_AG = 1.0, 1.0


def sozcukler(s):
    return [w for w in re.findall(r"[^\W\d_]+", (s or "").lower()) if len(w) > 3]


def kes(w):
    return w[:KES]


def sozluk_yukle():
    try:
        return json.load(open(SOZLUK, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def sozluk_kur(tavan):
    sys.path.insert(0, os.path.join(AD, "..", "..", "..", "tools"))
    import ucretsiz_havuz as H
    c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
    df = collections.Counter()
    for r in c.execute("SELECT title,subtitle,narrative,facts FROM observations"):
        df.update(set(sozcukler(" ".join(x or "" for x in r))))
    sz = sozluk_yukle()
    bekleyen = [w for w, v in df.most_common() if v >= 30 and w not in sz]
    print("bekleyen", len(bekleyen), "tavan", tavan)
    for k in range(0, min(len(bekleyen), tavan * 220), 220):
        parca = bekleyen[k:k + 220]
        ist = ("Satırlarda yazılım iş günlüğünde geçen Türkçe ya da İngilizce sözcükler var. Her sözcük için diğer dildeki en çok 3 karşılığı yaz "
               "(Türkçe ise İngilizce, İngilizce ise Türkçe). Format: `sözcük: karşılık1, karşılık2`. Tanımlayıcı/özel ad/iki dilde aynı olan sözcük için `sözcük: -`. "
               "Yalnız bu satırlar, girdiyle aynı sırada, başka metin yok.\n" + "\n".join(parca))
        y, kay, _ = H.cagir("ozet", ist, max_tokens=4000, haiku_tavan=0, etiket="mem-sozluk")
        if not y:
            print("çağrı başarısız", k)
            continue
        n = 0
        for satir in y.splitlines():
            if ":" in satir:
                a, b = satir.split(":", 1)
                a = a.strip().strip("`*- ").lower()
                if a in parca:
                    sz[a] = [x for x in sozcukler(b)] if b.strip() != "-" else []
                    n += 1
        json.dump(sz, open(SOZLUK, "w", encoding="utf-8"), ensure_ascii=False)
        print(k, kay, n, "/", len(parca))


def satirlar(c, son):
    return c.execute("SELECT id,title,subtitle,narrative,facts,concepts FROM observations WHERE id>? ORDER BY id", (son,))


def yan_ekle(son_i=None, sifirla=False):
    sz = sozluk_yukle()
    if sifirla and os.path.exists(YAN):
        os.replace(YAN, YAN + ".eski")
    y = sqlite3.connect(YAN)
    y.execute("CREATE VIRTUAL TABLE IF NOT EXISTS a USING fts5(title,subtitle,narrative,facts,concepts,kw,st)")
    y.execute("CREATE TABLE IF NOT EXISTS m(k TEXT PRIMARY KEY,v)")
    son = (y.execute("SELECT v FROM m WHERE k='son'").fetchone() or [0])[0]
    c = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
    n = 0
    for i, t, s, na, f, co in satirlar(c, son):
        own = sozcukler(" ".join(x or "" for x in (t, s, na, f, co)))
        kw = [kes(x) for w in dict.fromkeys(own) for x in sz.get(w, [])]
        st = [kes(w) for w in own]
        y.execute("INSERT INTO a(rowid,title,subtitle,narrative,facts,concepts,kw,st) VALUES(?,?,?,?,?,?,?,?)",
                  (i, t, s, na, f, co, " ".join(dict.fromkeys(kw)), " ".join(dict.fromkeys(st))))
        son, n = i, n + 1
    y.execute("INSERT OR REPLACE INTO m VALUES('son',?)", (son,))
    y.commit()
    print("eklendi", n, "son", son)


def ara(soru, k=5, proje=None, kw=None, st=None):
    kw = KW_AG if kw is None else kw
    st = ST_AG if st is None else st
    w = list(dict.fromkeys(x for x in re.findall(r"\w+", soru.lower()) if len(x) > 2))
    if not w:
        return []
    s = list(dict.fromkeys(kes(x) for x in w if len(x) > 3))
    orig = " OR ".join('"%s"' % x.replace('"', "") for x in w)
    q = "{title subtitle narrative facts concepts} : (%s)" % orig
    if s and (kw or st):
        q += " OR {kw st} : (%s)" % " OR ".join('"%s"' % x for x in s)
    y = sqlite3.connect(YAN, timeout=5)
    y.execute("ATTACH ? AS g", (DB,))
    sql = ("SELECT o.id,o.created_at,o.type,o.title,length(o.narrative)/4 FROM a JOIN g.observations o ON o.id=a.rowid "
           "WHERE a MATCH ? " + ("AND o.project=? " if proje else "") + "ORDER BY bm25(a,%s,%s,%s) LIMIT ?" % (",".join(map(str, AG)), kw, st))
    return y.execute(sql, (q, *([proje] if proje else []), k)).fetchall()


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "sozluk":
        sozluk_kur(int(a[1]) if len(a) > 1 else 5)
    elif a[0] in ("kur", "guncelle"):
        yan_ekle(sifirla=a[0] == "kur")
    else:
        sys.path.insert(0, AD)
        import mem2
        sys.stdout.reconfigure(encoding="utf-8")
        print(mem2.bicim(ara(a[1] if a[0] == "ara" else a[0])) or "sonuç yok")
