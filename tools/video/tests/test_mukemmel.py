"""23 video-mükemmel: ajan-denetle · her özelliğe departman · kural çifti fixture + kavram desteği · Site/UI teknikleri · Mekanizma teknik."""
import json
from pathlib import Path

from video import tarama as tr, uygula as uy
from video.cli import main

from test_derin import kayit, ozellikli, uygula_raporu
from test_tarama import SahteTas, rapor
from test_uygula import UKos, calis, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

REPO = Path(__file__).resolve().parents[3]
FIX = json.loads((Path(__file__).parent / "fixture" / "kural-cifti.json").read_text(encoding="utf-8"))


# --- K1 ajan-denetle ---

def _ajan(kok, ad, model="sonnet", tools="Bash, Read"):
    y = kok / ".claude" / "agents" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"---\nname: {ad}\ndescription: x\nmodel: {model}\ntools: {tools}\n---\ngövde\n", encoding="utf-8")


def _skill(kok, metin):
    y = kok / "skills" / "video-s" / "SKILL.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(metin, encoding="utf-8")


def test_ajan_denetle_olmayan_tip_hata(ortam, kok, capsys):
    _ajan(kok, "var-ajan")
    _skill(kok, "Agent (subagent_type: var-ajan) ve Agent (subagent_type: yok-ajan)\n")
    assert main(["ajan-denetle"], env=ortam) == 1
    out = capsys.readouterr().out
    assert "yok-ajan" in out and "var-ajan:" not in out


def test_ajan_denetle_model_ve_tools(ortam, kok, capsys):
    _ajan(kok, "pahali", model="opus")
    _ajan(kok, "genis", tools="*")
    _skill(kok, "subagent_type: pahali · subagent_type: genis\n")
    assert main(["ajan-denetle"], env=ortam) == 1
    out = capsys.readouterr().out
    assert "pahali: model" in out and "genis: tools" in out


def test_ajan_denetle_gercek_repo_ve_dusme_yasagi(ortam):
    assert main(["ajan-denetle"], env={**ortam, "VIDEO_UYGULA_KOK": str(REPO)}) == 0
    for s in ("video-uygula", "video-tarama"):
        assert "general-purpose'a DÜŞME" in (REPO / "skills" / s / "SKILL.md").read_text(encoding="utf-8")


# --- K2 departman ---

def _elle(kok, **d):
    y = kok / "docs" / "departmanlar" / "elle.json"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(json.dumps(d), encoding="utf-8")


def test_her_ozellige_ve_adaya_departman(ortam, kok, capsys):
    _elle(kok, arac="verimlilik", eski="frontend")
    y = ozellikli(kok, "arac",
                  {"slug": "a", "ne": "x", "etiket": "-", "karar": "RED", "gerekce": "lisans: yok"},
                  {"slug": "b", "ne": "y", "etiket": "-", "karar": "ZATEN VAR", "gerekce": "zaten var: graphify"},
                  {"slug": "c", "ne": "z", "etiket": "-", "karar": "DENE", "metrik": "süre"})
    z = kok / "docs" / "kurulumlar" / "adaylar" / "eski.md"
    z.write_text(f"# eski\nad: eski\ntur: CLI\nvideo: {VID}\nkarar: ZATEN VAR\ngerekce: zaten var: graphify\n## Ne\neski araç\n", encoding="utf-8")
    assert calis(ortam, [y, z], UKos()) == 0
    k = kayit(kok)
    assert all(k[a].get("departman") == "verimlilik" for a in ("arac/a", "arac/b", "arac/c")), k
    assert k["eski"].get("departman") == "frontend"
    dep = tr.bolum(uygula_raporu(kok), "DEPARTMAN")
    assert "arac → verimlilik" in dep and "eski → frontend" in dep
    kat = (kok / "docs" / "departmanlar" / "verimlilik.md").read_text(encoding="utf-8")
    assert "## Videodan gelen" in kat and "arac/a · RED" in kat and VID in kat
    ej = kok / "docs" / "departmanlar" / "envanter.json"
    envanter = json.loads(ej.read_text(encoding="utf-8")) if ej.is_file() else []
    assert not any(e["ad"] in ("arac", "eski") for e in envanter)  # KUR/UYARLA olmayan envantere girmez
    capsys.readouterr()
    r = next((kok / "docs" / "kurulumlar").glob("*-uygula.md"))
    assert main(["brief", str(r)], env=ortam) == 0
    assert "arac → verimlilik" in capsys.readouterr().out


def test_departman_geri_dosyalar(ortam, kok, capsys):
    _elle(kok, caveman="verimlilik")
    ky = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.parent.mkdir(parents=True, exist_ok=True)
    ky.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in [
        {"ad": "caveman/compress", "aday": "caveman", "ozellik": "compress", "yargi": "DENE", "karar": "d", "video": VID},
        {"ad": "caveman/skill", "aday": "caveman", "ozellik": "skill", "yargi": "RED", "karar": "r", "video": VID}]), encoding="utf-8")
    assert main(["departman-geri"], env=ortam) == 0
    assert all(x["departman"] == "verimlilik" for x in map(json.loads, ky.read_text(encoding="utf-8").splitlines()))
    kat = (kok / "docs" / "departmanlar" / "verimlilik.md").read_text(encoding="utf-8")
    assert "caveman/compress · DENE" in kat and "caveman/skill · RED" in kat
    assert "geri dosyalanan: 2" in capsys.readouterr().out


# --- K3 kural çifti ---

def test_fixture_bilinen_7_cift_ve_yanlis_pozitif():
    assert len(FIX["cift"]) == 7 and FIX["degil"]
    assert FIX["cift"][0]["beklenen"] == ["omer-kurallar:13", "CLAUDE:14"]


KL = [("omer-kurallar:13", "Context disiplini: keşifte önce graphify query; dosya yalnız kanıt satırı için açılır; verbose iş sonnet alt ajana."),
      ("omer-kurallar:3", "Yeterli bilgi varsa devam edeyim mi diye sormadan işi sonuna kadar götür.")]


def test_kavram_ortusmesi_esigi_04e_indirir():
    t = SahteTas({"omer-kurallar:13": 0.8, "hiçbiri": 0.1}, 0.45)
    assert tr.kural_esle(t, FIX["cift"][0]["state"], KL) == "omer-kurallar:13"


def test_ortusme_yoksa_esik_05_kalir():
    t = SahteTas({"omer-kurallar:3": 0.8, "hiçbiri": 0.1}, 0.45)
    assert tr.kural_esle(t, "İPUCU: Negatif prompt yazma\nipucu: istemde yapılmayacakları yaz", KL) is None


def test_yanlis_pozitif_fixture_cift_olmaz():
    for d in FIX["degil"]:
        t = SahteTas({d["kural"][0]: 0.8, "hiçbiri": 0.1}, 0.45)
        assert tr.kural_esle(t, d["state"], KL + [tuple(d["kural"])]) is None


def test_kural_regresyon_sayar():
    class Esle:  # state'teki fixture adına göre beklenen ilk etiketi seçer, degil'de kendi kuralını
        def yargila(self, states, q):
            s = states[0]
            if all(k.startswith("d") for k in q):
                x = next((c["beklenen"][0] for c in FIX["cift"] if c["state"] == s), None) or next(d["kural"][0] for d in FIX["degil"] if d["state"] == s)
                return [{k: {"type": "choice", "probabilities": {x: 0.9, "hiçbiri": 0.1}} for k in q}]
            return [{k: {"type": "noul", "noul": 0.3 if "paralellik" in json.dumps(q, ensure_ascii=False) else 0.6} for k in q}]
    r = tr.kural_regresyon(Esle(), FIX, KL)
    assert (len(r["bulunan"]), r["kacan"], r["yp"]) == (7, [], [])


# --- K5 Site/UI teknikleri ---

FRONT = "## Özet\nLanding page sitesi yapımı: GSAP ile scroll animasyonu, Tailwind grid ve tipografi.\n"
SITE = ("## Site/UI teknikleri\n| teknik | kanıt | kütüphane/araç | bizde |\n|---|---|---|---|\n"
        "| kaydırmaya bağlı animasyon | 1:40 altyazı “scroll ile döner” | {kut} | scroll-craft |\n")


def _front(kut=None):
    m = rapor().replace("## Özet\n", FRONT, 1)
    return m if kut is None else m.replace("## Kareden okunanlar", SITE.format(kut=kut) + "## Kareden okunanlar", 1)


def test_frontend_raporda_site_ui_zorunlu():
    assert "bölüm eksik: ## Site/UI teknikleri" in tr.denetle(_front(), 300)
    assert tr.denetle(rapor(), 300) == []  # frontend olmayan video: bölüm istenmez


def test_tahmin_isaretsiz_kutuphane_hata():
    assert any("tahmin" in x for x in tr.denetle(_front("GSAP ScrollTrigger"), 300))
    assert tr.denetle(_front("tahmin: GSAP ScrollTrigger"), 300) == []


def test_teknik_ogren_ve_uyarla(ortam, kok, capsys):
    r = kok / "docs" / "video-tarama" / "r.md"
    r.parent.mkdir(parents=True, exist_ok=True)
    r.write_text(_front("tahmin: GSAP").replace(
        "| scroll-craft |\n", "| scroll-craft |\n| helezon galeri | 2:10 kare x.jpg | - | yok |\n", 1), encoding="utf-8")
    assert main(["teknik", str(r)], env=ortam) == 0
    kart = (kok / "bilgi" / "kaydirmaya-bagli-animasyon.md").read_text(encoding="utf-8")
    assert "frontend" in kart and "scroll-craft" in kart
    b = (kok / "docs" / "kurulumlar" / "bekleyen" / "teknik-helezon-galeri.md").read_text(encoding="utf-8")
    assert "departman-frontend" in b and "omer-kutuphaneler" in b
    kat = (kok / "docs" / "departmanlar" / "frontend.md").read_text(encoding="utf-8")
    assert "## Teknikler" in kat and "kaydırmaya bağlı animasyon · ÖĞREN" in kat and "helezon galeri · UYARLA" in kat


def test_tarayici_talimati_site_ui():
    t = (REPO / ".claude" / "agents" / "video-tarayici.md").read_text(encoding="utf-8")
    assert "## Site/UI teknikleri" in t and "tahmin" in t


# --- K4 Mekanizma ---

def test_teknik_etiketli_ozellik_mekanizmasiz_hata():
    m = "# a\nad: a\n## Özellikler\n### kaydir\nne: yumuşak kaydırma\netiket: teknik\nkarar: ÖĞREN\n"
    assert any("kaydir" in x for x in uy.mekanizma_denetle(m))


def test_arastirici_teknik_mekanizma_talimati():
    t = (REPO / ".claude" / "agents" / "aday-arastirici.md").read_text(encoding="utf-8")
    assert "Token ya da teknik etiketli her özellik" in t and "GEÇTİ olmadan dönme" in t
