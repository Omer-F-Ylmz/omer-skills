import importlib.util
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fau", KOK / "onay" / "fable_ajan_uygula.py")
fau = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fau)


def kur(tmp_path, monkeypatch):
    ag = tmp_path / ".claude" / "agents"
    ag.mkdir(parents=True)
    (ag / "fe-a.md").write_text("---\nname: fe-a\nmodel: sonnet\n---\nGövde\n", encoding="utf-8")
    (ag / "fe-b.md").write_bytes(b"---\r\nname: fe-b\r\nmodel: haiku\r\n---\r\nG\r\n")
    (ag / "db-c.md").write_text("---\nname: db-c\nmodel: sonnet\n---\nG\n", encoding="utf-8")
    (tmp_path / ".claude.json").write_text(json.dumps({"mcpServers": {"x": {}}}), encoding="utf-8")
    karar = tmp_path / "karar.tsv"
    karar.write_text("aile\tmodel\tkarar\nfe\tsonnet\tKABUL\nfe\thaiku\tRET:out\ndb\tsonnet\tRET:kalite\n", encoding="utf-8")
    monkeypatch.setattr(fau, "KARAR", karar)
    return ag


def test_yalniz_kabul_aile_model_ve_geri(tmp_path, monkeypatch):
    ag = kur(tmp_path, monkeypatch)
    once = {p.name: p.read_bytes() for p in ag.glob("*.md")}
    assert fau.main(["--kuru"], ev=tmp_path) == 0 and {p.name: p.read_bytes() for p in ag.glob("*.md")} == once
    assert fau.main(["uygula"], ev=tmp_path) == 0
    assert "<!-- godmode:basla -->" in (ag / "fe-a.md").read_text(encoding="utf-8")
    assert (ag / "fe-b.md").read_bytes() == once["fe-b.md"] and (ag / "db-c.md").read_bytes() == once["db-c.md"]
    assert len(list((tmp_path / ".claude" / "backups").glob("fable-ajan-*/fe-a.md"))) == 1
    ikinci = (ag / "fe-a.md").read_bytes()
    fau.main(["uygula"], ev=tmp_path)
    assert (ag / "fe-a.md").read_bytes() == ikinci  # idempotent
    assert fau.main(["--geri"], ev=tmp_path) == 0 and (ag / "fe-a.md").read_bytes() == once["fe-a.md"]


def test_katman_taban_ustune_haiku_kisa_ve_plugin_hook(tmp_path, monkeypatch):
    """fable_1_uygula tabanı (skills: calisma-protokolu) atlanır; haiku ultra-kısa blok; plugin ajanı dosyası değişmez → hook."""
    ag = kur(tmp_path, monkeypatch)
    (ag / "fe-t.md").write_text("---\nname: fe-t\nmodel: sonnet\nskills: calisma-protokolu\n---\nG\n", encoding="utf-8")
    pl = tmp_path / ".claude" / "plugins" / "cache" / "mp" / "pl" / "1.0" / "agents" / "rev.md"
    pl.parent.mkdir(parents=True)
    pl.write_text("---\nname: rev\nmodel: sonnet\n---\nG\n", encoding="utf-8")
    ayar = tmp_path / ".claude" / "settings.json"
    ayar.write_text(json.dumps({"env": {"A": "1"}, "hooks": {"Stop": [{"hooks": []}]}}), encoding="utf-8")
    fau.KARAR.write_text("aile\tmodel\tkarar\tprotokol\nfe\tsonnet\tKABUL\tcalisma-protokolu\nfe\thaiku\tKABUL\thaiku-v1\n"
                         "plugin\tsonnet\tKABUL\tcalisma-protokolu\n", encoding="utf-8")
    once_t, once_pl = (ag / "fe-t.md").read_bytes(), pl.read_bytes()
    for _ in range(2):  # idempotent
        assert fau.main(["uygula"], ev=tmp_path) == 0
    assert (ag / "fe-t.md").read_bytes() == once_t and pl.read_bytes() == once_pl
    assert "Answer from the prompt" in (ag / "fe-b.md").read_text(encoding="utf-8")
    s = json.loads(ayar.read_text(encoding="utf-8"))
    assert s["env"] == {"A": "1"} and len(s["hooks"]["SubagentStart"]) == 1
    h = json.loads((tmp_path / ".claude" / "hooks" / "fable-ajan" / "harita.json").read_text(encoding="utf-8"))
    assert h["ajan"] == {"pl:rev": "calisma-protokolu"} and "calisma-protokolu" in h["metin"]
    assert fau.main(["--geri"], ev=tmp_path) == 0
    s = json.loads(ayar.read_text(encoding="utf-8"))
    assert "SubagentStart" not in s["hooks"] and s["hooks"]["Stop"] and not (tmp_path / ".claude" / "hooks" / "fable-ajan").exists()


def test_protokol_butcede():
    assert fau.jeton(fau.govde()) <= fau.PROTOKOL_TAVAN and fau.DERS_TAVAN == 300
