from video import tarama as tr

KUYRUK = ("# kuyruk\r\n| id | süre | başlık | not | durum |\r\n|---|---|---|---|---|\r\n"
          "| aaaaaaaaaaa | 1.0 | a | x | bekliyor |\r\n| bbbbbbbbbbb | 9.0 | b | x | işlendi: abc |\r\n")


def test_c4_tekil_atlama_ve_eski_hat_muafiyeti():
    sat = [(v, 1.0, v, "kaynak: Ömer") for v in ("aaaaaaaaaaa", "ccccccccccc", "ddddddddddd", "eeeeeeeeeee", "ccccccccccc")]
    yeni, atla = tr.kuyruk_ekle(KUYRUK, sat, raporlu={"ddddddddddd", "eeeeeeeeeee"}, muaf={"eeeeeeeeeee"}, baslik="## Eklenen: x")
    assert atla == {"aaaaaaaaaaa": "kuyrukta bekliyor", "ddddddddddd": "tarihli rapor", "ccccccccccc": "kuyrukta bekliyor"}
    assert yeni.startswith(KUYRUK) and "\r\n## Eklenen: x\r\n" in yeni
    eklenen = [tr._hucre(s)[0] for s in yeni[len(KUYRUK):].splitlines() if s.startswith("| ") and s.endswith("| bekliyor |")]
    assert eklenen == ["ccccccccccc", "eeeeeeeeeee"]
    assert "\n" not in yeni.replace("\r\n", "")
