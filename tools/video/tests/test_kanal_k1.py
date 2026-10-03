"""KANAL-1 K1: kanal listesi · öneri eşikleri · onay okuma · eski rapor toleransı."""
import json

from video import kanal
from video.cli import main

A1, A2, B1, C1, C2, C3 = "AAAAAAAAAA1", "-AAAAAAAAA2", "BBBBBBBBBB1", "CCCCCCCCCC1", "CCCCCCCCCC2", "CCCCCCCCCC3"


def _jsonl(yol, satirlar):
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(json.dumps(s, ensure_ascii=False) for s in satirlar), encoding="utf-8")


def _kur(tmp_path, monkeypatch):
    """A: 2 işlenen 2 değerli · B (adında |): 1 işlenen 1 değerli · C: 3 işlenen 0 değerli; C3 eski biçim rapor."""
    repo, onb = tmp_path / "repo", tmp_path / "onb"
    monkeypatch.setattr(kanal, "KOK", repo)
    rd = repo / "docs" / "video-tarama"
    rd.mkdir(parents=True)
    for v in (A1, A2, B1, C1, C2):
        (rd / f"2026-09-30-{v}.md").write_text("# x\n## İddialar\n- y\n", encoding="utf-8")
    (rd / f"2026-09-23-{C3}.md").write_text("# eski rapor\n| aday | x |\n", encoding="utf-8")
    (rd / "00-envanter.md").write_text("# envanter\n", encoding="utf-8")
    for v, ad, cid in ((A1, "A Kanal", "UCa"), (A2, "A Kanal", "UCa"), (C1, "C Kanal", None), (C2, "C Kanal", None), (C3, "C Kanal", None)):
        (onb / v).mkdir(parents=True)
        m = {"id": v, "channel": ad}
        if cid:
            m |= {"channel_id": cid, "channel_url": f"https://www.youtube.com/channel/{cid}"}
        (onb / v / "meta.json").write_text(json.dumps(m), encoding="utf-8")
    _jsonl(rd / "kayit.jsonl", [{"id": v, "tarih": "2026-09-30", "rapor": f"2026-09-30-{v}.md", "adaylar": []} for v in (A1, A2)])
    _jsonl(repo / "docs" / "kurulumlar" / "kayit.jsonl", [
        {"ad": "a1", "karar": "UYARLA (Ömer, panel)", "tarih": "2026-09-30", "video": A1},
        {"ad": "a2", "karar": "AL (Ömer, panel)", "tarih": "2026-09-30", "video": A2},
        {"ad": "b1", "karar": "deneme: docs/denemeler/b1.md", "yargi": "DENE", "tarih": "2026-09-24", "video": B1, "kanal": "Nate Herk | AI"},
        {"ad": "c1", "karar": "RED (Ömer, panel)", "tarih": "2026-09-30", "video": C1},
    ])
    return repo, {"VIDEO_CACHE": str(onb)}


def _satir(md, ad):
    return next(x for x in md.splitlines() if x.startswith(f"| {ad} "))


def test_liste_oneri_esikleri_ve_eski_rapor(tmp_path, monkeypatch, capsys):
    repo, env = _kur(tmp_path, monkeypatch)
    assert main(["kanal", "liste"], env=env) == 0
    md = (repo / "docs" / "video-tarama" / "kanallar.md").read_text(encoding="utf-8")
    assert "değerli ≥2 ve değerli/işlenen ≥0.5" in md and "değerli 0 ve işlenen ≥3" in md
    a, b, c = _satir(md, "A Kanal"), _satir(md, "Nate Herk \\| AI"), _satir(md, "C Kanal")
    assert "| UCa |" in a and "| 2 | 2 |" in a and a.endswith("| takip |  |")
    assert "| 1 | 1 |" in b and "| bir-kez |" in b  # n=1 ile takip önerilmez
    assert "| 3 | 0 |" in c and "| atla |" in c
    assert "2026-09-30" in a
    assert "eski biçim" in capsys.readouterr().out


def test_onay_bos_satir_islenmez(tmp_path, monkeypatch):
    repo, env = _kur(tmp_path, monkeypatch)
    assert main(["kanal", "liste"], env=env) == 0
    yol = repo / "docs" / "video-tarama" / "kanallar.md"
    md = yol.read_text(encoding="utf-8")
    md = md.replace(_satir(md, "A Kanal"), _satir(md, "A Kanal")[:-3] + " takip |")
    md = md.replace(_satir(md, "C Kanal"), _satir(md, "C Kanal")[:-3] + " atla |")
    yol.write_text(md, encoding="utf-8")
    assert main(["kanal", "onay", str(yol)], env=env) == 0
    j = json.loads((repo / "docs" / "video-tarama" / "kanallar.json").read_text(encoding="utf-8"))
    assert {k: v["karar"] for k, v in j.items()} == {"UCa": "takip", "C Kanal": "atla"}
    assert j["UCa"]["channel_id"] == "UCa" and j["C Kanal"]["channel_id"] == ""
