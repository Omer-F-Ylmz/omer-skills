"""19 departmanlar: envanter (skill · plugin · MCP · köprü CLI) → Jev choice → docs/departmanlar/; müdür skill denetimi; katman."""
import json
from pathlib import Path

import pytest

from video import departman as dp
from video.cli import main

from test_uygula import UKos, aday, calis, kayit, kok, skill_klon  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

REPO = Path(__file__).resolve().parents[3]


class DJev:
    """choice: state'te FE → frontend 0.95 · GUV → guvenlik 0.92 · BELIRSIZ → surec-plan 0.5 · diğer → diger 0.9."""

    def __init__(self):
        self.istek = []

    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        s = g["state"]
        d, p = ("frontend", 0.95) if "FE" in s else ("guvenlik", 0.92) if "GUV" in s else ("surec-plan", 0.5) if "BELIRSIZ" in s else ("diger", 0.9)
        cv = {k: {"type": "choice", "choice": d, "probabilities": {d: p}, "confidence": p} for k in g["questions"]}
        return 200, {}, json.dumps({"answers": cv}).encode()


def skill_yaz(ev, ad, aciklama):
    s = ev / ".claude" / "skills" / ad
    s.mkdir(parents=True, exist_ok=True)
    (s / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: {aciklama}\n---\n# {ad}\n", encoding="utf-8")


@pytest.fixture
def dkok(ortam, tmp_path):
    k, ev = tmp_path / "repo", tmp_path / "ev"
    (k / "tools" / "cc-kopru").mkdir(parents=True)
    (k / "tools" / "cc-kopru" / "kopru.json").write_text(json.dumps({"izinli": {"gitleaks": {}, "_not11k": "x"}}), encoding="utf-8")
    cl = ev / ".claude"
    cl.mkdir(parents=True)
    pk = tmp_path / "eklenti"
    (pk / ".claude-plugin").mkdir(parents=True)
    (pk / ".claude-plugin" / "plugin.json").write_text(json.dumps({"description": "FE tasarım eklentisi"}), encoding="utf-8")
    (cl / "settings.json").write_text(json.dumps({"enabledPlugins": {"ekl@pazar": True, "kapali@pazar": False},
                                                  "skillOverrides": {"sonuk": "off"}}), encoding="utf-8")
    (cl / "plugins").mkdir()
    (cl / "plugins" / "installed_plugins.json").write_text(json.dumps({"plugins": {"ekl@pazar": [{"installPath": str(pk)}]}}), encoding="utf-8")
    (ev / ".claude.json").write_text(json.dumps({"mcpServers": {"figma": {"env": {"GIZLI": "deger"}}}}), encoding="utf-8")
    skill_yaz(ev, "fe-skill", "FE arayüz tasarımı")
    skill_yaz(ev, "guv-skill", "GUV güvenlik taraması")
    skill_yaz(ev, "bel-skill", "BELIRSIZ bir şey")
    skill_yaz(ev, "sonuk", "kapalı skill")
    ortam.update(VIDEO_UYGULA_KOK=str(k), VIDEO_EV=str(ev))
    return k


def calistir(ortam, jev, *ek):
    return main(["departman", *ek], env=ortam, gonder=jev)


def envanter(k):
    return json.loads((k / "docs" / "departmanlar" / "envanter.json").read_text(encoding="utf-8"))


def test_her_aktif_arac_tam_bir_departmanda(ortam, dkok, capsys):
    assert calistir(ortam, DJev()) == 0
    e = envanter(dkok)
    anahtar = [(x["tur"], x["ad"]) for x in e]
    assert sorted(anahtar) == sorted([("skill", "bel-skill"), ("skill", "fe-skill"), ("skill", "guv-skill"),
                                      ("plugin", "ekl"), ("mcp", "figma"), ("cli", "gitleaks")])  # kapalı plugin/skill, _not yok
    assert all(x["departman"] in dp.DEPARTMANLAR and set(x) >= {"ad", "tur", "departman", "p", "kaynak"} for x in e)
    assert "deger" not in (dkok / "docs" / "departmanlar" / "envanter.json").read_text(encoding="utf-8")  # MCP env değeri okunmaz
    out = capsys.readouterr().out
    assert "frontend 2" in out and "gözden geçir: 1" in out and "bel-skill" in out  # BELIRSIZ p 0.5 < act


def test_denetle_eksik_cift_bilinmeyen():
    araclar = [{"ad": "a", "tur": "skill"}, {"ad": "b", "tur": "mcp"}]
    assert dp.denetle(araclar, [{"ad": "a", "tur": "skill", "departman": "frontend"},
                                {"ad": "b", "tur": "mcp", "departman": "veri-db"}]) == []
    hata = dp.denetle(araclar, [{"ad": "a", "tur": "skill", "departman": "frontend"}, {"ad": "a", "tur": "skill", "departman": "surec"},
                                {"ad": "b", "tur": "mcp", "departman": "muhasebe"}])
    assert any("a" in h and "2" in h for h in hata) and any("muhasebe" in h for h in hata)
    assert any("b" in h and "0" in h for h in dp.denetle(araclar, [{"ad": "a", "tur": "skill", "departman": "frontend"}]))


def test_elle_json_jevi_ezer(ortam, dkok):
    d = dkok / "docs" / "departmanlar"
    d.mkdir(parents=True)
    (d / "elle.json").write_text(json.dumps({"fe-skill": "belge"}), encoding="utf-8")
    jev = DJev()
    assert calistir(ortam, jev) == 0
    x = next(x for x in envanter(dkok) if x["ad"] == "fe-skill")
    assert (x["departman"], x["kaynak"]) == ("belge", "elle")
    assert not any("fe-skill" in i["state"] for i in jev.istek)
    assert calistir(ortam, DJev(), "--yeniden") == 0  # yeniden sınıflamada da elle kazanır
    assert next(x for x in envanter(dkok) if x["ad"] == "fe-skill")["departman"] == "belge"


def test_sira_elle_desen_onbellek_jev(ortam, dkok, capsys):
    assert calistir(ortam, DJev()) == 0  # önbellek: guv-skill → guvenlik (jev)
    d = dkok / "docs" / "departmanlar"
    (d / "elle.json").write_text(json.dumps({"fe-skill": "belge"}), encoding="utf-8")
    (d / "elle-desen.json").write_text(json.dumps({"fe-*": "veri-db", "guv-*": "veri-db", "mcp:fig*": "belge"}), encoding="utf-8")
    jev = DJev()
    assert calistir(ortam, jev) == 0
    e = {x["ad"]: x for x in envanter(dkok)}
    assert (e["fe-skill"]["departman"], e["fe-skill"]["kaynak"]) == ("belge", "elle")  # elle > desen
    assert (e["guv-skill"]["departman"], e["guv-skill"]["kaynak"]) == ("veri-db", "desen")  # desen > önbellek
    assert (e["figma"]["departman"], e["figma"]["kaynak"]) == ("belge", "desen")  # tur:ad joker
    assert not any(a in i["state"] for i in jev.istek for a in ("fe-skill", "guv-skill", "figma"))  # desen > Jev
    assert calistir(ortam, DJev(), "--yeniden") == 0 and next(x for x in envanter(dkok) if x["ad"] == "guv-skill")["kaynak"] == "desen"
    assert "guv-skill" not in capsys.readouterr().out.split("gözden geçir:")[-1].splitlines()[0]  # desen gözden geçire düşmez


def test_desen_joker_eslesmesi():
    desen = {"design:*": "frontend", "*msbuild*": "backend-dotnet", "*security*": "guvenlik", "gstack-upgrade": "surec-ajan-arac"}
    bul = lambda ad, tur="skill": dp._desen(desen, {"ad": ad, "tur": tur})  # noqa: E731
    assert bul("design:ux-copy") == "frontend" and bul("dotnet-msbuild:eval-performance") == "backend-dotnet"
    assert bul("phoenix-security-review:0day-scanner") == "guvenlik" and bul("gstack-upgrade") == "surec-ajan-arac"
    assert bul("gstack") is None and bul("designer") is None


def test_eski_surec_kaydi_tasinir(ortam, dkok):
    d = dkok / "docs" / "departmanlar"
    d.mkdir(parents=True)
    eski = {"ad": "bel-skill", "tur": "skill", "aciklama": "BELIRSIZ bir şey", "departman": "surec", "p": 0.5, "kaynak": "jev"}
    (d / "envanter.json").write_text(json.dumps([{**eski, "hash": dp._hash("bel-skill", "BELIRSIZ bir şey")}]), encoding="utf-8")
    jev = DJev()
    assert calistir(ortam, jev) == 0
    assert any("bel-skill" in i["state"] for i in jev.istek)  # hash aynı ama departman artık yok → yeniden sorulur
    assert next(x for x in envanter(dkok) if x["ad"] == "bel-skill")["departman"] == "surec-plan"


def test_onbellek_hash_degismeden_yeniden_sormaz(ortam, dkok):
    assert calistir(ortam, DJev()) == 0
    jev = DJev()
    assert calistir(ortam, jev) == 0 and jev.istek == []
    skill_yaz(Path(ortam["VIDEO_EV"]), "guv-skill", "GUV güvenlik taraması, yeni açıklama")
    jev = DJev()
    assert calistir(ortam, jev) == 0
    assert [i["state"].split(" · ")[0] for i in jev.istek] == ["guv-skill"]
    jev = DJev()
    assert calistir(ortam, jev, "--yeniden") == 0 and len(jev.istek) == 6


def test_istek_tavani_aga_cikmadan(ortam, dkok, capsys):
    jev = DJev()
    assert calistir(ortam, jev, "--istek-tavan", "3") == 1
    assert jev.istek == [] and "istek tavanı" in capsys.readouterr().out


def test_katalog_yeniden_uretimde_elle_bolumu_korunur(ortam, dkok):
    assert calistir(ortam, DJev()) == 0
    y = dkok / "docs" / "departmanlar" / "frontend.md"
    metin = y.read_text(encoding="utf-8")
    assert "fe-skill" in metin and "| araç |" in metin and "## Elle" in metin
    y.write_text(metin.replace("## Elle\n", "## Elle\nÖmer notu: önce DESIGN.md\n"), encoding="utf-8")
    assert calistir(ortam, DJev(), "--yeniden") == 0
    assert "Ömer notu: önce DESIGN.md" in y.read_text(encoding="utf-8")


def test_katalog_sonraki_adim_mudur_sirasindan():
    mudur = "---\nname: departman-x\ndescription: x\n---\n1. **Tasarım** — `aa` ile\n2. **Yapım** — `bb`\n"
    assert dp.sonraki(mudur, "aa") == "Yapım" and dp.sonraki(mudur, "bb") == "-" and dp.sonraki(mudur, "cc") == "-"


def mudur(tmp_path, satir=10, aciklama="Frontend işi: tasarım → yapım. UI işinde önce yükle."):
    y = tmp_path / "departman-frontend" / "SKILL.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"---\nname: departman-frontend\ndescription: \"{aciklama}\"\n---\n" + "satır\n" * (satir - 4), encoding="utf-8")
    return y


def test_mudur_60_satir_ve_200_karakter(tmp_path):
    assert dp.mudur_denetle(mudur(tmp_path, 60)) == []
    assert any("61" in h for h in dp.mudur_denetle(mudur(tmp_path, 61)))
    assert any("201" in h for h in dp.mudur_denetle(mudur(tmp_path, aciklama="x" * 201)))


def test_repodaki_mudur_skilleri_sinirda():
    yollar = sorted(REPO.glob("skills/departman-*/SKILL.md"))
    assert REPO / "skills" / "departman-frontend" / "SKILL.md" in yollar
    assert {y.parent.name for y in yollar} >= {"departman-frontend", "departman-test-qa", "departman-guvenlik"}
    assert all(dp.mudur_denetle(y) == [] for y in yollar), {y.parent.name: dp.mudur_denetle(y) for y in yollar}
    fe = (REPO / "skills" / "departman-frontend" / "SKILL.md").read_text(encoding="utf-8").split("## Adımlar", 1)[1]
    assert fe.index("DESIGN.md") < fe.index("frontend-craft") < fe.index("axe")  # ana hat sırası
    assert "departman-test-qa" in fe and "departman-guvenlik" in fe


def test_surec_alt_departmanlara_bolunur():
    assert "surec" not in dp.DEPARTMANLAR
    assert {"surec-plan", "surec-inceleme", "surec-git-yayin", "surec-ajan-arac"} <= set(dp.DEPARTMANLAR)
    adlar = {y.parent.name for y in REPO.glob("skills/departman-*/SKILL.md")}
    assert "departman-surec" not in adlar
    e = json.loads((REPO / "docs" / "departmanlar" / "envanter.json").read_text(encoding="utf-8"))
    assert not [x["ad"] for x in e if x["departman"] not in dp.DEPARTMANLAR]  # hiçbir araç "surec"te kalmaz
    assert {f"departman-{m}" for m in dp.mudurler(e)} == adlar  # müdür yalnız ≥3 araçlı (alt) departmana


def test_frontend_mudur_yigin_dali_ve_performans():
    fe = (REPO / "skills" / "departman-frontend" / "SKILL.md").read_text(encoding="utf-8").split("## Adımlar", 1)[1]
    yigin = fe.index("Razor")
    assert "dotnet-aspnetcore" in fe[yigin:] and fe.index("vercel-composition-patterns") > yigin and "Astro" in fe
    assert yigin < fe.index("21st-ui")  # yığın dalı referans/bileşen adımından önce
    perf = fe.index("fixing-motion-performance")
    assert fe.index("axe") < perf < fe.index("pixeljury") and "performance-optimization" in fe and "Lighthouse" in fe
    assert all(a in fe for a in ("claude-design", "figma", "stitch", "scroll-craft", "web-sahne-desenleri"))
    assert fe.index("DESIGN.md") < fe.index("claude-design")  # tuval DESIGN.md'den sonra
    e = {x["ad"].split(":")[-1] for x in json.loads((REPO / "docs" / "departmanlar" / "envanter.json").read_text(encoding="utf-8"))}
    k3 = {"dotnet-aspnetcore", "vercel-react-best-practices", "vercel-composition-patterns", "fixing-motion-performance",
          "performance-optimization", "claude-design", "figma", "stitch", "web-sahne-desenleri", "scroll-craft"}
    assert k3 <= e and "high-end-visual-design" not in fe, k3 - e  # yalnız envanterdeki adlar


def test_uc_arac_kurali():
    e = [{"departman": d} for d in ["frontend"] + ["guvenlik"] * 3 + ["belge"] * 2 + ["diger"] * 5]
    assert dp.mudurler(e) == {"frontend", "guvenlik"}  # frontend daima, diger hiç, belge 2 < 3


def test_uc_arac_kurali_komutta_fazla_mudur(ortam, dkok, capsys):
    mudur(dkok / "skills")
    (dkok / "skills" / "departman-belge").mkdir(parents=True)
    (dkok / "skills" / "departman-belge" / "SKILL.md").write_text("---\nname: departman-belge\ndescription: x\n---\n", encoding="utf-8")
    assert calistir(ortam, DJev()) == 1  # belge 0 araç: müdür fazla
    assert "departman-belge fazla" in capsys.readouterr().out


def test_description_token_toplami_600_alti(tmp_path):
    mudur(tmp_path / "skills")
    assert 0 < dp.aciklama_token(tmp_path) < 50
    assert 0 < dp.aciklama_token(REPO) <= 600


def test_katman_yeni_araca_departman_yazar(ortam, kok, tmp_path, capsys):
    repo, s = skill_klon(tmp_path, "scriptli", "kur.sh")
    y = aday(kok, "scriptli", kaynak=s)
    y.write_text(y.read_text(encoding="utf-8").replace("## Ne\ndeneme", "## Ne\nFE bileşen kütüphanesi"), encoding="utf-8")
    jev = DJev()
    assert calis(ortam, [y], UKos(repo), gonder=jev) == 0
    assert kayit(kok)[-1]["departman"] == "frontend"
    x = next(x for x in envanter(kok) if x["ad"] == "scriptli")
    assert (x["departman"], x["kaynak"]) == ("frontend", "katman")
    assert "scriptli" in (kok / "docs" / "departmanlar" / "frontend.md").read_text(encoding="utf-8")
    rapor = next((kok / "docs" / "kurulumlar").glob("*-uygula.md"))
    assert main(["brief", str(rapor)], env=ortam) == 0
    assert "scriptli → frontend" in capsys.readouterr().out
