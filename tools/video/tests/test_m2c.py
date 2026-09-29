"""MOTOR-M2c: öneri mantığı — alt tür · eksik alan SOR · eşdeğer eşiği · araştırma sonrası ön tarama · form erişilemez/karede."""
import json
from types import SimpleNamespace

from test_m2a import V, _form, _ns
from test_m2b import _actx, _arastirma, _parti, _rapor

from video import akil, hafif
from video import parti as pt

PID = "2026-09-29-short"


def _panel(kok, pid=PID):
    y = kok / "docs" / "kurulumlar" / "parti" / pid / "panel.md"
    t = y.read_text(encoding="utf-8")
    return {h[0]: h for s in t.splitlines() if len(h := [x.strip() for x in s.strip().strip("|").split("|")]) == 8}, t


class Ar:
    """Ada göre form döndüren sahte araştırıcı; çağrılan adlar kaydedilir."""
    def __init__(self, formlar):
        self.formlar, self.adlar, self.cagrilar = formlar, [], []

    def __call__(self, sistem, metin, sema, **k):
        ad = metin.split("ADAY: ", 1)[1].split(" (", 1)[0].split(" ·", 1)[0]
        self.adlar.append(ad)
        self.cagrilar.append(("karşılaştırma" if sistem == akil.SISTEM_GEL else "araştırma", ad, tuple(k.get("araclar") or ())))
        return {"form": {**_arastirma(ad), **self.formlar.get(ad, {})}, "usage": {}, "usd": 0.01, "sure": 0.1, "hata": None}


def _jev(alt="araç", es=0.1):
    def yargila(states, q):
        yargila.n += 1
        return [{"alt_tur": {"probabilities": {"araç": 0.05, "servis": 0.05, "ürün": 0.05, alt: 0.9}},
                 "esdeger": {"probabilities": {"aynı": es, "farklı": 1 - es}}} for _ in states]
    yargila.n = 0
    return yargila


def _ctx(kok, ar, jev=None, on=None):
    c = _actx(kok, ar)
    return {**c, "yargila": jev or _jev(), "on": on or (lambda ns, ctx: None), "env": {**c["env"], "VIDEO_UYGULA_KOK": str(kok)}}


# K1 kendi aracımız ZATEN VAR (araştırma yok); servise OSS lisans kapısı yok
def test_k1_alt_tur(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("claude-code", "CLI", None), ("groq", "CLI", None)])})
    ar = Ar({"groq": {"lisans": "yok", "son_commit": "2026-09-01", "alt_tur": "servis", "ucretsiz_katman": "var"}})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, ar))
    r, _ = _panel(tmp_path)
    assert [a for t, a, _ in ar.cagrilar if t == "araştırma"] == ["groq"]  # ilke 29: araştırma yalnız groq
    assert {(t, x) for t, a, x in ar.cagrilar if a == "claude-code"} == {("karşılaştırma", ())}  # yalnız araçsız karşılaştırma
    assert r["claude-code"][5] == "ZATEN VAR"
    assert r["groq"][5] != "RED" and "servis" in r["groq"][6]


# K2 bilinmiyor → SOR (eksik: alan); kanıtlı olumsuz → RED
def test_k2_eksik_alan_sor(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("markitdown", "CLI", None), ("gpl-arac", "CLI", None)])})
    ar = Ar({"markitdown": {"lisans": "MIT", "son_commit": None, "alt_tur": "araç"},
             "gpl-arac": {"lisans": "GPL-3.0", "son_commit": "2026-09-01", "alt_tur": "araç"}})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, ar))
    r, _ = _panel(tmp_path)
    assert r["markitdown"][5] == "SOR" and "eksik: son_commit" in r["markitdown"][6]
    assert r["gpl-arac"][5] == "RED"


def _aday(ad, **k):
    return {"ad": ad, "tur": "CLI", "repo": None, "adlar": [ad], "arac": True, "kurulu": None, "durum": "onceki", "alt_tur": "araç",
            "videolar": {V[0]: {"zaman": "0:01", "ne": "araç", "kanit": "k", "iddialar": []}}, **k}


# K3 zayıf eşdeğer ZATEN VAR değil; ad benzerliği tek başına tekrar değil
def test_k3_esdeger_esigi_ve_tekrar(tmp_path):
    (a := tmp_path / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    (a / "claude-mm.md").write_text("# claude-mm\nad: claude-mm\ntur: CLI\nrepo: baska/claude-mm\n", encoding="utf-8")
    (pdir := tmp_path / ".kos" / PID).mkdir(parents=True)
    d = {"parti": PID, "videolar": {}, "adaylar": {
        "jcode": _aday("jcode", kurulu="codex", esdeger_p=0.6, durum="kurulu"),
        "hizli": _aday("hizli", kurulu="hizli-cli", esdeger_p=0.8, durum="kurulu"),
        "claude-mem": _aday("claude-mem", repo="thedotmack/claude-mem")}}
    akil.panel(pdir, d, tmp_path)
    r, t = _panel(tmp_path)
    assert r["jcode"][5] != "ZATEN VAR" and "jcode ≈ codex" in t.split("## OLASI EŞDEĞER", 1)[1]
    assert r["hizli"][5] == "ZATEN VAR"
    assert t.split("## OLASI TEKRAR", 1)[1].split("##", 1)[0].strip() == "- yok"


# K4 araştırma repo bulunca ön tarama sonradan koşar; servis → sebepli "koşmadı"
def test_k4_arastirma_sonrasi_on_tarama(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("hizli", "CLI", None), ("groq", "CLI", None)])})
    ar = Ar({"hizli": {"repo_url": "https://github.com/ornek/hizli", "lisans": "MIT", "son_commit": "2026-09-01", "alt_tur": "araç"},
             "groq": {"alt_tur": "servis"}})
    kos = []

    def on(ns, ctx):
        kos.append((ns.aday, ns.repo))
        (y := tmp_path / ".kos" / ns.video / f"{ns.aday}-x").mkdir(parents=True)
        (y / "on.md").write_text("# on\n## Güvenlik ön taraması\nsemgrep 0 · HIGH/CRITICAL 0\n", encoding="utf-8")
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, ar, on=on))
    r, _ = _panel(tmp_path)
    assert kos == [("hizli", "ornek/hizli")]
    assert "HIGH/CRITICAL 0" in r["hizli"][4]
    assert r["groq"][4].startswith("koşmadı: servis")


# K5 erişilemez bağlantı kararı; karede görülen yalnız kaynak=kare
def test_k5_erisilemez_ve_karede(monkeypatch):
    monkeypatch.setattr(hafif, "GORSEL", True)
    assert "erisilemez" in pt.sema([V[0]])["properties"]["videolar"]["items"]["properties"]["aciklama_baglantilari"]["items"]["properties"]
    pk = {"id": V[0], "baslik": "B", "kanal": "K", "sure": 100, "dil": "tr", "metin": "## Segmentler\n[0:00] a\n",
          "linkler": ["https://www.skool.com/x"], "kareler": ["kare-1.jpg"]}
    f = _form(V[0])
    f["aciklama_baglantilari"] = [{"url": "https://www.skool.com/x", "ne": "topluluk", "aday_mi": False, "neden": "ücretli topluluk",
                                   "aday_adi": None, "erisilemez": "ücretli topluluk, giriş gerekli"}]
    f["site_ui"] = [{"teknik": "grid", "ne": "düzen", "kanit_zamani": "0:05", "kaynak": "altyazı"}]
    h = [e for e in pt.dogrula({"videolar": [f]}, {V[0]: pk}, [V[0]]).get(V[0], []) if "karede" in e or "aciklama" in e]
    assert h == []
    assert "erişilemez: ücretli topluluk" in pt.rapor_md(f, pk, [])
    f["site_ui"][0]["kaynak"] = "kare"
    assert any("site_ui[0].karede_gorulen" in e for e in pt.dogrula({"videolar": [f]}, {V[0]: pk}, [V[0]]).get(V[0], []))


# K6 panel uygula ogren.KARAR değerlerini de işler; boş satır dokunulmaz
def test_panel_uygula_karar_degerleri(tmp_path):
    y = tmp_path / "panel.md"
    y.write_text("| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |\n|---|---|---|---|---|---|---|---|\n"
                 "| groq | CLI | 1 | — | — | SOR | s | DENE |\n| webcmd | CLI | 1 | — | — | SOR | s | UYARLA |\n"
                 "| claude-code | CLI | 1 | — | — | ZATEN VAR | s | ZATEN VAR |\n| find-skills | CLI | 1 | — | — | SOR | s | |\n", encoding="utf-8")
    yak = []
    assert akil.panel_uygula(SimpleNamespace(panel=str(y)), {"karar": lambda ns, ctx: yak.append((ns.ad, ns.secim)) or 0}) == 0
    assert yak == [("groq", "DENE"), ("webcmd", "UYARLA"), ("claude-code", "ZATEN VAR")]


def test_jev_alt_tur_bir_kez(tmp_path):
    """alt_tur formda yoksa Jev doldurur; durum.json'a yazılır, ikinci koşuda sorulmaz."""
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("nim", "CLI", None)])})
    j = _jev(alt="servis")
    for _ in range(2):
        pt.parti(_ns("akil", p.name), _ctx(tmp_path, Ar({}), jev=j))
    d = json.loads((p / "durum.json").read_text(encoding="utf-8"))
    assert d["adaylar"]["nim"]["alt_tur"] == "servis" and j.n == 1
