from video import karar


def test_satir_kisaltir_ve_kunye():
    s = karar.satir({"ad": "X", "ne_dedi": " ".join(["k"] * 30)}, {"aciklama": "a " * 50, "lisans": "MIT", "yildiz": 5, "push": "2026-10-01"}).split("\t")
    assert len(s) == 5 and len(s[1].split()) == 20 and len(s[2].split()) == 40 and s[3:] == ["MIT", "5·2026-10-01"]


def test_repo_esi_zayif_eslesme_reddedilir_ozet_repo_bulunamadi():
    assert karar.repo_esi("RustFS", "rustfs/rustfs") and karar.repo_esi("Page Agent", "alibaba/page-agent") and karar.repo_esi("uv", "astral-sh/uv")
    assert not karar.repo_esi("GLM 5.3 Flash", "MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks")  # d3: barındırılan model ↔ üçüncü taraf dağıtım reposu
    assert not karar.repo_esi("Sales Navigator", "padmanabhan-s/scraping-linkedin-salesNavigator")
    assert karar.satir({"ad": "GLM 5.3 Flash", "ne_dedi": "x"}).split("\t")[2] == "repo bulunamadı"


def test_sorulacak_bilinmeyen_ya_da_surum_farki():
    assert karar.sorulacak({"ne_dedi": "x"}, None)
    assert not karar.sorulacak({"ne_dedi": "aynı"}, "kurulu:a")
    assert karar.sorulacak({"ne_dedi": "v2.1 çıktı"}, "kurulu:a")


def test_ayristir_yalniz_sorulan_ve_gecerli_karar():
    t = "A\tkur\tiyi\nB\tBELKI\tx\nZ\tATLA\tsorulmadı\nbozuk"
    assert karar.ayristir(t, ["A", "B"]) == {"A": ("KUR", "iyi")}


def test_ver_onbellek_ayni_kanit_sormaz_parti_tek_cagri(tmp_path):
    yol, cagri = tmp_path / "karar.tsv", []

    def cagir(sistem, metin, sema, **k):
        cagri.append(metin)
        return {"form": {"tsv": "\n".join(f"{s.split(chr(9))[0]}\tDENE\tg" for s in metin.splitlines())}, "usage": {}, "sure": 1, "hata": None}

    istek = {"A": ("A\tk\t\t\t", {"repo": "o/a"}), "B": ("B\tk\t\t\t", None)}
    out, c = karar.ver(istek, env={}, cagir=cagir, yol=yol)
    assert out == {"A": ("DENE", "g"), "B": ("DENE", "g")} and len(c) == 1 and cagri[0].count("\n") == 1
    out, c = karar.ver(istek, env={}, cagir=cagir, yol=yol)  # ikinci kez: önbellekten, çağrı yok
    assert out["A"] == ("DENE", "g") and c == []
    out, c = karar.ver({"A": ("A\tk\t\t\t", {"repo": "o/yeni"})}, env={}, cagir=cagir, yol=yol)  # yeni kanıt → yeniden sorulur
    assert len(c) == 1
