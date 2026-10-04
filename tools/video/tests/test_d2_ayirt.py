"""DERİNLİK-MASTER D2 ayırt edicilik + bağlam kuralı (Ömer kararı, 5 Eki): sözlük eşleşmesi engelleyen olur eğer (i) ad ayırt ediciyse
(tire/rakam/nokta/iç büyük harf ya da ≥5 harf ve YAYGIN değil) ya da (ii) aynı satırda araç işaretiyle geçiyorsa (skill · plugin · MCP ·
CLI · extension · agent · server komşu sözcük, "/ad", "ad-skill"/"ad-mcp", kurulum komutu, owner/repo); yoksa düşük güven.
İç büyük harfli tek kelime (LangGraph) tek geçişte de düşük güven."""

from video import tarama as tr

RAPOR = "## Künye\nşema 2\n## İz\n"
SOZ = ["taste", "design", "superpowers"]


def _video(tmp_path, satir):
    p = tmp_path / "paket.md"
    p.write_text(f"## Segmentler\n[00:01] {satir}\n", encoding="utf-8")
    eng, dus = tr.kacan_video(RAPOR, p, SOZ)
    return [t for _, t in eng], [t for _, t in dus]


def test_taste_skill_engelleyen(tmp_path):
    assert _video(tmp_path, "then the taste skill kurdum") == (["taste"], [])
    assert _video(tmp_path, "kurdum taste-skill bugün")[0] == ["taste"]


def test_good_taste_dusuk(tmp_path):
    assert _video(tmp_path, "that is good taste") == ([], ["taste"])


def test_slash_design_engelleyen(tmp_path):
    assert _video(tmp_path, "run /design now") == (["design"], [])


def test_design_is_hard_dusuk(tmp_path):
    assert _video(tmp_path, "design is hard") == ([], ["design"])


def test_superpowers_yalin_engelleyen(tmp_path):
    assert _video(tmp_path, "i use superpowers daily") == (["superpowers"], [])


def test_ic_buyuk_harf_tek_gecis_dusuk():
    assert tr.kacan_dusuk(RAPOR, [("paket", "we build it with LangGraph today")], SOZ) == [("paket", "LangGraph")]
