"""VİDEO-KUYRUK-HEDEF: raporlu video partiye alınmaz, kuyrukta `raporlu` olur · YT1 (Sıra 0) önce short, sonra uzun, sonra IG."""
import json
import re
from pathlib import Path

from test_m2a import _ctx, _ns

from video import parti as pt
from video import tarama as tr

Q = ("| id | süre | başlık | not | durum |\r\n|---|---|---|---|---|\r\n"
     "| aaaaaaaaaa1 | 0.8 | a |  | bekliyor |\r\n| bbbbbbbbbb2 | 0.9 | b |  | bekliyor |\r\n"
     "| cccccccccc3 | 0.7 | c |  | işlendi: abc |\r\n")


def _kok(tmp_path):
    (t := tmp_path / "docs" / "video-tarama").mkdir(parents=True)
    (t / "kayit.jsonl").write_text(json.dumps({"id": "aaaaaaaaaa1", "rapor": "x.md"}) + "\n"
                                   + json.dumps({"id": "dddddddddd4", "etiket": "erisilemez"}) + "\n", encoding="utf-8")
    (t / "2026-10-03-bbbbbbbbbb2.md").write_text("# rapor", encoding="utf-8")
    (tmp_path / "kuyruk.md").write_bytes(Q.encode("utf-8"))
    return t


def test_kuyruk_raporlu_yalniz_bekleyen_satir(tmp_path):
    t = _kok(tmp_path)
    metin, ids = tr.kuyruk_raporlu(Q + "| dddddddddd4 | 0.5 | d |  | bekliyor |\r\n", t / "kayit.jsonl", t)
    assert ids == ["aaaaaaaaaa1", "bbbbbbbbbb2"]  # erisilemez kaydı raporsuz → bekliyor kalır
    assert metin == Q.replace("| a |  | bekliyor |", "| a |  | raporlu |").replace("| b |  | bekliyor |", "| b |  | raporlu |") \
        + "| dddddddddd4 | 0.5 | d |  | bekliyor |\r\n"


def test_baslat_raporlu_videoyu_almaz_ve_kuyrugu_gunceller(tmp_path, capsys):
    _kok(tmp_path)
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _ctx(tmp_path, None)) == 1
    assert "kuyrukta bekleyen video yok" in capsys.readouterr().out
    assert not (tmp_path / ".kos").exists()
    assert (tmp_path / "kuyruk.md").read_bytes().decode("utf-8").count("| raporlu |\r\n") == 2


_BASLIK = "| id | süre | başlık | not | durum |\n|---|---|---|---|---|\n"
_S, _U, _I = "| ss1 | 0.5 | s |  | bekliyor |\n", "| uu1 | 5.0 | u |  | bekliyor |\n", "| ig-x1 | 0.5 | i |  | bekliyor |\n"


def test_fixture_kuyruk_yt1_once_short_sonra_uzun_sonra_ig():
    sirali = "### Sıra 1\n" + _BASLIK + "| zz9 | 0.5 | z |  | bekliyor |\n### Sıra 0\n" + _BASLIK + _S + _U + _I
    sira, sifir = 9, []
    for s in sirali.splitlines():
        if x := re.match(r"###\s+Sıra\s+(\d+)", s):
            sira = int(x[1])
        h = tr._hucre(s)
        if sira == 0 and s.startswith("|") and len(h) == 5 and h[4] == "bekliyor":
            sifir.append("i" if h[0].startswith("ig-") else "s" if float(h[1]) < 2 else "u")
    assert "".join(sifir) == "sui"
    tur, parti = tr.kuyruk_parti(sirali)
    assert tur == "short" and parti[0][0] == "ss1"
    tur, parti = tr.kuyruk_parti("### Sıra 0\n" + _BASLIK + _U + _I)  # short yok → uzun
    assert tur == "uzun" and parti[0][0] == "uu1"
