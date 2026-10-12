"""BİRLEŞTİR-3: plugins/blender skill'leri skills/blender-* ile birebir (CC eklenti kopyası sapmasın) + marketplace girdisi."""
import json
import subprocess
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def test_eklenti_kopyasi_kaynakla_ayni():
    kaynak = subprocess.run(["git", "ls-files", "skills/blender-oturum", "skills/blender-uretim"],
                            cwd=KOK, capture_output=True, text=True, check=True).stdout.split()
    assert kaynak
    for f in kaynak:
        assert (KOK / "plugins/blender" / f).read_bytes() == (KOK / f).read_bytes(), f


def test_marketplace_blender_girdisi():
    mj = json.loads((KOK / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    pj = json.loads((KOK / "plugins/blender/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
    g = next(p for p in mj["plugins"] if p["name"] == "blender")
    assert g["source"] == "./plugins/blender" and g["version"] == pj["version"] and pj["name"] == "blender"
