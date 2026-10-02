"""TOKEN-0 K1: tools/token_olc.py — oturum jsonl'lerinden ağırlıklı token ölçümü."""
import json
import os
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import token_olc as t  # noqa: E402

SIMDI = 1_790_000_000.0  # sabit "şimdi" (epoch sn)
TS = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(SIMDI - 3600))
ESKI_TS = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(SIMDI - 30 * 86400))
GIZLI = "GIZLI-ICERIK-METNI-42"


def usage(girdi=0, okuma=0, yazma=0, cikti=0, m5=None, h1=None):
    u = {"input_tokens": girdi, "cache_read_input_tokens": okuma,
         "cache_creation_input_tokens": yazma, "output_tokens": cikti}
    if m5 is not None or h1 is not None:
        u["cache_creation"] = {"ephemeral_5m_input_tokens": m5 or 0, "ephemeral_1h_input_tokens": h1 or 0}
    return u


def asistan(mid, u, ts=TS, entry="cli", model="claude-opus-5-5", **ek):
    o = {"type": "assistant", "timestamp": ts, "cwd": "C:\\p", "sessionId": "s1", "entrypoint": entry,
         "isSidechain": False, "message": {"id": mid, "model": model, "role": "assistant",
                                           "content": [{"type": "text", "text": GIZLI}], "usage": u}}
    o.update(ek)
    return o


def yaz(yol, satirlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(s if isinstance(s, str) else json.dumps(s) for s in satirlar), encoding="utf-8")
    os.utime(yol, (SIMDI - 60, SIMDI - 60))
    return yol


def tara(kok, **kw):
    return t.tara(kok, gun=14, simdi=SIMDI, **kw)


def test_agirlik_hesabi():
    u = usage(girdi=100, okuma=1000, yazma=30, cikti=10, m5=10, h1=20)
    assert t.agirlikli(u) == 100 + 1000 * 0.1 + 10 * 1.25 + 20 * 2 + 10 * 5


def test_5m_1h_ayrimi_ve_kirilimsiz_5m_sayilir():
    assert t.agirlikli(usage(h1=100, yazma=100, m5=0)) == 200
    assert t.agirlikli(usage(m5=100, yazma=100, h1=0)) == 125
    assert t.agirlikli(usage(yazma=100)) == 125  # kırılım yok → 5m


def test_eksik_usage_ve_bozuk_satir_atlanir(tmp_path):
    a = asistan("m1", usage(girdi=10))
    del a["message"]["usage"]
    yaz(tmp_path / "p" / "s.jsonl", ["{bozuk", a, asistan("m2", usage(girdi=7))])
    r = tara(tmp_path)
    assert r["bozuk_satir"] == 1 and r["usage_eksik"] == 1
    assert r["toplam"]["girdi"] == 7


def test_message_id_tekillestirme(tmp_path):
    a = asistan("m1", usage(girdi=10, cikti=2))
    yaz(tmp_path / "p" / "s.jsonl", [a, a])
    r = tara(tmp_path)
    assert r["toplam"]["girdi"] == 10 and r["toplam"]["istek"] == 1


def test_subagent_ayrimi(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [asistan("m1", usage(girdi=1))])
    yaz(tmp_path / "p" / "s" / "subagents" / "agent-x.jsonl",
        [asistan("m2", usage(girdi=2), isSidechain=True, agentId="x")])
    assert t.ajan_turu({"isSidechain": True}, Path("a.jsonl")) == "subagent"
    assert t.ajan_turu({}, Path("s/subagents/agent-1.jsonl")) == "subagent"
    assert t.ajan_turu({"agentId": "x"}, Path("a.jsonl")) == "subagent"
    assert t.ajan_turu({"isSidechain": False}, Path("a.jsonl")) == "ana"
    r = tara(tmp_path)
    ajan = {s["ajan"]: s["girdi"] for s in r["satirlar"]}
    assert ajan == {"ana": 1, "subagent": 2}


def test_claude_p_ve_observer_ayrimi(tmp_path):
    yaz(tmp_path / "p" / "a.jsonl", [asistan("m1", usage(girdi=1))])
    yaz(tmp_path / "p" / "b.jsonl", [asistan("m2", usage(girdi=2), entry="sdk-cli")])
    yaz(tmp_path / "C--Users-pc--claude-mem-observer-sessions" / "c.jsonl",
        [asistan("m3", usage(girdi=4), entry="sdk-ts")])
    r = tara(tmp_path)
    kaynak = {s["kaynak"]: s["girdi"] for s in r["satirlar"]}
    assert kaynak == {"etkilesimli": 1, "claude-p": 2, "observer": 4}
    assert t.kaynak({"entrypoint": "cli"}, Path("C--Users-pc--claude-mem-observer-sessions/x.jsonl")) == "observer"


def test_tarih_penceresi(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [asistan("m1", usage(girdi=5), ts=ESKI_TS), asistan("m2", usage(girdi=3))])
    eski = yaz(tmp_path / "p" / "eski.jsonl", [asistan("m3", usage(girdi=100))])
    os.utime(eski, (SIMDI - 30 * 86400, SIMDI - 30 * 86400))
    r = tara(tmp_path)
    assert r["toplam"]["girdi"] == 3 and r["dosya"] == 1


def test_oturum_taban_tur_son_ctx(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [asistan("m1", usage(girdi=5, okuma=100, yazma=20, m5=20)),
                                     asistan("m2", usage(girdi=1, okuma=200, yazma=10, h1=10))])
    o = tara(tmp_path)["oturumlar"][0]
    assert (o["taban"], o["tur"], o["son_ctx"]) == (125, 2, 211)


def test_en_buyuk_n_arac_ve_gorsel(tmp_path):
    satirlar = []
    for i, n in enumerate([40, 4000, 400]):
        satirlar.append({"type": "assistant", "timestamp": TS, "message": {
            "id": f"m{i}", "model": "x", "usage": usage(girdi=1),
            "content": [{"type": "tool_use", "id": f"t{i}", "name": f"Arac{i}", "input": {}}]}})
        satirlar.append({"type": "user", "timestamp": TS, "message": {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": f"t{i}", "content": "x" * n}]}})
    png = "iVBORw0KGgoAAAANSUhEUgAAAPAAAAB4CAYAAAA"  # 240x120 PNG başlığı
    satirlar.append({"type": "user", "timestamp": TS, "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": "t0", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": png}}]}]}})
    yaz(tmp_path / "p" / "s.jsonl", satirlar)
    r = tara(tmp_path, en_buyuk=2)
    assert [(a["arac"], a["token"]) for a in r["en_buyuk_arac"]] == [("Arac1", 1000), ("Arac2", 100)]
    o = r["oturumlar"][0]
    assert o["gorsel"] == 1 and o["gorsel_token"] == round(240 * 120 / 750)


def test_ek_turu_boyutu(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [
        {"type": "attachment", "timestamp": TS, "attachment": {"type": "hook_additional_context", "content": ["x" * 400]}},
        asistan("m1", usage(girdi=1))])
    ek = tara(tmp_path)["ekler"]["hook_additional_context"]
    assert ek["adet"] == 1 and ek["karakter"] >= 400


def test_bos_klasor(tmp_path):
    r = tara(tmp_path)
    assert r["dosya"] == 0 and r["toplam"]["agirlikli"] == 0 and r["satirlar"] == []


def test_ciktida_icerik_metni_yok(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [asistan("m1", usage(girdi=1)), {"type": "user", "timestamp": TS, "message": {
        "role": "user", "content": [{"type": "tool_result", "tool_use_id": "t", "content": GIZLI}]}}])
    r = tara(tmp_path)
    assert GIZLI not in json.dumps(r, ensure_ascii=False) and GIZLI not in t.tablo(r)
