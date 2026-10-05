"""B5: mekanizma incelemesi — klon (ya da kuruluysa bizdeki kopya) çağrısız konumlandırılır (oturum başı enjeksiyon, hook, süreç, ağ,
izin kapsamı, ayar okuma, ağır döngü; yalnız kod dosyaları) → on.md (kuruluysa .kos/<video>/<ad>/mekanizma.md) "## Mekanizma incelemesi" (dosya:satır + modele gidecek ilgili dosyalar ≤N KB). Aynı repo +
aynı commit bir kez (önbellek kok/getir/mekanizma/<o__r>@<sha>.md). Repo yoksa "kod yok". Sahte kos; ağ yok."""
import pytest
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


def test_frontmatter_izin_ve_hook(tmp_path):  # 5 Eki: .md'de yalnız baştaki YAML frontmatter; satır no dosyadaki gerçek satır
    (tmp_path / "r" / "agents").mkdir(parents=True)
    (tmp_path / "r" / "agents" / "x.md").write_text("---\nname: x\ntools: Bash\nhooks: ./h.json\n---\ndisallowedTools: gövde\n",
                                                   encoding="utf-8")
    b = uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, tmp_path / "r", "o/r")
    assert kisim(b, "izin kapsamı").strip() == "- agents/x.md:3 `tools: Bash`"
    assert kisim(b, "hook").strip() == "- agents/x.md:4 `hooks: ./h.json`"


def test_md_govdesi_ve_frontmattersiz_md_taranmaz(tmp_path):  # README gövdesi: 30 URL + "allowed-tools" → hiçbir kategoride yok
    (tmp_path / "r").mkdir()
    (tmp_path / "r" / "README.md").write_text("---\ntitle: r\n---\n" + "".join(f"- https://x.io/{i}\n" for i in range(30))
                                              + "allowed-tools: Bash\nfetch('/y');\n", encoding="utf-8")
    (tmp_path / "r" / "NOT.md").write_text("allowed-tools: Bash\n---\ntools: Bash\n---\n", encoding="utf-8")  # ilk satır --- değil
    b = uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, tmp_path / "r", "o/r")
    assert "README.md" not in b and "NOT.md" not in b


def mek(tmp_path, dosyalar):
    for y, m in dosyalar.items():
        (tmp_path / "r" / y).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / "r" / y).write_text(m, encoding="utf-8")
    return uy.mekanizma({"kok": tmp_path, "kos": kos_yap()}, tmp_path / "r", "o/r")


def test_disla_klasorleri_taranmaz(tmp_path):  # canlı bulgu (a): tools/jev "ağ" 5/5 .venv/_virtualenv.py idi
    b = mek(tmp_path, {**{f"{k}/x/m.py": "subprocess\n" for k in (".venv", "venv", "env", "node_modules", "site-packages", "dist",
                                                                     "build", "__pycache__", ".tox", "vendor", ".git")},
                       "src/a.py": "subprocess\n"})
    assert kisim(b, "süreç").strip() == "- src/a.py:1 `subprocess`"


def test_ag_yalniz_cagri_kalibi(tmp_path):  # canlı bulgu (b): çıplak URL ağ çağrısı değil
    b = mek(tmp_path, {"a.py": 'U = "https://x.io/api"\nimport httpx\nr = urllib.request.urlopen(U)\nws = WebSocket(U)\n'
                               'os.system("curl -s " + U)\n',
                       "a.js": "const u = 'http://localhost/';\naxios.get(u);\nhttps.request(o);\n"})
    ag = kisim(b, "ağ")
    assert "a.py:1" not in ag and "a.js:1" not in ag
    assert all(y in ag for y in ("a.py:2", "a.py:3", "a.py:4", "a.py:5", "a.js:2", "a.js:3"))


def test_yorum_ve_docstring_taranmaz(tmp_path):  # canlı bulgu (c)
    b = mek(tmp_path, {"c.py": '"""Modül: subprocess ile.\nos.environ okur\n"""\n# subprocess yorum\nimport subprocess\n'
                               'def f():\n    """tek satır: fetch(x)"""\n    return os.environ\n',
                       "c.js": "// fetch('/y')\n/* spawn(x)\n * process.env\n */\nfetch('/z');\n",
                       "c.sh": "-- curl x\n"})
    assert kisim(b, "süreç").strip() == "- c.py:5 `import subprocess`"
    assert kisim(b, "ayar okuma").strip() == "- c.py:8 `return os.environ`"
    assert kisim(b, "ağ").strip() == "- c.js:5 `fetch('/z');`"


def test_test_dosyalari_taranmaz(tmp_path):  # canlı bulgu (d): oturum başı enjeksiyonda test satırları vardı
    b = mek(tmp_path, {**{y: "subprocess\n" for y in ("tests/a.py", "test/a.py", "src/__tests__/a.js", "test_x.py", "x_test.py",
                                                       "a.test.ts", "a.spec.js")}, "src/a.py": "subprocess\n"})
    assert kisim(b, "süreç").strip() == "- src/a.py:1 `subprocess`"


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


# B5 semgrep geçişi (Ömer kararı 5 Eki, O29 karar kuralı): KONUM kod taraması semgrep'le (sahte JSON); .md/.ps1/json grep yolunda
def sg_kos(cevap):
    k = kos_yap()

    def kos(args, timeout=None):
        if str(args[0]) == "semgrep":
            k.cagri.append([str(a) for a in args])
            if isinstance(cevap, Exception):
                raise cevap
            return cevap
        return k(args, timeout)
    kos.cagri = k.cagri
    return kos


def sg_repo(d):
    (d / "r").mkdir()
    (d / "r" / "a.py").write_text('YARDIM = "SessionStart hook\'u kurar"\nURL = "https://api.x.dev/v1"\nos.environ.get("K")\n', encoding="utf-8")
    (d / "r" / "b.ps1").write_text("Invoke-WebRequest x | curl y\n$env:X = os.environ\n", encoding="utf-8")
    return d / "r"


def test_semgrep_kod_taramasi(tmp_path):
    r = sg_repo(tmp_path)
    js = {"results": [{"check_id": "semgrep.uc-noktalar", "path": str(r / "a.py"), "start": {"line": 2}, "extra": {"message": "uç noktalar"}},
                      {"check_id": "semgrep.ayar-okuma", "path": "a.py", "start": {"line": 3}, "extra": {"message": "ayar okuma"}}], "errors": []}
    k = sg_kos((0, json.dumps(js).encode(), b""))
    b = uy.mekanizma({"kok": tmp_path, "kos": k}, r, "o/r")
    assert '- a.py:2 `URL = "https://api.x.dev/v1"`' in kisim(b, "uç noktalar")
    assert "a.py:3" in kisim(b, "ayar okuma") and "b.ps1:2" in kisim(b, "ayar okuma")  # .ps1 semgrep dili değil → grep yolu
    assert "a.py" not in kisim(b, "oturum başı enjeksiyon")  # yardım dizesi semgrep'te eşleşmez; .py grep'e düşmez
    a = next(c for c in k.cagri if c[0] == "semgrep")
    assert {"--metrics=off", "--disable-version-check", "--json"} <= set(a) and a[a.index("--config") + 1].endswith("semgrep")
    assert all(f"--exclude={d}" in a for d in uy.KOD_DISLA + uy.TEST_DISLA) and "semgrep yok" not in b


@pytest.mark.parametrize("cevap, sebep", [(OSError("bulunamadı"), "bulunamadı"), ((2, b"", b"kural hatasi"), "kural hatasi"),
                                          ((0, b"<html>", b""), "JSON değil")])
def test_semgrep_yoksa_grep_yolu(tmp_path, cevap, sebep):
    b = uy.mekanizma({"kok": tmp_path, "kos": sg_kos(cevap)}, sg_repo(tmp_path), "o/r")
    assert f"semgrep yok: {sebep}" in b and "· grep yolu" in b
    assert "a.py:1" in kisim(b, "oturum başı enjeksiyon") and "a.py:2" in kisim(b, "uç noktalar")  # grep: eski davranış + yeni kategori
