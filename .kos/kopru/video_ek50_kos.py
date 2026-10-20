"""VIDEO-EK-50: video764_kos.py'yi ek-50 listesiyle koşar (karar adımı yok): python video_ek50_kos.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import video764_kos as V
V.LISTE = V.R / ".kos/kopru/devir/video-ek50-sira.txt"
V.kos(len(V.liste()))
