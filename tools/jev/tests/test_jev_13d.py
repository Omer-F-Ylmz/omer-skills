"""KURULUM-13d: ortak aday listesi (köprü katalog ile aynı fixture), hook.log, çağrı başına tam +1, aşama etiketi."""
import io
import json
import sys
from datetime import datetime
from pathlib import Path

from jev import cli
from jev import skill as sk
from test_jev_13c import ADAY, HOOK_ENV, Kayit, _yaz
from test_jev_cekirdek import ENV, OR_ANAHTAR

FIXTURE = Path(__file__).parent / "veri" / "skill_agaci.json"
GIZLI = "GIZLI-ISTEM-7f3a PDF fatura"
GUN = "2026-09-23"


def kur(ev):
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for rel, icerik in f["dosyalar"].items():
        (ev / rel).parent.mkdir(parents=True, exist_ok=True)
        (ev / rel).write_text(icerik.replace("{EV}", ev.as_posix()), encoding="utf-8")
    for rel in f["skilller"]:
        _yaz(ev / rel, Path(rel).name, f"{Path(rel).name} açıklama")
    return f["beklenen"]


def test_ortak_fixture_aday_kumesi(tmp_path):
    beklenen = kur(tmp_path)
    assert [a for a, _ in sk.adaylar(tmp_path)] == beklenen
    assert [a for a, _ in sk.adaylar(tmp_path)] == beklenen  # önbellekten aynı küme


def test_onbellek_yeni_skill_klasoru_imzayi_bozar(tmp_path):
    kur(tmp_path)
    sk.adaylar(tmp_path)
    _yaz(tmp_path / ".claude" / "skills" / "yerel3", "yerel3", "yeni")
    assert "yerel3" in dict(sk.adaylar(tmp_path))


def _h(ev, g, env=HOOK_ENV, saat=None, prompt=GIZLI):
    kw = {"saat": saat} if saat else {}
    return sk.hook(json.dumps({"prompt": prompt}), env, ev=ev, gonder=g, bugun=GUN, aday=ADAY, **kw)


def _log(ev):
    return (ev / ".config" / "jev" / "hook.log").read_text(encoding="utf-8").splitlines()


def test_hook_log_her_sonuc_bir_satir_istem_ad_anahtar_yok(tmp_path):
    _h(tmp_path, Kayit(), env=ENV)
    _h(tmp_path, Kayit(hata=RuntimeError(GIZLI)))
    zaman = iter([0.0] + [10.0] * 50)
    _h(tmp_path, Kayit(hata=TimeoutError()), saat=lambda: next(zaman))
    _h(tmp_path, Kayit({"skill-001": 0.9}, p={"skill-001": 0.7}))
    assert _h(tmp_path, Kayit({"skill-001": 0.9}, p={"skill-001": 0.95}))
    _h(tmp_path, Kayit(), env={**HOOK_ENV, "JEV_SKILL_GUNLUK": "1"})
    satirlar = _log(tmp_path)
    assert [s.split()[2] for s in satirlar] == ["sessiz-kapı", "hata", "zaman-aşımı", "act-yok", "öneri", "sessiz-tavan"]
    for s in satirlar:
        zaman_, ms, _, n = s.split()
        datetime.fromisoformat(zaman_)
        assert int(ms) >= 0 and int(n) in (0, len(ADAY))
    metin = "\n".join(satirlar)
    assert "GIZLI" not in metin and "fatura" not in metin and "skill-001" not in metin and OR_ANAHTAR not in metin


def test_hook_log_500_satirda_doner(tmp_path):
    yol = tmp_path / ".config" / "jev" / "hook.log"
    yol.parent.mkdir(parents=True)
    yol.write_text("".join(f"2026-09-22T00:00:00+03:00 {i} öneri 1\n" for i in range(500)), encoding="utf-8")
    _h(tmp_path, Kayit(hata=RuntimeError("x")))
    s = _log(tmp_path)
    assert len(s) == 500 and s[0].split()[1] == "1" and s[-1].split()[2] == "hata"


def test_hook_durum_p50_p95(tmp_path, monkeypatch, capsys):
    satirlar = [f"2026-09-23T01:00:00+03:00 {i} {'zaman-aşımı' if i > 18 else 'öneri'} 347" for i in range(1, 21)]
    d = sk.hook_durum(satirlar)
    assert d == {"n": 20, "p50": 10.5, "p95": 19, "sonuc": {"öneri": 18, "zaman-aşımı": 2}}
    yol = tmp_path / ".config" / "jev" / "hook.log"
    yol.parent.mkdir(parents=True)
    yol.write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    assert cli.main(["hook-durum", "-n", "10"], env={}) == 0
    out = capsys.readouterr().out
    assert "15.5" in out and "20%" in out and "çağrı" not in out


def test_tek_hook_cagrisi_gunluk_tam_1(tmp_path, monkeypatch):
    yol = tmp_path / ".config" / "jev" / "gunluk.json"
    _h(tmp_path, Kayit())
    assert json.loads(yol.read_text(encoding="utf-8")) == {GUN: 1}
    _h(tmp_path, Kayit(hata=RuntimeError("x")))
    assert json.loads(yol.read_text(encoding="utf-8")) == {GUN: 2}
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"prompt": "x"})))
    monkeypatch.setattr(sk, "adaylar", lambda ev=None: ADAY)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(sk, "date", type("D", (), {"today": staticmethod(lambda: datetime(2026, 9, 23).date())}))
    cli.main(["hook"], env=HOOK_ENV, gonder=Kayit(), uyu=lambda s: None)
    assert json.loads(yol.read_text(encoding="utf-8")) == {GUN: 3}
    assert len(_log(tmp_path)) == 3


def test_skill_cikti_asama_basina_cagri_istek(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sk, "adaylar", lambda ev=None: ADAY)
    g = Kayit({"skill-001": 0.6}, p={"skill-001": 0.95})
    assert cli.main(["skill", "x"], env=ENV, gonder=g, uyu=lambda s: None) == 0
    out = capsys.readouterr().out
    assert "aşama 1: 1 çağrı · 1 istek · aşama 2: 1 çağrı · 1 istek" in out and "batch" not in out
    assert cli.main(["skill", "x", "--json"], env=ENV, gonder=g, uyu=lambda s: None) == 0
    assert json.loads(capsys.readouterr().out)["cagri"]["asama"] == {"1": [1, 1], "2": [1, 1]}
