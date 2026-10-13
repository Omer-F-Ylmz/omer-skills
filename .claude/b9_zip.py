"""BİRLEŞTİR-9: dist/tasarim-3a/frontend-craft.zip birleşik main'in HEAD blob'larından (LF; çalışma ağacı CRLF'si girmez, node_modules izsiz)."""
import io, subprocess, sys, tarfile, tempfile
from pathlib import Path

WT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WT / "tools" / "skill-paket"))
import paketle

KAYNAK = "plugins/frontend-craft/skills/frontend-craft"
tar = subprocess.run(["git", "-C", str(WT), "archive", "HEAD", KAYNAK], capture_output=True, check=True).stdout
with tempfile.TemporaryDirectory() as t:
    tarfile.open(fileobj=io.BytesIO(tar)).extractall(t)
    print(paketle.paketle("frontend-craft", "Frontend UI tasarım ve uygulama: yön keşfi, DESIGN.md, slop denetimi, vitrin teknikleri (ajans/portfolyo/SaaS)",
                          [str(Path(t) / KAYNAK)], str(WT / "dist" / "tasarim-3a")))
