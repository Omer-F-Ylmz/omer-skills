import json
import os
import socket
import subprocess
import sys
from pathlib import Path

from jev import cekirdek as c
from jev import cli
from jev import skill as sk
from test_jev_cekirdek import ENV

HOOK_ENV = {**ENV, "JEV_SKILL_HOOK": "1"}
TCKN = "10000000146"


def _yaz(yol, ad, aciklama):
    yol.mkdir(parents=True, exist_ok=True)
    (yol / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: {aciklama}\n---\n# {ad}\n", encoding="utf-8")


def agac(ev):
    cl = ev / ".claude"
    cl.mkdir(parents=True)
    (cl / "settings.json").write_text(json.dumps({
        "enabledPlugins": {"pa@m": True, "pb@m": False},
        "skillOverrides": {"pa:s2": "off", "yerel2": "off", "anthropic-skills:sy2": "off"}}), encoding="utf-8")
    for s in ("yerel1", "yerel2"):
        _yaz(cl / "skills" / s, s, f"{s} yerel skill")
    for s in ("sy1", "sy2", "sy3"):
        _yaz(cl / "skills" / "synced" / "uuid-1" / s, s, f"{s} senkron skill")
    for s in ("s1", "s2"):
        _yaz(cl / "plugins" / "cache" / "m" / "pa" / "1.0" / "skills" / s, s, f"{s} plugin skill")
    _yaz(cl / "plugins" / "cache" / "m" / "pb" / "1.0" / "skills" / "s3", "s3", "kapalı plugin")
    return ev


def test_aktif_filtre_synced_plugin_yerel_off(tmp_path):
    ad = [a for a, _ in sk.adaylar(agac(tmp_path))]
    assert ad == ["anthropic-skills:sy1", "anthropic-skills:sy3", "pa:s1", "yerel1"]


def test_aciklama_blok_ve_200_tavan(tmp_path):
    cl = agac(tmp_path) / ".claude" / "skills" / "blok"
    cl.mkdir()
    (cl / "SKILL.md").write_text("---\nname: blok\ndescription: >\n  birinci satır\n  ikinci satır " + "x" * 300 + "\n---\n", encoding="utf-8")
    d = dict(sk.adaylar(tmp_path))["blok"]
    assert d.startswith("birinci satır ikinci satır") and len(d) <= 200


def test_onbellek_mtime_ile_yenilenir(tmp_path):
    agac(tmp_path)
    md = tmp_path / ".claude" / "skills" / "yerel1" / "SKILL.md"
    assert dict(sk.adaylar(tmp_path))["yerel1"] == "yerel1 yerel skill"
    st = md.stat()
    md.write_text("---\nname: yerel1\ndescription: yeni metin\n---\n", encoding="utf-8")
    os.utime(md, ns=(st.st_atime_ns, st.st_mtime_ns))
    assert dict(sk.adaylar(tmp_path))["yerel1"] == "yerel1 yerel skill"  # mtime aynı → önbellek
    os.utime(md, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
    assert dict(sk.adaylar(tmp_path))["yerel1"] == "yeni metin"


class Kayit:
    """Sahte taşıyıcı: choice → olasılık haritası, noul → ada göre p."""
    def __init__(self, olas=None, p=None, hata=None):
        self.olas, self.p, self.hata, self.istekler = olas, p or {}, hata, []

    def __call__(self, url, basliklar, govde):
        if self.hata:
            raise self.hata
        g = json.loads(govde)
        self.istekler.append(g)
        out = {}
        for ad, s in g["questions"].items():
            if s["type"] == "choice":
                pr = {k: v for k, v in (self.olas or {}).items() if k in s["criteria"]}
                pr = pr or {k: 1 / len(s["criteria"]) for k in s["criteria"]}
                out[ad] = {"type": "choice", "choice": max(pr, key=pr.get), "probabilities": pr, "confidence": max(pr.values())}
            else:
                hedef = next(a for a in self.p_adlari(s))
                out[ad] = {"type": "noul", "noul": self.p.get(hedef, 0.1)}
        return 200, {}, json.dumps({"answers": out, "usage": {"prompt_tokens": 100, "cost": 0.0001}}).encode()

    def p_adlari(self, s):
        return [a for a in self.p if f"`{a}`" in s["instructions"]] or ["?"]


def tas(g, **kw):
    return c.Tasiyici(env=ENV, gonder=g, uyu=lambda s: None, tekrar=0, en_fazla=9, **kw)


ADAY = [(f"skill-{i:03d}", f"açıklama {i}") for i in range(417)]
BANT = dict(c.VARSAYILAN_BANT)


def test_417_aday_asama1_tek_istek_dilim_210_hicbiri():
    g = Kayit()
    sk.yonlendir("fatura PDF'i oluştur", tas(g), BANT, ADAY)
    s1 = g.istekler[0]["questions"]
    assert len(s1) == 2
    for q in s1.values():
        assert q["type"] == "choice" and sk.HICBIRI in q["criteria"] and len(q["criteria"]) - 1 <= 210


def test_30k_ustu_soru_dilimi_kuculur():
    uzun = [(f"u{i:03d}", "😀" * 200) for i in range(210)]
    dl = sk.dilimle(uzun)
    assert len(dl) > 1 and sum(map(len, dl)) == 210
    assert all(c.token(json.dumps(sk.soru1(d), ensure_ascii=False)) <= sk.SORU_TOKEN for d in dl)


def test_asama1_en_fazla_10_aday_hicbiri_ve_kucuk_p_elenir():
    olas = {sk.HICBIRI: 0.5, "skill-400": 0.01, **{f"skill-{i:03d}": 0.03 + i / 1000 for i in range(12)}}
    ilk, _ = sk.yonlendir("x", tas(Kayit(olas)), BANT, ADAY)
    assert len(ilk) == 10 and sk.HICBIRI not in ilk and "skill-400" not in ilk
    assert ilk[0] == "skill-011"


def test_istem_basina_tam_2_istek_ve_asama2_tek_istek():
    g = Kayit({"skill-001": 0.6, "skill-002": 0.3}, p={"skill-001": 0.95, "skill-002": 0.9})
    ilk, sonuc = sk.yonlendir("x", tas(g), BANT, ADAY)
    assert len(g.istekler) == 2
    assert all(q["type"] == "noul" for q in g.istekler[1]["questions"].values())
    assert [s["ad"] for s in sonuc] == ["skill-001", "skill-002"]


def _hook(g, env=HOOK_ENV, ev=None, prompt="PDF fatura üret", gun="2026-09-23"):
    return sk.hook(json.dumps({"prompt": prompt}), env, ev=ev, gonder=g, bugun=gun, aday=ADAY)


def test_act_altinda_enjeksiyon_yok_ustunde_var(tmp_path):
    assert _hook(Kayit({"skill-001": 0.9}, p={"skill-001": 0.7}), ev=tmp_path) == ""
    o = json.loads(_hook(Kayit({"skill-001": 0.9}, p={"skill-001": 0.95}), ev=tmp_path))
    assert o["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    assert o["hookSpecificOutput"]["additionalContext"] == "Jev skill önerisi: skill-001"


def test_hook_fail_open(tmp_path):
    assert _hook(Kayit(hata=socket.timeout("zaman")), ev=tmp_path) == ""
    assert _hook(Kayit(hata=RuntimeError("beklenmedik")), ev=tmp_path) == ""
    assert _hook(lambda u, b, v: (503, {}, b"{}"), ev=tmp_path) == ""
    g = Kayit()
    assert _hook(g, env={"JEV_SKILL_HOOK": "1"}, ev=tmp_path) == "" and g.istekler == []


def test_hook_cli_exit0_cikti_yok(tmp_path, monkeypatch, capsys):
    import io
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"prompt": "x"})))
    monkeypatch.setattr(sk, "adaylar", lambda ev=None: ADAY)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    kod = cli.main(["hook"], env=HOOK_ENV, gonder=Kayit(hata=RuntimeError("x")), uyu=lambda s: None)
    o = capsys.readouterr()
    assert kod == 0 and o.out == "" and o.err == ""


def test_env_kapisi_kapaliyken_aga_cikmaz(tmp_path):
    g = Kayit()
    assert _hook(g, env=ENV, ev=tmp_path) == "" and g.istekler == []
    assert _hook(g, env={**ENV, "JEV_SKILL_HOOK": "0"}, ev=tmp_path) == "" and g.istekler == []


def test_gunluk_tavan_doluyken_aga_cikmaz_ertesi_gun_sifirlanir(tmp_path):
    yol = tmp_path / ".config" / "jev" / "gunluk.json"
    yol.parent.mkdir(parents=True)
    yol.write_text(json.dumps({"2026-09-23": 2}), encoding="utf-8")
    env = {**HOOK_ENV, "JEV_SKILL_GUNLUK": "2"}
    g = Kayit()
    _hook(g, env=env, ev=tmp_path)
    assert g.istekler == []
    _hook(g, env=env, ev=tmp_path, gun="2026-09-24")
    assert len(g.istekler) >= 1
    assert json.loads(yol.read_text(encoding="utf-8")) == {"2026-09-24": 1}


def test_istem_redakte_edilir(tmp_path):
    g = Kayit()
    _hook(g, ev=tmp_path, prompt=f"TCKN {TCKN} için skill?")
    assert g.istekler and all(TCKN not in json.dumps(i["state"]) for i in g.istekler)


def test_python_m_jev_help():
    r = subprocess.run([sys.executable, "-m", "jev", "--help"], cwd=Path(__file__).parents[1], capture_output=True)
    assert r.returncode == 0 and b"skill" in r.stdout
