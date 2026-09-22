import json

import pytest

from jev import cekirdek as c

# Sahte anahtarlar çalışma anında kurulur: repoda gitleaks'e takılacak düz desen yok.
OR_ANAHTAR = "sk-or-v1-" + "a1b2c3d4" * 6
ENV = {"OPENROUTER_API_KEY": OR_ANAHTAR}
NOUL = {"acil": {"type": "noul", "instructions": "Acil mi?"}}


def cevap(p=0.9):
    return json.dumps({"model": "typesafe/jev-1.13", "answers": {"acil": {"type": "noul", "noul": p}}, "usage": {}}).encode()


class Sahte:
    """gonder(url, basliklar, govde) -> (status, basliklar, govde). Sıradaki yanıtlar tükenince 200 döner."""

    def __init__(self, *yanitlar):
        self.yanitlar = list(yanitlar)
        self.istekler = []

    def __call__(self, url, basliklar, govde):
        self.istekler.append((url, basliklar, json.loads(govde)))
        return self.yanitlar.pop(0) if self.yanitlar else (200, {}, cevap())


def tasiyici(sahte, **k):
    uykular = []
    t = c.Tasiyici(env=ENV, gonder=sahte, uyu=uykular.append, **k)
    return t, uykular


# --- tekrar ---
def test_retry_after_uyulur():
    s = Sahte((429, {"retry-after": "3"}, b"{}"))
    t, uykular = tasiyici(s)
    t.yargila(["x"], NOUL)
    assert uykular == [3.0] and len(s.istekler) == 2


def test_529_ustel_geri_cekilme_2_tekrar_sonra_hata():
    s = Sahte(*[(529, {}, b"{}")] * 3)
    t, uykular = tasiyici(s)
    with pytest.raises(c.JevHata):
        t.yargila(["x"], NOUL)
    assert len(s.istekler) == 3 and uykular == [1, 2]


def test_400_tekrarlanmaz():
    s = Sahte((400, {}, b"{}"))
    t, _ = tasiyici(s)
    with pytest.raises(c.JevHata):
        t.yargila(["x"], NOUL)
    assert len(s.istekler) == 1


# --- tavan ---
def test_tavan_n_arti_1_agsiz_hata():
    s = Sahte()
    t, _ = tasiyici(s, en_fazla=1)
    t.yargila(["x"], NOUL)
    once = len(s.istekler)
    with pytest.raises(c.TavanHata):
        t.yargila(["y"], NOUL)
    assert len(s.istekler) == once


def test_tavan_parca_sayisini_onceden_sayar():
    s = Sahte()
    t, _ = tasiyici(s, en_fazla=2)
    with pytest.raises(c.TavanHata):
        t.yargila(["x"] * 450, NOUL)
    assert s.istekler == []


# --- parçalama ---
def test_450_oge_3_parca():
    assert [len(p) for p in c.parcala(list(range(450)))] == [200, 200, 50]


def test_mcp_arka_ucu_450_ogeyi_3_istekte_yollar():
    def mcp(url, basliklar, govde):
        n = len(json.loads(govde)["params"]["arguments"]["states"])
        sonuc = [{"index": i, "ok": True, "answers": {"acil": {"type": "noul", "noul": 0.9}}} for i in range(n)]
        mcp.n.append(n)
        return 200, {}, json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"content": [{"type": "text", "text": json.dumps(sonuc)}]}}).encode()

    mcp.n = []
    t = c.Tasiyici(env={"JEV_MCP_TOKEN": "t" * 20}, gonder=mcp, uyu=lambda s: None)
    sonuc = t.yargila(["x"] * 450, NOUL)
    assert mcp.n == [200, 200, 50] and len(sonuc) == 450 and t.cagri == 3


def test_32k_ustu_state_bolunur():
    buyuk = "\n".join(["satır " + "x" * 100] * 1400)  # ~35k token
    assert c.token(buyuk) > 32_000
    parcalar = c.bol_state(buyuk)
    assert len(parcalar) >= 2 and all(c.token(p) <= 32_000 for p in parcalar)
    assert c.bol_state("kısa") == ["kısa"]


def test_yargila_buyuk_statei_bolup_tek_sonuca_indirir():
    s = Sahte((200, {}, cevap(0.9)), (200, {}, cevap(0.55)))
    t, _ = tasiyici(s)
    sonuc = t.yargila(["\n".join(["x" * 100] * 1400)], NOUL)
    assert len(s.istekler) == 2 and len(sonuc) == 1
    assert sonuc[0]["acil"]["noul"] == 0.55  # parçalardan en belirsizi


# --- redaksiyon ---
TR_ORNEK = {
    "e-posta": "ali.veli@ornek.com.tr",
    "telefon": "0532 123 45 67",
    "tckn": "10000000146",
    "iban": "TR33 0006 1005 1978 6457 8413 26",
    "kart": "4111 1111 1111 1111",
}


@pytest.mark.parametrize("tur,deger", TR_ORNEK.items())
def test_redaksiyon_tr(tur, deger):
    r = c.redakte(f"müşteri {deger} yazdı")
    assert deger not in r and "[REDAKTE" in r


@pytest.mark.parametrize(
    "anahtar",
    ["sk-" + "Zx9" * 12, "ghp_" + "Ab1" * 12, "AKIA" + "IOSFODNN7EXAMPL" + "Q"],
)
def test_redaksiyon_anahtar(anahtar):
    r = c.redakte(f"token={anahtar} bitti")
    assert anahtar not in r and "[REDAKTE" in r


def test_state_aga_redakte_gider():
    s = Sahte()
    t, _ = tasiyici(s)
    t.yargila([f"bana {TR_ORNEK['e-posta']} ve {TR_ORNEK['tckn']} ile ulaşın"], NOUL)
    giden = json.dumps(s.istekler[0][2], ensure_ascii=False)
    assert TR_ORNEK["e-posta"] not in giden and TR_ORNEK["tckn"] not in giden


# --- anahtar ---
def test_anahtar_yalniz_baslikta():
    s = Sahte()
    t, _ = tasiyici(s)
    t.yargila(["x"], NOUL)
    url, basliklar, govde = s.istekler[0]
    assert url == "https://openrouter.ai/api/v1/systemone"
    assert basliklar["Authorization"] == f"Bearer {OR_ANAHTAR}"
    assert OR_ANAHTAR not in json.dumps(govde)


def test_hata_metninde_anahtar_ve_govde_yok():
    govde = json.dumps({"error": {"type": "auth", "message": f"bad key {OR_ANAHTAR} state=gizli"}}).encode()
    t, _ = tasiyici(Sahte((401, {}, govde)))
    with pytest.raises(c.JevHata) as e:
        t.yargila(["x"], NOUL)
    assert OR_ANAHTAR not in str(e.value) and "gizli" not in str(e.value) and "401" in str(e.value)


def test_arka_uc_sirasi():
    assert c.backend({"TYPESAFE_API_KEY": "a", "OPENROUTER_API_KEY": "b"})["ad"] == "TYPESAFE"
    assert c.backend({"OPENROUTER_API_KEY": "b", "JEV_MCP_TOKEN": "c"})["ad"] == "OPENROUTER"
    assert c.backend({"JEV_MCP_TOKEN": "c"})["ad"] == "MCP"
    assert c.backend({}) is None


def test_model_varsayilani_pinli():
    s = Sahte()
    t, _ = tasiyici(s)
    t.yargila(["x"], NOUL)
    assert s.istekler[0][2]["model"] == "jev-1.13"
    with pytest.raises(c.JevHata):
        c.Tasiyici(env=ENV, model="gpt-4")


# --- bantlar ---
@pytest.mark.parametrize("deger,beklenen", [(0.85, "Act"), (0.8499, "Flag"), (0.60, "Flag"), (0.5999, "Escalate")])
def test_bant_sinirlari(deger, beklenen):
    assert c.bant(deger, {"act": 0.85, "flag": 0.60}) == beklenen


def test_kesinlik():
    assert c.kesinlik({"type": "noul", "noul": 0.1}) == pytest.approx(0.9)
    assert c.kesinlik({"type": "choice", "choice": "a", "confidence": 0.7}) == 0.7


def test_bantlar_json_yoksa_varsayilan_ve_uyari(tmp_path, capsys):
    b = c.bantlar_oku(tmp_path / "yok.json")
    assert b == {"act": 0.85, "flag": 0.60}
    assert "uyarı" in capsys.readouterr().err


def test_bantlar_json_okunur(tmp_path):
    y = tmp_path / "bantlar.json"
    y.write_text(json.dumps({"act": 0.9, "flag": 0.7, "model": "jev-1.13"}))
    assert c.bantlar_oku(y)["act"] == 0.9


# --- tablo ---
def test_tablo_25_satiri_gecmez():
    t = c.tablo(["a", "b"], [[str(i), "x|y\nz"] for i in range(100)])
    satirlar = t.splitlines()
    assert len(satirlar) <= 25 and "--json" in satirlar[-1]
    assert "x|y" not in t
