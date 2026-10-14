"""KÜÇÜK-2: çağrı sayacı hook'u (tools/cagri_sayac.py)."""
import io
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cagri_sayac as cs  # noqa: E402


def _kok(tmp_path, sayac=None, dalga=None, sid="A"):
    (tmp_path / ".claude").mkdir()
    if sayac is not None:
        (tmp_path / ".claude" / "cagri-sayac").mkdir()
        (tmp_path / ".claude" / "cagri-sayac" / f"{sid}.txt").write_text(sayac, encoding="utf-8")
    if dalga is not None:
        (tmp_path / ".claude" / "dalga.md").write_bytes(dalga.encode("utf-8"))
    return tmp_path


def _sayac(kok, ad="A.txt"):
    return (kok / ".claude" / "cagri-sayac" / ad).read_text(encoding="utf-8")


def _kos(kok, monkeypatch, capsys, olay):
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(kok))
    monkeypatch.delenv("CAGRI_SAYAC_DIZIN", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(olay)))
    cs.main()
    out = capsys.readouterr().out
    return json.loads(out) if out else None


ARAC = {"hook_event_name": "PostToolUse", "tool_name": "Read", "session_id": "A"}
BASLA = {"hook_event_name": "SessionStart", "source": "startup", "session_id": "A"}
DUR = "ara kayıt (commit, push YOK) + devir ve DUR"


def test_basla_sifirlar(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="37")
    (kok / ".claude" / "cagri-sayac" / "A-alt.txt").write_text("8", encoding="utf-8")
    _kos(kok, monkeypatch, capsys, BASLA)
    assert _sayac(kok) == "0"
    assert _sayac(kok, "A-alt.txt") == "0"


def test_artis(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="0")
    for _ in range(3):
        assert _kos(kok, monkeypatch, capsys, ARAC) is None
    assert _sayac(kok) == "3"


def test_basarisiz_arac_da_sayilir(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    _kos(kok, monkeypatch, capsys, {**ARAC, "hook_event_name": "PostToolUseFailure"})
    assert _sayac(kok) == "5"


def test_alt_ajan_cagrisi_ayri_sayilir(tmp_path, monkeypatch, capsys):
    # MÜKEMMEL-2 madde 3: alt ajan ana bütçeye (45) girmez, ayrı sayılır
    kok = _kok(tmp_path, sayac="4")
    for _ in range(2):
        assert _kos(kok, monkeypatch, capsys, {**ARAC, "agent_id": "x1"}) is None
    assert _sayac(kok) == "4"
    assert _sayac(kok, "A-alt.txt") == "2"


def test_bozuk_ya_da_eksik_sayac_sifirdan(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="abc\x00")
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "1"
    (kok / ".claude" / "cagri-sayac" / "A.txt").unlink()
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "1"


def test_onda_baglam_dalgaya_dokunmaz(tmp_path, monkeypatch, capsys):
    # MÜKEMMEL-2 madde 2: sayaç dalga.md'ye yazmaz; görünürlük additionalContext ile
    kok = _kok(tmp_path, sayac="9", dalga="# KARAR\r\nkabul\r\n")
    (kok / ".claude" / "cagri-sayac" / "A-alt.txt").write_text("3", encoding="utf-8")
    out = _kos(kok, monkeypatch, capsys, ARAC)
    assert out == {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                   "additionalContext": "çağrı 10/45 · alt 3"}}
    dalga = kok / ".claude" / "dalga.md"
    assert dalga.read_bytes().decode("utf-8") == "# KARAR\r\nkabul\r\n"


def test_dalga_yoksa_olusturulmaz(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="9")
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "10"
    assert not (kok / ".claude" / "dalga.md").exists()


def test_sayac_dizini_ortamdan(tmp_path, monkeypatch, capsys):
    # MÜKEMMEL-2 madde 1: CAGRI_SAYAC_DIZIN verilirse proje sayacına dokunulmaz
    (tmp_path / "proje").mkdir()
    kok = _kok(tmp_path / "proje", sayac="7")
    dizin = tmp_path / "gecici"
    dizin.mkdir()
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(kok))
    monkeypatch.setenv("CAGRI_SAYAC_DIZIN", str(dizin))
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(ARAC)))
    cs.main()
    assert _sayac(kok) == "7"
    assert (dizin / "cagri-sayac" / "A.txt").read_text(encoding="utf-8") == "1"


def test_40_ve_45_mesaji(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="39", dalga="x\n")
    out = _kos(kok, monkeypatch, capsys, ARAC)
    assert out == {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                   "additionalContext": "çağrı 40/45: yeni madde başlatma"}}
    for n in range(41, 45):
        assert _kos(kok, monkeypatch, capsys, ARAC) is None, n
    out = _kos(kok, monkeypatch, capsys, ARAC)
    assert out["hookSpecificOutput"]["additionalContext"] == f"çağrı 45/45: {DUR}"
    out = _kos(kok, monkeypatch, capsys, {**ARAC, "hook_event_name": "PostToolUseFailure"})
    assert out == {"hookSpecificOutput": {"hookEventName": "PostToolUseFailure",
                   "additionalContext": f"çağrı 46/45: {DUR}"}}


def test_hata_sessiz_gecer(tmp_path, monkeypatch, capsys):
    # .claude yok → yazma hatası; bozuk stdin → JSON hatası; ikisi de çökmez
    monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(tmp_path / "yok"))
    monkeypatch.delenv("CAGRI_SAYAC_DIZIN", raising=False)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(ARAC)))
    cs.main()
    monkeypatch.setattr(sys, "stdin", io.StringIO("{bozuk"))
    cs.main()
    monkeypatch.setattr(sys, "stdin", io.StringIO("[1]"))
    cs.main()
    assert capsys.readouterr().out == ""


def test_compact_sayaci_korur(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="0")
    _kos(kok, monkeypatch, capsys, {**BASLA, "source": "clear"})
    for _ in range(3):
        _kos(kok, monkeypatch, capsys, ARAC)
    _kos(kok, monkeypatch, capsys, {**BASLA, "source": "compact"})
    _kos(kok, monkeypatch, capsys, ARAC)
    assert _sayac(kok) == "4"


# KANCA-SAYAÇ-1: sayaç session_id başına, bağlam eşiği, eski dosya temizliği
def test_eszamanli_oturumlar_ayri_sayilir(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path)
    for _ in range(3):
        _kos(kok, monkeypatch, capsys, ARAC)
        _kos(kok, monkeypatch, capsys, {**ARAC, "session_id": "B"})
    _kos(kok, monkeypatch, capsys, {**BASLA, "session_id": "B"})
    _kos(kok, monkeypatch, capsys, {**ARAC, "session_id": "B", "agent_id": "x"})
    assert _sayac(kok) == "3" and _sayac(kok, "B.txt") == "0" and _sayac(kok, "B-alt.txt") == "1"


def test_eski_tek_dosya_okunmaz(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path)
    (kok / ".claude" / "cagri-sayac.txt").write_text("44", encoding="utf-8")
    assert _kos(kok, monkeypatch, capsys, ARAC) is None
    assert _sayac(kok) == "1"


def test_gecersiz_session_id_sessiz(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path)
    for sid in ("", None, "../x", "a/b", 5):
        assert _kos(kok, monkeypatch, capsys, {**ARAC, "session_id": sid}) is None
    assert not (kok / ".claude" / "cagri-sayac").exists() or not list((kok / ".claude" / "cagri-sayac").iterdir())
    assert not (kok / "x.txt").exists()


def _transcript(tmp_path, *satirlar):
    t = tmp_path / "t.jsonl"
    t.write_text("\n".join(json.dumps(s) for s in satirlar) + "\n", encoding="utf-8")
    return str(t)


def _asistan(girdi, yaz=0, oku=0, yan=False):
    return {"type": "assistant", "isSidechain": yan, "message": {"usage": {
        "input_tokens": girdi, "cache_creation_input_tokens": yaz, "cache_read_input_tokens": oku, "output_tokens": 9}}}


def test_baglam_esigi_dur(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    t = _transcript(tmp_path, _asistan(5, 1000, 100_000), {"type": "user"},
                    _asistan(10, 4990, 145_000), _asistan(1, 0, 200_000, yan=True))
    out = _kos(kok, monkeypatch, capsys, {**ARAC, "transcript_path": t})
    assert out["hookSpecificOutput"]["additionalContext"] == f"çağrı 5/45: {DUR}"


def test_baglam_esik_alti_yalniz_sayi(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    t = _transcript(tmp_path, _asistan(10, 4989, 145_000))
    assert _kos(kok, monkeypatch, capsys, {**ARAC, "transcript_path": t}) is None
    assert _sayac(kok) == "5"


def test_45te_kucuk_baglam_bolmez(tmp_path, monkeypatch, capsys):
    # K14 (TOKEN-3): 45 çağrıda bağlam <120k ise yeni oturum (~100k) sürdürmekten pahalı
    kok = _kok(tmp_path, sayac="44")
    t = _transcript(tmp_path, _asistan(10, 0, 119_000))
    assert _kos(kok, monkeypatch, capsys, {**ARAC, "transcript_path": t}) is None
    t = _transcript(tmp_path, _asistan(10, 0, 120_000))
    assert DUR in _kos(kok, monkeypatch, capsys, {**ARAC, "transcript_path": t})["hookSpecificOutput"]["additionalContext"]


def test_baglam_okunamaz_yalniz_sayi(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="4")
    bozuk = tmp_path / "bozuk.jsonl"
    bozuk.write_bytes(b"\xff{bozuk\n[1]\n\"x\"\n" + json.dumps({"type": "assistant", "message": 3}).encode())
    for yol in (str(tmp_path / "yok.jsonl"), str(bozuk), None, 7):
        assert _kos(kok, monkeypatch, capsys, {**ARAC, "transcript_path": yol}) is None, yol
    assert _sayac(kok) == "8"


def test_eski_sayac_dosyalari_temizlenir(tmp_path, monkeypatch, capsys):
    kok = _kok(tmp_path, sayac="3", sid="eski")
    d = kok / ".claude" / "cagri-sayac"
    (d / "yeni.txt").write_text("2", encoding="utf-8")
    (d / "eski.md").write_text("x", encoding="utf-8")
    gun_once = time.time() - 25 * 3600
    for ad in ("eski.txt", "eski.md"):
        os.utime(d / ad, (gun_once, gun_once))
    _kos(kok, monkeypatch, capsys, BASLA)
    assert sorted(p.name for p in d.iterdir()) == ["A-alt.txt", "A.txt", "eski.md", "yeni.txt"]
