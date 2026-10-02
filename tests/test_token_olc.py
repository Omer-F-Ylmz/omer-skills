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


# --- TOKEN-1b K5: gerçek $ sütunu + motor-usage ayrı kaynak ---
# Beklenen fiyatlar ($/MTok: girdi · okuma · yazma5m · yazma1h · çıktı) platform.claude.com/docs/en/about-claude/pricing
# "Model pricing" tablosundan (2 Eki 2026) bağımsız yazıldı; tek fiyat değişirse burada en az bir test kırmızı olur.
RESMI = {"claude-opus-5-5": (4, 0.20, 5, 8, 20), "claude-opus-5": (5, 0.50, 6.25, 10, 25),
         "claude-sonnet-5-5": (2, 0.20, 2.50, 4, 10), "claude-sonnet-5": (2, 0.20, 2.50, 4, 10),
         "claude-haiku-4-5-20251001": (1, 0.10, 1.25, 2, 5)}


def test_usd_her_model_her_kalem_resmi_fiyat():
    for model, f in RESMI.items():
        for i, alan in enumerate(("girdi", "okuma", "m5", "h1", "cikti")):
            u = usage(**{"girdi": {"girdi": 1_000_000}, "okuma": {"okuma": 1_000_000}, "m5": {"m5": 1_000_000, "yazma": 1_000_000},
                         "h1": {"h1": 1_000_000, "yazma": 1_000_000}, "cikti": {"cikti": 1_000_000}}[alan])
            assert abs(t.usd(u, model) - f[i]) < 1e-9, (model, alan)


def test_usd_en_uzun_onek_ve_bilinmeyen_model():
    u = usage(girdi=1_000_000)
    assert t.usd(u, "claude-opus-5-5") == 4 and t.usd(u, "claude-opus-5") == 5  # opus-5-5 opus-5'e düşmez
    assert t.usd(u, "<synthetic>") is None and t.usd(u, None) is None


def test_tara_satir_toplam_oturum_usd_ve_fiyatsiz_sayaci(tmp_path):
    yaz(tmp_path / "p" / "s.jsonl", [asistan("m1", usage(girdi=1_000_000, cikti=100_000)),
                                      asistan("m2", usage(okuma=1_000_000, m5=1_000_000, yazma=1_000_000), model="claude-sonnet-5"),
                                      asistan("m3", usage(girdi=5), model="<synthetic>")])
    r = tara(tmp_path)
    assert abs(r["toplam"]["usd"] - (4 + 2 + 0.20 + 2.50)) < 1e-9 and r["fiyatsiz_istek"] == 1
    assert abs(r["oturumlar"][0]["usd"] - 8.70) < 1e-9
    assert "$" in t.tablo(r) and "8.70" in t.tablo(r)


def test_motor_usage_ayri_kaynak_satiri(tmp_path):
    m = tmp_path / "motor-usage.jsonl"
    m.write_text("\n".join([json.dumps({"ts": SIMDI - 60, "model": "claude-sonnet-5-5", "usage": {
                     "input_tokens": 1_000_000, "cache_creation": {"ephemeral_5m_input_tokens": 1_000_000, "ephemeral_1h_input_tokens": 0}},
                     "usd": 9.99}),
                 json.dumps({"ts": SIMDI - 30 * 86400, "model": "claude-sonnet-5-5", "usage": {"input_tokens": 7}, "usd": 1}),
                 "bozuk"]), encoding="utf-8")
    r = t.tara(tmp_path / "yok", gun=14, simdi=SIMDI, motor=m)
    s = [x for x in r["satirlar"] if x["kaynak"] == "motor"]
    assert len(s) == 1 and s[0]["istek"] == 1 and s[0]["cache_5m"] == 1_000_000
    assert abs(s[0]["usd"] - (2 + 2.50)) < 1e-9 and s[0]["agirlikli"] == 1_000_000 + 1_250_000  # fiyat tablodan, kayıttaki usd değil
    assert "motor" in t.tablo(r)


def test_motor_usage_yoksa_satir_yok(tmp_path):
    r = t.tara(tmp_path, gun=14, simdi=SIMDI, motor=tmp_path / "yok.jsonl")
    assert r["satirlar"] == [] and r["toplam"]["usd"] == 0


TS2 = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(SIMDI - 7200))
SIK = "Condense the tool payload below to under 12800 characters.\n\n"


def kul(metin, ts=TS):
    return {"type": "user", "timestamp": ts, "message": {"role": "user", "content": [{"type": "text", "text": metin}]}}


def test_compress_1h_yazma_uyarisi(tmp_path):
    """TOKEN-2: cmem yaması claude-mem güncellemesinde sessizce silinir → son compress isteğinde 1h yazma UYARI verir."""
    obs = tmp_path / "C--Users-pc--claude-mem-observer-sessions"
    yaz(obs / "eski.jsonl", [kul(SIK, TS2), asistan("m1", usage(girdi=1, yazma=500, h1=500), ts=TS2)])
    yaz(obs / "yeni.jsonl", [{**kul(""), "message": {"role": "user", "content": SIK}}, asistan("m2", usage(girdi=500))])
    yaz(obs / "bilgi.jsonl", [kul("You are a knowledge agent"), asistan("m3", usage(yazma=900, h1=900))])
    assert "UYARI" not in t.tablo(tara(tmp_path))
    yaz(obs / "yeni.jsonl", [kul(SIK), asistan("m2", usage(girdi=1, yazma=500, h1=500))])
    assert "UYARI: cmem yaması yok → python tools/cmem_yama.py" in t.tablo(tara(tmp_path))
