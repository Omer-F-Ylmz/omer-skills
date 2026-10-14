import json
import subprocess
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import katalog_kanca_uygula as k  # noqa: E402

ESKI = {"permissions": {"deny": ["Bash(git push:*)"]}, "env": {"X": "1"},
        "hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "command": "jev-skill.ps1", "timeout": 3}]}],
                  "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "block-destructive"}]}]}}
ZOR = "Go ile WebSocket sohbet servisi yaz, yatay ölçekle, yük testi yap ve Docker ile dağıt; hangi araçları kullanmalıyım?"


def test_kuru_uygula_geri(tmp_path):
    ev, dist = tmp_path / "ev", tmp_path / "dist"
    eski = ev / "skills" / "yetenek-getir"
    eski.mkdir(parents=True)
    (eski / "SKILL.md").write_text("eski", encoding="utf-8")
    ayar = ev / "settings.json"
    ayar.write_text(json.dumps(ESKI), encoding="utf-8")
    ham = ayar.read_bytes()
    assert k.main(["--kuru"], ev, dist) == 0 and ayar.read_bytes() == ham and not dist.exists() and (eski / "SKILL.md").read_text() == "eski"

    assert k.main(["uygula"], ev, dist) == 0
    j = json.loads(ayar.read_text(encoding="utf-8"))
    assert len(j["hooks"]["UserPromptSubmit"]) == 2 and j["hooks"]["PreToolUse"] == ESKI["hooks"]["PreToolUse"] and j["permissions"] == ESKI["permissions"]
    assert b"\r\n" not in ayar.read_bytes() and ayar.read_bytes().endswith(b"}\n")
    assert (eski / "katalog_kanca.py").exists() and (eski / "yetenek.jsonl").exists()
    assert len(list(dist.glob("*.zip"))) == 14 and (dist / "LISTE.md").read_text(encoding="utf-8").count(".zip") == 14

    # kurulu kanca kendi klasöründen çalışır (katalog_ara + yetenek.jsonl yanında)
    olay = json.dumps({"session_id": str(uuid.uuid4()), "hook_event_name": "UserPromptSubmit", "prompt": ZOR}).encode("utf8")
    r = subprocess.run([sys.executable, str(eski / "katalog_kanca.py")], input=olay, capture_output=True, timeout=30)
    assert r.returncode == 0 and "<katalog>" in r.stdout.decode("utf8")

    try:
        k.main(["uygula"], ev, dist)
        assert False, "ikinci uygula yedek varken durmalı"
    except SystemExit:
        pass
    assert k.main(["--geri"], ev, dist) == 0
    assert json.loads(ayar.read_text(encoding="utf-8")) == ESKI
    assert (eski / "SKILL.md").read_text() == "eski" and not (eski / "katalog_kanca.py").exists()
    assert not (ev / "yedek" / "katalog-kanca-1").exists()


def test_bos_ayarda_olay_listesi_geri_silinir(tmp_path):
    ev = tmp_path / "ev"
    ev.mkdir()
    (ev / "settings.json").write_text("{}", encoding="utf-8")
    assert k.main(["uygula"], ev, tmp_path / "dist") == 0
    assert json.loads((ev / "settings.json").read_text(encoding="utf-8"))["hooks"]["UserPromptSubmit"] == [{"hooks": [k.giris(ev)]}]
    assert k.main(["--geri"], ev, tmp_path / "dist") == 0
    assert json.loads((ev / "settings.json").read_text(encoding="utf-8")) == {}
