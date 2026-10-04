"""DERİNLİK-2: araştırma doğruluğu — S1 repo eşleşme doğrulaması · S4 repo geri yazımı · S5 güvenlik kapsamı · S6 lisans · S10 öneri kuralı · S2/S3 güncellik · S7 birleştirme."""
import base64
import json

from test_m2a import V, _ns
from test_m2b import _parti, _rapor
from test_m2c import Ar, _ctx

from video import parti as pt

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
