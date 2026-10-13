"""TOKEN-12 onay betiği — Desktop koşar (Ömer onayından sonra). TOKEN-10 betiğinin aynısı, eşleme docs/token-12/esleme.tsv:
kaynaksız 87 agency-agents ajanının ~/.claude/agents/<ad>.md description satırı sıkışmış metinle değişir; gövde/model/ad değişmez,
ajan silinmez. d4: + onarim.tsv (kendi 2 ajan, ara-arac-degerlendirme/ara-repo-karsilastirma; repo kaynağıyla aynı). Eski hal ~/.claude/agents-yedek-token12/'ye yedeklenir; tam orijinal metinler ayrıca docs/token-12/orijinal.tsv'de.

  python onay/token_12_uygula.py --kuru   # plan: değişecek / bulunmayan sayısı (varsayılan)
  python onay/token_12_uygula.py uygula   # yedekle + description değiştir + ajan-getir katalog yenile
  python onay/token_12_uygula.py --geri   # yedekten geri yükle + katalog yenile"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import token_10_uygula as t10  # noqa: E402

ESLEME = t10.KOK / "docs" / "token-12" / "esleme.tsv"
ONARIM = ESLEME.with_name("onarim.tsv")


def main(argv=None, ev=Path.home() / ".claude", es=None):
    return t10.main(argv, ev, es if es is not None else {**t10.esleme(ESLEME), **t10.esleme(ONARIM)}, "agents-yedek-token12")


if __name__ == "__main__":
    sys.exit(main())
