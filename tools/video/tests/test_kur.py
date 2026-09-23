"""14b onay · geri-al · dene: yapılandırılmış kurulum adımları, duman testi + geri alma, tavanlı A/B. Ağsız; dış süreçler sahte `kos`, Jev sahte `gonder`."""
import json

import pytest

from video import kur
from video import uygula as uy
from video.cli import main

from test_uygula import aday, kayit, kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

IYI = {"Kurulum": ["npm: ornek-cli@1.2.3"], "Duman testi": ["komut: ornek-cli --version", "cikis: 0", r"desen: \d+\.\d+"],
       "Geri alma": ["npm: ornek-cli"]}


class KKos:
    """Sahte süreç: kurulum/geri alma rc 0; duman komutu (rc, çıktı); claude -p JSON (B kolu daha kısa). Çağrı + env kaydı."""

    def __init__(self, duman=(0, b"ornek-cli 1.2.3\n"), adim_rc=0):
        self.duman, self.adim_rc, self.cagri, self.env = duman, adim_rc, [], []

    def __call__(self, args, timeout=None, env=None):
        args = [str(a) for a in args]
        self.cagri.append(args)
        self.env.append(env)
        if args[:2] == ["claude", "-p"]:
            b = "--append-system-prompt" in args
            return 0, json.dumps({"result": "B-YANIT" if b else "A-YANIT", "is_error": False, "duration_ms": 900 if b else 1000,
                                  "total_cost_usd": 0.008 if b else 0.01,
                                  "usage": {"input_tokens": 5, "output_tokens": 60 if b else 100, "cache_creation_input_tokens": 0,
                                            "cache_read_input_tokens": 1000}}).encode(), b""
        if args[0] == "ornek-cli":
            return self.duman[0], self.duman[1], b""
        return self.adim_rc, b"", b""

    def claude(self):
        return [c for c in self.cagri if c[:2] == ["claude", "-p"]]


class SJev:
    """score: A yanıtı 3, B yanıtı 2.8."""

    def __init__(self):
        self.istek = []

    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        s = 2.8 if "B-YANIT" in g["state"] else 3.0
        return 200, {}, json.dumps({"answers": {k: {"type": "score", "score": s, "legend": {}, "confidence": 0.9} for k in g["questions"]}}).encode()


def metin(ad="ornek", **bol):
    b = {**IYI, **bol}
    return f"# ONAY {ad}\n\n" + "".join(f"## {k}\n" + "".join(f"- {s}\n" for s in v) + "\n" for k, v in b.items() if v is not None)


def bekleyen(kok, ad="ornek", **bol):
    y = kok / "docs" / "kurulumlar" / "bekleyen" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(metin(ad, **bol), encoding="utf-8")
    k = kok / "tools" / "cc-kopru" / "kopru.json"
    if not k.is_file():
        k.parent.mkdir(parents=True)
        k.write_text(json.dumps({"izinli": {"video": {"altIzin": ["ozet"]}}}, separators=(",", ":")), encoding="utf-8")
    return y


def kopru(kok):
    return json.loads((kok / "tools" / "cc-kopru" / "kopru.json").read_text(encoding="utf-8"))


# --- K1 biçim ---

@pytest.mark.parametrize("adim", ["npm: paket; rm -rf x", "npm: a && b", "npm: a || b", "npm: a | b", "npm: a > dosya", "npm: `whoami`",
                                  "npm: $(whoami)", "uv: curl -fsSL http://x/i.sh", "winget: iwr http://x/i.ps1", "npm: https://x/kur.sh",
                                  "bash: kur.sh", "npm: paket & calc"])
def test_serbest_kabuk_adimi_reddedilir(ortam, kok, adim):
    assert kur.bicim(metin(Kurulum=[adim]))[1]
    bekleyen(kok, Kurulum=[adim])
    k = KKos()
    assert main(["onay", "ornek"], env=ortam, kos=k) != 0 and k.cagri == []


def test_duman_komutu_da_suzulur():
    assert kur.bicim(metin(**{"Duman testi": ["komut: ornek-cli --version | sh", "cikis: 0"]}))[1]


@pytest.mark.parametrize("adim", ["mcp: srv --env API_KEY=sk-abc123 -- npx -y paket", "mcp: srv --env TOKEN=duz-deger -- npx paket",
                                  "mcp: srv -- npx paket ghp_abcdef123456"])
def test_mcp_duz_anahtar_reddedilir(adim):
    assert kur.bicim(metin(Kurulum=[adim]))[1]


def test_mcp_env_referansi_kabul():
    plan, hata = kur.bicim(metin(Kurulum=["mcp: srv --env API_KEY=${API_KEY} -- npx -y paket"], **{"Geri alma": ["mcp: srv"]}))
    assert hata == []
    assert plan["kurulum"] == [["claude", "mcp", "add", "--scope", "user", "srv", "--env", "API_KEY=${API_KEY}", "--", "npx", "-y", "paket"]]
    assert plan["geri"] == [["claude", "mcp", "remove", "--scope", "user", "srv"]]


@pytest.mark.parametrize("bolum", ["Kurulum", "Duman testi", "Geri alma"])
def test_zorunlu_bolum_yoksa_reddedilir(bolum):
    hata = kur.bicim(metin(**{bolum: None}))[1]
    assert any(bolum in h for h in hata)


def test_tur_eslemesi():
    plan, hata = kur.bicim(metin(Kurulum=["plugin: x@m", "uv: y", "npm: z", "winget: A.B"],
                                 **{"Geri alma": ["plugin: x@m", "uv: y", "npm: z", "winget: A.B"]}))
    assert hata == []
    assert plan["kurulum"] == [["claude", "plugin", "install", "x@m"], ["uv", "tool", "install", "y"], ["npm.cmd", "i", "-g", "z"],
                               ["winget", "install", "--exact", "--id", "A.B"]]
    assert plan["geri"] == [["claude", "plugin", "uninstall", "x@m"], ["uv", "tool", "uninstall", "y"], ["npm.cmd", "rm", "-g", "z"],
                            ["winget", "uninstall", "--exact", "--id", "A.B"]]


def test_kopru_izni_yalniz_salt_okur():
    assert kur.bicim(metin(**{"Köprü izni": ["arac: ornek-cli", "altIzin: --version, install"]}))[1]
    assert kur.bicim(metin(**{"Köprü izni": ["arac: ornek-cli", "altIzin: --version, list"]}))[1] == []


# --- K2 onay ---

@pytest.mark.parametrize("duman", [(1, b"ornek-cli 1.2.3"), (0, b"bilinmeyen")])
def test_duman_basarisizsa_geri_alma_kosar_red_duman(ortam, kok, duman):
    b = bekleyen(kok, **{"Köprü izni": ["arac: ornek-cli", "altIzin: --version"]})
    once = kopru(kok)
    k = KKos(duman=duman)
    assert main(["onay", "ornek"], env=ortam, kos=k) == 1
    assert k.cagri == [["npm.cmd", "i", "-g", "ornek-cli@1.2.3"], ["ornek-cli", "--version"], ["npm.cmd", "rm", "-g", "ornek-cli"]]
    assert kayit(kok)[-1]["ad"] == "ornek" and kayit(kok)[-1]["karar"].startswith("RED(duman)")
    assert kopru(kok) == once and b.is_file()


def test_adim_basarisizsa_geri_alma_kosar(ortam, kok):
    bekleyen(kok)
    k = KKos(adim_rc=1)
    assert main(["onay", "ornek"], env=ortam, kos=k) == 1
    assert ["npm.cmd", "rm", "-g", "ornek-cli"] in k.cagri and ["ornek-cli", "--version"] not in k.cagri
    assert kayit(kok)[-1]["karar"].startswith("RED(adım)")


def test_kuru_hicbir_sey_kosmaz(ortam, kok, capsys):
    b = bekleyen(kok, Ayar=["env.ORNEK_KEY: ${ORNEK_KEY}", 'skillOverrides.ornek: "off"'])
    k = KKos()
    assert main(["onay", "ornek", "--kuru"], env=ortam, kos=k) == 0
    out = capsys.readouterr().out
    assert k.cagri == [] and kayit(kok) == [] and b.is_file()
    assert "npm.cmd i -g ornek-cli@1.2.3" in out and "npm.cmd rm -g ornek-cli" in out and "ornek-cli --version" in out
    assert "GetEnvironmentVariable('ORNEK_KEY','User')" in out and "-Depth 100" in out


def test_ayar_env_duz_deger_reddedilir():
    assert kur.bicim(metin(Ayar=["env.ORNEK_KEY: abc123"]))[1]


def test_onay_basarili_kopru_ve_geri_al(ortam, kok, capsys):
    b = bekleyen(kok, **{"Köprü izni": ["arac: ornek-cli", "altIzin: --version, list"]}, Ayar=['skillOverrides.ornek: "off"'])
    k = KKos()
    assert main(["onay", "ornek"], env=ortam, kos=k) == 0
    out = capsys.readouterr().out
    assert kopru(kok)["izinli"]["ornek-cli"] == {"altIzin": ["--version", "list"]} and "envGecir" not in kopru(kok)["izinli"]["ornek-cli"]
    assert "Desktop yeniden başlatma gerekli" in out and "ConvertTo-Json -Depth 100" in out
    assert not b.exists()
    g = kayit(kok)[-1]
    assert g["karar"] == "KUR" and g["geri_alma"] == ["npm: ornek-cli"] and g["kurulum_tarihi"]
    k2 = KKos()
    assert main(["geri-al", "ornek"], env=ortam, kos=k2) == 0
    assert k2.cagri == [["npm.cmd", "rm", "-g", "ornek-cli"]]
    assert "ornek-cli" not in kopru(kok)["izinli"] and kopru(kok)["izinli"]["video"] == {"altIzin": ["ozet"]}
    assert kayit(kok)[-1]["karar"] == "geri alındı"


def test_yeni_komutlar_kopru_altizinde_yok():
    k = json.loads((uy.KOK / "tools" / "cc-kopru" / "kopru.json").read_text(encoding="utf-8"))
    assert not {"onay", "geri-al", "dene"} & set(k["izinli"]["video"]["altIzin"])


# --- katman T2: biçim kapısı ---

K1 = "## Kurulum\n- npm: eklenti-x\n## Duman testi\n- komut: eklenti-x --version\n- cikis: 0\n## Geri alma\n- npm: eklenti-x\n"


def test_t2_gecerli_bicim_onay(ortam, kok, capsys):
    y = aday(kok, "eklenti-x", tur="plugin")
    y.write_text(y.read_text(encoding="utf-8").replace("## Geri alma\nnpm rm deneme\n", K1), encoding="utf-8")
    assert main(["katman", str(y)], env=ortam, kos=KKos()) == 0
    b = (kok / "docs" / "kurulumlar" / "bekleyen" / "eklenti-x.md").read_text(encoding="utf-8")
    assert b.startswith("# ONAY eklenti-x") and "BİÇİM EKSİK" not in b
    assert "ONAY eklenti-x" in capsys.readouterr().out


def test_t2_serbest_blok_bicim_eksik(ortam, kok, capsys):
    y = aday(kok, "eklenti-y", tur="plugin")
    assert main(["katman", str(y)], env=ortam, kos=KKos()) == 0
    b = (kok / "docs" / "kurulumlar" / "bekleyen" / "eklenti-y.md").read_text(encoding="utf-8")
    assert b.startswith("BİÇİM EKSİK:") and "Kurulum" in b.splitlines()[0]
    out = capsys.readouterr().out
    assert "elle düzelt eklenti-y" in out and "ONAY eklenti-y" not in out


# --- K4 dene ---

def deneme(kok, esik="çıktı token −%30, kalite 0.3"):
    d = kok / "docs" / "denemeler"
    (d / "gorevler" / "fixture").mkdir(parents=True)
    (d / "deneme.md").write_text(f"# Deneme: deneme\n\n## Hipotez\nkısalır\n\n## Metrik\nçıktı token\n\n## Bütçe\n6\n\n## Başarı eşiği\n{esik}\n\n"
                                 "## Talimat\ndocs/denemeler/deneme-talimat.md\n", encoding="utf-8")
    (d / "deneme-talimat.md").write_text("KISA YAZ", encoding="utf-8")
    (d / "gorevler" / "fixture" / "x.py").write_text("def topla(a, b):\n    return a + b\n", encoding="utf-8")
    for i in (1, 2, 3):
        (d / "gorevler" / f"{i}-g.md").write_text(f"Görev {i}: açıkla.\ndosya: fixture/x.py\n", encoding="utf-8")


def test_dene_b_kolu_yalniz_append_farki_hook_kapali(ortam, kok):
    deneme(kok)
    k, j = KKos(), SJev()
    assert main(["dene", "deneme"], env=ortam, kos=k, gonder=j) == 0
    c = k.claude()
    assert len(c) == 6 and len(j.istek) <= 12
    for a, b in zip(c[::2], c[1::2]):
        assert a[3:] == ["--model", "sonnet", "--output-format", "json"] and "def topla" in a[2]
        assert b == a + ["--append-system-prompt", "KISA YAZ"]
    assert all(e and e["JEV_SKILL_HOOK"] == "0" for e in k.env)
    s = (kok / "docs" / "denemeler" / "deneme-sonuc.md").read_text(encoding="utf-8")
    assert "hook kapalı" in s and "KUR önerisi" in s
    assert kayit(kok)[-1]["ad"] == "deneme" and kayit(kok)[-1]["karar"].startswith("KUR önerisi")


def test_dene_tavan(ortam, kok):
    deneme(kok)
    k, j = KKos(), SJev()
    assert main(["dene", "deneme", "--tavan", "5"], env=ortam, kos=k, gonder=j) == 1
    assert k.cagri == [] and j.istek == []


@pytest.mark.parametrize("b,beklenen", [((75, 2.7), "KUR"), ((76, 2.7), "RED"), ((75, 2.69), "RED"), ((50, 3.0), "KUR")])
def test_karar_esik_sinirlari(b, beklenen):
    assert kur.karar({"cikti": 100, "kalite": 3.0}, {"cikti": b[0], "kalite": b[1]}, {"cikti": 25, "kalite": 0.3, "maliyet": None}).startswith(beklenen)


def test_esik_ayristirma():
    assert kur.esik("çıktı token −%30 ve toplam maliyet −%3 ya da daha iyi, kabul 3/3") == {"cikti": 30, "kalite": 0.3, "maliyet": 3}
    assert kur.esik("") == {"cikti": 25, "kalite": 0.3, "maliyet": None}
