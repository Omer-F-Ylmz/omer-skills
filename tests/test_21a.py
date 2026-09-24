"""21a: suite-kosucu ajan tanımı (K2/K3) ve RTK proje filtresi hata satırı koruması (K4)."""
import re
import tomllib
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
FIX = KOK / "tests" / "fixture" / "rtk"
HATA = re.compile(r"^\s*✖|not ok|Error|Traceback|hata:|failed|FAIL", re.I)


def _ajan():
    m = (KOK / ".claude" / "agents" / "suite-kosucu.md").read_text(encoding="utf-8")
    _, fm, govde = m.split("---", 2)
    alan = dict(s.split(":", 1) for s in fm.strip().splitlines())
    return {k.strip(): v.strip() for k, v in alan.items()}, govde


def test_suite_kosucu_yalniz_bash_read_sonnet():
    fm, _ = _ajan()
    assert {x.strip() for x in fm["tools"].split(",")} == {"Bash", "Read"}
    assert fm["model"] == "sonnet"


def test_suite_kosucu_alti_sabit_komut_ve_kisa_donus():
    _, g = _ajan()
    for k in ("tools/video", "tools/jev", "python -m pytest -q -p no:cacheprovider tests", "tools/cc-kopru",
              "mcp/jev", "templates/jev-dotnet/Jev.Tests/Jev.Tests.csproj"):
        assert k in g
    assert "en fazla 6 satır" in g


def test_suite_kosucu_kok_suite_ortam_pythonu_ile():
    # K3: uv --no-project --with pytest ortamında playwright yok → test_browse_shim test başına 120 sn bekler (28 dk)
    _, g = _ajan()
    kok_satir = next(s for s in g.splitlines() if "pytest -q -p no:cacheprovider tests" in s)
    assert "uv run" not in kok_satir and "--no-project" not in g


def test_tam_suit_suite_kosucuya_gider():
    assert "suite-kosucu" in (KOK / "skills" / "departman-test-qa" / "SKILL.md").read_text(encoding="utf-8")


def _filtre():
    f = tomllib.loads((KOK / ".rtk" / "filters.toml").read_text(encoding="utf-8"))["filters"]["cc-kopru-suit"]
    return f, lambda metin: [s for s in metin.splitlines() if not any(re.search(p, s) for p in f["strip_lines_matching"])]


def test_rtk_filtresi_suit_komutlarini_eslestirir():
    f, _ = _filtre()
    for k in ("node araclar/suit.mjs", "npm test"):
        assert re.search(f["match_command"], k)


def test_rtk_filtresi_hata_satirlarini_korur_gecenleri_suzer():
    _, suz = _filtre()
    for ad in ("cc-kopru-suit.txt", "cc-kopru-suit-kirmizi.txt"):
        ham = (FIX / ad).read_text(encoding="utf-8")
        kalan = suz(ham)
        hatalar = [s for s in ham.splitlines() if HATA.search(s) and not s.startswith("✔")]
        assert all(h in kalan for h in hatalar), ad
        assert len("\n".join(kalan)) < 0.3 * len(ham), ad
    assert any("✖" in s for s in suz((FIX / "cc-kopru-suit-kirmizi.txt").read_text(encoding="utf-8")))
