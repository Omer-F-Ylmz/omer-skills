import json
import subprocess
import tempfile
import time
from pathlib import Path

MASAUSTU = Path.home() / "Desktop"
DURUM = Path(tempfile.gettempdir()) / "blender-oturum.json"
SONUC = Path(tempfile.gettempdir()) / "blender-oturum-sonuc.json"


def main(argv=None):
    raise NotImplementedError
