import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import zip_denetle as zd  # noqa: E402


def _zip(yol, dosyalar):
    with zipfile.ZipFile(yol, "w") as z:
        for ad, icerik in dosyalar.items():
            z.writestr(ad, icerik)
    return yol


def test_temiz_zip_gecer(tmp_path):
    z = _zip(tmp_path / "a.zip", {"a/SKILL.md": "---\nname: a\ndescription: Does a. Use when a.\n---\n# a\n"})
    assert zd.denetle(z) == []


def test_gorunmez_unicode(tmp_path):
    # IG-41 #164: sıfır genişlik / Unicode etiket karakterleriyle gizlenmiş talimat; .md dışı (ör. görsel) taranmaz
    z = _zip(tmp_path / "g.zip", {"g/SKILL.md": "---\nname: g\ndescription: Does g. Use when g.\n---\nok​gizli\U000E0041\n",
                                  "g/a.png": "​"})
    s = " ".join(zd.denetle(z))
    assert "görünmez" in s and "1 dosyada" in s


def test_claude_ai_ret_nedenleri(tmp_path):
    # 16:40: claude.ai "description cannot contain XML tags" ile reddetti; blender-uretim zip'inde __pycache__ vardı
    z = _zip(tmp_path / "b.zip", {"b/SKILL.md": "---\nname: b\ndescription: says /b <ad|konu>.\n---\n",
                                  "b/references/__pycache__/x.cpython-313.pyc": "x"})
    s = " ".join(zd.denetle(z))
    assert "XML" in s and "__pycache__" in s


def test_belge_ornek_anahtari_yanlis_alarm_degil(tmp_path):
    # 16:50: mukul975 güvenlik paketlerindeki AWS belge örnekleri (AKIAIOSFODNN7EXAMPLE, AKIAXXXX…) gerçek sır değil
    ornek = "AKIA" + "IOSFODNN7EXAMPLE" + " ve AKIA" + "X" * 16 + " ve AKIA" + "EXPOSEDKEY123456"
    z = _zip(tmp_path / "f.zip", {"f/SKILL.md": "---\nname: f\ndescription: Use when f.\n---\n", "f/R.md": ornek})
    assert zd.denetle(z) == []
    gercek = _zip(tmp_path / "g.zip", {"g/SKILL.md": "---\nname: g\ndescription: Use when g.\n---\n",
                                         "g/R.md": "AKIA" + "Q3J7K2LM9PZT4WXY"})
    assert any("gizli" in x for x in zd.denetle(gercek))
    tablo = _zip(tmp_path / "h.zip", {"h/SKILL.md": "---\nname: h\ndescription: Use when h.\n---\n",
                                       "h/R.md": "| Private Key | `-----BEGIN " + "PRIVATE KEY-----` | PEM format |"})
    assert zd.denetle(tablo) == []
    pem = _zip(tmp_path / "i.zip", {"i/SKILL.md": "---\nname: i\ndescription: Use when i.\n---\n",
                                     "i/k.pem": "-----BEGIN " + "PRIVATE KEY-----\n" + "M" * 64 + "\n"})
    assert any("gizli" in x for x in zd.denetle(pem))


def test_derinlik_ve_git_klasoru(tmp_path):
    # 17:47: claude.ai frontend-slides-paket'i "Zip file contains path more than 10 folders deep" ile reddetti; içinde .git/ de vardı
    derin = "j/" + "/".join(f"d{i}" for i in range(10)) + "/x.md"
    z = _zip(tmp_path / "j.zip", {"j/SKILL.md": "---\nname: j\ndescription: Use when j.\n---\n", derin: "x",
                                  "j/r/.git/HEAD": "ref"})
    s = " ".join(zd.denetle(z))
    assert "derin" in s and ".git" in s
    sig = _zip(tmp_path / "k.zip", {"k/SKILL.md": "---\nname: k\ndescription: Use when k.\n---\n",
                                    "k/" + "/".join(f"d{i}" for i in range(8)) + "/x.md": "x"})  # 9 ayraç: sınır içi (red örneği 10 ayraçtı)
    assert zd.denetle(sig) == []


def test_dosya_sayisi_200_siniri(tmp_path):
    # 17:54: claude.ai ajan-getir.zip'i (286 dosya) "Zip contains too many files (maximum 200)" ile reddetti
    bas = {"m/SKILL.md": "---\nname: m\ndescription: Use when m.\n---\n"}
    fazla = _zip(tmp_path / "m.zip", {**bas, **{f"m/r/{i}.md": "x" for i in range(200)}})  # 201 giriş
    assert any("200" in x and "dosya" in x for x in zd.denetle(fazla))
    sinir = _zip(tmp_path / "n.zip", {**bas, **{f"m/r/{i}.md": "x" for i in range(199)}})  # tam 200
    assert zd.denetle(sinir) == []


def test_eksik_ve_uzun(tmp_path):
    assert any("SKILL.md yok" in x for x in zd.denetle(_zip(tmp_path / "c.zip", {"c/README.md": "x"})))
    uzun = _zip(tmp_path / "d.zip", {"d/SKILL.md": "---\nname: d\ndescription: " + "a" * 1100 + "\n---\n"})
    assert any("1024" in x for x in zd.denetle(uzun))
    adsiz = _zip(tmp_path / "e.zip", {"e/SKILL.md": "---\ndescription: x\n---\n"})
    assert any("name" in x for x in zd.denetle(adsiz))
