"""VİDEO-GÖZ-1b-1 M3: Groq transkript — sözlük prompt'u ≤224 tk · ≤24 MB parça planı · offset birleştirme · önbellek · ≤12 çağrı · yedek."""
import json

from video import cli
from video import goz as g

SZ = [("Claude Sonnet", ["Sonet"]), ("Topview", []), ("Behance", []), ("Vercel", [])]


def test_prompt_aciklamada_gecen_once_ve_tavan():
    p = g.groq_prompt(SZ, "Behance galerisi ve topview.ai")
    assert p.startswith("Behance, Topview, ") and "Claude Sonnet" in p
    assert len(g.groq_prompt([(f"Ad{i:04d}", []) for i in range(500)], "", tk=lambda s: len(s) // 3)) // 3 <= 224


def test_parca_plani_25mb_alti():
    assert g.parca_plani(600, 10_000_000) == [(0, 600)]
    assert g.parca_plani(1800, 60_000_000) == [(0, 600), (600, 600), (1200, 600)]


def test_offset_birlestirme():
    assert g.birlestir([(0, [{"start": 1.0, "text": " a "}]), (600, [{"start": 2.5, "text": "b"}, {"start": 3, "text": " "}])]) == [
        (1.0, "a"), (602.5, "b")]


def _ctx(tmp_path, http, env=None):
    d = tmp_path / "abcdefghijk"
    d.mkdir(parents=True, exist_ok=True)
    (d / "ses16k.flac").write_bytes(b"x" * 100)

    def kos(a, timeout):
        if a[0] == "ffmpeg":
            open(a[-1], "wb").write(b"x")
        return 0, b"", b""
    return {"kos": kos, "http": http, "env": {"GROQ_API_KEY": "gizli-anahtar-123"} if env is None else env}, d


def test_groq_istek_basligi_onbellek_ve_tavan(tmp_path):
    cagri = []

    def http(url, veri, basliklar):
        cagri.append((url, basliklar))
        return json.dumps({"segments": [{"start": 0.5, "text": "Sonet çıktı"}]}).encode()
    ctx, d = _ctx(tmp_path, http)
    assert cli._asr(ctx, d, 60, "tr", "Claude Sonnet") == ([(0.5, "Sonet çıktı")], "groq")
    assert cagri[0][1]["Authorization"] == "Bearer gizli-anahtar-123" and "whisper-large-v3-turbo" not in cagri[0][0]
    assert (d / "groq.txt").is_file() and cli._asr(ctx, d, 60, "tr", "") == ([(0.5, "Sonet çıktı")], "groq") and len(cagri) == 1
    ctx2, d2 = _ctx(tmp_path / "b", http)
    ctx2["groq_n"] = cli.GROQ_UST
    seg, kaynak = cli._asr(ctx2, d2, 60, "tr", "")
    assert len(cagri) == 1 and kaynak != "groq"


def test_anahtar_yoksa_yedek_ve_not(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "WMODEL", tmp_path / "yok")
    ctx, d = _ctx(tmp_path, lambda *a: b"{}", env={})
    seg, kaynak = cli._asr(ctx, d, 60, "tr", "")
    assert seg is None and kaynak == "faster-whisper" and "GROQ_API_KEY" in ctx["asr_not"] and "gizli" not in ctx["asr_not"]
