import json
from pathlib import Path

import pytest

from jev import cekirdek as c
from jev import cli

F = Path(__file__).parent / "fixtures"
ANAHTAR = "sk-or-v1-" + "f00dbabe" * 6
ENV = {"OPENROUTER_API_KEY": ANAHTAR}


class Yargic:
    """Her soru tipine makul bir yanıt veren sahte taşıyıcı; giden gövdeleri saklar."""

    def __init__(self, noul=0.3):
        self.govdeler, self.noul = [], noul

    def __call__(self, url, basliklar, govde):
        self.govdeler.append(govde.decode())
        q = json.loads(govde)["questions"]
        cevap = {}
        for ad, s in q.items():
            if s["type"] == "noul":
                cevap[ad] = {"type": "noul", "noul": self.noul}
            elif s["type"] == "choice":
                ilk = next(iter(s["criteria"]))
                cevap[ad] = {"type": "choice", "choice": ilk, "probabilities": {ilk: 0.9}, "confidence": 0.9}
            else:
                cevap[ad] = {"type": "score", "score": 1.0, "legend": {}, "confidence": 0.7}
        return 200, {}, json.dumps({"model": "typesafe/jev-1.13", "answers": cevap}).encode()


@pytest.fixture(autouse=True)
def bantlar(tmp_path, monkeypatch):
    monkeypatch.setattr(c, "BANT_YOLU", tmp_path / "bantlar.json")


def calistir(argv, capsys, env=ENV, gonder=None):
    kod = cli.main(argv, env=env, gonder=gonder or Yargic(), uyu=lambda s: None)
    o = capsys.readouterr()
    return kod, o.out, o.err


def test_anahtar_yoksa_exit_2_yalniz_ad(capsys):
    kod, out, err = calistir(["log", str(F / "pytest.txt")], capsys, env={})
    assert kod == 2 and "TYPESAFE_API_KEY" in err and "OPENROUTER_API_KEY" in err and "JEV_MCP_TOKEN" in err


def test_log_tablosu(capsys):
    kod, out, err = calistir(["log", str(F / "dotnet-konsol.txt"), "--diff", "src/App/Siparis.cs"], capsys)
    assert kod == 0 and len(out.splitlines()) <= 25
    assert "Toplam_dogru" in out and "regresyon" in out


def test_ilgili_ilk_k(tmp_path, capsys):
    d = tmp_path / "m.py"
    d.write_text("\n".join(["def a():"] + ["  x = 1"] * 200))
    kod, out, _ = calistir(["ilgili", "kargo ücreti nerede", str(d), "-k", "2"], capsys)
    assert kod == 0 and out.count("m.py:") == 2


def test_kanit_desteklenmeyenleri_listeler(capsys):
    kod, out, _ = calistir(["kanit", str(F / "rapor.md"), str(F / "pytest.txt")], capsys, gonder=Yargic(noul=0.2))
    assert kod == 0 and "gitleaks 0 sızıntı" in out and out.count("\n| ") >= 5


def test_triage_gitleaks_gizli_alan_aga_gitmez(tmp_path, capsys):
    from test_jev_ayristir import GIZLI, gitleaks_kaydi

    d = tmp_path / "gitleaks.json"
    d.write_text(json.dumps(gitleaks_kaydi()))
    y = Yargic()
    kod, out, _ = calistir(["triage", str(d)], capsys, gonder=y)
    assert kod == 0 and y.govdeler and all(GIZLI not in g for g in y.govdeler)
    assert GIZLI not in out


def test_tavan_cli(capsys, tmp_path):
    d = tmp_path / "m.py"
    d.write_text("x = 1\n")
    kod, _, err = calistir(["ilgili", "s", str(d), "--en-fazla", "0"], capsys)
    assert kod == 1 and "tavan" in err


def test_anahtar_hicbir_ciktida_yok(tmp_path, capsys):
    veri = tmp_path / "k.jsonl"
    veri.write_text("\n".join(json.dumps({"mesaj": f"m{i}", "niyet": "kargo", "acil": i % 2 == 0, "sinir": i == 0}, ensure_ascii=False) for i in range(4)), encoding="utf-8")
    md = tmp_path / "kalibre.md"
    kod, out, err = calistir(["kalibre", "--veri", str(veri), "--cikti", str(md)], capsys)
    assert kod == 0
    kod2, out2, err2 = calistir(["log", str(F / "pytest.txt"), "--json"], capsys, gonder=lambda u, b, g: (401, {}, ANAHTAR.encode()))
    assert kod2 == 1
    for metin in (out, err, out2, err2, md.read_text(encoding="utf-8"), c.BANT_YOLU.read_text()):
        assert ANAHTAR not in metin


def test_kalibre_bantlari_yazar(tmp_path, capsys):
    veri = tmp_path / "k.jsonl"
    veri.write_text("\n".join(json.dumps({"mesaj": f"m{i}", "niyet": "kargo", "acil": False, "sinir": False}) for i in range(4)))
    md = tmp_path / "kalibre.md"
    y = Yargic()
    kod, _, _ = calistir(["kalibre", "--veri", str(veri), "--cikti", str(md)], capsys, gonder=y)
    b = json.loads(c.BANT_YOLU.read_text())
    assert kod == 0 and {"act", "flag", "model"} <= b.keys()
    metin = md.read_text(encoding="utf-8")
    assert "n=4" in metin and "Brier" in metin and "doygunluk" in metin.lower()
    assert {json.loads(g)["model"] for g in y.govdeler} == {"jev-1.13", "jev-latest"}


def test_kalibre_verisi_40_sentetik():
    satirlar = [json.loads(s) for s in (Path(__file__).parent / "veri" / "jev_kalibre.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    assert len(satirlar) == 40
    assert {s["niyet"] for s in satirlar} == {"kargo", "iade", "ödeme", "ürün", "diğer"}
    assert sum(s["sinir"] for s in satirlar) >= 12 and any(s["acil"] for s in satirlar)
    assert all(c.redakte(s["mesaj"]) == s["mesaj"] for s in satirlar)  # kişi verisi yok
