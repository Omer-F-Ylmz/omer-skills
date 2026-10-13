"""KAYNAK-5 onay betiği — Desktop/Ömer koşar. 5 repodan KUR yok; Atlas UYARLA kendi skill'imize Kapı satırı ekler
(OpenResearch UYARLA'sı tools/olcum/kosucu.py'de, kurulum gerektirmez).

  python onay/kaynak_5_uygula.py --kuru   # plan: satır var mı (varsayılan, değişiklik yok)
  python onay/kaynak_5_uygula.py uygula   # eksikse ekler (idempotent) + dist/kaynak-5/kendi zip + zip_denetle
  python onay/kaynak_5_uygula.py --geri   # yalnız BU betiğin eklediği satırı çıkarır
CC tarafı: skill omer-skills marketplace'inden gelir (kol/kaynak5 main'e birleşince `claude plugin marketplace update omer-skills`);
~/.claude'a yazılmaz. claude.ai: dist/kaynak-5/kendi/*.zip (Replace). Hiçbir şey kaldırılmaz; MCP listesi önce=sonra değilse rc=1.
"""
import sys, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_40_kur_p2_uygula import EV, KOK, _cikar, _ekle, _yol, mcp_var_mi  # noqa: E402

EKLE = [
    ("departman-surec-git-yayin",
     "- Paralel ajan kolunda her commit `git commit --trailer \"Gorev: <AD>\"` taşır; birleştirmede \"zaten var/özdeş\" iddiası "
     "`git cherry -v main <kol>` ile (patch-id; `-` = içerikçe main'de) kanıtlanır, rapora commit → görev satırı (KAYNAK-5, Atlas)."),
]


def plan(kok=KOK):
    return [(s, satir in _yol(kok, s).read_text(encoding="utf-8")) for s, satir in EKLE]


def paketle(kok=KOK):
    sys.path.insert(0, str(kok / "tools" / "skill-paket"))
    from zip_denetle import denetle
    dist = kok / "dist" / "kaynak-5" / "kendi"
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
