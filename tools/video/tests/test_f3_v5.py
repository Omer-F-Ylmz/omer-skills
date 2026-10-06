"""F3-V5: bölümleme — paket zamana göre k parçaya (sınır en yakın bölüm başında), parçalar paralel taranır, formlar mekanik
birleşir (eslesir ile tekil). Testler sahte, canlı çağrı 0."""
import json
import threading
import time

import pytest

from video import hafif
from video import parti as pt
from video import tarama as tr
from video import yonlendir as yon

E1 = "openrouter/openai/gpt-6-luna"
ENV = {"OMNIROUTE_URL": "http://x:1", "OMNIROUTE_KEY": "gizli-anahtar"}
SV = pt.sema(["vid1"])
KARELER = ["C:/c/kare_01.jpg", "C:/c/kare_02.jpg", "C:/c/kare_03.jpg"]
P = "\n".join([
    "=== VIDEO vid1 · süre 9:00 · kare görseli 3 ===",
    "# vid1 · Başlık · Kanal · süre 9:00 · sure_sn 540 · short: false · dil tr · https://youtu.be/vid1",
    "## Chapter", "0:00 Giriş", "2:50 Kurulum", "6:10 Deneme",
    "## Açıklama bağlantıları", "https://x.dev/a",
    "## Segmentler", "damgasız satır", "[0:10] Önce Alfa anlatılıyor.", "[3:00] Sonra Beta kuruluyor.", "[7:00] Sonra Gama deneniyor.",
    "## Ekran metni (OCR)", "[0:20] ALFA EKRAN", "[3:10] BETA EKRAN", "[8:00] GAMA EKRAN",
    "## Kareler", *[f"{k} · {t}" for k, t in zip(KARELER, ("0:30", "3:20", "8:30"))]])


@pytest.fixture(autouse=True)
def _kelime_kurali(monkeypatch):
    monkeypatch.setattr(yon, "ANLAMSAL", False)  # eşleşme yalnız kelime kurallarıyla (belirlenimli)


def _aday(ad):
    return {"ad": ad, "tur": sorted(tr.TUR)[0], "ne": "x", "kanit_zamani": "0:10", "kaynak": "altyazı", "kanit": "x", "repo_url": None}


def _vf(ozet, adlar, bel=(), bolumler=(), linkler=()):
    return {"videolar": [{"id": "vid1", "ozet": ozet, "bolumler": list(bolumler), "adaylar": [_aday(a) for a in adlar],
                          "aciklama_baglantilari": list(linkler), "site_ui": [], "promptlar": [], "iddialar": [],
                          "kareden_okunanlar": [], "belirsizlikler": list(bel)}]}


def test_bolumle_sinirlar_bolum_basinda():
    p3, p4 = yon.bolumle(P, 3), yon.bolumle(P, 4)
    assert [p.splitlines()[0] for p in p3] == [f"Bu çağrı videonun {a}–{b} aralığı; yalnız bu aralıktaki öğeleri yaz."
                                               for a, b in (("0:00", "2:50"), ("2:50", "6:10"), ("6:10", "9:00"))]
    assert len(p4) == 4 and p4[1].startswith("Bu çağrı videonun 2:50–6:10") and p4[3].splitlines()[0].endswith("–9:00 aralığı; yalnız bu aralıktaki öğeleri yaz.")


def test_bolumle_satirlar_dogru_parcada():
    p = yon.bolumle(P, 3)
    for i, (s, o, k) in enumerate([("Alfa", "ALFA", "kare_01"), ("Beta", "BETA", "kare_02"), ("Gama", "GAMA", "kare_03")]):
        for j, x in enumerate(p):
            assert (f"Sonra {s}" in x or f"Önce {s}" in x) == (i == j) and (f"{o} EKRAN" in x) == (i == j) and (k in x) == (i == j)
    for x in p:  # başlık + bölümler + açıklama bağlantıları hepsinde, bölüm başlıkları sırayla
        assert "=== VIDEO vid1" in x and "# vid1 · Başlık" in x and "2:50 Kurulum" in x and "https://x.dev/a" in x
        assert [s for s in x.splitlines() if s.startswith("## ")] == \
            ["## Chapter", "## Açıklama bağlantıları", "## Segmentler", "## Ekran metni (OCR)", "## Kareler"]


def test_bolumle_damgasiz_ilk_parcada():
    p = yon.bolumle(P, 3)
    assert "damgasız satır" in p[0] and not any("damgasız satır" in x for x in p[1:])


def test_bolumle_degerlendir_suzme():
    o = [yon.on_cikarim(x) for x in yon.bolumle(P, 3)]
    assert all("url: https://x.dev/a" in x for x in o)
    assert ["ad: Alfa" in x for x in o] == [True, False, False] and ["ad: Gama" in x for x in o] == [False, False, True]
    assert ["kare: [3:10] BETA EKRAN" in x for x in o] == [False, True, False]


def test_birlestir_tekrar_yok_paraphrase_dahil():
    f = yon.birlestir([_vf("bir", ["Codex GitHub", "Alfa"], ["b1"], [{"zaman": "0:00", "baslik": "G"}], [{"url": "u", "ne": "n", "aday_mi": False, "neden": "n"}]),
                       _vf("iki", ["Codex on GitHub", "Beta"], ["b1", "b2"], [{"zaman": "0:00", "baslik": "G"}], [{"url": "u", "ne": "n", "aday_mi": False, "neden": "n"}]),
                       _vf("üç", ["alfa", "Gama"])])
    v = f["videolar"]
    assert len(v) == 1 and [a["ad"] for a in v[0]["adaylar"]] == ["Codex GitHub", "Alfa", "Beta", "Gama"]
    assert v[0]["ozet"] == "bir iki üç" and v[0]["belirsizlikler"] == ["b1", "b2"]
    assert len(v[0]["bolumler"]) == 1 and len(v[0]["aciklama_baglantilari"]) == 1


def test_birlestir_sema_gecer():
    f = yon.birlestir([_vf("bir", ["A1"]), _vf("iki", ["B1"]), _vf("üç", [])])
    assert pt._denet(f, SV, "form") == []


def _b(c, yanit=None, engel=None):
    def kur(m, env, timeout=600, govde_ek=None):
        def tas(sistem, metin, sema, kareler=(), model=None, **_):
            if engel:
                engel.wait()  # sıralı çağrıda k'ya ulaşılmaz → BrokenBarrierError
            i = next((j for j, s in enumerate(("Alfa", "Beta", "Gama")) if s in metin), 3)  # 3: konuşmasız parça (V54 6:10–6:45)
            c.append({"i": i, "sistem": sistem, "metin": metin, "kareler": list(kareler)})
            return (yanit or {}).get(i) or {"form": _vf(f"o{i}", [["Alfa"], ["Beta", "alfa"], ["Gama"], []][i]), "usage": {"input_tokens": 10, "output_tokens": 5},
                                             "usd": 0.001, "sure": float(i + 1), "hata": None}
        return tas
    return kur


def _e5(tmp_path, adaylar, c, **k):
    o = tmp_path / "ORN2.json"
    o.write_text('{"id": "ORN2"}', encoding="utf-8")
    kr = [tmp_path / x.rsplit("/", 1)[1] for x in KARELER]  # A önbelleği kare dosyalarını okur
    for x in kr:
        x.write_bytes(b"k")
    return yon.eleme(("S", P, SV, kr), adaylar, lambda *a, **kw: {"form": None, "hata": "A yok", "usd": 0}, hafif.MODEL, ENV,
                     lambda ms: [0.8] * len(ms), onbellek=tmp_path / "ab", b_kur=k.pop("b_kur", None) or _b(c),
                     yokla=lambda m, env, gorsel=False: None, ornek21=o, kayit=tmp_path / "k", **k)


def _kayit(tmp_path, ad, i=0):
    return json.loads((tmp_path / "k" / ad.replace("/", "_") / f"{i}.json").read_text(encoding="utf-8"))["yanit"]


def test_v5_v54_k_parca_k_cagri(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c)
    assert len(c) == 6 and sorted(x["i"] for x in c) == [0, 0, 1, 1, 2, 2]
    for x in c:  # V21 sistemi + parçaya süzülmüş liste · yalnız aralıktaki kareler
        assert x["sistem"].startswith("S\n\n" + yon.EKSIKSIZLIK) and x["sistem"].endswith(yon.ORNEK_BASLIK + '{"id": "ORN2"}')
        assert "url: https://x.dev/a" in x["sistem"] and ("ad: Alfa" in x["sistem"]) == (x["i"] == 0)
        assert x["metin"].startswith("Bu çağrı videonun") and [k.name for k in x["kareler"]] == [KARELER[x["i"]].rsplit("/", 1)[1]]
    c4 = []
    _e5(tmp_path, [f"{E1}@V54"], c4)
    assert len(c4) == 8


def test_v5_paralel(tmp_path, monkeypatch):
    monkeypatch.setattr(yon, "PARALEL_TAVAN", 3, raising=False)  # F3-V5b: tavan 1 (OmniRoute); paralellik tavan kadar
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c, b_kur=_b(c, engel=threading.Barrier(3, timeout=5)))
    assert len(c) == 6


def test_v5_birlesik_yanit(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c)
    y = _kayit(tmp_path, f"{E1}@V5")
    v = y["form"]["videolar"][0]
    assert v["ozet"] == "o0 o1 o2" and [a["ad"] for a in v["adaylar"]] == ["Alfa", "Beta", "Gama"] and pt._denet(y["form"], SV, "form") == []
    assert y["usd"] == pytest.approx(0.003) and y["usage"] == {"input_tokens": 30, "output_tokens": 15} and y["sure"] < 1 and y["hata"] is None  # F3-V5b: duvar saati (parça sure toplamı/maksimumu değil)


def test_v5_tavan_parca_basina(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V5"], c, tavan_cagri=5)  # 3 + 3 > 5 → ikinci yanıt yok
    assert len(c) == 3 and s["b_usd"] == pytest.approx(0.003)
    c = []
    s = _e5(tmp_path, [f"{E1}@V5"], c, tavan_usd=yon._tahmin(E1, 3) * 2)  # ön tahmin = _tahmin × 3
    assert c == [] and s["satirlar"][0].endswith(" · hata: tavan · çağrı 0")


def test_v5_parca_hatasi(tmp_path):
    c = []
    _e5(tmp_path, [f"{E1}@V5"], c, b_kur=_b(c, {1: {"form": None, "usage": {}, "usd": 0.001, "sure": 1.0, "hata": "boom"}}))
    y = _kayit(tmp_path, f"{E1}@V5")
    assert len(c) == 3 and y["hata"] == "parça 2: boom" and y["form"] is None


def test_v5_bilinmeyen_varyant_cagri_0(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V55"], c)
    assert c == [] and s["satirlar"] == [f"{E1}@V55 · hata: bilinmeyen varyant: V55 · çağrı 0"]


# F3-V5b: OmniRoute kabul sınırı (chatBodyAdmission.ts — 503 chat_admission_busy, Retry-After 2)
OK = (200, {"choices": [{"message": {"content": '{"a": 1}'}}], "usage": {"prompt_tokens": 10, "completion_tokens": 5}}, {})
KABUL = (503, {"error": {"message": "Chat admission capacity is temporarily unavailable. Retry shortly.", "code": "chat_admission_busy"}}, {})


def _omni(yanitlar):
    it, u = iter(yanitlar), []
    return yon.omni_cagir(E1, ENV, gonder=lambda url, govde, bas: next(it), uyku=u.append)("s", "t", {}), u


def test_omni_503_kabul_yeniden_basari():
    r, u = _omni([KABUL, OK])
    assert r["hata"] is None and r["yeniden"] == 1 and len(u) == 1 and 2 <= u[0] <= 2.5
    assert r["usd"] == _omni([OK])[0]["usd"]  # usd yalnız başarılı yanıttan


def test_omni_3_yeniden_sonra_hata():
    r, u = _omni([KABUL] * 4)
    assert r["hata"].startswith("ölçülemedi: HTTP 503") and r["yeniden"] == 3 and r["usd"] == 0.0
    assert [int(x) for x in u] == [2, 4, 8] and all(x - int(x) <= 0.5 for x in u)


def test_omni_retry_after_uyulur():
    r, u = _omni([(503, {}, {"retry-after": "7"}), (429, {}, {"Retry-After": "60"}), OK])
    assert r["hata"] is None and r["yeniden"] == 2 and u == [7.0, 15]


def test_omni_diger_hata_yeniden_yok():
    for y in [(400, {"error": {"message": "Retry later"}}, {}), (503, {"error": {"message": "upstream down"}}, {})]:
        r, u = _omni([y, OK])
        assert r["hata"].startswith(f"ölçülemedi: HTTP {y[0]}") and r["yeniden"] == 0 and u == []


def test_post_hata_dali_basliklar(monkeypatch):
    import email.message
    import io
    import urllib.error
    from video import ikinci_goz as ig
    h = email.message.Message()
    h["Retry-After"] = "2"

    def ac(*a, **k):
        raise urllib.error.HTTPError("http://x", 503, "busy", h, io.BytesIO(b'{"error": {}}'))
    monkeypatch.setattr(ig.urllib.request, "urlopen", ac)
    assert ig._post("http://x", {}, {}, basliklar=True) == (503, {"error": {}}, {"Retry-After": "2"})
    assert ig._post("http://x", {}, {}) == (503, {"error": {}})


def test_v5_es_zaman_tavan(tmp_path):
    c, an, en, kilit = [], [0], [0], threading.Lock()
    ic = _b(c)

    def kur(m, env, timeout=600, govde_ek=None):
        t = ic(m, env)

        def tas(*a, **k):
            with kilit:
                an[0] += 1
                en[0] = max(en[0], an[0])
            time.sleep(0.05)
            try:
                return t(*a, **k)
            finally:
                with kilit:
                    an[0] -= 1
        return tas
    _e5(tmp_path, [f"{E1}@V5"], c, b_kur=kur)
    assert yon.PARALEL_TAVAN == 1  # OMNIROUTE_CHAT_MAX_HEAVY_IN_FLIGHT varsayılanı
    assert len(c) == 6 and en[0] <= yon.PARALEL_TAVAN
    assert _kayit(tmp_path, f"{E1}@V5")["sure"] < 1  # duvar saati, parça sure'lerinin en büyüğü (3.0) değil


def test_v5_yeniden_satirda(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V5"], c, b_kur=_b(c, {1: {"form": None, "usage": {}, "usd": 0.0, "sure": 1.0, "hata": "ölçülemedi: HTTP 503", "yeniden": 3}}))
    assert _kayit(tmp_path, f"{E1}@V5")["yeniden"] == 3
    assert any(x.startswith(f"{E1}@V5 ") and " · yeniden 3" in x for x in s["satirlar"])


def test_tek_cagri_etkilenmez(tmp_path):
    c = []
    s = _e5(tmp_path, [f"{E1}@V21"], c)
    assert c and not any(x["metin"].startswith("Bu çağrı videonun") for x in c) and not any(" · yeniden " in x for x in s["satirlar"])


# F3-V6: tam örnek · mekanik bölümler · sabit sistem öneki · yük dengesi · son geçiş
def _form6(tmp_path, ad, dolu):
    (tmp_path / f"{ad}.json").write_text(json.dumps({**{x: ([{"x": 1}] if x in dolu else []) for x in yon.OLCUM}, "ozet": "o" * len(ad)}), encoding="utf-8")
    return tmp_path / f"{ad}.json"


def test_ornek_sec6_alti_liste(tmp_path):
    h = list(yon.OLCUM)
    ys = [_form6(tmp_path, "uzunuzun", h), _form6(tmp_path, "kisa", h), _form6(tmp_path, "k", h[:4]), _form6(tmp_path, "b2QkhmQ0sT0", h)]
    assert yon.ornek_sec6(ys) == (ys[1], [])


def test_ornek_sec6_eksik_rapor(tmp_path):
    h = list(yon.OLCUM)
    ys = [_form6(tmp_path, "dort", h[:4]), _form6(tmp_path, "bes", [x for x in h if x != "site_ui"])]
    assert yon.ornek_sec6(ys) == (ys[1], ["site_ui"])


P2 = "\n".join(["=== VIDEO vid1 · süre 9:00 · kare görseli 4 ===", "# vid1 · B · K · süre 9:00 · sure_sn 540 · short: false · dil tr · https://youtu.be/vid1",
                "## Chapter", *[f"{i}:00 Bölüm {i}" for i in range(9)], "## Segmentler", "[5:00] Alfa.", "[7:00] Gama.",
                "## Kareler", *[f"C:/c/kare_0{i}.jpg · {i - 1}:30" for i in range(1, 5)]])
P3 = "\n".join(["=== VIDEO vid1 · süre 4:00 · kare görseli 1 ===", "# vid1 · B · K · süre 4:00 · sure_sn 240 · short: false · dil tr · https://youtu.be/vid1",
                "## Chapter", "0:00 A", "1:00 B", "2:00 C", "3:00 D", "## Segmentler", "[0:40] Önce Alfa.", "[3:30] Sonra Gama.",
                "## Kareler", "C:/c/kare_01.jpg · 0:30"])


def test_bolumle_yuk_dengesi():
    assert yon.bolumle(P2, 2)[1].startswith("Bu çağrı videonun 4:00–9:00")  # süreye göre (V5/V54 değişmez)
    p = yon.bolumle(P2, 2, yuk=True)  # yük = metin/4 + kare × 1000 → 2 kare | 2 kare
    assert p[1].startswith("Bu çağrı videonun 2:00–9:00") and p[0].count("kare_0") == 2


def test_bolumle_bos_parca_k_duser():
    assert [x.splitlines()[0] for x in yon.bolumle(P3, 3, yuk=True)] == \
        [f"Bu çağrı videonun {a}–{b} aralığı; yalnız bu aralıktaki öğeleri yaz." for a, b in (("0:00", "1:00"), ("1:00", "4:00"))]


SON_OK = {"ozet": "bütün özet", "belirsizlikler": ["s1"], "ek_adaylar": [_aday("Delta"), _aday("alfa")], "ek_iddialar": [],
          "ek_kurulum_komutlar": [], "ek_promptlar": [], "ek_site_ui": []}


def _b6(c, son=None):
    ic = _b(c)

    def kur(m, env, timeout=600, govde_ek=None):
        t = ic(m, env)

        def tas(sistem, metin, sema, kareler=(), model=None, **_):
            if sistem in (yon.SON_SISTEM, getattr(yon, "SON_SISTEM10", None)):
                c.append({"i": "son", "sistem": sistem, "metin": metin, "kareler": list(kareler), "sema": sema})
                return son or {"form": SON_OK, "usage": {"input_tokens": 7, "output_tokens": 3}, "usd": 0.001, "sure": 1.0, "hata": None}
            return t(sistem, metin, sema, kareler, model=model)
        return tas
    return kur


def _e6(tmp_path, adaylar, c, paket=P, **k):
    o = tmp_path / "ORN6.json"
    o.write_text('{"id": "ORN6"}', encoding="utf-8")
    kr = [tmp_path / x.rsplit("/", 1)[1] for x in KARELER]
    for x in kr:
        x.write_bytes(b"k")
    return yon.eleme(("S", paket, SV, kr), adaylar, lambda *a, **kw: {"form": None, "hata": "A yok", "usd": 0}, hafif.MODEL, ENV,
                     lambda ms: [0.8] * len(ms), onbellek=tmp_path / "ab", b_kur=k.pop("b_kur", None) or _b6(c),
                     yokla=lambda m, env, gorsel=False: None, ornek6=o, kayit=tmp_path / "k", **k)


def test_v6_parca_talimatlari_sistem_ozdes(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V63"], c)
    p = [x for x in c if x["i"] != "son"]
    assert len(p) == 6 and len({x["sistem"] for x in p}) == 1
    assert p[0]["sistem"] == "S\n\n" + yon.EKSIKSIZLIK + yon.ORNEK_BASLIK + '{"id": "ORN6"}'
    for x in p:  # parçaya özel her şey kullanıcı mesajının başında; bolumler hepsinde boş, linkler yalnız 1. parçada
        assert x["metin"].startswith(yon.PARCA_BOLUM) and (yon.PARCA_LINK in x["metin"]) == ("Bu çağrı videonun 0:00" not in x["metin"])
        assert "DEĞERLENDİR LİSTESİ" in x["metin"] and ("ad: Alfa" in x["metin"]) == (x["i"] == 0) and "Bu çağrı videonun" in x["metin"]


def test_v6_son_gecis_basari(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c)
    y = _kayit(tmp_path, f"{E1}@V63")
    v = y["form"]["videolar"][0]
    assert v["bolumler"] == [{"zaman": "0:00", "baslik": "Giriş"}, {"zaman": "2:50", "baslik": "Kurulum"}, {"zaman": "6:10", "baslik": "Deneme"}]
    assert v["ozet"] == "bütün özet" and [a["ad"] for a in v["adaylar"]] == ["Alfa", "Beta", "Gama", "Delta"] and "s1" in v["belirsizlikler"]
    assert pt._denet(y["form"], SV, "form") == []
    son = [x for x in c if x["i"] == "son"]
    assert len(son) == 2 and son[0]["kareler"] == [] and "- adaylar: Alfa" in son[0]["metin"] and "ALFA EKRAN" in son[0]["metin"]
    assert "kare_01" not in son[0]["metin"] and set(son[0]["sema"]["properties"]) == set(SON_OK)
    assert y["usd"] == pytest.approx(0.004) and y["usage"]["input_tokens"] == 37 and "son geçiş" not in s["satirlar"][0]


def test_v6_son_gecis_hata(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b6(c, {"form": None, "usage": {}, "usd": 0.001, "sure": 1.0, "hata": "boom"}))
    y = _kayit(tmp_path, f"{E1}@V63")
    v = y["form"]["videolar"][0]
    assert y["hata"] is None and v["ozet"] == "o0 o1 o2" and [a["ad"] for a in v["adaylar"]] == ["Alfa", "Beta", "Gama"] and len(v["bolumler"]) == 3
    assert y["usd"] == pytest.approx(0.004) and " · son geçiş: hata" in s["satirlar"][0]


def test_v6_tavan_son_gecis_sayilir(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V63"], c, tavan_cagri=7)  # (3 + 1) + 4 > 7 → ikinci yanıt yok
    assert len(c) == 4
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, tavan_cagri=3)
    assert c == [] and s["satirlar"][0].endswith(" · hata: tavan · çağrı 0")


def test_v6_bos_parca_satirda_k(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, paket=P3)
    assert len([x for x in c if x["i"] != "son"]) == 4 and " · k 3→2" in s["satirlar"][0]


# F3-V7a: önbellek-duyarlı maliyet · cümle dayanağı kalibrasyonu (DAYANAK_ESIK)
import pytest  # noqa: E402


def test_v7a_usd_onbellek_indirimli():
    m = "openrouter/google/gemini-3.5-flash-lite"
    assert yon.FIYAT[m]["onbellek"] == 0.03 and yon.FIYAT["openrouter/google/gemini-3.8-flash"]["onbellek"] == 0.075
    u = {"prompt_tokens": 1000, "completion_tokens": 100, "prompt_tokens_details": {"cached_tokens": 600}}
    assert yon._usd(m, u, {}) == pytest.approx((400 * 0.3 + 600 * 0.03 + 100 * 2.5) / 1e6)
    assert yon._usd(m, {"prompt_tokens": 1000, "completion_tokens": 100}, {}) == pytest.approx((1000 * 0.3 + 100 * 2.5) / 1e6)


def test_v7a_omni_usage_cached_tasinir():
    r, _ = _omni([(200, {**OK[1], "usage": {"prompt_tokens": 10, "completion_tokens": 5, "prompt_tokens_details": {"cached_tokens": 4}}}, {})])
    assert r["usage"]["cached"] == 4
    assert "cached" not in _omni([OK])[0]["usage"]  # sağlayıcı bildirmediyse bilinmiyor, 0 yazılmaz


def test_v7a_onbellek_orani_satirda(tmp_path):
    c, r = [], {"form": None, "usage": {"input_tokens": 1000, "output_tokens": 10, "cached": 250}, "usd": 0.001, "sure": 1.0, "hata": None}
    s = _e5(tmp_path, [f"{E1}@V21"], c, b_kur=_b(c, {0: r, 1: r}))
    assert any(" · önbellek %25" in x for x in s["satirlar"])


# Elle etiketli: Türkçe iddia ↔ İngilizce konuşma penceresi (b2QkhmQ0sT0); ilk ikisi O68 "dayanaksız" sayılan doğru iddialar
_IDDIA = ["İnceleme derinliği değişikliğin blast radius'una göre ayarlanmalı.",
          "Leaf kodlar izole olduğu ve feature gate ile korunduğu için daha hafif incelenebilir.",
          "Kodu yazan ajan kendi bağlamıyla 'hile yapar'; inceleme için bağlamsız ayrı ajan kullanılmalı.",
          "Codex incelemesi iki hata buldu: yinelenen oylar skoru şişirebilir, iptal edilmeyen zamanlayıcı sonraki kartı yeniden yükleyebilir.",
          "Son %20'lik kısım ilk %80 kadar sürer ama en önemlisidir.",
          "Stil nit'leri artık kod incelemesinin konusu olmamalı.",
          "Merge'e hazır olmak yayına hazır olmak anlamına gelmez.",
          "PR üzerindeki kanıtlar okunması gereken kod miktarını azaltır.",
          "Tek bir mühendisin ürettiği kodun hepsini incelemesi neredeyse imkansız hale geldi.",
          "Codex'in inceleme için özel eğitilmiş ayrı bir modeli olduğu düşünülüyor."]
_PENCERE = ["3:47 Codebase trees and blast radius. If you change infrastructure that touches all the different image renderings, and there's a "
            "lot of downstream dependencies, then I would spend a lot of time reading that piece of code.",
            "And then for any like one off leaf node code, you could probably just have agents do simple validations like component testing or "
            "snapshot testing. You wanna feature gate and run experiments on your code.",
            "You know, all the context that you gave it, will cheat. And they will really try to anchor on like a lot of the previous "
            "conversation. So you really want a fresh agent to review it.",
            "It found two issues I missed. Duplicate votes could inflate the score. An uncancelled timer could reload the next card.",
            "And then I'm really like detailing the animations or anything like that. And so this last 20% actually takes as long as the "
            "first 80%, but it's actually the most important part.",
            "I think the old days of like having your nits, oh, the code should look this way, are over. I think these kinds of nits don't "
            "really belong in the conversation of code reviews anymore.",
            "Review loop. Merge-ready does not mean launch-ready.",
            "So having proof lets you move faster because you don't have to manually check these proofs. If you have a lot of these proofs "
            "upfront on the PR, then you don't have to read as much code.",
            "They're just doing a lot more because one person can split up multiple agents and generate a ton of code. And to be honest, "
            "it's almost impossible to review all of it.",
            "And essentially it's this chat to be the Codex connector. And I think there's a separate model slightly that is custom trained "
            "just for like reviewing code."]
_ILGISIZ = [(0, 3), (1, 4), (2, 6), (3, 5), (4, 9), (5, 8), (6, 2), (7, 3), (8, 6), (9, 4)]


@pytest.fixture
def anlam7(monkeypatch):
    monkeypatch.setattr(yon, "ANLAMSAL", True)
    assert yon._acik(), "anlamsal: kapalı (embedding yüklenemedi)"


def test_v7a_dayanak_esik_sabit():
    assert yon.DAYANAK_ESIK == 0.37 and yon.ANLAM_ESIK == 0.6 and yon.DAYANAK_LISTE == ("iddialar", "site_ui", "promptlar")


@pytest.mark.parametrize("i", range(10))
def test_v7a_kalibrasyon_ayni(anlam7, i):
    assert yon._benzerlik(_IDDIA[i], _PENCERE[i]) >= yon.DAYANAK_ESIK
    assert yon.dayanak("iddialar", {"iddia": _IDDIA[i], "kaynak": "altyazı"}, _PENCERE[i]) == "dayanaklı"


@pytest.mark.parametrize("i,j", _ILGISIZ)
def test_v7a_kalibrasyon_farkli(anlam7, i, j):
    assert yon._benzerlik(_IDDIA[i], _PENCERE[j]) < yon.DAYANAK_ESIK
    assert yon.dayanak("iddialar", {"iddia": _IDDIA[i], "kaynak": "altyazı"}, _PENCERE[j]) == "dayanaksız"


def test_v7a_kisa_ad_anlam_esikte(anlam7, monkeypatch):
    monkeypatch.setattr(yon, "DAYANAK_ESIK", -1.0)  # cümle eşiği ne olursa olsun kısa ad ANLAM_ESIK'te kalır
    m = "Today we deploy with Docker Compose."
    assert yon.dayanak("adaylar", {"ad": "Stripe ödeme"}, m) == "dayanaksız"
    assert yon.dayanak("iddialar", {"iddia": "Stripe ödeme", "kaynak": "altyazı"}, m) == "dayanaklı"


# F3-V8: kararlılık (temperature/seed · B ve görev bandı) · ALAN KURALI + tek cümle parça özeti · dolu alan · boyutlu hakem
from video import kur  # noqa: E402

A8 = {"form": _vf("a", ["Alfa", "Beta"]), "usage": {"input_tokens": 10, "output_tokens": 5}, "usd": 0.001, "sure": 1.0, "hata": None}
BY = {"eksiksizlik", "kanit", "tutarlilik", "dogruluk", "ozet"}
ALAN = ("ALAN KURALI: Her öğede şemadaki alanları doldur: karede görülen öğede karede_gorulen'e karede ne göründüğünü yaz; kanit_zamani "
        "ve kaynak boş kalmaz; kanıt en az bir somut cümle; iz öğelerinde baglandigi neye ve neden bağlandığını açıklar; site_ui öğelerinde "
        "teknik uygulama ayrıntısını verir. Bilgi yoksa uydurma, 'bilinmiyor' yaz.")


def _b8(c, ge):
    ic = _b6(c)

    def kur_(m, env, timeout=600, govde_ek=None):
        ge.append(govde_ek)
        return ic(m, env)
    return kur_


def _e8(tmp_path, adaylar, c, ge=None, puanla=None, **k):
    tmp_path.mkdir(parents=True, exist_ok=True)
    o = tmp_path / "ORN6.json"
    o.write_text('{"id": "ORN6"}', encoding="utf-8")
    kr = [tmp_path / x.rsplit("/", 1)[1] for x in KARELER]
    for x in kr:
        x.write_bytes(b"k")
    return yon.eleme(("S", P, SV, kr), adaylar, lambda *a, **kw: dict(A8), hafif.MODEL, ENV,
                     puanla or (lambda ms: [0.8] * len(ms)), onbellek=tmp_path / "ab", b_kur=_b8(c, [] if ge is None else ge),
                     yokla=lambda m, env, gorsel=False: None, ornek6=o, kayit=tmp_path / "k", **k)


def _by(bc):
    def f(ms):
        bc.append(len(ms))
        return [{k: (0.9 if i < 2 else 0.5) if k in ("kanit", "ozet") else 0.8 for k in sorted(BY)} for i in range(len(ms))]
    return f


def test_v8_govde_temperature_seed(tmp_path):
    ge = []
    s = _e8(tmp_path, [f"{E1}@V8"], [], ge, destek={E1: ["seed", "temperature"]})
    assert ge == [{"temperature": 0.2, "seed": 7}] and "seed yok" not in s["satirlar"][0]


def test_v8_seed_desteksiz_yok(tmp_path):
    ge = []
    s = _e8(tmp_path, [f"{E1}@V8"], [], ge, destek={E1: ["temperature", "reasoning"]})
    assert ge == [{"reasoning": {"effort": "minimal"}, "temperature": 0.2}] and " · seed yok" in s["satirlar"][0]


def test_v8_diger_varyant_govde_degismez(tmp_path):
    ge = []
    _e8(tmp_path, [f"{E1}@V6", f"{E1}@V63"], [], ge, destek={E1: ["seed", "reasoning"]})
    assert ge == [{"reasoning": {"effort": "minimal"}}] * 2


def test_v8_bant_satirlari(tmp_path):
    s = _e8(tmp_path, [f"{E1}@V8"], [], puanla=lambda ms: [0.7, 0.9, 0.6, 0.75][:len(ms)])
    r = s["satirlar"][0]
    assert " · B bant 0.15 · görev bant (A 0.00 · B 0.00)" in r and "bant 0.20" in r  # A bandı kur.karar satırında


def test_v8_alan_kurali_tek_cumle_yalniz_v8_parcalarinda(tmp_path):
    c8, c6 = [], []
    _e8(tmp_path / "8", [f"{E1}@V8"], c8)
    _e8(tmp_path / "6", [f"{E1}@V6"], c6)
    assert yon.ALAN_KURALI == ALAN and "ozet: tek cümle" in yon.PARCA_OZET
    p8, p6 = [x for x in c8 if x["i"] != "son"], [x for x in c6 if x["i"] != "son"]
    assert p8 and all(yon.ALAN_KURALI in x["metin"] and yon.PARCA_OZET in x["metin"] for x in p8)
    assert p6 and not any(yon.ALAN_KURALI in x["metin"] or yon.PARCA_OZET in x["metin"] for x in p6)
    assert [x for x in c8 if x["i"] == "son"] and all(yon.ALAN_KURALI not in x["metin"] for x in c8 if x["i"] == "son")
    assert {x["sistem"] for x in p8} == {x["sistem"] for x in p6}  # sabit sistem öneki V6 ile aynı


def test_v8_dolu_alan_bilinmiyor_ayri():
    ks = list(SV["properties"]["videolar"]["items"]["properties"]["adaylar"]["items"]["properties"])
    o = {a: "x" for a in ks}
    o[ks[0]], o[ks[1]] = "bilinmiyor", ""
    f = _vf("o", [])
    f["videolar"][0]["adaylar"] = [o, {a: v for a, v in o.items() if a != ks[2]}]  # eksik alan boş sayılır
    f["videolar"][0]["bolumler"] = [{"zaman": "0:00", "baslik": "x"}]  # paketten gelen liste sayılmaz
    assert yon.dolu_alan([f], SV) == (2 * len(ks) - 5, 2, 2 * len(ks))


def test_v8_dolu_alan_satir_rapor(tmp_path):
    s = _e8(tmp_path, [f"{E1}@V8"], [])
    assert " · dolu alan %75 (A %75) · bilinmiyor %0 (A %0)" in s["satirlar"][0]
    assert "dolu alan %75 (A %75) · bilinmiyor %0 (A %0)" == s["rapor"][f"{E1}@V8"]["dolu"]


def test_v8_bilinmeyen_varyant_cagri_0(tmp_path):
    c = []
    s = _e8(tmp_path, [f"{E1}@V8", f"{E1}@V12"], c)
    assert s["satirlar"][1] == f"{E1}@V12 · hata: bilinmeyen varyant: V12 · çağrı 0"
    assert yon.PARCA["V8"] == 4 and "V8" in yon.SON and "V8" in yon.VARYANT and c


def test_boyut_sorulari_olcek_ayni():
    assert set(kur.BOYUT_Q) == BY and all(q["type"] == "score" and q["criteria"] == kur.KALITE_Q["criteria"] for q in kur.BOYUT_Q.values())


def test_boyut_yalniz_modda_rapor(tmp_path):
    bc = []
    s = _e8(tmp_path / "0", [f"{E1}@V8"], [])
    assert "boyut" not in s["rapor"][f"{E1}@V8"] and "boyut fark" not in s["satirlar"][0]
    s = _e8(tmp_path / "b", [f"{E1}@V8"], [], boyut=_by(bc))
    r = s["rapor"][f"{E1}@V8"]
    assert bc == [4] and r["boyut"]["A"]["kanit"] == 0.9 and r["boyut"]["B"]["kanit"] == 0.5 and r["boyut"]["B"]["dogruluk"] == 0.8
    assert " · boyut fark: kanit 0.90→0.50, ozet 0.90→0.50" in s["satirlar"][0] and r["boyut"]["satir"].startswith("boyut A/B:")


def test_boyut_tavan_on_kontrol(tmp_path, monkeypatch):
    assert yon.JEV_BOYUT_TAVAN == 24
    c, bc = [], []
    monkeypatch.setattr(yon, "JEV_BOYUT_TAVAN", 7)
    s = _e8(tmp_path / "a", [f"{E1}@V8"], c, boyut=_by(bc))
    assert c == [] and bc == [] and s["satirlar"] == [f"{E1}@V8 · hata: TAVAN jev · çağrı 0"] and s["jev_istek"] == 8
    monkeypatch.setattr(yon, "JEV_BOYUT_TAVAN", 8)
    assert _e8(tmp_path / "b", [f"{E1}@V8"], c, boyut=_by(bc))["jev_istek"] == 8 and bc == [4]


def test_boyut_kayittan_yalniz_eksikler(tmp_path):
    c, bc, kp = [], [], []
    _e8(tmp_path, [f"{E1}@V8"], c)  # kayıt boyutsuz
    n = len(c)
    pl = lambda ms: kp.append(len(ms)) or [0.8] * len(ms)  # noqa: E731
    s = _e8(tmp_path, [f"{E1}@V8"], c, puanla=pl, boyut=_by(bc), yeniden=tmp_path / "k")
    assert len(c) == n and kp == [] and bc == [4] and s["jev_istek"] == 4
    k = json.loads((tmp_path / "k" / f"{E1}@V8".replace("/", "_") / "0.json").read_text(encoding="utf-8"))
    assert k["boyut"]["kanit"] == 0.5 and json.loads((tmp_path / "k" / "A" / "1.json").read_text(encoding="utf-8"))["boyut"]["kanit"] == 0.9
    s = _e8(tmp_path, [f"{E1}@V8"], c, puanla=pl, boyut=_by(bc), yeniden=tmp_path / "k")
    assert bc == [4] and kp == [] and s["jev_istek"] == 0 and len(c) == n


# F3-V9: zengin örnek · son geçiş yeniden deneme · JPEG + koşullu paralellik · V9
def _form9(tmp_path, ad, deger, bos=0, dolu=tuple(yon.OLCUM), pad=0):
    s = SV["properties"]["videolar"]["items"]["properties"]
    ks = lambda x: list(((s.get(x) or {}).get("items") or {}).get("properties") or ()) or ["v"]  # noqa: E731
    f = {x: ([{k: ("" if i < bos else deger) for i, k in enumerate(ks(x))}] if x in dolu else []) for x in yon.OLCUM}
    (tmp_path / f"{ad}.json").write_text(json.dumps({**f, "pad": "p" * pad}), encoding="utf-8")
    return tmp_path / f"{ad}.json"


def test_v9_ornek_sec9_zengin_ve_haric(tmp_path):
    h = list(yon.OLCUM)
    ys = [_form9(tmp_path, "a", "xx"), _form9(tmp_path, "b", "xxxxx"), _form9(tmp_path, "c", "y" * 50, bos=1),
          _form9(tmp_path, "d", "z" * 9, pad=13000), _form9(tmp_path, "b2QkhmQ0sT0", "w" * 9),
          _form9(tmp_path, "f", "u" * 9, dolu=h[:5]), _form9(tmp_path, "HARIC1", "q" * 8)]
    assert yon.ornek_sec9(ys, SV, haric=("b2QkhmQ0sT0", "HARIC1")) == ys[1]  # oran eşit → uzun alan; az dolu, > 12 KB, eksik liste elenir
    assert yon.ornek_sec9(ys[4:5], SV) is None and yon.ornek_sec9(ys[6:], SV) == ys[6]
    assert yon.ornek_olc(json.loads(ys[1].read_text(encoding="utf-8")), SV) == (1.0, 5.0)


J = {"form": None, "usage": {}, "usd": 0.001, "sure": 1.0, "hata": None}


def _b9(c, sonlar):
    ic = _b6(c)

    def kur_(m, env, timeout=600, govde_ek=None):
        t = ic(m, env)

        def tas(sistem, metin, sema, kareler=(), model=None, **_):
            r = t(sistem, metin, sema, kareler, model=model)
            return sonlar.pop(0) if sistem == yon.SON_SISTEM and sonlar else r
        return tas
    return kur_


def test_v9_son_gecis_json_yeniden_basari(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b9(c, [dict(J)]))
    y = _kayit(tmp_path, f"{E1}@V63")
    assert y["form"]["videolar"][0]["ozet"] == "bütün özet" and "son_hata" not in y and y["son_yeniden"] == 1
    assert y["usd"] == pytest.approx(0.005) and len([x for x in c if x["i"] == "son"]) == 3 and "son geçiş" not in s["satirlar"][0]


def test_v9_son_gecis_ikinci_hata_mekanik(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b9(c, [dict(J), {**J, "form": {"ozet": 5}}]))
    y = _kayit(tmp_path, f"{E1}@V63")
    assert y["form"]["videolar"][0]["ozet"] == "o0 o1 o2" and y["son_hata"].startswith("şema") and len(y["son_hata"]) <= 200
    assert y["usd"] == pytest.approx(0.005) and " · son geçiş: hata (şema" in s["satirlar"][0]


def test_v9_son_gecis_json_ikinci_hata_neden(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b9(c, [dict(J), dict(J)]))
    assert _kayit(tmp_path, f"{E1}@V63")["son_hata"] == "JSON" and " · son geçiş: hata (JSON)" in s["satirlar"][0]


def test_v9_son_gecis_http_hata_yeniden_yok(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b9(c, [{**J, "hata": "ölçülemedi: HTTP 500"}] * 2))
    y = _kayit(tmp_path, f"{E1}@V63")
    assert y["son_hata"] == "ölçülemedi: HTTP 500" and y["usd"] == pytest.approx(0.004) and "son_yeniden" not in y
    assert " · son geçiş: hata (ölçülemedi: HTTP 500)" in s["satirlar"][0]


def test_v9_son_yeniden_tavana_sayilir(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V63"], c, b_kur=_b9(c, [dict(J)]), tavan_cagri=8)  # (3 + 1 + 1) + 4 > 8 → ikinci yanıt yok
    assert len([x for x in c if x["i"] != "son"]) == 3


def test_v9_jpeg_boyut_ayni_bayt_azalir(tmp_path):
    import random
    from PIL import Image
    random.seed(1)
    k = tmp_path / "kare_01.png"
    Image.frombytes("RGB", (160, 90), bytes(random.randrange(256) for _ in range(160 * 90 * 3))).save(k)
    once = k.read_bytes()
    (j,) = yon._jpeg([k], tmp_path / "j")
    with Image.open(j) as i:
        assert i.format == "JPEG" and i.size == (160, 90)
    assert j.suffix == ".jpg" and j.stat().st_size < len(once) and k.read_bytes() == once
    assert yon.govde_bayt("s", "m", {}, [j]) < yon.govde_bayt("s", "m", {}, [k]) and yon.govde_bayt("s", "m", {}, [k]) > 4 * len(once) // 3


def _e9(tmp_path, adaylar, c, ge=None, **k):
    tmp_path.mkdir(parents=True, exist_ok=True)
    o = tmp_path / "ORN9.json"
    o.write_text('{"id": "ORN9"}', encoding="utf-8")
    return _e8(tmp_path, adaylar, c, ge, ornek9=o, **k)


def test_v9_tanim_ornek_jpeg_govde(tmp_path, monkeypatch):
    jc, ge, c = [], [], []
    monkeypatch.setattr(yon, "_jpeg", lambda ks, d: jc.append(list(ks)) or list(ks))
    s = _e9(tmp_path / "9", [f"{E1}@V9"], c, ge, destek={E1: ["seed"]})
    assert yon.PARCA["V9"] == 4 and "V9" in yon.SON and "V9" in yon.VARYANT and ge == [{"temperature": 0.2, "seed": 7}]
    p = [x for x in c if x["i"] != "son"]
    assert p and all(x["sistem"].endswith('{"id": "ORN9"}') and yon.ALAN_KURALI in x["metin"] for x in p) and jc
    assert " · hata" not in s["satirlar"][0]
    jc.clear()
    _e9(tmp_path / "8", [f"{E1}@V8"], [])
    assert jc == []  # V8 kareleri değişmez
    s = _e8(tmp_path / "y", [f"{E1}@V9"], [])
    assert s["satirlar"][0] == f"{E1}@V9 · hata: V9 örneği yok · çağrı 0"


def test_v9_paralel_ya_da_sirali(tmp_path, monkeypatch):
    import concurrent.futures as cf
    en, gercek = [], cf.ThreadPoolExecutor
    monkeypatch.setattr(cf, "ThreadPoolExecutor", lambda n: en.append(n) or gercek(n))
    monkeypatch.setattr(yon, "_jpeg", lambda ks, d: list(ks))
    assert yon.BUYUK_GOVDE == 262144  # OmniRoute OMNIROUTE_CHAT_LARGE_BODY_BYTES varsayılanı
    s = _e9(tmp_path / "a", [f"{E1}@V9"], [])
    assert en[0] > 1 and f" · paralel {en[0]}" in s["satirlar"][0]
    en.clear()
    monkeypatch.setattr(yon, "BUYUK_GOVDE", 100)
    s = _e9(tmp_path / "b", [f"{E1}@V9"], [])
    assert set(en) == {1} and " · sıralı (gövde " in s["satirlar"][0] and " KB > 0 KB)" in s["satirlar"][0]
    en.clear()
    s = _e9(tmp_path / "c", [f"{E1}@V8"], [])
    assert set(en) == {1} and "paralel" not in s["satirlar"][0] and "sıralı" not in s["satirlar"][0]


# F3-V10: uyarlanır k · bölümsüz pakette bölüm üretimi · EKSIKSIZLIK10 + SON_SISTEM10
PB = P.replace("## Chapter\n0:00 Giriş\n2:50 Kurulum\n6:10 Deneme\n", "")
BOL = [{"zaman": "0:00", "baslik": "Açılış"}, {"zaman": "3:00", "baslik": "Kurulum"}]
SON_B = {"form": {**SON_OK, "bolumler": BOL}, "usage": {"input_tokens": 7, "output_tokens": 3}, "usd": 0.001, "sure": 1.0, "hata": None}
SON_HATA = {"form": None, "usage": {}, "usd": 0.001, "sure": 1.0, "hata": "boom"}


def _kp(n):  # n zamanlı kare satırlı paket (yük ≈ n × 1000)
    return "\n".join(["# v · sure_sn 600", "## Segmentler", "[0:01] a", "## Kareler",
                      *[f"C:/c/k{i:03}.jpg · {i // 60}:{i % 60:02}" for i in range(n)]])


def test_v10_yuk_bolumle_ile_ayni():
    assert 3000 < yon.yuk(P) < 3100 and yon.yuk("# başlık yok") == 0


def test_v10_parca_k_yukten():
    py = yon.PARCA_YUK
    assert yon.parca_k(P3) == (1, yon.yuk(P3))  # kısa paket
    assert yon.parca_k(_kp(round(4 * py / 1000)))[0] == 4  # b2QkhmQ0sT0 yükü = 4 × PARCA_YUK
    assert yon.parca_k(_kp(round(2 * py / 1000)))[0] == 2  # orta yük
    assert yon.parca_k(_kp(round(9 * py / 1000)))[0] == 4 and yon.parca_k("# boş")[0] == 1


def test_v10_k1_tek_cagri_son_gecis(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V10"], c, paket=P3)
    assert len([x for x in c if x["i"] != "son"]) == 2 and len(c) == 4  # 2 yanıt × (1 parça + son geçiş)
    assert f" · k 1 (yük {yon.yuk(P3)})" in s["satirlar"][0]


def test_v10_bolumlu_paket_mekanik(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V10"], c)
    v = _kayit(tmp_path, f"{E1}@V10")["form"]["videolar"][0]
    son = [x for x in c if x["i"] == "son"]
    assert "bolumler" not in son[0]["sema"]["properties"] and yon.SON_BOLUM not in son[0]["metin"]
    assert [b["baslik"] for b in v["bolumler"]] == ["Giriş", "Kurulum", "Deneme"]


def test_v10_bolumsuz_paket_son_gecis_bolum_uretir(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V10"], c, paket=PB, b_kur=_b6(c, SON_B))
    y = _kayit(tmp_path, f"{E1}@V10")
    son = [x for x in c if x["i"] == "son"]
    assert son[0]["sema"]["properties"]["bolumler"] == SV["properties"]["videolar"]["items"]["properties"]["bolumler"]
    assert yon.SON_BOLUM in son[0]["metin"] and all(x["metin"].count("bolumler: boş bırak") == 1 for x in c if x["i"] != "son")
    assert y["form"]["videolar"][0]["bolumler"] == BOL and pt._denet(y["form"], SV, "form") == []


def test_v10_bolumsuz_son_gecis_hata_bolum_bos(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V10"], c, paket=PB, b_kur=_b6(c, SON_HATA))
    assert _kayit(tmp_path, f"{E1}@V10")["form"]["videolar"][0]["bolumler"] == [] and " · son geçiş: hata" in s["satirlar"][0]


def test_v10_metinler_yalniz_v10(tmp_path):
    e = yon.EKSIKSIZLIK10
    assert "Emin değilsen ekle" not in e and "öğeyi listeye değil belirsizlikler" in e
    assert "betimlemesi aday, iddia ya da site_ui öğesi değildir" in e and "(komut, prompt, ayar, başlık, kod, araç adı)" in e
    assert "5–8 cümle (ana fikir · gösterilen araçlar/teknikler · adımlar · sonuç)" in yon.SON_SISTEM10
    assert "Emin değilsen ekle" in yon.EKSIKSIZLIK and "5–8" not in yon.SON_SISTEM  # diğer varyantların metni aynı
    c = []
    _e6(tmp_path, [f"{E1}@V10"], c)
    assert {x["sistem"] for x in c if x["i"] != "son"} == {"S\n\n" + e + yon.ORNEK_BASLIK + '{"id": "ORN6"}'}
    assert {x["sistem"] for x in c if x["i"] == "son"} == {yon.SON_SISTEM10}


def test_v10_diger_varyant_metni_ayni(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V8"], c)
    assert {x["sistem"] for x in c if x["i"] != "son"} == {"S\n\n" + yon.EKSIKSIZLIK + yon.ORNEK_BASLIK + '{"id": "ORN6"}'}
    assert {x["sistem"] for x in c if x["i"] == "son"} == {yon.SON_SISTEM}


def test_v10_tanim(tmp_path):
    ge, c = [], []
    s = _e6(tmp_path, [f"{E1}@V10"], c, b_kur=_b8(c, ge), destek={E1: ["seed", "temperature"]})
    assert ge[0] == {"temperature": 0.2, "seed": 7} and "V10" in yon.VARYANT and "V10" in yon.SON
    p = [x for x in c if x["i"] != "son"]
    assert p and all(x["metin"].startswith(yon.ALAN_KURALI + "\n" + yon.PARCA_OZET) for x in p) and "seed yok" not in s["satirlar"][0]


def test_v10_son_gecis_json_yeniden(tmp_path):
    c = []
    s = _e6(tmp_path, [f"{E1}@V10"], c, b_kur=_b6(c, {**SON_HATA, "hata": None}))
    assert len([x for x in c if x["i"] == "son"]) == 4 and "son geçiş: hata (JSON)" in s["satirlar"][0]


# F3-V11: ayrıntı örneği (öğe sayısı korunur) · ad/teknik kuralı · EKRAN METNİ (OCR) bloğu
AD_KURALI = ("adaylar[].ad: aracın ya da kavramın tam adı + kısa tanımı (ör. 'Ağaç modeli: trunk/leaf ve blast radius'); tek kelimelik ad "
             "yazma. site_ui[].teknik: uygulama ayrıntısı (kütüphane, efekt, etkileşim) en az iki cümle.")
OCR3 = {"[0:20] ALFA EKRAN", "[3:10] BETA EKRAN", "[8:00] GAMA EKRAN"}
AYR = {"adaylar": {"video": "src1", "oge": {"ad": "Ağaç modeli: trunk/leaf"}}}


def _ks(x):
    return list(SV["properties"]["videolar"]["items"]["properties"][x]["items"]["properties"])


def _oge(x, d, bos=0):
    return {k: ("" if i < bos else d) for i, k in enumerate(_ks(x))}


def _f11(tmp_path, ad, **lst):
    (tmp_path / f"{ad}.json").write_text(json.dumps({**lst, "fazla": "f" * 50}, ensure_ascii=False), encoding="utf-8")
    return tmp_path / f"{ad}.json"


def _blok(x):
    return x["metin"].split(yon.EKRAN_OCR + "\n", 1)[1].split("\n\n", 1)[0].splitlines()


def test_v11_ayrinti_ornegi_secim(tmp_path):
    ys = [_f11(tmp_path, "a", adaylar=[_oge("adaylar", "x" * 10), _oge("adaylar", "y" * 300, bos=1)], site_ui=[_oge("site_ui", "s" * 5)]),
          _f11(tmp_path, "b", adaylar=[_oge("adaylar", "z" * 20)], site_ui=[{**_oge("site_ui", "t" * 2000), "fazla": "f"}]),
          *[_f11(tmp_path, h, adaylar=[_oge("adaylar", "w" * 99)]) for h in yon.AYRINTI_HARIC]]
    assert yon.AYRINTI_HARIC == ("b2QkhmQ0sT0", "rABIViSQmsc", "ptGXxk1-Uj4", "Ysr7oNDajJI")
    a = yon.ayrinti_ornegi(ys, SV)
    assert a["adaylar"] == {"video": "b", "oge": _oge("adaylar", "z" * 20)}  # dolu 1.0 içinde en uzun; boş alanlı ve hariçler elenir
    o = a["site_ui"]["oge"]
    assert a["site_ui"]["video"] == "b" and set(o) == set(_ks("site_ui"))  # şema dışı alan atılır
    assert 1100 < sum(map(len, o.values())) <= 1200 and all(o.values())  # uzun alan kırpılır, alan boşalmaz
    assert set(a) == {"adaylar", "site_ui"} and yon.ayrinti_ornegi(ys[2:], SV) == {}


def test_v11_onek_ozdes_v10_degismez(tmp_path, monkeypatch):
    monkeypatch.setattr(yon, "PARCA_YUK", 800)  # k > 1: önek tüm parçalarda özdeş
    v10 = "S\n\n" + yon.EKSIKSIZLIK10 + yon.ORNEK_BASLIK + '{"id": "ORN6"}'
    assert yon.AYRINTI_BASLIK == "\n\nAYRINTI ÖRNEĞİ (öğe başına beklenen derinlik; öğe sayısını etkilemez):\n"
    for v, bek in (("V11", v10 + yon.AYRINTI_BASLIK + json.dumps({"adaylar": AYR["adaylar"]["oge"]}, ensure_ascii=False)), ("V10", v10)):
        c = []
        (tmp_path / v).mkdir()
        _e6(tmp_path / v, [f"{E1}@{v}"], c, ayrinti=AYR)
        p = [x for x in c if x["i"] != "son"]
        assert len(p) > 2 and {x["sistem"] for x in p} == {bek}
    s = _e6(tmp_path, [f"{E1}@V11"], [])
    assert s["satirlar"][0] == f"{E1}@V11 · hata: V11 ayrıntı örneği yok · çağrı 0"


def test_v11_ad_kurali_ocr_blogu_parcaya_suzulur(tmp_path, monkeypatch):
    assert yon.ALAN_KURALI11 == yon.ALAN_KURALI + " " + AD_KURALI
    assert yon.EKRAN_OCR.startswith("EKRAN METNİ (OCR)") and ("anlamlı ekran metinlerini (komut, prompt, ayar, başlık, kod, araç adı) "
                                                             "kareden_okunanlar'a kare zamanıyla aktar") in yon.EKRAN_OCR
    c = []
    _e6(tmp_path, [f"{E1}@V11"], c, ayrinti=AYR)  # k 1: aynı mesaj
    p = [x for x in c if x["i"] != "son"]
    assert p and all(x["metin"].startswith(yon.ALAN_KURALI11 + "\n" + yon.PARCA_OZET) and set(_blok(x)) == OCR3 for x in p)
    monkeypatch.setattr(yon, "PARCA_YUK", 800)
    c = []
    (tmp_path / "p4").mkdir()
    _e6(tmp_path / "p4", [f"{E1}@V11"], c, ayrinti=AYR)
    bl = [_blok(x) for x in c if x["i"] != "son" and yon.EKRAN_OCR in x["metin"]]
    assert {s for b in bl for s in b} == OCR3 and max(map(len, bl)) < 3  # her parçada yalnız kendi aralığının OCR satırları


def test_v11_diger_varyant_metni_ayni(tmp_path):
    c = []
    _e6(tmp_path, [f"{E1}@V10"], c, ayrinti=AYR)
    p = [x for x in c if x["i"] != "son"]
    assert p and all(x["metin"].startswith(yon.ALAN_KURALI + "\n" + yon.PARCA_OZET + "\n") and AD_KURALI not in x["metin"]
                     and "EKRAN METNİ" not in x["metin"] for x in p)
    assert yon.ALAN_KURALI == ALAN and AD_KURALI not in yon.EKSIKSIZLIK10


def test_v11_tanim(tmp_path):
    ge, c = [], []
    s = _e6(tmp_path, [f"{E1}@V11"], c, b_kur=_b8(c, ge), destek={E1: ["seed"]}, ayrinti=AYR)
    assert ge[0] == {"temperature": 0.2, "seed": 7} and "V11" in set(yon.VARYANT) & set(yon.SON) & set(yon.PARCA)
    assert f" · k 1 (yük {yon.yuk(P)})" in s["satirlar"][0] and " · hata" not in s["satirlar"][0]
    assert {x["sistem"] for x in c if x["i"] == "son"} == {yon.SON_SISTEM10}
