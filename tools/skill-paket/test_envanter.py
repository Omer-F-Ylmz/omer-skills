import json, sys, zipfile, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import envanter as V


def kur(tmp_path):
    ev = tmp_path / "home"
    for ad, ek in [("var-olan", []), ("qa", []), ("ship", []), ("eksik-bir", [("run.py", "print(1)"), ("a.png", "\x00png")]),
                   ("claude-api", []), ("eksik-iki", [])]:
        d = ev / ".claude" / "skills" / ad
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: aciklama {ad}\n---\n", encoding="utf-8")
        for y, i in ek:
            (d / y).write_text(i, encoding="utf-8")
    j = tmp_path / "ai.json"
    j.write_text(json.dumps({"giris": ["var-olan", "cc-api", "gstack-ship"], "paket_uyesi": ["cc-qa"]}), encoding="utf-8")
    return ev, j


def test_varyantlar(tmp_path):
    ev, j = kur(tmp_path)
    ai = V.ai_adlar(j)
    assert V.var("ship", ai) and V.var("qa", ai)  # gstack- öneki, cc- öneki
    assert V.var("claude-api", ai)  # claude→cc
    assert V.var("CLAUDE-API", ai)
    assert not V.var("yok", ai)


def test_calistir_liste_ve_zip(tmp_path):
    ev, j = kur(tmp_path)
    cik = tmp_path / "o"
    eksik = V.calistir(j, cik, home=ev)
    assert sorted(r["ad"] for r in eksik) == ["eksik-bir", "eksik-iki"]
    tsv = (cik / "envanter-fark.tsv").read_text(encoding="utf-8").splitlines()
    assert tsv[0].startswith("kaynak\tad") and len(tsv) == 3
    z = zipfile.ZipFile(cik / "eksik-metin.zip")
    L = z.namelist()
    liste = json.loads(z.read("_liste.json"))
    assert {x["ad"] for x in liste} == {"eksik-bir", "eksik-iki"}
    on = next(x["on"] for x in liste if x["ad"] == "eksik-bir")
    assert f"{on}/run.py" in L and f"{on}/a.png" not in L
    assert f"{on}/a.png" in z.read("_ikili.tsv").decode()
