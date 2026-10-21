"""TOKEN-3 K11: ajan-sira.tsv isteğe bağlı 4. sütun efor=medium|high → --effort; yoksa eski davranış."""
import importlib.util
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos/kopru"))  # ajan_sira / kontrol_ozet → maliyet_defter
_s = importlib.util.spec_from_file_location("ajan_sira", Path(__file__).resolve().parents[1] / ".kos/kopru/ajan_sira.py")
ajan_sira = importlib.util.module_from_spec(_s)
_s.loader.exec_module(ajan_sira)


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
    assert ajan_sira.kuyruk() == [("a", "i.md", "", "", None), ("b", "i.md", "", "medium", None), ("c", "i.md", "x::y", "high", None)]


def test_gecersiz_efor_reddedilir(tmp_path, monkeypatch):
    tsv = tmp_path / "k.tsv"
    tsv.write_text("a\ti.md\t\tefor=max\n", encoding="utf-8")
    monkeypatch.setattr(ajan_sira, "KUYRUK", tsv)
    with pytest.raises(ValueError):
        ajan_sira.kuyruk()


def test_baslat_argv_env(tmp_path, monkeypatch):
    monkeypatch.setattr(ajan_sira, "SLASH_DOSYA", tmp_path / "slash.bayrak")  # canlı bayraktan bağımsız
    monkeypatch.setenv("CLAUDE_CODE_EFFORT_LEVEL", "high")
    argv, env = ajan_sira.baslat_argv("medium")
    assert argv[-2:] == ["--effort", "medium"] and "CLAUDE_CODE_EFFORT_LEVEL" not in env
    argv, env = ajan_sira.baslat_argv("")
    assert argv == ajan_sira.ARGV and isinstance(env, dict)


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
