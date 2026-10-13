"""TOKEN-10 onay betiği — Desktop koşar (Ömer onayından sonra). Tüm ajanlar listede kalır; kendi ajanlarımızın
(docs/token-10/esleme.tsv) ~/.claude/agents/<ad>.md frontmatter description satırı sıkışmış metinle değişir. Gövde/model/ad,
plugin ajanları ve settings değişmez. Değişen dosyaların eski hali ~/.claude/agents-yedek-token10/'a yedeklenir.

  python onay/token_10_uygula.py --kuru   # plan: değişecek / bulunmayan sayısı (varsayılan)
  python onay/token_10_uygula.py uygula   # yedekle + description değiştir + ajan-getir katalog yenile
  python onay/token_10_uygula.py --geri   # yedekten geri yükle + katalog yenile"""
import shutil, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / "tools" / "olcum"))
import ajan_katalog  # noqa: E402
from ajan_aciklama import aciklama_degistir  # noqa: E402

ESLEME = KOK / "docs" / "token-10" / "esleme.tsv"


def esleme(yol=ESLEME):
    return {s.split("\t")[0]: s.split("\t")[2] for s in yol.read_text(encoding="utf8").splitlines()[1:] if s.strip()}


def katalog(ev):
    satirlar, _ = ajan_katalog.uret(ev)
    y = ev / "skills" / "ajan-getir" / "katalog.tsv"
    if y.parent.is_dir():
        y.write_text("ad\tmodel\ttek_satir\tyol\n" + "".join("\t".join(s) + "\n" for s in satirlar), encoding="utf-8", newline="\n")
    return len(satirlar)


def main(argv=None, ev=Path.home() / ".claude", es=None, yedek="agents-yedek-token10"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    ag, yd = ev / "agents", ev / yedek
    if a[0] == "--geri":
        n = 0
        for p in sorted(yd.glob("*.md")) if yd.is_dir() else []:
            shutil.copy2(p, ag / p.name); p.unlink(); n += 1
        if yd.is_dir() and not any(yd.iterdir()):
            yd.rmdir()
        print("geri:", n, "ajan eski açıklamaya döndü · katalog", katalog(ev)); return 0
    es = es if es is not None else esleme()
    plan = {}
    for ad, yeni in es.items():
        p = ag / f"{ad}.md"
        if p.exists():
            eski = p.read_bytes().decode("utf8")
            y = aciklama_degistir(eski, yeni)
            if y != eski:
                plan[p] = y
    eksik = sorted(ad for ad in es if not (ag / f"{ad}.md").exists())
    if a[0] != "uygula":
        print(f"KURU: değişecek {len(plan)} · eşlemede olup agents'ta bulunmayan {len(eksik)} {eksik[:5]}"); return 0
    if yd.exists():
        sys.exit(f"yedek dizini zaten var ({yd}); önce --geri")
    yd.mkdir()
    for p in plan:
        shutil.copy2(p, yd / p.name)
    for p, y in plan.items():
        p.write_bytes(y.encode("utf8"))
    print("uygulandı:", len(plan), "ajan açıklaması · yedek", yd, "· katalog", katalog(ev), "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.exit(main())
