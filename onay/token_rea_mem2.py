"""TOKEN-REA mem2 onay betiği — Desktop koşar (Ömer onayından sonra). claude-mem aramasına worker'sız salt-okur FTS5 yolu (`mem2.py`: 0.056 sn vs 0.228 sn · 140 vs 204 tok · isabet 0.93 vs 0.91, held-out 20102403).
d16 kararı: global CLAUDE.md'ye satır EKLENMEZ. Repo CLAUDE.md'deki sor2 satırı sor2+mem2 tek satırla değişir; ~/.claude/CLAUDE.md'deki ikilenmiş sor2 satırı çıkar.
Eski hal ev/yedek-token-rea-mem2/ altına kopyalanır; --geri satırı sor2'ye çevirir ve global'e sor2 satırını geri koyar (mem-search/graphify KALDIRILMAZ).

  python onay/token_rea_mem2.py --kuru   # plan (varsayılan)
  python onay/token_rea_mem2.py uygula   # yedekle + birleştir
  python onay/token_rea_mem2.py --geri   # sor2 satırlarını geri koy"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from token_rea_sor2 import SATIR as SOR2  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
SATIR = ('- sor2/mem2 (TOKEN-REA): omer-skills kod sorusunda `graphify query`, önceki oturum bilgisinde `mem-search` yerine önce '
         '`python -I -S .kos/kopru/token-rea/sor2.py "<soru>"` / `.../mem2.py "<soru>"` (≤1.5k / ~140 tok; sor2 `--genis` havuzla genişletir; '
         'mem2 #ID listesi, ayrıntı get_observations); boş/yetersizse eski araç.')


def main(argv=None, ev=Path.home() / ".claude", kok=KOK):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    s, o = SATIR.encode("utf-8"), SOR2.encode("utf-8")
    yd = ev / "yedek-token-rea-mem2"
    for md, ad, repo in ((ev / "CLAUDE.md", "ev-CLAUDE.md", False), (kok / "CLAUDE.md", "repo-CLAUDE.md", True)):
        ham = md.read_bytes() if md.exists() else b""
        yeni = ham
        if repo and mod in ("--kuru", "uygula"):
            if s not in ham:
                yeni = ham.replace(o, s) if o in ham else ham + (b"" if ham.endswith(b"\n") or not ham else b"\n") + s + b"\n"
        elif not repo and mod in ("--kuru", "uygula"):
            yeni = ham.replace(o + b"\n", b"").replace(o, b"")
        elif mod == "--geri":
            if repo:
                yeni = ham.replace(s, o)
            elif o not in ham:
                yeni = ham + (b"" if ham.endswith(b"\n") or not ham else b"\n") + o + b"\n"  # bayt: write_text CRLF'ye çevirir
        if mod == "--kuru":
            print(f"{md}: {'değişecek' if yeni != ham else 'zaten uygulanmış'}")
        elif yeni != ham:
            yd.mkdir(parents=True, exist_ok=True)
            if mod == "uygula" and not (yd / ad).exists(): (yd / ad).write_bytes(ham)
            md.write_bytes(yeni)
    return 0


if __name__ == "__main__":
    sys.exit(main())
