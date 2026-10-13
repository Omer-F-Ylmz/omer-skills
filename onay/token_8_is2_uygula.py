"""TOKEN-8 iş 2 onay betiği — Desktop koşar (Ömer onayından sonra). Kapı f2c d2: önek −44.2k/istek, kör seçim A 34 = V1 34, tur 5 → 6.
Agent listesinde yalnız çekirdek (.claude/token8/cekirdek_v1.txt, 59 ajan) kalır; diğer ~/.claude/agents/*.md SİLİNMEZ,
~/.claude/agents-katalog/'a taşınır ve ajan-getir katalog.tsv'den (yol yeni yer) bulunur. Plugin ajanları ve settings değişmez.

  python onay/token_8_is2_uygula.py --kuru   # plan: kalan / taşınacak sayısı (varsayılan)
  python onay/token_8_is2_uygula.py uygula   # taşı + katalog yenile
  python onay/token_8_is2_uygula.py --geri   # hepsini agents/'a geri taşı + katalog yenile"""
import shutil, sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import ajan_katalog  # noqa: E402

CEKIRDEK = set((KOK / ".claude" / "token8" / "cekirdek_v1.txt").read_text(encoding="utf8").split())


def katalog(ev):
    satirlar, _ = ajan_katalog.uret(ev)
    y = ev / "skills" / "ajan-getir" / "katalog.tsv"
    if y.parent.is_dir():
        y.write_text("ad\tmodel\ttek_satir\tyol\n" + "".join("\t".join(s) + "\n" for s in satirlar), encoding="utf-8", newline="\n")
    return len(satirlar)


def main(argv=None, ev=Path.home() / ".claude"):
    a = (argv if argv is not None else sys.argv[1:]) or ["--kuru"]
    ag, ak = ev / "agents", ev / "agents-katalog"
    if a[0] == "--geri":
        n = 0
        for p in sorted(ak.glob("*.md")) if ak.is_dir() else []:
            if not (ag / p.name).exists():  # aynı adla yeni kurulan varsa ona dokunma, katalogda kalır
                shutil.move(str(p), ag / p.name); n += 1
        if ak.is_dir() and not any(ak.iterdir()):
            ak.rmdir()
        print("geri:", n, "ajan agents/'a döndü · katalog", katalog(ev)); return 0
    tasinacak = [p for p in sorted(ag.glob("*.md")) if p.stem not in CEKIRDEK]
    eksik = sorted(CEKIRDEK - {p.stem for p in ag.glob("*.md")} - {p.stem for p in ak.glob("*.md")})
    if a[0] != "uygula":
        print(f"KURU: listede kalır {len(CEKIRDEK) - len(eksik)} · taşınacak {len(tasinacak)} -> {ak} · çekirdekte bulunmayan {eksik}"); return 0
    ak.mkdir(exist_ok=True)
    for p in tasinacak:
        shutil.move(str(p), ak / p.name)
    print("uygulandı:", len(tasinacak), "ajan agents-katalog/'a · katalog", katalog(ev), "· geri: --geri"); return 0


if __name__ == "__main__":
    sys.exit(main())
