"""KONSOL-DEFTER-1: kesilen işin json'u boşsa harcama oturum transkriptinden hesaplanır."""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / ".kos/kopru"))
sys.path.insert(0, str(KOK / "tools"))
import maliyet_defter  # noqa: E402


def _yaz(ev, sid, satirlar):
    d = ev / ".claude/projects/p"
    d.mkdir(parents=True)
    (d / f"{sid}.jsonl").write_text("\n".join(json.dumps(s) for s in satirlar) + "\n", encoding="utf-8")


def _ast(mid, u, model="claude-opus-5-5"):
    return {"type": "assistant", "message": {"id": mid, "model": model, "usage": u}}


def test_transkript_usd_toplar_ve_tekrari_sayar(tmp_path):
    u = {"input_tokens": 1_000_000, "output_tokens": 100_000}  # 4$ + 2$
    _yaz(tmp_path, "s1", [_ast("m1", u), _ast("m1", u), {"type": "user"}, _ast("m2", {"input_tokens": 1_000_000})])
    assert abs(maliyet_defter.transkript_usd("s1", tmp_path) - 10.0) < 1e-9


def test_transkript_usd_yoksa_none(tmp_path):
    assert maliyet_defter.transkript_usd("yok", tmp_path) is None


def test_konsol_kurus_alti_usd_sifira_yuvarlanmaz(tmp_path):
    y = tmp_path / "m.tsv"
    maliyet_defter.yaz("a", "haiku-kontrol", 0.0019, True, yol=y, kaynak="konsol", cache=0)
    assert maliyet_defter.konsol_harcama(maliyet_defter.oku(y), model="haiku-kontrol") == 0.0019
