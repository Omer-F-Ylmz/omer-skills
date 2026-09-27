"""KURULUM-24a hat-düzeltme: yarım araştırma · prompt metni on.md · yeniden→kural-onay · teknik≠araç · rapor ezilmez ·
uyarlama alanları · brief tarama raporu · işlevsel eşdeğer. Ağsız; Jev sahte `gonder`."""
import json

from video import cli
from video import getir as gt
from video import uygula as uy
from video.cli import main

from test_ogren import OJev
from test_uygula import UKos, aday, calis, kayit, kok, kurallar  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

TOKEN_OZ = "## Özellikler\n### sikistir\nne: x\netiket: token\nkarar: DENE\ngerekce: -\n"


def _yaz(kok, ad, govde):
    y = kok / "docs" / "kurulumlar" / "adaylar" / f"{ad}.md"
    y.write_text(govde, encoding="utf-8")
    return y


def _elle(kok, **dep):
    d = kok / "docs" / "departmanlar"
    d.mkdir(parents=True, exist_ok=True)
    (d / "elle.json").write_text(json.dumps(dep), encoding="utf-8")
    return d


# K1 yarım araştırma: geçerli ama işaretli, DENE verilmez
def test_yarim_arastirma_denetimden_isaretli_gecer(tmp_path, capsys):
    y = tmp_path / "a.md"
    y.write_text(f"# a\nad: a\narastirma: yarım: tur tavanı: Mekanizma araştırılamadı\n{TOKEN_OZ}", encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env={"VIDEO_CACHE": str(tmp_path)}) == 0
    assert "yarım" in capsys.readouterr().out
    y.write_text(f"# a\nad: a\n{TOKEN_OZ}", encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env={"VIDEO_CACHE": str(tmp_path)}) == 1


def test_yarim_arastirmada_dene_verilmez(tmp_path):
    o = {"ozellik": "sikistir", "etiket": "token", "karar": "DENE"}
    assert uy.ozellik_karar(o, {"arastirma": "yarım: tur tavanı"}, "", tmp_path, {})[0] == "ÖĞREN"
    assert uy.ozellik_karar(o, {}, "", tmp_path, {})[0] == "DENE"


# K2 prompt metni on.md'ye
def test_on_prompt_metni_rapor_ve_altyazidan(tmp_path):
    rapor = tmp_path / "r.md"
    rapor.write_text("# v\n## Bölümler\n- 0:00 Giriş\n- 1:00 Prompt\n- 2:00 Kapanış\n## Adaylar\n| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |\n"
                     "|---|---|---|---|---|---|---|\n| galeri promptu | yok | prompt | yok | site kurar | 1:00 | kare: DESIGN TOKENS |\n"
                     "| x | yok | CLI | yok | y | 0:10 | z |\n", encoding="utf-8")
    seg = tmp_path / "segmentler.jsonl"
    seg.write_text("\n".join(json.dumps({"i": i, "bas": b, "son": b + 30, "metin": [m]}) for i, (b, m) in enumerate(
        [(0, "merhaba"), (60, "Build a 3D ring gallery " + "x" * 5000), (130, "abone olun")])), encoding="utf-8")
    y = gt.on(tmp_path, VID, "galeri", rapor=rapor, seg=seg)
    m = y.read_text(encoding="utf-8")
    assert "## Prompt metni" in m and "1:00" in m and "DESIGN TOKENS" in m and "Build a 3D ring gallery" in m
    assert "kesildi" in m and "abone olun" not in m and "merhaba" not in m


# K3 yeniden → kural-onay
def test_yeniden_kural_dosyasi_kural_onay_ile_uyumlu(ortam, kok, capsys):
    bk = kok / "docs" / "kurulumlar" / "bekleyen"
    cli._kural_bekleyen(bk, {"ad": "Soruları tek mesajda topla", "not": "tek tur", "video": VID}, "yeniden:2026-09-28")
    slug = cli._slug("Soruları tek mesajda topla")
    assert main(["kural-onay", slug, "--kapsam", "genel"], env=ortam) == 0
    assert "madde eklendi" in capsys.readouterr().out


# K4 teknik/kavram araç değil
def test_teknik_aday_lisans_kapisina_girmez(ortam, kok):
    _elle(kok, **{"design-system-ui-kit-paneli": "frontend"})
    y = _yaz(kok, "design-system-ui-kit-paneli", "# design-system-ui-kit-paneli\nad: design-system-ui-kit-paneli\ntur: teknik\n"
             f"video: {VID}\nkural: Design System paneli — token ve bileşen inceleme\n## Ne\nTasarım token'larını inceleme\n")
    assert not uy.arac_mu(uy.alanlar(y.read_text(encoding="utf-8")), y.read_text(encoding="utf-8"))
    calis(ortam, [y], UKos(), OJev(tur="olgu"))
    k = kayit(kok)[-1]
    assert k["yargi"] == "ÖĞREN" and "lisans" not in k["karar"]


def test_arac_mu_kurulabilir_paket():
    assert uy.arac_mu({"tur": "CLI", "repo": "o/r"}, "")
    assert uy.arac_mu({"tur": "skill", "repo": "yok"}, "## Kurulum\n- npm: x@1\n")
    assert not uy.arac_mu({"tur": "skill", "repo": "yok"}, "## Kurulum\n\n")
    assert not uy.arac_mu({"tur": "iş akışı", "repo": "o/r"}, "")


# K5 aynı gün ikinci koşu raporu ezmez
def _hazir(kok, ad):
    return _yaz(kok, ad, f"# {ad}\nad: {ad}\ntur: CLI\nvideo: {VID}\nkarar: ZATEN VAR\ngerekce: zaten var: x\n## Ne\nbir iş\n")


def test_ikinci_kosu_raporu_ezmez(ortam, kok):
    _elle(kok, a1="diger", a2="diger")
    calis(ortam, [_hazir(kok, "a1")], UKos(), OJev())
    calis(ortam, [_hazir(kok, "a2")], UKos(), OJev())
    r = next((kok / "docs" / "kurulumlar").glob("*-uygula.md")).read_text(encoding="utf-8")
    assert "## a1 → ZATEN VAR" in r and "## Koşu 2" in r and "## a2 → ZATEN VAR" in r
    assert r.index("## a1") < r.index("## Koşu 2") < r.index("## a2")


# K6 uyarlama alanları aday.md'den (Parti A iki örnek)
NYNS = {"ozellik": "scroll-mouse-parallax-rotasyon", "ne": "scroll ve mouse ile ring döner", "etiket": "teknik", "karar": "UYARLA",
        "gerekce": "fikir: scroll/mouse olaylarını tek ortak açı fonksiyonuna (angleOf) bağlamak · hedef: departman-frontend prompt şablonu notu · kod yazılmaz"}
JGJ0 = {"ozellik": "tek-prompt-e-ticaret-sitesi", "ne": "tek promptla e-ticaret sitesi", "etiket": "teknik", "karar": "UYARLA",
        "gerekce": "kurulacak araç değil; fikir (asset+sıfat kısıtlı tek prompt kalıbı) kendi frontend-craft akışımıza aktarılabilir, kod yazılmaz."}


def test_uyarlama_alanlari_doldurulur_uretilebilir(tmp_path):
    for s in ("frontend-craft", "departman-frontend"):
        (tmp_path / "skills" / s).mkdir(parents=True)
    for o, ad in ((NYNS, "nyns"), (JGJ0, "jgj0")):
        al = uy.uyarla_alan(tmp_path, o)
        assert al["hedef_tur"] == "skill", ad
        uy.uyarla_yaz(tmp_path, o, ad)
        m = (tmp_path / "docs" / "uyarlamalar" / f"{ad}.md").read_text(encoding="utf-8")
        assert "\n?\n" not in m and "aday.md'de yok" in m, ad
    assert "angleOf" in uy.uyarla_alan(tmp_path, NYNS)["fikir"] and "departman-frontend" in uy.uyarla_alan(tmp_path, NYNS)["hedef"]
    assert "frontend-craft" in uy.uyarla_alan(tmp_path, JGJ0)["hedef"] and uy.uyarla_alan(tmp_path, JGJ0)["fikir"] == JGJ0["ne"]


# K7 brief tarama raporunun bölümlerini okur
TARAMA = f"""# Video
## Künye
X · https://youtu.be/{VID}
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| galeri promptu | yok | prompt | yok | 3D galeri kurar | 6:14 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Site of the Day seçildi | 0:30 | sayısal |
## Site/UI teknikleri
| teknik | kanıt | kütüphane/araç | bizde |
|---|---|---|---|
| ring galeri | 6:14 kare | three.js | yok |
## Belirsizlikler
- yok
"""


def test_brief_tarama_raporu_bos_bolum_birakmaz(ortam, kok, capsys):
    r = kok / "r.md"
    r.write_text(TARAMA, encoding="utf-8")
    (kok / "docs" / "kurulumlar" / "kayit.jsonl").write_text(json.dumps(
        {"ad": "galeri/ring", "aday": "galeri", "yargi": "UYARLA", "karar": "u", "video": VID, "departman": "frontend"}) + "\n", encoding="utf-8")
    _yaz(kok, "galeri", f"# galeri\nad: galeri\ntur: prompt\nvideo: {VID}\n## Prompt anatomisi\nbolumler: hero\n### Kalıplar\n"
         "- dosya yapısını tekrarla · 4:42 · teknik: yok · şablon: dosya\n")
    assert main(["brief", str(r)], env=ortam) == 0
    out = capsys.readouterr().out.splitlines()
    bas = [i for i, s in enumerate(out) if s.startswith("## ")]
    assert all(i + 1 < len(out) and not out[i + 1].startswith("## ") for i in bas), out
    t = "\n".join(out)
    for x in ("galeri promptu", "Site of the Day", "ring galeri", "frontend", "dosya yapısını tekrarla"):
        assert x in t, x


# K8 işlevsel eşdeğer ZATEN VAR
ENV = [{"ad": "anthropic-skills:skill-ui-cli", "tur": "skill", "departman": "surec-ajan-arac", "aciklama": "discover list install skills from repos"},
       {"ad": "cli-skill-collector", "tur": "skill", "departman": "surec-ajan-arac", "aciklama": "collect and install agent skills"},
       {"ad": "hookify", "tur": "plugin", "departman": "surec-ajan-arac", "aciklama": "hook rules"},
       {"ad": "frontend-craft", "tur": "skill", "departman": "frontend", "aciklama": "install skills ui"}]


def _skills_cli(kok):
    d = _elle(kok, **{"skills-cli": "surec-ajan-arac"})
    (d / "envanter.json").write_text(json.dumps(ENV), encoding="utf-8")
    return _yaz(kok, "skills-cli", f"# skills-cli\nad: skills-cli\ntur: CLI\nvideo: {VID}\nrepo: vercel-labs/skills\nlisans: MIT\n"
                "## Ne\nrepolardan tek komutla agent skill kurar ve install eder\n## Özellikler\n### skill-kurma\nne: skill kurar\nkarar: KUR\ngerekce: yeni\n")


def test_esdeger_varsa_zaten_var(ortam, kok):
    j = OJev(secim=[("ana işini", "anthropic-skills:skill-ui-cli")])
    calis(ortam, [_skills_cli(kok)], UKos(), j)
    k = kayit(kok)[-1]
    assert k["yargi"] == "ZATEN VAR" and "skill-ui-cli" in k["karar"]
    q = next(q for g in j.istek for q in g["questions"].values() if "ana işini" in q.get("instructions", ""))
    assert {"anthropic-skills:skill-ui-cli", "cli-skill-collector", "yok"} <= set(q["criteria"]) and "frontend-craft" not in q["criteria"]
    assert len(q["criteria"]) <= 6


def test_esdeger_yoksa_kur_kalir_sinirda_isaret(ortam, kok):
    calis(ortam, [_skills_cli(kok)], UKos(), OJev(secim=[("ana işini", "yok")]))
    assert kayit(kok)[-1]["yargi"] == "KUR"
    calis(ortam, ["--yeniden", _skills_cli(kok)], UKos(), OJev(secim=[("ana işini", {"cli-skill-collector": 0.5, "yok": 0.5})]))
    k = kayit(kok)[-1]
    assert k["yargi"] == "KUR" and "işaret" in k["karar"] and "cli-skill-collector" in k["karar"]
