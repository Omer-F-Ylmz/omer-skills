import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
import ruflo_1_kanca as rk  # noqa: E402

AYAR = {"permissions": {"deny": ["Bash(rm -rf:*)"]}, "env": {"X": "1"},
        "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "block-destructive"}]}],
                  "SessionEnd": [{"hooks": [{"type": "command", "command": "baska"}]}]}}


def ev_kur(tmp_path):
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps(AYAR, indent=2) + "\n", encoding="utf-8")
    kanca = tmp_path / "kanca.py"
    kanca.write_text("", encoding="utf-8")
    return tmp_path, kanca


def oku(ev):
    return json.loads((ev / ".claude" / "settings.json").read_text(encoding="utf-8"))


def test_kuru_yazmaz_uygula_ekler_geri_soker(tmp_path):
    ev, kanca = ev_kur(tmp_path)
    assert rk.main(ev, "--kuru", kanca) == 0 and oku(ev) == AYAR
    assert rk.main(ev, "uygula", kanca) == 0
    j = oku(ev)
    assert {k: v for k, v in j.items() if k != "hooks"} == {k: v for k, v in AYAR.items() if k != "hooks"}
    assert j["hooks"]["PreToolUse"] == AYAR["hooks"]["PreToolUse"]
    assert [h["command"] for g in j["hooks"]["SessionEnd"] for h in g["hooks"]] == ["baska", rk.KOMUT]
    assert all(rk._bizim(j["hooks"][o][-1]) for o in rk.OLAYLAR)
    assert len(list((ev / ".claude" / "yedek").iterdir())) == 1
    assert rk.main(ev, "uygula", kanca) == 0 and oku(ev) == j  # idempotent
    assert rk.main(ev, "--geri", kanca) == 0 and oku(ev) == AYAR


def test_kanca_yoksa_uygulamaz(tmp_path):
    ev, _ = ev_kur(tmp_path)
    assert rk.main(ev, "uygula", tmp_path / "yok.py") == 1 and oku(ev) == AYAR
