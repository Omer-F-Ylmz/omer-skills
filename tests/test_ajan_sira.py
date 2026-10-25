"""TOKEN-3 K11: ajan-sira.tsv isteğe bağlı 4. sütun efor=medium|high → --effort; yoksa eski davranış."""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos/kopru"))  # ajan_sira / kontrol_ozet → maliyet_defter
_s = importlib.util.spec_from_file_location("ajan_sira", Path(__file__).resolve().parents[1] / ".kos/kopru/ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)


@pytest.fixture(autouse=True)
def _beyin_olay_izole(tmp_path, monkeypatch):
    """is_kaydi 2. beyin olay günlüğüne yazar; testler gerçek beyin-olay.jsonl'ı kirletmesin."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import beyin_dusun
    monkeypatch.setattr(beyin_dusun, "OLAY", tmp_path / "beyin-olay.jsonl")


def test_ders_onek_bayrakli(tmp_path, monkeypatch):
    monkeypatch.setenv("OGRENME_DIZIN", str(tmp_path))
    bayrak = tmp_path / "ders.bayrak"
    monkeypatch.setattr(ajan_sira, "DERS_DOSYA", bayrak)
    gorev = "rapor dosyasını yazmadan önce teslim koşullarını doğrula"
    assert ajan_sira.ders_onek(gorev) == ""  # bayrak kapalı
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools/ogrenme"))
    import ders
    ders.ekle("general-purpose", "Rapor teslim koşulu", "rapor yazmadan önce", "Teslim koşullarını doğrula.", "basari", "t", gorev=gorev)
    assert ajan_sira.ders_onek(gorev) == ""  # ders var ama bayrak kapalı
    bayrak.write_text("1")
    assert "Rapor teslim koşulu" in ajan_sira.ders_onek(gorev)
    assert ajan_sira.ders_onek("alakasız zeytin hasadı") == ""  # ilgisiz görev → boş blok, 0 jeton


def test_dorduncu_sutun_efor(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("# yorum\na\ti.md\nb\ti.md\t\tefor=medium\nc\ti.md\tx::y\tefor=high\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "", None, None, None), ("b", "i.md", "", "medium", None, None, None), ("c", "i.md", "x::y", "high", None, None, None)]


def test_gecersiz_efor_reddedilir(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tefor=max\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    with pytest.raises(ValueError):
        ajan_sira.kuyruk()


def test_node_heap_tavani(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")
    monkeypatch.delenv("NODE_OPTIONS", raising=False)
    assert "--max-old-space-size=2048" in ajan_sira.baslat_argv("")[1]["NODE_OPTIONS"]
    monkeypatch.setenv("NODE_OPTIONS", "--max-old-space-size=512 --trace-warnings")
    assert ajan_sira.baslat_argv("")[1]["NODE_OPTIONS"] == "--max-old-space-size=512 --trace-warnings"  # var olan tavan ezilmez


def test_baslat_argv_env(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")  # canlı bayraktan bağımsız
    monkeypatch.setenv("CLAUDE_CODE_EFFORT_LEVEL", "high")
    argv, env = ajan_sira.baslat_argv("medium")
    assert argv[-2:] == ["--effort", "medium"] and "CLAUDE_CODE_EFFORT_LEVEL" not in env
    argv, env = ajan_sira.baslat_argv("")
    assert argv == ajan_sira.ARGV and isinstance(env, dict)


def test_ruflo_ogren_araclari_kapanmaz(tmp_path, monkeypatch):
    """RUFLO-BAG-1: ogren_blok'un istediği hooks_intelligence_pattern-* araçları KEEP'te olmalı, --disallowedTools'a düşmemeli."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import mcp_profil
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")
    monkeypatch.setattr(mcp_profil, "ARACLAR", tmp_path / "araclar.json")
    (tmp_path / "araclar.json").write_text('{"ruflo": ["hooks_intelligence_pattern-search", "hooks_intelligence_pattern-store", "memory_delete"]}', encoding="utf-8")
    mcp = tmp_path / "mcp.json"
    mcp.write_text('{"mcpServers": {"ruflo": {}}}', encoding="utf-8")
    argv, _ = ajan_sira.baslat_argv("", "haiku", mcp)
    assert argv[argv.index("--disallowedTools") + 1] == "mcp__ruflo__memory_delete"


def test_ajan_env_mcp_timeout(monkeypatch):
    """RUFLO-BAG-1: ruflo soğuk başlangıç yük altında 30 sn varsayılanı aşıyor ('failed'); ajan env'inde MCP_TIMEOUT ≥120 sn."""
    monkeypatch.delenv("MCP_TIMEOUT", raising=False)
    _, env = ajan_sira.baslat_argv("", "haiku")
    assert int(env["MCP_TIMEOUT"]) >= 120000


def test_baslat_argv_mcp_ertele(tmp_path, monkeypatch):
    """MCP-AÇ-2: mcp verilince KEEP dışı araçlar kapalı; CC_MCP_ERTELE=0 ya da mcp yoksa eski argv."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import mcp_profil
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")
    monkeypatch.setattr(mcp_profil, "ARACLAR", tmp_path / "araclar.json")
    (tmp_path / "araclar.json").write_text('{"rea": ["inspect_web_page", "zz_gereksiz"], "blender": ["a"]}', encoding="utf-8")
    mcp = tmp_path / "mcp.json"
    mcp.write_text('{"mcpServers": {"rea": {}, "blender": {}}}', encoding="utf-8")
    argv, _ = ajan_sira.baslat_argv("", "haiku", mcp)
    assert "ToolSearch" in argv[argv.index("--tools") + 1]  # ERİŞİM-TAM-1: ertelemeyi profil sağlar
    assert argv[argv.index("--disallowedTools") + 1] == "mcp__rea__zz_gereksiz"  # KEEP'te olmayan MCP (blender) tam kalır
    assert json.loads(Path(argv[argv.index("--settings") + 1]).read_text(encoding="utf-8"))["env"]["ENABLE_TOOL_SEARCH"] == "true"
    assert ajan_sira.baslat_argv("", "haiku")[0] == [a if a != "opus" else "haiku" for a in ajan_sira.ARGV]  # mcp yok → dokunulmaz
    monkeypatch.setenv("CC_MCP_ERTELE", "0")
    assert "--disallowedTools" not in ajan_sira.baslat_argv("", "haiku", mcp)[0]


def test_is_kaydi(tmp_path, monkeypatch):
    """TOKEN-3 K17: biten işin JSON'u → is-kaydi.tsv tek satır; bozuk JSON da satır yazar (rc ile)."""
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    (tmp_path / "a.json").write_text('uyarı satırı\n{"subtype":"success","num_turns":7,"total_cost_usd":1.5,"result":"tamam\\nKalite: kör puan 3/3 geçti",'
                                     '"usage":{"input_tokens":100,"cache_creation_input_tokens":1000,"cache_read_input_tokens":10000,"output_tokens":20}}\n', encoding="utf-8")
    (tmp_path / "b.json").write_text("Traceback", encoding="utf-8")
    assert ajan_sira.is_kaydi("a", 0, 12.4, "medium", "haiku") is True
    assert ajan_sira.is_kaydi("b", 1, 0.2, "", "haiku") is False
    s = (tmp_path / "is.tsv").read_text(encoding="utf-8").splitlines()
    assert s[0].startswith("zaman\tis\t")
    assert s[1].split("\t")[1:] == ["a", "medium", "12", "7", "2450", "1.50", "success", "Kalite: kör puan 3/3 geçti"]
    assert s[2].split("\t")[1:] == ["b", "-", "0", "0", "0", "0.00", "rc1", "-"]
    d = (tmp_path / "maliyet.tsv").read_text(encoding="utf-8").splitlines()
    assert d[1].split("\t")[1:] == ["a", "haiku-medium", "1.50", "a", "1"] and d[2].split("\t")[1:] == ["b", "haiku", "0.00", "b", "0"]


def test_is_kaydi_beyne_olay_dusurur(tmp_path, monkeypatch):
    """BEYIN-CANLI-1: iş bitince beyin-olay.jsonl'a 'is' olayı (iş · model · $ · KABUL/DUR) düşer."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import beyin_dusun
    monkeypatch.setattr(beyin_dusun, "OLAY", tmp_path / "olay.jsonl")
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    (tmp_path / "a.json").write_text('{"subtype":"success","num_turns":3,"total_cost_usd":0.2,"result":"tamam"}\n', encoding="utf-8")
    assert ajan_sira.is_kaydi("a", 0, 2.0, "", "haiku") is True
    o = [json.loads(s) for s in (tmp_path / "olay.jsonl").read_text(encoding="utf-8").splitlines()]
    assert o[0]["tur"] == "is" and "a · haiku · $0.20" in o[0]["ozet"] and "KABUL" in o[0]["ozet"]


def test_basamak_sec_merdiven(tmp_path, monkeypatch):
    """MERDIVEN: model yok → haiku medium (0); son 7 günde Haiku'da başarısız tür → sonnet medium (2); yeniden deneme basamağı aynen."""
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    ajan_sira.maliyet_defter.yaz("token-1-d1", "haiku-medium", 0.5, False)
    assert ajan_sira.basamak_sec("atlas-1-d1", None) == 1  # UCRETSIZ-MOTOR-1: 0. basamak ücretsiz; kolay işaretsiz iş haiku medium (1)
    assert ajan_sira.basamak_sec("token-2-d3", None) == 3
    assert ajan_sira.basamak_sec("token-2-d3-r", 1) == 1
    assert ajan_sira.MERDIVEN[3] == ("sonnet", "medium")


def test_kontrol_ozet_zaman_asimi(monkeypatch):
    """≤10 sn hedefi: LLM özeti süreyi aşarsa kontrol_ozet beklemez, zaman aşımı satırı döner."""
    import time
    _k = importlib.util.spec_from_file_location("kontrol_ozet", Path(__file__).resolve().parents[1] / ".kos/kopru/kontrol_ozet.py")
    kontrol_ozet = importlib.util.module_from_spec(_k)
    _k.loader.exec_module(kontrol_ozet)
    monkeypatch.setattr(kontrol_ozet, "ozet", lambda ad: (time.sleep(3), ["x"])[1])
    t0 = time.time()
    s = kontrol_ozet.ozetle(["a1"], sure=0.3)
    assert time.time() - t0 < 1.5
    assert s == [["(özet zaman aşımı) python sonuc_kisa.py --kisa a1"]]
    monkeypatch.setattr(kontrol_ozet, "ozet", lambda ad: ["hızlı"])
    assert kontrol_ozet.ozetle(["a2"]) == [["hızlı"]]


def test_butce_bul():
    """BÜTÇE-KAPI-1: görev satırındaki ≤$X okunur (virgül ya da nokta); BÜTÇE satırı ≤$ içermezse atlanır; yoksa 0,50."""
    assert ajan_sira.butce_bul("BÜTÇE Claude ≤$0,30 (Haiku).") == 0.30
    assert ajan_sira.butce_bul("BÜTÇE Claude ≤$2.50 (Sonnet)") == 2.5
    assert ajan_sira.butce_bul("3. BÜTÇE: varsayılan ≤600 token\nBÜTÇE Claude ≤$0,80") == 0.8
    assert ajan_sira.butce_bul("bütçe satırı yok") == ajan_sira.BUTCE_VARSAYILAN == 0.50


def test_baslat_argv_butce(tmp_path, monkeypatch):
    """BÜTÇE-KAPI-1: bütçe verilince --max-budget-usd claude'a geçer; verilmezse argv değişmez."""
    argv, _ = ajan_sira.baslat_argv("", "haiku", None, (), 0.3)
    assert argv[argv.index("--max-budget-usd") + 1] == "3"  # 22 Eki: bütçe hedef; sert sınır max(3, 8×hedef)
    assert "--max-budget-usd" not in ajan_sira.baslat_argv("", "haiku")[0]


def test_sonuc_temizle(tmp_path, monkeypatch):
    """BÜTÇE-KAPI-1: erisim-tam-1d (başta CLI uyarı satırı) ve bhs5-d0 (sonda kesik parça) → ad.json geçerli JSON kalır, geri kalan ad.stray.txt'ye gider."""
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    (tmp_path / "a.json").write_text('Background tasks still running 10m\n{"subtype":"success"}\n', encoding="utf-8")
    ajan_sira.sonuc_temizle("a")
    assert json.loads((tmp_path / "a.json").read_text(encoding="utf-8")) == {"subtype": "success"}
    assert (tmp_path / "a.stray.txt").read_text(encoding="utf-8") == "Background tasks still running 10m\n"
    (tmp_path / "b.json").write_text('{"subtype":"success"}\ntent_frame_ms":2398,"result_index":0}', encoding="utf-8")
    ajan_sira.sonuc_temizle("b")
    assert json.loads((tmp_path / "b.json").read_text(encoding="utf-8")) == {"subtype": "success"}
    (tmp_path / "c.json").write_text('{"subtype":"success"}\n', encoding="utf-8")
    ajan_sira.sonuc_temizle("c")  # temiz dosyaya dokunmaz
    assert not (tmp_path / "c.stray.txt").exists()


def test_butce_durdurma(tmp_path, monkeypatch):
    """BÜTÇE-KAPI-1 sahte görev: %80 uyarısı loga düşer; bütçe dolan iş (error_max_budget_usd) yeniden denenmez listesine girer ve defterde kalır."""
    import time
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(ajan_sira, "BUTCE_ASTI", set())
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    monkeypatch.setattr(ajan_sira.maliyet_defter, "BUTCE_DEFTER", tmp_path / "butce.tsv")
    logs = []
    monkeypatch.setattr(ajan_sira, "log", lambda *a: logs.append(" ".join(map(str, a))))
    (tmp_path / "f80.json").write_text('{"subtype":"success","total_cost_usd":0.25}\n', encoding="utf-8")
    assert ajan_sira.is_kaydi("f80", 0, 1.0, "", "haiku", 0.30) is True
    assert any(s.startswith("BÜTÇE %80+ f80") for s in logs)
    (tmp_path / "f100.json").write_text('{"subtype":"error_max_budget_usd","total_cost_usd":0.31}\n', encoding="utf-8")
    assert ajan_sira.is_kaydi("f100", 0, 1.0, "", "haiku", 0.30) is False
    assert ajan_sira.BUTCE_ASTI == {"f100"}
    assert ajan_sira.maliyet_defter.butce_asan(time.strftime("%Y-%m-%d")) == ["f100"]
    assert len((tmp_path / "butce.tsv").read_text(encoding="utf-8").splitlines()) == 3  # başlık + 2 iş


def test_baslat_argv_slash_bayragi(tmp_path, monkeypatch):
    """SLASH-ÖĞREN d1: bayrak varsa köprü oturumu Skill aracını alır, --disable-slash-commands düşer; yoksa değişmez."""
    bayrak = tmp_path / "slash.bayrak"
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", bayrak)
    kapali, _ = ajan_sira.baslat_argv("")
    assert "--disable-slash-commands" in kapali and "Skill" not in kapali[kapali.index("--tools") + 1].split(",")
    bayrak.write_text("1")
    acik, _ = ajan_sira.baslat_argv("")
    assert "--disable-slash-commands" not in acik and "Skill" in acik[acik.index("--tools") + 1].split(",")


def test_baslat_argv_slash_dar(tmp_path, monkeypatch):
    """SLASH-ÖĞREN d2: bayrakta dar=<küme> varsa yalnız slash-dar/<küme> eklentisi yüklenir (--setting-sources ''); düz bayrakta eklenmez."""
    bayrak = tmp_path / "slash.bayrak"
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", bayrak)
    bayrak.write_text("1")
    assert "--plugin-dir" not in ajan_sira.baslat_argv("")[0]
    bayrak.write_text("acik dar=cekirdek")
    a, _ = ajan_sira.baslat_argv("")
    assert "--setting-sources" not in a and a[a.index("--settings") + 1].endswith("birlesik-ayar.json") and a[a.index("--plugin-dir") + 1].endswith("slash-dar\cekirdek")


def test_ordu_ve_slash_dar_birlikte(tmp_path, monkeypatch):
    """ORDU-1 d2: ordu önsözü (istem) ile SLASH dar küme (argv) ayrı katmanlar; iki bayrak açıkken ikisi de çalışır, kapalıyken ordu önsözü boş."""
    ordu, slash = tmp_path / "ordu", tmp_path / "slash.bayrak"
    monkeypatch.setattr(ajan_sira, "ORDU_DOSYA", ordu)
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", slash)
    assert ajan_sira.ordu_onek() == ""
    ordu.write_text("1")
    slash.write_text("acik dar=cekirdek")
    a, _ = ajan_sira.baslat_argv("")
    assert ajan_sira.ordu_onek().startswith("ORDU-1 derleyici") and a[a.index("--plugin-dir") + 1].endswith("slash-dar\cekirdek")


def test_ordu_onsoz_somut_tetik():
    """ORDU-1 d11: önsöz soyut rol değil somut tetik + çalışır komut + görev başı ayrıştırma adımı; ≤700 karakter."""
    o = ajan_sira.ORDU_ONEK
    assert "tools/ucuz_alt.py --tur ozet" in o and (ajan_sira.KOK / "tools/ucuz_alt.py").exists()
    assert "Agent" in o and "ilk" in o.lower() and len(o) <= 700
    for tetik in ("okuma", "keşif", "log", "test"):
        assert tetik in o


def test_ordu_on_ozet_bayrakli(tmp_path, monkeypatch):
    """ORDU-1 d12: bayrak kapalı → ''; açık + ≥3 dosya → ucuz_alt çağrılır, özet eklenir; <3 dosya → çağrı yok; hata → ''."""
    bayrak = tmp_path / "on"
    monkeypatch.setattr(ajan_sira, "ON_DOSYA", bayrak)
    monkeypatch.setattr(ajan_sira, "KOK", tmp_path)
    for d in ("a.py", "b.py", "c.md"):
        (tmp_path / d).write_text("x")
    (tmp_path / ".claude/ordu3").mkdir(parents=True)
    metin = "bak a.py b.py c.md ve yok.py"
    cagri = []

    def sahte(argv, **kw):
        cagri.append(argv)
        (tmp_path / ".claude/ordu3/on-t.md").write_text("OZET")
        return type("R", (), {"returncode": 0})()
    monkeypatch.setattr(ajan_sira.subprocess, "run", sahte)
    assert ajan_sira.ordu_on_ozet("t", metin) == "" and not cagri
    bayrak.write_text("1")
    assert "OZET" in ajan_sira.ordu_on_ozet("t", metin) and cagri[0][-3:] == ["a.py", "b.py", "c.md"]
    cagri.clear()
    assert ajan_sira.ordu_on_ozet("t", "yalniz a.py b.py") == "" and not cagri
    monkeypatch.setattr(ajan_sira.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(OSError()))
    assert ajan_sira.ordu_on_ozet("t", metin) == ""


def test_arac_onek_on_soz_gorevi_korur(tmp_path, monkeypatch):
    soz = tmp_path / "on-soz.md"
    soz.write_text("ÖN SÖZ test\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "ON_SOZ", soz)
    gorev = "Görev: a.py dosyasını düzelt"
    istem = ajan_sira.arac_onek() + gorev
    assert istem.startswith("ÖN SÖZ test") and istem.endswith(gorev)


def test_arac_onek_yoksa_bos(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "ON_SOZ", tmp_path / "yok.md")
    assert ajan_sira.arac_onek() == ""


def test_cwd_sutunu_ayrisir(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tefor=medium\tcwd=Projeler/TELVE\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "medium", None, None, "Projeler/TELVE")]


def test_cwd_yoksa_baslatilmaz(tmp_path):
    assert ajan_sira.cwd_hedef(str(tmp_path / "yok")) is None  # yol yok → satır başlatılmaz
    assert ajan_sira.cwd_hedef(str(tmp_path)) == tmp_path  # var olan klasör → başlatılır


def test_cwd_sutunsuz_eski_davranis(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "", None, None, None)]
    assert ajan_sira.cwd_hedef(None) == ajan_sira.KOK
    soz = tmp_path / "on-soz.md"
    soz.write_text("ÖN SÖZ test\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "ON_SOZ", soz)
    assert ajan_sira.arac_onek() == "ÖN SÖZ test\n\n"
    assert ajan_sira.arac_onek(str(tmp_path)).startswith(f"Çalışma dizini: {tmp_path}\nÖN SÖZ test")


def test_ram_tahmin_ve_izin():
    """RAM-1: görev türüne göre başlatma tahmini (MB) + başlatmadan sonraki RAM% eşiği aşıyorsa bekle."""
    hafif = ajan_sira.tahmin_mb("kurulum notu yaz")
    site = ajan_sira.tahmin_mb("site-3d landing three.js")
    render = ajan_sira.tahmin_mb("blender render sahnesi")
    assert hafif < site < render
    assert 1564 <= hafif <= 2116  # RAM-BEKCI-3c: ölçülen ağaç (son 20 örnek) 1552–2410, medyan 1840 MB → tahmin medyanın ±%15'inde; stdio MCP 5-6'da eğim ≈0
    assert not ajan_sira.ram_izin(84, 2000, 32000, 85, False)  # 84 + %6.25 > 85 → bekle
    assert ajan_sira.ram_izin(70, 2000, 32000, 85, False)
    assert ajan_sira.ram_izin(84, 9000, 32000, 85, True)  # hiçbir şey çalışmıyorsa kilitlenmesin


def test_tekil_yonetici_kilit(tmp_path, monkeypatch):
    """TEKİL-YÖNETİCİ: canlı bir ajan_sira.py kilidi tutuyorsa ikinci kopya almaz; pid'i ölmüş kilit devralınır."""
    kilit = tmp_path / "ajan-sira.kilit"
    monkeypatch.setattr(ajan_sira, "KILIT", kilit)
    betik = tmp_path / "ajan_sira.py"
    betik.write_text("import time\ntime.sleep(120)\n", encoding="utf-8")
    canli = subprocess.Popen([sys.executable, str(betik)])
    try:
        kilit.write_text(f"{canli.pid} 00:00:00", encoding="utf-8")
        assert ajan_sira.kilit_al() is False
        canli.kill()
        canli.wait()
        assert ajan_sira.kilit_al() is True
        assert kilit.read_text(encoding="utf-8").split()[0] == str(os.getpid())
    finally:
        canli.kill()


def test_hayalet_basladi_calisan_sayilmaz(tmp_path, monkeypatch):
    """PID yeniden kullanımı: pid canlı ama süreç claude.exe değil (explorer) → dış çalışan değil."""
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    ep = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Process explorer | Select -First 1).Id"],
                        capture_output=True, text=True, creationflags=0x08000000).stdout.strip()
    (tmp_path / "sahte.basladi").write_text(f"12:00:00 pid {ep}", encoding="utf-8")
    assert ajan_sira.pid_canli(ep)
    assert ajan_sira.dis_calisan(set()) == 0


def _olu_is(tmp_path, ad, yas_sn=60):
    """Süreci ölmüş, sonucu olmayan iş: .basladi (ölü pid) + boş json."""
    f = tmp_path / f"{ad}.basladi"
    f.write_text("12:00:00 pid 999999", encoding="utf-8")
    (tmp_path / f"{ad}.json").write_text("", encoding="utf-8")
    t = ajan_sira.time.time() - yas_sn
    os.utime(f, (t, t))


def _kurtar_ortam(tmp_path, monkeypatch, git=False):
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "git_var", lambda ad: git)
    monkeypatch.setattr(ajan_sira, "log", lambda *a: None)


def test_kurtar_olu_is_yeniden_siraya(tmp_path, monkeypatch):
    _kurtar_ortam(tmp_path, monkeypatch)
    _olu_is(tmp_path, "is-a")
    baslayan = {"is-a"}
    assert ajan_sira.kurtar([("is-a", "g.md")], baslayan) == {"is-a": None}
    assert "is-a" not in baslayan


def test_kurtar_ayni_gorev_dosyasi_baska_satir_bitmis(tmp_path, monkeypatch):
    """arac-bul-2 / 2b olayı: aynı görev dosyasını kullanan başka satırın sonucu var → kurtarma yok."""
    _kurtar_ortam(tmp_path, monkeypatch)
    _olu_is(tmp_path, "arac-2")
    (tmp_path / "arac-2b.json").write_text('{"type": "result"}\n', encoding="utf-8")
    baslayan = {"arac-2"}
    satirlar = [("arac-2", "g.md"), ("arac-2b", "g.md")]
    assert ajan_sira.kurtar(satirlar, baslayan) == {}
    assert "arac-2" in baslayan and not (tmp_path / "arac-2.kurtar").exists()


def test_kurtar_git_logda_gorev_adi_var(tmp_path, monkeypatch):
    _kurtar_ortam(tmp_path, monkeypatch, git=True)
    _olu_is(tmp_path, "is-g")
    assert ajan_sira.kurtar([("is-g", "g.md")], {"is-g"}) == {}


def test_kurtar_yas_alti_saat_alarm(tmp_path, monkeypatch):
    """Yaş >6 saat: kurtarma yok, beyin alarmı (hata olayı) ve Desktop'a soru."""
    _kurtar_ortam(tmp_path, monkeypatch)
    _olu_is(tmp_path, "is-eski", yas_sn=7 * 3600)
    assert ajan_sira.kurtar([("is-eski", "g.md")], {"is-eski"}) == {}
    import beyin_dusun
    olaylar = [json.loads(s) for s in beyin_dusun.OLAY.read_text(encoding="utf-8").splitlines()]
    assert any(o["tur"] == "kurtar-atla" and o["arac"] == "is-eski" and o["hata"] for o in olaylar)


def test_kurtar_atla_gunlugu_neden_yazar(tmp_path, monkeypatch):
    _kurtar_ortam(tmp_path, monkeypatch)
    satirlar = []
    monkeypatch.setattr(ajan_sira, "log", lambda *a: satirlar.append(" ".join(map(str, a))))
    _olu_is(tmp_path, "is-x")
    (tmp_path / "is-y.json").write_text('{"type": "result"}\n', encoding="utf-8")
    ajan_sira.kurtar([("is-x", "g.md"), ("is-y", "g.md")], {"is-x"})
    assert any(s.startswith("KURTAR-ATLA is-x") and "is-y" in s for s in satirlar)


def _kapi_izole(tmp_path, monkeypatch):
    import beyin_dusun
    monkeypatch.setattr(beyin_dusun, "DURUM", tmp_path / "durum.json")
    monkeypatch.setattr(beyin_dusun, "ALARM", tmp_path / "alarm.txt")
    baslatildi = []
    monkeypatch.setattr(beyin_dusun, "_baslat", lambda: baslatildi.append(1))
    return beyin_dusun, baslatildi


def test_nihai_kapi_satirsiz_gorev_baslamaz(tmp_path, monkeypatch):
    b, _ = _kapi_izole(tmp_path, monkeypatch)
    b.olay("arac", "Bash", "taze")
    b.DURUM.write_text(json.dumps({"tur_t": __import__("time").time()}), encoding="utf-8")
    sebep = ajan_sira.nihai_kapi("sahte-1", "görev metni, satır yok")
    assert sebep and "NİHAİ 31+32" in sebep
    assert "sahte-1" in b.ALARM.read_text(encoding="utf-8")
    assert json.loads(b.OLAY.read_text(encoding="utf-8").splitlines()[-1])["tur"] == "kapi"


def test_nihai_kapi_bekci_kapaliyken_baslamaz(tmp_path, monkeypatch):
    b, baslatildi = _kapi_izole(tmp_path, monkeypatch)
    b.olay("arac", "Bash", "taze")
    b.DURUM.write_text(json.dumps({"tur_t": __import__("time").time() - 900}), encoding="utf-8")
    sebep = ajan_sira.nihai_kapi("sahte-2", "NİHAİ 31+32 (kabul şartı): ...")
    assert sebep and "bekçi ölü" in sebep
    assert baslatildi == [1]  # ölü bekçi yeniden başlatılır


def test_nihai_kapi_bayat_olay_baslamaz_ve_kapi_olayi_sayilmaz(tmp_path, monkeypatch):
    import time
    b, _ = _kapi_izole(tmp_path, monkeypatch)
    b.DURUM.write_text(json.dumps({"tur_t": time.time()}), encoding="utf-8")
    b.olay("kapi", "x", "kapı kendi olayı")  # tek olay 'kapi' → sayılmaz
    assert "son beyin olayı" in ajan_sira.nihai_kapi("sahte-3", "NİHAİ 31+32 satırı var")


def test_nihai_kapi_satirli_gorev_baslar(tmp_path, monkeypatch):
    import time
    b, _ = _kapi_izole(tmp_path, monkeypatch)
    b.olay("arac", "Bash", "taze")
    b.DURUM.write_text(json.dumps({"tur_t": time.time()}), encoding="utf-8")
    assert ajan_sira.nihai_kapi("gercek-1", "NİHAİ 31+32 (kabul şartı): ...") is None
    assert not b.ALARM.exists()


def test_nihai_bitis_kismi(tmp_path, monkeypatch):
    import time
    b, _ = _kapi_izole(tmp_path, monkeypatch)
    t0 = time.time() - 600
    b.olay("arac", "Bash", "tek olay")  # 10 dk'da 1 olay, pattern-store yok
    eksik = ajan_sira.nihai_bitis("is-x", t0, time.time())
    assert len(eksik) == 2 and "KISMI-NİHAİ is-x" in b.ALARM.read_text(encoding="utf-8")


def test_nihai_bitis_tam(tmp_path, monkeypatch):
    import time
    b, _ = _kapi_izole(tmp_path, monkeypatch)
    t0 = time.time() - 60
    b.olay("arac", "mcp__ruflo__agentdb_pattern-store", "ders")
    assert ajan_sira.nihai_bitis("is-y", t0, time.time() + 1) == []  # olay t'si round(,1) ile yukarı yuvarlanır; +1 sn olmadan ~%50 dalgalanır
    assert not b.ALARM.exists()


def test_bekci_yokla_oluyse_yeniden_baslatir(tmp_path, monkeypatch):
    import time
    b, baslatildi = _kapi_izole(tmp_path, monkeypatch)
    assert b.bekci_yokla() and baslatildi == [1]  # durum dosyası yok → ölü sayılır, uyarı + yeniden başlatma
    b.DURUM.write_text(json.dumps({"tur_t": time.time()}), encoding="utf-8")
    assert b.bekci_yokla() == "" and baslatildi == [1]


def test_nihai_ozet_sablonlarda():
    import nihai_ozet
    assert nihai_ozet.OZET.count("\n") <= 3 and "31+32" in nihai_ozet.OZET


def test_gorev_yolu_mutlak_satir():
    s = ajan_sira.gorev_yolu_satir(".kos/kopru/gorev-havuz-genis-2.md")
    assert "[görev dosyası]" in s and os.path.isabs(s.split("] ", 1)[1].split(" (")[0])
    assert s.split("] ", 1)[1].split(" (")[0].endswith("gorev-havuz-genis-2.md")


def test_yenile_mtime_degisince_yenile(tmp_path):
    """YONETICI-YENILE-1: izlenen modülün mtime'ı değişince karar 'yenile'; aynı küme ikinci turda tekrar derlenmez."""
    f = tmp_path / "m.py"
    f.write_text("X = 1\n", encoding="utf-8")
    ilk = {str(f): 100.0}
    assert ajan_sira.yenile_karar(ilk, {}, {str(f): 100.0}) == (None, {}, [])
    karar, degisen, hatalar = ajan_sira.yenile_karar(ilk, {}, {str(f): 200.0})
    assert (karar, hatalar) == ("yenile", []) and degisen == {str(f): 200.0}
    assert ajan_sira.yenile_karar(ilk, degisen, {str(f): 200.0}) == (None, degisen, [])


def test_yenile_derleme_hatasi_yenileme_yok(tmp_path):
    f = tmp_path / "bozuk.py"
    f.write_text("def x(:\n", encoding="utf-8")
    karar, degisen, hatalar = ajan_sira.yenile_karar({str(f): 1.0}, {}, {str(f): 2.0})
    assert karar == "alarm" and len(hatalar) == 1 and hatalar[0].startswith("bozuk.py") and "SyntaxError" in hatalar[0]


def test_yenile_yeni_modul_kayda_girer(tmp_path):
    ilk = {}
    assert ajan_sira.kod_degisti(ilk, {"a.py": 5.0}) == {} and ilk == {"a.py": 5.0}


def test_izlenen_mtime_yerel_modulleri_alir():
    m = ajan_sira.izlenen_mtime()
    assert any(os.path.basename(f) == "maliyet_defter.py" for f in m) and not any("site-packages" in f for f in m)


def test_yenile_et_kilidi_birakir_ve_execv(tmp_path, monkeypatch):
    kilit = tmp_path / "ajan-sira.kilit"
    kilit.write_text(f"{os.getpid()} 00:00:00", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KILIT", kilit)
    gor = []
    monkeypatch.setattr(ajan_sira.os, "execv", lambda exe, argv: gor.append((exe, argv, kilit.exists())))
    ajan_sira.yenile_et({"x/ajan_sira.py": 1.0})
    exe, argv, kilit_var = gor[0]
    assert exe == sys.executable and argv[0] == sys.executable and not kilit_var


def test_yenile_hazir_calisan_beklemez_yeniden_en_cok_5_dk():
    """YONETICI-YENILE-2: uzun çalışan ajan yenilemeyi tutmaz (yeni yönetici devralır); bekleyen yeniden deneme en çok 5 dk tutar."""
    assert ajan_sira.yenile_hazir([], 1000.0, 1000.0)
    assert not ajan_sira.yenile_hazir([("is-r",)], 1000.0, 1000.0 + 299)
    assert ajan_sira.yenile_hazir([("is-r",)], 1000.0, 1000.0 + 300)


def test_devralinan_poll_pid_olunce_sonuca_gore_rc(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    canli = [True]
    monkeypatch.setattr(ajan_sira, "claude_sureci", lambda pid, t: canli[0])
    p = ajan_sira.Devralinan("is-d", 4242, 0.0)
    assert p.poll() is None and p.pid == 4242
    canli[0] = False
    (tmp_path / "is-d.json").write_text('{"type": "result"}\n', encoding="utf-8")
    assert p.poll() == 0 and p.returncode == 0
    (tmp_path / "is-d.json").write_text("", encoding="utf-8")
    assert ajan_sira.Devralinan("is-d", 4242, 0.0).poll() == 1


class _Dur(Exception):
    pass


def _main_ortam(tmp_path, monkeypatch, canli):
    """main()'i gerçek kuyruk/çıktı klasörüyle (tmp) sürer; uyku çağrısında _Dur fırlatır. canli[0]=False → devralınan ajan ölür."""
    kuyruk = tmp_path / "ajan-sira.tsv"
    kuyruk.write_text("is-d\tg.md\t\tefor=medium\n", encoding="utf-8")
    (tmp_path / "g.md").write_text("x", encoding="utf-8")
    (tmp_path / "is-d.basladi").write_text("12:00:00 pid 4242 sid abc", encoding="utf-8")
    (tmp_path / "is-d.json").write_text("", encoding="utf-8")
    satirlar = []

    def log(*a):
        satirlar.append(" ".join(map(str, a)))
        if a and a[0] == "DEVRAL":
            canli[0] = False  # devralma yapıldı → ajan şimdi ölsün; BİTTİ yeni yöneticide yazılmalı
    for ad, deger in {"CIKTI": tmp_path, "KUYRUK": kuyruk, "KOK": tmp_path, "DUR": tmp_path / "dur"}.items():
        monkeypatch.setattr(ajan_sira, ad, deger)
    monkeypatch.setattr(ajan_sira, "log", log)
    monkeypatch.setattr(ajan_sira, "kilit_al", lambda: True)
    monkeypatch.setattr(ajan_sira, "claude_sureci", lambda pid, t: canli[0])
    monkeypatch.setattr(ajan_sira, "pid_canli", lambda pid: canli[0])
    monkeypatch.setattr(ajan_sira, "ram_bekle", lambda c: None)
    monkeypatch.setattr(ajan_sira, "nihai_bitis", lambda *a: [])
    monkeypatch.setattr(ajan_sira, "ram", lambda: 10)
    monkeypatch.setattr(ajan_sira, "yenile_karar", lambda *a: (None, {}, []))
    monkeypatch.setattr(ajan_sira.arka_istek, "isle", lambda log=None: None)
    monkeypatch.setattr(ajan_sira.zorunlu_arac, "denetle", lambda ad: None)
    monkeypatch.setattr(ajan_sira.subprocess, "Popen", lambda *a, **k: None)
    kayit = []
    monkeypatch.setattr(ajan_sira, "is_kaydi", lambda *a: kayit.append(a) or True)
    monkeypatch.setitem(sys.modules, "yarim_bekci", type("Y", (), {"calistir": staticmethod(lambda K, KOK: (0, []))}))
    import beyin_dusun
    monkeypatch.setattr(beyin_dusun, "ara_olay", lambda *a: None)
    monkeypatch.setattr(beyin_dusun, "bekci", lambda n: None)

    def uyku(_):
        raise _Dur
    monkeypatch.setattr(ajan_sira.time, "sleep", uyku)
    return satirlar, kayit


def test_main_yonetici_yenilenince_calisan_ajan_devralinir_ve_bitti_yazilir(tmp_path, monkeypatch):
    """YONETICI-YENILE-2: .basladi'sı canlı ajan yeni yöneticide calisan'a girer; ölünce BİTTİ + iş kaydı yeni yöneticide yazılır."""
    canli = [True]
    satirlar, kayit = _main_ortam(tmp_path, monkeypatch, canli)
    with pytest.raises(_Dur):
        ajan_sira.main()
    assert any(s.startswith("DEVRAL is-d") for s in satirlar)
    assert any(s.startswith("BİTTİ is-d") for s in satirlar) and [k[0] for k in kayit] == ["is-d"]


def test_main_yenile_calisan_ajan_varken_hemen_yenilenir(tmp_path, monkeypatch):
    canli = [True]
    _main_ortam(tmp_path, monkeypatch, canli)
    monkeypatch.setattr(ajan_sira, "log", lambda *a: None)  # DEVRAL kancası kapalı: ajan yenileme anında canlı
    monkeypatch.setattr(ajan_sira, "yenile_karar", lambda *a: ("yenile", {"x.py": 1.0}, []))
    yenilendi = []

    def yenile_et(degisen):
        yenilendi.append(degisen)
        raise _Dur
    monkeypatch.setattr(ajan_sira, "yenile_et", yenile_et)
    with pytest.raises(_Dur):
        ajan_sira.main()
    assert yenilendi and canli[0]


def test_ram_kesti_isareti_bir_kez_tuketilir(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    assert not ajan_sira.ram_kesti_al("is-a")
    ajan_sira.ram_kesti_isaretle("is-a", 95)
    assert (tmp_path / "is-a.ramkesti").exists()
    assert ajan_sira.ram_kesti_al("is-a") and not ajan_sira.ram_kesti_al("is-a")


def test_ram_yeniden_b_adi_ve_tek_sefer():
    y = ajan_sira.ram_yeniden("is-a", "gorev/x.md", "kosul", "medium", "haiku", 1, None)
    assert y[0] == "is-a-b" and y[1] == "gorev/x.md" and y[3:] == ("medium", "haiku", 1, None)
    assert ajan_sira.ram_yeniden("is-a-b", "gorev/x.md", "kosul", "medium", "haiku", 1, None) is None  # RAM ile ikinci kesilen tekrar sıraya girmez


def test_ram_yeniden_yalniz_ram_85_altinda_baslar():
    assert not ajan_sira.ram_yeniden_hazir("is-a-b", 85) and ajan_sira.ram_yeniden_hazir("is-a-b", 84)
    assert ajan_sira.ram_yeniden_hazir("is-a", 99)  # -b olmayan işleri bu kapı etkilemez


def test_baslamadan_dustu_bos_json_rc1():
    """RC1-TESHIS-1: rc≠0 + boş json + RAM kesmedi + kısa süre → 'BAŞLAMADAN DÜŞTÜ' (merdiven yükselmez); RAM kesmesi, dolu json, uzun iş değil."""
    assert ajan_sira.baslamadan_dustu(1, True, False, 1)
    assert not ajan_sira.baslamadan_dustu(1, True, True, 1)  # RAM bekçisi kesti → ayrı yol
    assert not ajan_sira.baslamadan_dustu(1, False, False, 1)  # sonuç var
    assert not ajan_sira.baslamadan_dustu(0, True, False, 1)
    assert not ajan_sira.baslamadan_dustu(1, True, False, 30)  # uzun koştu → başlamadan düşmedi


def test_kok_adlari_calisan_ve_basladi(tmp_path, monkeypatch):
    class P:
        pid = 4242
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "claude_sureci", lambda pid, t: pid == "777")
    (tmp_path / "dis-is.basladi").write_text("10:00:00 pid 777 sid x", encoding="utf-8")
    (tmp_path / "olu-is.basladi").write_text("10:00:00 pid 888 sid y", encoding="utf-8")
    assert ajan_sira.kok_adlari({"is-a": (P(),)}) == {4242: "is-a", 777: "dis-is"}


def test_ara_aralik_100_sn_ve_dongu_kullanir():
    """YARIM-B1 5: yoklama 30 sn adımlı; eşik 100 sn → ara olay aralığı ≤2 dk (önceden 2.0–2.6)."""
    assert ajan_sira.ARA_ARALIK == 100
    assert "time.time() - ara_t >= ARA_ARALIK" in Path(ajan_sira.__file__).read_text(encoding="utf-8")


def test_is_kaydi_hook_hatasi_rc1_yine_basari(tmp_path, monkeypatch):
    """RC1-TESHIS-1: JSON'un arkasına SessionEnd hook hata satırı (aynı satırda da) → rc 1 olsa da subtype=success BAŞARILI."""
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    j = '{"type":"result","subtype":"success","num_turns":3,"total_cost_usd":0.2,"result":"tamam"}'
    (tmp_path / "h1.json").write_text(j + "\nSessionEnd hook [bash x] failed: Executable not found in $PATH: \"bash\"\n", encoding="utf-8")
    (tmp_path / "h2.json").write_text(j + "SessionEnd hook [bash x] failed\n", encoding="utf-8")
    assert ajan_sira.is_kaydi("h1", 1, 4.0, "", "haiku") is True
    assert ajan_sira.is_kaydi("h2", 1, 4.0, "", "haiku") is True
    assert ajan_sira.sonuc_var("h2") is True
    ajan_sira.sonuc_temizle("h2")
    assert json.loads((tmp_path / "h2.json").read_text(encoding="utf-8").strip())["subtype"] == "success"
    assert "SessionEnd" in (tmp_path / "h2.stray.txt").read_text(encoding="utf-8")


def test_kurtar_yeniden_kopya_canliysa_ikinci_kopya_yok(tmp_path, monkeypatch):
    """RC1-TESHIS-1 (c): ad-b (RAM yeniden) koşuyorken ya da bitmişken ad için KURTAR --resume açılmaz."""
    _kurtar_ortam(tmp_path, monkeypatch)
    monkeypatch.setattr(ajan_sira, "pid_canli", lambda p: True)
    monkeypatch.setattr(ajan_sira, "claude_sureci", lambda p, t: True)
    _olu_is(tmp_path, "is-k")
    (tmp_path / "is-k-b.basladi").write_text("12:00:00 pid 4242", encoding="utf-8")
    (tmp_path / "is-k-b.json").write_text("", encoding="utf-8")
    assert ajan_sira.kurtar([("is-k", "g.md")], {"is-k", "is-k-b"}) == {}
    assert not (tmp_path / "is-k.kurtar").exists()
    monkeypatch.setattr(ajan_sira, "pid_canli", lambda p: False)  # kopya öldü, sonuç da yok → asıl iş kurtarılır
    assert ajan_sira.kurtar([("is-k", "g.md")], {"is-k"}) == {"is-k": None}
    (tmp_path / "is-k-b.json").write_text('{"type":"result","subtype":"success"}\n', encoding="utf-8")  # kopya bitti → kurtarma gereksiz
    (tmp_path / "is-k.kurtar").unlink()
    assert ajan_sira.kurtar([("is-k", "g.md")], {"is-k"}) == {}


def test_bash_yolu_ekle(tmp_path, monkeypatch):
    """RC1-TESHIS-1 (a): PATH'te bash yoksa Git Bash dizini eklenir; varsa PATH aynen kalır."""
    (tmp_path / "bash.exe").write_text("", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "GIT_BASH", tmp_path)
    e = ajan_sira.bash_yolu_ekle({"PATH": r"C:\Windows\system32"})
    assert e["PATH"] == rf"C:\Windows\system32;{tmp_path}"
    assert ajan_sira.bash_yolu_ekle(dict(e))["PATH"] == e["PATH"]


def _konsol_hazir(tmp_path, monkeypatch, bayrak=True):
    """KONSOL-GECIS-1: sahte anahtar + izole bayrak/defter; gerçek anahtar/kayıt defteri hiç okunmaz."""
    monkeypatch.setattr(ajan_sira, "KONSOL", tmp_path / "ajan-sira.konsol")
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")
    monkeypatch.setattr(ajan_sira.maliyet_defter, "DEFTER", tmp_path / "maliyet.tsv")
    monkeypatch.setattr(ajan_sira, "taze_env", lambda: {"ANTHROPIC_API_KEY_AJAN": "sahte-anahtar", "CLAUDE_CODE_OAUTH_TOKEN": "sahte-oauth", "PATH": "x"})
    if bayrak:
        (tmp_path / "ajan-sira.konsol").write_text("1")


def test_konsol_bayrak_anahtari_aktarir(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    _, env = ajan_sira.baslat_argv("medium", "haiku", rol="kontrol")
    assert env["ANTHROPIC_API_KEY"] == "sahte-anahtar" and "ANTHROPIC_API_KEY_AJAN" not in env and "CLAUDE_CODE_OAUTH_TOKEN" not in env
    assert env["MAX_THINKING_TOKENS"] == "10000"  # think10k yalnız kuyruk ajanında


def test_konsol_is_ajani_ortaminda_anahtar_yok(tmp_path, monkeypatch):
    """KONSOL-GECIS-2: bayrak AÇIKKEN bile rol≠kontrol alt sürecinde Console anahtarı yok; abonelik kalır."""
    _konsol_hazir(tmp_path, monkeypatch)
    for model in ("haiku", "sonnet", "opus", "ucretsiz", "hermes"):
        monkeypatch.setattr(ajan_sira.ucretsiz_motor, "anahtar", lambda e: "omni")
        _, env = ajan_sira.baslat_argv("medium", model)
        assert "sahte-anahtar" not in env.values() and "ANTHROPIC_API_KEY" not in env and "ANTHROPIC_API_KEY_AJAN" not in env, model
        assert not ajan_sira.konsol_sizdi(env, None, "sahte-anahtar"), model


def test_konsol_sizdi_red():
    assert ajan_sira.konsol_sizdi({"ANTHROPIC_API_KEY": "k"}, None, "k")
    assert not ajan_sira.konsol_sizdi({"ANTHROPIC_API_KEY": "k"}, "kontrol", "k")
    assert not ajan_sira.konsol_sizdi({"ANTHROPIC_API_KEY": "baska"}, None, "k") and not ajan_sira.konsol_sizdi({}, None, None)


def test_konsol_bayraksiz_eski_davranis(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch, bayrak=False)
    _, env = ajan_sira.baslat_argv("medium", "haiku")
    assert "ANTHROPIC_API_KEY" not in env and "MAX_THINKING_TOKENS" not in env and env["CLAUDE_CODE_OAUTH_TOKEN"] == "sahte-oauth"


def test_konsol_ucretsiz_motor_anahtar_tasimaz(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    monkeypatch.setattr(ajan_sira.ucretsiz_motor, "anahtar", lambda e: "omni")
    _, env = ajan_sira.baslat_argv("high", "ucretsiz")
    assert "sahte-anahtar" not in env.values() and "ANTHROPIC_API_KEY" not in env and "MAX_THINKING_TOKENS" not in env


def test_konsol_anahtar_yoksa_abonelik(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    monkeypatch.setattr(ajan_sira, "taze_env", lambda: {"PATH": "x"})
    _, env = ajan_sira.baslat_argv("", "haiku", rol="kontrol")
    assert "ANTHROPIC_API_KEY" not in env


def test_defter_konsol_sutunu(tmp_path):
    import time
    y = tmp_path / "m.tsv"
    md = ajan_sira.maliyet_defter
    md.yaz("a-1", "haiku-medium", 0.5, True, yol=y)  # eski 6 sütun
    md.yaz("b-1", "haiku-medium", 2.0, True, yol=y, kaynak="konsol", cache=0.9)
    md.yaz("c-1", "sonnet-medium", 3.0, False, yol=y, kaynak="konsol", cache=0.5)
    rows = md.oku(y)
    assert [r["kaynak"] for r in rows] == ["abonelik", "konsol", "konsol"] and rows[1]["cache"] == 0.9
    assert md.konsol_harcama(rows, time.strftime("%Y-%m-%d")) == 5.0 and md.konsol_harcama(rows, "1999-01-01") == 0 and md.konsol_harcama(rows) == 5.0
    assert y.read_text(encoding="utf-8").splitlines()[1].count("\t") == 5  # konsol dışı satır 6 sütun kalır


def test_konsol_izle_tavan_ve_uyari(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    uyari = set()
    assert ajan_sira.konsol_izle(uyari) is False
    ajan_sira.maliyet_defter.yaz("x-1", "haiku-medium", 12.5, True, kaynak="konsol", cache=0.8)
    logs = []
    monkeypatch.setattr(ajan_sira, "log", lambda *a: logs.append(" ".join(map(str, a))))
    assert ajan_sira.konsol_izle(uyari) is True and ajan_sira.konsol_izle(uyari) is True
    assert sum("KONSOL-TAVAN" in x for x in logs) == 1  # bir kez yazılır
    ajan_sira.maliyet_defter.yaz("x-2", "haiku-medium", 160, True, kaynak="konsol", cache=0.8)
    ajan_sira.konsol_izle(uyari)
    assert any("KONSOL-UYARI" in x and "150" in x for x in logs) and not any("180" in x for x in logs)


def test_konsol_izle_bayraksiz_kapali(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch, bayrak=False)
    ajan_sira.maliyet_defter.yaz("x-1", "haiku-medium", 99, True, kaynak="konsol", cache=0.8)
    assert ajan_sira.konsol_izle(set()) is False


def test_konsol_politika(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    k = "kontrol"
    assert ajan_sira.konsol_politika("opus", "high", "sıradan iş", k) == ("sonnet", "medium")
    assert ajan_sira.konsol_politika("sonnet", "high", "mimari karar ver", k) == ("sonnet", "high")  # zor etiketi → high kalır
    assert ajan_sira.konsol_politika("haiku", "", "iş", k) == ("haiku", "")
    assert ajan_sira.konsol_politika("ucretsiz", "high", "iş", k) == ("ucretsiz", "high")
    assert ajan_sira.konsol_politika("opus", "high", "iş") == ("opus", "high")  # iş ajanı (rol yok): bayrak dokunmaz
    (tmp_path / "ajan-sira.konsol").unlink()
    assert ajan_sira.konsol_politika("opus", "high", "iş", k) == ("opus", "high")


def test_konsol_butce_hedefi(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    assert ajan_sira.butce_bul("sıradan iş", "kontrol") == 0.15 and ajan_sira.butce_bul("mimari karar", "kontrol") == 0.40
    assert ajan_sira.butce_bul("sıradan iş") == ajan_sira.BUTCE_VARSAYILAN  # iş ajanı: bayrak açık olsa da varsayılan
    assert ajan_sira.butce_bul("BÜTÇE ≤$2") == 2.0  # açık bütçe satırı kazanır
    (tmp_path / "ajan-sira.konsol").unlink()
    assert ajan_sira.butce_bul("sıradan iş") == ajan_sira.BUTCE_VARSAYILAN


def test_is_kaydi_konsol_kaynak(tmp_path, monkeypatch):
    _konsol_hazir(tmp_path, monkeypatch)
    monkeypatch.setattr(ajan_sira, "CIKTI", tmp_path)
    monkeypatch.setattr(ajan_sira, "ISKAYDI", tmp_path / "is.tsv")
    (tmp_path / "k.json").write_text('{"subtype":"success","total_cost_usd":0.4,"usage":{"input_tokens":100,"cache_creation_input_tokens":100,"cache_read_input_tokens":800,"output_tokens":5}}\n', encoding="utf-8")
    ajan_sira.KONSOL_ISLER.add("k")
    assert ajan_sira.is_kaydi("k", 0, 1, "medium", "haiku") is True
    r = ajan_sira.maliyet_defter.oku()[-1]
    assert r["kaynak"] == "konsol" and r["cache"] == 0.8 and r["usd"] == 0.4
