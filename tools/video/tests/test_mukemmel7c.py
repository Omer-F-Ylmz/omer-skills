"""MÜKEMMEL-7c: U1 köprüsüz link taraması (parti link → V10 → toplu) · U10 parti kuyruk/kayıt yolu."""
import json

from test_m2a import V, Sahte, _ctx, _kurulum, _ns, _pid
from video import parti as pt
from video import tarama as tr


def test_u10_paket_bagli_video_verilen_kuyruga(tmp_path):
    """U10: bağlantılı videolar parti'ye verilen kuyruğa gider, gerçek docs/video-tarama/kuyruk.md'ye değil."""
    kok = _kurulum(tmp_path, [V[0]])
    s = Sahte()
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, s))
    ctx, alt = _ctx(kok, s), []
    ctx["alt"] = lambda argv: alt.append(argv) or 0
    assert pt.parti(_ns("devam", _pid(kok), yeniden_tara=True, paket_yeniden=True), ctx) == 0
    a = next(a for a in alt if a[0] == "paket")
    assert a[a.index("--kuyruk") + 1] == (kok / "kuyruk.md").as_posix()


def test_u10_kayit_yolu_bayrakla(tmp_path):
    """U10: --kayit verilirse rapor kaydı oraya; verilmezse varsayılan tarama dizini kayit.jsonl."""
    kok = _kurulum(tmp_path, [V[0]])
    ozel = tmp_path / "ozel-kayit.jsonl"
    assert pt.parti(_ns("baslat", kok / "kuyruk.md", kayit=str(ozel)), _ctx(kok, Sahte())) == 0
    assert [k["id"] for k in tr.kayit_oku(ozel)] == [V[0]]
    assert not (kok / "docs" / "video-tarama" / "kayit.jsonl").exists()
    kok2 = _kurulum(tmp_path / "b", [V[1]])
    assert pt.parti(_ns("baslat", kok2 / "kuyruk.md"), _ctx(kok2, Sahte())) == 0
    assert [k["id"] for k in tr.kayit_oku(kok2 / "docs" / "video-tarama" / "kayit.jsonl")] == [V[1]]


def test_u1_link_tek_komut_toplu_gercek_kuyruga_dokunmaz(tmp_path):
    """U1: parti link <url> → tek satırlık geçici kuyruk → V10 tarama → toplu otomatik; gerçek kuyruk.md yaratılmaz/değişmez."""
    kok = _kurulum(tmp_path, [V[0]], sure=300)
    (kok / "c" / V[0] / "meta.json").write_text(json.dumps({"duration": 300, "title": "Araç | tanıtım"}), encoding="utf-8")
    gercek = kok / "docs" / "video-tarama" / "kuyruk.md"
    gercek.parent.mkdir(parents=True)
    gercek.write_text("### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n", encoding="utf-8")
    once = gercek.read_bytes()
    ctx, alt = _ctx(kok, Sahte()), []
    ctx["alt"] = lambda argv: alt.append(argv) or 0
    assert pt.parti(_ns("link", f"https://www.youtube.com/watch?v={V[0]}"), ctx) == 0
    assert gercek.read_bytes() == once
    d = json.loads((kok / ".kos" / _pid(kok) / "durum.json").read_text(encoding="utf-8"))
    assert d["kuyruk"] != gercek.as_posix() and d["videolar"][V[0]]["tarama"]["durum"] == "tamam"
    assert [a for a in alt if a[0] == "toplu"] == [["toplu", d["videolar"][V[0]]["tarama"]["cikti"]]]


def test_7d_link_partisi_kapanir_ikinci_link_atlanmaz(tmp_path):
    """7d: link partisi toplu'dan sonra kapanır; aynı videonun ikinci link'i açık-parti engeline takılmaz, mevcut rapor yeniden taranmaz."""
    kok = _kurulum(tmp_path, [V[0]], sure=300)
    (kok / "c" / V[0] / "meta.json").write_text(json.dumps({"duration": 300, "title": "Araç"}), encoding="utf-8")
    ctx, alt = _ctx(kok, Sahte()), []
    ctx["alt"] = lambda argv: alt.append(argv) or 0
    url = f"https://www.youtube.com/watch?v={V[0]}"
    assert pt.parti(_ns("link", url), ctx) == 0
    assert [json.loads(j.read_text(encoding="utf-8"))["durum"] for j in (kok / ".kos").glob("*/durum.json")] == ["kapandi"]
    assert pt.parti(_ns("link", url), ctx) == 0
    toplu = [a for a in alt if a[0] == "toplu"]
    assert len(toplu) == 2 and toplu[0] == toplu[1]
