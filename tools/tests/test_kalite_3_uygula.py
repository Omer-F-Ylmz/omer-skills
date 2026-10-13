import importlib.util
import json
from pathlib import Path

_s = importlib.util.spec_from_file_location("k3u", Path(__file__).resolve().parents[2] / "onay" / "kalite_3_uygula.py")
k3u = importlib.util.module_from_spec(_s)
_s.loader.exec_module(k3u)


def test_uygula_geri_gidis_donus(tmp_path):
    ev, kok = tmp_path / "ev", tmp_path / "kok"
    canli = ev / ".claude" / "skills" / "pdf"
    canli.mkdir(parents=True)
    (canli / "SKILL.md").write_text("---\nname: pdf\ndescription: Eski.\n---\nUZUN GÖVDE\n", encoding="utf-8")
    (ev / ".claude.json").write_text(json.dumps({"mcpServers": {"a": {}}}), encoding="utf-8")
    bol = kok / ".kalite3" / "pilot" / "pdf"
    (bol / "references").mkdir(parents=True)
    (bol / "SKILL.md").write_text("---\nname: pdf\ndescription: Eski.\n---\nÇEKİRDEK\n", encoding="utf-8")
    (bol / "references" / "r.md").write_text("ayrıntı", encoding="utf-8")
    (kok / "docs" / "kutuphane").mkdir(parents=True)
    (kok / "docs" / "kutuphane" / "kalite3-kabul.txt").write_text("pdf\nyok-boyle\n", encoding="utf-8")
    (kok / ".kalite3" / "aciklama-yeni.jsonl").write_text(json.dumps(
        {"ad": "pdf", "yeni": 'Birleştirir "pdf". Use when merging.', "gecerli": True, "denetim": "yok"}) + "\n", encoding="utf-8")
    assert k3u.uygula(ev, kok) is True
    yeni = (canli / "SKILL.md").read_text(encoding="utf-8")
    assert "ÇEKİRDEK" in yeni and 'description: "Birleştirir \\"pdf\\". Use when merging."' in yeni
    assert (canli / "references" / "r.md").exists()
    assert k3u.geri(ev) is True
    assert (canli / "SKILL.md").read_text(encoding="utf-8").endswith("UZUN GÖVDE\n") and not (canli / "references").exists()


def test_subagent_model_env_kaldirilir_ve_geri_gelir(tmp_path):
    ayar = tmp_path / ".claude" / "settings.json"
    ayar.parent.mkdir(parents=True)
    ayar.write_text(json.dumps({"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "x", "BASKA": "1"}, "model": "opus"}), encoding="utf-8")
    assert k3u.subagent_env_var_mi(tmp_path)
    assert k3u.uygula(tmp_path, tmp_path)
    j = json.loads(ayar.read_text(encoding="utf-8"))
    assert j == {"env": {"BASKA": "1"}, "model": "opus"}
    assert not k3u.subagent_env_var_mi(tmp_path)
    assert k3u.geri(tmp_path)
    assert json.loads(ayar.read_text(encoding="utf-8"))["env"]["CLAUDE_CODE_SUBAGENT_MODEL"] == "x"


def test_gecen_ajanlar_kurulur_ve_geri_alinir(tmp_path):
    kok, ev = tmp_path / "kok", tmp_path / "ev"
    (kok / "ajanlar" / "kalite3" / "frontend").mkdir(parents=True)
    (kok / "ajanlar" / "kalite3" / "frontend" / "fe-x.md").write_text("---\nname: fe-x\nmodel: sonnet\n---\nyeni\n", encoding="utf-8")
    (kok / "docs" / "kutuphane").mkdir(parents=True)
    (kok / "docs" / "kutuphane" / "kalite3-ajan-kabul.txt").write_text("fe-x\nyok-boyle\n", encoding="utf-8")
    assert k3u.ajan_plani(kok) == [("fe-x", kok / "ajanlar" / "kalite3" / "frontend" / "fe-x.md")]
    assert k3u.uygula(ev, kok)
    assert (ev / ".claude" / "agents" / "fe-x.md").read_text(encoding="utf-8").endswith("yeni\n")
    assert k3u.geri(ev)
    assert not (ev / ".claude" / "agents" / "fe-x.md").exists()  # önceden yoktu → geri alınca yok


def test_d15_yeni_aileler_ve_ruflo_kurulur(tmp_path):
    kok, ev = tmp_path / "kok", tmp_path / "ev"
    adlar = [("kalite3-d15", "dil-cerceve", "dil-a"), ("kalite3-d15", "altyapi", "ops-b"), ("kalite3-d15", "ml-yapay-zeka", "ml-c"),
             ("kalite3-d15", "urun-is", "urn-d"), ("kalite3-ruflo", "surec-plan", "pln-e"), ("kalite3-d16", "mobil", "mob-f"), ("kalite3-d17", "backend", "be-g")]
    for k, aile, ad in adlar:
        (kok / "ajanlar" / k / aile).mkdir(parents=True)
        (kok / "ajanlar" / k / aile / f"{ad}.md").write_text(f"---\nname: {ad}\nmodel: sonnet\n---\n{ad}\n", encoding="utf-8")
    (kok / "docs" / "kutuphane").mkdir(parents=True)
    (kok / "docs" / "kutuphane" / "kalite3-ajan-kabul.txt").write_text("\n".join(a for _, _, a in adlar) + "\n", encoding="utf-8")
    assert k3u.ajan_plani(kok) == [(ad, kok / "ajanlar" / k / aile / f"{ad}.md") for k, aile, ad in adlar]
    assert k3u.uygula(ev, kok)
    assert all((ev / ".claude" / "agents" / f"{ad}.md").read_text(encoding="utf-8").endswith(f"{ad}\n") for _, _, ad in adlar)


def test_ajan_getir_katalog_guncellenir_ve_geri_alinir(tmp_path):
    kok, ev = tmp_path / "kok", tmp_path / "ev"
    (kok / "skills" / "ajan-getir").mkdir(parents=True)
    (kok / "skills" / "ajan-getir" / "katalog.tsv").write_text("ad\nyeni-ajan\n", encoding="utf-8")
    canli = ev / ".claude" / "skills" / "ajan-getir" / "katalog.tsv"
    canli.parent.mkdir(parents=True)
    canli.write_text("ad\n", encoding="utf-8")
    assert k3u.katalog_farkli_mi(ev, kok)
    assert k3u.uygula(ev, kok)
    assert canli.read_text(encoding="utf-8") == "ad\nyeni-ajan\n" and not k3u.katalog_farkli_mi(ev, kok)
    assert k3u.geri(ev)
    assert canli.read_text(encoding="utf-8") == "ad\n"
