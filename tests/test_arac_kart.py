"""BEYIN-ARAC-KART-1: kart (≤150 jeton) · bölüm indeksi (FTS5) · arama kapısı · bayatlık · canlı geçmiş · seçici · MCP."""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import arac_ara  # noqa: E402
import arac_kart as ak  # noqa: E402

SKILL = """---
name: deadlock-avcisi
description: Use when a Postgres table deadlock or lock wait appears. Do not use for slow queries without locks.
---
# Deadlock avcısı

Kilitlenme izini bulur.

## Teşhis
pg_locks ve pg_stat_activity ile bekleyen kilit zincirini çıkar.

## Çözüm
İşlem sırasını sabitle, kısa transaction kullan.
"""


@pytest.fixture
def kok(tmp_path):
    """Sahte envanter: 1 skill (dosyası var), 1 cli, 1 aday (kurulu değil) + iki ajan işi."""
    (tmp_path / "skills/deadlock-avcisi").mkdir(parents=True)
    md = tmp_path / "skills/deadlock-avcisi/SKILL.md"
    md.write_text(SKILL, encoding="utf8")
    satir = [
        {"ad": "deadlock-avcisi", "tur": "skill", "kaynak": "x", "cagri": "Skill deadlock-avcisi", "durum": "CC", "tetik": "deadlock kilit",
         "alan": "veri-db", "karar": "VARSAYILAN", "asama": "kesif", "metin": "kilit", "is": "kilit", "imza": "aa"},
        {"ad": "semgrep", "tur": "cli", "kaynak": "uv tool", "cagri": "Bash: semgrep --help", "durum": "CC", "tetik": "guvenlik", "alan": "guvenlik",
         "metin": "Static analysis", "is": "Static analysis", "imza": "bb"},
        {"ad": "baska-arac", "tur": "arac", "kaynak": "y", "cagri": "kurulu değil", "durum": "aday", "tetik": "", "metin": "m", "is": "m", "imza": "cc"},
    ]
    yet = tmp_path / "yetenek.jsonl"
    yet.write_text("\n".join(json.dumps(o) for o in satir), encoding="utf8")
    sira = tmp_path / "sira"
    sira.mkdir()
    for ad, usd, durum, eksik in (("is1", 0.5, "ok", []), ("is2", 1.5, "arac_eksik", ["semgrep"])):
        (sira / f"{ad}.json").write_text(json.dumps({"subtype": "success", "is_error": False, "total_cost_usd": usd, "num_turns": 5, "duration_ms": 60000}))
        (sira / f"{ad}.zorunlu.json").write_text(json.dumps({"tur": "veri", "araclar": [{"ad": "deadlock-avcisi"}, {"ad": "semgrep"}]}))
        (sira / f"{ad}.denetim.json").write_text(json.dumps({"durum": durum, "eksik": eksik}))
    return {"yetenek": yet, "kart": tmp_path / "kart.jsonl", "db": tmp_path / "bolum.db", "sira": sira, "log": None,
            "atlas": None, "ogrenim": None, "olay": None, "kok": tmp_path, "md": md, "kombin": tmp_path / "kombin.json"}


def test_bolumle_baslik_bazli():
    b = ak.bolumle(SKILL)
    assert [x[0] for x in b] == ["açıklama", "Deadlock avcısı", "Teşhis", "Çözüm"]
    assert "pg_locks" in b[2][1]


def test_kart_150_jeton_tavani():
    k = {"ad": "x" * 60, "tur": "skill", "ne": "n" * 400, "ne_zaman": "z" * 400, "degil": "d" * 400, "cagri": "c" * 400,
         "birlikte": ["b" * 40] * 9, "esdeger": ["e" * 40] * 9, "maliyet": "m" * 100, "guven": "g" * 100, "surum": "1.0.0",
         "gecmis": {"n": 4, "kabul": 3, "usd": 1.2}, "ders": ["l" * 300] * 3, "gc": "g" * 200}
    assert len(ak.kart_metni(k)) <= ak.KART_TAVAN


def test_yenile_kart_ve_bolum(kok):
    ak.yenile(kok)
    kartlar = [json.loads(s) for s in kok["kart"].read_text(encoding="utf8").splitlines()]
    assert {k["ad"] for k in kartlar} == {"deadlock-avcisi", "semgrep"}  # aday kurulu sayılmaz
    d = next(k for k in kartlar if k["ad"] == "deadlock-avcisi")
    assert d["hash"] and d["yol"].endswith("SKILL.md")
    assert "Do not use" in d["degil"] or "slow queries" in d["degil"]
    assert d["gecmis"]["n"] == 2 and d["gecmis"]["kabul"] == 2
    assert d["birlikte"] == ["semgrep"]


def test_gecmis_arac_kullanimi_eksikten_dusulur(kok):
    g = ak.gecmis_hesapla(kok["sira"], None)
    assert g["arac"]["deadlock-avcisi"]["n"] == 2
    assert g["arac"]["semgrep"]["n"] == 1  # is2'de eksik → kullanılmadı


def test_bayatlik_hash_degisince_yenilenir(kok):
    ak.yenile(kok)
    assert ak.bayat(kok) == []
    kok["md"].write_text(SKILL + "\n## Yeni bölüm\nadvisory lock kullan\n", encoding="utf8")
    assert ak.bayat(kok) == ["deadlock-avcisi"]
    ak.yenile(kok)
    assert ak.bayat(kok) == []
    assert any("advisory" in b["metin"] for b in arac_ara.bolumler(kok["db"], "advisory lock", ["deadlock-avcisi"]))


def test_arama_kart_once_sonra_ilgili_bolum(kok):
    ak.yenile(kok)
    s = arac_ara.ara("postgres deadlock kilit zinciri teşhis", kok, n=5, bolum=2)
    assert s["kartlar"][0]["ad"] == "deadlock-avcisi"
    assert s["bolumler"][0]["ad"] == "deadlock-avcisi"
    assert s["bolumler"][0]["baslik"] == "Teşhis"  # tam metin değil, ilgili bölüm
    assert "Çözüm" not in arac_ara.metin(s) or len(arac_ara.metin(s)) < len(SKILL) + 600
    assert arac_ara.tam("deadlock-avcisi", kok) == SKILL


def test_ekle_tek_arac_kurulum_kancasi(kok):
    ak.yenile(kok)
    yet = kok["yetenek"]
    yet.write_text(yet.read_text(encoding="utf8") + "\n" + json.dumps(
        {"ad": "yeni-arac", "tur": "cli", "kaynak": "npm -g", "cagri": "Bash: yeni-arac --help", "durum": "CC", "tetik": "", "metin": "yeni", "is": "yeni", "imza": "dd"}),
        encoding="utf8")
    assert "yeni-arac" in ak.bayat(kok)  # kartı olmayan kurulu araç bayat sayılır
    ak.yenile(kok, yalniz=["yeni-arac"])
    assert "yeni-arac" in kok["kart"].read_text(encoding="utf8")


def test_secici_isle_ilgili_kume(kok):
    ak.yenile(kok)
    s = arac_ara.sec("postgres deadlock hatası", kok)
    assert s["kume"][0] == "deadlock-avcisi"
    assert "semgrep" in s["kume"]  # birlikte başarılı olan eş


def test_mcp_el_sikisma(kok):
    ak.yenile(kok)
    girdi = "\n".join(json.dumps(m) for m in (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "t", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "arac_ara", "arguments": {"sorgu": "postgres deadlock"}}}))
    cikti = subprocess.run([sys.executable, "-I", str(KOK / "tools/arac_ara_mcp.py"), "--kok", str(kok["kok"]), "--kart", str(kok["kart"]), "--db", str(kok["db"])],
                           input=girdi + "\n", capture_output=True, text=True, encoding="utf8", timeout=60,
                           env={**os.environ, "PYTHONIOENCODING": "utf-8"}).stdout.splitlines()
    r = {j["id"]: j for j in map(json.loads, cikti)}
    assert {t["name"] for t in r[2]["result"]["tools"]} == {"arac_ara", "arac_sec"}
    assert "deadlock-avcisi" in r[3]["result"]["content"][0]["text"]


def test_zorunlu_blok_secici_satiri(monkeypatch, kok):
    sys.path.insert(0, str(KOK / ".kos/kopru"))
    import zorunlu_arac as za
    ak.yenile(kok)
    monkeypatch.setattr(za, "SECICI_KOK", kok)
    s = za.secici_satir("postgres deadlock hatası çöz", "veri")
    assert s.startswith("SEÇİCİ") and "deadlock-avcisi" in s
