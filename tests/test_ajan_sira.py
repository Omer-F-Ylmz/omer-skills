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
    assert ajan_sira.basamak_sec("atlas-1-d1", None) == 0
    assert ajan_sira.basamak_sec("token-2-d3", None) == 2
    assert ajan_sira.basamak_sec("token-2-d3-r", 1) == 1
    assert ajan_sira.MERDIVEN[2] == ("sonnet", "medium")


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
