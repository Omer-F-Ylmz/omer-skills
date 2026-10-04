"""DERİNLİK-MASTER C3: yerel OCR (Windows.Media.Ocr, tr + en) — metin pakete girer; modele kare yalnız OCR'ın anlamlandıramadığı anlarda;
tavanı aşan model anları "incelenmedi"; kare sırası OCR karakter sayısıyla (C2'nin JPEG vekili kalktı)."""
import json
from pathlib import Path

from video import cli
from video.cli import main
from test_c2 import SahneKos
from test_video import VID, onbellek, ortam  # noqa: F401 (ortam fixture)

KUTU = lambda y: [10, y, 300, y + 20]  # noqa: E731


def test_birlesim_teknik_en_turkce_tr_cakismada_anlamli_olan():
    tr_ = [["npx skilis add owner/repo", *KUTU(0)], ["Ayarlar ekranında şöyle", *KUTU(40)], ["Hello wrld", *KUTU(80)],
           ["Merhaba dunya", *KUTU(120)], ["claude mcp add x — npx -y paket", *KUTU(160)]]
    en = [["npx skills add owner/repo", *KUTU(0)], ["Ayarlar ekramnda Pyle", *KUTU(40)], ["Hello world", *KUTU(80)],
          ["Mrhb dunya", *KUTU(120)], ["claude mcp add x — npx -y paket", *KUTU(160)], ["yalniz en satiri", *KUTU(200)]]
    assert cli._ocr_birlestir(tr_, en) == ["npx skills add owner/repo", "Ayarlar ekranında şöyle", "Hello world", "Merhaba dunya",
                                           "claude mcp add x -- npx -y paket", "yalniz en satiri"]
    assert cli._ocr_birlestir([["sadece tr", *KUTU(0)]], []) == ["sadece tr"]


def test_model_karari_sema_arayuz_kod_bozuk():
    okunur = ["Bu skill kurulumu için şu komutu çalıştırın", "npx skills add vercel-labs/agent-skills", "https://github.com/obra/superpowers"]
    assert not cli._ocr_model(okunur)
    assert cli._ocr_model([]) and cli._ocr_model(["Başlat", "Bitir"])  # az metin: şema/görsel
    assert cli._ocr_model(["Dosya", "Düzen", "Görünüm", "Araçlar", "Yardım", "Kaydet", "Aç", "Yeni"] * 2)  # kısa satırlar: arayüz
    assert cli._ocr_model(["def kur(ns, ctx):", "    yol = Path(ns.yol)", "    return calistir(yol) == 0", "import json"])  # kod
    assert cli._ocr_model(["xkcd qwrtp zzzz mmnn vbbb kkkk llll", "prrt sdfg hjkl qwrt zxcv bnmm ffff"])  # anlamsız


class OcrKos(SahneKos):
    def __init__(self, metin, rc=0, sahne_rc=1, **k):
        super().__init__(rc=sahne_rc, **k)  # varsayılan sahne yok: aday = eşit aralık
        self.metin, self.ocr_rc = metin, rc

    def __call__(self, args, timeout=None):
        if args[0] == "powershell":
            self.cagri.append(list(args))
            if self.ocr_rc:
                return self.ocr_rc, b"", "OCR tanıyıcı yok: en-US".encode()
            adlar = [Path(a).name for a in args[args.index("-File") + 2:]]
            return 0, json.dumps({a: self.metin.get(a[:6], {"tr": [], "en": []}) for a in adlar}, ensure_ascii=False).encode(), b""
        return super().__call__(args, timeout)


OKUNUR = {"tr": [["Bu skill kurulumu için şu komutu çalıştırın", *KUTU(0)], ["npx skilis add owner/repo", *KUTU(40)]],
          "en": [["Bu skill kurulumu icin su komutu calistirin", *KUTU(0)], ["npx skills add owner/repo", *KUTU(40)]]}
KOD = {"tr": [[s, *KUTU(i * 30)] for i, s in enumerate(["def kur(ns, ctx):", "    return calistir(ns) == 0", "import json; x = {}"])], "en": []}


def paket(ortam, kos, kare=2):
    onbellek(ortam, [], duration=600)
    assert main(["paket", VID, "--kare", str(kare), "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    d = Path(ortam["VIDEO_CACHE"]) / VID
    return d, (d / "paket.md").read_text(encoding="utf-8")


def bolum(md, ad):
    return md.split(f"## {ad}\n")[1].split("\n## ")[0].splitlines()


def test_ocr_metni_pakete_girer_okunan_kare_modele_gitmez(ortam):
    kos = OcrKos({"k00150": OKUNUR, "k00450": KOD})
    d, md = paket(ortam, kos)
    (ps,) = [a for a in kos.cagri if a[0] == "powershell"]  # tüm adaylar tek çağrıda
    assert Path(ps[ps.index("-File") + 1]).name == "ocr.ps1" and len(ps[ps.index("-File") + 2:]) == 2
    ekran = bolum(md, "Ekran metni (OCR)")
    assert "[2:30] Bu skill kurulumu için şu komutu çalıştırın" in ekran and "[2:30] npx skills add owner/repo" in ekran
    assert "[7:30] def kur(ns, ctx):" in ekran
    assert [s.split(" · ")[1] for s in bolum(md, "Kareler")] == ["7:30"]  # kod → modele; 2:30 OCR ile anlamlandı
    assert not (d / "kareler" / "k00150_0.jpg").exists() and (d / "kareler" / "k00450_0.jpg").exists()
    assert md.rstrip().endswith(bolum(md, "Kareler")[-1])  # Kareler son bölüm kalır


def test_tavani_asan_model_ani_incelenmedi(ortam):
    _, md = paket(ortam, OcrKos({"k00300": KOD, "k00100": KOD}, sahne_rc=0), kare=1)  # aday 5:00 (eşit aralık) + 1:40 (sahne)
    assert [s.split(" · ")[1] for s in bolum(md, "Kareler")] == ["5:00"]
    assert bolum(md, "İncelenmedi") == ["[1:40] kare tavanı 1"]


def test_ocr_yoksa_kareler_eskisi_gibi_sebep_yazilir(ortam):
    _, md = paket(ortam, OcrKos({}, rc=2))
    assert bolum(md, "Ekran metni (OCR)")[0].startswith("OCR yok (") and "en-US" in bolum(md, "Ekran metni (OCR)")[0]
    assert [s.split(" · ")[1] for s in bolum(md, "Kareler")] == ["2:30", "7:30"]


def test_jpeg_vekili_kalkti_aday_sahne_sureye_gore(ortam, monkeypatch):
    assert not hasattr(cli, "_yogunluk")
    istek = []
    monkeypatch.setattr(cli, "_sahneler", lambda ctx, d, n: istek.append(n) or [])
    onbellek(ortam, [], duration=3600)
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=OcrKos({}), uyku=lambda s: None) == 0
    assert istek == [3600 // cli.OCR_ADAY_SN]  # uzun video: dakikada bir sahne adayı (en az 2×kare)
