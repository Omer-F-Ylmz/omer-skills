import ctypes, io, json, os, sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import fable_ajan_olc as f  # noqa: E402
import kosucu  # noqa: E402


def test_protokol_govde_frontmatter_atar(tmp_path):
    p = tmp_path / "SKILL.md"
    p.write_text("---\nname: x\ndescription: y\n---\n\n# Work protocol\n1. a\n", encoding="utf-8")
    assert f.protokol_govde(p) == "# Work protocol\n1. a"


def test_secim_aile_model_basina_bir_ve_deterministik():
    g = json.loads((f.KOK / "ajanlar" / "kalite3" / "gorevler.json").read_text(encoding="utf-8"))
    s1, s2 = f.sec_temsilci(["fe", "vrm"], g), f.sec_temsilci(["fe", "vrm"], g)
    assert s1 == s2 and [(a, m) for a, m, _ in s1] == [("fe", "sonnet"), ("fe", "haiku"), ("vrm", "sonnet"), ("vrm", "haiku")]


def test_ayristir_dosyadan_satir_satir():
    akis = io.StringIO('{"type":"result","result":"tamam","usage":{"output_tokens":7},"total_cost_usd":0.01,"num_turns":1}\n')
    o = kosucu.ayristir(akis)
    assert o["metin"] == "tamam" and kosucu.jeton(o["usage"])[3] == 7


@pytest.mark.skipif(os.name != "nt", reason="Windows Job Object")
def test_is_bellek_tavani_ve_oz_bellek():
    is_ = kosucu.is_olustur()
    f.is_bellek(is_)
    s = (ctypes.c_byte * 144)()
    ctypes.windll.kernel32.QueryInformationJobObject(is_, 9, s, 144, None)
    assert ctypes.c_ulong.from_buffer(s, 16).value & 0x2200 == 0x2200  # KILL_ON_JOB_CLOSE + JOB_MEMORY
    assert ctypes.c_size_t.from_buffer(s, 120).value == f.JOB_TAVAN_MB << 20
    kosucu.is_kapat(is_)
    assert 5 < f.oz_bellek_mb() < f.OZ_TAVAN_MB


def test_tablo_tohumla_yalniz_eksik_taban_ve_jev(tmp_path):
    import fable_ajan_tablo as t
    b = f.BASLIK
    k, d = tmp_path / "k", tmp_path / "d"
    for x in (k, d):
        (x / "metin").mkdir(parents=True)
    satir = lambda a, kol, r: "\t".join([a, "fe", "haiku", kol, r] + ["1"] * 9) + "\n"  # noqa: E731
    (k / "olcum.tsv").write_text(b + satir("x", "taban", "1") + satir("y", "taban", "1"), encoding="utf-8")
    (k / "metin" / "x__taban__1.md").write_text("T", encoding="utf-8")
    (k / "jev.json").write_text('{"x__taban__1": 8.0}', encoding="utf-8")
    (d / "olcum.tsv").write_text(b + satir("x", "proto", "1"), encoding="utf-8")
    t.tohumla(k, d)
    t.tohumla(k, d)  # ikinci çağrı bir şey eklemez
    assert [(s["ajan"], s["kol"]) for s in t.oku(d)] == [("x", "proto"), ("x", "taban")]
    assert json.loads((d / "jev.json").read_text(encoding="utf-8")) == {"x__taban__1": 8.0}


def test_limit_satiri_out0_yapilmamis_ve_tabloda_yok(tmp_path):
    """Plan limiti ('You've hit your session limit') rc 0 + out 0 yazar; ne yeniden koşudan düşer ne ortalamaya girer."""
    import fable_ajan_tablo as t
    satir = lambda a, out: "\t".join([a, "fe", "haiku", "proto", "1"] + ["1"] * 3 + [out] + ["1"] * 5) + "\n"  # noqa: E731
    (tmp_path / "olcum.tsv").write_text(f.BASLIK + satir("x", "0") + satir("y", "120"), encoding="utf-8")
    assert f.yapilanlar(tmp_path / "olcum.tsv") == {("y", "proto", "1")}
    assert [s["ajan"] for s in t.oku(tmp_path)] == ["y"]


def test_hook_yalniz_haritadaki_ajana_baglam_verir(tmp_path):
    import subprocess
    hook = Path(__file__).resolve().parents[1] / "fable_ajan_hook.py"
    h = tmp_path / "h.json"
    h.write_text(json.dumps({"metin": {"sonnet": "PROTO"}, "ajan": {"ecc:security-reviewer": "sonnet"}}), encoding="utf-8")
    kos = lambda girdi: subprocess.run([sys.executable, str(hook), str(h)], input=girdi, capture_output=True, text=True)  # noqa: E731
    o = kos('{"agent_type": "ecc:security-reviewer"}')
    assert json.loads(o.stdout)["hookSpecificOutput"]["additionalContext"] == "PROTO"
    assert kos('{"agent_type": "fe-x"}').stdout == "" and kos("bozuk").returncode == 0


def test_karar_yaz_birlestirir(tmp_path):
    import fable_ajan_tablo as t
    y = tmp_path / "k.tsv"
    t.yaz(y, [("fe", "haiku", "KABUL"), ("db", "haiku", "RET:out"), ("sec", "haiku", "KABUL")], "calisma-protokolu")
    t.yaz(y, [("fe", "haiku", "RET:out"), ("db", "haiku", "KABUL"), ("sec", "haiku", "KABUL")], "haiku-v1")
    assert y.read_text(encoding="utf-8").splitlines() == ["aile\tmodel\tkarar\tprotokol", "db\thaiku\tKABUL\thaiku-v1",
                                                          "fe\thaiku\tKABUL\tcalisma-protokolu", "sec\thaiku\tKABUL\thaiku-v1"]
