import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import beyin  # noqa: E402
import beyin_al  # noqa: E402
import beyin_diyet  # noqa: E402


def test_bol_baslik_ve_tavan():
    satir = ["# A", "x", "## B"] + [f"s{i}" for i in range(35)]
    p = beyin_al.bol(satir)
    assert [b for b, _ in p] == [1, 3, 33]
    assert p[1][1][0] == "## B"


def test_diyet_gecerli_ve_gecmis():
    m = ("# G\n★ D 10:00 — d15\n(d1 için GEÇERLİ) ★ D 09:50\n(d14 için, UYGULANDI) ★ D 09:10\n"
         "(d14 için ★ 09:10 ile GEÇERLİ) ★ D 09:00\ngövde ★ içte\n")
    diyet, gecmis = beyin_diyet.ayir(m, "g")
    assert [s[:10] for s in gecmis] == ["(d14 için,", "(d14 için "]
    assert "★ D 10:00" in diyet and "(d1 için GEÇERLİ)" in diyet and "gövde ★ içte" in diyet
    assert diyet.split("\n")[3].startswith("(geçmiş ★ 2 satır")


def test_terimler_durak_ve_onek():
    assert beyin.terimler("ÖĞREN-0b kapı eşiği nedir?") == ["ogren", "0b", "kapi", "esigi"]
    assert beyin.terimler("Headroom PID'ine dokunulur mu?") == ["headr", "pid", "ine", "dokun"]


def test_ara_uctan_uca(tmp_path):
    kasa = tmp_path / "kasa"
    beyin_al.kaynak_al(kasa, "20-ogren", "ogren-x", "kaynak.md",
                       "# Başlık\nboş satır\nKapı eşiği %92 kararlı\nson", "2026-10-20", "ogren", 2)
    assert (kasa / "20-ogren/ogren-x--2.md").read_text(encoding="utf-8").count("gecersiz: true") == 1
    db = tmp_path / "i.sqlite"
    c = sqlite3.connect(db)
    c.executescript("""create table store_collections(name, path);
        create table documents(id integer primary key, collection, path, active);
        create virtual table documents_fts using fts5(filepath, title, body, tokenize='porter unicode61');""")
    c.execute("insert into store_collections values ('beyin', ?)", (str(kasa),))
    for i, ad in enumerate(["ogren-x--1", "ogren-x--2"], 1):
        metin = (kasa / f"20-ogren/{ad}.md").read_text(encoding="utf-8")
        c.execute("insert into documents values (?, 'beyin', ?, 1)", (i, f"20-ogren/{ad}.md"))
        c.execute("insert into documents_fts(rowid, filepath, title, body) values (?, ?, '', ?)",
                  (i, ad, metin))
    c.commit()
    c.close()
    sonuc = beyin.ara("kapı eşiği kaç?", indeks=db)
    assert sonuc == [("kaynak.md", 3, ["boş satır", "Kapı eşiği %92 kararlı", "son"])]
