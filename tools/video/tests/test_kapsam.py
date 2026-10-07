"""VİDEO-GÖZ-1b-1 M0: `video altin kapsam` — altın adaylarının paket.md metninde geçme oranı (LLM yok)."""
import subprocess
import sys
from pathlib import Path

from video import altin as au
from video import cli

PAKET = """# x · başlık
## Açıklama bağlantıları
https://github.com/acme/tool
## Segmentler
[0:05] bugün v0 ile Topviev aracını deniyoruz, bolted değil
## Ekran metni
[1:00] dala.craftedbygc.com · npm run build
## Kareler
C:/k/k00060_0.jpg · 1:00
"""


def _altin(**k):
    return {"adaylar": [], "komutlar": [], "urller": [], **k}


def test_kisa_ad_kelime_siniriyla():
    a = _altin(adaylar=[{"ad": "v0", "tur": "araç", "kaynak": "ses"}, {"ad": "Bolt", "tur": "araç", "kaynak": "ses"},
                        {"ad": "n8n", "tur": "araç", "kaynak": "ekran"}])
    p = au.kapsam(PAKET + "nv0x n8nx\n", a, boyut=lambda y: None)
    assert p["aday"] == (1, 3)  # v0 kelime; bolted ≠ Bolt; n8nx ≠ n8n


def test_uzun_ad_alt_dize_ve_lev1():
    a = _altin(adaylar=[{"ad": "Topview", "tur": "araç", "kaynak": "ses"},
                        {"ad": "Sonnet 5.5", "alias": ["Claude Sonnet 5.5"], "tur": "model", "kaynak": "ses"},
                        {"ad": "Acme Tool", "tur": "repo", "kaynak": "açıklama"}])
    p = au.kapsam(PAKET, a, boyut=lambda y: None)
    assert p["aday"] == (2, 3)  # Topviev lev 1 · acme/tool alt dize · Sonnet yok


def test_belirsiz_paydada_yok_ama_kacanda_neden():
    a = _altin(adaylar=[{"ad": "Gizli Araç", "tur": "araç", "kaynak": "ekran", "belirsiz": True}])
    p = au.kapsam(PAKET, a, boyut=lambda y: None)
    assert p["aday"] == (0, 0) and p["kacan"] == [("Gizli Araç", "belirsiz")]


def test_kacan_nedeni_kaynaktan():
    a = _altin(adaylar=[{"ad": "Ekranaraci", "kaynak": "ekran", "tur": "a"}, {"ad": "Sesaraci", "kaynak": "ses", "tur": "a"},
                        {"ad": "Aciklamaaraci", "kaynak": "açıklama", "tur": "a"}, {"ad": "Yorumaraci", "kaynak": "yorum", "tur": "a"}])
    assert dict(au.kapsam(PAKET, a, boyut=lambda y: None)["kacan"]) == {
        "Ekranaraci": "ekranda-var-OCR-kaçırdı", "Sesaraci": "ASR-bozdu", "Aciklamaaraci": "açıklamada", "Yorumaraci": "yorumda"}
    sessiz = PAKET.replace("[0:05] bugün v0 ile Topviev aracını deniyoruz, bolted değil", "altyazı yok: kare-yalnız")
    assert au.kapsam(sessiz, _altin(adaylar=[{"ad": "Sesaraci", "kaynak": "ses", "tur": "a"}]), boyut=lambda y: None)["kacan"] == [("Sesaraci", "ses-yok")]


def test_komut_ve_url_kapsami():
    a = _altin(komutlar=[{"komut": "npm run build"}, {"komut": "npx skills add x"}],
               urller=[{"url": "https://dala.craftedbygc.com/"}, {"url": "https://yok.example.com"}])
    p = au.kapsam(PAKET, a, boyut=lambda y: None)
    assert p["komut"] == (1, 2) and p["url"] == (1, 2)


def test_token_metin_ve_kare():
    p = au.kapsam(PAKET, _altin(), boyut=lambda y: (1366, 768))
    assert p["token"] == {"metin": len(PAKET) // 4, "kare": 49 * 28, "kare_n": 1}


def test_cli_altin_kapsam(tmp_path, capsys):
    (tmp_path / "paket.md").write_text(PAKET, encoding="utf-8")
    (tmp_path / "a.json").write_text('{"adaylar": [{"ad": "v0", "tur": "a", "kaynak": "ses"}]}', encoding="utf-8")
    assert cli.main(["altin", "kapsam", str(tmp_path / "paket.md"), str(tmp_path / "a.json")], env={}) == 0
    assert "aday 1/1" in capsys.readouterr().out


def test_altin_jevsiz_ice_alinir():
    kod = "import sys; sys.modules['jev'] = None; from video import altin; print('ok')"
    r = subprocess.run([sys.executable, "-c", kod], cwd=Path(__file__).parents[1], capture_output=True, text=True)
    assert r.stdout.strip() == "ok", r.stderr[-300:]
