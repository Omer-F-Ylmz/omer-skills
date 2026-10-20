"""d16: CLAUDE.md birleştirmesinin önce/sonra gerçek token'ı (1 claude -p başlık yakalama + count_tokens). Yalnız sayı yazar.
Önce = yedek-token-rea-mem2/ dosyaları, sonra = güncel dosyalar."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import taban  # noqa: E402

ev = Path.home() / ".claude"
taban.GOVDE, taban.BASLIK = taban.kur_baslik()
for ad, onc, son in (("global", ev / "yedek-token-rea-mem2" / "ev-CLAUDE.md", ev / "CLAUDE.md"),
                     ("repo", ev / "yedek-token-rea-mem2" / "repo-CLAUDE.md", taban.KOK / "CLAUDE.md")):
    a, b = taban.tok(onc.read_text(encoding="utf-8")), taban.tok(son.read_text(encoding="utf-8"))
    print(ad, "önce", a, "sonra", b, "fark", b - a)
