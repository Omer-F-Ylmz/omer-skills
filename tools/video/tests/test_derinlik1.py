"""DERİNLİK-1: araştırma kapsamı — R2 sınıf ne olursa olsun repo araştırılır · R3 repo araması · R5 kapsam · R6 --yeniden · R1 güncellik · R4 yorum/kare."""
import json

from test_m2a import V, _ns
from test_m2b import _parti, _rapor
from test_m2c import Ar, _ctx, _jev, _panel

from video import parti as pt

PID = "2026-10-03-short"


# R2 servis/ürün sınıfı reposu varsa normal araştırmadan geçer (eskiden arac_degil → atlanıyordu)
def test_r2_servis_repolu_arastirilir(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("harness-audit", "servis", "https://github.com/ornek/harness-audit")])})
    ar = Ar({"harness-audit": {"alt_tur": "araç"}})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, ar, _jev("servis")))
    assert "harness-audit" in ar.adlar
    assert json.loads((p / "durum.json").read_text(encoding="utf-8"))["adaylar"]["harness-audit"]["durum"] == "tamam"


def _gh(bulunan=None):
    def gh(args):
        q = next(x[2:] for x in args if x.startswith("q="))
        gh.sorgular.append(q)
        return {"items": [{"name": "ajan-x", "full_name": "Ornek/Ajan-X"}] if q == bulunan else [{"name": "baska", "full_name": "z/baska"}]}
    gh.sorgular = []
    return gh


def _uyku():
    def u(s):
        u.n.append(s)
    u.n = []
    return u


# R3 repo yok → GitHub araması (en fazla 3 sorgu, aralarında ≥2 sn); bulunursa repo araştırmaya girer
def test_r3_repo_bulunur(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("ajan-x", "servis", None)])})
    ar, gh, u = Ar({}), _gh("ajan-x claude"), _uyku()
    pt.parti(_ns("akil", p.name), {**_ctx(tmp_path, ar), "gh": gh, "uyku": u})
    a = json.loads((p / "durum.json").read_text(encoding="utf-8"))["adaylar"]["ajan-x"]
    assert (a["repo"], a["repo_arama"]) == ("ornek/ajan-x", "bulundu: ornek/ajan-x")
    assert gh.sorgular == ["ajan-x", "ajan-x claude"] and u.n == [2] and "ajan-x" in ar.adlar


def test_r3_bulunamadi_ve_gh_yok(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("ajan-x", "servis", None)])})
    gh, u = _gh(), _uyku()
    pt.parti(_ns("akil", p.name), {**_ctx(tmp_path, Ar({})), "gh": gh, "uyku": u})
    _, t = _panel(tmp_path, PID)
    assert len(gh.sorgular) == 3 and u.n == [2, 2]
    assert "## Repo araması" in t and f"- ajan-x: arandı, bulunamadı ({'; '.join(gh.sorgular)})" in t
    p2 = _parti(tmp_path / "b", PID, {V[0]: _rapor(V[0], [("ajan-y", "servis", None)])})
    pt.parti(_ns("akil", p2.name), _ctx(tmp_path / "b", Ar({})))
    assert "- ajan-y: arama koşmadı (gh bağlamı yok)" in _panel(tmp_path / "b", PID)[1]


# R5 panelde ayrı "## Kapsam" bölümü; kapsamı eksik aday "Araştırılmadı"ya da düşer; 8 sütunlu tablo değişmez
def test_r5_kapsam_bolumu(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("hizli", "CLI", "https://github.com/ornek/hizli"), ("ajan-y", "servis", None)])})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, Ar({"hizli": {"alt_tur": "araç"}})))
    r, t = _panel(tmp_path, PID)
    assert set(r) >= {"hizli", "ajan-y"}
    ks = t.split("## Kapsam", 1)[1].split("\n## ", 1)[0]
    h = next(s for s in ks.splitlines() if s.startswith("- hizli ·"))
    assert all(x in h for x in ("repo ✓", "README ✓", "lisans ✓", "commit ✓", "prompt metni —", "güncellik — (kurulu değil)", "yorum "))
    y = next(s for s in ks.splitlines() if s.startswith("- ajan-y ·"))
    assert "repo arama koşmadı (gh bağlamı yok)" in y and "README " in y and "README ✓" not in y
    ar_ = t.split("## Araştırılmadı", 1)[1].split("\n## ", 1)[0]
    assert "- ajan-y: kapsam eksik (repo, README, lisans, commit, güvenlik)" in ar_ and "- hizli: kapsam eksik (güvenlik)" in ar_


# R6 --yeniden durum + repo_arama sıfırlanır, araştırma yeniden koşar; güvenlik yalnız repo değiştiyse yeniden
def test_r6_yeniden_arastirir(tmp_path):
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("eski-servis", "servis", "https://github.com/ornek/eski-servis"), ("ajan-x", "servis", None)])})
    pt.parti(_ns("akil", p.name), _ctx(tmp_path, Ar({})))
    y = p / "durum.json"
    d = json.loads(y.read_text(encoding="utf-8"))
    d["adaylar"]["eski-servis"].update(durum="arac_degil", guvenlik="HIGH/CRITICAL 0 (eski)")  # DERİNLİK-1 öncesi durum: repolu servis atlanmış
    y.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    m = tmp_path / "docs" / "kurulumlar" / "adaylar" / "eski-servis.md"
    m.write_text(m.read_text(encoding="utf-8").replace("arastirma: tam", "arastirma: yarım"), encoding="utf-8")
    ar, ns = Ar({}), _ns("akil", p.name)
    ns.yeniden = True
    pt.parti(ns, {**_ctx(tmp_path, ar), "gh": _gh("ajan-x"), "uyku": _uyku()})
    d = json.loads(y.read_text(encoding="utf-8"))["adaylar"]
    assert set(ar.adlar) >= {"eski-servis", "ajan-x"} and d["ajan-x"]["repo"] == "ornek/ajan-x"
    assert d["eski-servis"]["guvenlik"] == "HIGH/CRITICAL 0 (eski)"  # repo aynı → ön tarama yeniden koşmaz


# R2 paket içi parça kurulu paketteki karşılığıyla eşleşir; dosya yolu panelde
def test_r2_paket_ici_eslesir(tmp_path):
    evi = tmp_path / "evi"
    s = evi / "plugins" / "cache" / "everything-claude-code" / "1.0" / "skills" / "harness-audit"
    s.mkdir(parents=True)
    (s / "SKILL.md").write_text("---\nname: harness-audit\n---\n", encoding="utf-8")
    p = _parti(tmp_path, PID, {V[0]: _rapor(V[0], [("harness-audit (ECC içinde)", "skill", None)])})
    c = _ctx(tmp_path, Ar({}))
    c["env"]["CLAUDE_EVI"] = str(evi)
    pt.parti(_ns("akil", p.name), c)
    _, t = _panel(tmp_path, PID)
    assert "paket içi: " in t and "everything-claude-code/1.0/skills/harness-audit" in t
