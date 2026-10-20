"""Küçük fikstür: python -m pytest test_katalog_son.py"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import katalog_son as s


def _k(i, ad, tur="skill", kaynak="cc-skills", grup="", aciklama="", bayt=10, kat="diğer"):
    return {"id": i, "ad": ad, "tur": tur, "kaynak": kaynak, "yol": f"x/{i}", "aciklama": aciklama, "bayt": bayt,
            "kopya_grubu": grup, "kategori_tahmin": kat}


def test_karar_oylari():
    assert s.karar({"oy1": "token", "oy2": "token"}, "diğer") == ("token", "iki-oy")
    assert s.karar({"oy1": "token", "oy2": "belge"}, "diğer") == (None, "bekliyor")
    assert s.karar({"oy1": "token", "oy2": "belge", "oy3": "belge"}, "diğer") == ("belge", "üç-oy")
    assert s.karar({"oy1": "token", "oy2": "belge", "oy3": "3d"}, "belge") == ("belge", "düşük")
    assert s.karar({"oy1": "uydurma"}, "3d") == ("3d", "kural")


def test_guven_ve_token_ipucu():
    assert s.kural_guven(_k("a", "blender-mesh", aciklama="blender mesh shader")) == "yüksek"
    assert s.kural_guven(_k("b", "x", aciklama="react test")) == "düşük"
    assert s.oylanacak(_k("c", "ozet-hafiza", aciklama="blender blender oturum hafıza", kat="3d"))  # yüksek ama token ipucu
    assert not s.oylanacak(_k("d", "m", tur="model", kat="diğer"))


def test_kullanim_ayristirma():
    assert s.ilk_sozcukler('cd /c/x && FOO=1 rtk git status | C:\\py\\python.exe -X a') == ["cd", "rtk", "python"]
    assert s.mcp_sunucu("mcp__plugin_context-mode_context-mode__ctx_search") == "context-mode"
    assert s.mcp_sunucu("mcp__blender__execute") == "blender"
    say = __import__("collections").Counter()
    s.satir_say({"type": "assistant", "timestamp": "2026-10-10", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "superpowers:Brainstorming"}},
        {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "okuyucu"}}]}}, say, "2026-09-15")
    s.satir_say({"type": "assistant", "timestamp": "2026-08-01", "message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "eski"}}]}}, say, "2026-09-15")
    assert say["skill", "brainstorming"] == 1 and say["agent", "okuyucu"] == 1 and say["skill", "eski"] == 0


def test_katman_kanonik():
    rows = [_k("k1", "departman-x"), _k("k2", "kardes", kaynak="plugin:p@m"), _k("k3", "araç-a", kaynak="plugin:p@m"),
            _k("k4", "yalniz"), _k("k5", "az-kullanilan"), _k("k6", "aday-x", tur="aday"),
            _k("g1", "dup", grup="ad:dup", bayt=5), _k("g2", "dup", grup="ad:dup", bayt=9)]
    kull = {"k1": 0, "k2": 0, "k3": 4, "k4": 0, "k5": 1, "k6": 0, "g1": 0, "g2": 0}
    kat = s.katmanla(rows, kull, {"departman-x"})
    assert [kat[i] for i in ("k1", "k2", "k3", "k4", "k5", "k6")] == ["A", "B", "A", "C", "B", "-"]
    kan, fark = s.kanonikle(rows, bilgi=lambda y: {"x/g1": (2.0, "aa"), "x/g2": (1.0, "bb")}.get(y, (0, None)))
    assert kan["g1"] == kan["g2"] == "g1" and fark["g2"] is True and kan["k4"] == "k4"


def test_kullanim_esle_plugin_toplami():
    rows = [_k("p", "pwt", tur="plugin", kaynak="plugins"), _k("s", "kos", kaynak="plugin:pwt@m"), _k("c", "rtk", tur="cli")]
    out = s.kullanim_esle(rows, {"skill\tkos": 2, "cli\trtk": 7})
    assert out == {"p": 2, "s": 2, "c": 7}


def test_modeller_tsv(tmp_path):
    j = tmp_path / "m.json"
    j.write_text(json.dumps({"data": [{"id": "openrouter/a/coder:free", "owned_by": "openrouter", "capabilities": {"vision": True}, "context_length": 9},
                                      {"id": "x/tts-1", "owned_by": "x", "type": "audio", "capabilities": {}}]}), encoding="utf-8")
    assert s.modeller_tsv(j, tmp_path / "m.tsv") == 2
    L = (tmp_path / "m.tsv").read_text(encoding="utf-8").splitlines()
    assert L[1] == "openrouter/a/coder:free\topenrouter\ttrue\t1\t1\t0\t1\t9"
    assert L[2].split("\t")[4:6] == ["0", "1"]  # görsel 0, ses 1


def test_aciklamasiz_ilk_satirlar(tmp_path):
    assert s.aciklamasiz(_k("a", "x")) and s.aciklamasiz(_k("a", "x", aciklama="!/usr/bin/env bash"))
    assert s.aciklamasiz(_k("a", "uvx", aciklama="uvx 0.12.12 (c4be)")) and s.aciklamasiz(_k("a", "h", aciklama="tel.sh"))
    assert not s.aciklamasiz(_k("a", "x", aciklama="Builds Remix routes"))
    (tmp_path / "SKILL.md").write_text("\n".join(f"satır {i}" for i in range(40)), encoding="utf-8")
    k = _k("a", "x")
    k["yol"] = str(tmp_path)
    assert s.ilk_satirlar(k).endswith("satır 29")
    k["yol"] = str(tmp_path / "liste.json")
    (tmp_path / "liste.json").write_text("{}", encoding="utf-8")
    assert s.ilk_satirlar(k) == ""
    ic = tmp_path / "pkt" / "pkt"  # paket zip açılımı X/X/SKILL.md
    ic.mkdir(parents=True)
    (ic / "SKILL.md").write_text("description: iç içe", encoding="utf-8")
    k["yol"] = str(tmp_path / "pkt")
    assert s.ilk_satirlar(k) == "description: iç içe"


def test_claudeai_kaydi_synced_kopyadan(tmp_path, monkeypatch):
    d = tmp_path / ".claude" / "skills" / "synced" / "u1" / "kb"
    d.mkdir(parents=True)
    (d / "README.md").write_text("# KB arama", encoding="utf-8")
    monkeypatch.setattr(s.Path, "home", lambda: tmp_path)
    k = _k("a", "kb")
    k["yol"] = ".kos/kopru/claudeai_adlar.json"
    assert s.ilk_satirlar(k) == "# KB arama"


def test_onbellek_v2_v1in_yerine_gecer(tmp_path):
    v1, v2 = tmp_path / "1.jsonl", tmp_path / "2.jsonl"
    v1.write_text('{"k": "a", "kol": "oy1", "c": "bilim"}\n{"k": "a", "kol": "oy3", "c": "diğer"}\n{"k": "b", "kol": "oy1", "c": "3d"}\n', encoding="utf-8")
    v2.write_text('{"k": "a", "kol": "oy1", "c": "veri-db"}\n', encoding="utf-8")
    oy = s.onbellek((v1, v2))
    assert oy["a"] == {"oy1": "veri-db"} and oy["b"] == {"oy1": "3d"}


def test_dengeli_ve_etiketler(tmp_path, monkeypatch):
    rows = [dict(_k(f"k{i:03d}", f"a{i}"), kategori_son="3d" if i < 50 else "bilim") for i in range(60)]
    sec = s.dengeli(rows, n=20, tohum=18)
    assert len(sec) == 20 and sum(k["kategori_son"] == "bilim" for k in sec) == 10  # azınlık kategori yarıyı alır
    assert sec == s.dengeli(rows, n=20, tohum=18) and sec != s.dengeli(rows, n=20, tohum=19)
    assert not {k["id"] for k in sec} & {k["id"] for k in s.dengeli(rows, n=20, tohum=18, haric={k["id"] for k in sec})}
    assert s.satir(rows[0]).startswith("k000 | skill | a0 | ") and s.satir(rows[0]).endswith("(açıklama yok)")
    monkeypatch.setattr(s, "PARTI_DIZIN", tmp_path)
    (tmp_path / "p00.out.jsonl").write_text('{"id": "k001", "ana": "3d", "ikincil": ""}\n\n', encoding="utf-8")
    assert s.etiketler() == {"k001": {"id": "k001", "ana": "3d", "ikincil": ""}}


def test_etiketler_v5_oncelik(tmp_path, monkeypatch):
    monkeypatch.setattr(s, "PARTI_DIZIN", tmp_path)
    for ad, c in (("pzv00", "token"), ("pz00", "3d"), ("py00", "bilim"), ("p00", "belge")):
        (tmp_path / f"{ad}.out.jsonl").write_text(json.dumps({"id": "k1", "ana": c}) + "\n", encoding="utf-8")
    monkeypatch.setattr(s.Path, "glob", lambda self, d: [tmp_path / f"{a}.out.jsonl" for a in ("pzv00", "pz00", "py00", "p00")])
    assert s.etiketler()["k1"]["ana"] == "token"  # glob sırası ters gelse de pzv (tanim-v5) kazanır
    (tmp_path / "pzw00.out.jsonl").write_text(json.dumps({"id": "k1", "ana": "araştırma"}) + "\n", encoding="utf-8")
    monkeypatch.setattr(s.Path, "glob", lambda self, d: [tmp_path / f"{a}.out.jsonl" for a in ("pzw00", "pzv00", "p00")])
    assert s.etiketler()["k1"]["ana"] == "araştırma"  # pzw (tanim-v6) pzv'yi ezer


def test_capa(tmp_path):
    import capa
    for d, m in (("test-qa", "## Adımlar\n1. `survey-kit` x `run-tests`\n## Kapılar\n`gecen-soz`\n"),
                 ("arastirma-ogrenme", "`giris-sozu`\n## Dizin\najan:ara-web-kazima\ncli:survey-kit: y\none-on-one: torba\n"),
                 ("diger", "## Sıra\n| Blender, 3D | `blender` → ajan `bl-*` |\n| Mobil | `expo` |\n"), ("frontend", "## Çakışma\nbl-uv-acma: z\n")):
        (tmp_path / f"departman-{d}").mkdir()
        (tmp_path / f"departman-{d}" / "SKILL.md").write_text(m, encoding="utf-8")
    c = capa.capalar(tmp_path, s.norm)
    assert capa.capa("ara-web-kazima", c, s.norm) == {"araştırma"}
    assert capa.capa("run-tests", c, s.norm) == {"test-qa"}
    assert capa.capa("survey-kit", c, s.norm) == {"test-qa", "araştırma"}  # çok müdür → etiketçi seçer
    assert capa.capa("bl-uv-acma", c, s.norm) == {"3d", "frontend-tasarım"}  # joker + tam ad birleşir
    assert capa.capa("expo", c, s.norm) == {"diğer"} and capa.capa("blender", c, s.norm) == {"3d"}
    assert capa.capa("departman-frontend", c, s.norm) == {"frontend-tasarım"} and not capa.capa("yok", c, s.norm)
    # yalnız elle yazılmış liste: Dizin'in anahtar sözcükle yerleşen öneksiz satırı, giriş ve Kapılar çapa değil
    assert not any(capa.capa(a, c, s.norm) for a in ("one-on-one", "gecen-soz", "giris-sozu"))


def test_ad_esitle():
    rows = [dict(_k("a", "audit"), kategori_son="belge", kullanim_30g=0), dict(_k("b", "audit", tur="komut"), kategori_son="belge", kullanim_30g=0),
            dict(_k("c", "Audit", aciklama="x"), kategori_son="3d", kullanim_30g=5),
            dict(_k("d", "doc"), kategori_son="belge", kullanim_30g=0), dict(_k("e", "doc", aciklama="y"), kategori_son="bilim", kullanim_30g=2),
            dict(_k("h1", "Stop", tur="hook"), kategori_son="token", kullanim_30g=0), dict(_k("h2", "Stop", tur="hook", aciklama="z"), kategori_son="3d", kullanim_30g=0)]
    assert s.ad_esitle(rows) == 2
    assert [k["kategori_son"] for k in rows] == ["belge", "belge", "belge", "bilim", "bilim", "token", "3d"]  # çoğunluk; eşitlikte çok kullanılan; hook hariç


def test_hook_mcp_baglami(monkeypatch):
    rows = [_k("p", "chrome-devtools-mcp", tur="plugin", aciklama="Chrome DevTools ile canlı tarayıcı hata ayıklama"),
            _k("q", "octo", tur="plugin", aciklama="Çoklu ajan orkestrasyonu")]
    monkeypatch.setattr(s, "_ad_aciklamalari", lambda: s.ad_sozlugu(rows))
    h = _k("h", "PreCompact:*", tur="hook", kaynak="plugin:octo@nyldn", aciklama="pre-compact.sh")
    m = _k("m", "chrome-devtools", tur="mcp", kaynak="cc-user-mcp", aciklama="npx")
    assert "olay PreCompact:*" in s.satir(h) and "pre-compact.sh" in s.satir(h) and "Çoklu ajan" in s.satir(h)
    assert "komut npx" in s.satir(m) and "canlı tarayıcı" in s.satir(m)


def test_mcp_araclari(tmp_path, monkeypatch):
    (tmp_path / "kullanim-30g.json").write_text(json.dumps({"sayim": {
        "mcp-arac\tmcp__plugin_cd_chrome-devtools__take_screenshot": 3,
        "mcp-arac\tmcp__headroom__headroom_retrieve": 1, "cli\tmcp": 2}}), encoding="utf-8")
    monkeypatch.setattr(s, "BURASI", tmp_path)
    monkeypatch.setattr(s, "_ARACLAR", [], raising=False)
    monkeypatch.setattr(s, "_ad_aciklamalari", lambda: {})
    assert s.mcp_araclari()["chrome-devtools"] == ["take_screenshot"]
    assert "araçlar headroom_retrieve" in s.satir(_k("m", "headroom", tur="mcp", kaynak="cc-user-mcp", aciklama="uvx"))


def test_uzlas():
    byid = {i: _k(i, i) for i in "abc"}
    cl = {s.anahtar(byid[i]): {"id": i, "ana": "belge"} for i in "abc"}
    y = {"a": {"ana": "belge"}, "b": {"ana": "3d"}, "c": {"ana": "3d"}}
    s.uzlas(cl, y, {"c": {"id": "c", "ana": "bilim"}}, byid)
    assert [(cl[s.anahtar(byid[i])]["ana"], cl[s.anahtar(byid[i])]["guven"]) for i in "abc"] == \
        [("belge", "uyuştu"), ("belge", "ayrışık"), ("bilim", "hakem")]


def test_etiketler_pzx_oncelik():
    assert s._oncelik(Path("pzx00.out.jsonl")) > s._oncelik(Path("pzw06.out.jsonl")) > s._oncelik(Path("pzv18.out.jsonl"))
