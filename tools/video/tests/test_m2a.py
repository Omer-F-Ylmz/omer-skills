"""MOTOR-M2a: hafif taşıyıcı · atomik durum + devam · form reddi · short toplu · tavan · karar arşivi."""
import json
import subprocess
from types import SimpleNamespace

import pytest

from video import cli, hafif
from video import metin as m
from video import parti as pt
from video import tarama as tr

V = ["aaaaaaaaaa1", "bbbbbbbbbb2", "cccccccccc3"]
OZET = "Kısa video bir aracı tanıtıyor."


def _paket(kok, v, sure, link):
    d = kok / "c" / v
    d.mkdir(parents=True)
    (d / "paket.md").write_text(
        f"# {v} · Başlık {v} · Kanal · süre {m.ss(sure)} · sure_sn {sure} · short: {'true' if sure <= 60 else 'false'} · dil tr · https://youtu.be/{v}\n"
        "## Chapter\nyok\n## Açıklama bağlantıları\n" + ("\n".join(link) or "yok")
        + "\n## Segmentler\n[0:00] merhaba\n[0:05] bu araç işi hızlandırıyor\n## Kareler\nyok\n", encoding="utf-8")


def _kurulum(kok, videolar, sure=30, link=()):
    for v in videolar:
        _paket(kok, v, sure, link)
    (kok / "kuyruk.md").write_text("### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n"
                                   + "".join(f"| {v} | {sure / 60:.1f} | t | - | bekliyor |\n" for v in videolar), encoding="utf-8")
    return kok


def _form(v, ozet=OZET):
    return {"id": v, "ozet": ozet, "bolumler": [{"zaman": "0:00", "baslik": "Giriş"}],
            "adaylar": [{"ad": "Hızlı Araç", "tur": "CLI", "ne": "İşi hızlandıran komut satırı aracı", "kanit_zamani": "0:05",
                         "kaynak": "altyazı", "kanit": "Anlatıcı aracın işi hızlandırdığını söylüyor.", "repo_url": None}],
            "aciklama_baglantilari": [], "site_ui": [], "promptlar": [],
            "iddialar": [{"iddia": "Araç işi hızlandırıyor", "kanit_zamani": "0:05", "kaynak": "altyazı", "tur": "özellik", "aday_adi": "Hızlı Araç"}],
            "kareden_okunanlar": [], "belirsizlikler": ["Aracın adı net değil."]}


class Sahte:
    """Sahte hafif taşıyıcı: her çağrının istediği id'ler kaydedilir; bozuk(v, n) → n. çağrıda boş özet; kes=n → n. çağrıda kesinti."""

    def __init__(self, bozuk=lambda v, n: False, kes=None):
        self.cagrilar, self.bozuk, self.kes = [], bozuk, kes

    def __call__(self, sistem, metin, sema, **k):
        ids = sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"]
        self.cagrilar.append((ids, metin))
        n = len(self.cagrilar)
        if n == self.kes:
            raise KeyboardInterrupt
        return {"form": {"videolar": [_form(v, "" if self.bozuk(v, n) else OZET) for v in ids]},
                "usage": {"input_tokens": 10, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 100, "output_tokens": 50},
                "usd": 0.01, "sure": 0.1, "hata": None}


def _ns(eylem, hedef, **k):
    return SimpleNamespace(**{"eylem": eylem, "hedef": str(hedef), "en_fazla": 8, "short": False, "uzun": False, "model": hafif.MODEL,
                              "cagri_tavan": 12, "usd_tavan": 1.0, "butce": 0.5, "tarih": "2026-09-29", **k})


def _ctx(kok, cagir):
    return {"env": {"VIDEO_UYGULA_KOK": str(kok)}, "kok": kok / "c", "tarama_dizin": kok / "docs" / "video-tarama", "cagir": cagir,
            "alt": lambda argv: pytest.fail(f"paket varken aşama 2 çağrılmamalı: {argv}"), "temizle": lambda s: s}


def _pid(kok):
    return next((kok / ".kos").iterdir()).name


def _durum(kok):
    return json.loads((kok / ".kos" / _pid(kok) / "durum.json").read_text(encoding="utf-8"))


def _defter(kok):
    return tr.kayit_oku(kok / ".kos" / _pid(kok) / "defter.jsonl")


def test_hafif_tasiyici_bayraklar_env_ve_form(tmp_path):
    goren = {}

    def kos(args, girdi, env, timeout):
        goren.update(args=args, girdi=girdi, env=env)
        son = {"type": "result", "is_error": False, "structured_output": {"videolar": []}, "total_cost_usd": 0.028,
               "usage": {"input_tokens": 2, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 3648, "output_tokens": 1315}}
        return subprocess.CompletedProcess(args, 0, '{"type":"system","subtype":"init"}\n' + json.dumps(son) + "\n", "")

    (kare := tmp_path / "k.jpg").write_bytes(b"\xff\xd8\xff")
    y = hafif.cagir("sistem", "metin", {"type": "object"}, kareler=[kare], butce=0.3,
                    env={"ANTHROPIC_BASE_URL": "http://127.0.0.1:1", "PATH": "x"}, kos=kos)
    assert y["form"] == {"videolar": []} and y["usd"] == 0.028 and y["usage"]["output_tokens"] == 1315 and y["hata"] is None
    a = goren["args"]
    assert a[a.index("--model") + 1] == "claude-sonnet-5-5" and a[a.index("--max-budget-usd") + 1] == "0.30"
    assert a[a.index("--tools") + 1] == "" and "--no-session-persistence" in a and "--json-schema" in a
    assert "ANTHROPIC_BASE_URL" not in goren["env"]
    blok = json.loads(goren["girdi"])["message"]["content"]
    assert [b["type"] for b in blok] == ["text", "image"]


def test_hafif_zaman_asimi_hata_doner():
    def kos(args, girdi, env, timeout):
        raise subprocess.TimeoutExpired(args, timeout)

    y = hafif.cagir("s", "m", {}, env={}, kos=kos, timeout=5)
    assert y["form"] is None and "zaman aşımı" in y["hata"]


def test_kesinti_devam_tamamlanan_cagri_tekrarlanmaz(tmp_path):
    kok = _kurulum(tmp_path, V[:2], sure=300)  # uzun: video başına tek çağrı
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Sahte(kes=2)))
    d = _durum(kok)
    assert d["videolar"][V[0]]["tarama"]["durum"] == "tamam" and d["videolar"][V[1]]["tarama"]["durum"] != "tamam"
    assert not list((kok / ".kos").rglob("*.tmp"))
    s = Sahte()
    assert pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s)) == 0
    assert [ids for ids, _ in s.cagrilar] == [[V[1]]]
    assert pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s)) == 0
    assert len(s.cagrilar) == 1 and len(_defter(kok)) == 2


def test_form_red_iki_yeniden_istek_sonra_form_red(tmp_path):
    kok = _kurulum(tmp_path, V[:1], sure=300)
    s = Sahte(bozuk=lambda v, n: True)
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    assert len(s.cagrilar) == 3 and "ozet" in s.cagrilar[1][1]  # yeniden istek hata mesajıyla
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam_eksik"  # M2e K1: iki yeniden istekten sonra kısmi kabul
    assert (kok / "docs" / "video-tarama" / f"2026-09-29-{V[0]}.md").exists()  # M2e K1: kısmi rapor yazılır


def test_form_red_sonra_duzelen_form_kabul(tmp_path):
    kok = _kurulum(tmp_path, V[:1], sure=300)
    s = Sahte(bozuk=lambda v, n: n == 1)
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    assert len(s.cagrilar) == 2 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"


def test_aciklama_baglantisi_karari_zorunlu(tmp_path):
    kok = _kurulum(tmp_path, V[:1], sure=300, link=["https://github.com/a/b"])
    s = Sahte()  # form bağlantı kararı içermiyor
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    assert len(s.cagrilar) == 3 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam_eksik"  # M2e K1: iki yeniden istekten sonra kısmi kabul
    assert "https://github.com/a/b" in s.cagrilar[1][1]


def test_short_toplu_tek_cagri_ayri_rapor_ayri_kayit(tmp_path):
    kok = _kurulum(tmp_path, V, sure=30)
    kayit = kok / "docs" / "video-tarama" / "kayit.jsonl"
    kayit.parent.mkdir(parents=True)
    kayit.write_bytes(b'{"id": "eskieskiesk", "tarih": "2026-01-01"}')  # sonda satır sonu yok; eski bayt değişmez
    s = Sahte()
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s)) == 0
    assert len(s.cagrilar) == 1 and sorted(s.cagrilar[0][0]) == sorted(V)
    for v in V:
        md = (kok / "docs" / "video-tarama" / f"2026-09-29-{v}.md").read_text(encoding="utf-8")
        assert tr.denetle(md, 30) == [] and f"https://youtu.be/{v}" in md
    satirlar = kayit.read_bytes().split(b"\n")
    assert satirlar[0] == b'{"id": "eskieskiesk", "tarih": "2026-01-01"}'
    assert [json.loads(x)["id"] for x in satirlar[1:] if x] == V


def test_mevcut_rapor_tamam_olarak_ice_alinir(tmp_path):
    kok = _kurulum(tmp_path, V[:2], sure=30)
    r = kok / "docs" / "video-tarama" / f"2026-09-28-{V[0]}.md"
    r.parent.mkdir(parents=True)
    r.write_text("# eski\n", encoding="utf-8")
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    assert s.cagrilar[0][0] == [V[1]] and r.read_text(encoding="utf-8") == "# eski\n"
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"


def test_tavan_asilinca_motor_durur(tmp_path):
    kok = _kurulum(tmp_path, V[:2], sure=300)
    s = Sahte()
    assert pt.parti(_ns("baslat", kok / "kuyruk.md", cagri_tavan=1), _ctx(kok, s)) == 3
    d = _durum(kok)
    assert len(s.cagrilar) == 1 and d["durum"] == "tavan" and d["videolar"][V[1]]["tarama"]["durum"] == "tavan"


def test_karar_bekleyeni_silmez_arsive_tasir(tmp_path):
    b = tmp_path / "docs" / "kurulumlar" / "bekleyen"
    b.mkdir(parents=True)
    (b / "sor-x.md").write_text("# SOR x\n\nsatır üç\n", encoding="utf-8")
    rc = cli.main(["karar", "x", "RED"], env={"VIDEO_UYGULA_KOK": str(tmp_path), "VIDEO_CACHE": str(tmp_path / "c")})
    a = b / "arsiv" / "sor-x.md"
    assert rc == 0 and not (b / "sor-x.md").exists() and a.is_file()
    assert a.read_text(encoding="utf-8").startswith("# SOR x\n") and "RED (Ömer)" in a.read_text(encoding="utf-8")
