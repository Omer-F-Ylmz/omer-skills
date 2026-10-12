import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ajan_uret as au  # noqa: E402

R4 = [{"regex": "aria", "puan": 4}, {"regex": "focus", "puan": 3}, {"regex": "contrast", "puan": 2}, {"regex": "label", "puan": 1}]
SKILLER = {"anthropic-skills:fixing-accessibility", "dotnet-aspnetcore:dotnet-webapi"}


def kayit(ad="fe-a11y-denetci", **ek):
    k = {
        "ad": ad, "departman": "frontend", "uzmanlik": "a11y",
        "aciklama": "Audits accessibility. Use when reviewing ARIA, focus, contrast.",
        "model": "haiku", "araclar": ["Read", "Grep"],
        "skiller": ["anthropic-skills:fixing-accessibility"],
        "adimlar": ["Tara", "Raporla", "Oneri ver"],
        "kurallar": ["MUST kanit goster", "NEVER dosya degistirme"],
        "cikti": "En fazla 15 satir liste.",
        "gorev": {"istem": "Audit a button.", "rubrik": R4},
    }
    k.update(ek)
    return k


def calistir(tmp_path, kayitlar, mevcut=()):
    m = tmp_path / "matris.json"
    m.write_text(json.dumps(kayitlar), encoding="utf-8")
    return au.uret(m, tmp_path / "cikti", set(mevcut), SKILLER)


def test_dosyalar_uretilir(tmp_path):
    hatalar = calistir(tmp_path, [kayit(), kayit("fe-b", departman="frontend")])
    assert hatalar == []
    md = (tmp_path / "cikti/frontend/fe-a11y-denetci.md").read_text(encoding="utf-8")
    assert md.startswith("---\nname: fe-a11y-denetci\ndescription: Audits")
    assert "\nmodel: haiku\ntools: Read, Grep\n---\n" in md
    assert "Önce yükle: anthropic-skills:fixing-accessibility" in md
    g = json.loads((tmp_path / "cikti/gorevler.json").read_text(encoding="utf-8"))
    assert g[0]["ajan"] == "fe-a11y-denetci" and g[0]["model"] == "haiku" and g[0]["istem"]
    tsv = (tmp_path / "cikti/katalog-ek.tsv").read_text(encoding="utf-8").splitlines()
    assert tsv[0] == "ad\tmodel\ttek_satir\tyol" and tsv[1].startswith("fe-a11y-denetci\thaiku\t")


def test_puan_toplami_10_degilse_hata(tmp_path):
    k = kayit(gorev={"istem": "x", "rubrik": R4[:3] + [{"regex": "z", "puan": 2}]})
    assert any("puan" in h for h in calistir(tmp_path, [k]))
    assert not (tmp_path / "cikti").exists()


def test_cakisan_ad_reddedilir(tmp_path):
    assert any("çakış" in h for h in calistir(tmp_path, [kayit()], mevcut={"fe-a11y-denetci"}))
    assert any("tekrar" in h for h in calistir(tmp_path, [kayit(), kayit()]))


def test_bozuk_regex_ve_uydurma_skill(tmp_path):
    k = kayit(gorev={"istem": "x", "rubrik": R4[:3] + [{"regex": "(", "puan": 1}]})
    assert any("regex" in h for h in calistir(tmp_path, [k]))
    assert any("skill" in h for h in calistir(tmp_path, [kayit(skiller=["uydurma:yok"])]))
