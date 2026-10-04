"""KÜÇÜK-2: çağrı sayacı hook'u (tools/cagri_sayac.py)."""
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cagri_sayac as cs  # noqa: E402


def _kok(tmp_path, sayac=None, dalga=None):
    (tmp_path / ".claude").mkdir()
    if sayac is not None:
        (tmp_path / ".claude" / "cagri-sayac.txt").write_text(sayac, encoding="utf-8")
    if dalga is not None:
        (tmp_path / ".claude" / "dalga.md").write_bytes(dalga.encode("utf-8"))
    return tmp_path


def _sayac(kok):
    return (kok / ".claude" / "cagri-sayac.txt").read_text(encoding="utf-8")


def _kos(kok, monkeypatch, capsys, olay):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(kok))
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(olay)))
    cs.main()
    out = capsys.readouterr().out
    return json.loads(out) if out else None


ARAC = {"hook_event_name": "PostToolUse", "tool_name": "Read"}


def test_basla_sifirlar(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="37")
    _kos(kok, monkeypatch, capsys, {"hook_event_name": "SessionStart"})
    assert _sayac(kok) == "0"


def test_artis(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="0")
    for _ in range(3):
        assert _kos(kok, monkeypatch, capsys, ARAC) is None
    assert _sayac(kok) == "3"


def test_basarisiz_arac_da_sayilir(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    _kos(kok, monkeypatch, capsys, {"hook_event_name": "PostToolUseFailure"})
    assert _sayac(kok) == "5"


def test_alt_ajan_cagrisi_sayilmaz(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    _kos(kok, monkeypatch, capsys, {**ARAC, "agent_id": "x1"})
    assert _sayac(kok) == "4"


def test_bozuk_ya_da_eksik_sayac_sifirdan(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="abc\x00")
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "1"
    (kok / ".claude" / "cagri-sayac.txt").unlink()
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "1"


def test_onda_dalga_ilk_satiri(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="9", dalga="# KARAR\r\nkabul\r\n")
    _kos(kok, monkeypatch, capsys, ARAC)
    dalga = kok / ".claude" / "dalga.md"
    assert dalga.read_bytes().decode("utf-8") == "çağrı 10/45\r\n# KARAR\r\nkabul\r\n"
    (kok / ".claude" / "cagri-sayac.txt").write_text("19", encoding="utf-8")
    _kos(kok, monkeypatch, capsys, ARAC)
    assert dalga.read_bytes().decode("utf-8") == "çağrı 20/45\r\n# KARAR\r\nkabul\r\n"


def test_dalga_yoksa_olusturulmaz(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="9")
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "10"
    assert not (kok / ".claude" / "dalga.md").exists()


def test_40_ve_45_mesaji(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="39", dalga="x\n")
    out = _kos(kok, monkeypatch, capsys, ARAC)
    assert out == {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                   "additionalContext": "çağrı 40/45: yeni madde başlatma"}}
    for n in range(41, 45):
        assert _kos(kok, monkeypatch, capsys, ARAC) is None, n
    out = _kos(kok, monkeypatch, capsys, ARAC)
    assert out["hookSpecificOutput"]["additionalContext"] == "çağrı 45/45: commit + push ve DUR"
    out = _kos(kok, monkeypatch, capsys, {"hook_event_name": "PostToolUseFailure"})
    assert out == {"hookSpecificOutput": {"hookEventName": "PostToolUseFailure",
                   "additionalContext": "çağrı 46/45: commit + push ve DUR"}}


def test_hata_sessiz_gecer(tmp_path, monkeypatch, capsys):
    # .claude yok → yazma hatası; bozuk stdin → JSON hatası; ikisi de çökmez
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "yok"))
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(ARAC)))
    cs.main()
    monkeypatch.setattr(sys, "stdin", io.StringIO("{bozuk"))
    cs.main()
    assert capsys.readouterr().out == ""
