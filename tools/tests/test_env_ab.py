import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import env_ab  # noqa: E402

SIFIR = {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}


def test_butce_hatasi_olcum_sayilmaz():
    # d4: $0.50 aşılınca is_error + usage sıfır geldi, tsv'ye 0 jeton yazıldı
    with pytest.raises(SystemExit):
        env_ab.sonuc(json.dumps({"is_error": True, "subtype": "error_max_budget_usd", "usage": SIFIR}))


def test_plan_limiti_olcum_sayilmaz():
    with pytest.raises(SystemExit):
        env_ab.sonuc(json.dumps({"is_error": False, "result": "You've hit your session limit · resets 3am", "usage": SIFIR}))


def test_normal_yanit():
    u = {"input_tokens": 5, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 900}
    assert env_ab.sonuc(json.dumps({"is_error": False, "result": "tamam", "usage": u})) == (1005, 100)
