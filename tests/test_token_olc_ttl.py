"""TOKEN-6b K2: tools/token_olc.py --ttl-sim — etkileşimli ana oturum önbellek yazması sınıflama ve TTL karşı-olgu kolları."""
import time

from test_token_olc import SIMDI, asistan, t, usage, yaz

T0 = SIMDI - 20_000


def zs(sn):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(T0 + sn))


def kul(sn):
    return {"type": "user", "timestamp": zs(sn), "message": {"role": "user", "content": "x"}}


def ist(mid, sn, okuma=0, m5=0, h1=0, effort="high", **kw):
    return asistan(mid, usage(okuma=okuma, yazma=m5 + h1, m5=m5, h1=h1), ts=zs(sn + 5), effort=effort, **kw)


def sim(tmp_path, *oturumlar):
    for i, satirlar in enumerate(oturumlar):
        yaz(tmp_path / "p" / f"s{i}.jsonl", satirlar)
    return t.ttl_sim(tmp_path / "p", gun=14, simdi=SIMDI)


def test_yazma_yeni_ve_bastan_ayrimi(tmp_path):
    r = sim(tmp_path, [kul(0), ist("a", 0, h1=1000), kul(10), ist("b", 10, okuma=1000, h1=200),
                       {"type": "system", "subtype": "compact_boundary", "timestamp": zs(20)},
                       kul(20), ist("c", 20, okuma=100, h1=1300)])
    assert r["yazma"] == {"a": 1400, "b": 1100}
    assert r["sebep"]["compact"] == {"adet": 1, "token": 1100}


def test_sebep_ara_ttl(tmp_path):
    r = sim(tmp_path, [kul(0), ist("a", 0, h1=1000), kul(4000), ist("b", 4000, okuma=0, h1=1050)])
    assert r["sebep"]["ara>ttl"] == {"adet": 1, "token": 1000}
    assert r["yazma"] == {"a": 1050, "b": 1000}


def test_sebep_model_effort_arac_diger(tmp_path):
    r = sim(tmp_path,
            [kul(0), ist("a", 0, h1=1000), kul(10), ist("b", 10, okuma=0, h1=1000, effort="xhigh")],
            [kul(0), ist("c", 0, h1=1000), {"type": "attachment", "timestamp": zs(5),
                                            "attachment": {"type": "deferred_tools_delta"}},
             kul(10), ist("d", 10, okuma=400, h1=600)],
            [kul(0), ist("e", 0, h1=1000), kul(10), ist("f", 10, okuma=700, h1=300)])
    assert r["sebep"]["model/effort"] == {"adet": 1, "token": 1000}
    assert r["sebep"]["arac_listesi"] == {"adet": 1, "token": 600}
    assert r["sebep"]["diger"] == {"adet": 1, "token": 300}


def test_5m_sinir_300_sn(tmp_path):
    a = sim(tmp_path / "a", [kul(0), ist("a", 0, h1=1000), kul(300), ist("b", 300, okuma=1000, h1=100)])
    b = sim(tmp_path / "b", [kul(0), ist("c", 0, h1=1000), kul(301), ist("d", 301, okuma=1000, h1=100)])
    assert a["kollar"]["1h"]["agirlikli"] == b["kollar"]["1h"]["agirlikli"] == 2300
    assert a["kollar"]["5m"]["agirlikli"] == 1475  # 300 sn: önbellek canlı
    assert b["kollar"]["5m"]["agirlikli"] == 2625  # 301 sn: okuma 5m yazmaya döner


def test_gonderim_zamani_user_satirindan(tmp_path):
    # asistan satırı geç yazılsa da ara = user satırları arası (0 → 200 sn)
    r = sim(tmp_path, [kul(0), ist("a", 0, h1=1000), kul(200),
                       asistan("b", usage(okuma=1000, yazma=100, m5=0, h1=100), ts=zs(900))])
    assert r["ara"]["n"] == 1 and r["ara"]["p50"] == 200
    assert r["kollar"]["5m"]["agirlikli"] == 1475


def test_hibrit_oturum_basina_ucuz_kol(tmp_path):
    hizli = [kul(0), ist("a", 0, h1=1000), kul(10), ist("b", 10, okuma=1000, h1=100)]
    yavas = [kul(0), ist("c", 0, h1=1000), kul(1000), ist("d", 1000, okuma=1000, h1=100)]
    r = sim(tmp_path, hizli, yavas)
    k = r["kollar"]
    assert k["1h"]["agirlikli"] == 4600
    assert k["5m"]["agirlikli"] == 1475 + 2625
    assert k["hibrit"]["agirlikli"] == 1475 + 2300


def test_ara_dagilimi_ve_5dk_payi(tmp_path):
    sn, satirlar = 0, [kul(0), ist("i0", 0, h1=10)]
    for i, ara in enumerate([10, 20, 30, 400, 5000], 1):
        sn += ara
        satirlar += [kul(sn), ist(f"i{i}", sn, okuma=10 * i, h1=10)]
    r = sim(tmp_path, satirlar)
    assert r["ara"]["n"] == 5
    assert (r["ara"]["p50"], r["ara"]["p90"], r["ara"]["p99"]) == (30, 5000, 5000)
    assert r["ara"]["5dk_ustu_pay"] == 0.4


def test_yalniz_etkilesimli_ana(tmp_path):
    yaz(tmp_path / "p" / "cp.jsonl", [kul(0), ist("a", 0, h1=1000, entry="sdk-cli")])
    yaz(tmp_path / "p" / "s" / "subagents" / "x.jsonl", [kul(0), ist("b", 0, h1=1000, isSidechain=True)])
    yaz(tmp_path / "p" / "e.jsonl", [kul(0), ist("c", 0, h1=1000)])
    r = t.ttl_sim(tmp_path / "p", gun=14, simdi=SIMDI)
    assert (r["oturum"], r["istek"]) == (1, 1)


def test_usd_opus55_carpanlari(tmp_path):
    # Opus 5.5 $4/MTok girdi: okuma 0.05× · 5m 1.25× · 1h 2×
    r = sim(tmp_path, [kul(0), ist("a", 0, h1=1_000_000), kul(10), ist("b", 10, okuma=1_000_000, h1=0)])
    assert abs(r["kollar"]["1h"]["usd"] - (8 + 0.2)) < 1e-9
    assert abs(r["kollar"]["5m"]["usd"] - (5 + 0.2)) < 1e-9


def test_main_ttl_sim(tmp_path, capsys):
    yaz(tmp_path / "p" / "e.jsonl", [kul(0), ist("a", 0, h1=1000), kul(10), ist("b", 10, okuma=1000, h1=10)])
    out = tmp_path / "o.json"
    assert t.main(["olc", "--ttl-sim", "--kok", str(tmp_path / "p"), "--gun", "100000", "--cikti", str(out)]) == 0
    assert "hibrit" in capsys.readouterr().out and out.is_file()
