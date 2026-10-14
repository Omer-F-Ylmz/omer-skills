"""Test vekili: headroom proxy + _breakpoint_index yer değiştirmelerini K1_IZ dosyasına yazar.
Kullanım (runtime venv python'u): python k1_vekil.py proxy --port 6769 --no-http2 --no-rate-limit"""
import os, sys, time
import headroom.cache.prefix_tracker as pt

_asil, _iz = pt._breakpoint_index, os.environ["K1_IZ"]

def _sarili(content, message, message_index, previous):
    i = _asil(content, message, message_index, previous)
    with open(_iz, "a", encoding="utf-8") as f:
        f.write(f"{time.time():.3f}\t{message_index}\t{len(content)}\t{i}\t{int(i != len(content) - 1)}\n")
    return i

pt._breakpoint_index = _sarili
from headroom.cli import main
sys.argv[0] = "headroom"
main()
