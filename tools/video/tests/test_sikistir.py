"""23c araştırıcı-sıkıştır: getir/repo üst sınırları · araştırıcıda WebFetch yok · kayit.jsonl append-only · departmansız satır kalmaz ·
prompt anatomisi zorunlu · site prompt kütüphanesinde video+zaman zorunlu · kural-onay kapsamsız olmaz. Ağsız."""
import json
from pathlib import Path

import pytest

from video import getir as g
from video import tarama as tr
from video import uygula as uy
from video.cli import main

from test_tarama import TaramaJev, dizin, kayit_yaz, rapor  # noqa: F401 (dizin fixture)
from test_uygula import kok  # noqa: F401 (kok fixture)
from test_video import VID, Kos, ortam  # noqa: F401 (ortam fixture)

REPO = Path(__file__).resolve().parents[3]
HTML = ("<html><head><title>Başlık</title><script>kod()</script></head><body><nav>MENÜ</nav><header>ÜST</header>"
        "<main><p>" + "a" * 9000 + "</p><a href='/x'>x</a></main><footer>ALTBİLGİ</footer></body></html>")
ANATOMI = """## Prompt anatomisi
bolumler: hero, galeri, iletişim
hareket: scroll reveal, stagger, parallax
teknoloji: Three.js r160, GSAP 3.12, Lenis 1.1, Vite 5
dosya: main.js sahne · style.css tipografi · config.js parametreler
config: CONFIG nesnesi (helezon yarıçapı, kart sayısı)
asset: 12 dikey fotoğraf, koyu arka plan
kabul: 60 fps, mobil 390px taşma yok
### Kalıplar
- teknolojiyi sürümüyle say, dosya başına sorumluluk yaz · 2:01 · teknik: helezon galeri · şablon: dosya
- tüm ayarları tek CONFIG nesnesinde topla · 2:05 · teknik: helezon galeri · şablon: yok
"""


def _aday(kok, ad, govde, tur="prompt"):
    y = kok / "docs" / "kurulumlar" / "adaylar" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"# {ad}\nad: {ad}\ntur: {tur}\nvideo: {VID}\n## Ne\nsite yapım promptu\n{govde}", encoding="utf-8")
    return y


# --- K2 getir / repo ---

def test_getir_ana_metin_ust_sinir_kesildi(tmp_path):
    out = g.getir("https://s.test/p", al=lambda u: HTML, cache=tmp_path)
    assert out.startswith("# Başlık") and "https://s.test/x" in out
    assert not any(x in out for x in ("MENÜ", "ÜST", "ALTBİLGİ", "kod()"))
    assert "…(kesildi: 3002 karakter)" in out and len(out) < 6400

    def yok(u):
        raise OSError("ağ yok")
    assert g.getir("https://s.test/p", al=yok, cache=tmp_path) == out  # önbellek


def test_repo_readme_agac_satir_araligi():
    def kos(args, timeout=120, env=None):
        s = " ".join(args)
        if "/readme" in s:
            return 0, "\n".join(f"r{i}" for i in range(300)).encode(), b""
        if "/git/trees/" in s:
            return 0, "\n".join(["a", "a/b", "a/b/c", "d"]).encode(), b""
        return 0, "\n".join(f"s{i}" for i in range(1, 501)).encode(), b""
    out = g.repo("o/r", kos=kos)
    assert "r119" in out and "r120" not in out and "…(kesildi: 180 satır)" in out
    assert "a/b" in out and "a/b/c" not in out
    d = g.repo("o/r", dosya="src/x.js", satir="1-500", kos=kos)
    assert "s200" in d and "s201" not in d and "…(kesildi: 300 satır)" in d


# --- K3 araştırıcı ---

def test_arastirici_webfetch_yok_butce_var():
    m = (REPO / ".claude" / "agents" / "aday-arastirici.md").read_text(encoding="utf-8")
    tools = next(s for s in m.splitlines() if s.startswith("tools:"))
    assert "WebFetch" not in tools and "WebSearch" in tools
    assert "video getir" in m and "video repo" in m and "on.md" in m and "≤12 araç" in m


# --- K5 append-only ---

def test_kayit_ekle_eski_bayt_korunur(tmp_path):
    y = tmp_path / "kayit.jsonl"
    y.write_text(json.dumps({"ad": "a"}), encoding="utf-8")  # sonunda satır sonu yok
    eski = y.read_bytes()
    tr.kayit_ekle(y, [{"ad": "b"}])
    assert y.read_bytes().startswith(eski) and [k["ad"] for k in tr.kayit_oku(y)] == ["a", "b"]


def test_toplu_eski_satiri_silmez(ortam, dizin, capsys):
    kayit_yaz(dizin, VID)
    eski = (dizin / "kayit.jsonl").read_bytes()
    r = dizin / f"2026-09-23-{VID}.md"
    r.write_text(rapor(), encoding="utf-8")
    ortam["VIDEO_EV"] = str(dizin / "ev")
    assert main(["toplu", str(r)], env=ortam, kos=Kos(), gonder=TaramaJev()) == 0
    assert (dizin / "kayit.jsonl").read_bytes().startswith(eski)
    assert [k["id"] for k in tr.kayit_oku(dizin / "kayit.jsonl")] == [VID, VID]


def test_departman_geri_islem_kaydi_ekler(ortam, kok, capsys):
    ky = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.parent.mkdir(parents=True, exist_ok=True)
    ky.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in [
        {"ad": "caveman/x", "aday": "caveman", "yargi": "DENE", "departman": "verimlilik"},
        {"ad": "caveman-oz", "karar": "RED(token)"}, {"ad": "yalniz", "karar": "KUR"}]), encoding="utf-8")
    eski = ky.read_bytes()
    assert main(["departman-geri"], env=ortam) == 0
    assert ky.read_bytes().startswith(eski)
    son = tr.kayit_son(tr.kayit_oku(ky))
    assert all(k.get("departman") for k in son.values())
    assert son["caveman-oz"]["departman"] == "verimlilik" and son["yalniz"]["departman"].startswith("uygulanamaz")
    assert son["caveman-oz"]["karar"] == "RED(token)"


# --- K7 prompt anatomisi ---

def test_prompt_adayi_anatomisiz_denetimden_gecmez(ortam, kok, capsys):
    y = _aday(kok, "p", "")
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    assert "Prompt anatomisi" in capsys.readouterr().out
    y = _aday(kok, "p", ANATOMI.replace("hareket: scroll reveal, stagger, parallax\n", ""))
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    y = _aday(kok, "p", ANATOMI)
    assert main(["rapor-denetle", str(y)], env=ortam) == 0


def test_kutuphane_video_zaman_zorunlu(kok):
    with pytest.raises(ValueError):
        uy.kutuphane_ekle(kok, [{"kalip": "x", "video": "", "zaman": "2:01", "teknik": "-", "sablon": "yok"}])
    with pytest.raises(ValueError):
        uy.kutuphane_ekle(kok, [{"kalip": "x", "video": VID, "zaman": "", "teknik": "-", "sablon": "yok"}])


def test_prompt_isle_kutuphane_ve_uyarla(kok):
    s = kok / "skills" / "departman-frontend" / "SKILL.md"
    s.parent.mkdir(parents=True, exist_ok=True)
    s.write_text("# x\n## Yapım promptu şablonu\n- dosya: dosya başına sorumluluk\n", encoding="utf-8")
    y = _aday(kok, "p", ANATOMI)
    say = uy.prompt_isle(kok, "p", y.read_text(encoding="utf-8"))
    assert say == {"ZATEN VAR": 1, "UYARLA": 1}
    kut = (kok / "docs" / "departmanlar" / "frontend-promptlar.md").read_text(encoding="utf-8")
    assert f"| {VID} | 2:01 |" in kut and "tüm ayarları tek CONFIG" in kut
    assert (kok / "docs" / "kurulumlar" / "bekleyen" / "prompt-tum-ayarlari-tek-config-nesnesinde-topla.md").is_file()
    uy.prompt_isle(kok, "p", y.read_text(encoding="utf-8"))  # ikinci koşu çift satır eklemez
    assert (kok / "docs" / "departmanlar" / "frontend-promptlar.md").read_text(encoding="utf-8").count("2:01") == 1


# --- K6 kapsam ---

def test_kural_onay_kapsamsiz_olmaz(ortam):
    with pytest.raises(SystemExit):
        main(["kural-onay", "x"], env=ortam)
