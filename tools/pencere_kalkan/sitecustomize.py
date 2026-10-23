import sys
if sys.platform == "win32":
    try:
        import ctypes, subprocess
        if not ctypes.windll.kernel32.GetConsoleWindow():
            _orig_init = subprocess.Popen.__init__
            def _gizli_init(self, *a, **k):
                if not k.get("creationflags", 0) & 0x00000010:
                    k["creationflags"] = k.get("creationflags", 0) | 0x08000000
                _orig_init(self, *a, **k)
            subprocess.Popen.__init__ = _gizli_init
    except Exception:
        pass
