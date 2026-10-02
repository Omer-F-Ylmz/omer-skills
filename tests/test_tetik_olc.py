import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import tetik_olc as t  # noqa: E402


def init(araclar=("Read", "Skill")):
    return json.dumps({"type": "system", "subtype": "init", "tools": list(araclar)})


def arac(ad, girdi, usage=None):
    m = {"content": [{"type": "tool_use", "id": "x", "name": ad, "input": girdi}]}
    if usage:
        m["usage"] = usage
    return json.dumps({"type": "assistant", "message": m})


def sonuc(subtype="success", usd=0.12):
    return json.dumps({"type": "result", "subtype": subtype, "total_cost_usd": usd})


def test_skill_cagrisi_yakalanir():
    k = t.ayristir([init(), arac("Skill", {"skill": "anthropic-skills:blender-oturum"}), sonuc()])
    assert k["skiller"] == ["anthropic-skills:blender-oturum"]
    assert t.tetiklenen(k) == {"blender-oturum"}


def test_read_ile_skill_md_yakalanir():
    win = r"C:\Users\pc\.claude\skills\mod-atolyesi\SKILL.md"
    posix = "/c/x/plugins/cache/p/impeccable/1.0/skills/impeccable/SKILL.md"
    k = t.ayristir([arac("Read", {"file_path": win}), arac("Read", {"file_path": posix}),
                    arac("Read", {"file_path": r"C:\x\README.md"})])
    assert k["skill_okuma"] == [win, posix]
    assert t.tetiklenen(k) == {"mod-atolyesi", "impeccable"}


def test_alternatif_etiket_eslesir():
    istem = {"id": "fe1", "kabul": ["frontend-craft", "impeccable", "departman-frontend"]}
    k = t.ayristir([arac("Skill", {"skill": "impeccable:impeccable"})])
    d = t.degerlendir(istem, k)
    assert d["isabet"] is True and d["dogru"] == ["impeccable"] and d["yanlis"] == []


def test_beklenmeyen_skill_isteminde_tetik_yanlis_sayilir():
    istem = {"id": "neg1", "kabul": []}
    k = t.ayristir([arac("Skill", {"skill": "superpowers:brainstorming"})])
    d = t.degerlendir(istem, k)
    assert d["isabet"] is None and d["yanlis"] == ["brainstorming"]


def test_recall_precision_hesabi():
    ds = [
        {"isabet": True, "dogru": ["a"], "yanlis": ["z"], "ilk_ctx": 100, "usd": 0.1},
        {"isabet": False, "dogru": [], "yanlis": [], "ilk_ctx": 300, "usd": 0.3},
        {"isabet": True, "dogru": ["b"], "yanlis": [], "ilk_ctx": 200, "usd": 0.2},
        {"isabet": None, "dogru": [], "yanlis": ["z"], "ilk_ctx": 200, "usd": 0.2},
        {"isabet": None, "dogru": [], "yanlis": [], "ilk_ctx": 200, "usd": 0.2},
    ]
    o = t.ozet(ds)
    assert o["recall"] == round(2 / 3, 3)
    assert o["precision"] == round(2 / 4, 3)
    assert o["negatif_temiz"] == "1/2"
    assert o["yanlis_skill"] == {"z": 2}
    assert o["ilk_ctx_ort"] == 200 and o["usd_top"] == 1.0


def test_bozuk_satir_atlanir():
    k = t.ayristir(["{bozuk", "", arac("Skill", {"skill": "sdp"}), "null"])
    assert k["bozuk"] == 1
    assert t.tetiklenen(k) == {"sdp"}


def test_max_turns_sonu_okunur():
    u = {"input_tokens": 5, "cache_read_input_tokens": 40000, "cache_creation_input_tokens": 1000}
    k = t.ayristir([init(), arac("Read", {"file_path": "a"}, u), arac("Read", {"file_path": "b"}, {"input_tokens": 9}),
                    sonuc("error_max_turns", 0.31)])
    assert k["son"] == "error_max_turns" and k["usd"] == 0.31
    assert k["ilk_ctx"] == 41005


def test_bos_akis():
    k = t.ayristir([])
    assert k == {"skiller": [], "skill_okuma": [], "skill_araci": False, "ilk_ctx": 0,
                 "usd": 0.0, "son": None, "bozuk": 0}
    d = t.degerlendir({"id": "p", "kabul": ["sdp"]}, k)
    assert d["isabet"] is False


def test_init_skill_araci():
    assert t.ayristir([init(("Read", "Skill"))])["skill_araci"] is True
    assert t.ayristir([init(("Read", "Bash"))])["skill_araci"] is False


def test_kos_komutu_cwd_ve_bayraklar(tmp_path):
    gorulen = {}

    def sahte(args, **kw):
        gorulen.update(args=args, **kw)
        return subprocess.CompletedProcess(args, 0, init() + "\n" + sonuc() + "\n", "")

    ham = tmp_path / "p1.jsonl"
    k = t.kos({"id": "p1", "cwd": str(tmp_path), "istem": "merhaba"}, ham,
              env={"ANTHROPIC_BASE_URL": "http://x", "A": "1"}, base_url=False, calistir=sahte)
    a = gorulen["args"]
    assert a[:3] == ["claude", "-p", "merhaba"]
    assert a[a.index("--max-turns") + 1] == "2" and a[a.index("--permission-mode") + 1] == "plan"
    assert "stream-json" in a and gorulen["cwd"] == str(tmp_path)
    assert "ANTHROPIC_BASE_URL" not in gorulen["env"] and gorulen["env"]["A"] == "1"
    assert k["skill_araci"] is True and ham.read_text(encoding="utf-8").count("\n") == 2


def _sunucu():
    import socket
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    s.listen(1)
    return s


def test_headroom_kayit_tanimli_ve_acik(monkeypatch):
    s = _sunucu()
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://x")
    monkeypatch.setattr(t, "HEADROOM", s.getsockname())
    try:
        assert t.headroom_kayit() == "headroom: ANTHROPIC_BASE_URL=tanımlı · 127.0.0.1:6767=açık"
    finally:
        s.close()


def test_headroom_kayit_yok_ve_kapali(monkeypatch):
    s = _sunucu()
    adres = s.getsockname()
    s.close()
    monkeypatch.delenv("ANTHROPIC_BASE_URL", raising=False)
    monkeypatch.setattr(t, "HEADROOM", adres)
    assert t.headroom_kayit() == "headroom: ANTHROPIC_BASE_URL=yok · 127.0.0.1:6767=kapalı"


def test_headroom_kayit_degeri_yazmaz(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://GIZLI-DEGER-123")
    assert "GIZLI" not in t.headroom_kayit()


def test_main_cikti_basinda_headroom_satiri(monkeypatch, tmp_path, capsys):
    (tmp_path / "set.json").write_text('{"istemler": []}', encoding="utf-8")
    monkeypatch.setattr(t, "headroom_kayit", lambda: "headroom: SENTINEL")
    monkeypatch.setattr(sys, "argv", ["tetik_olc", str(tmp_path / "set.json"), str(tmp_path / "o.json"),
                                      "--ham", str(tmp_path / "ham")])
    t.main()
    assert capsys.readouterr().out.splitlines()[0] == "headroom: SENTINEL"
