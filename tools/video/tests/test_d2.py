"""DERİNLİK-MASTER D2 çağrısız kaçak denetimi: altyazı + OCR + linkler (+ D2 eki: ocr-gurultu.txt) içinden aday benzeri her şey
(sözlük: kurulu araçlar + aday adları; desenler: URL, owner/repo, kurulum komutu, büyük harfli ürün adı) İz'de yoksa "KAÇAN?"."""

from video import tarama as tr

RAPOR = """## Künye
şema 2
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 01:00 | OpenAI | aday değil: konu dışı | geçti |
| kare 02:00 | https://github.com/a/b | b | link |
"""
SOZLUK = ["OpenAI", "rtk", "Meta Stan"]


def kacan(*kaynaklar):
    return tr.kacan(RAPOR, list(kaynaklar), SOZLUK)


def test_desenler_izde_yoksa_kacan():
    k = kacan(("konuşma", "şuraya bakın https://example.com/x ve vercel-labs/agent-skills reposu"),
              ("OCR", "uvx graphify-cli kurun · ChatGPT ekranı"))
    assert {t for _, t in k} == {"https://example.com/x", "vercel-labs/agent-skills", "graphify-cli", "ChatGPT"}
    assert ("konuşma", "https://example.com/x") in k and ("OCR", "ChatGPT") in k


def test_izde_olan_kacan_degil():
    assert kacan(("açıklama", "repo: https://github.com/a/b · OpenAI anlatıldı")) == []


def test_gurultu_satirinda_sozluk_esnek_eslesir_kisa_ad_dahil():
    k = kacan(("gürültü", "00:12 · OpenA1 ve Open A I\n00:13 · rtk gain\n00:14 · artkey\n00:15 · MetaStan"))
    assert sorted(t for _, t in k) == ["Meta Stan", "rtk"]  # OpenAI İz'de (OpenA1/Open A I aynı ad); artkey rtk değil
