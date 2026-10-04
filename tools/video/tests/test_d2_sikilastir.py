"""DERİNLİK-MASTER D2 sıkılaştırma (Ömer kararı, 5 Eki): (a) owner/repo engelleyen yalnız iki taraf ≥2 karakter, ikisinde de harf var ve
kalıp DESEN_YASAK'ta değilse; gürültüden gelen owner/repo düşük güven. (b) raporun herhangi bir bölümünde geçen URL kaçak değil; SOSYAL
alan adları düşük güven. (c) YAYGIN'a "me", "al"."""

from video import tarama as tr

RAPOR = "## Künye\nşema 2\n## Açıklama bağlantıları\n- https://foo.dev/kit\n## İz\n"


def _video(tmp_path, satir, gurultu=None):
    p = tmp_path / "paket.md"
    p.write_text(f"## Açıklama bağlantıları\nyok\n## Segmentler\n[00:01] {satir}\n", encoding="utf-8")
    if gurultu:
        (tmp_path / "ocr-gurultu.txt").write_text(gurultu, encoding="utf-8")
    eng, dus = tr.kacan_video(RAPOR, p, [])
    return [t for _, t in eng], [t for _, t in dus]


def test_owner_repo_yasak_kalip_hic(tmp_path):
    assert _video(tmp_path, "we ran an A/B test and some i/o work") == ([], [])


def test_owner_repo_gurultuden_dusuk(tmp_path):
    assert _video(tmp_path, "nothing here", "00:05 · Z/57\n") == ([], ["Z/57"])


def test_owner_repo_gercek_engelleyen(tmp_path):
    assert _video(tmp_path, "clone affaan-m/everything-claude-code now") == (["affaan-m/everything-claude-code"], [])


def test_raporda_gecen_url_hic(tmp_path):
    assert _video(tmp_path, "see https://foo.dev/kit for more") == ([], [])


def test_sosyal_url_dusuk_github_engelleyen(tmp_path):
    assert _video(tmp_path, "follow https://instagram.com/someone") == ([], ["https://instagram.com/someone"])
    assert _video(tmp_path, "repo https://github.com/x/y here") == (["https://github.com/x/y"], [])


def test_yaygin_me_al():
    k = [("paket", "call Me now and Me again, then Al said Al is here")]
    assert tr.kacan_dusuk(RAPOR, k, []) == []
