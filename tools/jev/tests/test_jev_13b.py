import json
from pathlib import Path

import pytest

from jev import ayristir as a
from jev import cekirdek as c
from jev import cli
from test_jev_cekirdek import ENV, NOUL, Sahte

F = Path(__file__).parent / "fixtures"


def cevapla(questions, noul=0.3):
    out = {}
    for ad, s in questions.items():
        if s["type"] == "noul":
            out[ad] = {"type": "noul", "noul": noul}
        elif s["type"] == "choice":
            ilk = next(iter(s["criteria"]))
            out[ad] = {"type": "choice", "choice": ilk, "probabilities": {ilk: 0.9}, "confidence": 0.9}
        else:
            out[ad] = {"type": "score", "score": 1.0, "legend": {}, "confidence": 0.7}
    return out


def api(noul_sec=lambda state: 0.3, istekler=None):
    def gonder(url, basliklar, govde):
        g = json.loads(govde)
        if istekler is not None:
            istekler.append(g)
        return 200, {}, json.dumps({"answers": cevapla(g["questions"], noul_sec(g["state"]))}).encode()
    return gonder


def calistir(argv, capsys, env=ENV, gonder=None):
    kod = cli.main(argv, env=env, gonder=gonder or api(), uyu=lambda s: None)
    o = capsys.readouterr()
    return kod, o.out, o.err


@pytest.fixture
def veri(tmp_path, monkeypatch):
    monkeypatch.setattr(c, "BANT_YOLU", tmp_path / "bantlar.json")
    v = tmp_path / "k.jsonl"
    v.write_text("\n".join(json.dumps({"mesaj": f"m{i}", "niyet": "kargo", "acil": False, "sinir": False}) for i in range(4)))
    return v


# --- K1 bantlar ---
def test_kalibre_bantlar_jsonu_degistirmez(veri, tmp_path, capsys):
    c.BANT_YOLU.write_text('{"act": 0.85, "flag": 0.6}')
    once = c.BANT_YOLU.read_text()
    kod, _, _ = calistir(["kalibre", "--veri", str(veri), "--cikti", str(tmp_path / "k.md")], capsys)
    assert kod == 0 and c.BANT_YOLU.read_text() == once
    assert "öneri" in (tmp_path / "k.md").read_text(encoding="utf-8")


def test_bant_yaz_oneri_tabanin_altindaysa_taban_yazilir(veri, tmp_path, capsys):
    kod, _, _ = calistir(["kalibre", "--veri", str(veri), "--cikti", str(tmp_path / "k.md"), "--bant-yaz"], capsys)
    b = json.loads(c.BANT_YOLU.read_text())
    assert kod == 0 and b["act"] == 0.85 and b["flag"] >= 0.60  # sahte öneri 0.7 < 0.85


def test_noul_045_escalate():
    k = c.kesinlik({"type": "noul", "noul": 0.45})
    assert k == pytest.approx(0.55) and c.bant(k, c.VARSAYILAN_BANT) == "Escalate"


# --- K2 çift birim tavan ---
def test_istek_tavani_tekrarlari_sayar_m_arti_1_agsiz():
    s = Sahte((429, {}, b"{}"), (429, {}, b"{}"))
    t = c.Tasiyici(env=ENV, gonder=s, uyu=lambda x: None, istek_tavan=2)
    with pytest.raises(c.TavanHata):
        t.yargila(["x"], NOUL)
    assert len(s.istekler) == 2 and t.istek == 2


def test_istek_tavani_onceden_kontrol():
    s = Sahte()
    t = c.Tasiyici(env=ENV, gonder=s, uyu=lambda x: None, istek_tavan=3)
    with pytest.raises(c.TavanHata):
        t.yargila(["a", "b", "c", "d", "e"], NOUL)
    assert s.istekler == []


def test_batch_tavani_ayri_calisir():
    s = Sahte()
    t = c.Tasiyici(env=ENV, gonder=s, uyu=lambda x: None, en_fazla=1, istek_tavan=250)
    t.yargila(["x"], NOUL)
    with pytest.raises(c.TavanHata):
        t.yargila(["y"], NOUL)
    assert len(s.istekler) == 1 and t.cagri == 1 and t.istek == 1


def test_json_iki_sayiyi_verir(capsys):
    kod, out, _ = calistir(["log", str(F / "pytest.txt"), "--json"], capsys)
    j = json.loads(out)
    assert kod == 0 and j["cagri"] == {"batch": 1, "istek": 3} and len(j["satirlar"]) == 3


def test_tablo_altinda_iki_sayi(capsys):
    kod, out, _ = calistir(["log", str(F / "pytest.txt")], capsys)
    assert kod == 0 and "1/5 batch" in out and "3/250 istek" in out and len(out.splitlines()) <= 25


# --- K3 kanit parçalama ---
def test_kanit_60k_parcalanir_destek_bulunur(tmp_path, capsys):
    dolgu = ["dolgu satırı " + "x" * 90] * 2400
    dolgu[2000] = "DESTEK: gitleaks taraması 0 sızıntı buldu."
    k = tmp_path / "kanit.txt"
    k.write_text("\n".join(dolgu), encoding="utf-8")
    assert c.token(k.read_text(encoding="utf-8")) > 56_000
    r = tmp_path / "rapor.md"
    r.write_text("- gitleaks 0 sızıntı.\n", encoding="utf-8")
    istekler = []
    kod, out, err = calistir(["kanit", str(r), str(k)], capsys, gonder=api(lambda s: 0.95 if "DESTEK" in s else 0.1, istekler))
    assert kod == 0, err
    assert len(istekler) >= 3 and "destekli" in out


# --- K4 JEV_MCP_TOKEN ---
def test_mcp_token_yolu(capsys):
    token = "jevmcp-" + "7c" * 16
    goruldu = []

    def mcp(url, basliklar, govde):
        g = json.loads(govde)
        assert url == c.MCP_URL and basliklar["x-api-key"] == token and "Authorization" not in basliklar
        assert g["method"] == "tools/call" and g["params"]["name"] == "jev_batch"
        arg = g["params"]["arguments"]
        goruldu.append(len(arg["states"]))
        sonuc = [{"index": i, "ok": True, "answers": cevapla(arg["questions"])} for i in range(len(arg["states"]))]
        return 200, {}, json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": json.dumps(sonuc)}]}}).encode()

    kod, out, err = calistir(["log", str(F / "pytest.txt"), "--json"], capsys, env={"JEV_MCP_TOKEN": token}, gonder=mcp)
    assert kod == 0 and goruldu == [3]
    assert json.loads(out)["cagri"] == {"batch": 1, "istek": 1}
    assert token not in out and token not in err


# --- K5 SkillSpector gerçek şema ---
def test_skillspector_gercek_sema():
    b = a.bulgular(json.loads((F / "skillspector.json").read_text(encoding="utf-8")))
    assert b[0]["kural"] == "TM1" and b[0]["dosya"] == "SKILL.md" and b[0]["satir"] == 226
    assert "HIGH" in b[0]["state"] and "Tool Parameter Abuse" in b[0]["state"]
    assert "özgün kod" not in b[0]["state"] and "özgün eşleşme" not in b[0]["state"]
