"""DERİNLİK-MASTER E3: uyarlamalı örneklem. Bulgu = desktop-denetim.jsonl'de denetim.md "Rastgele" bölümündeki adaya yazılmış
kötü-yan · onarım · güçlendirme · aday-değil-itiraz satırı (bolum alanı yoksa sayılmaz). Boy: geçmiş yok 3 · son 3 parti bulgusuz 1 ·
aksi halde min(6, 3 + 3 × son partideki bulgu). KAÇAN?, aday değil, ONARIM BEKLİYOR ve risk en yüksek 5 her zaman kalır."""
import json

from test_e1 import _d, _karar, _z
from test_e2 import _j, _kur
from test_m11 import _kur as _kur_panel

from video import akil as ak
from video import tarama as tr

R = "Rastgele 3 (tohum p1)"


def _gecmis(kok, *kayit):
    y = kok / "docs" / "kurulumlar" / "desktop-denetim.jsonl"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text("".join(json.dumps({"parti": p, "aday": "x", "tur": t, **b}, ensure_ascii=False) + "\n" for p, t, b in kayit), encoding="utf-8")
    return kok


def _bulgusuz(kok, *son):
    return _gecmis(kok, ("q1", "not", {"bolum": R}), ("q2", "kötü-yan", {"bolum": "Risk puanı en yüksek 5"}), ("q3", "not", {"bolum": R}), *son)


def test_gecmis_yok_3(tmp_path):
    assert ak.orneklem(tmp_path, "p9") == 3
    assert len(tr.bolum(ak.denetim_md(_d(), _z(), _karar(), boy=ak.orneklem(tmp_path, "p9")), "Rastgele 3").strip().splitlines()) == 3


def test_son_3_parti_bulgusuz_1(tmp_path):
    assert ak.orneklem(_bulgusuz(tmp_path), "p9") == 1


def test_son_partide_1_bulgu_6(tmp_path):
    assert ak.orneklem(_bulgusuz(tmp_path, ("q4", "kötü-yan", {"bolum": R})), "p9") == 6
    assert ak.orneklem(_bulgusuz(tmp_path, ("q4", "onarım", {"bolum": R}), ("q4", "güçlendirme", {"bolum": R})), "p9") == 6  # tavan


def test_not_ve_risk_bolumu_bulgu_sayilmaz(tmp_path):
    assert ak.orneklem(_bulgusuz(tmp_path, ("q4", "not", {"bolum": R}), ("q4", "kötü-yan", {"bolum": "Risk puanı en yüksek 5"}),
                                 ("q4", "KAÇAN-yanlış", {"bolum": R}), ("q4", "kötü-yan", {"bolum": R, "okunamadi": "x"})), "p9") == 1


def test_bolum_alani_olmayan_eski_kayit_sayilmaz(tmp_path):
    assert ak.orneklem(_bulgusuz(tmp_path, ("q4", "kötü-yan", {})), "p9") == 1


def test_mevcut_parti_gecmise_girmez(tmp_path):
    assert ak.orneklem(_bulgusuz(tmp_path, ("p9", "kötü-yan", {"bolum": R})), "p9") == 1


def test_boy_1_digerleri_kalir():
    t3, t1 = ak.denetim_md(_d(), _z(), _karar()), ak.denetim_md(_d(), _z(), _karar(), boy=1)
    assert len(tr.bolum(t1, "Rastgele 1").strip().splitlines()) == 1
    assert all(tr.bolum(t1, b) == tr.bolum(t3, b) for b in ("KAÇAN?", "aday değil", "ONARIM BEKLİYOR", "Risk puanı en yüksek 5"))


def test_denetim_isle_bolum_yazar(tmp_path):
    r = tr.bolum(ak.denetim_md(_d(), _z(), _karar()), R).strip().splitlines()[0].split(" · ")[0][2:]
    _kur(tmp_path, f"- {r} · kötü-yan · u · x", "- a0 · onarım · u · y", "- v1 · not · u · z")
    assert ak.denetim_isle({"parti": "p1", **{k: v for k, v in _d().items() if k != "parti"}}, tmp_path) == 0
    assert [x["bolum"] for x in _j(tmp_path)] == [R, "Risk puanı en yüksek 5", "KAÇAN?"]


def test_panel_orneklem_kullanir(tmp_path):
    pdir, d = _kur_panel(tmp_path)
    _bulgusuz(tmp_path)
    p = ak.panel(pdir, d, tmp_path)
    assert "## Rastgele 1 (tohum" in (p.parent / "denetim.md").read_text(encoding="utf-8")
