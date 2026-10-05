"""F1: model yönlendirme adaptörü — OmniRoute (OpenAI biçimi, sahte sağlayıcı) · adım başı seçim · varsayılan değişmez · anahtar sızmaz."""
import io
import json
import urllib.error
import urllib.request

import pytest

from video import akil, hafif
from video import ikinci_goz as ig
from video import parti as pt
from video import tarama as tr
from video import yonlendir as yon
from test_m2a import V, Sahte, _ctx, _kurulum, _ns, _pid

ANAHTAR = "sk-omni-gizli-1234567890"
ENV = {"OMNIROUTE_KEY": ANAHTAR}
SEMA = {"type": "object", "required": ["a"], "additionalProperties": False, "properties": {"a": {"type": "string"}}}
FORM = {"a": "b"}
ROTA = {"arastirma": {"saglayici": "omniroute", "model": "gpt-4o-mini"}}


class Omni:
    """Sahte OmniRoute: openapi.yaml:9031 ChatCompletionResponse (choices[].message.content · usage.prompt/completion/total_tokens)."""

    def __init__(self, durum=200, govde=None, hata=None):
        self.cagrilar, self.durum, self.govde, self.hata = [], durum, govde, hata

    def __call__(self, url, govde, bas):
        self.cagrilar.append((url, govde, bas))
        if self.hata:
            raise self.hata
        return self.durum, self.govde if self.govde is not None else {
            "id": "c1", "object": "chat.completion", "created": 1, "model": govde["model"],
            "choices": [{"index": 0, "message": {"role": "assistant", "content": json.dumps(FORM)}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18}}


def test_omni_istek_openai_bicimi_yanit_cozulur():
    o = Omni()
    y = yon.omni_cagir("gpt-4o-mini", ENV, gonder=o)("SİS", "METİN", SEMA, model="yok-sayılır", butce=0.5, env={})
    url, govde, bas = o.cagrilar[0]
    assert url == "http://localhost:20128/v1/chat/completions" and yon.OMNI_YOL == "/v1/chat/completions"
    assert govde["model"] == "gpt-4o-mini" and [m["role"] for m in govde["messages"]] == ["system", "user"]
    assert govde["messages"][0]["content"] == "SİS" and "METİN" in json.dumps(govde["messages"][1], ensure_ascii=False)
    assert bas["Authorization"] == f"Bearer {ANAHTAR}"
    assert y["form"] == FORM and y["hata"] is None and y["usd"] is None  # F1 eki (Ömer, 5 Eki): fiyatsız model 0 değil
    assert y["usage"] == {"input_tokens": 11, "output_tokens": 7}


def test_omni_url_ortamdan_yol_ayar_sabiti(monkeypatch):
    o = Omni()
    yon.omni_cagir("m", {**ENV, "OMNIROUTE_URL": "http://127.0.0.1:9999/"}, gonder=o)("s", "m", SEMA)
    monkeypatch.setattr(yon, "OMNI_YOL", "/api/v1/chat/completions")
    yon.omni_cagir("m", ENV, gonder=o)("s", "m", SEMA)
    assert [u for u, _, _ in o.cagrilar] == ["http://127.0.0.1:9999/v1/chat/completions", "http://localhost:20128/api/v1/chat/completions"]


@pytest.mark.parametrize("o, neden", [
    (Omni(401, {"error": {"message": f"geçersiz anahtar {ANAHTAR}"}}), "HTTP 401"),
    (Omni(400, {"error": {"code": "invalid_model", "message": "model yok"}}), "invalid_model"),
    (Omni(hata=urllib.error.URLError(ConnectionRefusedError(10061, "bağlantı reddedildi"))), "URLError"),
    (Omni(hata=TimeoutError(f"zaman aşımı {ANAHTAR}")), "TimeoutError"),
])
def test_omni_hata_adim_dusmez_sebep_gorunur_anahtar_yok(o, neden):
    y = yon.omni_cagir("m", ENV, gonder=o)("s", "m", SEMA)
    assert y["form"] is None and neden in y["hata"] and y["hata"].startswith("ölçülemedi")
    assert ANAHTAR not in json.dumps(y, ensure_ascii=False)


def test_post_hata_govdesi_korunur(monkeypatch):
    def ac(govde):
        def urlopen(r, timeout=None):
            raise urllib.error.HTTPError(r.full_url, 400, "Bad Request", {}, io.BytesIO(govde))
        return urlopen
    monkeypatch.setattr(urllib.request, "urlopen", ac(b'{"error": {"code": "invalid_model"}}'))
    assert ig._post("http://x/v1/chat/completions", {}, {}) == (400, {"error": {"code": "invalid_model"}})
    monkeypatch.setattr(urllib.request, "urlopen", ac(b"<html>"))
    assert ig._post("http://x/v1/chat/completions", {}, {}) == (400, {})


def test_sec_tanimsiz_adim_varsayilan_birebir():
    c = object()
    assert yon.sec({"model": hafif.MODEL}, "arastirma", c, ENV) == (c, hafif.MODEL)
    assert yon.sec({"model": hafif.MODEL, "yonlendirme": ROTA}, "tarama", c, ENV) == (c, hafif.MODEL)
    c2, model = yon.sec({"model": hafif.MODEL, "yonlendirme": ROTA}, "arastirma", c, ENV)
    assert c2 is not c and callable(c2) and model == "gpt-4o-mini"


def _d(**k):
    return {"model": hafif.MODEL, "butce": 0.5, "tavan": {"usd": 1.0, "cagri": 5}, "yonlendirme": ROTA, **k}


@pytest.mark.parametrize("o, durum", [(Omni(), "tamam"), (Omni(401, {"error": {"message": ANAHTAR}}), "hata")])
def test_form_al_adim_ayardan_yonlenir(tmp_path, monkeypatch, o, durum):
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: yon.omni_cagir(m, env, gonder=o))
    varsayilan = lambda *a, **k: pytest.fail("yönlendirilen adımda varsayılan taşıyıcı çağrılmamalı")  # noqa: E731
    sonuc = akil._form_al(tmp_path, _d(), varsayilan, "s", "m", SEMA, "arastirma", "aday", ENV)
    satir = tr.kayit_oku(tmp_path / "defter.jsonl")
    assert sonuc[0] == durum and len(o.cagrilar) == 1 and satir[0]["model"] == "gpt-4o-mini"
    assert sonuc[1] == FORM if durum == "tamam" else ("HTTP 401" in sonuc[1] and ANAHTAR not in json.dumps(satir))


def test_form_al_tanimsiz_adim_varsayilan_tasiyici(tmp_path):
    s = []
    akil._form_al(tmp_path, _d(), lambda *a, **k: s.append(k["model"]) or {"form": FORM, "usage": {}, "usd": 0.0, "sure": 0, "hata": None},
                  "s", "m", SEMA, "gelistirme", "parti", ENV)
    assert s == [hafif.MODEL] and tr.kayit_oku(tmp_path / "defter.jsonl")[0]["model"] == hafif.MODEL


def test_parti_tarama_adimi_yonlenir(tmp_path, monkeypatch):
    kok = _kurulum(tmp_path, V[:1], sure=300)
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Sahte(kes=1)))
    yol = kok / ".kos" / _pid(kok) / "durum.json"
    d = json.loads(yol.read_text(encoding="utf-8"))
    yol.write_text(json.dumps({**d, "yonlendirme": {"tarama": {"saglayici": "omniroute", "model": "gpt-4o-mini"}}}), encoding="utf-8")
    o = Omni(hata=KeyboardInterrupt())
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: yon.omni_cagir(m, env, gonder=o))
    s = Sahte()
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    assert s.cagrilar == [] and o.cagrilar[0][1]["model"] == "gpt-4o-mini"


# F1 eki — maliyet (Ömer, 5 Eki): FIYAT ayarı boş başlar; yanıt başlığı X-OmniRoute-Response-Cost (openapi.yaml:1173) önceliklidir;
# fiyatı bilinmeyen model → usd None (0 değil), defterde "maliyet bilinmiyor", panel Denetim'de satır.
class OmniBaslik(Omni):
    def __init__(self, basliklar, **k):
        super().__init__(**k)
        self.basliklar = basliklar

    def __call__(self, url, govde, bas):
        return (*super().__call__(url, govde, bas), self.basliklar)


def test_maliyet_fiyat_tablosundan(monkeypatch):
    monkeypatch.setitem(yon.FIYAT, "gpt-4o-mini", {"girdi": 2.0, "cikti": 10.0, "kaynak": "test"})
    y = yon.omni_cagir("gpt-4o-mini", ENV, gonder=Omni())("s", "m", SEMA)
    assert y["usd"] == pytest.approx((11 * 2.0 + 7 * 10.0) / 1e6)


def test_maliyet_bilinmeyen_model_none_defter_panel(tmp_path, monkeypatch):
    assert yon.FIYAT == {}  # değerler tahmin edilmez; F1-KURULUM'da sağlayıcı sayfasından
    assert yon.omni_cagir("gpt-4o-mini", ENV, gonder=Omni())("s", "m", SEMA)["usd"] is None
    from test_m11 import _kur
    pdir, d = _kur(tmp_path)
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: yon.omni_cagir(m, env, gonder=Omni()))
    akil._form_al(pdir, {**d, **_d()}, None, "s", "m", SEMA, "arastirma", "aday", ENV)
    satir = tr.kayit_oku(pdir / "defter.jsonl")[-1]
    assert satir["usd"] is None and satir["maliyet"] == "bilinmiyor"
    p = akil.panel(pdir, d, tmp_path).read_text(encoding="utf-8")
    assert "- maliyet bilinmiyor: arastirma · gpt-4o-mini" in tr.bolum(p, "Denetim")


@pytest.mark.parametrize("bas, usd", [({"x-omniroute-response-cost": "0.0001234500"}, 0.00012345),
                                      ({"X-OmniRoute-Response-Cost": "0.0000000000"}, (11 * 2.0 + 7 * 10.0) / 1e6)])
def test_maliyet_yanit_basligi_oncelikli(monkeypatch, bas, usd):
    monkeypatch.setitem(yon.FIYAT, "gpt-4o-mini", {"girdi": 2.0, "cikti": 10.0, "kaynak": "test"})
    assert yon.omni_cagir("gpt-4o-mini", ENV, gonder=OmniBaslik(bas))("s", "m", SEMA)["usd"] == pytest.approx(usd)


def test_post_basliklari_doner(monkeypatch):
    class Y(io.BytesIO):
        status, headers = 200, {"X-OmniRoute-Response-Cost": "0.5"}
        def __enter__(self): return self
        def __exit__(self, *a): pass
    monkeypatch.setattr(urllib.request, "urlopen", lambda r, timeout=None: Y(b"{}"))
    assert ig._post("http://x", {}, {}) == (200, {}) and ig._post("http://x", {}, {}, basliklar=True)[2]["X-OmniRoute-Response-Cost"] == "0.5"
