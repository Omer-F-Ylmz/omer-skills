"""ERTELE-1: skill/ajan ertelenmiş yükleme kataloğu (MCP ToolSearch mantığı: başta liste yok, iş gelince ara → tam metni o an oku).
python tools/ertele_katalog.py kur            → ~/.claude/ertele-dizin.json (skill + ajan adı → tanım dosyası; hiçbir dosya taşınmaz/silinmez)
python tools/ertele_katalog.py ara "<iş>"     → arac_ara kartları + kartsız tanımlarda anahtar sözcük isabeti (ad · tür · tek satır)
python tools/ertele_katalog.py tam <ad>       → tanımın tam metni (skill: SKILL.md, ajan: .md)"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
EV = Path.home() / ".claude"
DIZIN = EV / "ertele-dizin.json"


def _on_bilgi(yol):
    m = re.match(r"---\s*\n(.*?)\n---", yol.read_text(encoding="utf-8", errors="ignore"), re.S)
    alan = dict(re.findall(r"^(name|description):\s*(.*)$", m.group(1), re.M)) if m else {}
    return alan.get("name", "").strip().strip("'\""), alan.get("description", "").strip().strip("'\"")[:200]


def _ekle(d, tur, ad, yol):
    if ad and ad not in d:
        d[ad] = {"tur": tur, "yol": str(yol), "acik": _on_bilgi(yol)[1]}


def kur():
    d = {}
    for kok in (KOK / ".claude", EV):
        for f in sorted((kok / "skills").glob("*/SKILL.md")) + sorted((kok / "skills").glob("*/skills/*/SKILL.md")) \
                + sorted((kok / "skills").glob("synced/*/**/SKILL.md")):  # claude.ai senkron kopyaları
            _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)
            _ekle(d, "skill", f.parent.name, f)  # ön bilgideki ad klasör adından farklı olabilir ("Bug Triage")
        for f in sorted((kok / "skills").glob("**/skills/*/TALIMAT.md")):  # paket içi alt skill (SKILL.md yerine TALIMAT.md)
            _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)
            _ekle(d, "skill", f.parent.name, f)
        for f in sorted((kok / "agents").glob("*.md")):
            _ekle(d, "ajan", _on_bilgi(f)[0] or f.stem, f)
    kurulu = json.loads((EV / "plugins" / "installed_plugins.json").read_text(encoding="utf-8"))
    for anahtar, kayitlar in kurulu.get("plugins", kurulu).items():
        eklenti = anahtar.split("@")[0]
        for k in kayitlar:
            p = Path(k["installPath"])
            for f in sorted(p.glob("**/SKILL.md")):
                _ekle(d, "skill", f"{eklenti}:{f.parent.name}", f)
                _ekle(d, "skill", _on_bilgi(f)[0] or f.parent.name, f)  # CC listesinde öneksiz görünen eklenti skill'i
            for f in sorted(p.glob("agents/**/*.md")):
                ic = ":".join(f.relative_to(p / "agents").with_suffix("").parts[:-1] + (_on_bilgi(f)[0] or f.stem,))
                _ekle(d, "ajan", f"{eklenti}:{ic}", f)
            for f in sorted(p.glob("commands/**/*.md")):
                _ekle(d, "komut", f"{eklenti}:{f.stem}", f)
    DIZIN.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def _dizin():
    return json.loads(DIZIN.read_text(encoding="utf-8")) if DIZIN.exists() else kur()


def _katla(s):
    return s.lower().translate(str.maketrans("çğıöşüâî", "cgiosuai"))


def _mudur(gorev, d, n=2):
    """departman-* müdür skill'leri: Türkçe katlama + 5 harflik kök eşleşmesi (araştır → arastirma)."""
    kok = {s[:5] for s in re.findall(r"\w{4,}", _katla(gorev))}
    puan = sorted(((sum(k in _katla(ad + " " + v["acik"]) for k in kok), ad) for ad, v in d.items()
                   if ad.startswith("departman-") and ":" not in ad), key=lambda x: -x[0])
    return [ad for p, ad in puan[:n] if p > 0]


def ara(gorev, n=8):
    import arac_ara as aa
    d = _dizin()
    mudur = _mudur(gorev, d)
    o = [f"{ad} · müdür skill · {d[ad]['acik'][:110]}" for ad in mudur]
    kartlar = [k for k in aa.ara(gorev)["kartlar"] if k.get("tur") in ("skill", "ajan", None) and k["ad"] not in mudur][:n] \
        or aa.ara(gorev)["kartlar"][:n]
    o += [f"{k['ad']} · {k.get('tur', '?')} · {(k.get('ne_yapar') or k.get('aciklama') or '')[:110]}" for k in kartlar]
    gor = {k["ad"] for k in kartlar} | set(mudur)
    sozcuk = [s for s in re.findall(r"\w{4,}", gorev.lower())]
    puan = sorted(((sum(s in (ad + " " + v["acik"]).lower() for s in sozcuk), ad, v) for ad, v in _dizin().items() if ad not in gor),
                  key=lambda x: -x[0])
    o += [f"{ad} · {v['tur']} · {v['acik'][:110]}" for p, ad, v in puan[:n] if p > 0]
    return "\n".join(o) + "\n(tam metin: python tools/ertele_katalog.py tam <ad>)"


def tam(ad):
    import arac_ara as aa
    d = _dizin()
    v = d.get(ad) or d.get(ad.split(":")[-1]) or next(  # komuttan türeyen alt ad: modernize-harden-scan → modernize-harden
        (d[k] for k in sorted(d, key=len, reverse=True) if ad.startswith(k + "-")), None)
    if v:
        return Path(v["yol"]).read_text(encoding="utf-8", errors="ignore")
    return aa.tam(ad) or f"bulunamadı: {ad}"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k, *a = sys.argv[1:] or ["?"]
    print({"kur": lambda: f"{len(kur())} tanım → {DIZIN}", "ara": lambda: ara(" ".join(a)), "tam": lambda: tam(a[0])}.get(k, lambda: __doc__)())
