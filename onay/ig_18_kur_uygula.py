"""IG-18-KUR onay betiği — Desktop/Ömer koşar. IG-18'de KUR yok; 1 UYARLA (anti-slop/oxlint) departman-frontend'e kural satırı ekler.

  python onay/ig_18_kur_uygula.py --kuru   # plan: hangi satır eksik (varsayılan, değişiklik yok)
  python onay/ig_18_kur_uygula.py uygula   # eksik satırı ekler (idempotent) + dist/ig-18/kendi zip + zip_denetle
  python onay/ig_18_kur_uygula.py --geri   # yalnız BU betiğin eklediği satırı çıkarır
Karar: `.claude/igkur18/karar18.tsv`. CC tarafı: skill omer-skills marketplace'inden gelir (dal main'e birleşince
`claude plugin marketplace update omer-skills`); ~/.claude'a yazılmaz. claude.ai: dist/ig-18/kendi/*.zip (Replace).
Üçüncü taraf zip yok (KUR yok; tasarım/animasyon/router/blender/ruflo adayları devir/*.tsv'de). MCP listesi önce=sonra değilse rc=1.
"""
import json, sys, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EV = Path.home()
# (skill, eklenecek Kapılar satırı) — mekanizma kendi sözümüzle, kaynak metin kopyası yok
EKLE = [
    ("departman-frontend",
     "- TS projesinde lint: oxlint + dmmulroy/anti-slop kural seti (MIT), proje devDependency'si, sürüm sabit; global kurulmaz (IG-18 DdrNeEUN63i)."),
]


def mcp_var_mi(ev=EV):
    """~/.claude.json'daki MCP sunucu adları (değer yazdırılmaz, yalnız adlar)."""
    try:
        j = json.loads((ev / ".claude.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    adlar = set(j.get("mcpServers") or {})
    for p in (j.get("projects") or {}).values():
        adlar |= set((p or {}).get("mcpServers") or {})
    return adlar


def _yol(kok, skill):
    return kok / "skills" / skill / "SKILL.md"


def plan(kok=KOK):
    """[(skill, satır_var_mı)] — değişiklik yapmaz."""
    return [(s, satir in _yol(kok, s).read_text(encoding="utf-8")) for s, satir in EKLE]


def _ekle(f, satir):
    """Kapılar bölümünün son maddesinin altına ekler; bayt düzeyinde (CRLF/LF korunur)."""
    b = f.read_bytes()
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    sat = b.split(nl)
    i = sat.index("## Kapılar".encode())
    j = i + 1
    while j < len(sat) and sat[j].startswith(b"- "):
        j += 1
    sat.insert(j, satir.encode())
    f.write_bytes(nl.join(sat))


def _cikar(f, satir):
    b = f.read_bytes()
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    f.write_bytes(nl.join(s for s in b.split(nl) if s != satir.encode()))


def paketle(kok=KOK):
    sys.path.insert(0, str(kok / "tools" / "skill-paket"))
    from zip_denetle import denetle
    dist = kok / "dist" / "ig-18" / "kendi"
    dist.mkdir(parents=True, exist_ok=True)
    sorun = []
    for s, _ in EKLE:
        d = kok / "skills" / s
        with zipfile.ZipFile(dist / f"{s}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(x for x in d.rglob("*") if x.is_file()):
                z.write(f, f"{s}/{f.relative_to(d).as_posix()}")
        sorun += denetle(dist / f"{s}.zip")
    return sorun


def uygula(kok=KOK, ev=EV):
    once = mcp_var_mi(ev)
    for (s, satir), (_, var) in zip(EKLE, plan(kok)):
        if not var:
            _ekle(_yol(kok, s), satir)
            print("eklendi:", s)
    sorun = paketle(kok)
    print("zip_denetle:", "TEMİZ" if not sorun else sorun)
    return once == mcp_var_mi(ev) and not sorun


def geri(kok=KOK, ev=EV):
    once = mcp_var_mi(ev)
    for s, satir in EKLE:
        _cikar(_yol(kok, s), satir)
    return once == mcp_var_mi(ev)


def main():
    kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
    if kip == "--kuru":
        for s, var in plan():
            print(("var   " if var else "EKLE  ") + s)
        return 0
    ok = uygula() if kip == "uygula" else geri() if kip == "--geri" else None
    if ok is None:
        print(__doc__)
        return 2
    print("mcp önce=sonra" if ok else "HATA: MCP listesi değişti ya da zip sorunu")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
