"""12b video-tarama: kayıt, içe alma, sözlük eşleşmesi, tekilleme, rapor denetimi, dalgalar, K6 tam-t karesi. Ağsız."""
import json
from pathlib import Path

import pytest

from video import tarama as tr
from video.cli import main

from test_video import VID, Jev, Kos, ag, ayri, kare_kur, onbellek, ortam  # noqa: F401  (ortam fixture)

ESKI_MADDE = """# Claude ile Kendi Reklam Ekibimi Kurdum
kanal: X · 2026-09-18 · 14 dk
- Meta Ads MCP → ELE · reklam paneli
- claude-in-chrome → ZATEN VAR · tarayıcı eklentisi
"""
ESKI_TABLO = """# Token Hackleri
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| kullanılmayan MCP'yi kapat | YENİ | BİLGİ | not |
| darkroomengineering/lenis | YENİ | ELENDİ | bağımlılık |
## ölçütler
| ölçüt | değer |
|---|---|
| süre | 23 dk |
"""


@pytest.fixture
def dizin(ortam, tmp_path):
    d = tmp_path / "tarama"
    d.mkdir()
    ortam["VIDEO_TARAMA_DIZIN"] = str(d)
    return d


def kayit_yaz(d, *ids):
    (d / "kayit.jsonl").write_text("\n".join(json.dumps({"id": i, "tarih": "2026-09-19", "rapor": f"{i}.md", "adaylar": []}) for i in ids),
                                   encoding="utf-8")


# --- K1 kayıt ---

def test_kayittaki_id_atlanir(ortam, dizin, capsys):
    kayit_yaz(dizin, VID)
    assert main(["kayit", VID, "abcdefghijk"], env=ortam, kos=Kos()) == 0
    out = capsys.readouterr().out
    assert "atlandı: 1" in out and "tara: abcdefghijk" in out and f"tara: {VID}" not in out


def test_yeniden_zorlar(ortam, dizin, capsys):
    kayit_yaz(dizin, VID)
    assert main(["kayit", VID, "--yeniden"], env=ortam, kos=Kos()) == 0
    out = capsys.readouterr().out
    assert f"tara: {VID}" in out and "atlandı: 0" in out


def test_eski_raporlardan_ice_alma(tmp_path):
    (tmp_path / "0ewGD79TMkM.md").write_text(ESKI_MADDE, encoding="utf-8")
    (tmp_path / "1Jb517FRX7I.md").write_text(ESKI_TABLO, encoding="utf-8")
    (tmp_path / "2026-09-23-yp7gg8cG5wc.md").write_text("# yeni\n## Adaylar\n| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |\n"
                                                         "|---|---|---|---|---|---|---|\n| graphify | graphify 1.00 | CLI | yok | graf | 1:00 | anlatıyor |\n",
                                                         encoding="utf-8")
    (tmp_path / "00-envanter.md").write_text("| ad | x |\n|---|---|\n| sahte | y |\n", encoding="utf-8")
    (tmp_path / "99-sentez.md").write_text("x", encoding="utf-8")
    kayit = {k["id"]: k for k in tr.ice_al(tmp_path)}
    assert set(kayit) == {"0ewGD79TMkM", "1Jb517FRX7I", "yp7gg8cG5wc"}
    assert kayit["0ewGD79TMkM"]["adaylar"] == ["Meta Ads MCP", "claude-in-chrome"] and kayit["0ewGD79TMkM"]["ele"] == ["Meta Ads MCP"]
    assert kayit["1Jb517FRX7I"]["adaylar"] == ["kullanılmayan MCP'yi kapat", "darkroomengineering/lenis"]
    assert kayit["1Jb517FRX7I"]["ele"] == ["darkroomengineering/lenis"]
    assert kayit["yp7gg8cG5wc"]["adaylar"] == ["graphify"]


def test_ice_al_cli_kayit_yazar(ortam, dizin, capsys):
    (dizin / "0ewGD79TMkM.md").write_text(ESKI_MADDE, encoding="utf-8")
    assert main(["kayit", "--ice-al"], env=ortam, kos=Kos()) == 0
    satir = [json.loads(x) for x in (dizin / "kayit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [s["id"] for s in satir] == ["0ewGD79TMkM"] and "1 video" in capsys.readouterr().out


# --- K2 sözlük ---

SOZLUK = [("Claude Code", "yerlesik"), ("graphify", "skill"), ("superpowers", "plugin"), ("mcp-git", "mcp"),
          ("darkroomengineering/lenis", "ele"), ("anthropic-skills:jev", "skill")]


@pytest.mark.parametrize("ad,beklenen", [("cloud code", "Claude Code"), ("graphyfy", "graphify"), ("Graphify", "graphify"),
                                         ("lenis", "darkroomengineering/lenis"), ("jev", "anthropic-skills:jev")])
def test_bulanik_eslesme(ad, beklenen):
    e = tr.eslestir(ad, SOZLUK)
    assert e and e[0] == beklenen and 0.8 <= e[2] <= 1.0


@pytest.mark.parametrize("ad", ["graph", "totally new tool", "Remotion"])
def test_esik_alti_eslesmesiz(ad):
    assert tr.eslestir(ad, SOZLUK) is None


# --- K3 tekilleme, dalgalar, işaret ---

def test_ayni_ad_tekillenir():
    t = tr.tekille([{"ad": "Graphify", "video": "a"}, {"ad": "graphify ", "video": "b"}, {"ad": "lenis", "video": "a"}])
    assert [x["ad"] for x in t] == ["Graphify", "lenis"] and t[0]["videolar"] == ["a", "b"]


def test_dalgalar_en_fazla_3():
    ids = [f"v{i}" for i in range(8)]
    d = tr.dalgalar(ids)
    assert max(len(x) for x in d) <= 3 and sum(d, []) == ids


def test_kayit_dalga_ciktisi(ortam, dizin, capsys):
    ids = [f"v{i:010d}" for i in range(7)]
    assert main(["kayit", *ids], env=ortam, kos=Kos()) == 0
    dalga = [x for x in capsys.readouterr().out.splitlines() if x.startswith("dalga")]
    assert len(dalga) == 3 and all(len(x.split(":")[1].split()) <= 3 for x in dalga)


@pytest.mark.parametrize("es,cift,risk,beklenen", [(("graphify", "skill", 0.9), 0.1, 0, "ÇİFT"), (None, 0.7, 0, "ÇİFT"),
                                                   (("lenis", "ele", 0.9), 0.1, 0, "ÖNCEDEN-GÖRÜLDÜ"), (None, 0.1, 2, "BEKLE"),
                                                   (None, None, None, "BEKLE"), (None, 0.1, 1, "UYGULA")])
def test_isaret(es, cift, risk, beklenen):
    assert tr.isaret(es, cift, risk) == beklenen


# --- K4 rapor-denetle ---

def rapor(**deg):
    b = {"kanit": "videoda kuruluşu adım adım gösteriyor", "zaman": "3:20", "tur": "CLI", "alinti": "“tek komutla kurulur”", "bolum": "## Belirsizlikler"}
    b.update(deg)
    return f"""# Deneme
## Künye
başlık · kanal · süre: 5:00 · dil: tr · url: https://youtu.be/{VID}
## Özet
Bir araç anlatılıyor. {b['alinti']}
## Bölümler
- 0:00 Giriş
- 1:40 Asıl
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| graphify | graphify 1.00 | {b['tur']} | https://github.com/x/graphify | kod grafiği | {b['zaman']} | {b['kanit']} |
## Kareden okunanlar
- 3:20 komut satırı
{b['bolum']}
- yok
## Atlanan segment oranı
2/5
"""


def test_rapor_gecerli():
    assert tr.denetle(rapor(), 300) == []


@pytest.mark.parametrize("deg,parca", [({"bolum": "## Notlar"}, "bölüm eksik"), ({"zaman": "7:30"}, "süre dışı"),
                                        ({"alinti": "“" + " ".join(["kelime"] * 16) + "”"}, "alıntı"), ({"kanit": " "}, "boş alan"),
                                        ({"tur": "araç"}, "tür")])
def test_rapor_hatalari_ayri_ayri(deg, parca):
    h = tr.denetle(rapor(**deg), 300)
    assert len(h) == 1 and parca in h[0], h


def test_alinti_15_kelime_gecer():
    assert tr.denetle(rapor(alinti="“" + " ".join(["kelime"] * 15) + "”"), 300) == []


def test_rapor_denetle_cli_sure_onbellekten(ortam, tmp_path, capsys):
    onbellek(ortam, ["a"])  # meta süresi 300 sn: 5:00 sınırda geçer
    y = tmp_path / f"2026-09-23-{VID}.md"
    y.write_text(rapor(zaman="5:00"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    y.write_text(rapor(zaman="5:01"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 1
    assert "süre dışı" in capsys.readouterr().out


# --- K3 ozet çoklu ---

def test_ozet_coklu_link(ortam, capsys):
    kos = Kos()
    assert main(["ozet", VID, "abcdefghijk"], env=ortam, kos=kos) == 0
    out = capsys.readouterr().out
    assert VID in out and "abcdefghijk" in out


# --- K3 toplu ---

class TaramaJev(Jev):
    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        return 200, {}, json.dumps({"answers": {"cift": {"type": "noul", "noul": 0.1}, "risk": {"type": "score", "score": 1}}}).encode()

def test_toplu_tekiller_isaretler_kayda_yazar(ortam, dizin, capsys):
    kayit_yaz(dizin, "0ewGD79TMkM")
    k = json.loads((dizin / "kayit.jsonl").read_text(encoding="utf-8"))
    k["adaylar"] = ["Meta Ads MCP"]
    (dizin / "kayit.jsonl").write_text(json.dumps(k), encoding="utf-8")
    r1, r2 = dizin / f"2026-09-23-{VID}.md", dizin / "2026-09-23-abcdefghijk.md"
    r1.write_text(rapor(), encoding="utf-8")
    r2.write_text(rapor().replace("| graphify | graphify 1.00", "| Meta Ads MCP | yok").replace(VID, "abcdefghijk")
                  + "", encoding="utf-8")
    ortam["VIDEO_EV"] = str(dizin / "ev")  # boş ev: gerçek ~/.claude okunmaz
    jev = TaramaJev()
    assert main(["toplu", str(r1), str(r2)], env=ortam, kos=Kos(), gonder=jev) == 0
    out = capsys.readouterr().out.splitlines()
    assert len(out) <= 25 and len(jev.istek) <= 2
    metin = "\n".join(out)
    assert "ÖNCEDEN-GÖRÜLDÜ" in metin
    ids = [json.loads(x)["id"] for x in (dizin / "kayit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert ids == ["0ewGD79TMkM", VID, "abcdefghijk"]
    assert next(dizin.glob("*-toplu.md")).is_file()


# --- K6 kare: tam-t karesi ilk ---

def test_kare_pencere_ilk_kare_tam_t(ortam, capsys):
    kare_kur(ortam, [0.1] * 5)
    kos = Kos(ham=ayri)
    assert main(["kare", VID, "--t", "12:30", "--pencere", "8"], env=ortam, kos=kos) == 0
    net = ag(kos)
    ilk = net[0]
    assert ilk[ilk.index("-ss") + 1] == "750" and ilk[ilk.index("-frames:v") + 1] == "1" and "-t" not in ilk
    pen = net[1]
    assert (pen[pen.index("-ss") + 1], pen[pen.index("-t") + 1]) == ("742", "16")
    vf = pen[pen.index("-vf") + 1]
    assert "gt(scene,0.3)" in vf and "eq(n,0)" not in vf
    satir = capsys.readouterr().out.splitlines()
    assert "12:30" in satir[0] and "_0.jpg" in satir[0]


# --- alt ajan girdisi: yalnız okunacak segmentler ---

def test_oku_varsayilan_tam_suzgecli_atlar(ortam, capsys):
    """12b ölçümü: süzgeçli geri çağırma %74 < %90 → varsayılan tam okuma, süzgeç --suzgecli ile."""
    d = onbellek(ortam, ["ARAC bir", "BOS iki", "ARAC uc"])
    seg = [json.loads(x) for x in (d / "segmentler.jsonl").read_text(encoding="utf-8").splitlines()]
    seg[1]["atla"] = True
    (d / "segmentler.jsonl").write_text("\n".join(json.dumps(s) for s in seg), encoding="utf-8")
    (d / "linkler.json").write_text('["https://a.com/x"]', encoding="utf-8")
    assert main(["oku", VID, "--suzgecli"], env=ortam) == 0
    out = capsys.readouterr().out
    assert "ARAC bir" in out and "BOS iki" not in out and "Giriş" in out and "https://a.com/x" in out and "atlanan 1/3" in out
    assert main(["oku", VID], env=ortam) == 0
    assert "BOS iki" in capsys.readouterr().out
