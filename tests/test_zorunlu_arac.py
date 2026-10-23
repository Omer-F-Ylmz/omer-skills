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
    assert 0 < len(ad)  # N tavanı yalnız BM25 dolgusuna; çekirdek+şablon tavansız
    assert "departman-frontend" in ad  # site şablonu (ARAÇ-ZORUNLU-4)
    assert "web-sahne-desenleri" in ad and "threejs-3d-paket" in ad  # anılan + tür çekirdeği
    assert not {"git", "mcp-server-git"} & set(ad) and "blender-uretim" not in ad  # genel elenir, kapsam dışı tür girmez


def test_yeniden_kosu_kapali_ve_ad_alanli_skill_sayilir():
    assert z.YENIDEN is True
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


def test_logo_marka_cekirdegin_tamami_listelenir():
    ad = [o["ad"] for o in z.araclar("# BHS5-LOGO-2 — havalı spor markası logosu\n\n## İLK VE BAĞLAYICI\nlogo üret")]
    assert {"illustrasyon-logo-paket", "brandkit", "design-dna", "gorsel-uret"} <= set(ad) and len(ad) >= 4 + 3


def test_intro_animasyon_cekirdegin_tamami_listelenir():
    ad = [o["ad"] for o in z.araclar("# INTRO-1 — site intro animasyonu\n\n## İLK VE BAĞLAYICI\nintro animasyon")]
    assert {"hyperframes-paket", "remotion-video-paket", "animasyon-atolyesi", "hareket-altyazi-3d-paket", "ffmpeg", "blender-uretim"} <= set(ad)


def test_plan_tablosu_gerekce_sutunu(tmp_path, monkeypatch):
    for a, v in (("SIRA", tmp_path), ("GOREV", tmp_path), ("KOK", tmp_path)):
        monkeypatch.setattr(z, a, v)
    monkeypatch.setattr(z, "araclar", lambda m: LISTE)
    monkeypatch.setattr(z, "_calistir", lambda a, s: "")
    b = z.blok("g1", "x")
    assert "PLAN TABLOSU" in b and "kullanılacak adım / kullanılmama gerekçesi" in b and "gerekçesiz atlama" in b


def test_devam_karar_uc_isaret_iki_tur_sonra_dur():
    ok = {"durum": "ok", "eksik": []}
    assert z.devam("a", ok) == (None, "ok")
    for isaret in ("arac_eksik", "kanit_eksik", "ogrenme_eksik", "arac_eksik+tekrar_hata"):
        assert z.devam("a", {"durum": isaret, "eksik": ["x"]})[0] == "a-a"
    assert z.devam("a-a", {"durum": "kanit_eksik", "eksik": []})[0] == "a-a2"
    assert z.devam("a-a2", {"durum": "kanit_eksik", "eksik": []}) == (None, "dur")
    assert z.devam("a", {"durum": "tekrar_hata", "eksik": []}) == (None, "ok")  # tam işaret yok → yanlış alarm 0


def test_eksik_liste_uc_kaynak():
    den = {"durum": "arac_eksik+kanit_eksik+ogrenme_eksik", "eksik": ["ffmpeg"], "cekirdek_eksik": ["rtk"], "ogrenme_eksik": ["sonda"]}
    assert z.eksik_liste(den) == ["ffmpeg", "rtk", "gorsel_hakem", "öğrenme:sonda"]


# ---- ARAÇ-ZORUNLU-4 ----
def test_pasif_cekirdek_ayarlardaysa_eksik_sayilmaz(tmp_path, monkeypatch):
    ayar = tmp_path / "settings.json"
    ayar.write_text('{"hooks": "rtk claude-mem context-mode", "env": "headroom"}', encoding="utf-8")
    monkeypatch.setattr(z, "AYARLAR", ayar)
    yok, _ = z.cekirdek_ogrenme("belge", ([], [], [], []))
    assert set(yok) == {"beyin", "ruflo"}


def test_pasif_cekirdek_ayarda_yoksa_eksik(tmp_path, monkeypatch):
    ayar = tmp_path / "settings.json"
    ayar.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(z, "AYARLAR", ayar)
    yok, _ = z.cekirdek_ogrenme("belge", ([], [], [], []))
    assert {"rtk", "headroom", "claude-mem", "context-mode"} <= set(yok)


def test_canli_is_tam_set_ekler_degilse_bos():
    assert z.canli_set("Siteyi canlıya al, yayın öncesi kontrol") == z.TUR_SET["canli"]["skill"] + z.TUR_SET["canli"]["cli"]
    assert z.canli_set("yerelde bir betik düzelt") == []


def test_sablon_ve_yaratici_kombin_katalogda_gecerli():
    import json as j
    import katalog_ara
    ad = {o["ad"].split(":")[-1] for o in map(j.loads, katalog_ara.KATALOG.read_text(encoding="utf8").splitlines())}
    for a in z.canli_set("canlıya") + [x for s in z.TUR_SET["sablon"].values() for x in s["araclar"]]:
        assert a in ad, a
    assert "REA" in z.yaratici("Landing site yap", "site-3d")


def test_gecmis_yazilir_ve_ders_cikar(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "GECMIS", tmp_path / "gecmis.jsonl")
    for i, (durum, yok) in enumerate([("arac_eksik", ["x"]), ("ok", []), ("arac_eksik", ["x", "y"])]):
        z.gecmis_yaz(f"is{i}", "belge", [{"ad": "x"}, {"ad": "y"}, {"ad": "z"}], {"durum": durum, "eksik": yok})
    d = z.gecmis_ders("belge")
    assert "x 2/3" in d and "is1" in d
    assert z.gecmis_ders("video") == ""


def test_oran_pasif_kurali_ile_yeniden_hesaplar(tmp_path, monkeypatch):
    ayar = tmp_path / "settings.json"
    ayar.write_text("rtk headroom claude-mem context-mode", encoding="utf-8")
    monkeypatch.setattr(z, "AYARLAR", ayar)
    kur(tmp_path, monkeypatch, "o1", "s1", LISTE[:1], False, [("Skill", {"skill": "pixeljury"}), ("Bash", {"command": "beyin ara x; beyin kaydet y"}),
                                                           ("mcp__ruflo__agentdb_pattern-search", {}), ("mcp__ruflo__agentdb_pattern-store", {})])
    (tmp_path / "o1.zorunlu.json").write_text(json.dumps({"araclar": LISTE[:1], "gorsel": False, "tur": "belge"}), encoding="utf-8")
    assert z.oran_yeniden(["o1"])[0] == 0


def test_onucus_beyin_ruflo_sorgusu_kullanilmis_sayilir(tmp_path, monkeypatch):
    ayar = tmp_path / "settings.json"
    ayar.write_text("rtk headroom claude-mem context-mode", encoding="utf-8")
    monkeypatch.setattr(z, "AYARLAR", ayar)
    yok, ogr = z.cekirdek_ogrenme("belge", ([], [], [], []), onucus=("beyin", "ruflo"))
    assert yok == [] and ogr == ["sonda"]


def test_yeniden_istem_yalniz_eksik_adim(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "GOREV", tmp_path)
    monkeypatch.setattr(z, "KOK", tmp_path)
    (tmp_path / "g.md").write_text("iş", encoding="utf-8")
    yol = z.yeniden_istem("g", "g.md", ["x"])
    assert "baştan yapma" in (tmp_path / "g-a.md").read_text(encoding="utf-8") and yol.endswith("g-a.md")


# ---- ZORUNLU-KULLANIM-1: Stop kapısı ----

def kapi_kur(tmp, monkeypatch, sid, liste, araclar):
    monkeypatch.setattr(z, "PROJELER", tmp)
    monkeypatch.setattr(z, "OTURUM", tmp / "zorunlu")
    monkeypatch.setattr(z, "MUAF_LOG", tmp / "muaf.jsonl")
    monkeypatch.setattr(z, "KOK", tmp)
    (tmp / ".kos/kopru").mkdir(parents=True)
    (tmp / "zorunlu").mkdir()
    (tmp / "zorunlu" / f"{sid}.json").write_text(json.dumps({"araclar": liste, "muaf": {}, "red": 0}), encoding="utf-8")
    dokum(tmp, sid, araclar)


def test_kapi_atlayan_oturumu_reddeder(tmp_path, monkeypatch):
    kapi_kur(tmp_path, monkeypatch, "k1", LISTE[:2], [("Skill", {"skill": "pixeljury"})])
    assert z.kapi("k1") == ("red", ["okuyucu"])  # HER araç şart: 2'den 1'i yetmez


def test_kapi_hepsi_kullanildiysa_izin(tmp_path, monkeypatch):
    kapi_kur(tmp_path, monkeypatch, "k2", LISTE[:2], [("Skill", {"skill": "pixeljury"}), ("Agent", {"subagent_type": "okuyucu"})])
    assert z.kapi("k2") == ("izin", [])


def test_kapi_gerekceli_muafiyet_gecer_gerekcesiz_gecmez(tmp_path, monkeypatch):
    kapi_kur(tmp_path, monkeypatch, "k3", LISTE[:2], [("Skill", {"skill": "pixeljury"})])
    with __import__("pytest").raises(ValueError):
        z.muaf_ekle("k3", "okuyucu", "  ")
    z.muaf_ekle("k3", "okuyucu", "salt okuma yok, işe uymuyor")
    assert z.kapi("k3") == ("izin", [])
    assert "okuyucu" in (tmp_path / "muaf.jsonl").read_text(encoding="utf-8")  # denetime düştü


def test_kapi_red_tavani_sonra_izin_ve_rapor(tmp_path, monkeypatch):
    kapi_kur(tmp_path, monkeypatch, "k4", LISTE[:1], [("Read", {})])
    assert [z.kapi("k4")[0] for _ in range(z.RED_TAVAN)] == ["red"] * z.RED_TAVAN
    assert z.kapi("k4") == ("izin", ["pixeljury"])
    assert "k4" in (tmp_path / ".kos/kopru/arac-eksik-rapor.jsonl").read_text(encoding="utf-8")


def test_kapi_liste_yoksa_izin(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "OTURUM", tmp_path)
    assert z.kapi("yok") == ("izin", [])


def test_dolgu_arac_denetime_girmez():
    liste = [{"ad": "a", "tur": "skill", "cagri": "", "ne": ""}, {"ad": "premiere-pro", "tur": "mcp", "cagri": "", "ne": "", "dolgu": True}]
    assert z.karar(liste, False, ([], [], [], [])) == ("arac_eksik", ["a"])  # premiere-pro eksik listesinde yok


def test_ui_isi_ic_betik_seo_istemez_site_ister():
    assert not z.ui_isi("arka-aski-1 — kart_dogrula.py havuz-bos dongusu düzeltmesi, tools/ betiği")
    assert not z.ui_isi("usta-web-1 — web okulu ders kitabı, frontend dersleri")
    assert z.ui_isi("landing page yap: site tasarla")
    assert z.ui_isi("tools/ıcı betik değil, landing sayfası canlıya çıkacak")
    assert z.ui_isi("yeni site yapılacak, hero bölümü")


def _denetim_kur(tmp, monkeypatch, sonuc):
    monkeypatch.setattr(z, "SIRA", tmp)
    monkeypatch.setattr(z, "PROJELER", tmp)
    (tmp / "g1.json").write_text(json.dumps({"session_id": "s1", "result": sonuc}), encoding="utf-8")
    (tmp / "g1.zorunlu.json").write_text(json.dumps({"araclar": LISTE, "gorsel": False}), encoding="utf-8")
    dokum(tmp, "s1", [("Bash", {"command": "git status"})])


def test_gerekceli_atlama_yeniden_kosu_tetiklemez(tmp_path, monkeypatch):
    _denetim_kur(tmp_path, monkeypatch, "Atlanan araç: pixeljury — çünkü iç betik, görsel çıktı yok\nokuyucu kullanılmadı: tek dosya işi, gerek yok (neden: küçük)\nffmpeg atlandı: video işi değil -> gerekçe")
    d = z.denetle("g1")
    assert set(d["gerekceli"]) == {"pixeljury", "okuyucu", "ffmpeg"}
    assert "arac_eksik" not in d["durum"]


def test_gerekcesiz_atlama_arac_eksik_kalir(tmp_path, monkeypatch):
    _denetim_kur(tmp_path, monkeypatch, "iş bitti, 3 test geçti")
    d = z.denetle("g1")
    assert "arac_eksik" in d["durum"] and not d.get("gerekceli")
    assert z.devam("g1", d) == ("g1-a", "devam")
    assert z.devam("g1-a2", d) == (None, "dur")
