"""TOKEN-REA bağlam diyeti onay betiği — Desktop koşar (Ömer onayından sonra). claude-mem SessionStart enjeksiyonunu 15 → 6 gözleme indirir
(~2k token/oturum, her istekte cache okuma; hiçbir araç kapanmaz, tam geçmiş `mem-search` ile erişilir). Eski hal ev/yedek-token-rea-baglam/ içine kopyalanır.

  python onay/token_rea_baglam.py --kuru   # plan (varsayılan)
  python onay/token_rea_baglam.py uygula   # yedekle + 15 → 6
  python onay/token_rea_baglam.py --geri   # yedekten geri yükle"""
import shutil
import sys
from pathlib import Path

ESKI, YENI = b'"CLAUDE_MEM_CONTEXT_OBSERVATIONS": "15"', b'"CLAUDE_MEM_CONTEXT_OBSERVATIONS": "6"'


def main(argv=None, ev=Path.home() / ".claude", mem=Path.home() / ".claude-mem" / "settings.json"):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    yedek = ev / "yedek-token-rea-baglam" / "claude-mem-settings.json"
    ham = mem.read_bytes()
    if mod == "--kuru":
        print(f"{mem}: {'15 -> 6 yapilacak' if ESKI in ham else 'zaten uygulanmis ya da farkli deger'}")
    elif mod == "uygula" and ESKI in ham:
        yedek.parent.mkdir(parents=True, exist_ok=True)
        if not yedek.exists(): yedek.write_bytes(ham)
        mem.write_bytes(ham.replace(ESKI, YENI))  # bayt: write_text CRLF'ye çevirir
    elif mod == "--geri" and yedek.exists():
        shutil.copyfile(yedek, mem)
    return 0


if __name__ == "__main__":
    sys.exit(main())
