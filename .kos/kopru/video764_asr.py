"""Hafif ASR: yalnız ses→Groq (OCR/kare/link derinliği yok). tools/video venv'iyle: python video764_asr.py <cache-id>"""
import os, sys
from pathlib import Path
from video import cli
d = Path(os.environ.get("VIDEO_CACHE") or cli.KOK) / sys.argv[1]
import json
meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
ctx = {"env": os.environ, "kos": cli.kos, "http": cli._http, "kok": d.parent}
seg, kaynak = cli._asr(ctx, d, meta.get("duration") or 0, "en", "")
print(kaynak, len(seg or []))
