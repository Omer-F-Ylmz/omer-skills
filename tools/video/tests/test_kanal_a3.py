"""KANAL-2a A3: Ömer kuralı — işlenen videonun kanalı kanallar.json'da yoksa 'takip' eklenir; varsa değişmez; envanter kaynaklı eklemez; ağ isteği yok."""
import inspect
import json

from video import akil, cli, kanal

A, N, K, V, Y = "AAAAAAAAAA1", "NNNNNNNNNN1", "KKKKKKKKKK1", "VVVVVVVVVV1", "YYYYYYYYYY1"
KUYRUK = f"| {K} | 12 | x | kaynak: kanal:UCk | bekliyor |\n| {N} | 12 | x | not | bekliyor |\n"


def _kur(tmp_path):
    repo, onb = tmp_path / "repo", tmp_path / "onb"
    (repo / "docs" / "video-tarama").mkdir(parents=True)
    (repo / "docs" / "video-tarama" / "kanallar.json").write_text(json.dumps(
        {"UCa": {"kanal": "A", "channel_id": "UCa", "url": "", "karar": "bir-kez"}}), encoding="utf-8")
    for v, cid in ((A, "UCa"), (N, "UCn"), (K, "UCk")):
        (onb / v).mkdir(parents=True)
        (onb / v / "meta.json").write_text(json.dumps({"channel": f"{cid} ad", "channel_id": cid, "channel_url": f"u/{cid}"}), encoding="utf-8")
    (repo / ".kos" / "kanal").mkdir(parents=True)
    (repo / ".kos" / "kanal" / "video-kanal.json").write_text(json.dumps({V: {"channel": "V", "channel_id": "UCv", "channel_url": "u/UCv"}}), encoding="utf-8")
    return repo, {"kok": onb}  # kos yok: ağ isteği atılırsa KeyError


def test_takip_ekle(tmp_path, capsys):
    repo, ctx = _kur(tmp_path)
    assert sorted(kanal.takip_ekle(repo, [A, N, K, V, Y], ctx, KUYRUK)) == ["UCn", "UCv"]
    j = json.loads((repo / "docs" / "video-tarama" / "kanallar.json").read_text(encoding="utf-8"))
    assert j["UCa"]["karar"] == "bir-kez"  # mevcut değer korunur
    assert j["UCn"] == {"kanal": "UCn ad", "channel_id": "UCn", "url": "u/UCn", "karar": "takip", "kaynak": "otomatik · Ömer kuralı 3 Eki"}
    assert "UCk" not in j  # kanal envanterinden gelen video ekleme yapmaz
    assert j["UCv"]["karar"] == "takip"  # meta'da yok → .kos/kanal/video-kanal.json
    assert Y in capsys.readouterr().out  # iki kaynakta da yok → uyarı


def test_parti_ve_parti_disi_yol_baglar():
    assert "takip_ekle(" in inspect.getsource(akil.kapat)
    assert "takip_ekle(" in inspect.getsource(cli.toplu)
