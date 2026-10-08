"""VİDEO-PARTİ-YT1-ONARIM: gece koşucusu tavanda devam --cagri-ek/--usd-ek kullanır; tavanın üst sınırları silinmez."""
from test_m2a import V, Sahte, _ctx, _durum, _kurulum, _ns, _pid

from video import parti as pt


def test_devam_ek_tavan_ust_sinirlarini_korur(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md", usd_tavan_max=3.75), _ctx(kok, s))
    pt.parti(_ns("devam", _pid(kok), cagri_ek=2, usd_ek=0.5), _ctx(kok, s))
    t = _durum(kok)["tavan"]
    assert t["usd_max"] == 3.75 and "cagri_max" in t


def test_tara_ikili_ham_kol_formlarini_yazar(tmp_path):  # 2: karede_gorulen hangi kolda boş — kol başı ham form diskte
    import json
    from test_m2a import _form
    v, son, hai = "aaaaaaaaaa1", "claude-sonnet-5-5", "claude-haiku-5-5"
    pk = {v: {"kareler": [], "sure": 300, "metin": "x"}}
    d = {"butce": .5, "tavan": {"usd": 5.0}, "videolar": {v: {"tarama": {}}}}

    def cagir(sistem, metin, sema, **k):
        return {"form": {"videolar": [{**_form(v), "baslik": k["model"]}]}, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": None, "model": k["model"]}
    pt._tara_ikili([v], pk, {}, lambda s: s, d, tmp_path, {}, cagir, [son, hai])
    for kol, mdl in (("sonnet", son), ("haiku", hai)):
        assert json.loads((tmp_path / "form" / f"{v}.{kol}.json").read_text(encoding="utf-8"))["baslik"] == mdl


def test_sema_modele_giden_form_1b_2a_ile_ayni():  # 2 KARAR: kare zorunluluğu geri alındı — karede_gorulen opsiyonel string/null
    it = pt.sema(["aaaaaaaaaa1"], iz=True)["properties"]["videolar"]["items"]["properties"]
    for b in ("adaylar", "site_ui", "promptlar", "iddialar", "kurulum_komutlar"):
        assert "karede_gorulen" not in it[b]["items"]["required"] and it[b]["items"]["properties"]["karede_gorulen"]["type"] == ["string", "null"]


def _kare_form(tmp_path, monkeypatch, kanit):
    from test_m2a import _form
    v = "aaaaaaaaaa1"
    (k := tmp_path / "k.jpg").write_bytes(b"x")
    monkeypatch.setattr(pt.hafif, "GORSEL", True)
    f = _form(v)
    f["adaylar"][0].update(kaynak="kare", kanit=kanit, karede_gorulen=None)
    p = {"baslik": "b", "kanal": "k", "sure": 300, "dil": "en", "id": v, "metin": "x", "linkler": [], "kareler": [str(k)]}
    return v, {"videolar": [f]}, p


def test_kanitli_bos_karede_kanittan_doldurulur(tmp_path, monkeypatch):  # 2 KARAR: yedek kural
    v, form, p = _kare_form(tmp_path, monkeypatch, "Ekranda Hızlı Araç penceresi")
    pt.kanittan(form)
    assert not [h for h in pt.dogrula(form, {v: p}, [v]).get(v, []) if "karede_gorulen" in h]
    assert "(karede: kanıttan) Ekranda Hızlı Araç penceresi" in pt.rapor_md(form["videolar"][0], p, [])


def test_kanitsiz_bos_karede_eksik_kalir(tmp_path, monkeypatch):  # 2 KARAR: ikisi de boşsa eski EKSİK kuralı
    v, form, p = _kare_form(tmp_path, monkeypatch, "Ekranda Hızlı Araç penceresi")  # site_ui satırında kanit alanı yok
    form["videolar"][0]["site_ui"] = [{"teknik": "Hero", "ne": "Tam ekran giriş", "kanit_zamani": "0:05", "kaynak": "kare", "karede_gorulen": ""}]
    pt.kanittan(form)
    f, eksik = pt.kismi(form["videolar"][0], pt.dogrula(form, {v: p}, [v]).get(v, []), v)
    assert [e[1] for e in eksik] == ["karede_gorulen"] and f["site_ui"][0]["karede_gorulen"].startswith("EKSİK")
