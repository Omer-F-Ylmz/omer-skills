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


def test_varyant_es_anlam_ve_kok():
    v = beyin.varyantlar("açılış afişini kapatan bayrak")
    assert "banner" in v[2] and "flag" in v[2]  # TR→EN eş anlam (ıska 29)
    assert "sayi" in beyin.varyantlar("sayımdan sayısı")[1]  # 4 harf kök


def test_parca_ayni_puanda_ikinci_pencere(tmp_path):
    # ıska 19: aynı puanlı iki satırdan ilki seçiliyordu; cevap satırı ikinci pencerede gelmeli
    govde = ["kategori yeniden tekil kalem 351"] + [f"dolgu {i}" for i in range(12)] + \
            ["Token kategorisi yeniden: 71 → 159 tekil"]
    (tmp_path / "n.md").write_text("---\nkaynak: o.md\nsatir: 10\n---\n" + "\n".join(govde),
                                   encoding="utf-8")
    p = beyin.parca(tmp_path / "n.md", "token kategorisi yeniden tekil kalem kaçtan kaça?")
    assert [no for _, no, _ in p] == [10, 23]
    assert "159" in p[1][2][0]


def test_en_varyanti_ve_simge_es(tmp_path):
    # ıska 40: İngilizce kaynak için TR terim EN karşılığıyla değişir; ıska 12: "en fazla" = "≤"
    assert {"long", "break", "new", "session"} <= set(beyin.varyantlar("uzun aradan yeni oturum")[3])
    govde = ["ölçüm claude router1 olcum.tsv 19:31", "x", "Ölçüm claude -p ≤30"]
    (tmp_path / "n.md").write_text("---\nkaynak: r.md\nsatir: 5\n---\n" + "\n".join(govde),
                                   encoding="utf-8")
    assert beyin.parca(tmp_path / "n.md", "ölçüm en fazla kaç claude çağrısı?")[0][1] == 7


def test_global_kaynaklar():
    desenler = [d for *_, d in beyin_al.KAYNAKLAR]
    assert any(d.endswith(str(Path(".claude/CLAUDE.md"))) for d in desenler)
    assert any(d.endswith(str(Path(".claude/RTK.md"))) for d in desenler)


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


def test_bag_ve_komsu(tmp_path):
    g = [("10-kararlar", "gorev-beyin-2", "g/beyin-2.md", "gorev", "# BEYIN-2\nKapi esigi %92 iki tohum".encode(), "d", "k")]
    g += [("20-ogren", f"ogren-{i}", f"o/n{i}.md", "ogren", b"genel-ad", "d", "k") for i in range(4)]
    g += [("20-ogren", "ogren-genel-ad", "o/genel-ad.md", "ogren", b"x", "d", "k")]
    t = beyin_al.takma_adlar(g)
    assert t == {"beyin-2": "gorev-beyin-2"}  # kısa (n0) ve genel (4 kaynakta geçen) elenir
    kasa = tmp_path / "kasa"
    beyin_al.kaynak_al(kasa, "10-kararlar", "gorev-beyin-2", "g/beyin-2.md", g[0][4].decode(), "d", "gorev", 0, tadlar=t)
    beyin_al.kaynak_al(kasa, "20-ogren", "ogren-x", "x.md", "Kapı kararı beyin-2 ile verildi", "d", "ogren", 0, tadlar=t)
    assert "Bağlar: [[gorev-beyin-2--1|beyin-2]]" in (kasa / "20-ogren/ogren-x--1.md").read_text(encoding="utf-8")
    assert 'aliases: ["beyin-2"]' in (kasa / "10-kararlar/gorev-beyin-2--1.md").read_text(encoding="utf-8")
    db = tmp_path / "i.sqlite"
    c = sqlite3.connect(db)
    c.executescript("""create table store_collections(name, path);
        create table documents(id integer primary key, collection, path, active);
        create virtual table documents_fts using fts5(filepath, title, body, tokenize='porter unicode61');""")
    c.execute("insert into store_collections values ('beyin', ?)", (str(kasa),))
    c.execute("insert into documents values (1, 'beyin', '20-ogren/ogren-x--1.md', 1)")
    c.execute("insert into documents_fts(rowid, filepath, title, body) values (1, 'ogren-x--1', '', ?)",
              ((kasa / "20-ogren/ogren-x--1.md").read_text(encoding="utf-8"),))
    c.commit()
    c.close()
    sonuc = beyin.ara("kapı eşiği kaç?", indeks=db)
    assert [s[0] for s in sonuc] == ["x.md", "g/beyin-2.md"]  # ikincisi FTS'de yok, bağ komşusu
    assert beyin.varyantlar("kapı")[-1] == ["kapı"]
