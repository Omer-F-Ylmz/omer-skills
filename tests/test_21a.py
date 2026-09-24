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


def _filtreler():
    return tomllib.loads((KOK / ".rtk" / "filters.toml").read_text(encoding="utf-8"))["filters"]


def _filtre(ad="cc-kopru-suit"):
    f = _filtreler()[ad]
    return f, lambda metin: [s for s in metin.splitlines() if not any(re.search(p, s) for p in f["strip_lines_matching"])]


def test_rtk_filtresi_suit_komutlarini_eslestirir():
    f, _ = _filtre()
    for k in ("node araclar/suit.mjs", "npm test", "node --test tests/"):  # 22 K2: node --test 75× süzülmeden
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


def test_her_rtk_filtresi_fixturelu_ve_hata_uyari_satiri_suzmez():
    # 22 K2: kural tüm filtrelere genişler; hata/uyarı/FAIL/Traceback satırı hiçbir filtrede süzülmez
    uyari = re.compile(HATA.pattern + r"|warn|uyar|\[!\]|TRUNCATED", re.I)
    for ad, f in _filtreler().items():
        fx = sorted(FIX.glob(f"{ad}*.txt"))
        assert fx, f"{ad}: tests/fixture/rtk/{ad}*.txt yok"
        assert f.get("max_lines") is None and f.get("keep_lines_matching") is None, f"{ad}: satır kesen/seçen alan hata satırını düşürebilir"
        for y in fx:
            satirlar = y.read_text(encoding="utf-8").splitlines()
            hatalar = [s for s in satirlar if uyari.search(s) and not s.lstrip().startswith("✔")]
            assert hatalar, y.name
            silinen = [s for s in hatalar if any(re.search(p, s) for p in f["strip_lines_matching"])]
            assert not silinen, f"{ad}: {silinen[:2]}"
