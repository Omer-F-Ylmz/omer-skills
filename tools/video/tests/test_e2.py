"""DERİNLİK-MASTER E2: denetim.md "## Desktop" şablonu → `video parti denetim-isle <id>` → desktop-denetim.jsonl + aday dosyası.
Satır: `- <aday|video> · <tür> · <URL> · <açıklama>`; hoşgörülü okuma; okunamayan satır sessiz düşmez (rc 1); tekrar işlenmez."""
import json

from test_e1 import _d, _karar, _z

from video import akil as ak
from video import tarama as tr


def _kur(tmp_path, *satir):
    p = tmp_path / "docs" / "kurulumlar" / "parti" / "p1"
    p.mkdir(parents=True)
    (p / "denetim.md").write_text(ak.denetim_md(_d(), _z(), _karar()) + "".join(s + "\n" for s in satir), encoding="utf-8")
    a = tmp_path / "docs" / "kurulumlar" / "adaylar"
    a.mkdir(parents=True)
    for k in ("a0", "a2"):
        (a / f"{k}.md").write_text(f"# {k}\n## Kurulum\n- x\n", encoding="utf-8")
    return tmp_path


def _j(kok):
    y = kok / "docs" / "kurulumlar" / "desktop-denetim.jsonl"
    return [json.loads(s) for s in y.read_text(encoding="utf-8").splitlines()] if y.is_file() else []


def test_sablon_bicim_ve_turler():
    t = tr.bolum(ak.denetim_md(_d(), _z(), _karar()), "Desktop")
    assert "<aday ya da video id> · <tür> · <kanıt URL> · <açıklama>" in t
    assert all(x in t for x in ak.DESKTOP_TUR) and len(ak.DESKTOP_TUR) == 7


def test_yalniz_sablon_kayit_yok(tmp_path, capsys):
    kok = _kur(tmp_path)
    assert ak.denetim_isle(_d(), kok) == 0 and _j(kok) == []


def test_gecerli_uc_tur(tmp_path):
    kok = _kur(tmp_path, "- a0 · KAÇAN-doğru · https://x/1 · gerçek kaçan", "a2 · kötü-yan · https://x/2 · y · z",
               "  - v1 · Güçlendirme · https://x/3 · w  ")
    assert ak.denetim_isle(_d(), kok) == 0
    j = _j(kok)
    assert [(x["parti"], x["aday"], x["tur"], x["url"], x["aciklama"]) for x in j] == [
        ("p1", "a0", "KAÇAN-doğru", "https://x/1", "gerçek kaçan"), ("p1", "a2", "kötü-yan", "https://x/2", "y · z"),
        ("p1", "v1", "güçlendirme", "https://x/3", "w")]
    assert all(x["tarih"] for x in j)
    b = tr.bolum((kok / "docs/kurulumlar/adaylar/a0.md").read_text(encoding="utf-8"), "Desktop denetimi")
    assert "· p1 · KAÇAN-doğru · https://x/1 · gerçek kaçan" in b


def test_turkce_ascii_tur(tmp_path):
    kok = _kur(tmp_path, "- a0 · kotu-yan · u · x", "- a0 · KACAN-DOGRU · u · y", "- a2 · aday-degil-itiraz · u · z", "- a2 · onarim · u · q")
    assert ak.denetim_isle(_d(), kok) == 0
    assert [x["tur"] for x in _j(kok)] == ["kötü-yan", "KAÇAN-doğru", "aday-değil-itiraz", "onarım"]


def test_bilinmeyen_tur_okunamadi(tmp_path, capsys):
    kok = _kur(tmp_path, "- a0 · harika · u · x")
    assert ak.denetim_isle(_d(), kok) == 1
    assert "okunamadı: - a0 · harika · u · x" in capsys.readouterr().out
    j = _j(kok)
    assert len(j) == 1 and j[0]["okunamadi"] == "- a0 · harika · u · x" and "tür" in j[0]["sebep"]


def test_ayracsiz_okunamadi(tmp_path, capsys):
    kok = _kur(tmp_path, "a0 kötü-yan bir şey")
    assert ak.denetim_isle(_d(), kok) == 1
    assert "okunamadı: a0 kötü-yan bir şey" in capsys.readouterr().out
    assert _j(kok)[0]["okunamadi"] == "a0 kötü-yan bir şey"


def test_olmayan_aday_okunamadi(tmp_path, capsys):
    kok = _kur(tmp_path, "- zz · not · u · x")
    assert ak.denetim_isle(_d(), kok) == 1
    j = _j(kok)
    assert j[0]["okunamadi"] == "- zz · not · u · x" and "yok" in j[0]["sebep"]
    assert "okunamadı: - zz · not · u · x" in capsys.readouterr().out


def test_tekrar_islenmez(tmp_path):
    kok = _kur(tmp_path, "- a0 · not · u · x", "- a0 · harika · u · x")
    ak.denetim_isle(_d(), kok)
    ak.denetim_isle(_d(), kok)
    assert len(_j(kok)) == 2
    assert (kok / "docs/kurulumlar/adaylar/a0.md").read_text(encoding="utf-8").count("· not · u · x") == 1


def test_panel_yeniden_yazinca_desktop_korunur():
    eski = ak.denetim_md(_d(), _z(), _karar()) + "- a0 · not · u · x\n"
    t = ak.denetim_md(_d(), _z(), _karar(), eski=eski)
    assert tr.bolum(t, "Desktop").count("- a0 · not · u · x") == 1
