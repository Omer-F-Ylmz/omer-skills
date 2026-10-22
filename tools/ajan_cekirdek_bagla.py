"""AJAN-AKIS-1: ~/.claude/agents/*.md içinden yalnız model: haiku|sonnet profillerinin sonuna iş-akışı çekirdeğini (tools/ajan_cekirdek.md) işaretli blok olarak yazar.
Tek kaynak değişince yeniden çalıştırmak bloğu günceller (idempotent); opus/modelsiz profile dokunmaz.
  python tools/ajan_cekirdek_bagla.py            → kuru koşu (kaç dosya değişir)
  python tools/ajan_cekirdek_bagla.py --uygula   → yazar"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ajan_cekirdek as ac  # noqa: E402

ACIL, KAPA = "<!-- ajan-cekirdek -->", "<!-- /ajan-cekirdek -->"
BLOK_RE = re.compile(re.escape(ACIL) + r".*?" + re.escape(KAPA) + r"\n?", re.S)


def bagla(metin):
    m = re.search(r"(?m)^model:\s*(\w+)", metin.split("\n---", 2)[0] if metin.startswith("---") else "")
    if not m or m.group(1) not in ("haiku", "sonnet"):
        return metin
    blok = f"{ACIL}\n{ac.onek().strip()}\n{KAPA}\n"
    if BLOK_RE.search(metin):
        return BLOK_RE.sub(lambda _: blok, metin, count=1)
    return metin.rstrip("\n") + "\n\n" + blok


if __name__ == "__main__":
    degisen = 0
    for p in sorted((Path.home() / ".claude/agents").glob("*.md")):
        eski = p.read_bytes().decode("utf-8")
        yeni = bagla(eski.replace("\r\n", "\n"))
        if yeni != eski.replace("\r\n", "\n"):
            degisen += 1
            if "--uygula" in sys.argv:
                p.write_bytes((yeni.replace("\n", "\r\n") if "\r\n" in eski else yeni).encode("utf-8"))
    print(("yazıldı" if "--uygula" in sys.argv else "değişecek"), degisen)
