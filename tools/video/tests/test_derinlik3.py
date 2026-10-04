"""DERİNLİK-3: panel doğruluğu — Y3 S7 gerçek adlarla + eski satırlar · Y1 ön-doldurma ≠ Ömer kararı."""
from test_derinlik2 import V, _rapor
from test_m11 import _kur
from test_m2c import _aday, _panel

from video import akil as ak


def _gercek():
    """Bu partinin gerçek aday adları (2026-10-03-short)."""
    return {"everything-claude-code-ecc": _aday("everything-claude-code-ecc", adlar=["Everything Claude Code (ECC)"], tur="plugin"),
            "guvenlik-denetleyicisi-security-guidance": _aday("guvenlik-denetleyicisi-security-guidance", tur="plugin",
                                                              adlar=["Güvenlik denetleyicisi (security-guidance)"]),
            "ruflo-videoda-rufflow": _aday("ruflo-videoda-rufflow", adlar=["Ruflo (videoda 'Rufflow')"], tur="plugin"),
            "security-review": _aday("security-review", adlar=["Security Review"], tur="plugin")}


def _eski_panel(kok, satirlar):
    y = kok / "docs" / "kurulumlar" / "parti" / "p1" / "panel.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text("| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |\n|---|---|---|---|---|---|---|---|\n"
                 + "".join(f"| {k} | plugin | 1 | — | — | ZATEN VAR | g | {o} |\n" for k, o in satirlar), encoding="utf-8")


# Y3 parantez içi ad başka videodaki adla birebir aynıysa tek aday (ruflo: Rufflow + Rooflow farklı videolarda)
def test_y3_parantezli_ad_videolar_arasi_tek_aday(tmp_path):
    md0 = _rapor(V[0], [("Ruflo (videoda 'Rufflow')", "plugin", "https://github.com/ruvnet/ruflo")])
    md1 = _rapor(V[1], [("Rooflow (karede Ruflo)", "iş akışı", None), ("ajan-xy", "plugin", None)])
    md2 = _rapor(V[2], [("ajan-x", "plugin", None), ("Security Review", "plugin", None)])
    out, _ = ak.birlestir([(V[0], md0), (V[1], md1), (V[2], md2)], tmp_path)
    assert len(out) == 4 and {"ajan-x", "ajan-xy", "security-review"} <= set(out)
    ruf = next(a for a in out.values() if "Rooflow (karede Ruflo)" in a["adlar"])
    assert len(ruf["adlar"]) == 2 and ruf["repo"] == "ruvnet/ruflo" and set(ruf["videolar"]) == {V[0], V[1]}


# Y3 --yeniden: eski panelde slug'la kalan satır (parantez kaybı) gerçek adın parantez içiyle eşleşir → tek satır; Ömer kararı taşınır
def test_y3_eski_satirlar_birlesik_adaya_iner(tmp_path):
    PID = "p1"
    pdir, d = _kur(tmp_path, adaylar=_gercek())
    d.update(parti=PID, on_doldurma={})
    _eski_panel(tmp_path, [("ruflo", "ÖĞREN"), ("everything-claude-code", "DENE"), ("security-guidance", "ZATEN VAR"),
                           ("everything-claude-code-ecc-gelistirme", "UYARLA")])
    ak.panel(pdir, d, tmp_path)
    r, _ = _panel(tmp_path, PID)
    assert not {"ruflo", "everything-claude-code", "security-guidance"} & set(r)
    assert r["everything-claude-code-ecc-gelistirme"][7] == "UYARLA" and r["security-review"][7] == ""
    assert r["guvenlik-denetleyicisi-security-guidance"][7] == "ZATEN VAR"
    assert (r["ruflo-videoda-rufflow"][7], r["everything-claude-code-ecc"][7]) == ("ÖĞREN", "DENE")


# Y1 ön-doldurma durum.json'da saklanır; hücre saklananla aynıysa yeni öneriyle yenilenir, Ömer yazdıysa korunur
def test_y1_on_doldurma_yenilenir_omer_korunur(tmp_path):
    pdir, d = _kur(tmp_path, adaylar={"skill-creator": _aday("skill-creator", kurulu="skill-creator", tur="skill"),
                                      "gh-kurulu": _aday("gh-kurulu", kurulu="gh")})
    y = ak.panel(pdir, d, tmp_path)
    assert d["on_doldurma"] == {"skill-creator": "ZATEN VAR", "gh-kurulu": "ZATEN VAR"}
    y.write_text("\n".join(s[:s.rstrip().rstrip("|").rstrip().rfind("|")] + "| AL |" if s.startswith("| gh-kurulu") else s
                           for s in y.read_text(encoding="utf-8").splitlines()), encoding="utf-8")
    d["adaylar"]["skill-creator"]["guncellik"] = "fark: kurulu a1 ↔ upstream b2"
    ak.panel(pdir, d, tmp_path)
    r, _ = _panel(tmp_path)
    assert r["skill-creator"][5] == "UYARLA" and r["skill-creator"][7] != "ZATEN VAR" and r["gh-kurulu"][7] == "AL"


# Y1 ön-doldurma kaydı olmayan eski durum: mevcut hücrelerin hepsi ön-doldurma sayılır (bu partide Ömer hücre yazmadı)
def test_y1_kayitsiz_eski_durumda_hucreler_on_doldurma(tmp_path):
    pdir, d = _kur(tmp_path, adaylar={"skill-creator": _aday("skill-creator", kurulu="skill-creator", tur="skill",
                                                               guncellik="fark: kurulu a1 ↔ upstream b2")})
    d["parti"] = "p1"
    _eski_panel(tmp_path, [("skill-creator", "ZATEN VAR")])
    ak.panel(pdir, d, tmp_path)
    r, _ = _panel(tmp_path, "p1")
    assert r["skill-creator"][7] != "ZATEN VAR"
