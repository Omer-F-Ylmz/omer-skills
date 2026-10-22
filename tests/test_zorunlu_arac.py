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


def test_kosul_gorev_dosyasinda_geciyorsa_uyar(tmp_path, monkeypatch):
    monkeypatch.setattr(z, "KOK", tmp_path)
    (tmp_path / "t.md").write_text("İLK VE BAĞLAYICI ...", encoding="utf-8")
    assert "kendi içinde" in z.kosul_uyari("t.md::İLK VE BAĞLAYICI", "t.md")
    assert z.kosul_uyari("t.md::BAŞKA", "t.md") == ""
    assert z.kosul_uyari("", "t.md") == ""
