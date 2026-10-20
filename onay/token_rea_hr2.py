"""TOKEN-REA hr2 onay betiği — Desktop koşar (Ömer onayından sonra). Headroom yanına `hr2` (ML'siz şablon-satır çökertici) kural satırı ekler:
~/.claude/CLAUDE.md ve repo CLAUDE.md sonuna tek satır; Headroom KALDIRILMAZ. Held-out 2010206: token Headroom -42.6 → hr2 -97.0 (sentetik tekrarlı yük), kalite 10/10, ort 0.10 sn, 16 MB, 0 PASSTHROUGH.
SINIR: gerçek git çıktısında kazanç ~0-6% (log --stat 0, ls-files -6%); yalnız çok tekrarlı log/json/arama çıktısında anlamlı. Eski hal ev/yedek-token-rea-hr2/ altına kopyalanır.

  python onay/token_rea_hr2.py --kuru   # plan (varsayılan)
  python onay/token_rea_hr2.py uygula   # yedekle + satırı ekle
  python onay/token_rea_hr2.py --geri   # yedekten geri yükle"""
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
SATIR = ('- hr2 (TOKEN-REA): çok tekrarlı uzun çıktıyı (≥100 benzer satır: log, JSON dizisi, arama, fark) bağlama almadan önce '
         '`<komut> | python -I -S .kos/kopru/token-rea/hr2.py`; sapan satırlar aynen kalır, tam metin özetteki `hr2.py ac <id>` ile; kısa/çeşitli çıktıda gerekmez.')


def hedefler(ev, kok):
    return [(ev / "CLAUDE.md", ev / "yedek-token-rea-hr2" / "ev-CLAUDE.md"), (kok / "CLAUDE.md", ev / "yedek-token-rea-hr2" / "repo-CLAUDE.md")]


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
