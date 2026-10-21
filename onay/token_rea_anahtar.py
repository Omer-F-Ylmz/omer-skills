"""TOKEN-REA d20b kayıt-zamanı anahtar modu onay betiği — Desktop koşar (Ömer onayından sonra). claude-mem'i `code--anahtar` moduna alır:
yeni gözlemlerin subtitle'ına " | TR: ... | EN: ..." anahtar satırı yazılır (FTS + Chroma metni bunu içerir; TR↔EN paraphrase isabeti için).
Mod dosyası ~/.claude-mem/modes/ altına yazılır (güncellemede kalır, claude-mem koduna dokunulmaz); sadece YENİ gözlemleri etkiler.
Eski hal ev/yedek-token-rea-anahtar/ içine kopyalanır.

  python onay/token_rea_anahtar.py --kuru   # plan + işaretli gözlem sayısı (varsayılan)
  python onay/token_rea_anahtar.py uygula   # mod dosyası + CLAUDE_MEM_MODE code -> code--anahtar
  python onay/token_rea_anahtar.py --geri   # yedekten geri yükle, mod dosyasını kaldır"""
import json
import shutil
import sqlite3
import sys
from pathlib import Path

ESKI, YENI = b'"CLAUDE_MEM_MODE": "code"', b'"CLAUDE_MEM_MODE": "code--anahtar"'
ISARET = " | TR:"
MOD = {
    "name": "Code Development (TR+EN keywords)",
    "prompts": {
        "xml_subtitle_placeholder": (
            "[**subtitle**: One sentence explanation (max 24 words), then append exactly "
            "' | TR: <3-5 Turkish keywords> | EN: <3-5 English keywords>'. Give BOTH languages on every observation "
            "regardless of the language you write in; keywords are the terms a person would search with "
            "(synonyms and translations of the key concepts, tool and file names kept as they are)]"
        )
    },
}


def isaretli(mem):
    db = mem.parent / "claude-mem.db"
    if not db.exists(): return None
    c = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    try:
        return c.execute("SELECT count(*) FROM observations WHERE subtitle LIKE ?", (f"%{ISARET} %",)).fetchone()[0]
    finally:
        c.close()


def main(argv=None, ev=Path.home() / ".claude", mem=Path.home() / ".claude-mem" / "settings.json"):
    mod = (argv if argv is not None else sys.argv[1:] or ["--kuru"])[0]
    yedek = ev / "yedek-token-rea-anahtar" / "claude-mem-settings.json"
    dosya = mem.parent / "modes" / "code--anahtar.json"
    ham = mem.read_bytes()
    if mod == "--kuru":
        print(f"{mem}: {'code -> code--anahtar yapilacak' if ESKI in ham else 'zaten uygulanmis ya da farkli mod'}; isaretli gozlem: {isaretli(mem)}")
    elif mod == "uygula" and ESKI in ham:
        yedek.parent.mkdir(parents=True, exist_ok=True)
        if not yedek.exists(): yedek.write_bytes(ham)
        dosya.parent.mkdir(parents=True, exist_ok=True)
        dosya.write_bytes(json.dumps(MOD, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")  # bayt: write_text CRLF'ye çevirir
        mem.write_bytes(ham.replace(ESKI, YENI))
    elif mod == "--geri" and yedek.exists():
        shutil.copyfile(yedek, mem)
        dosya.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
