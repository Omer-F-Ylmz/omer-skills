"""18 kalite kapısı + skill fabrikası: görev başarısı (makine kontrolü) · gürültü bandı · uret (tavan · 8-gram · KAYNAK.md) · RED şablonu · caveman yeni özellikler."""
import time

import pytest

from video import kur, uygula as uy
from video.cli import kos as gercek_kos, main

from test_kur import KKos, SJev, deneme
from test_uygula import UKos, calis, kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

A = {"cikti": 100, "kalite": 3.0, "maliyet": 0.01}
E = {"cikti": 25, "maliyet": None}


# --- K1 karar ---

def test_token_tutsa_da_bir_gorevde_basari_dusukse_red_kalite():
    k = kur.karar(A, {"cikti": 50, "kalite": 3.0, "maliyet": 0.005}, E, 0.0, [(1.0, 1), (1.0, 0), (0.0, 0)])
    assert k.startswith("RED(kalite)")


def test_gurultu_icinde_kalite_gecer():
    assert kur.karar(A, {"cikti": 50, "kalite": 2.95, "maliyet": 0.005}, E, 0.1, [(1.0, 1)]).startswith("KUR önerisi")


def test_gurultu_disinda_kalite_red():
    assert kur.karar(A, {"cikti": 50, "kalite": 2.8, "maliyet": 0.005}, E, 0.05, [(1.0, 1)]).startswith("RED(kalite)")


def test_token_tutmazsa_red_token():
    assert kur.karar(A, {"cikti": 90, "kalite": 3.0, "maliyet": 0.01}, E, 0.0, [(1.0, 1)]).startswith("RED(token)")


# --- K1 beklenen: makine kontrolü ---

HATALI = "def kdv_dahil(fiyat, oran=20):\n    return round(fiyat + oran / 100, 2)\n"
DOGRU = "def kdv_dahil(fiyat, oran=20):\n    return round(fiyat * (1 + oran / 100), 2)\n"
TEST = "from fiyat import kdv_dahil\n\n\ndef test_kdv():\n    assert kdv_dahil(100) == 120\n    assert kdv_dahil(50, 10) == 55\n"


@pytest.fixture
def gorev(tmp_path):
    (tmp_path / "fixture").mkdir()
    (tmp_path / "fixture" / "fiyat.py").write_text(HATALI, encoding="utf-8")
    (tmp_path / "fixture" / "test_fiyat.py").write_text(TEST, encoding="utf-8")
    g = tmp_path / "4-kod.md"
    g.write_text("Hatayı düzelt, tam dosyayı ver.\ndosya: fixture/fiyat.py\nbeklenen:\n- pytest: fixture/test_fiyat.py\n- olgu: (?i)düzelt\n- yasak: (?i)sayın\n",
                 encoding="utf-8")
    return g


def test_pytest_beklenen_dogru_yanlis(gorev):
    assert kur.basari(gorev, f"Düzeltme kdv:\n```python\n{DOGRU}```", gercek_kos)[0]
    assert not kur.basari(gorev, f"Düzeltme kdv:\n```python\n{HATALI}```", gercek_kos)[0]
    assert not kur.basari(gorev, f"Sayın kullanıcı, kdv:\n```python\n{DOGRU}```", gercek_kos)[0]  # yasak desen
    assert not kur.basari(gorev, f"```python\n{DOGRU}```", gercek_kos)[0]  # zorunlu olgu yok


def test_beklenen_istemde_yok(gorev):
    assert "beklenen" not in kur._istem(gorev) and "pytest:" not in kur._istem(gorev) and "def kdv_dahil" in kur._istem(gorev)


# --- K2 uret ---

KAYNAK = ("Respond terse like smart caveman all technical substance stay only fluff die drop articles filler pleasantries "
          "and hedging fragments are fine short synonyms are fine code blocks unchanged errors quoted exact")


def uyarlama(kok, ad="u", arac="talimat", tavan=40, lisans="MIT"):
    d = kok / "docs" / "uyarlamalar"
    d.mkdir(parents=True, exist_ok=True)
    (kok / "docs" / "k.md").write_text(KAYNAK, encoding="utf-8")
    (d / f"{ad}.md").write_text(f"# Uyarlama: {ad}\narac: {arac}\ntoken_tavani: {tavan}\nkaynak_metin: docs/k.md\nlisans: {lisans}\n\n## Fikir\nkısa yaz\n",
                                encoding="utf-8")
    g = kok / "docs" / "denemeler" / "gorevler"
    g.mkdir(parents=True, exist_ok=True)
    for i in (1, 2):
        (g / f"{i}-g.md").write_text(f"Görev {i}: açıkla.\n", encoding="utf-8")
    return d


def taslak(kok, govde, ad="u", arac="talimat"):
    y = kok / ("docs/uyarlamalar/" + f"{ad}-talimat.md" if arac == "talimat" else f"skills/{ad}/SKILL.md")
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(f"---\nname: {ad}\ndescription: Use when yanıt açıklama metni içeriyorsa kullan.\n---\n{govde}\n", encoding="utf-8")
    return y


def test_uret_taslak_yoksa_brief_kosmaz(ortam, kok, capsys):
    uyarlama(kok)
    k = KKos()
    assert main(["uret", "u"], env=ortam, kos=k, gonder=SJev()) == 3
    assert k.cagri == [] and "u-talimat.md" in capsys.readouterr().out


def test_uret_tavani_asan_taslak_hata(ortam, kok, capsys):
    uyarlama(kok, tavan=10)
    taslak(kok, "Hitap yok. Dolgu yok. Çekince yok. Tekrar yok. Kod, komut, yol ve hata mesajı olduğu gibi kalır; yalnız açıklama kısalır.")
    k = KKos()
    assert main(["uret", "u"], env=ortam, kos=k, gonder=SJev()) == 2
    assert k.cagri == [] and "tavan" in capsys.readouterr().out


def test_uret_kaynakla_ortusme_hata(ortam, kok, capsys):
    uyarlama(kok, tavan=200)
    taslak(kok, KAYNAK)
    k = KKos()
    assert main(["uret", "u"], env=ortam, kos=k, gonder=SJev()) == 2
    assert k.cagri == [] and "örtüşme" in capsys.readouterr().out


def test_ortusme_olcumu():
    assert kur.ortusme(KAYNAK, KAYNAK) == 1.0
    assert kur.ortusme("Hitap yok, dolgu yok; kod ve komut aynen kalır, açıklama kısalır ve Türkçe doğal kalır her zaman.", KAYNAK) == 0.0


def test_uret_mit_kaynak_md_ve_dene(ortam, kok, capsys):
    uyarlama(kok, arac="skill", tavan=200)
    taslak(kok, "Hitap yok. Dolgu yok. Kod ve komut aynen kalır; yalnız açıklama kısalır.", arac="skill")
    k = KKos()
    assert main(["uret", "u"], env=ortam, kos=k, gonder=SJev()) == 0
    assert "MIT" in (kok / "skills" / "u" / "KAYNAK.md").read_text(encoding="utf-8")
    assert len(k.claude()) == 8  # 2 görev × 2 kol × 2 koşu (20a)
    assert "## Talimat\nskills/u/SKILL.md" in (kok / "docs" / "denemeler" / "u.md").read_text(encoding="utf-8")
    b = [c for c in k.claude() if "--append-system-prompt" in c]
    assert b and all("name: u" not in c[-1] and "Hitap yok" in c[-1] for c in b)  # frontmatter B'ye gitmez
    assert (kok / "bilgi" / "u.md").is_file()  # SJev B 2.8 < A 3.0 − 0.1 → RED(kalite) → bilgi kartı


# --- K0 RED şablonu · caveman ---

def test_red_aday_eksik_uretmez(ortam, kok, capsys):
    y = kok / "docs" / "kurulumlar" / "adaylar" / "php-x.md"
    y.write_text("# php-x\nad: php-x\ntur: CLI\nkarar: RED\ngerekce: PHP projesi yok\n", encoding="utf-8")
    assert calis(ortam, [y], UKos()) == 0
    r = next((kok / "docs" / "kurulumlar").glob("*-uygula.md")).read_text(encoding="utf-8")
    assert "(eksik)" not in r and "PHP projesi yok" in r and "eksik alan" not in capsys.readouterr().out


def test_caveman_yeni_ozellikler_token_dene(ortam):
    y = uy.KOK / "docs" / "kurulumlar" / "adaylar" / "caveman.md"
    metin = y.read_text(encoding="utf-8")
    oz = {o["ozellik"]: o for o in uy.ozellikler(metin)}
    assert {"convert", "browse", "shrink", "cavecrew", "calisma-kaliplari", "trial"} <= set(oz)
    for s in ("convert", "browse", "shrink"):
        assert "token" in oz[s]["etiket"] and uy.ozellik_karar(oz[s], uy.alanlar(metin), metin, uy.KOK, ortam)[0] == "DENE"
    assert oz["cavecrew"]["karar"] == oz["trial"]["karar"] == "UYARLA" and oz["calisma-kaliplari"]["karar"] == "ÖĞREN"
    assert uy.iddia_sinama(metin)[1] == []  # parantezli sonuçlar geçerli


def test_kismen_dogru_parantezli_sonuc_gecerli():
    m = "## İddia sınama\n| iddia | kaynak | sonuç | not | kart |\n|---|---|---|---|---|\n| x | docs/cikti-notlari.md | kısmen doğru (çıktı içinde) | n | - |\n"
    s, h = uy.iddia_sinama(m)
    assert h == [] and s[0]["sonuc"] == "kısmen doğru (çıktı içinde)"


# --- 18 düzeltme: felaket geri izleme · satır sayısı · kontrol zaman aşımı · önbellek ---

FELAKET = r"(?:[^\n]*\S[^\n]*(?:\n+|$)){11}"


def test_felaket_desenli_gorev_yuklenirken_reddedilir(ortam, kok, capsys):
    deneme(kok)
    (kok / "docs" / "denemeler" / "gorevler" / "4-f.md").write_text(f"Kısa yaz.\nbeklenen:\n- yasak: {FELAKET}\n", encoding="utf-8")
    k, t = KKos(), time.monotonic()
    assert main(["dene", "deneme"], env=ortam, kos=k, gonder=SJev()) == 1
    assert time.monotonic() - t <= 2 and k.cagri == [] and "4-f.md" in capsys.readouterr().out


def test_satir_en_fazla_bos_olmayan_satiri_sayar(tmp_path):
    g = tmp_path / "g.md"
    g.write_text("Yaz.\nbeklenen:\n- satir-en-fazla: 10\n", encoding="utf-8")
    assert kur.basari(g, "\n\n".join(["x"] * 10) + "\n  \n", gercek_kos)[0]
    assert not kur.basari(g, "\n".join(["x"] * 11), gercek_kos)[0]


def test_satir_deseni_her_satiri_kodla_denetler(tmp_path):
    g = tmp_path / "g.md"
    g.write_text("Yaz.\nbeklenen:\n- satir-en-fazla: 2\n- satir-desen: - `git [^`]*`|BİTTİ\n", encoding="utf-8")
    assert kur.basari(g, "- `git fetch`\nBİTTİ\n", gercek_kos)[0]
    assert not kur.basari(g, "Tabii\nBİTTİ", gercek_kos)[0]


def test_kontrol_zaman_asimi_basarisiz_doner(tmp_path, monkeypatch):
    monkeypatch.setattr(kur, "KONTROL_SN", 1)
    g = tmp_path / "g.md"
    g.write_text(f"Yaz.\nbeklenen:\n- yasak: {FELAKET}\n", encoding="utf-8")
    t = time.monotonic()
    ok, neden = kur.basari(g, "a" * 50000, gercek_kos)
    assert not ok and "zaman aşımı" in neden and time.monotonic() - t <= 5


def test_onbellekteki_sonuc_yeniden_cagrilmaz(ortam, kok):
    deneme(kok)
    assert main(["dene", "deneme"], env=ortam, kos=KKos(), gonder=SJev()) == 0
    assert (kok / "docs" / "denemeler" / ".kos" / "deneme" / "1-g-A-2.json").is_file()
    k = KKos()
    assert main(["dene", "deneme"], env=ortam, kos=k, gonder=SJev()) == 0 and k.claude() == []
    (kok / "docs" / "denemeler" / "deneme-talimat.md").write_text("BAŞKA", encoding="utf-8")
    k = KKos()
    assert main(["dene", "deneme"], env=ortam, kos=k, gonder=SJev()) == 0
    assert len(k.claude()) == 6 and all("--append-system-prompt" in c for c in k.claude())  # yalnız B (3 görev × 2 koşu): talimat hash'i değişti
