import os, runpy, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".kos", "kopru"))
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".kos", "kopru", "gpu_sinir_olcum.py"), run_name="__main__")
