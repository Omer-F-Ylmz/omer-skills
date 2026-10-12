"""VİDEO-16: VIDEO_SHORT_HIZ=<efor> → short'ta şema id enum'suz (A: partideki short'lar ortak önek → önbellek okuma) + claude -p --effort <efor>; uzun video ve bayraksız yol değişmez."""
from video import hafif, parti

METIN = "[00:01] merhaba\n[00:20] Ollama kurulumu"


def _kos(monkeypatch, tmp_path, short, env):
    yol = tmp_path / "paket.md"
    yol.write_text("# V1 · başlık · kanal · sure_sn 25\n" + METIN, encoding="utf-8")
    pk = {"V1": {**parti.paket_oku(yol), "metin": METIN, "short": short}}
    cag = []

    def cagir(sis, istem, sema, kareler, model, butce, env, **ek):
        cag.append((sema["properties"]["videolar"]["items"]["properties"]["id"], ek.get("efor")))
        return {"form": {"videolar": [{"id": "V1", "ozet": model, "adaylar": []}]}, "usd": .01, "usage": {}}

    monkeypatch.setattr(parti, "_defter", lambda p: (0, 0))
    monkeypatch.setattr(parti.hafif, "GORSEL", False)
    d = {"butce": 1, "tavan": {"usd": 9}, "videolar": {"V1": {"tarama": {}}}}
    parti._tara_ikili(["V1"], pk, {}, lambda s: s, d, tmp_path, env, cagir, ["claude-sonnet-5-5", "claude-haiku-5-5"])
    return cag


def test_short_hiz_bayrakli(monkeypatch, tmp_path):
    cag = _kos(monkeypatch, tmp_path, True, {"VIDEO_JETON": "0", "VIDEO_SHORT_HIZ": "low"})
    assert len(cag) == 2 and all("enum" not in s and e == "low" for s, e in cag)


def test_short_hiz_bayraksiz_ve_uzun(monkeypatch, tmp_path):
    for short, env in ((True, {"VIDEO_JETON": "0"}), (False, {"VIDEO_JETON": "0", "VIDEO_SHORT_HIZ": "low"})):
        cag = _kos(monkeypatch, tmp_path, short, env)
        assert len(cag) == 2 and all("enum" in s and e is None for s, e in cag)


def test_cagir_effort_bayragi(tmp_path):
    arg = []
    kos = lambda a, g, e, t: arg.append(a) or type("R", (), {"stdout": "", "stderr": "", "returncode": 1})()
    hafif.cagir("s", "m", {}, kos=kos, efor="low", env={})
    hafif.cagir("s", "m", {}, kos=kos, env={})
    assert arg[0][arg[0].index("--effort") + 1] == "low" and "--effort" not in arg[1]
