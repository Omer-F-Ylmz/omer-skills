"""MOTOR-M5: ikinci göz — luna'ya özgü kalem tekilleştirme · doğrulama süzgeci · luna hatasında video düşmez · defter/tavan kalemleri."""
import json

from video import ikinci_goz as ig
from video import parti as pt
from video import tarama as tr

from test_m2a import V, _ctx, _defter, _durum, _form, _kurulum, _ns, _pid

K_EVET = {"komut": "uv tool install yenisey", "ne_yapar": "yeni aracı kurar", "kanit_zamani": "0:05", "kaynak": "altyazı"}
K_UYDURMA = {"komut": "npm i uydurmapaket", "ne_yapar": "uydurma kurulum", "kanit_zamani": "0:05", "kaynak": "altyazı"}
K_KARE = {"teknik": "Parlayan Buton", "ne": "hover ile parlar", "kanit_zamani": "0:05", "kaynak": "kare", "karede_gorulen": "buton"}


def _son(sistem, metin, sema, kareler=(), model=None, butce=.5, env=None, **_):
    if "kararlar" in sema["properties"]:  # görsel yargıç
        return {"form": {"kararlar": [{"no": 1, "karar": "evet"}]}, "usage": {"input_tokens": 3, "output_tokens": 2}, "usd": .002, "sure": .1, "hata": None}
    ids = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"]
    return {"form": {"videolar": [_form(v) for v in ids]}, "usage": {"input_tokens": 10, "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 100, "output_tokens": 50}, "usd": .01, "sure": .1, "hata": None}


class Luna:
    def __init__(self, hata=None):
        self.n, self.hata = 0, hata

    def __call__(self, sistem, metin, sema, kareler=(), **_):
        self.n += 1
        if self.hata:
            return {"form": None, "usage": {}, "usd": 0.0, "sure": .1, "hata": self.hata}
        v = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"][0]
        f = _form(v)
        f["kurulum_komutlar"] = [dict(K_EVET), dict(K_UYDURMA)]
        f["site_ui"] = [*f.get("site_ui", []), dict(K_KARE)]
        return {"form": {"videolar": [f]}, "usage": {"input_tokens": 5, "output_tokens": 5}, "usd": .001, "sure": .1, "hata": None}


def _jev(durumlar, q):
    return [{"dayanir": {"noul": .9 if "yenisey" in s else .1}} for s in durumlar]


def _hazir(tmp_path):
    kok = _kurulum(tmp_path, [V[0]])
    (kare := tmp_path / "k1.jpg").write_bytes(b"\xff\xd8\xff")
    p = kok / "c" / V[0] / "paket.md"
    p.write_text(p.read_text(encoding="utf-8").replace("## Kareler\nyok", f"## Kareler\n{kare.as_posix()} · 0:05"), encoding="utf-8")
    return kok


def _rapor(kok):
    return (kok / "docs" / "video-tarama" / f"2026-09-29-{V[0]}.md").read_text(encoding="utf-8")


def test_ozgu_tekillestirir():
    fs = {"adaylar": [{"ad": "Yenisey", "ne": "araç", "kanit": "x", "repo_url": "https://github.com/a/yenisey"}]}
    fl = {"adaylar": [{"ad": "yenisey (CLI)", "ne": "aynı araç", "kanit": "y", "repo_url": None}],
          "kurulum_komutlar": [{"komut": "npx baska-arac", "ne_yapar": "başka"}]}
    oz = ig.ozgu(fs, fl)
    assert [(b, k.get("komut")) for b, k in oz] == [("kurulum_komutlar", "npx baska-arac")]


def test_dogrulanan_eklenir_dogrulanmayan_ekte_panelde_yok(tmp_path):
    kok = _hazir(tmp_path)
    luna = Luna()
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), {**_ctx(kok, _son), "luna": luna, "jev": _jev}) == 0
    md = _rapor(kok)
    govde, ek = md.split("## Doğrulanamadı (ikinci göz)")
    assert "yenisey" in govde and "Parlayan Buton" in govde and "(ikinci göz)" in govde
    assert "uydurmapaket" not in govde and "uydurmapaket" in ek
    assert "uydurmapaket" not in json.dumps(tr.ayikla(md), ensure_ascii=False)
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert t["durum"] == "tamam" and t["ikinci_goz"]["eklenen"] == 2 and t["ikinci_goz"]["dogrulanamadi"] == 1
    assert luna.n == 1


def test_defter_ve_tavan_kalemleri_ayri(tmp_path, capsys):
    kok = _hazir(tmp_path)
    pt.parti(_ns("baslat", kok / "kuyruk.md"), {**_ctx(kok, _son), "luna": Luna(), "jev": _jev})
    adim = [x["adim"] for x in _defter(kok)]
    assert adim.count("tarama") == 1 and adim.count("ikinci_goz_luna") == 1 and adim.count("ikinci_goz_yargic") == 1
    assert next(x for x in _defter(kok) if x["adim"] == "ikinci_goz_jev")["durum"] == 2
    pdir = kok / ".kos" / _pid(kok)
    assert pt._defter(pdir)[0] == 1  # Sonnet tavanı ikinci göz satırlarını saymaz
    g = pt._ig_defter(pdir)
    assert g["luna"] == 1 and g["jev"] == 2 and g["yargic"] == 1 and abs(g["or_usd"] - .001) < 1e-9
    assert "ikinci göz:" in capsys.readouterr().out


def test_openrouter_tavani_luna_cagirmaz(tmp_path, monkeypatch):
    monkeypatch.setattr(pt, "IG_TAVAN", {"or_usd": 0.0, "jev": 150, "yargic": 8})
    kok = _hazir(tmp_path)
    luna = Luna()
    pt.parti(_ns("baslat", kok / "kuyruk.md"), {**_ctx(kok, _son), "luna": luna, "jev": _jev})
    assert luna.n == 0 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"
    assert "ikinci göz: tavan" in _rapor(kok)


def test_luna_hatasinda_video_dusmez(tmp_path):
    kok = _hazir(tmp_path)
    luna = Luna(hata="ölçülemedi: HTTP 429")
    pt.parti(_ns("baslat", kok / "kuyruk.md"), {**_ctx(kok, _son), "luna": luna, "jev": _jev})
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam" and luna.n == 2
    md = _rapor(kok)
    assert "ikinci göz: luna hatası" in md and "yenisey" not in md


def test_anahtarsiz_kapali_satiri(tmp_path, capsys):
    kok = _hazir(tmp_path)
    pt.parti(_ns("baslat", kok / "kuyruk.md"), {**_ctx(kok, _son), "jev": _jev})
    assert "ikinci göz KAPALI: OPENROUTER_API_KEY yok" in _rapor(kok)
    assert "ikinci göz KAPALI: OPENROUTER_API_KEY yok" in capsys.readouterr().out
    assert all(not x["adim"].startswith("ikinci_goz") for x in _defter(kok))


def test_bayrak_yok_kapali(tmp_path):
    kok = _hazir(tmp_path)
    luna = Luna()
    pt.parti(_ns("baslat", kok / "kuyruk.md", ikinci_goz="yok"), {**_ctx(kok, _son), "luna": luna, "jev": _jev})
    assert luna.n == 0 and "ikinci göz KAPALI: --ikinci-goz yok" in _rapor(kok)
