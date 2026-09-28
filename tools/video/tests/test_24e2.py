"""KURULUM-24e-2 hat genişletme: açıklama bağlantıları · kaynak · short partisi · yapım tarifi · deneme şeması (takas) · kuyruk. Ağsız."""
from pathlib import Path

from video import cli, ogren as og, tarama as tr
from video.cli import main

from test_derin import ozellikli, uygula_raporu
from test_uygula import UKos, calis, kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

REPO = Path(__file__).resolve().parents[3]


# K1 açıklama bağlantıları → 2 repo adayı + 1 Site/UI referansı; sosyal ve bölüm dışı bağlantı atlanır
def test_k1_aciklama_baglantilari():
    metin = ("# r\n## Açıklama bağlantıları\nhttps://github.com/acme/tool-a\nhttps://www.npmjs.com/package/pkg-b\n"
             "https://www.awwwards.com/sites/x\nhttps://youtube.com/@kanal\n## Segmentler\n[0:01] https://github.com/yok/segment\n")
    ad, ref = tr.aciklama_adaylari(metin, "AAAAAAAAAAA")
    assert [(x["ad"], x["tur"], bool(x["repo"])) for x in ad] == [("tool-a", "araç", True), ("pkg-b", "araç", True)]
    assert ad[0]["repo"] == "acme/tool-a" and ad[0]["video"] == "AAAAAAAAAAA"
    assert ref == ["https://www.awwwards.com/sites/x"]


# K2 doğrudan kaynak: repo ve alt klasör URL'si → doğru repo + alt yol + ASCII id
def test_k2_kaynak_ayristir():
    k = tr.kaynak_ayristir("https://github.com/anthropics/claude-plugins-official")
    assert (k["repo"], k["alt"], k["id"]) == ("anthropics/claude-plugins-official", "", "kaynak-claude-plugins-official")
    k = tr.kaynak_ayristir("https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup")
    assert (k["repo"], k["alt"], k["ad"], k["id"]) == ("anthropics/claude-plugins-official", "plugins/claude-code-setup",
                                                       "claude-code-setup", "kaynak-claude-code-setup")
    k = tr.kaynak_ayristir("https://www.awwwards.com/sites/Güzel-Site/")
    assert k["repo"] is None and k["id"] == "kaynak-guzel-site"


# K3 short partisi: 2 short → 2 kayıt satırı (karşılaştırmalı rapor `videolar:`), kare ≤3
def test_k3_short_iki_kayit_kare_uc():
    assert cli.kare_tavan(45, 6) == 3 and cli.kare_tavan(600, 6) == 6 and cli.kare_tavan(0, 6) == 6
    metin = "# karşılaştırmalı short\nvideolar: AAAAAAAAAAA, BBBBBBBBBBB\n## Karşılaştırma\n- x\n"
    assert tr.rapor_videolari(metin, "AAAAAAAAAAA") == ["AAAAAAAAAAA", "BBBBBBBBBBB"]
    assert tr.rapor_videolari("# tek\n", "AAAAAAAAAAA") == ["AAAAAAAAAAA"]


# K4 UYARLA(MCP) → yapım tarifi + brief satırı; UYARLA(skill) → ÜRETİLEBİLİR
def test_k4_mcp_yapim_tarifi_skill_uretilebilir(ortam, kok, capsys):
    y = ozellikli(kok, "arac",
                  {"slug": "mcp-x", "karar": "UYARLA", "fikir": "f", "hedef": "yeni MCP sunucusu", "hedef_tur": "MCP", "etki": "girdi −%10"},
                  {"slug": "ozet-skill", "karar": "UYARLA", "fikir": "f", "hedef": "skills/ozet/SKILL.md", "hedef_tur": "skill", "etki": "çıktı −%30"})
    assert calis(ortam, [y], UKos()) == 0
    assert (kok / "docs" / "uyarlamalar" / "arac-mcp-x-yapim.md").is_file()
    r = uygula_raporu(kok)
    assert "arac-mcp-x" in tr.bolum(r, "YAPIM TARİFLERİ") and "arac-mcp-x" not in tr.bolum(r, "ÜRETİLEBİLİR")
    assert "arac-ozet-skill" in tr.bolum(r, "ÜRETİLEBİLİR")
    capsys.readouterr()
    assert main(["brief", str(next(kok.rglob("*-uygula.md")))], env=ortam) == 0
    o = capsys.readouterr().out
    assert "## Yapım tarifleri" in o and "arac-mcp-x" in o


# K5 deneme şeması: tek eşikli karar denetimden geçmez; takas tablosu geçer; iki deneme dosyası taşındı, tavan korundu
DENEME = "# Deneme: d\n\n## Kollar\nA · B\n\n## Görevler\n6 görev\n\n## Tavan\nclaude -p en fazla 24\n\n## Karar ölçütü\n{}\n"


def test_k5_tek_esikli_deneme_gecmez(tmp_path, ortam, capsys):
    y = tmp_path / "d.md"
    y.write_text(DENEME.format("sıcak koşu $ ≥%20 düşüş"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    assert "(deneme)" in capsys.readouterr().out
    y.write_text(DENEME.format("takas tablosu (omer-kurallar 21)"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    assert og.deneme_denetle(DENEME.format("takas tablosu").replace("## Görevler\n6 görev\n\n", ""))


def test_k5_denemeler_takas_tavan_korunur(tmp_path):
    for ad, tavan in (("max-thinking-tokens", "en fazla 24"), ("subagent-haiku", "en fazla 16")):
        m = (REPO / "docs" / "denemeler" / f"{ad}.md").read_text(encoding="utf-8")
        assert og.deneme_denetle(m) == [] and "≥%20" not in m and tavan in tr.bolum(m, "Tavan")
    og.deneme_yaz(tmp_path, {"esik": "çıktı −%30"}, "yeni", "")
    assert og.deneme_denetle((tmp_path / "docs" / "denemeler" / "yeni.md").read_text(encoding="utf-8")) == []


# K6 kuyruk: sıra 1'den short partisi + aynı konu; --isle yalnız durum sütununu yazar (CRLF ve diğer sütunlar bayt bayt aynı)
KUYRUK = ("# Kuyruk\r\n\r\n### Sıra 2 — araç\r\n| id | süre | başlık | Desktop notu | durum |\r\n|---|---|---|---|---|\r\n"
          "| UUUUUUUUUUU | 12.0 | uzun u | not | bekliyor |\r\n"
          "### Sıra 1 — token\r\n| id | süre | başlık | Desktop notu | durum |\r\n|---|---|---|---|---|\r\n"
          "| AAAAAAAAAAA | 0.6 | kısa a | x |  bekliyor |\r\n"
          "| BBBBBBBBBBB | 9.0 | uzun b | y | bekliyor |\r\n"
          "| CCCCCCCCCCC |1.3| kısa c  | AAAAAAAAAAA ile aynı konu | bekliyor |\r\n"
          "| DDDDDDDDDDD | 0.9 | kısa d | z | işlendi: eski |\r\n"
          "### Kaynaklar\r\n| kaynak | ilgili video | Desktop notu | durum |\r\n| owner/repo | AAAAAAAAAAA | n | bekliyor |\r\n")


def test_k6_kuyruk_parti_sira_ve_ayni_konu():
    tur, parti = tr.kuyruk_parti(KUYRUK)
    assert tur == "short" and [h[0] for h in parti] == ["AAAAAAAAAAA", "CCCCCCCCCCC"]


def test_k6_kuyruk_yalniz_durum_sutunu(tmp_path, ortam, capsys):
    y = tmp_path / "kuyruk.md"
    y.write_bytes(KUYRUK.encode("utf-8"))
    assert main(["kuyruk", "--dosya", str(y)], env=ortam) == 0
    assert "AAAAAAAAAAA" in capsys.readouterr().out
    assert main(["kuyruk", "--dosya", str(y), "--isle", "CCCCCCCCCCC,owner/repo", "--commit", "abc1234"], env=ortam) == 0
    eski, yeni = KUYRUK.split("\r\n"), y.read_bytes().decode("utf-8").split("\r\n")
    fark = [(a, b) for a, b in zip(eski, yeni) if a != b]
    assert len(eski) == len(yeni) and len(fark) == 2
    for a, b in fark:
        assert b[:b.rstrip(" |").rfind("|")] == a[:a.rstrip(" |").rfind("|")] and b.endswith("| işlendi: abc1234 |")
