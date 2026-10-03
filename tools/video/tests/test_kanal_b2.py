"""KANAL-1b B2: videoya bağlanmamış karar → (a) aday dosyası video alanı (b) rapor aday bölümü · ortak · aşırı eşleşme · video-dışı."""
from test_kanal_k1 import _jsonl
from video import kanal

V = [f"WWWWWWWWWW{i}" for i in range(7)]


def test_bagsiz_karar_siniflari(tmp_path):
    repo = tmp_path / "repo"
    rd = repo / "docs" / "video-tarama"
    rd.mkdir(parents=True)
    tablo = "## Adaylar\n| aday | tür |\n|---|---|\n"
    rapor = {V[0]: tablo + "| Foo Tool | CLI |\n## Özet\nBar Aracı burada geçer.\n",
             V[1]: tablo + "| Multi | skill |\n", V[2]: tablo + "| Multi | skill |\n",
             **{V[i]: tablo + "| Cok | skill |\n" for i in range(3, 7)}}
    for v, md in rapor.items():
        (rd / f"2026-09-30-{v}.md").write_text("# x\n" + md, encoding="utf-8")
    ad = repo / "docs" / "kurulumlar" / "adaylar"
    ad.mkdir(parents=True)
    (ad / "baz.md").write_text(f"# baz\nad: Baz\nvideo: {V[6]}\nkaynak: yok\n", encoding="utf-8")
    _jsonl(repo / "docs" / "kurulumlar" / "kayit.jsonl", [
        {"ad": "foo-tool", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-09-29"},
        {"ad": "baz", "karar": "DENE (Ömer, panel)", "tarih": "2026-09-29"},
        {"ad": "bar-araci", "karar": "AL (Ömer, panel)", "tarih": "2026-09-29"},
        {"ad": "multi", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-09-29"},
        {"ad": "cok", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-09-29"},
        {"ad": "blend", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-10-01", "parti": "kaynak-tarama-x"},
    ])
    deg, b2 = kanal.degerli(repo)
    assert deg[V[0]] == ["UYARLA:foo-tool"] and deg[V[6]] == ["DENE:baz"]
    assert deg[V[1]] == deg[V[2]] == ["UYARLA:multi ortak"]
    assert not any(x in k for ks in deg.values() for k in ks for x in ("cok", "bar", "blend"))
    assert {k: sorted(v) for k, v in b2.items()} == {"video": ["baz", "foo-tool", "multi"], "video-dışı": ["blend"],
                                                     "çözülemedi": ["bar-araci", "cok (aşırı eşleşme)"]}
