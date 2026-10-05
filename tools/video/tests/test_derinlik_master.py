"""DERİNLİK-MASTER (docs/video-tarama/derinlik-plan.md) maddeleri."""
import json

from test_derinlik2 import PID, _kos, _lisans_satiri, _uyku
from test_m2a import _ns
from test_m2c import Ar, _ctx, _panel

from video import parti as pt


def _gh_a2():
    def gh(args):
        gh.cagrilar.append(args[1])
        if "search/repositories" in args:
            return {"items": []}
        if args[1].endswith("/license"):
            return {"license": {"spdx_id": "Apache-2.0"}}
        if "/commits?" in args[1]:
            return [{"sha": "f00", "commit": {"committer": {"date": "2026-09-30T10:00:00Z"}}}]
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


# A2 (=Y2) --yeniden: önceki aday yeniden araştırılmaz; Kapsam'daki çağrısız eksikler (lisans API, son commit, koşmamış güvenlik) tamamlanır
def test_a2_yeniden_onceki_eksik_kapsam_tamamlanir(tmp_path):
    _kos(tmp_path, [("ajan-k", "plugin", None)], None,
         Ar({"ajan-k": {"repo_url": "https://github.com/o/ajan-k", "lisans": "bilinmiyor", "son_commit": None}}))
    y = next(tmp_path.rglob("durum.json"))
    d = json.loads(y.read_text(encoding="utf-8"))
    d["adaylar"]["ajan-k"]["guvenlik"] = "koşmadı: klon başarısız (ağ)"
    y.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    gh, ar, ns = _gh_a2(), Ar({}), _ns("akil", y.parent.name)
    ns.yeniden = True

    def on(n, c):
        on.n.append(n.aday)
    on.n = []
    c = {**_ctx(tmp_path, ar), "gh": gh, "uyku": _uyku(), "on": on}
    c["env"]["CLAUDE_EVI"] = str(tmp_path / "evi")
    pt.parti(ns, c)
    assert "ajan-k" not in ar.adlar  # model araştırması yok
    assert on.n == ["ajan-k"]  # koşmamış güvenlik taraması yeniden denendi
    assert {"repos/o/ajan-k/license", "repos/o/ajan-k/commits?per_page=1"} <= set(gh.cagrilar)
    ks = next(s for s in _panel(tmp_path, PID)[1].split("## Kapsam", 1)[1].splitlines() if s.startswith("- ajan-k ·"))
    assert "lisans ✓" in ks and "commit ✓ 2026-09-30" in ks
    assert "| Apache-2.0 |" in _lisans_satiri(tmp_path, "ajan-k")


def _gh_fork(fork):
    tarih = {"ust/depo": "2026-01-23", "asil/depo": "2026-10-02", "baska/alt-arac": "2026-10-01"}

    def gh(args):
        gh.cagrilar.append(args[1])
        if "search/repositories" in args:
            return {"items": []}
        if args[1] == "repos/ust/depo":
            return {"fork": fork, **({"parent": {"full_name": "Asil/depo"}, "source": {"full_name": "Asil/depo"}} if fork else {})}
        if "/commits?" in args[1]:
            return [{"sha": "f00", "commit": {"committer": {"date": tarih[args[1].split("/commits?")[0][6:]] + "T10:00:00Z"}}}]
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


def _satir(tmp_path, ad):
    return next(s for s in _panel(tmp_path, PID)[1].splitlines() if s.startswith(f"| {ad} |"))


# A3 (=Y7) kurulu marketplace reposu fork → asıl (source/parent) son commit'iyle Kapsam satırı, öneri UYARLA / kaynağa geç
def test_a3_kurulu_fork_kaynak_farki(tmp_path):
    from test_derinlik2 import _kurulu_kayit
    _kurulu_kayit(tmp_path)
    d, _ = _kos(tmp_path, [("alt-arac", "plugin", None)], _gh_fork(True))
    k = "kaynak farklı: kurulu ust/depo (son commit 2026-01-23) ↔ asıl asil/depo (son commit 2026-10-02)"
    assert d["alt-arac"]["kaynak"] == k
    assert k in _panel(tmp_path, PID)[1].split("## Kapsam", 1)[1]
    s = _satir(tmp_path, "alt-arac")
    assert "| UYARLA |" in s and "kaynağa geç" in s


# A3 fork bayrağı yok ama videodaki sahip kurulu reponun sahibinden farklı → aynı kontrol; sahip aynıysa kaynak satırı yok
def test_a3_videodaki_sahip_farkli(tmp_path):
    from test_derinlik2 import _kurulu_kayit
    _kurulu_kayit(tmp_path)
    d, _ = _kos(tmp_path, [("alt-arac", "plugin", "https://github.com/baska/alt-arac")], _gh_fork(False))
    assert d["alt-arac"]["kaynak"] == "kaynak farklı: kurulu ust/depo (son commit 2026-01-23) ↔ asıl baska/alt-arac (son commit 2026-10-01)"


def test_a3_fork_degil_sahip_ayni_kaynak_yok(tmp_path):
    from test_derinlik2 import _kurulu_kayit
    _kurulu_kayit(tmp_path)
    d, _ = _kos(tmp_path, [("alt-arac", "plugin", None)], _gh_fork(False))
    assert not d["alt-arac"].get("kaynak")


# --- A4 (=Y5) kurulu kaynakların tamamı + açıklamadan "bizde benzer" ---
ENV_A4 = [{"ad": "ui-ux-pro-max", "tur": "skill", "aciklama": "Design intelligence: styles, palettes, fonts, CSV search script"},
          {"ad": "security-assessment", "tur": "skill", "aciklama": "Repository wide security scan and findings report"},
          {"ad": "gstack", "tur": "skill", "aciklama": "Ship, review, QA workflow"},
          {"ad": "jev", "tur": "plugin", "aciklama": "typed judgments"}]


def _envanter(tmp_path):
    y = tmp_path / "docs" / "departmanlar" / "envanter.json"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(json.dumps(ENV_A4), encoding="utf-8")


def test_a4_repo_adindan_kurulu_eslesir(tmp_path):
    from test_derinlik2 import _rapor
    from test_m2a import V
    from video import akil as ak
    _envanter(tmp_path)
    out, _ = ak.birlestir([(V[0], _rapor(V[0], [("tasarim-skill-i", "skill", "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill")]))], tmp_path)
    assert out["tasarim-skill-i"]["kurulu"] == "ui-ux-pro-max"


def test_a4_paket_ici_skill_paket_reposuna_baglanir(tmp_path):
    from test_derinlik2 import _kurulu_kayit
    from video import akil as ak
    _kurulu_kayit(tmp_path)
    env = {"CLAUDE_EVI": str(tmp_path / "evi")}
    assert ak._kayit_repo(env, {"kurulu": "alt-arac:security-review", "adlar": ["security-review"]}) == ("ust/depo", "plugins/alt-arac")


def test_a4_kurulu_skill_git_uzak_adresinden_repo(tmp_path):
    from video import akil as ak
    g = tmp_path / "evi" / "skills" / "gstack" / ".git"
    g.mkdir(parents=True)
    (g / "config").write_text('[core]\n\tbare = false\n[remote "origin"]\n\turl = https://github.com/garrytan/gstack.git\n', encoding="utf-8")
    env = {"CLAUDE_EVI": str(tmp_path / "evi")}
    assert ak._kayit_repo(env, {"kurulu": "gstack", "adlar": ["stack-garry-tan"]}) == ("garrytan/gstack", "")


def test_a4_aciklamadan_en_yakin_3_benzer_kapsamda(tmp_path):
    from test_m2a import V
    from video import akil as ak
    a = {"ad": "renk-araci", "tur": "skill", "repo": None, "kurulu": None, "durum": "tamam", "adlar": ["renk-araci"],
         "videolar": {V[0]: {"ne": "CSV palettes and styles search script"}}}
    b = ak._benzer(a, ENV_A4)
    assert b[0] == "ui-ux-pro-max" and len(b) <= 3 and "jev" not in b
    a["benzer"] = b
    assert "bizde benzer ui-ux-pro-max" in ak._kapsam("renk-araci", a, {}, "", "koşmadı: x", {})[0]


# --- A5 KUR + ONARIM + GÜÇLENDİRME: çözülmemiş kötü yan → ONARIM BEKLİYOR (kurulmaz, elenmez); kapatma onarım sayılmaz ---
def _a5(tmp_path, onarim):
    ky = [{"sinif": "token", "ne": "oturum başı 4k enjeksiyon", "neden": "hooks/session.js:12", "olcum": "tahmin", "onarim": "TOKEN-3 profili", "kaynak": "README"},
          {"sinif": "kalite", "ne": "kurulu araçla çakışma", "neden": "aynı tetik", "olcum": "tahmin", "onarim": onarim, "kaynak": "issue #3"}]
    ar = Ar({"ajan-a5": {"repo_url": "https://github.com/o/ajan-a5", "lisans": "MIT", "lisans_kaynak": "LICENSE", "son_commit": "2026-09-20",
                         "kotu_yanlar": ky, "guclendirme": "graphify ile bağlam daraltma"}})
    _kos(tmp_path, [("ajan-a5", "plugin", None)], None, ar)
    return _panel(tmp_path, PID)[1]


def test_a5_cozulmemis_kotu_yan_onarim_bekliyor(tmp_path):
    t = _a5(tmp_path, None)  # onarım yolu yok
    assert "| ONARIM BEKLİYOR |" in _satir(tmp_path, "ajan-a5")
    b = t.split("## Kötü yan + onarım + güçlendirme", 1)[1].split("\n## ", 1)[0]
    assert "ajan-a5 · kalite · kurulu araçla çakışma" in b and "onarım: çözülmedi" in b and "onarım: TOKEN-3 profili" in b
    assert "güçlendirme: graphify ile bağlam daraltma" in b


def test_a5_kapatma_onarim_sayilmaz(tmp_path):
    _a5(tmp_path, "kurulu impeccable'ı kapat")
    assert "| ONARIM BEKLİYOR |" in _satir(tmp_path, "ajan-a5")


def test_a5_hepsi_onarilmis_kur_yolunda(tmp_path):
    _a5(tmp_path, "Skill aracıyla tembel yükleme")
    assert "ONARIM BEKLİYOR" not in _satir(tmp_path, "ajan-a5")


def test_a5_istem_ve_arastirici_tanimi():
    from pathlib import Path
    from video import akil as ak
    assert all(x in ak.SISTEM for x in ("kotu_yanlar", "TOKEN-3 profili", "tembel yükleme", "sarmalayıcı", "güçlendirme", "kapatan"))
    t = (Path(__file__).resolve().parents[3] / ".claude" / "agents" / "aday-arastirici.md").read_text(encoding="utf-8")
    assert "## Kötü yan + onarım + güçlendirme" in t


# --- A4b "bizde benzer" İngilizce kaynakla (gerçek envanter) ---
UI_EN = ("UI UX Pro Max - An AI skill that provides design intelligence for building professional UI/UX across multiple platforms.\n"
         "67 UI styles, 96 color palettes, 57 font pairings, 25 chart types and 99 UX guidelines. Searchable database with a CSV search script.\n"
         "Works with Claude Code, Cursor, Windsurf. Generate a design system for landing pages, dashboards, mobile apps.")
SEC_EN = ("RepoGuard - scan your whole repository for security vulnerabilities.\n"
          "Static analysis of every file, secret detection, vulnerable dependency audit and a findings report ranked by severity.\n"
          "Run it in CI or locally before you ship.")
GUVENLIK = {"security-assessment", "cso", "gstack-cso"}


def _env_gercek():
    from pathlib import Path
    return json.loads((Path(__file__).resolve().parents[3] / "docs" / "departmanlar" / "envanter.json").read_text(encoding="utf-8"))


def _aday_en(ad, repo, ne):
    return {"ad": ad, "repo": repo, "videolar": {"v": {"ne": ne}}}


def _gh_en(aciklama, readme):
    import base64

    def gh(args):
        gh.cagrilar.append(args[1])
        if args[1].endswith("/readme"):
            return {"content": base64.b64encode(readme.encode()).decode(), "encoding": "base64"}
        return {"description": aciklama}
    gh.cagrilar = []
    return gh


def _strix_cso(b):
    return [x for x in b if x in GUVENLIK or "strix" in x]


def test_a4b_turkce_notlu_ingilizce_readmeli_tasarim_adayi():
    from video import akil as ak
    env, a = _env_gercek(), _aday_en("tasarim-zekasi", "nextlevelbuilder/ui-ux-pro-max-skill", "tasarım skill'i: stil, palet, font önerisi; CSV arama betiği")
    assert "ui-ux-pro-max" not in ak._benzer(a, env)  # Türkçe not tek başına kaçırır
    gh, u = _gh_en("Design intelligence skill for UI/UX", UI_EN + "\n" + "x\n" * 40), _uyku()
    a["kaynak_en"] = ak._kaynak_en({"gh": gh, "uyku": u}, a)
    assert gh.cagrilar == ["repos/nextlevelbuilder/ui-ux-pro-max-skill", "repos/nextlevelbuilder/ui-ux-pro-max-skill/readme"] and u.n == [2, 2]
    assert a["kaynak_en"].startswith("Design intelligence") and a["kaynak_en"].count("\nx") < 30  # README ilk 30 satır
    sorulan = []
    assert "ui-ux-pro-max" in ak._benzer(a, env, sec=lambda *x: sorulan.append(x)) and sorulan == []  # açık fark: Jev yok


def test_a4b_depo_geneli_guvenlik_belirsizde_tek_jev():
    from video import akil as ak
    env, a = _env_gercek(), _aday_en("repoguard", "o/repoguard", "depo geneli güvenlik taraması, bulgu raporu")
    assert not _strix_cso(ak._benzer(a, env))  # Türkçe not tek başına kaçırır
    a["kaynak_en"] = SEC_EN
    assert _strix_cso(ak._benzer(a, env))
    sorulan = []

    def sec(ad, ilk, metin):
        sorulan.append((ad, ilk, metin))
        return next(x for x in ilk if "strix" in x)
    b = ak._benzer(a, env, sec=sec)
    assert len(sorulan) == 1 and len(sorulan[0][1]) == 5 and sorulan[0][2] == SEC_EN and "strix" in b[0] and len(b) == 3
    assert ak._benzer(a, env, sec=sec) == b and len(sorulan) == 1  # sonuç a["benzer_jev"]; tekrar sorulmaz


def test_a4b_jev_secimi_mevcut_esdeger_yolu_defterde(tmp_path):
    ev = tmp_path / "docs" / "departmanlar" / "envanter.json"
    ev.parent.mkdir(parents=True, exist_ok=True)
    ev.write_text(json.dumps([{"ad": x, "tur": "skill", "aciklama": "security scan of the repository"} for x in ("cso", "tarayici-b", "tarayici-c")]
                             + [{"ad": "ui-ux-pro-max", "tur": "skill", "aciklama": "design system palettes"}]), encoding="utf-8")
    gh = _gh_en("repo security scan", SEC_EN)
    jev = []

    def yargila(states, q):
        jev.append((states, q))
        return [{"es": {"probabilities": {"cso": 0.8, "tarayici-b": 0.1, "yok": 0.1}}}]
    from video import akil as ak
    ctx = {"yargila": yargila}
    a = _aday_en("repoguard", "o/repoguard", "depo geneli güvenlik taraması")
    a["kaynak_en"] = ak._kaynak_en({"gh": gh, "uyku": _uyku()}, a)
    pdir = tmp_path / "p"
    pdir.mkdir()
    b = ak._benzer(a, json.loads(ev.read_text(encoding="utf-8")), sec=ak._benzer_sec(ctx, pdir, json.loads(ev.read_text(encoding="utf-8"))))
    assert b[0] == "cso" and a["benzer_jev"] == "cso" and len(jev) == 1 and "yok" in jev[0][1]["es"]["criteria"]
    assert [x["adim"] for x in pt.tr.kayit_oku(pdir / "defter.jsonl")] == ["benzer_jev"]


# A6(a) (=Y4): eski aday.md'de lisans:/son_commit: satırı yoksa alan bloğunun sonuna (ilk '#' satırından önce) eklenir; mevcut içerik değişmez
def test_a6a_eksik_satir_alan_blogu_sonuna_eklenir(tmp_path):
    from video import akil as ak
    y = ak._aday_yol(tmp_path, "stop-slop")
    y.parent.mkdir(parents=True)
    eski = "# stop-slop\nrepo: o/stop-slop\ntur: skill\n\n## Ne yapar\nmetin\n"
    y.write_text(eski, encoding="utf-8", newline="")
    ak._eksik_tamamla({"gh": _gh_a2(), "uyku": _uyku()}, tmp_path, "stop-slop", {"repo": "o/stop-slop"})
    m = y.read_text(encoding="utf-8")
    assert m == "# stop-slop\nrepo: o/stop-slop\ntur: skill\nlisans: Apache-2.0\nson_commit: 2026-09-30\n\n## Ne yapar\nmetin\n"
    assert ak.uy.alanlar(m)["son_commit"] == "2026-09-30"  # panelin okuduğu blokta


def _gh_etiket(kirik):
    def gh(args):
        gh.cagrilar.append(args[1])
        if args[1].endswith("releases/latest"):
            return {"tag_name": "v1.3.0"}
        if args[1].endswith("commits/v1.3.0") and not kirik:
            return {"sha": "c0ffee1", "commit": {"committer": {"date": "2026-09-01T10:00:00Z"}}}
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


# A6(b) (=Y4, derinlik-3 S3): sürümle (etiket) kurulu plugin'de etiket → commit → tarih (REST, arama değil); zincir kırılırsa aday düşmez, sebep satırda
def test_a6b_etiketli_kurulu_tarih_zinciri(tmp_path):
    from video import akil as ak
    (evi := tmp_path / "evi" / "plugins").mkdir(parents=True)
    (evi / "installed_plugins.json").write_text(json.dumps(
        {"plugins": {"hizli-paket@m": [{"installPath": str(tmp_path / "yok"), "version": "1.2.0"}]}}), encoding="utf-8")
    a = {"kurulu": "m:hizli-paket", "repo": "ornek/hizli-paket", "adlar": ["hizli-paket"]}
    for kirik, son in ((False, " · etiket v1.3.0 commit 2026-09-01"), (True, " · etiket v1.3.0 tarihi alınamadı (gh: HTTP 404)")):
        gh = _gh_etiket(kirik)
        g = ak._guncellik({"gh": gh, "uyku": _uyku(), "env": {"CLAUDE_EVI": str(tmp_path / "evi")}}, a)
        assert g == "fark: kurulu 1.2.0 ↔ upstream 1.3.0" + son
        assert "repos/ornek/hizli-paket/commits/v1.3.0" in gh.cagrilar and not any("search/" in x for x in gh.cagrilar)
