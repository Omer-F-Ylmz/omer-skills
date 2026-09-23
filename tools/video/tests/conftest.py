import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK), str(KOK.parent / "jev")]
