"""B5: mekanizma incelemesi — klon (ya da kuruluysa bizdeki kopya) çağrısız konumlandırılır (oturum başı enjeksiyon, hook, süreç, ağ,
izin kapsamı, ayar okuma, ağır döngü; yalnız kod dosyaları) → on.md (kuruluysa .kos/<video>/<ad>/mekanizma.md) "## Mekanizma incelemesi" (dosya:satır + modele gidecek ilgili dosyalar ≤N KB). Aynı repo +
aynı commit bir kez (önbellek kok/getir/mekanizma/<o__r>@<sha>.md). Repo yoksa "kod yok". Sahte kos; ağ yok."""
import json
from pathlib import Path

from video import tarama as tr
from video import uygula as uy
from video.cli import main

from test_uygula import kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


def repo_yap(d):
    (d / "hooks").mkdir(parents=True, exist_ok=True)
    (d / "hooks" / "hooks.json").write_text('{"hooks": {"SessionStart": [{"command": "node a.js"}]}}\n', encoding="utf-8")
    (d / "a.js").write_text("const x = 1;\nrequire('child_process').spawn('x');\nfetch('https://api.x/y');\n", encoding="utf-8")
    (d / "b.py").write_text("import os\nk = os.environ['K']\nwhile True:\n    pass\n", encoding="utf-8")
    (d / "SKILL.md").write_text("---\nallowed-tools: Bash\n---\n", encoding="utf-8")
    (d / ".claude").mkdir(exist_ok=True)
    (d / ".claude" / "settings.json").write_text('{"permissions": {"allow": ["Bash"]}}\n', encoding="utf-8")
    (d / "buyuk.py").write_text("import subprocess\n" + "#" * (uy.MEKANIZMA["kb"] * 1024 + 10) + "\n", encoding="utf-8")
    (d / "notlar.txt").write_text("düz metin\n", encoding="utf-8")


def kos_yap(sha="abc1234"):
    def kos(args, timeout=None):
        args = [str(a) for a in args]
        kos.cagri.append(args)
        if args[:2] == ["git", "clone"]:
            repo_yap(Path(args[-1]))
        if "rev-parse" in args:
            return 0, f"{sha}\n".encode(), b""
        return 0, b"", b""
    kos.cagri = []
    return kos


def kisim(b, ad):
    return tr.bolum(b.replace("### ", "## "), ad)


def test_konumlandirma_dosya_satir_ve_kb_tavani(tmp_path):
    repo_yap(tmp_path / "r")
    b = uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, tmp_path / "r", "o/r")
    assert b.startswith("## Mekanizma incelemesi") and "@ abc1234" in b
    for kat, yer in (("oturum başı enjeksiyon", "hooks/hooks.json:1"), ("süreç", "a.js:2"), ("ağ", "a.js:3"),
                     ("izin kapsamı", "SKILL.md:2"), ("izin kapsamı", ".claude/settings.json:1"), ("ayar okuma", "b.py:2"),
                     ("ağır döngü", "b.py:3")):  # SKILL.md:2 geri geldi (Ömer onayı 5 Eki: .md frontmatter taranır)
        assert yer in kisim(b, kat), kat
    ilgili = kisim(b, "ilgili dosyalar")
    assert "a.js" in ilgili and "b.py" in ilgili and "buyuk.py" not in ilgili and "notlar.txt" not in ilgili  # ≤ MEKANIZMA kb
    assert "dosya:satır" in b and "ayar · sarmalayıcı · kendi sürüm" in b and "iyi yan" in b  # A5'e doldurulacak alanlar


def test_ayni_repo_ayni_commit_bir_kez(tmp_path):
    repo_yap(tmp_path / "r")
    ctx = {"kok": tmp_path, "kos": kos_yap()}
    ilk = uy.mekanizma(ctx, tmp_path / "r", "o/r")
    (tmp_path / "r" / "c.py").write_text("import requests\nrequests.get('https://z')\n", encoding="utf-8")
    assert uy.mekanizma(ctx, tmp_path / "r", "o/r") == ilk  # önbellek
    assert (tmp_path / "getir" / "mekanizma" / "o__r@abc1234.md").is_file()
    assert "c.py:2" in uy.mekanizma({**ctx, "kos": kos_yap("def5678")}, tmp_path / "r", "o/r")  # yeni commit → yeniden


def test_repo_yoksa_kod_yok(tmp_path):
    b = uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, None, "servis")
    assert b.startswith("## Mekanizma incelemesi") and "kod yok" in b and "B2–B4" in b


def test_video_on_mekanizma_bolumu(ortam, kok):  # noqa: F811
    assert main(["on", VID, "cm", "--repo", "o/cm", "--tur", "plugin"], env=ortam, kos=kos_yap()) == 0
    assert "a.js:2" in kisim(next(kok.rglob("on.md")).read_text(encoding="utf-8"), "süreç")


def test_kurulu_bizdeki_kopya(ortam, kok, capsys):  # noqa: F811
    repo_yap(Path(ortam["VIDEO_EV"]) / ".claude" / "skills" / "cm")
    (kok / "docs" / "departmanlar").mkdir(parents=True, exist_ok=True)
    (kok / "docs" / "departmanlar" / "envanter.json").write_text(json.dumps([{"ad": "cm", "tur": "skill"}]), encoding="utf-8")
    assert main(["on", VID, "cm", "--tur", "skill"], env=ortam, kos=kos_yap()) == 0
    assert "ZATEN VAR" in capsys.readouterr().out
    assert not list(kok.rglob("on.md"))  # 5 Eki (b): kurulu araçta on.md yok (test_24e:37), çıktı mekanizma.md
    m = (kok / ".kos" / VID / "cm" / "mekanizma.md").read_text(encoding="utf-8")
    assert "bizdeki kopya" in m and "a.js:3" in kisim(m, "ağ")


def test_belge_dosyasi_taranmaz(tmp_path):  # 5 Eki: README linkleri ağ kategorisinin satır sınırını doldurmaz
    (tmp_path / "r").mkdir()
    (tmp_path / "r" / "README.md").write_text("".join(f"- https://x.io/{i}\n" for i in range(30)), encoding="utf-8")
    (tmp_path / "r" / "a.js").write_text("fetch('/y');\n", encoding="utf-8")
    assert kisim(uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, tmp_path / "r", "o/r"), "ağ").strip() == "- a.js:1 `fetch('/y');`"


def test_gelistir_mekanizma_okur(tmp_path):  # tüketici: ZATEN VAR karşılaştırması bizdeki kopyanın mekanizma.md'sini görür
    from test_m2f import Tasiyici, _a, _d
    from test_m2a import V
    from video import akil
    (tmp_path / ".kos" / V[0] / "a1").mkdir(parents=True)
    (tmp_path / ".kos" / V[0] / "a1" / "mekanizma.md").write_text("## Mekanizma incelemesi\nMEKX a.js:3\n", encoding="utf-8")
    (tmp_path / "p").mkdir()
    d, t = _d(), Tasiyici({"satirlar": []})
    d["adaylar"] = {"a1": _a("rtk")}
    akil.gelistir(tmp_path / "p", d, tmp_path, {"env": {}, "cagir": t})
    assert len(t.cagrilar) == 1 and "MEKX a.js:3" in t.cagrilar[0]
