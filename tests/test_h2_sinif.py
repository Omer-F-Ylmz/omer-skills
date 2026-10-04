import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import h2_sinif as H  # noqa: E402

T0 = time.time() - 86400


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(t))


def yaz(yol, satirlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("".join(json.dumps(s) + "\n" for s in satirlar), encoding="utf-8")


def kul(t):
    return {"type": "user", "timestamp": iso(t)}


def ist(mid, t, cr, h1, **ek):
    u = {"input_tokens": 1, "cache_read_input_tokens": cr, "output_tokens": 1,
         "cache_creation": {"ephemeral_5m_input_tokens": 0, "ephemeral_1h_input_tokens": h1}}
    return {"type": "assistant", "timestamp": iso(t), "message": {"id": mid, "model": "claude-opus-5-5", "usage": u}, **ek}


def away(t):
    return {"type": "system", "subtype": "away_summary", "timestamp": iso(t)}


def oturum(t, ek=None):
    return [kul(t), ist("1", t + 1, 0, 1000, **(ek or {})), kul(t + 300), away(t + 301), ist("2", t + 302, 0, 1100, **(ek or {})),
            kul(t + 600), ist("3", t + 601, 2100, 50, **(ek or {}))]


def test_recap_testi_ve_filtre(tmp_path):
    yaz(tmp_path / "C--proje" / "a.jsonl", oturum(T0))
    yaz(tmp_path / "C--Users-pc-Desktop-Kendi-oyun-modlarim" / "b.jsonl", oturum(T0))
    yaz(tmp_path / "C--proje" / "c.jsonl", oturum(T0, {"entrypoint": "sdk-cli"}))
    ist_ = H.istekler(tmp_path)
    r = H.recap(ist_, T0 - 10, T0 + 1000)
    assert (r["oturum"], r["istek"]) == (1, 3)
    assert (r["away_var"]["n"], r["away_var"]["kirik"]) == (1, 1)
    assert (r["away_yok"]["n"], r["away_yok"]["kirik"]) == (1, 0)
    assert r["away_var"]["ek_w"] == 1000 * (2 - 0.1)
    assert H.recap(ist_, T0 + 5000, T0 + 9000)["istek"] == 0


def h2a(rid, t, cr, cw, ist_m, sik_m, tr=()):
    return {"ts": iso(t).replace("Z", "+00:00"), "request_id": rid, "cache_read_tokens": cr, "cache_write_tokens": cw,
            "transforms_applied": list(tr), "request_messages": [["user", x] for x in ist_m],
            "compressed_messages": [["user", x] for x in sik_m]}


def test_h2a_oku_tekillestirir(tmp_path):
    yol = tmp_path / "h.jsonl"
    yaz(yol, [h2a("r1", T0, 0, 1, "a", "a"), h2a("r1", T0, 0, 1, "a", "a"), {"bosluk": "2026-10-04T10:00:00"},
              {"hata": "x", "ts": "2026-10-04T10:01:00"}])
    kayit, bosluk = H.h2a_oku(yol)
    assert len(kayit) == 1 and len(bosluk) == 1


def test_sinifla(tmp_path):
    def r(t, ara, b=500, aw=False, ttl=3600, olay=False):
        return {"oturum": "s", "an": t, "ts": t, "ara": ara, "b": b, "away": aw, "ttl": ttl, "olay": olay,
                "cr": int(t), "cw": 7, "onceki": (int(t) - 1, 7, t - 1), "ek_w": b, "ek_usd": 0.0}
    hp = lambda t, m: h2a(f"p{t}", t - 1, int(t) - 1, 7, m, m)  # noqa: E731
    kayit = []
    istek = []
    for t, aw, ist_m, sik_m, tr in ((T0, True, "abc", "axc", ()), (T0 + 10, False, "abc", "axc", ("kompress_background",)),
                                   (T0 + 20, False, "abc", "abc", ()), (T0 + 30, False, "xbc", "xbc", ())):
        kayit += [hp(t, "ab"), h2a(f"c{t}", t, int(t), 7, ist_m, sik_m, tr)]
        istek.append(r(t, 60, aw=aw))
    istek += [r(T0 + 40, 4000), r(T0 + 50, 60), r(T0 + 60, 60, b=0), r(T0 + 70, 60, olay=True)]  # d · eşleşmedi · kırılmasız · eylem
    # CC öneki sonda değişir (cache_control kayması), Headroom daha önce (1) → b · mesaj kaydı boş → e
    kayit += [h2a("p80", T0 + 79, int(T0 + 80) - 1, 7, "abcd", "abcd"), h2a("c80", T0 + 80, int(T0 + 80), 7, "abce", "aycd"),
              h2a("p90", T0 + 89, int(T0 + 90) - 1, 7, "", ""), h2a("c90", T0 + 90, int(T0 + 90), 7, "", "")]
    istek += [r(T0 + 80, 60), r(T0 + 90, 60)]
    istek.append(r(T0 + 500, 60))
    s = H.sinifla(istek, kayit, [], kayit_yok=[(T0 + 400, T0 + 600)], bas=T0 - 1, bit=T0 + 1000)
    adet = {k: v["adet"] for k, v in s["sinif"].items()}
    assert adet == {"a": 1, "b": 2, "c": 1, "d": 1, "e": 4, "kayit_yok": 1, "bosluk": 0}
    assert s["e_sebep"] == {"cc_onek": 1, "eslesmedi": 1, "oturum_eylemi": 1, "mesaj_yok": 1}
    assert s["sicak_headroom_etiketli"] == 1
    assert s["sinif"]["a"]["token"] == 500


def test_bosluk_kapsar():
    istek = [{"oturum": "s", "an": T0, "ts": T0, "ara": 60, "b": 9, "away": False, "ttl": 3600, "olay": False,
              "cr": 1, "cw": 1, "onceki": (0, 1, T0 - 1), "ek_w": 0, "ek_usd": 0}]
    s = H.sinifla(istek, [], [T0 + 30], kayit_yok=[], bas=T0 - 1, bit=T0 + 1)
    assert s["sinif"]["bosluk"]["adet"] == 1
