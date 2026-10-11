import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ajan_katalog as ak  # noqa: E402


def _ajan(yol, ad, model=None, aciklama="Bir iş yapar. İkinci cümle."):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text(f"---\nname: {ad}\ndescription: {aciklama}\n" + (f"model: {model}\n" if model else "") + "---\n\ngövde\n", encoding="utf-8")


def test_gizli_plugin_ve_kullanici_ajanlari(tmp_path):
    (tmp_path / "settings.json").write_text(json.dumps({"permissions": {"deny": ["Agent(pl:gizli)", "Agent(pl:yok)", "Agent(pl:alt:derin)", "Bash(rm -rf *)"]}}), encoding="utf-8")
    _ajan(tmp_path / "plugins/cache/mk/pl/1.0/agents/gizli.md", "gizli", "sonnet")
    _ajan(tmp_path / "plugins/cache/mk/pl/1.0/agents/alt/derin.md", "derin")
    _ajan(tmp_path / "plugins/cache/mk/pl/1.0/agents/acik.md", "acik")
    _ajan(tmp_path / "agents/kullanici.md", "Kullanıcı Ajanı", aciklama="Tek\tsekmeli açıklama. Devamı.")
    satirlar, eksik = ak.uret(tmp_path)
    assert [s[0] for s in satirlar] == ["pl:gizli", "pl:alt:derin", "Kullanıcı Ajanı"]  # açık plugin ajanı katalogda yok
    assert satirlar[0][1] == "sonnet" and satirlar[1][1] == "inherit"
    assert satirlar[0][2] == "Bir iş yapar." and "\t" not in satirlar[1][2]
    assert satirlar[0][3].endswith("agents/gizli.md")
    assert eksik == ["pl:yok"]
