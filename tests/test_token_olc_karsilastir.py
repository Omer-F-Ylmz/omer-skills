"""TOKEN-6b K1: tools/token_olc.py --karsilastir — grup başına dönem başı, ölçüm koşusu ayrımı, Σ pay × düşüş."""
import json
import time

from test_token_olc import SIMDI, asistan, t, usage, yaz

OMER = "C:\\Projeler\\omer-skills"


def zs(sn_once):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(SIMDI - sn_once))


def kul(metin, sn_once, **ek):
    return {"type": "user", "timestamp": zs(sn_once), "message": {"role": "user", "content": metin}, **ek}


def ist(mid, sn_once, cikti, girdi=0, **ek):  # ağırlıklı = girdi + 5 × çıktı
    return asistan(mid, usage(girdi=girdi, cikti=cikti), ts=zs(sn_once), **ek)


def satir(kaynak, ajan, istek, agirlikli, proje=OMER, cikti=0):
    return {"proje": proje, "kaynak": kaynak, "ajan": ajan, "model": "claude-opus-5-5", "istek": istek, "girdi": 0,
            "cache_okuma": 0, "cache_5m": 0, "cache_1h": 0, "cikti": cikti, "agirlikli": agirlikli}


TABAN = {"pencere_gun": 14,
         "satirlar": [satir("etkilesimli", "ana", 10, 3000, cikti=600), satir("observer", "ana", 10, 1400, "C:\\o", 280)],
         "oturumlar": [{"proje": OMER, "kaynak": "etkilesimli", "ajan": "ana", "taban": 400}]}
BAS = {"varsayilan": SIMDI - 86400}


def kars(tmp_path, baslar=BAS, taban=TABAN, az=1):
    return t.karsilastir(taban, tmp_path / "p", baslar, simdi=SIMDI, az=az)


def test_toplam_tasarruf_pay_agirlikli(tmp_path):
    yaz(tmp_path / "p" / "e.jsonl", [kul("x", 100, cwd=OMER)] + [ist(f"e{i}", 90 - i, 30, cwd=OMER) for i in range(10)])
    yaz(tmp_path / "p" / "claude-mem-observer" / "o.jsonl", [ist("o", 50, 20, entry="sdk-ts")])
    r = kars(tmp_path)
    assert r["gruplar"]["etk·ana omer-skills"]["birincil"] == {"taban": 300, "simdi": 150}
    assert r["gruplar"]["observer"]["birincil"] == {"taban": 100, "simdi": 100}
    assert abs(r["tasarruf"] - 3000 / 4400 * 0.5) < 1e-9


def test_olcum_kosusu_ayri_ve_haric(tmp_path):
    yaz(tmp_path / "p" / "a.jsonl", [kul("ok", 100), ist("a", 90, 10, entry="sdk-cli")])
    yaz(tmp_path / "p" / "a" / "subagents" / "x.jsonl", [ist("ax", 80, 10, entry="sdk-cli", isSidechain=True)])
    yaz(tmp_path / "p" / "b.jsonl", [kul("gerçek iş", 100), ist("b", 90, 20, entry="sdk-cli")])
    r = kars(tmp_path)
    assert r["gruplar"]["claude-p"]["istek"] == 1
    assert r["olcum"] == {"oturum": 2, "istek": 2, "agirlikli": 100}


def test_grup_basina_donem_basi(tmp_path):
    yaz(tmp_path / "p" / "e.jsonl", [ist("e1", 5000, 10, cwd=OMER), ist("e2", 500, 20, cwd=OMER)])
    yaz(tmp_path / "p" / "claude-mem-observer" / "o.jsonl", [ist("o1", 5000, 10), ist("o2", 500, 10)])
    g = kars(tmp_path, {"varsayilan": SIMDI - 86400, "etk·ana omer-skills": SIMDI - 1000})["gruplar"]
    assert (g["etk·ana omer-skills"]["istek"], g["etk·ana omer-skills"]["bas"]) == (1, SIMDI - 1000)
    assert g["observer"]["istek"] == 2


def test_cikti_ilk_istem_usd(tmp_path):
    yaz(tmp_path / "p" / "e.jsonl", [ist("e1", 90, 10, girdi=600, cwd=OMER), ist("e2", 80, 30, girdi=700, cwd=OMER)])
    g = kars(tmp_path)["gruplar"]["etk·ana omer-skills"]
    assert g["cikti_istek"] == {"taban": 60, "simdi": 20}
    assert g["ilk_istem"] == {"taban": 400, "simdi": 600}
    assert abs(g["usd_istek"]["taban"] - 600 * 20 / 1e6 / 10) < 1e-12


def test_claude_p_cagri_basi(tmp_path):
    for i in range(2):
        yaz(tmp_path / "p" / f"c{i}.jsonl", [kul("iş", 100), ist(f"c{i}a", 90, 10, entry="sdk-cli"),
                                             ist(f"c{i}b", 80, 10, entry="sdk-cli")])
    taban = {**TABAN, "satirlar": TABAN["satirlar"] + [satir("claude-p", "ana", 4, 400)],
             "oturumlar": TABAN["oturumlar"] + [{"proje": OMER, "kaynak": "claude-p", "ajan": "ana", "taban": 1}] * 2}
    assert kars(tmp_path, taban=taban)["gruplar"]["claude-p"]["birincil"] == {"taban": 200, "simdi": 100}


def test_yetersiz_ornek_isaretli_ve_toplamda_yok(tmp_path):
    yaz(tmp_path / "p" / "e.jsonl", [ist("e1", 90, 30, cwd=OMER)])
    r = kars(tmp_path, az=30)
    assert r["gruplar"]["etk·ana omer-skills"]["yetersiz"] is True
    assert r["tasarruf"] == 0


def test_main_karsilastir(tmp_path, capsys):
    taban = tmp_path / "taban.json"
    taban.write_text(json.dumps(TABAN), encoding="utf-8")
    out = tmp_path / "o.json"
    assert t.main(["olc", "--karsilastir", str(taban), "--kok", str(tmp_path / "p"),
                   "--bas", "varsayilan=2026-10-02T15:00:14Z", "--cikti", str(out)]) == 0
    assert "yetersiz" in capsys.readouterr().out and out.is_file()
