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


def test_yuklenmeyen_kopyalar_haric(tmp_path):
    # kök neden: ecc'nin docs/<dil> ve .kiro kopyaları CC'ye yüklenmez ama denetime ve açıklama hedefine giriyordu
    ev = _kur(tmp_path)
    pl = ev / ".claude/plugins/cache/mk/pl/1.0"
    for d in ("docs/ja-JP/skills/iyi", ".kiro/skills/iyi", ".agents/skills/iyi", "skills/kat/derin"):
        _skill(pl / d, "iyi", "kopya")
    _skill(pl / "ozel/ek", "ek", "Özel yol. Use when E.")
    (pl / ".claude-plugin").mkdir()
    (pl / ".claude-plugin/plugin.json").write_text(json.dumps({"skills": ["./ozel/ek", "./skills/"]}), encoding="utf-8")
    kok = ev / ".claude/plugins/cache/mk/tek/1.0"
    _skill(kok, "tek", "Kök skill. Use when T.")
    _skill(kok / "docs/es", "tek", "copia")
    sk = ev / ".claude/skills"
    _skill(sk / "aile/.cursor/skills/alt", "alt", "kopya")
    _skill(sk / "aile/docs/zh-CN/skills/alt", "alt", "kopya")
    paket = ev / ".claude/plugins/cache/mk/paket/1.0"
    _skill(paket / "pa", "pa", "Paket üyesi. Use when P.")
    _skill(paket / "pb", "pb", "listede yok")
    mp = ev / ".claude/plugins/marketplaces/mk/.claude-plugin/marketplace.json"
    mp.parent.mkdir(parents=True)
    mp.write_text(json.dumps({"plugins": [{"name": "paket", "skills": ["./pa"]}]}), encoding="utf-8")
    ip = ev / ".claude/plugins/installed_plugins.json"
    ip.write_text(json.dumps({"plugins": {"pl@mk": [{"installPath": str(pl)}], "tek@mk": [{"installPath": str(kok)}],
                                          "paket@mk": [{"installPath": str(paket)}]}}), encoding="utf-8")
    haric = __import__("collections").Counter()
    yollar = {Path(k["yol"]).relative_to(ev).as_posix() for k in fd.topla(ev, haric)}
    assert {y for y in yollar if "plugins" in y} == {".claude/plugins/cache/mk/pl/1.0/skills/iyi/SKILL.md",
                                                     ".claude/plugins/cache/mk/pl/1.0/ozel/ek/SKILL.md",
                                                     ".claude/plugins/cache/mk/tek/1.0/SKILL.md",
                                                     ".claude/plugins/cache/mk/paket/1.0/pa/SKILL.md"}  # marketplace skills
    assert not any("docs/" in y or "/." in y.replace("/.claude/", "/") for y in yollar)
    assert haric == {"docs": 3, ".kiro": 1, ".agents": 1, ".cursor": 1, "skills/<kat>/<ad>": 1, "pb": 1}


def test_tetik_cok_dilli():
    for metin in ("Usar cuando se pide x.", "在需要X时使用。", "何时使用", "Xが必要な時に使用。", "X가 필요할 때 사용."):
        assert fd.TETIK.search(metin), metin
