"""DERİNLİK-MASTER O11 (5): aday sayısı ile model tavanı ayrı (Ömer kararı, 4 Eki) — --kare aday tabanı, --model-tavan model karesi."""

import json
import re
from pathlib import Path

from video import cli
from video.cli import main
from test_c3 import OcrKos
from test_video import VID, onbellek, ortam  # noqa: F401 (ortam fixture)

SAHNE = [[10.0 + 23 * i, round(0.99 - i / 100, 2)] for i in range(51)]  # 51 sahne; skor sırası = zaman sırası; merkezlerle çakışmaz


def kos(ortam, monkeypatch, *ek):
    onbellek(ortam, [], duration=1200)
    d = Path(ortam["VIDEO_CACHE"]) / VID
    (d / "sahne.json").write_text(json.dumps({"durum": "✓", "sahneler": SAHNE}), encoding="utf-8")
    zam, asil = [], cli._kare_uret
    monkeypatch.setattr(cli, "_kare_uret", lambda *a: (zam.append(a[3]), asil(*a))[1])
    assert main(["paket", VID, "--kare", "8", "--istek-tavan", "0", "--kare-yalniz", *ek], env=ortam, kos=OcrKos({}), uyku=lambda s: None) == 0
    return zam, json.loads((d / "kapsam.json").read_text(encoding="utf-8"))


def test_51_sahneli_20dk_aday_tum_sahneler_arti_8_merkez(ortam, monkeypatch):
    zam, _ = kos(ortam, monkeypatch, "--model-tavan", "60")
    assert len(zam) == 51 + 8  # eskisi: 8 + max(2*8, 20) sahne = 28


def test_aday_ust_asilinca_sahneler_skor_sirasiyla_kesilir(ortam, monkeypatch):
    monkeypatch.setattr(cli, "ADAY_UST", 30)
    zam, kj = kos(ortam, monkeypatch, "--model-tavan", "60")
    assert len(zam) == 30 and {int(t) for t in zam} >= {int(t) for t, _ in SAHNE[:22]}
    assert sorted(t for t, s in kj["incelenmedi"] if s == "aday tavanı") == [t for t, _ in SAHNE[22:]]


def test_model_tavan_ayri_butce_sinirli_varsayilan_eski_davranis(ortam, monkeypatch):
    _, kj = kos(ortam, monkeypatch, "--model-tavan", "60")
    assert int(re.search(r"model (\d+)", kj["izleme"])[1]) > 8
    _, kj = kos(ortam, monkeypatch)
    assert int(re.search(r"model (\d+)", kj["izleme"])[1]) == 8 and any(s == "kare tavanı 8" for _, s in kj["incelenmedi"])
