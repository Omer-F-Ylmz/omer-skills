"""MOTOR-M2d: görsel blok biçimi · açıklama bağlantısı çağrı girdisinde · envanter önek soyma · parti kuyruk tek komut · devam --yeniden-tara."""
import json
from types import SimpleNamespace

from test_m2a import V, Sahte, _ctx, _durum, _kurulum, _ns, _paket, _pid
from test_m2c import _jev

from video import akil, cli, hafif
from video import parti as pt


# K1 kare görsel bloğu: stream-json image/base64, media_type dosya türünden
def test_gorsel_blok_bicimi(tmp_path):
    png, jpg = tmp_path / "k.png", tmp_path / "k.jpg"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")
    jpg.write_bytes(b"\xff\xd8\xff")
    gelen = []

    def kos(args, girdi, env, timeout):
        gelen.append(json.loads(girdi))
        return SimpleNamespace(stdout=json.dumps({"type": "result", "structured_output": {"x": 1}, "usage": {}, "total_cost_usd": 0.0}) + "\n",
                               stderr="", returncode=0)
    hafif.cagir("s", "m", {"type": "object"}, kareler=[str(png), str(jpg)], kos=kos, env={})
    icerik = gelen[0]["message"]["content"]
    assert icerik[0] == {"type": "text", "text": "m"}
    assert [(b["type"], b["source"]["type"], b["source"]["media_type"]) for b in icerik[1:]] == \
        [("image", "base64", "image/png"), ("image", "base64", "image/jpeg")]


# K2 açıklama bağlantısı temizlenmiş çağrı girdisinde kalır (M9qgd benzeri); yerel yol yine gizlenir
def test_aciklama_baglantisi_cagri_girdisinde(tmp_path):
    u = "https://www.skool.com/buildroom/"
    _paket(tmp_path, V[0], 30, [u])
    pk = {V[0]: pt.paket_oku(tmp_path / "c" / V[0] / "paket.md")}
    assert u in pt._istem([V[0]], pk, {}, lambda x: cli._temizle(x, {}))
    assert cli._temizle("kare C:/Projeler/.video-cache/a.jpg", {}) == "kare [yol]"


def _aday(ad, kurulu):
    return {"ad": ad, "adlar": [ad], "tur": "CLI", "repo": None, "kurulu": kurulu, "alt_tur": "araç", "videolar": {V[0]: {"ne": "gözlem"}}}


# K3 `<paket>:<ad>` öneki soyulur: ad birebirse tam eşleşme (Jev'e sorulmaz); benzer ama farklı ad Jev'e gider
def test_onek_soyma_tam_eslesme(tmp_path):
    ad = {"task-observer": _aday("task-observer", "anthropic-skills:task-observer"),
          "task-watcher": _aday("task-watcher", "anthropic-skills:task-observer")}
    assert akil._tam(ad["task-observer"]) and not akil._tam(ad["task-watcher"])
    j, sorulan = _jev(), []
    akil._yargi({"yargila": lambda s, q: sorulan.append(s) or j(s, q)}, ad, tmp_path)
    assert len(sorulan) == 1 and len(sorulan[0]) == 1 and "esdeger_p" in ad["task-watcher"] and "esdeger_p" not in ad["task-observer"]


# K4 tek komut: kuyruk → baslat → tarama → akil → panel yolu + defter özeti, panelde durur
def test_parti_kuyruk_panelde_durur(tmp_path, monkeypatch, capsys):
    kok = _kurulum(tmp_path, V[:2])
    cagri = []
    monkeypatch.setattr(akil, "akil", lambda pdir, d, k, tdir, ctx, tum=False: cagri.append(d["parti"]) or 0)
    s = Sahte()
    assert pt.parti(_ns("kuyruk", kok / "kuyruk.md"), _ctx(kok, s)) == 0
    assert cagri == [_pid(kok)] and len(s.cagrilar) == 1
    assert all(x["tarama"]["durum"] == "tamam" for x in _durum(kok)["videolar"].values())
    o = capsys.readouterr().out
    assert f"docs/kurulumlar/parti/{_pid(kok)}/panel.md" in o and "defter 1 çağrı" in o


# Ek: URL hatası sonrası motorla taranmış video yeniden taranır
def test_devam_yeniden_tara(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    assert pt.parti(_ns("devam", _pid(kok), yeniden_tara=True), _ctx(kok, s)) == 0
    assert len(s.cagrilar) == 2 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"
