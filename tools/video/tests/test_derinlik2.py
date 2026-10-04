"""DERİNLİK-2: araştırma doğruluğu — S1 repo eşleşme doğrulaması · S4 repo geri yazımı · S5 güvenlik kapsamı · S6 lisans · S10 öneri kuralı · S2/S3 güncellik · S7 birleştirme."""
import base64
import json

from test_m2a import V, _ns
from test_m2b import _parti, _rapor
from test_m2c import Ar, _ctx

from pathlib import Path

from video import akil as ak, parti as pt, uygula as uy

PID = "2026-10-03-short"


def _uyku():
    def u(s):
        u.n.append(s)
    u.n = []
    return u


def _gh(arama, readme=None):
    """arama: arama sonucu öğeleri (her sorguda aynı); readme: {repo: metin}."""
    def gh(args):
        gh.cagrilar.append(args)
        if "search/repositories" in args:
            return {"items": arama}
        y = args[1]
        if y.endswith("/readme") and (r := (readme or {}).get(y[6:-7])) is not None:
            return {"content": base64.b64encode(r.encode()).decode(), "encoding": "base64"}
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


def _kos(tmp_path, adaylar, gh, ar=None, rapor_duzelt=None):
    md = _rapor(V[0], adaylar)
    p = _parti(tmp_path, PID, {V[0]: rapor_duzelt(md) if rapor_duzelt else md})
    ar = ar or Ar({})
    c = {**_ctx(tmp_path, ar), "gh": gh, "uyku": _uyku()}
    c["env"]["CLAUDE_EVI"] = str(tmp_path / "evi")
    pt.parti(_ns("akil", p.name), c)
    return json.loads((p / "durum.json").read_text(encoding="utf-8"))["adaylar"], ar


# S1 ad eşleşmesi yetmez: açıklamada anahtar kelime yoksa "olası (doğrulanmadı)", araştırmaya girmez
def test_s1_stack_reddedilir(tmp_path):
    gh = _gh([{"name": "stack", "full_name": "commercialhaskell/stack", "description": "The Haskell Tool Stack", "topics": ["haskell"]}])
    d, ar = _kos(tmp_path, [("stack", "plugin", None)], gh)
    assert d["stack"]["repo"] is None and d["stack"]["repo_arama"] == "olası: commercialhaskell/stack (doğrulanmadı)"
    assert "stack" not in ar.adlar


# S1 videoda sahip adı geçiyorsa sahip eşleşmeli: ECC → affaan-m/everything-claude-code (fork değil)
def test_s1_ecc_sahip_adi(tmp_path):
    gh = _gh([{"name": "everything-claude-code", "full_name": "WorldFlowAI/everything-claude-code", "description": "Claude Code config fork"},
              {"name": "everything-claude-code", "full_name": "affaan-m/everything-claude-code", "description": "Claude Code agents and skills"}])
    d, _ = _kos(tmp_path, [("everything-claude-code (ECC)", "plugin", None)], gh,
                rapor_duzelt=lambda md: md.replace("Anlatıcı aracı çalıştırıyor.", "Ekranda affaan-m imzası görünüyor."))
    a = d["everything-claude-code-ecc"]
    assert (a["repo"], a["repo_arama"]) == ("affaan-m/everything-claude-code", "bulundu: affaan-m/everything-claude-code")


# S1 açıklama boşsa topics + README ilk 30 satırı; hiçbirinde anahtar kelime yoksa olası
def test_s1_aciklama_bos_readme(tmp_path):
    bos = lambda n: {"name": n, "full_name": f"o/{n}", "description": None, "topics": []}
    gh = _gh([bos("ajan-r"), bos("ajan-s")], {"o/ajan-r": "# ajan-r\nA Claude Code skill.\n", "o/ajan-s": "# ajan-s\n" + "satır\n" * 35 + "claude\n"})
    d, _ = _kos(tmp_path, [("ajan-r", "plugin", None), ("ajan-s", "plugin", None)], gh)
    assert d["ajan-r"]["repo_arama"] == "bulundu: o/ajan-r"
    assert d["ajan-s"]["repo_arama"] == "olası: o/ajan-s (doğrulanmadı)" and d["ajan-s"]["repo"] is None


def _kurulu_kayit(tmp_path):
    evi, ml = tmp_path / "evi", tmp_path / "evi" / "plugins" / "marketplaces" / "pazar"
    (ml / ".claude-plugin").mkdir(parents=True)
    (ml / ".claude-plugin" / "marketplace.json").write_text(json.dumps({"plugins": [
        {"name": "yerel-arac", "source": "./plugins/yerel-arac"},
        {"name": "alt-arac", "source": {"source": "git-subdir", "url": "https://github.com/Ust/Depo.git", "path": "plugins/alt-arac"}}]}), encoding="utf-8")
    (evi / "plugins" / "known_marketplaces.json").write_text(json.dumps(
        {"pazar": {"source": {"source": "github", "repo": "Sahip/Pazar"}, "installLocation": str(ml)}}), encoding="utf-8")
    (evi / "plugins" / "installed_plugins.json").write_text(json.dumps({"plugins": {
        "yerel-arac@pazar": [{"installPath": str(tmp_path / "ip1"), "version": "1.0.0"}],
        "alt-arac@pazar": [{"installPath": str(tmp_path / "ip2"), "version": "2.0.0"}]}}), encoding="utf-8")
    ky = tmp_path / "docs" / "kurulumlar" / "kayit.jsonl"
    ky.parent.mkdir(parents=True, exist_ok=True)
    ky.write_text("".join(json.dumps({"ad": x, "karar": "KUR (test)"}) + "\n" for x in ("yerel-arac", "alt-arac")), encoding="utf-8")


# S1 kurulu araçta repo kurulum kaydından (marketplace kaynağı); arama yapılmaz
def test_s1_kurulu_repo_kayittan(tmp_path):
    _kurulu_kayit(tmp_path)
    gh = _gh([{"name": "yerel-arac", "full_name": "baska/yerel-arac", "description": "claude"}])
    d, _ = _kos(tmp_path, [("yerel-arac", "plugin", None), ("alt-arac", "plugin", None)], gh)
    assert d["yerel-arac"]["repo"] == "sahip/pazar" and d["alt-arac"]["repo"] == "ust/depo"
    assert not any("search/repositories" in x for x in gh.cagrilar)


# S4 araştırıcının bulduğu repo durum.json'a geri yazılır; Kapsam "repo ✓ owner/ad"; Repo araması çelişmez
def test_s4_arastirici_reposu_geri_yazilir(tmp_path):
    from test_m2c import _panel
    d, _ = _kos(tmp_path, [("ajan-z", "plugin", None)], None, Ar({"ajan-z": {"repo_url": "https://github.com/Bulan/Ajan-Z"}}))
    assert (d["ajan-z"]["repo"], d["ajan-z"]["repo_arama"]) == ("bulan/ajan-z", "araştırıcı buldu: bulan/ajan-z")
    t = _panel(tmp_path, PID)[1]
    assert "- ajan-z: araştırıcı buldu: bulan/ajan-z" in t
    assert next(s for s in t.split("## Kapsam", 1)[1].splitlines() if s.startswith("- ajan-z ·")).startswith("- ajan-z · repo ✓ bulan/ajan-z ·")


def _skos(icerik_mb):
    """Sahte kos: repo 195 MB; seyrek klon SKILL.md'yi icerik_mb boyutunda bırakır."""
    def kos(args, timeout=None):
        kos.cagri.append(args)
        if args[:2] == ["gh", "api"]:
            return 0, b"200000", b""
        if args[:2] == ["git", "clone"]:
            Path(args[-1]).mkdir(parents=True)
        if "sparse-checkout" in args:
            with open(Path(args[2]) / "SKILL.md", "wb") as f:
                f.truncate(icerik_mb * 1024 * 1024)
        return 0, b"", b""
    kos.cagri = []
    return kos


# S5 büyük repo (>100 MB): tam klon yok; seyrek klon (SKILL.md/hooks/commands/agents) + SkillSpector
def test_s5_buyuk_repo_seyrek_taranir(tmp_path):
    kos = _skos(1)
    on = uy.on_tarama({"kok": tmp_path, "kos": kos}, "o/lh")
    klon = next(a for a in kos.cagri if a[:2] == ["git", "clone"])
    assert "--sparse" in klon and "--filter=blob:none" in klon
    ss = next(a for a in kos.cagri if "sparse-checkout" in a)
    assert all(x in ss for x in ("SKILL.md", "hooks/", "commands/", "agents/"))
    assert any(a[0] == "skillspector" for a in kos.cagri) and "seyrek tarama (repo 195 MB)" in on


# S5 seyrek içerik >20 MB → "atlandı (sebep)", SkillSpector koşmaz
def test_s5_seyrek_icerik_20mb_ustu_atlanir(tmp_path):
    kos = _skos(21)
    on = uy.on_tarama({"kok": tmp_path, "kos": kos}, "o/lh")
    assert "atlandı (seyrek içerik 21 MB)" in on and not any(a[0] == "skillspector" for a in kos.cagri)


# S5 atlanan güvenlik taraması Kapsam'da ✓ sayılmaz
def test_s5_atlanan_tarama_kapsamda_tik_degil():
    a = {"tur": "plugin", "repo": "o/lh", "kurulu": None, "durum": "araştırıldı", "videolar": {V[0]: {}}}
    satir, eksik = ak._kapsam("lh", a, {}, "", "atlandı (seyrek içerik 21 MB)", {})
    assert "güvenlik atlandı (seyrek içerik 21 MB)" in satir and "güvenlik" in eksik


def _gh_lisans(spdx):
    def gh(args):
        gh.cagrilar.append(args)
        if "search/repositories" in args:
            return {"items": []}
        if args[1].endswith("/license") and spdx:
            return {"license": {"spdx_id": spdx}}
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


def _lisans_satiri(tmp_path, ad):
    from test_m2c import _panel
    return next(s for s in _panel(tmp_path, PID)[1].splitlines() if s.startswith(f"| {ad} |"))


# S6 lisans gh api repos/<r>/license'tan; araştırıcının yazdığı lisans ezilir
def test_s6_lisans_gh_apiden(tmp_path):
    gh = _gh_lisans("Apache-2.0")
    _kos(tmp_path, [("ajan-l", "plugin", None)], gh, Ar({"ajan-l": {"repo_url": "https://github.com/o/ajan-l", "lisans": "MIT"}}))
    assert ["api", "repos/o/ajan-l/license"] in gh.cagrilar
    assert "| Apache-2.0 |" in _lisans_satiri(tmp_path, "ajan-l")


# S6 API okunamaz + lisans "hatırlanan bilgi" → reddedilir, "bilinmiyor"
def test_s6_hatirlanan_lisans_reddedilir(tmp_path):
    ar = Ar({"ajan-h": {"repo_url": "https://github.com/o/ajan-h", "lisans": "MIT", "lisans_kaynak": "hatırlanan bilgi"}})
    _kos(tmp_path, [("ajan-h", "plugin", None)], _gh_lisans(None), ar)
    assert "| bilinmiyor |" in _lisans_satiri(tmp_path, "ajan-h")


# S10 kurulu araç kapatma/kaldırma önerisi panelde işaretlenir; kurala uyan öneri işaretlenmez; kural akıl isteminde
def test_s10_kapatma_onerisi_isaretlenir(tmp_path):
    from test_m11 import _kur
    from test_m2c import _aday, _panel
    pdir, d = _kur(tmp_path, (), {"x": _aday("x", kurulu="x"), "y": _aday("y")}, ["x", "y"])
    d["gelistirme"][0]["gelistirme_onerisi"] = "x eklentisini kapat, token yiyor"
    ak.panel(pdir, d, tmp_path)
    t = _panel(tmp_path)[1]
    sx = next(s for s in t.splitlines() if s.startswith("| x-gelistirme |"))
    sy = next(s for s in t.splitlines() if s.startswith("| y-gelistirme |"))
    assert "S10 ihlali" in sx and "S10" not in sy
    assert "S10 ihlali" in t.split("## Geliştirme önerileri", 1)[1]
    assert "TOKEN-3" in ak.SISTEM_GEL and "kapatma/kaldırma" in ak.SISTEM_GEL


def _gh_commit(sha, tarih):
    def gh(args):
        gh.cagrilar.append(args[1])
        if "search/repositories" in args:
            return {"items": []}
        if "/commits?" in args[1]:
            return [{"sha": sha, "commit": {"committer": {"date": tarih + "T10:00:00Z"}}}]
        raise RuntimeError("HTTP 404")
    gh.cagrilar = []
    return gh


# S2+S3 marketplace alt yolundaki kurulu plugin: güncellik ve son commit o alt yol için gh api'den; tarih güncellik (Kapsam) satırında
def test_s2_s3_alt_yol_guncellik_ve_tarih(tmp_path):
    _kurulu_kayit(tmp_path)
    ip = tmp_path / "evi" / "plugins" / "installed_plugins.json"
    k = json.loads(ip.read_text(encoding="utf-8"))
    k["plugins"]["alt-arac@pazar"][0]["gitCommitSha"] = "abc1234"
    ip.write_text(json.dumps(k), encoding="utf-8")
    gh = _gh_commit("abc1234def", "2026-09-30")
    d, _ = _kos(tmp_path, [("alt-arac", "plugin", None)], gh)
    assert "repos/ust/depo/commits?per_page=1&path=plugins/alt-arac" in gh.cagrilar
    assert any(x.startswith("repos/ust/depo/contents/plugins/alt-arac/") for x in gh.cagrilar)
    g = d["alt-arac"]["guncellik"]
    assert g.startswith("güncel (abc1234)") and "son commit 2026-09-30" in g


# S3 araştırılan araçta son commit tarihi gh api'den (araştırıcının yazdığı ezilir); Kapsam'da "commit ✓ <tarih>"
def test_s3_son_commit_gh_apiden(tmp_path):
    from test_m2c import _panel
    ar = Ar({"ajan-c": {"repo_url": "https://github.com/o/ajan-c", "son_commit": "2025-01-01"}})
    _kos(tmp_path, [("ajan-c", "plugin", None)], _gh_commit("f00", "2026-08-15"), ar)
    ks = next(s for s in _panel(tmp_path, PID)[1].split("## Kapsam", 1)[1].splitlines() if s.startswith("- ajan-c ·"))
    assert "commit ✓ 2026-08-15" in ks


# S7 aynı videoda ad benzerliği ≥0.8 (parantez içi ad dahil) → tek aday (ruflo ×3, ECC ×3 tek satır); farklı videoda birleşmez
def test_s7_ayni_videoda_benzer_adlar_tek_aday(tmp_path):
    md0 = _rapor(V[0], [("ruflo", "plugin", None), ("Ruflo (videoda 'Rufflow')", "plugin", "https://github.com/ruvnet/ruflo"),
                        ("Everything Claude Code (ECC)", "plugin", None), ("everything-claude-code", "plugin", None)])
    md1 = _rapor(V[1], [("ruflo", "plugin", None), ("Rooflow (karede Ruflo)", "iş akışı", None), ("ajan-xy", "plugin", None)])
    md2 = _rapor(V[2], [("ajan-x", "plugin", None)])
    out, _ = ak.birlestir([(V[0], md0), (V[1], md1), (V[2], md2)], tmp_path)
    assert len(out) == 4 and {"ajan-x", "ajan-xy"} <= set(out)
    ruf = next(a for a in out.values() if "ruflo" in a["adlar"])
    assert len(ruf["adlar"]) == 3 and ruf["repo"] == "ruvnet/ruflo" and set(ruf["videolar"]) == {V[0], V[1]}


# S6b servis/ürün sınıfı da lisans API'sine gider
def test_s6b_servis_lisans_apiden(tmp_path):
    gh = _gh_lisans("Apache-2.0")
    _kos(tmp_path, [("ajan-s", "servis", "https://github.com/o/ajan-s")], gh, Ar({"ajan-s": {"alt_tur": "servis", "lisans": "MIT"}}))
    assert ["api", "repos/o/ajan-s/license"] in gh.cagrilar and "| Apache-2.0 |" in _lisans_satiri(tmp_path, "ajan-s")


# S6b API okunamaz: lisans_kaynak okunan dosya (LICENSE/README) ise düz; değilse ya da alan yoksa "(doğrulanmadı)"
def test_s6b_dogrulanmayan_lisans_isaretlenir(tmp_path):
    ar = Ar({"ajan-a": {"repo_url": "https://github.com/o/ajan-a", "lisans": "MIT", "lisans_kaynak": "README"},
             "ajan-b": {"repo_url": "https://github.com/o/ajan-b", "lisans": "MIT", "lisans_kaynak": "gh api"},
             "ajan-c": {"repo_url": "https://github.com/o/ajan-c", "lisans": "MIT"}})
    _kos(tmp_path, [("ajan-a", "plugin", None), ("ajan-b", "plugin", None), ("ajan-c", "plugin", None)], _gh_lisans(None), ar)
    assert "| MIT |" in _lisans_satiri(tmp_path, "ajan-a")
    assert all("| MIT (doğrulanmadı) |" in _lisans_satiri(tmp_path, k) for k in ("ajan-b", "ajan-c"))
