"""TOKEN-4a K1: token_olc --arac-dokum — araç sonucu dökümü (sentetik jsonl; içerik metni yazılmaz)."""
import json
import time

import pytest

from test_token_olc import GIZLI, SIMDI, TS, t, usage, yaz


def zs(sn):
    return time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(SIMDI - 3600 + sn))


def ist(mid, ctx=1000, araclar=(), sn=0, cikti=0):
    """Asistan isteği: ctx = gerçek bağlam (cache okuma); araclar = [(id, ad, input)]."""
    icerik = [{"type": "tool_use", "id": i, "name": a, "input": g} for i, a, g in araclar]
    return {"type": "assistant", "timestamp": zs(sn), "cwd": "C:\\p", "sessionId": "s1", "isSidechain": False,
            "message": {"id": mid, "model": "claude-opus-5-5", "role": "assistant",
                        "content": icerik or [{"type": "text", "text": GIZLI}], "usage": usage(okuma=ctx, cikti=cikti)}}


def son(tid, metin, sn=0, sonuc=None):
    o = {"type": "user", "timestamp": zs(sn), "message": {"role": "user", "content": [
        {"type": "tool_result", "tool_use_id": tid, "content": metin}]}}
    if sonuc is not None:
        o["toolUseResult"] = sonuc
    return o


def okuma(satir):
    return {"type": "text", "file": {"filePath": "x", "content": GIZLI, "numLines": satir, "startLine": 1,
                                     "totalLines": satir}}


def istem(metin, sn=0):
    return {"type": "user", "timestamp": zs(sn), "message": {"role": "user", "content": metin}}


def rtk_ek(tid, komut):
    cikti = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": {"command": komut}}}
    return {"type": "attachment", "timestamp": TS, "attachment": {
        "type": "hook_success", "hookEvent": "PreToolUse", "hookName": "PreToolUse:Bash", "toolUseID": tid,
        "stdout": json.dumps(cikti)}}


def dok(tmp_path, satirlar, **kw):
    yaz(tmp_path / "p" / "s.jsonl", satirlar)
    return t.dokum(tmp_path / "p", gun=14, simdi=SIMDI, **kw)


def test_read_aralik_limitsiz_buyuk_ve_uzanti(tmp_path):
    d = dok(tmp_path, [
        ist("m1", araclar=[("r1", "Read", {"file_path": "C:/p/a.py"})]), son("r1", "x" * 400, sonuc=okuma(500)),
        ist("m2", araclar=[("r2", "Read", {"file_path": "C:/p/b.md", "offset": 10, "limit": 50})]),
        son("r2", "y" * 40, sonuc=okuma(800)), ist("m3")])
    r = d["read"]
    assert (r["adet"], r["aralikli"], r["token"]) == (2, 1, 110)
    assert r["uzanti"][".py"]["token"] == 100
    assert [(x["dosya"], x["satir"], x["adet"]) for x in d["limitsiz_buyuk"]] == [("C:/p/a.py", 500, 1)]


def test_satir_toolUseResult_yoksa_diskten(tmp_path):
    f = tmp_path / "uzun.txt"
    f.write_text("a\n" * 350, encoding="utf-8")
    d = dok(tmp_path, [ist("m1", araclar=[("r1", "Read", {"file_path": str(f)})]), son("r1", "z" * 8), ist("m2")])
    assert [x["satir"] for x in d["limitsiz_buyuk"]] == [350]


def test_rehber_okumasi_muaf_ve_ayri_sayilir(tmp_path):
    d = dok(tmp_path, [
        ist("m1", araclar=[("r1", "Read", {"file_path": "C:\\Users\\pc\\.claude\\skills\\x\\SKILL.md"}),
                           ("r2", "Read", {"file_path": "C:/r/plugins/p/skills/y/references/a.md"})]),
        son("r1", "a" * 40, sonuc=okuma(1000)), son("r2", "b" * 40, sonuc=okuma(900)), ist("m2")])
    assert d["read"]["rehber"] == 2 and d["limitsiz_buyuk"] == []


def test_tekrar_okuma_ve_degismeden(tmp_path):
    a = {"file_path": "C:/p/a.py"}
    d = dok(tmp_path, [
        ist("m1", araclar=[("r1", "Read", a)]), son("r1", "a" * 80, sonuc=okuma(10)),
        ist("m2", araclar=[("r2", "Read", a)]), son("r2", "a" * 80, sonuc=okuma(10)),
        ist("m3", araclar=[("e1", "Edit", {"file_path": "C:\\p\\a.py", "old_string": GIZLI, "new_string": GIZLI})]),
        son("e1", "ok"),
        ist("m4", araclar=[("r3", "Read", a)]), son("r3", "a" * 80, sonuc=okuma(10)),
        ist("m5", araclar=[("r4", "Read", {**a, "offset": 5, "limit": 3})]), son("r4", "a" * 80, sonuc=okuma(10)),
        ist("m6")])
    assert [(x["dosya"], x["adet"], x["degismeden"], x["ayni_aralik"], x["token"]) for x in d["tekrar"]] == [
        ("C:/p/a.py", 3, 2, 1, 60)]


def test_bash_aile_medyan_rtk_pipe_tail(tmp_path):
    d = dok(tmp_path, [
        ist("m1", araclar=[("b1", "Bash", {"command": "git status"}), ("b2", "Bash", {"command": "git status --short"}),
                           ("b3", "Bash", {"command": "cd /c/x && PYTHONIOENCODING=utf-8 python -m pytest -q | tail -5"}),
                           ("b4", "Bash", {"command": "rtk git status"}),
                           ("b5", "Bash", {"command": "rtk proxy cat C:/p/a.txt"})]),
        rtk_ek("b1", "rtk git status"),
        son("b1", "s" * 40), son("b2", "s" * 80), son("b3", "s" * 400), son("b4", "s" * 4), son("b5", "s" * 8),
        ist("m2")])
    b = {x["aile"]: x for x in d["bash"]}
    g = b["git status"]
    assert (g["adet"], g["token"], g["medyan"], g["rtk"]) == (3, 31, 10, 2)
    assert (g["medyan_rtk"], g["medyan_rtksiz"]) == (5.5, 20)
    assert b["cat"]["adet"] == 1 and "proxy" not in b
    p = b["python -m pytest"]
    assert (p["adet"], p["pipe"], p["tail"], p["rtk"]) == (1, 1, 1, 0)
    assert d["bash"][0]["aile"] == "python -m pytest"


def test_retrieve_onceki_arac_ve_aralik(tmp_path):
    d = dok(tmp_path, [
        ist("m1", araclar=[("r1", "Read", {"file_path": "C:/p/buyuk.cs"})], sn=0),
        son("r1", "c" * 4000, sn=1, sonuc=okuma(900)),
        ist("m2", araclar=[("h1", "mcp__headroom__headroom_retrieve", {"hash": "ab" * 12})], sn=30),
        son("h1", "c" * 400, sn=31), ist("m3", sn=40)])
    r = d["retrieve"]
    assert (r["adet"], r["onceki"], r["sn_medyan"], r["tur_medyan"]) == (1, {"Read": 1}, 30, 1)
    assert [(x["dosya"], x["adet"], x["token"]) for x in r["read_dosyalar"]] == [("C:/p/buyuk.cs", 1, 1000)]


def test_tur_paralellik_ve_kucuk_read_dizisi(tmp_path):
    def r(i):
        return ("r%d" % i, "Read", {"file_path": "C:/p/k%d.py" % i, "limit": 20})
    d = dok(tmp_path, [
        ist("m1", araclar=[r(1)]), ist("m1", araclar=[r(2)]), son("r1", "a" * 40), son("r2", "a" * 40),
        ist("m2", araclar=[r(3)]), son("r3", "a" * 40),
        ist("m3", araclar=[r(4)]), son("r4", "a" * 40),
        ist("m4", araclar=[r(5)]), son("r5", "a" * 40), ist("m5")])
    u = d["tur"]
    assert (u["istek"], u["aracli"], u["paralel"]) == (5, 4, 1)
    assert u["arac_sayisi"] == {"0": 1, "1": 3, "2": 1}
    k = u["kucuk_read_dizisi"]
    assert (k["dizi"], k["istek"], k["kazanc"]) == (1, 3, 2)


def test_arsiv_tavan_gercek_orani(tmp_path):
    a = tmp_path / "arsiv"
    a.mkdir()
    (a / "T-1.md").write_bytes("Tur 17/20 · suite 6/6 · tur tavanı (~59 > 40)\n".encode("utf-8") + b"\xb7 bozuk")
    d = dok(tmp_path, [ist("m1")], arsiv=a)
    assert [(x["dosya"], x["gercek"], x["tavan"]) for x in d["arsiv"]] == [("T-1.md", 17, 20), ("T-1.md", 59, 40)]
    assert d["arsiv"][0]["oran"] == 0.85


def test_headroom_katsayisi_ve_duzeltilmis_katki(tmp_path):
    # taban 1000; transcript büyümesi ≈10k token, usage büyümesi 5k → k ≈ 0.5
    d = dok(tmp_path, [
        ist("m1", ctx=1000, araclar=[("r1", "Read", {"file_path": "C:/p/a.py", "limit": 9})]),
        son("r1", "x" * 40000, sonuc=okuma(5000)), ist("m2", ctx=6000), ist("m3", ctx=6000)])
    k = d["katsayi"]["medyan"]
    assert k == pytest.approx(0.5, abs=0.01)
    assert d["read"]["katki"] == pytest.approx(10000 * (1.25 + 0.1))  # m2 yazar, m3 okur
    assert d["read"]["katki_duz"] == pytest.approx(d["read"]["katki"] * k)


def test_headroom_katsayisi_cikti_duser_kirli_adim_dislanir(tmp_path):
    # adım 1: (Δctx 7000 − çıktı 2000) / 10000 sonuç token = 0.5; adım 2'de bağlama giren ek var → dışlanır
    d = dok(tmp_path, [
        ist("m1", ctx=1000, cikti=2000, araclar=[("r1", "Read", {"file_path": "C:/p/a.py", "limit": 9})]),
        son("r1", "x" * 40000),
        ist("m2", ctx=8000, araclar=[("r2", "Read", {"file_path": "C:/p/b.py", "limit": 9})]),
        son("r2", "x" * 16000),
        {"type": "attachment", "timestamp": TS, "attachment": {"type": "hook_additional_context", "content": [GIZLI]}},
        ist("m3", ctx=18000)])
    assert d["katsayi"]["medyan"] == pytest.approx(0.5) and d["katsayi"]["adim"] == 1


def test_uzun_oturum_dalga_bolme(tmp_path):
    d = dok(tmp_path, [
        istem("TOKEN-9a — ilk " + GIZLI), ist("m1", ctx=20_000), ist("m2", ctx=150_000),
        istem("TOKEN-9b — ikinci"), ist("m3", ctx=160_000), ist("m4", ctx=210_000)])
    u = d["uzun"]
    assert (u["oturum"], u["tek_dalga"], u["cok_dalga"]) == (1, 0, 1)
    assert u["bolme_tasarruf"] == pytest.approx(0.1 * 2 * (160_000 - 20_000))


def test_dokum_ciktida_icerik_metni_yok(tmp_path):
    d = dok(tmp_path, [
        istem("TOKEN-9a " + GIZLI),
        ist("m1", araclar=[("b1", "Bash", {"command": "echo " + GIZLI + " | grep x"}),
                           ("r1", "Read", {"file_path": "C:/p/a.py"})]),
        son("b1", GIZLI * 10), son("r1", GIZLI, sonuc=okuma(400)), ist("m2")])
    assert GIZLI not in json.dumps(d, ensure_ascii=False) and GIZLI not in t.tablo_dokum(d)


def test_cli_arac_dokum_json_ve_tablo(tmp_path, capsys):
    yaz(tmp_path / "p" / "s.jsonl", [ist("m1", araclar=[("r1", "Read", {"file_path": "C:/p/a.py"}),
                                                       ("r2", "Read", {"file_path": "C:/p/b.py"})]),
                                     son("r1", "x" * 40, sonuc=okuma(400)), son("r2", "x" * 40, sonuc=okuma(600)),
                                     ist("m2")])
    out = tmp_path / "o.json"
    assert t.main(["olc", "--arac-dokum", "--kok", str(tmp_path / "p"), "--gun", "100000", "--cikti", str(out),
                   "--arsiv", str(tmp_path / "yok")]) == 0
    d = json.loads(out.read_text(encoding="utf-8"))
    assert [(x["kategori"], x["adet"]) for x in d["kaynaklar"]] == [("limitsiz>300", 2)]
    assert "kaynak" in capsys.readouterr().out
