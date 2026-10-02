"""TOKEN-1 K5: motor (hafif) ve deney hattı (kur) ttl profiline bağlı; motor usage'ı yalnız sayı olarak olcum/motor-usage.jsonl'e."""
import json
from types import SimpleNamespace

from video import hafif, kur

TTL = {"promptCacheTtl": "5m"}


def _ayar(args):
    assert args.count("--settings") == 1
    return json.loads(args[args.index("--settings") + 1])


def test_motor_ttl_profili_ve_zorla_tam():
    yakala = []
    kos = lambda args, *a: yakala.append(args) or SimpleNamespace(stdout="", stderr="", returncode=1)
    hafif.cagir("s", "m", {}, env={}, kos=kos)
    hafif.cagir("s", "m", {}, env={"CC_PROFIL_ZORLA": "tam"}, kos=kos)
    assert _ayar(yakala[0]) == TTL and "--settings" not in yakala[1]
    assert "--setting-sources" in yakala[0] and "--no-session-persistence" in yakala[0]  # a1 bayrakları yerinde


def test_motor_usage_yalniz_sayi(tmp_path, monkeypatch):
    monkeypatch.setattr(hafif, "USAGE_YOL", tmp_path / "u.jsonl")
    sonuc = {"type": "result", "result": "GIZLI METIN", "structured_output": {"a": "GIZLI"}, "total_cost_usd": 0.01,
             "usage": {"input_tokens": 3, "cache_read_input_tokens": 5, "cache_creation_input_tokens": 7, "output_tokens": 2,
                       "cache_creation": {"ephemeral_5m_input_tokens": 7, "ephemeral_1h_input_tokens": 0}, "service_tier": "standard"}}
    monkeypatch.setattr(hafif.subprocess, "run", lambda *a, **k: SimpleNamespace(stdout=json.dumps(sonuc) + "\n", stderr="", returncode=0))
    hafif._kos(["claude", "-p", "--model", "claude-sonnet-5-5", "--system-prompt", "GIZLI SISTEM"], "GIZLI GIRDI", {}, 10)
    metin = (tmp_path / "u.jsonl").read_text(encoding="utf-8")
    s = json.loads(metin)
    assert "GIZLI" not in metin and "standard" not in metin
    assert s["model"] == "claude-sonnet-5-5" and s["usd"] == 0.01 and isinstance(s["ts"], (int, float))
    assert s["usage"] == {"input_tokens": 3, "cache_read_input_tokens": 5, "cache_creation_input_tokens": 7, "output_tokens": 2,
                          "cache_creation": {"ephemeral_5m_input_tokens": 7, "ephemeral_1h_input_tokens": 0}}


def test_deney_ttl_kol_env_ile_tek_settings():
    assert _ayar(kur._ayar_args({"A": "1", "B": "${X}"}, {})) == {"env": {"A": "1"}, **TTL}
    assert kur._ayar_args({}, {}) == ["--settings", json.dumps(TTL)]
    assert kur._ayar_args({"A": "1"}, {"CC_PROFIL_ZORLA": "tam"}) == ["--settings", json.dumps({"env": {"A": "1"}})]
    assert kur._ayar_args({}, {"CC_PROFIL_ZORLA": "tam"}) == []
