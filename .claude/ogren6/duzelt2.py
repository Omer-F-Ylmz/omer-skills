"""ÖĞREN-6 d4: yazar satırlarında 'belirsiz' kalan komut/sınırlar → kaynak satırından BİREBİR (model yok).
  python -X utf8 .claude/ogren6/duzelt2.py    (v1-yazar-*.jsonl yerinde; sonra v1.py birlestir)
komut = ÖĞREN-3 komut.py yöntemi (name: / "command" / "url" / usage); sınırlar = duzelt.py kalıbı, yoksa gevşek uyarı/kısıt kalıbı."""
import json, re, sys
from pathlib import Path

B = Path(__file__).parent
sys.path.insert(0, str(B.parent / "ogren3"))
import komut  # noqa: E402

SIKI = re.compile(r"\b(NEVER|MUST NOT|MUST|ALWAYS|DO NOT|Do not)\b|\bASLA\b|[Yy]asak|[Aa]sla ")
GEVSEK = re.compile(r"\b(never|must|should not|shouldn't|don't|do not|avoid|warning|caution|limitation|limited to|only works|not supported|unsupported|"
                    r"requires?|cannot|can't|note:)\b|yalnız|dikkat|uyarı|sınır", re.I)


# kalıbın kaçırdığı 5 alan: (ad, alan) → kaynak satırında geçen iğne (satır birebir alınır)
ELLE = {("csharp-lsp", "komut"): "dotnet tool install --global csharp-ls", ("push-kapi", "komut"): "gitleaks git --exit-code 1",
        ("duman_claudeai", "komut"): "python tools/duman_claudeai.py dist/yukle-10b/replace", ("tdd", "komut"): "command: tdd",
        ("owasp-top-10-testing", "sinirlar"): "A09 Security Logging"}


def elle(o, m):
    for a in ("komut", "sinirlar"):
        igne = ELLE.get((o["ad"], a))
        if igne and o[a]["deger"].startswith("belirsiz"):
            s = next(x.strip() for x in m.splitlines() if igne in x)
            o[a] = {"deger": s[:150] if a == "komut" else "Kaynaktaki kural: " + s[:150], "alinti": s[:700]}
    return o


# hakem t65/t66: ders-yuvasi işareti (`basla ` ⊂ [Aa]sla ) sınır sayılmıştı; mekanizma Y'leri
MEK = {"phoenix-cti-search": ["G4-dışı"], "cti-domain-research": ["G4-dışı"], "pixeljury": ["LLM değerlendirme"], "drizzle-docs": ["veri/şema", "rehber"]}
ORTAK = ("gstack-skill-start", "Follow ", "## ", '"url"')  # skill'in kendi komutu değil: ortak önsöz / şablon başlığı / paket url'si


def duzelt(o, m):
    if o["sinirlar"]["alinti"].startswith("<!--"):
        o["sinirlar"] = {"deger": "belirsiz — yeniden", "alinti": ""}
    kendi = re.search(rf"^(?!#).*(?<![\w/-])/{re.escape(o['ad'])}(?![\w-]).*$", m, re.M)
    if kendi and o["komut"]["deger"].lstrip().startswith(ORTAK + ("gstack",)) or o["komut"]["alinti"].lstrip().startswith(ORTAK):
        if kendi:
            o["komut"] = {"deger": kendi.group(0).strip()[:150], "alinti": kendi.group(0).strip()[:700]}
    r = {"komut": o["komut"]["deger"], "alinti": {}}
    if o["komut"]["deger"].startswith("belirsiz"):
        komut.doldur(r, m)
        if r["alinti"]:
            o["komut"] = {"deger": r["komut"][:150], "alinti": r["alinti"]["komut"][:700]}
    if o["sinirlar"]["deger"].startswith("belirsiz"):
        satirlar = [x.strip() for x in m.splitlines() if len(x.strip()) >= 25 and not x.lstrip().startswith(("#", "```", "|", "<!--"))]
        s = next((x for x in satirlar if SIKI.search(x)), None) or next((x for x in satirlar if GEVSEK.search(x)), None)
        if s:
            o["sinirlar"] = {"deger": "Kaynaktaki kural: " + s[:150], "alinti": s[:700]}
    return o


if __name__ == "__main__":
    kalan = {"komut": [], "sinirlar": []}
    for p in sorted(B.glob("v1-yazar-*.jsonl")):
        out = []
        for l in p.read_text(encoding="utf-8").splitlines():
            o = json.loads(l)
            m = (B / "kaynak" / (re.sub(r"[^\w.-]", "_", o["ad"]) + ".txt")).read_text(encoding="utf-8", errors="replace")
            o = elle(duzelt(o, m), m)
            o["mekanizma"] = MEK.get(o["ad"], o["mekanizma"])
            out.append(json.dumps(o, ensure_ascii=False))
            for a in kalan:
                if o[a]["deger"].startswith("belirsiz"):
                    kalan[a].append(o["ad"])
        p.write_bytes(("\n".join(out) + "\n").encode("utf-8"))
    print({a: len(v) for a, v in kalan.items()}, kalan)
