"""GRAPHIFY-ULTRA-1 G0: bugünkü CC transkriptlerinde keşif maliyeti. python graphify_ultra_g0.py [YYYY-MM-DD]
Read/Grep/Glob ve Bash (rtk grep|read, oku, graphify query, grep/cat/sed/head) çağrı sayısı + sonuç jetonu (karakter/4);
"graf yanıtlardı" = sembol/dosya-nerede sınıfı (tanımlayıcı desenli Grep, ad desenli Glob, tam Read >300 satır).
Çıktı: rapor/graphify-ultra-1/g0-pahali.tsv (en pahalı 20) + özet satırları."""
import glob, json, os, re, sys, time
from collections import Counter
from datetime import date

gun = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
t0 = time.mktime(time.strptime(gun, "%Y-%m-%d"))
dosyalar = [f for f in glob.glob(os.path.expanduser("~/.claude/projects/*/**/*.jsonl"), recursive=True)
            if os.path.getmtime(f) >= t0]
SEMBOL = re.compile(r"^(def |class |function |const |async )?\\?b?[A-Za-z_][\w.]*(\\\(|\(|\\b)?$")


def sinif(ad, g):
    if ad == "Read":
        if re.search(r"\.(png|jpe?g|webp|gif|pdf)$", g.get("file_path", ""), re.I):
            return None  # görsel: base64 boyu jeton değil, keşif de değil
        return "read-aralik" if g.get("offset") or g.get("limit") else "read-tam"
    if ad in ("Grep", "Glob"):
        return ad.lower()
    k = g.get("command", "")
    for s, d in (("graphify", r"\bgraphify (query|explain|path)"), ("oku", r"\boku\b|cc-kopru"),
                 ("rtk-grep", r"\brtk grep|\bgrep |\brg "), ("rtk-read", r"\brtk read|\bcat |\bsed -n|\bhead |\btail ")):
        if re.search(d, k):
            return s
    return None


say, jeton, graf, pahali = Counter(), Counter(), Counter(), []
for f in dosyalar:
    bek = {}
    for satir in open(f, encoding="utf-8", errors="replace"):
        try:
            o = json.loads(satir)
        except ValueError:
            continue
        for c in (o.get("message") or {}).get("content") or []:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "tool_use" and (s := sinif(c.get("name"), c.get("input") or {})):
                bek[c["id"]] = (s, c.get("input") or {})
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in bek:
                s, g = bek.pop(c["tool_use_id"])
                ic = c.get("content")
                n = len(ic if isinstance(ic, str) else json.dumps(ic, ensure_ascii=False)) // 4
                say[s] += 1; jeton[s] += n
                desen = g.get("pattern", "")
                yanit = (s == "grep" and SEMBOL.match(desen)) or (s == "glob" and "*" not in desen.rsplit("/", 1)[-1][:-3]) \
                    or (s == "read-tam" and n > 3000)
                if yanit:
                    graf[s] += n
                pahali.append((n, s, os.path.basename(f)[:8], (g.get("file_path") or desen or g.get("command", ""))[:90]))

os.makedirs(os.path.join(os.path.dirname(__file__), "rapor", "graphify-ultra-1"), exist_ok=True)
with open(os.path.join(os.path.dirname(__file__), "rapor", "graphify-ultra-1", "g0-pahali.tsv"), "w", encoding="utf-8") as w:
    w.write("jeton\tsinif\toturum\thedef\n")
    for p in sorted(pahali, reverse=True)[:20]:
        w.write("\t".join(map(str, p)).replace("\n", " ") + "\n")
top = sum(jeton.values()) or 1
print(f"G0 {gun}: {len(dosyalar)} transkript · keşif {sum(say.values())} çağrı · {top / 1e3:.0f}k jeton · "
      f"graf yanıtlardı {sum(graf.values()) / 1e3:.0f}k (%{100 * sum(graf.values()) / top:.0f})")
for s in sorted(say, key=lambda s: -jeton[s]):
    print(f"  {s}: {say[s]} çağrı · {jeton[s] / 1e3:.0f}k · graf-yanıtlardı {graf[s] / 1e3:.0f}k")
