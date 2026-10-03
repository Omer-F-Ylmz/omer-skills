"""TOKEN-6f: Headroom 0.39.0 sıcak önbellek kırılması — kurulu runtime'ın prefix_tracker'ı üzerinde davranış.
K2 kökü: (i) recap/away_summary yan isteği ana lineage zincirini ezer → sonraki tur yeni lineage → frozen 0
(prefix_tracker.py:1488, :926); (iii) tracker TTL 600 sn (models.py:342) < CC önbelleği 1 sa.
frozen == 0 → kompress_background kuyruğa (anthropic.py:1835-1837) + read_maturation tüm geçmişe (:2366) → önek kırılır.
Sentetik diziler gerçek away_summary yapısından (system/away_summary, isMeta, 203 krk; içerik maskeli)."""
import importlib.util
import sys
from pathlib import Path

import pytest

SP = Path.home() / "AppData/Local/Headroom/headroom/runtime/venv/Lib/site-packages"
PT = SP / "headroom/cache/prefix_tracker.py"
AWAY = 203

pytestmark = pytest.mark.skipif(not PT.is_file(), reason="Headroom runtime kurulu değil")


def yukle(yol):
    spec = importlib.util.spec_from_file_location(f"pt_{abs(hash(str(yol)))}", yol)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m  # dataclass modül sözlüğünü arar
    spec.loader.exec_module(m)
    return m


@pytest.fixture
def pt():
    return yukle(PT)


def u(n, tag="u"):
    return {"role": "user", "content": [{"type": "text", "text": tag + "x" * n}]}


def asis(n=400):
    return {"role": "assistant", "content": [{"type": "text", "text": "c" * n}]}


def gecmis(k=12):
    m = [u(4000, "ilk")]
    for i in range(k):
        m += [{"role": "assistant", "content": [{"type": "text", "text": "y" * 300},
                                                 {"type": "tool_use", "id": f"t{i}", "name": "Read", "input": {"p": f"/f{i}"}}]},
              {"role": "user", "content": [{"type": "tool_result", "tool_use_id": f"t{i}", "content": "z" * 6000}]}]
    return m + [asis(150), u(800)]


def tur(store, msgs, cache_read, ttl=3600):
    """Handler'ın bir turu: lineage çöz → frozen oku → (yamalı handler) TTL ipucunu damgala → yanıtla güncelle."""
    t = store.resolve_tracker("sid", "anthropic", messages=msgs, cache_affinity="aff")
    f = t.get_frozen_message_count()
    t._cache_ttl_hint = ttl  # yamalı anthropic.py: _cc_ttl damgası; yamasızda etkisiz
    t.update_from_response(cache_read_tokens=cache_read, cache_write_tokens=500,
                           messages=msgs + [asis()], original_messages=msgs)
    return t, f


def bekle(store, sn):
    for t in store._trackers.values():
        t._last_activity -= sn
    store._last_cleanup -= 10 ** 6  # temizlik aralığını aç


def isit(pt):
    """İki turluk ısınmış ana konuşma; (store, ana tracker, ana tur mesajları M)."""
    store = pt.SessionTrackerStore(default_config=pt.PrefixFreezeConfig())
    M = gecmis()
    tur(store, M[:-2], 55000)
    t1, f1 = tur(store, M, 60000)
    assert f1 > 0
    return store, t1, M


SONRAKI = {
    "yalin": [u(500)],
    "away_ayri_mesaj": [u(AWAY, "away:"), u(500)],
    "away_son_usera_ekli": [{"role": "user", "content": [{"type": "text", "text": "away:" + "x" * AWAY},
                                                         {"type": "text", "text": "x" * 500}]}],
}


@pytest.mark.parametrize("bicim", SONRAKI)
def test_sicak_recap_catali_frozen_korunur(pt, bicim):
    store, t1, M = isit(pt)
    ty, _ = tur(store, M + [asis(), u(300, "recap:")], 62000)  # özet yan isteği: ana lineage'ın devamı
    assert ty is t1
    t2, f2 = tur(store, M + [asis()] + SONRAKI[bicim], 63000)
    assert t2 is t1, "gerçek tur ana lineage'a dönmeli"
    assert 0 < f2 <= len(M) + 1, "frozen sıcak önekte kalır, çatal noktasını aşmaz"


def test_sicak_bosluk_frozen_korunur(pt):
    store, t1, M = isit(pt)
    bekle(store, 700)  # 600 sn tracker TTL'ini aşar, 1 sa önbellek hâlâ sıcak
    t2, f2 = tur(store, M + [asis(), u(500)], 63000)
    assert t2 is t1 and f2 > 0


@pytest.mark.parametrize("durum", ["bosluk_ttl_ustu", "bosluk_5dk_istemci", "onek_degismis"])
def test_soguk_onek_kompress_ve_maturation_tetiklenir(pt, durum):
    """Önek gerçekten soğukken frozen 0 kalır → kompress_background + read_maturation tetiklenir (yamalı da)."""
    store, t1, M = isit(pt)
    if durum == "bosluk_ttl_ustu":
        bekle(store, 3700)  # > 3600 sn önbellek TTL'i
        sonraki = M + [asis(), u(500)]
    elif durum == "bosluk_5dk_istemci":
        for t in store._trackers.values():
            t._cache_ttl_hint = 300
        bekle(store, 700)
        sonraki = M + [asis(), u(500)]
    else:
        eski = {"role": "user", "content": [{"type": "tool_result", "tool_use_id": "t0", "content": "w" * 6000}]}
        sonraki = M[:2] + [eski] + M[3:] + [asis(), u(500)]  # erken tool_result değişti
    _, f2 = tur(store, sonraki, 30000)
    assert f2 == 0
