import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skill_iyilestir as si  # noqa: E402

GOVDE = """# Araç

Giriş paragrafı.

## When to use

- PDF birleştirme istenince.

## Workflow

1. Run `pdf birlestir a.pdf b.pdf`.
2. NEVER overwrite the input file.

## Reference: flags

""" + ("Uzun açıklama satırı. " * 600) + """
```bash
pdf birlestir --sayfa 1-3 a.pdf
```

## Troubleshooting

""" + ("Hata ayrıntısı. " * 500) + """
- ALWAYS check mcp__eskiad__ara first.
"""


def _skill(tmp, aciklama="Merges PDF files into one document."):
    d = tmp / "pdf"
    d.mkdir()
    (d / "SKILL.md").write_text(f"---\nname: pdf\ndescription: {aciklama}\n---\n{GOVDE}", encoding="utf-8")
    return d


def test_bol_bilgi_kaybi_yok(tmp_path):
    d = _skill(tmp_path)
    cikti = tmp_path / "out"
    r = si.iyilestir(d, cikti, {"yeniad"}, {"eskiad": "yeniad"})
    cekirdek = (cikti / "SKILL.md").read_text(encoding="utf-8")
    refs = sorted(p.name for p in (cikti / "references").iterdir())
    assert refs == ["reference-flags.md", "troubleshooting.md"]
    assert "## When to use" in cekirdek and "## Workflow" in cekirdek and "NEVER overwrite" in cekirdek
    assert "references/troubleshooting.md" in cekirdek and cekirdek.count("Hata ayrıntısı") == 1  # yalnız ilk cümle işaretçide
    assert r["once"] > 2 * r["sonra"] and r["kayip"] == []
    # (c) eski MCP adı kurulu karşılığa bağlanır
    assert "mcp__yeniad__ara" in (cikti / "references/troubleshooting.md").read_text(encoding="utf-8")
    assert r["arac"] == ["mcp__eskiad→mcp__yeniad"]
    assert (d / "SKILL.md").read_text(encoding="utf-8").count("Hata ayrıntısı") == 500  # orijinal dokunulmaz


def test_siniflandirici_is_akisi_kalir_ekler_tasinir(tmp_path):
    uzun = "Ayrıntılı açıklama cümlesi. " * 300
    bolumler = ["Stage 1: Context Gathering", "Step 2 - Draft", "Output format", "Rules and prohibitions", "Phase 3",
                "Examples", "API reference", "Quick reference", "Templates", "Appendix", "FAQ", "Changelog"]
    govde = "# Akış\n\nGiriş.\n\n" + "".join(f"## {b}\n\n{b} ilk cümle. {uzun}\n\n" for b in bolumler)
    govde += "## Example 1\n\nKısa örnek bir.\n\n## Example 2\n\nKısa örnek iki.\n\n"
    govde += "## Parameters\n\n" + uzun + "\n- NEVER pass --force in production.\n"
    d = tmp_path / "akis"
    d.mkdir()
    (d / "SKILL.md").write_text(f"---\nname: akis\ndescription: Use when x.\n---\n{govde}", encoding="utf-8")
    r = si.iyilestir(d, tmp_path / "o", set(), {})
    refs = {p.stem for p in (tmp_path / "o/references").iterdir()}
    cekirdek = (tmp_path / "o/SKILL.md").read_text(encoding="utf-8")
    for b in bolumler[:5]:  # iş akışı / çıktı biçimi / kurallar çekirdekte bütün kalır
        assert cekirdek.count(f"{b} ilk cümle") == 1 and cekirdek.count("Ayrıntılı açıklama") >= 1
    assert {"stage-1-context-gathering", "step-2-draft", "output-format", "rules-and-prohibitions", "phase-3"}.isdisjoint(refs)
    assert {"examples", "api-reference", "quick-reference", "templates", "appendix", "faq", "changelog", "parameters"} <= refs
    assert "Kısa örnek bir." in cekirdek and "example-2" in refs  # en fazla 1 kısa örnek çekirdekte
    assert "NEVER pass --force in production." in cekirdek  # taşınan bölümdeki kural satırı çekirdekte kalır
    assert r["kayip"] == []


def test_kontrol_listesi_kaybi_yakalar():
    once = "## A\n- MUST do x\n```\nkomut --bayrak\n```\n"
    assert si.kontrol(once, ["## A\n"]) == ["- MUST do x", "komut --bayrak"]


def test_kucuk_skill_ve_tetik_istegi(tmp_path):
    d = tmp_path / "kucuk"
    d.mkdir()
    (d / "SKILL.md").write_text("---\nname: kucuk\ndescription: Does a thing.\n---\n# K\nkısa\n", encoding="utf-8")
    istek = tmp_path / "istek.jsonl"
    r = si.iyilestir(d, tmp_path / "o", set(), {}, istek)
    assert r["bolundu"] is False and not (tmp_path / "o/references").exists()
    satir = json.loads(istek.read_text(encoding="utf-8").splitlines()[0])
    assert satir["custom_id"] == "aciklama-kucuk" and satir["params"]["model"] == si.YAZAR
    assert "Does a thing." in satir["params"]["messages"][0]["content"]
