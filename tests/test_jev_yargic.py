import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "olcum"))
import jev_yargic  # noqa: E402


class Sahte:
    def yargila(self, states, questions):
        assert set(questions) == {"kalite"} and questions["kalite"]["type"] == "score"
        return [{"kalite": {"score": 2.5, "confidence": 0.7}} for _ in states]


def test_veri_ve_puan(tmp_path):
    d = tmp_path / "2026-10-11-x"
    d.mkdir()
    (d / "G01-1.md").write_text("await _db.Orders.FirstOrDefaultAsync .Result deadlock", encoding="utf-8")
    (d / "notlar.md").write_text("görev değil", encoding="utf-8")
    k = jev_yargic.jev_puanla(jev_yargic.veri([d]), Sahte(), onbellek=tmp_path / "ob.json")
    assert [x["dosya"] for x in k] == ["2026-10-11-x/G01-1.md"]
    assert k[0]["regex"] == 8 and k[0]["jev"] == 5.0 and k[0]["guven"] == 0.7
    assert k[0]["state"]["gorev"] and k[0]["state"]["kabul"]


class Sayan:
    def __init__(self, cevap=lambda s: {"k": {"type": "noul", "noul": 0.9}}):
        self.gelen, self.cevap = [], cevap

    def yargila(self, states, questions):
        self.gelen.append(list(states))
        return [self.cevap(s) for s in states]


def test_yargila_onbellek_ikinci_kez_ucretlenmez(tmp_path):
    ob, t, soru = tmp_path / "ob.json", Sayan(), {"k": {"type": "noul", "question": "?"}}
    a = jev_yargic.yargila([{"x": 1}, {"x": 2}, {"x": 1}], soru, tasiyici=t, onbellek=ob)
    assert t.gelen == [[{"x": 1}, {"x": 2}]] and a[0] == a[2] == {"k": {"type": "noul", "noul": 0.9}}
    b = jev_yargic.yargila([{"x": 2}, {"x": 1}], soru, tasiyici=t, onbellek=ob)
    assert len(t.gelen) == 1 and b == a[1::-1]  # ikinci koşu: 0 çağrı
    jev_yargic.yargila([{"x": 1}], {"baska": soru["k"]}, tasiyici=t, onbellek=ob)
    assert t.gelen[-1] == [{"x": 1}]  # soru farklı → yeni anahtar


def test_yargila_cevapsiz_onbellege_girmez(tmp_path):
    ob, t = tmp_path / "ob.json", Sayan(lambda s: None)
    assert jev_yargic.yargila(["a"], {"k": {}}, tasiyici=t, onbellek=ob) == [None]
    jev_yargic.yargila(["a"], {"k": {}}, tasiyici=t, onbellek=ob)
    assert len(t.gelen) == 2


def test_tsv_doldur_eski_baslik_sutun_eklenir(tmp_path):
    t = tmp_path / "2026-10-11-x.tsv"
    t.write_text("gorev\ttekrar\tkalite\thata\nG01\t1\t8\t\nG02\t1\t10\t\n", encoding="utf-8")
    jev_yargic.tsv_doldur(t, [{"gorev": "G01", "tekrar": "1", "jev": 6.0, "guven": 0.9}, {"gorev": "G02", "tekrar": "1"}])
    L = t.read_text(encoding="utf-8").splitlines()
    assert L == ["gorev\ttekrar\tkalite\thata\tjev\tjev_guven", "G01\t1\t8\t\t6.0\t0.9", "G02\t1\t10\t\t\t"]
    jev_yargic.tsv_doldur(t, [{"gorev": "G02", "tekrar": "1", "jev": 9.0, "guven": 0.8}])  # ikinci kez: sütun yinelenmez
    assert t.read_text(encoding="utf-8").splitlines()[1:] == ["G01\t1\t8\t\t6.0\t0.9", "G02\t1\t10\t\t9.0\t0.8"]


class Kopuk(Sayan):
    """İlk `kac` çağrıda ağ kopuk, sonra normal."""
    def __init__(self, kac, hata=None):
        super().__init__()
        self.kac, self.hata = kac, hata

    def yargila(self, states, questions):
        from jev.cekirdek import BaglantiHata
        if self.kac:
            self.kac -= 1
            raise (self.hata or BaglantiHata)("kopuk")
        return super().yargila(states, questions)


def test_ag_kopuklugunda_duraklar_ve_ayni_parcayi_yeniden_dener(tmp_path):
    t, uyku = Kopuk(2), []
    a = jev_yargic.yargila([{"x": 1}], {"k": {}}, tasiyici=t, onbellek=tmp_path / "ob.json", ag_bekle=(1, 2, 3), uyu=uyku.append)
    assert uyku == [1, 2] and a == [{"k": {"type": "noul", "noul": 0.9}}]


def test_ag_bekleme_tukenirse_biten_parcalar_onbellekte_kalir(tmp_path):
    import pytest
    from jev.cekirdek import BaglantiHata

    class Yarida(Sayan):
        def yargila(self, states, questions):
            if self.gelen:
                raise BaglantiHata("kopuk")
            return super().yargila(states, questions)

    ob, t = tmp_path / "ob.json", Yarida()
    with pytest.raises(BaglantiHata):
        jev_yargic.yargila([{"x": 1}, {"x": 2}, {"x": 3}], {"k": {}}, tasiyici=t, onbellek=ob, parca=1, ag_bekle=(1,), uyu=lambda s: None)
    t2 = Sayan()
    jev_yargic.yargila([{"x": 1}, {"x": 2}, {"x": 3}], {"k": {}}, tasiyici=t2, onbellek=ob)
    assert t2.gelen == [[{"x": 2}, {"x": 3}]]  # 1. parça kopukluktan önce yazılmıştı: yeniden ücretlenmez


def test_saglayici_hatasi_parcayi_none_birakir_tavan_yukselir(tmp_path):
    import pytest
    from jev.cekirdek import JevHata, TavanHata
    a = jev_yargic.yargila([{"x": 1}], {"k": {}}, tasiyici=Kopuk(1, JevHata), onbellek=tmp_path / "ob.json", uyu=lambda s: None)
    assert a == [None]  # geri kuyruk: önbelleğe girmez
    with pytest.raises(TavanHata):
        jev_yargic.yargila([{"x": 9}], {"k": {}}, tasiyici=Kopuk(1, TavanHata), onbellek=tmp_path / "ob.json")


def test_onbellek_tavani_en_eskiyi_dusurur(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(jev_yargic, "OB_TAVAN", 2)
    ob = tmp_path / "ob.json"
    for i in range(3):
        jev_yargic.yargila([{"x": i}], {"k": {}}, tasiyici=Sayan(), onbellek=ob)
    assert len(json.loads(ob.read_text(encoding="utf-8"))) == 2


def test_jev_puanla_cevapsizi_puansiz_birakir(tmp_path):
    from jev.cekirdek import JevHata
    k = jev_yargic.jev_puanla([{"state": "s"}], Kopuk(1, JevHata), onbellek=tmp_path / "ob.json")
    assert "jev" not in k[0]


def test_rapor_onyargi_karar_ve_geri_kuyruk(tmp_path):
    from jev.cekirdek import JevHata

    class Puan(Sayan):
        def __init__(self):
            super().__init__(lambda s: {"kalite": {"score": 4.0 if "iyi" in s["rapor"] else 1.5, "confidence": 0.8}})

    ob = tmp_path / "ob.json"
    r = jev_yargic.rapor_onyargi(["iyi rapor", "zayıf"], tasiyici=Puan(), onbellek=ob)
    assert [x["karar"] for x in r] == ["gec", "yeniden"] and r[0]["jev"] == 8.0
    assert jev_yargic.rapor_onyargi(["yeni"], tasiyici=Kopuk(1, JevHata), onbellek=ob) == [{"jev": None, "guven": None, "karar": None}]


def test_onbellekli_tasiyici_yerine_gecer(tmp_path):
    import pytest
    from jev.cekirdek import JevHata
    t = Sayan()
    o = jev_yargic.Onbellekli(t, tmp_path / "ob.json")
    assert o.yargila([{"x": 1}], {"k": {}}) == o.yargila([{"x": 1}], {"k": {}}) and len(t.gelen) == 1
    assert o.gelen is t.gelen  # kullanim/cagri gibi öznitelikler taşıyıcıdan okunur
    with pytest.raises(JevHata):  # eski çağıranların sözleşmesi: cevapsız → JevHata (biten öğeler önbellekte)
        jev_yargic.Onbellekli(Sayan(lambda s: None), tmp_path / "ob.json").yargila([{"x": 2}], {"k": {}})


def test_belirsiz_merkeze_en_yakini_secer_puansizi_atlar():
    assert jev_yargic.belirsiz([10.0, 7.2, None, 2.0, 6.0, 9.0, 8.0, 4.0, 7.0, 5.0], oran=0.2) == [8, 1]
    assert jev_yargic.belirsiz([], oran=0.1) == []
