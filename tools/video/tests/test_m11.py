"""MOTOR-M11: panel Ömer sütunu ön-doldurma (a önceki karar · b ZATEN VAR · c prompt/teknik · d T0) · şeffaflık · dolu hücre ezilmez."""
import json

from test_m2c import PID, _aday, _panel

from video import akil


def _kur(kok, kayit=(), adaylar=None, gelistirme=()):
    (pdir := kok / ".kos" / PID).mkdir(parents=True, exist_ok=True)
    (ky := kok / "docs" / "kurulumlar" / "kayit.jsonl").parent.mkdir(parents=True, exist_ok=True)
    ky.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in kayit), encoding="utf-8")
    d = {"parti": PID, "videolar": {}, "adaylar": adaylar or {}, "gelistirme": [
        {"aday": a, "oneri": "UYARLA", "gelistirme_onerisi": "g", "kanit": "k", "videodaki_kullanim": "v", "bizdeki_durum": "b", "fark": "f"}
        for a in gelistirme]}
    return pdir, d


ONCEKI = [{"ad": "codex-plugin-for-claude-code", "parti": "p1", "karar": "UYARLA (Ömer, panel p1)"},
          {"ad": "codex-plugin-for-claude-code", "parti": "p2", "karar": "ERTELE (Ömer, panel p2)"},
          {"ad": "eski-red", "parti": "p1", "karar": "RED (Ömer, panel p1)"}]


# K1 a–d ilk uyan kural; araştırılmış araç · RED geçmişi · -gelistirme · OLASI TEKRAR boş kalır
def test_k1_kurallar_ve_bos_kalanlar(tmp_path, capsys):
    (e := tmp_path / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    (e / "claude-mem.md").write_text("# claude-mem\nad: claude-mem\ntur: CLI\nrepo: thedotmack/claude-mem\n", encoding="utf-8")
    pdir, d = _kur(tmp_path, ONCEKI + [{"ad": "claude-memx", "parti": "p1", "karar": "AL (Ömer, panel p1)"}], {
        "codex-plugin-for-claude-code": _aday("codex-plugin-for-claude-code"),
        "gh-kurulu": _aday("gh-kurulu", kurulu="gh"),
        "prompt-kalibi": _aday("prompt-kalibi", tur="prompt", arac=False),
        "teknik-x": _aday("teknik-x", tur="teknik", arac=False),
        "ipucu-x": _aday("ipucu-x", tur="ipucu", arac=False),
        "yeni-arac": _aday("yeni-arac"),
        "eski-red": _aday("eski-red"),
        "claude-memx": _aday("claude-memx", repo="thedotmack/claude-mem")}, ["yeni-arac"])
    akil.panel(pdir, d, tmp_path)
    r, t = _panel(tmp_path)
    assert {k: r[k][7] for k in r if k not in ("aday", "---")} == {
        "codex-plugin-for-claude-code": "ERTELE", "gh-kurulu": "ZATEN VAR", "prompt-kalibi": "ÖĞREN", "teknik-x": "ÖĞREN", "ipucu-x": "ÖĞREN",
        "yeni-arac": "", "eski-red": "", "claude-memx": "", "yeni-arac-gelistirme": ""}
    on = t.split("## Ön-doldurulan", 1)[1].split("\n## ", 1)[0]
    for s in ("codex-plugin-for-claude-code · ERTELE · kural a", "gh-kurulu · ZATEN VAR · kural b", "prompt-kalibi · ÖĞREN · kural c",
              "teknik-x · ÖĞREN · kural c", "ipucu-x · ÖĞREN · kural d"):
        assert s in on
    # K2 panel başına özet + akil çıktısı
    assert "karar bekleyen 4 · ön-doldurulan 5" in t and "karar bekleyen 4 · ön-doldurulan 5" in capsys.readouterr().out


# K3 dolu Ömer hücresi ezilmez; ön-doldurulan listesinde görünmez
def test_k3_dolu_hucre_ezilmez(tmp_path):
    pdir, d = _kur(tmp_path, ONCEKI, {"gh-kurulu": _aday("gh-kurulu", kurulu="gh"),
                                      "codex-plugin-for-claude-code": _aday("codex-plugin-for-claude-code")})
    y = akil.panel(pdir, d, tmp_path)
    y.write_text(y.read_text(encoding="utf-8").replace("| ZATEN VAR |\n", "| RED |\n").replace("| ERTELE |\n", "| AL |\n"), encoding="utf-8")
    akil.panel(pdir, d, tmp_path)
    r, t = _panel(tmp_path)
    assert (r["gh-kurulu"][7], r["codex-plugin-for-claude-code"][7]) == ("RED", "AL")
    assert "karar bekleyen 0 · ön-doldurulan 0" in t


# K3 akil --yeniden: geliştirme yeniden üretilip satır kalksa da Ömer'in kararı korunur
def test_k3_yeniden_uretimde_omer_korunur(tmp_path):
    pdir, d = _kur(tmp_path, adaylar={"x-arac": _aday("x-arac")}, gelistirme=["x-arac"])
    y = akil.panel(pdir, d, tmp_path)
    y.write_text("\n".join(s[:s.rstrip().rstrip("|").rstrip().rfind("|")] + "| DENE |" if s.startswith("| x-arac") else s
                           for s in y.read_text(encoding="utf-8").splitlines()), encoding="utf-8")
    d["gelistirme"] = []  # parti.py --yeniden: d.pop("gelistirme") → gelistir öneri üretmedi
    akil.panel(pdir, d, tmp_path)
    r, _ = _panel(tmp_path)
    assert (r["x-arac"][7], r["x-arac-gelistirme"][7]) == ("DENE", "DENE")
