"""MOTOR-M2e: kısmi kabul · açıklama kaynaklı kalemde zaman beklenmez · kare sayısı · panel satır doğrulaması · ipucu araç eşleşmesine girmez · alt tür önceliği."""
from types import SimpleNamespace

from test_m2a import V, Sahte, _ctx, _durum, _form, _kurulum, _ns, _pid
from test_m2d import _aday

from video import akil, cli
from video import parti as pt
from video import tarama as tr


# K1 iki yeniden istekten sonra form hâlâ geçmiyor → video kaybolmaz: tamam_eksik + EKSİK işareti + son form diskte
def test_kismi_kabul_iki_yeniden_istekten_sonra(tmp_path, capsys):
    kok = _kurulum(tmp_path, V[:1])
    s = Sahte(bozuk=lambda v, n: True)
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s)) == 0
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert len(s.cagrilar) == 3 and t["durum"] == "tamam_eksik"
    assert t["eksik"] == [["-", "ozet", "boş olamaz"]]
    md = open(t["cikti"], encoding="utf-8").read()
    assert "EKSİK: ozet (boş olamaz)" in md
    assert (kok / ".kos" / _pid(kok) / "form" / f"{V[0]}.json").is_file()
    capsys.readouterr()
    assert cli.rapor_denetle(SimpleNamespace(rapor=t["cikti"]), {"kok": kok / "c", "env": {}}) == 0
    assert "uyarı: 1 EKSİK" in capsys.readouterr().out


# K1 devam --kismi-kabul: diskteki son formdan, çağrısız
def test_devam_kismi_kabul_cagrisiz(tmp_path):
    kok = _kurulum(tmp_path, V[:1])
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Sahte(bozuk=lambda v, n: True)))
    pid = _pid(kok)
    d = _durum(kok)
    d["videolar"][V[0]]["tarama"].update(durum="form_red", cikti=None)
    pt._yaz(kok / ".kos" / pid / "durum.json", d)
    s = Sahte()
    assert pt.parti(_ns("devam", pid, kismi_kabul=True), _ctx(kok, s)) == 0
    assert s.cagrilar == [] and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam_eksik"


# K1 kanıt zamanı yalnız kaynak altyazı|kare kaleminde; açıklama kaynaklı kalemde zaman beklenmez
def test_aciklama_kaynakli_site_ui_zaman_beklenmez():
    f = _form(V[0], "Landing sayfası için CSS animasyon, Tailwind bileşen ve hero tekniği.")
    f["site_ui"] = [{"teknik": "Framer Motion", "ne": "animasyon kütüphanesi", "kanit_zamani": "açıklama", "kaynak": "açıklama"},
                    {"teknik": "21st bileşenleri", "ne": "bileşen kataloğu", "kanit_zamani": "0:05", "kaynak": "altyazı"},
                    {"teknik": "Üçüncü teknik", "ne": "hero düzeni", "kanit_zamani": "belirsiz", "kaynak": "kare"}]
    pk = {"baslik": "t", "kanal": "k", "sure": 30, "dil": "tr", "id": V[0], "metin": "## Segmentler\n[0:00] a\n"}
    z = [h for h in tr.site_ui_denetle(pt.rapor_md(f, pk, [])) if "zamansız" in h]
    assert len(z) == 1 and "Üçüncü" in z[0]


# K2 kare sayısı: short ≤3 · uzun süre/2.5 dk (4–8) · site/UI ≤12
def test_kare_sayisi():
    assert pt.kare_sayisi(50, False)[0] == 3
    assert pt.kare_sayisi(5 * 60, False)[0] == 4
    assert pt.kare_sayisi(20 * 60, False)[0] == 8
    assert pt.kare_sayisi(45 * 60, False)[0] == 8
    assert pt.kare_sayisi(45 * 60, True)[0] == 12
    assert pt.site_mu("Site/UI teknikleri + prompt anatomisi zorunlu") and pt.site_mu("uçtan uca iş akışı + prompt anatomisi")
    assert not pt.site_mu("7 GitHub repo; her biri araç adayı")


# K2 çağrı girdisi ≤40k korunur: aşarsa kare düşürülür, not düşülür
def test_kare_girdi_siniri():
    metin = ""
    while pt.c.token(metin) < pt.GIRDI_TAVAN - 3 * pt.KARE_TK:
        metin += "kelime " * 500
    pk = {V[0]: {"short": False, "metin": metin, "kareler": [f"k{i}.jpg" for i in range(8)]}}
    pt.kare_sigdir(pk)
    p = pk[V[0]]
    assert 0 < len(p["kareler"]) < 8 and pt.c.token(metin) + pt.KARE_TK * len(p["kareler"]) <= pt.GIRDI_TAVAN
    assert "girdi" in p["kare_not"]


PANEL = "| aday | tür | video | lisans | güvenlik | önerilen | gerekçe | Ömer |\n|---|---|---|---|---|---|---|---|\n"


# K3 sütun sayısı bozuk satır → uyarı + satır no, hiçbir karar işlenmez, rc≠0
def test_panel_bozuk_satir_hicbir_karar_islenmez(tmp_path, capsys):
    p = tmp_path / "panel.md"
    p.write_text(PANEL + "| a | CLI | 1 | MIT | - | DENE | g | AL |\n| b | CLI | 1 | MIT | - | g | AL |\n", encoding="utf-8")
    islenen = []
    rc = akil.panel_uygula(SimpleNamespace(panel=str(p)), {"karar": lambda ns, ctx: islenen.append(ns.ad)})
    out = capsys.readouterr().out
    assert rc != 0 and islenen == [] and "satır 4" in out and "sütun sayısı uyuşmuyor" in out


def test_panel_uygula_ozet(tmp_path, capsys):
    p = tmp_path / "panel.md"
    p.write_text(PANEL + "| a | CLI | 1 | MIT | - | DENE | g | AL |\n| b | CLI | 1 | MIT | - | DENE | g | |\n"
                 "| c | CLI | 1 | MIT | - | DENE | g | BELKİ |\n", encoding="utf-8")
    islenen = []
    akil.panel_uygula(SimpleNamespace(panel=str(p)), {"karar": lambda ns, ctx: islenen.append(ns.ad)})
    assert islenen == ["a"] and "işlenen 1 · boş 1 · hatalı 1" in capsys.readouterr().out


def _satir(tmp_path, a):
    (tmp_path / "pd").mkdir(exist_ok=True)
    y = akil.panel(tmp_path / "pd", {"parti": "p", "videolar": {}, "adaylar": {a["ad"]: a}}, tmp_path)
    return next(s for s in y.read_text(encoding="utf-8").splitlines() if s.startswith(f"| {a['ad']} |"))


# K4 ipucu araç eşdeğer/kurulu eşleşmesine sokulmaz (clear ≠ learn)
def test_ipucu_arac_eslesmesine_girmez(tmp_path):
    a = _aday("clear", "learn")
    a.update(tur="ipucu", alt_tur=None, arac=False)
    s = _satir(tmp_path, a)
    assert "| T0 |" in s and "eşdeğer" not in s


# K4 alt tür tek değer: kurulu > servis; çelişkide gerekçede not
def test_alt_tur_cakismasi(tmp_path):
    a = _aday("gosterge", "gösterge-x")
    a.update(alt_tur="servis", esdeger_p=0.2, arac=True)
    s = _satir(tmp_path, a)
    assert "alt tür çakışması" in s and "servis: koşullar" not in s


# TEST-HIJYEN-1: instagram görsel/carousel gönderisinde zaman yerine görsel sırası ("görsel 2/5") kanıt sayılır; reel ve YouTube'da zaman şartı kalır
def _site_ui(kunye, zaman):
    return (f"# r\n\n## Künye\n{kunye}\n\n## Özet\nlanding css tailwind\n\n## Site/UI teknikleri\n| teknik | ne işe yarar | zaman | kaynak |\n|---|---|---|---|\n"
            f"| Form akışı | adım adım form (karede: x) | {zaman} | kare |\n\n## Kareden okunanlar\nform\n")


def test_instagram_gorsel_sirasi_zaman_yerine_kabul():
    ig = "x · süre: 0:00 · platform: instagram · tür: görsel gönderi · yorum: y"
    assert not any("zamansız" in h for h in tr.site_ui_denetle(_site_ui(ig, "görsel 2/5")))
    assert any("zamansız" in h for h in tr.site_ui_denetle(_site_ui(ig, "açıklama")))
    for k in (ig.replace("görsel gönderi", "reel"), "x · süre: 3:00 · https://youtu.be/abc"):  # reel/YouTube: görsel sırası yetmez
        assert any("zamansız" in h for h in tr.site_ui_denetle(_site_ui(k, "görsel 2/5")))
