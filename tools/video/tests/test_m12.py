"""MOTOR-M12: kapat içe alınan eski rapor UYARI · açık parti koruması · parti iptal · ön-doldurma (a) çoğul -s."""
import json

from test_m2a import V, _ns
from test_m2b import _actx, _kos_sahte, _parti, _rapor

from video import akil
from video import parti as pt
from video import tarama as tr


def _durum(p, **k):
    d = json.loads((p / "durum.json").read_text(encoding="utf-8"))
    d.update(parti=p.name, **{x: y for x, y in k.items() if x != "ice"})
    if k.get("ice"):
        d["videolar"][V[0]]["tarama"]["ice_alindi"] = True
    (p / "durum.json").write_text(json.dumps(d), encoding="utf-8")


def _eski():
    return _rapor(V[0], [("Hızlı Araç", "CLI", None)]).replace("## İddialar", "## Eski")


# K1: içe alınan eski rapor kapanışı durdurmaz, özet satırında UYARI
def test_k1_ice_alinan_eski_rapor_uyari(tmp_path, capsys):
    p = _parti(tmp_path, "2026-09-29-short", {V[0]: _eski()})
    _durum(p, ice=True)
    kos, _ = _kos_sahte(False)
    assert pt.parti(_ns("kapat", p.name), {**_actx(tmp_path, None), "kos": kos}) == 0
    out = capsys.readouterr().out
    assert "UYARI" in out and "bölüm eksik: ## İddialar" in out


# K1: partinin kendi yazdığı rapor sıkı kalır
def test_k1_kendi_raporunda_eksik_bolum_dur(tmp_path, capsys):
    p = _parti(tmp_path, "2026-09-29-short", {V[0]: _eski()})
    kos, cagri = _kos_sahte(False)
    assert pt.parti(_ns("kapat", p.name), {**_actx(tmp_path, None), "kos": kos}) != 0
    assert "rapor-denetle KALDI" in capsys.readouterr().out and not any("commit" in a for a in cagri)


# K2: açık partideki videolar yeni partiye alınmaz
def test_k2_acik_parti_yeni_parti_acmaz(tmp_path, capsys):
    p = _parti(tmp_path, "2026-10-01-uzun", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    _durum(p, durum="calisiyor")
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _actx(tmp_path, None)) != 0
    assert "açık parti: 2026-10-01-uzun — önce: video parti kapat 2026-10-01-uzun" in capsys.readouterr().out
    assert [x.name for x in (tmp_path / ".kos").iterdir()] == ["2026-10-01-uzun"]


# K3: iptal durum + neden; dosya kalır; açık sayılmaz; kapat reddeder
def test_k3_parti_iptal(tmp_path):
    p = _parti(tmp_path, "2026-10-01-uzun-2", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    _durum(p, durum="calisiyor")
    assert pt._acik(tmp_path) == {V[0]: "2026-10-01-uzun-2"}
    assert pt.parti(_ns("iptal", p.name, neden="aynı videolar"), _actx(tmp_path, None)) == 0
    d = json.loads((p / "durum.json").read_text(encoding="utf-8"))
    assert d["durum"] == "iptal" and d["neden"] == "aynı videolar" and (tmp_path / "docs" / "video-tarama").is_dir()
    assert pt._acik(tmp_path) == {}
    kos, cagri = _kos_sahte(False)
    assert pt.parti(_ns("kapat", p.name), {**_actx(tmp_path, None), "kos": kos}) != 0 and not cagri


# K4: kural (a) ad eşleşmesi sondaki çoğul -s farkını tolere eder
def test_k4_tekil_cogul():
    assert akil._tekil(tr.normal("obsidian-skill")) == akil._tekil(tr.normal("obsidian-skills"))
    assert akil._tekil(tr.normal("graphify")) == tr.normal("graphify")
