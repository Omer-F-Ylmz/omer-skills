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


def test_ipucu_turu_gecer():
    assert tr.denetle(rapor(tur="ipucu"), 300) == []


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


# --- 12e K1: kayda yalnız denetimden geçen rapor ---

def test_toplu_denetimden_gecmeyen_rapor_kayda_yazilmaz(ortam, dizin, capsys):
    onbellek(ortam, ["a"])
    iyi, kotu = dizin / f"2026-09-23-{VID}.md", dizin / "2026-09-23-abcdefghijk.md"
    iyi.write_text(rapor(), encoding="utf-8")
    kotu.write_text(rapor(tur="araç").replace(VID, "abcdefghijk"), encoding="utf-8")
    ortam["VIDEO_EV"] = str(dizin / "ev")
    assert main(["toplu", str(iyi), str(kotu)], env=ortam, kos=Kos(), gonder=TaramaJev()) == 0
    ids = [json.loads(x)["id"] for x in (dizin / "kayit.jsonl").read_text(encoding="utf-8").splitlines()]
    assert ids == [VID]
    assert "abcdefghijk" in capsys.readouterr().out


# --- 12f: ipucu/iş akışı adaylar kural kaynaklarıyla karşılaştırılır ---

KURAL_METNI = "# Kurallar\n\n- Yeterli bilgi varsa harekete geç, soru sorma.\n- Commit mesajları Türkçe yazılır.\n"


class KuralJev(Jev):
    """Aşama 1 (choice): state'te 'harekete' varsa kural satırı, yoksa hiçbiri · aşama 2 (noul): 0.99 · tarama: çift 0.1 risk 1."""
    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        q = g["questions"]
        if "cift" in q:
            cv = {"cift": {"type": "noul", "noul": 0.1}, "risk": {"type": "score", "score": 1}}
        elif all(k.startswith("d") for k in q):
            cv = {k: {"type": "choice", "choice": "?", "probabilities":
                      ({a: 0.97 for a in v["criteria"] if a.endswith(":3")} if "harekete" in g["state"] else {"hiçbiri": 0.97})}
                  for k, v in q.items()}
        else:
            cv = {k: {"type": "noul", "noul": 0.99} for k in q}
        return 200, {}, json.dumps({"answers": cv}).encode()


def kural_ortam(ortam, dizin, tmp_path):
    k = tmp_path / "kurallar" / "kurallar.md"
    k.parent.mkdir()
    k.write_text(KURAL_METNI, encoding="utf-8")
    ortam["VIDEO_KURALLAR"] = str(k)
    ortam["VIDEO_EV"] = str(dizin / "ev")
    return k


def aday_raporu(dizin, vid, ad, tur):
    y = dizin / f"2026-09-23-{vid}.md"
    y.write_text(rapor(tur=tur).replace("| graphify | graphify 1.00", f"| {ad} | yok").replace(VID, vid), encoding="utf-8")
    return y


def kural_istekleri(jev):
    return [g for g in jev.istek if "cift" not in g["questions"]]


def test_kuralda_olan_ipucu_cift_ve_kural_kisaltmasi(ortam, dizin, tmp_path, capsys):
    kural_ortam(ortam, dizin, tmp_path)
    r = aday_raporu(dizin, VID, "Yeterli bilgide harekete geçirme", "ipucu")
    jev = KuralJev()
    assert main(["toplu", str(r)], env=ortam, kos=Kos(), gonder=jev) == 0
    out = capsys.readouterr().out
    assert "ÇİFT (kural: kurallar:3)" in out
    assert "ÇİFT (kural: kurallar:3)" in next(dizin.glob("*-toplu.md")).read_text(encoding="utf-8")
    assert len(kural_istekleri(jev)) <= 2


def test_kuralda_olmayan_ipucu_onceki_isaret_korunur(ortam, dizin, tmp_path, capsys):
    kural_ortam(ortam, dizin, tmp_path)
    r = aday_raporu(dizin, VID, "Bağlamı (neden) verme", "iş akışı")
    jev = KuralJev()
    assert main(["toplu", str(r)], env=ortam, kos=Kos(), gonder=jev) == 0
    out = capsys.readouterr().out
    assert "[UYGULA]" in out and "kural:" not in out
    assert 1 <= len(kural_istekleri(jev)) <= 2


def test_arac_turu_kural_karsilastirmasina_girmez(ortam, dizin, tmp_path, capsys):
    kural_ortam(ortam, dizin, tmp_path)
    r = aday_raporu(dizin, VID, "harekete geç aracı", "CLI")
    jev = KuralJev()
    assert main(["toplu", str(r)], env=ortam, kos=Kos(), gonder=jev) == 0
    assert kural_istekleri(jev) == [] and "kural:" not in capsys.readouterr().out


def test_kural_onbellegi_mtime_ile_yenilenir(ortam, dizin, tmp_path, capsys):
    import os
    k = kural_ortam(ortam, dizin, tmp_path)
    assert main(["kurallar"], env=ortam) == 0
    assert "2 kural" in capsys.readouterr().out
    mt = k.stat().st_mtime_ns
    k.write_text(KURAL_METNI + "- Üçüncü kural burada.\n", encoding="utf-8")
    os.utime(k, ns=(mt, mt))  # mtime aynı: önbellek kullanılır
    assert main(["kurallar"], env=ortam) == 0
    assert "2 kural" in capsys.readouterr().out
    os.utime(k, ns=(mt + 10**9, mt + 10**9))
    assert main(["kurallar"], env=ortam) == 0
    out = capsys.readouterr().out
    assert "3 kural" in out and "kurallar ·" in out


class SahteTas:
    """Aşama 1: sabit olasılıklar · aşama 2: her soruya aynı noul p."""
    def __init__(self, olas, p):
        self.olas, self.p = olas, p

    def yargila(self, states, q):
        if all(k.startswith("d") for k in q):
            return [{k: {"type": "choice", "probabilities": self.olas} for k in q}]
        return [{k: {"type": "noul", "noul": self.p} for k in q}]


KL = [("omer-kurallar:3", "Yeterli bilgi varsa harekete geç."), ("omer-kurallar:4", "Bitti yalnız kanıtla söylenir.")]
BANT = {"act": 0.85, "flag": 0.60}


def test_asama1_birinci_ve_p_055_cift():
    t = SahteTas({"omer-kurallar:3": 0.7, "omer-kurallar:4": 0.2, "hiçbiri": 0.1}, 0.55)
    assert tr.kural_esle(t, BANT, "İPUCU: harekete geç", KL) == "omer-kurallar:3"


def test_asama1_ikinci_p_09_cift_degil():
    class Ikinci(SahteTas):
        def yargila(self, states, q):
            if all(k.startswith("d") for k in q):
                return super().yargila(states, q)
            return [{k: {"type": "noul", "noul": 0.9 if i else 0.2} for i, k in enumerate(q)}]
    t = Ikinci({"omer-kurallar:3": 0.7, "omer-kurallar:4": 0.2, "hiçbiri": 0.1}, None)
    assert tr.kural_esle(t, BANT, "İPUCU: kanıt", KL) is None
