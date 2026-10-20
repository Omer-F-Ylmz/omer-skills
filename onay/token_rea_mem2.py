"""TOKEN-REA mem2 onay betiği — Desktop koşar (Ömer onayından sonra). claude-mem aramasına worker'sız salt-okur FTS5 yolu (`mem2.py`: 0.056 sn vs 0.228 sn · 140 vs 204 tok · isabet 0.93 vs 0.91, held-out 20102403)
kural satırı ekler: ~/.claude/CLAUDE.md ve repo CLAUDE.md sonuna tek satır; mem-search KALDIRILMAZ (boş/yetersizse yedek). Eski hal ev/yedek-token-rea-mem2/ altına kopyalanır; --geri yalnız bu satırı çıkarır.

  python onay/token_rea_mem2.py --kuru   # plan (varsayılan)
  python onay/token_rea_mem2.py uygula   # yedekle + satırı ekle
  python onay/token_rea_mem2.py --geri   # satırı çıkar"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SATIR = ('- mem2 (TOKEN-REA): önceki oturum bilgisi için `mem-search` yerine önce `python -I -S .kos/kopru/token-rea/mem2.py "<soru>"` '
         '(≤0.1 sn, ~140 tok, #ID listesi; ayrıntı get_observations); boş/yetersizse `mem-search`.')


def hedefler(ev, kok):
    return [(ev / "CLAUDE.md", ev / "yedek-token-rea-mem2" / "ev-CLAUDE.md"), (kok / "CLAUDE.md", ev / "yedek-token-rea-mem2" / "repo-CLAUDE.md")]


def main(argv=None, ev=Path.home() / ".claude", kok=KOK):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    s = SATIR.encode("utf-8")
    for md, yedek in hedefler(ev, kok):
        ham = md.read_bytes() if md.exists() else b""
        if mod == "--kuru":
            print(f"{md}: {'zaten var' if s in ham else 'satır eklenecek'}")
        elif mod == "uygula" and s not in ham:
            yedek.parent.mkdir(parents=True, exist_ok=True)
            if not yedek.exists(): yedek.write_bytes(ham)
            md.write_bytes(ham + (b"" if ham.endswith(b"\n") or not ham else b"\n") + s + b"\n")  # bayt: write_text CRLF'ye çevirir
        elif mod == "--geri" and s in ham:
            md.write_bytes(ham.replace(s + b"\n", b"").replace(s, b""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
