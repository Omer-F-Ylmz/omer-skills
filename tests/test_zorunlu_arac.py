"""ZORUNLU-ARAÇ-1: ön uçuş bloğu, döküm sayımı (arac_eksik / kanit_eksik), yeniden istem, koşul uyarısı."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos/kopru"))
import zorunlu_arac as z

LISTE = [{"ad": "pixeljury", "tur": "skill", "cagri": "Skill pixeljury", "ne": "gorsel QA"},
         {"ad": "okuyucu", "tur": "ajan", "cagri": "Agent okuyucu", "ne": "salt okuma"},
         {"ad": "ffmpeg", "tur": "cli", "cagri": "Bash: ffmpeg", "ne": "video"},
         {"ad": "katalog_ara", "tur": "arac", "cagri": "python tools/katalog_ara.py", "ne": "katalog"}]


def dokum(tmp, sid, araclar):
    """araclar: [(arac adı, input)] → ~/.claude/projects/<x>/<sid>.jsonl benzeri döküm."""
    d = tmp / "proje"
    d.mkdir(exist_ok=True)
    satirlar = [{"message": {"content": [{"type": "tool_use", "name": a, "input": i}]}} for a, i in araclar]
    (d / f"{sid}.jsonl").write_text("\n".join(json.dumps(s) for s in satirlar), encoding="utf-8")


def kur(tmp, monkeypatch, ad, sid, liste, gorsel, araclar):
    monkeypatch.setattr(z, "SIRA", tmp)
    monkeypatch.setattr(z, "PROJELER", tmp)
    (tmp / f"{ad}.zorunlu.json").write_text(json.dumps({"araclar": liste, "gorsel": gorsel}), encoding="utf-8")
    (tmp / f"{ad}.json").write_text(json.dumps({"session_id": sid}), encoding="utf-8")
    dokum(tmp, sid, araclar)


def test_hic_arac_kullanilmadi_arac_eksik(tmp_path, monkeypatch):
    kur(tmp_path, monkeypatch, "a1", "s1", LISTE, False, [("Read", {}), ("Bash", {"command": "git status"})])
    d = z.denetle("a1")
    assert d["durum"] == "arac_eksik" and len(d["eksik"]) == 4
    assert json.loads((tmp_path / "a1.denetim.json").read_text())["durum"] == "arac_eksik"


def test_yeterince_arac_kullanildi_ok(tmp_path, monkeypatch):
    kur(tmp_path, monkeypatch, "a2", "s2", LISTE, False,
        [("Skill", {"skill": "slash-dar:pixeljury"}), ("Agent", {"subagent_type": "okuyucu"}), ("Bash", {"command": "ffmpeg -i x"})])
    d = z.denetle("a2")
    assert d == {"durum": "ok", "eksik": ["katalog_ara"]}  # 1 eksik < min(3, 2)


def test_gorsel_is_hakemsiz_kanit_eksik(tmp_path, monkeypatch):
    kur(tmp_path, monkeypatch, "a3", "s3", LISTE, True,
        [("Skill", {"skill": "pixeljury"}), ("Agent", {"subagent_type": "okuyucu"}), ("Bash", {"command": "ffmpeg x"})])
    assert z.denetle("a3")["durum"] == "kanit_eksik"
    dokum(tmp_path, "s3", [("Skill", {"skill": "pixeljury"}), ("Agent", {"subagent_type": "okuyucu"}),
                           ("Bash", {"command": "ffmpeg x && python .kos/kopru/gorsel_hakem.py a.png"})])
    assert z.denetle("a3")["durum"] == "ok"


def test_liste_ya_da_dokum_yoksa_none(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "SIRA", tmp_path)
    monkeypatch.setattr(z, "PROJELER", tmp_path)
    assert z.denetle("yok") is None
    (tmp_path / "b.zorunlu.json").write_text(json.dumps({"araclar": LISTE, "gorsel": False}))
    (tmp_path / "b.json").write_text(json.dumps({"session_id": "yok-sid"}))
    assert z.denetle("b") is None


def test_kisa_liste_yarisi_esik():
    k = ([], [], [], [])
    assert z.karar(LISTE[:2], False, k)[0] == "arac_eksik"  # 2 araçta eşik = 1
    assert z.karar([], False, k)[0] == "ok"


def test_blok_ve_yeniden_istem(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "SIRA", tmp_path)
    monkeypatch.setattr(z, "GOREV", tmp_path)
    monkeypatch.setattr(z, "KOK", tmp_path)
    monkeypatch.setattr(z, "araclar", lambda m: LISTE)
    monkeypatch.setattr(z, "_calistir", lambda a, s: "")
    b = z.blok("g1", "logo render işi")
    assert b.startswith("ZORUNLU ARAÇLAR") and "pixeljury (skill)" in b and "gorsel_hakem" in b
    assert json.loads((tmp_path / "g1.zorunlu.json").read_text())["gorsel"] is True
    (tmp_path / "g.md").write_text("görev", encoding="utf-8")
    yol = z.yeniden_istem("g1", "g.md", ["okuyucu", "ffmpeg"])
    assert yol == "g1-a.md" and "kullanmadığın araçlar: okuyucu, ffmpeg" in (tmp_path / yol).read_text(encoding="utf-8")
    monkeypatch.setattr(z, "araclar", lambda m: [])
    assert z.blok("g2", "x") == ""  # katalog boş → blok yok, görev bozulmaz


GOREV_3D = ("# ABC-2 — landing sayfası\n\n## İLK VE BAĞLAYICI\nthree.js sahnesi, `web-sahne-desenleri` ile; git ve mcp-server-git geçsin.\n"
            "\n## SONRA\nblender render video kurulum")


def test_kapsam_baslik_oneki_atar_ve_bolumle_sinirlar():
    k = z.kapsam(GOREV_3D)
    assert k.startswith("landing sayfası") and "web-sahne-desenleri" in k and "SONRA" not in k and "blender" not in k


def test_tur_bul_esitlikte_diger():
    assert z.tur_bul("three.js landing")[0] == "site-3d"
    assert z.tur_bul("render ve video")[0] == "diğer"  # 1-1 eşitlik
    assert z.tur_bul("merhaba") == ("diğer", [])


def test_araclar_ozel_liste_genel_kayitlar_yok():
    ar = z.araclar(GOREV_3D)
    ad = [o["ad"] for o in ar]
    assert 0 < len(ad) <= z.N
    assert "web-sahne-desenleri" in ad and "threejs-3d-paket" in ad  # anılan + tür çekirdeği
    assert not {"git", "mcp-server-git"} & set(ad) and "blender-uretim" not in ad  # genel elenir, kapsam dışı tür girmez


def test_yeniden_kosu_kapali_ve_ad_alanli_skill_sayilir():
    assert z.YENIDEN is False
    k = (["slash-dar:frontend-craft"], [], [], [])
    assert z._kullanildi({"ad": "frontend-craft:frontend-craft", "tur": "skill"}, k)


def test_kosul_gorev_dosyasinda_geciyorsa_uyar(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "KOK", tmp_path)
    (tmp_path / "t.md").write_text("İLK VE BAĞLAYICI ...", encoding="utf-8")
    assert "kendi içinde" in z.kosul_uyari("t.md::İLK VE BAĞLAYICI", "t.md")
    assert z.kosul_uyari("t.md::BAŞKA", "t.md") == ""
    assert z.kosul_uyari("", "t.md") == ""


def test_kombin_cekirdek_ogrenme_denetimi(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "KOK", tmp_path)
    kombin = [{"id": "s3d-hazir-sahne", "adimlar": ["varlik_indir", "gltf-transform", "threejs-3d-paket"]}]
    kur(tmp_path, monkeypatch, "k1", "s1", LISTE[:1], False, [("Skill", {"skill": "threejs-3d-paket"}), ("Bash", {"command": "rtk git status"})])
    (tmp_path / "k1.zorunlu.json").write_text(json.dumps({"araclar": LISTE[:1], "gorsel": False, "kombin": kombin, "tur": "site-3d", "hata": ""}), encoding="utf-8")
    d = z.denetle("k1")
    assert d["kombin"] == ["s3d-hazir-sahne 1/3"] and "beyin" in d["cekirdek_eksik"] and "graphify" in d["cekirdek_eksik"] and "rtk" not in d["cekirdek_eksik"]
    assert d["ogrenme_eksik"] == ["basta", "sonda"] and "ogrenme_eksik" in d["durum"] and "arac_eksik" in d["durum"]


def test_kombin_sec_ve_dogrula():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import kombin_sec
    assert kombin_sec.dogrula() == []  # kombin + tür seti adları katalogda
    assert len(kombin_sec.yukle(kombin_sec.KOMBIN)["kombinler"]) >= 60
    assert kombin_sec.sec("three.js landing sayfası", 2, "site-3d")[1]
