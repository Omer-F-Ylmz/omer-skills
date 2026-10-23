"""Öğrenme döngüsünde Claude çağrısı 0 (K2n a): canlı döngü dosyaları claude/haiku/kosucu çağırmaz; kanca._damit ücretsiz havuza gider."""
import re
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
DONGU = ["tools/beyin_dusun.py", "tools/beyin_kayit.py", "tools/beyin.py", "tools/ucuz_alt.py", "tools/ogrenme/kanca.py",
         "tools/ogrenme/ders.py", "tools/ogrenme/sinav.py", "tools/ogrenme/onsoz.py"]
YASAK = re.compile(r"import kosucu|kosucu\.kos|\[\s*\"claude\"|shutil\.which\(\"claude\"\)|claude -p --model|haiku_tavan\s*=\s*[1-9]")


@pytest.mark.parametrize("yol", DONGU)
def test_dongu_dosyasinda_claude_cagrisi_yok(yol):
    kod = "\n".join(s for s in (KOK / yol).read_text(encoding="utf-8").splitlines() if not s.lstrip().startswith("#"))
    assert not YASAK.search(kod)


def test_damit_ucretsiz_havuza_gider(monkeypatch):
    sys.path.insert(0, str(KOK / "tools")); sys.path.insert(0, str(KOK / "tools" / "ogrenme"))
    import kanca
    import ucretsiz_havuz as H
    gorulen = {}
    monkeypatch.setattr(H, "cagir", lambda tur, istem, **kw: gorulen.update(kw) or ("[]", "havuz/x", []))
    assert kanca._damit("istem") == "[]" and gorulen["haiku_tavan"] == 0
    monkeypatch.setattr(H, "cagir", lambda tur, istem, **kw: (None, None, ["429"]))
    with pytest.raises(RuntimeError):
        kanca._damit("istem")
