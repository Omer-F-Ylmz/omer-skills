"""F3 ön kontrol: A/B'den önce OmniRoute ücretsiz model listesiyle yoklanır; sunucu yok / 401 / model yok → hata metni, model çağrısı yok."""
from video import yonlendir as yon

ENV = {"OMNIROUTE_URL": "http://x:1", "OMNIROUTE_KEY": "gizli-anahtar"}


def _getir(cevap):
    gorulen = []

    def getir(url, govde, bas):
        gorulen.append((url, govde, bas))
        if isinstance(cevap, Exception):
            raise cevap
        return cevap
    return getir, gorulen


def test_model_listede_hata_yok_ve_uc_nokta_openapi():
    g, gorulen = _getir((200, {"object": "list", "data": [{"id": "a/m1"}, {"id": "b/m2"}]}))
    assert yon.omni_yokla("b/m2", ENV, g) is None
    url, govde, bas = gorulen[0]
    assert url == "http://x:1/api/v1/models" and govde is None and bas["Authorization"] == "Bearer gizli-anahtar"


def test_sunucu_yok():
    g, _ = _getir(ConnectionRefusedError("bağlanılamadı"))
    h = yon.omni_yokla("b/m2", ENV, g)
    assert "OmniRoute yok" in h and "gizli-anahtar" not in h


def test_401_kimlik():
    g, _ = _getir((401, {"error": "unauthorized gizli-anahtar"}))
    h = yon.omni_yokla("b/m2", ENV, g)
    assert "401" in h and "OMNIROUTE_KEY" in h and "gizli-anahtar" not in h


def test_model_listede_yok():
    g, _ = _getir((200, {"data": [{"id": "a/m1"}]}))
    assert "model yok: b/m2" in yon.omni_yokla("b/m2", ENV, g)
