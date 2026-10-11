import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import skill_filo_denetim as fd  # noqa: E402


def _skill(d, ad, aciklama, govde="# Başlık\nkısa\n"):
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: {aciklama}\n---\n{govde}", encoding="utf-8")


def _kur(tmp):
    ev = tmp / "ev"
    sk = ev / ".claude/skills"
    _skill(sk / "iyi", "iyi", "PDF birleştirir. Use when the user asks to merge PDFs.", "# İyi\nBak [ref](references/a.md)\n")
    (sk / "iyi/references").mkdir()
    (sk / "iyi/references/a.md").write_text("x", encoding="utf-8")
    _skill(sk / "sisman", "sisman", "Kısa.", "# Sisman\n" + ("kelime " * 2000) + "\n[yok](references/kayip.md)\nmcp__hayalet__ara kullan\n"
           "ALWAYS use git rebase here.\nNEVER use git rebase on main.\n")
    _skill(sk / "aile", "aile", "Aile girişi. Use when X.")
    _skill(sk / "aile/alt", "alt", "Alt skill. Use when Y.")
    _skill(sk / "aile/alt2", "sisman", "Sisman'ın başka sürümü. Use when Q.", "# farklı\n[yer](<project>.md)\n")
    _skill(sk / ".trash/eski", "eski", "silinmiş")
    pl = ev / ".claude/plugins/cache/mk/pl/1.0"
    _skill(pl / "skills/iyi", "iyi", "PDF birleştirir. Use when the user asks to merge PDFs.", "# İyi\nBak [ref](references/a.md)\n")
    (ev / ".claude/plugins/installed_plugins.json").write_text(json.dumps(
        {"plugins": {"pl@mk": [{"installPath": str(pl)}]}}), encoding="utf-8")
    (ev / ".claude.json").write_text(json.dumps({"mcpServers": {"gercek": {}}}), encoding="utf-8")
    sy = sk / "synced/uuid/pk-paket"
    _skill(sy, "pk-paket", "Paket girişi, Z işleri. Use when Z is needed.", "# P\n")
    (sy / "skills/uye").mkdir(parents=True)
    (sy / "skills/uye/TALIMAT.md").write_text("---\nname: uye\ndescription: Üye skill W yapar. Use when W is needed.\n---\n# U\n"
                                            "mcp__gercek__x\n[r](references/ic.md)\n", encoding="utf-8")
    (sy / "skills/uye/REFERANS.md").write_text("## [references/ic.md]\nx\n", encoding="utf-8")
    return ev


def test_kaynaklar_ve_sorunlar(tmp_path):
    ev = _kur(tmp_path)
    satir = {(k["kaynak"], k["ad"]): k for k in fd.denetle(fd.topla(ev), fd.mcp_adlari(ev))}
    assert set(satir) == {("gevşek", "iyi"), ("gevşek", "sisman"), ("gevşek", "aile"), ("gevşek", "alt"), 
                          ("plugin", "iyi"), ("claude.ai", "pk-paket"), ("claude.ai", "uye")}
    assert satir[("gevşek", "alt")]["aile"] == "aile"
    assert satir[("claude.ai", "uye")]["aile"] == "pk-paket"
    iyi, sis = satir[("gevşek", "iyi")], satir[("gevşek", "sisman")]
    assert iyi["sorunlar"] == "" and iyi["kopya"] == 1  # plugin kopyasıyla aynı ad+gövde: çift değil, kopya
    for s in ("tetik_yok", "aciklama_kisa", "kirik_bag", "eski_arac", "celiski", "pd_yok"):
        assert s in sis["sorunlar"].split(","), s
    assert sis["kirik"] == "references/kayip.md" and sis["eski_arac"] == "mcp__hayalet"
    assert sis["govde_jeton"] > 2000
    assert satir[("claude.ai", "uye")]["sorunlar"] == ""  # kurulu MCP + REFERANS.md'ye birleşmiş bağlantı


def test_ozet_puan(tmp_path):
    ev = _kur(tmp_path)
    satirlar = fd.denetle(fd.topla(ev), fd.mcp_adlari(ev))
    sayi, aile = fd.ozet(satirlar)
    assert sayi["cift"] == 2 and sayi["pd_yok"] == 1 and sayi.get("kirik_bag") == 2  # sisman + references/a.md'si olmayan plugin kopyası
    assert aile["iyi"] == 100 and aile["sisman"] < 100 and aile["pk-paket"] == 100
