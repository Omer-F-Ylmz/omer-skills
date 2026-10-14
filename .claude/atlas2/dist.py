"""ATLAS-2: değişen departman skill'leri + atıf yaptıkları kitaplar → dist/claude-ai-25 (yöntem .claude/atlas/dist.py)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "atlas"))
import dist  # noqa: E402

dist.DIST, dist.BASLIK = dist.KOK / "dist" / "claude-ai-25", "ATLAS-2"
K = "docs/atlas/kart.jsonl"
dist.EK = {"departman-guvenlik": ["docs/atlas/guvenlik-test.md", K], "departman-test-qa": ["docs/atlas/guvenlik-test.md", K],
           "departman-arastirma-ogrenme": ["docs/atlas/video-icerik.md", K], "departman-belge": ["docs/atlas/belge-sunum.md", K]}
sys.exit(dist.main())
