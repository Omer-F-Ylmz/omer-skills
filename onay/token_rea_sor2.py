"""TOKEN-REA sor2 onay betiği — Desktop koşar (Ömer onayından sonra). `graphify query` yanına `sor2` (10/10 vs 6/10 · 628 vs 3647 tok · ~0.4 sn vs 3.8 sn) kural satırı ekler:
~/.claude/CLAUDE.md ve repo CLAUDE.md sonuna tek satır; graphify KALDIRILMAZ (yedek yol). Eski hal ev/yedek-token-rea-sor2/ ve repo yedeğine kopyalanır.

  python onay/token_rea_sor2.py --kuru   # plan (varsayılan)
  python onay/token_rea_sor2.py uygula   # yedekle + satırı ekle
  python onay/token_rea_sor2.py --geri   # yedekten geri yükle"""
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SATIR = ('- sor2 (TOKEN-REA): omer-skills kod sorusunda `graphify query` yerine önce '
         '`python -I -S .kos/kopru/token-rea/sor2.py "<soru>"` (≤1.5k tok, ~0.4 sn; `--genis` havuzla sorgu genişletir); boş/yetersizse `graphify query`.')


def hedefler(ev, kok):
    return [(ev / "CLAUDE.md", ev / "yedek-token-rea-sor2" / "ev-CLAUDE.md"), (kok / "CLAUDE.md", ev / "yedek-token-rea-sor2" / "repo-CLAUDE.md")]


def main(argv=None, ev=Path.home() / ".claude", kok=KOK):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    for md, yedek in hedefler(ev, kok):
        ham = md.read_bytes() if md.exists() else b""
        if mod == "--kuru":
            print(f"{md}: {'zaten var' if SATIR.encode('utf-8') in ham else 'satır eklenecek'}")
        elif mod == "uygula" and SATIR.encode("utf-8") not in ham:
            yedek.parent.mkdir(parents=True, exist_ok=True)
            if not yedek.exists(): yedek.write_bytes(ham)
            md.write_bytes(ham + (b"" if ham.endswith(b"\n") or not ham else b"\n") + SATIR.encode("utf-8") + b"\n")  # bayt: write_text CRLF'ye çevirir
        elif mod == "--geri" and yedek.exists():
            shutil.copyfile(yedek, md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
