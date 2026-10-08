"""MÜKEMMEL-1c (O79): baslat DUR · --a-yolu CLI · üretim YONLENDIRME varsayılanı."""
import importlib.util

import pytest

from video import cli
from video import parti as pt
from video import yonlendir as yon
from test_derinlik_kapanis import ROTA10, V, Sahte, _ctx, _kurulum, _ns


# 4: baslat da motoru koşturur; OmniRoute/anahtar yoksa çağrı 0, DUR (rc 4)
def test_baslat_omni_yok_dur_cagri_0(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(pt, "YONLENDIRME", ROTA10)
    monkeypatch.setattr(pt, "YOKLA", lambda *a, **k: "OMNIROUTE_KEY yok", raising=False)
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: pytest.fail("DUR'da tara_v10 çağrılmaz"))
    _kurulum(tmp_path, V[:1], sure=300)
    s = Sahte()
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _ctx(tmp_path, s)) == 4
    assert s.cagrilar == [] and "DUR: OmniRoute/anahtar yok (OMNIROUTE_KEY yok)" in capsys.readouterr().out


# 3: "video parti devam <pid> --a-yolu" → ns.a_yolu True; bayraksız False
@pytest.mark.parametrize("ek, beklenen", [(["--a-yolu"], True), ([], False)])
def test_a_yolu_cli(monkeypatch, ek, beklenen):
    yakala = []
    monkeypatch.setattr(cli.pt, "parti", lambda ns, ctx: yakala.append(ns) or 0)
    cli.main(["parti", "devam", "2026-10-06-short", *ek], env={})
    assert yakala[0].a_yolu is beklenen


# 2: conftest {} yamasından bağımsız — parti.py'nin taze kopyasındaki gerçek değer ROTA10
def test_uretim_yonlendirme_rota10():
    spec = importlib.util.spec_from_file_location("video._parti_kopya", pt.__file__)
    spec.loader.exec_module(kopya := importlib.util.module_from_spec(spec))
    assert kopya.YONLENDIRME == {"tarama": {"yontem": "ikili", "modeller": ["claude-sonnet-5-5", "claude-haiku-5-5"]}}  # 1b-2a KAPANIŞ: varsayılan kurgu 2 (V10 geri alma notu parti.py'de)
