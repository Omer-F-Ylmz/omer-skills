import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ogrenme"))
import ders  # noqa: E402
import kanca  # noqa: E402

KANCA = Path(kanca.__file__)


@pytest.fixture
def depo(tmp_path, monkeypatch):
    monkeypatch.setenv("OGRENME_DIZIN", str(tmp_path))
    return tmp_path


def jsonl(yol, satirlar):
    yol.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in satirlar), encoding="utf-8")
    return str(yol)


def ana(tmp_path, ajan="kodcu", istem="islev.py sayac fonksiyonunu düzelt, testleri geçir"):
    return jsonl(tmp_path / "ana.jsonl", [
        {"type": "user", "message": {"content": "başla"}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Agent",
                                                       "input": {"subagent_type": ajan, "description": "düzelt", "prompt": istem}}]}}])


def alt(tmp_path, hata=1):
    return jsonl(tmp_path / "alt.jsonl", [
        {"type": "user", "message": {"content": "islev.py sayac düzelt"}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Read", "input": {}}]}},
        {"type": "user", "message": {"content": [{"type": "tool_result", "is_error": bool(hata), "content": "x"}]}},
        {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Edit", "input": {}},
                                                      {"type": "tool_use", "name": "Bash", "input": {}}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "Düzeltildi, 4 test geçti."}]}}])


def ders_ekle(**k):
    d = dict(ajan="kodcu", baslik="sayac harf duyarsız", kosul="islev.py sayac düzeltirken",
             icerik="tr_kucuk ile karşılaştır.", sonuc="basari", kaynak="k0", gorev="islev.py sayac fonksiyonu")
    d.update(k)
    return ders.ekle(**d)["id"]


def test_subagent_start_dersi_ekler_ve_kuyruga_yazar(depo, tmp_path):
    i = ders_ekle()
    cikti = kanca.kanca({"hook_event_name": "SubagentStart", "session_id": "s1", "agent_id": "a1", "agent_type": "kodcu",
                         "transcript_path": ana(tmp_path)})
    blok = json.loads(cikti)["hookSpecificOutput"]
    assert blok["hookEventName"] == "SubagentStart" and i in blok["additionalContext"]
    assert json.loads(kanca.kuyruk("s1").read_text(encoding="utf-8"))["ids"] == [i]


def test_subagent_start_ilgisiz_gorev_bos(depo, tmp_path):
    ders_ekle()
    assert kanca.kanca({"hook_event_name": "SubagentStart", "session_id": "s1", "agent_type": "kodcu",
                        "transcript_path": ana(tmp_path, istem="video kırp")}) == ""
    assert not kanca.kuyruk("s1").exists()


def test_subagent_stop_yorunge_ve_session_end(depo, tmp_path):
    cagri = []
    kanca.kanca({"hook_event_name": "SessionEnd", "session_id": "s2"}, baslat=cagri.append)
    assert cagri == []  # kuyruk yok → arka plan yok
    kanca.kanca({"hook_event_name": "SubagentStop", "session_id": "s2", "agent_id": "a1", "agent_type": "kodcu",
                 "agent_transcript_path": alt(tmp_path)})
    k = json.loads(kanca.kuyruk("s2").read_text(encoding="utf-8"))
    assert (k["arac"], k["hata"], k["tur"], k["son"]) == (3, 1, 3, "Düzeltildi, 4 test geçti.")
    kanca.kanca({"hook_event_name": "SessionEnd", "session_id": "s2"}, baslat=cagri.append)
    assert cagri == ["s2"]


def test_karma():
    assert kanca.karma(8, 4, 0, "tamam") == 8 and kanca.karma(8, 4, 2, "tamam") == 6 and kanca.karma(9, 3, 0, " ") == 0


def kuyruk_kur(oturum, ids, karmalar):
    for n, (j, getir) in enumerate(zip(karmalar, ids)):
        if getir:
            kanca._ekle(oturum, {"tip": "getir", "ajan_id": f"a{n}", "ajan": "kodcu", "ids": getir})
        kanca._ekle(oturum, {"tip": "bitti", "ajan_id": f"a{n}", "ajan": "kodcu", "gorev": f"görev {n} islev.py düzelt",
                             "arac": 5, "hata": 0, "tur": 4, "son": "bitti"})


def test_isle_yargi_damitma_geri_bildirim(depo):
    i = ders_ekle()
    kuyruk_kur("s3", [[i], None], [2, 9])
    istemler = []
    damit = lambda m: istemler.append(m) or json.dumps([  # noqa: E731
        {"no": 1, "baslik": "önce testleri oku", "kosul": "islev düzeltirken", "icerik": "Görünür testleri ilk turda oku."},
        {"no": 2, "baslik": "sızıntı", "kosul": "her zaman", "icerik": "anahtar sk-ant-abcdefghijklmnop kullan"}])
    assert kanca.isle("s3", yargic=lambda s: [2.0, 9.0], damit=damit) == 2
    dersler = {x["id"]: x for x in ders.oku()}
    assert dersler[i]["kullanim"] == 1 and dersler[i]["yardim"] == 0  # düşük karmalı koşuda kullanılan ders yardım almaz
    yeni = [x for x in dersler.values() if x["id"] != i]
    assert [x["baslik"] for x in yeni] == ["önce testleri oku"] and yeni[0]["tur"] == "basarisizlik"  # sırlı ders reddedildi
    assert len(istemler) == 1 and not kanca.kuyruk("s3").exists() and kanca.kuyruk("s3").with_suffix(".islendi").exists()


def test_isle_yargi_hatasi_sessiz_atlar(depo):
    kuyruk_kur("s4", [None], [5])
    damit = lambda m: pytest.fail("yargı yokken damıtma çağrılmaz")  # noqa: E731

    def yargic(s):
        raise ConnectionError("ağ yok")
    assert kanca.isle("s4", yargic=yargic, damit=damit) == 0 and kanca.kuyruk("s4").with_suffix(".atlandi").exists()


def test_cli_kapali_ve_bozuk_girdi_rc0(depo, tmp_path):
    env = {**os.environ, "OGRENME_DIZIN": str(depo)}
    for girdi, e in ((b"{bozuk", env), (b'{"hook_event_name": "SubagentStop", "session_id": "s5", "agent_type": "x"}',
                                         {**env, "OGRENME_KANCA": "0"})):
        r = subprocess.run([sys.executable, str(KANCA)], input=girdi, capture_output=True, env=e, timeout=30)
        assert (r.returncode, r.stdout, r.stderr) == (0, b"", b"")
    assert not (depo / "kuyruk").exists() or not any((depo / "kuyruk").iterdir())


def test_cli_subagent_start_2_sn_altinda(depo, tmp_path):
    for n in range(300):
        ders_ekle(baslik=f"kural {n} sayac", kosul=f"islev düzeltirken {n}")
    girdi = json.dumps({"hook_event_name": "SubagentStart", "session_id": "s6", "agent_id": "a1", "agent_type": "kodcu",
                        "transcript_path": ana(tmp_path)}).encode()
    t = time.monotonic()
    r = subprocess.run([sys.executable, str(KANCA)], input=girdi, capture_output=True,
                       env={**os.environ, "OGRENME_DIZIN": str(depo)}, timeout=30)
    assert time.monotonic() - t < 2 and r.returncode == 0
    assert "additionalContext" in r.stdout.decode("utf-8")
