"""20a girdi-deneme düzeneği: kollar (env · önek · sistem), eşit sayı + karışık sıra, soğuk/sıcak maliyet, sıcakla karar, okuma görevleri, compress yalnız kopyaya, caveman onay --kuru. Ağsız."""
import json
import shutil
from pathlib import Path

import pytest

from video import kur
from video.cli import main

from test_kur import KKos, SJev
from test_uygula import kayit, kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

REPO = Path(__file__).resolve().parents[3]
OKUMA = REPO / "docs" / "denemeler" / "gorevler-okuma"
GIZLI = "sk-test-gizlideger0123456789"


class GKos:
    """claude -p (önekli de) → kol env'indeki KOL'a göre soğuk/sıcak maliyet; aynı (kol, istem) ilk çağrı soğuk. Diğer komutlar `yaz` ile dosyaya yazar."""

    def __init__(self, fiyat, yaz=None):
        self.fiyat, self.yaz, self.cagri, self.env, self.say = fiyat, yaz, [], [], {}

    def __call__(self, args, timeout=None, env=None):
        args = [str(a) for a in args]
        self.cagri.append(args)
        self.env.append(env)
        if "claude" in args and args[args.index("claude") + 1] == "-p":
            kol = (env or {}).get("KOL", "?")
            n = self.say[(kol, args[args.index("claude") + 2])] = self.say.get((kol, args[args.index("claude") + 2]), 0) + 1
            return 0, json.dumps({"result": "yanıt", "is_error": False, "duration_ms": 1000, "total_cost_usd": self.fiyat[kol][min(n, 2) - 1],
                                  "usage": {"input_tokens": 10, "output_tokens": 50, "cache_creation_input_tokens": 0,
                                            "cache_read_input_tokens": 1000 if kol == "b" else 2000}}).encode(), b""
        if self.yaz:
            self.yaz(args)
        return 0, b"", b""

    def claude(self):
        return [(a, e) for a, e in zip(self.cagri, self.env) if "-p" in a]


def deneme(kok, kollar, esik="girdi token −%20", gorev=2, ek=""):
    d = kok / "docs" / "denemeler"
    (d / "gorevler" / "fixture").mkdir(parents=True, exist_ok=True)
    (d / "gorevler" / "fixture" / "x.txt").write_text("veri\n" * 10, encoding="utf-8")
    for i in range(1, gorev + 1):
        (d / "gorevler" / f"{i}-g.md").write_text(f"Görev {i}: dosyada kaç satır var?\noku: fixture/x.txt\naraclar: Read,Grep\n", encoding="utf-8")
    (d / "d.md").write_text("# Deneme: d\n\n## Başarı eşiği\n" + esik + "\n\n## Kollar\n" + "".join(f"- {k}\n" for k in kollar) + "\n" + ek, encoding="utf-8")


IKI = ["a: temel · env KOL=a ANTHROPIC_BASE_URL=http://127.0.0.1:6767", "b: env KOL=b ANTHROPIC_BASE_URL=https://api.anthropic.com"]


def test_kollar_esit_sayida_ve_karisik_sirayla(ortam, kok):
    deneme(kok, IKI)
    k = GKos({"a": (0.3, 0.02), "b": (0.3, 0.02)})
    assert main(["dene", "d"], env=ortam, kos=k, gonder=SJev()) == 0
    sira = [e["KOL"] for _, e in k.claude()]
    assert sira == ["a", "b", "a", "b"] * 2  # görev başına a1 b1 a2 b2
    a, _ = k.claude()[0]
    assert a[a.index("--allowedTools") + 1] == "Read,Grep"
    assert str(kok / "docs" / "denemeler" / "gorevler" / "fixture" / "x.txt") in a[a.index("-p") + 1] and "veri" not in a[a.index("-p") + 1]
    s = json.loads(a[a.index("--settings") + 1])
    assert s == {"env": {"KOL": "a", "ANTHROPIC_BASE_URL": "http://127.0.0.1:6767"}}


def test_tavan_gorev_x_kol_x_2(ortam, kok):
    deneme(kok, IKI)
    k = GKos({"a": (0.3, 0.02), "b": (0.3, 0.02)})
    assert main(["dene", "d", "--tavan", "7"], env=ortam, kos=k, gonder=SJev()) == 1
    assert k.cagri == []


def test_rapor_soguk_sicak_ayri_karar_sicakla(ortam, kok):
    # soğukta b ucuz (−%67), sıcakta b pahalı (+%150): karar sıcakla → RED(token)
    deneme(kok, IKI, esik="çıktı token −%0, maliyet −%10")
    k = GKos({"a": (0.30, 0.02), "b": (0.10, 0.05)})
    assert main(["dene", "d"], env=ortam, kos=k, gonder=SJev()) == 0
    s = (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")
    assert "soğuk $" in s and "sıcak $" in s
    assert "| a |" in s and "0.3000 | 0.0200" in s and "0.1000 | 0.0500" in s
    assert "b: RED(token)" in s


def test_karar_sicak_ucuz_kol_kur(ortam, kok):
    deneme(kok, IKI, esik="çıktı token −%0, maliyet −%10")
    k = GKos({"a": (0.10, 0.05), "b": (0.30, 0.02)})
    assert main(["dene", "d"], env=ortam, kos=k, gonder=SJev()) == 0
    assert "b: AL" in (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")


def test_girdi_esigi_girdi_tokeniyla(ortam, kok):
    deneme(kok, IKI, esik="girdi token −%40")  # a 2010, b 1010 girdi: −%49.8
    k = GKos({"a": (0.1, 0.1), "b": (0.1, 0.1)})
    assert main(["dene", "d"], env=ortam, kos=k, gonder=SJev()) == 0
    assert "b: AL" in (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")
    assert kur.esik("girdi token Headroom'a göre ≥%15 daha az") == {"cikti": None, "girdi": 15, "maliyet": None}


def test_kol_env_gecer_anahtar_degeri_hicbir_ciktida_yok(ortam, kok, capsys):
    deneme(kok, ["a: temel · env KOL=a", "b: env KOL=b ANTHROPIC_API_KEY=${GIZLI_ANAHTAR} · önek sarmal --"])
    k = GKos({"a": (0.1, 0.1), "b": (0.1, 0.1)})
    assert main(["dene", "d"], env={**ortam, "GIZLI_ANAHTAR": GIZLI}, kos=k, gonder=SJev()) == 0
    b = [(a, e) for a, e in k.claude() if e["KOL"] == "b"]
    assert b and all(e["ANTHROPIC_API_KEY"] == GIZLI and a[:2] == ["sarmal", "--"] and a[2:4] == ["claude", "-p"] for a, e in b)
    assert all(GIZLI not in " ".join(a) for a in k.cagri)  # argv (--settings dahil) değeri taşımaz
    d = kok / "docs" / "denemeler"
    metinler = [capsys.readouterr().out, (d / "d-sonuc.md").read_text(encoding="utf-8"), (kok / "docs" / "kurulumlar" / "kayit.jsonl").read_text(encoding="utf-8")]
    metinler += [p.read_text(encoding="utf-8") for p in (d / ".kos").rglob("*.json")]
    assert all(GIZLI not in m for m in metinler)
    assert "ANTHROPIC_API_KEY=${GIZLI_ANAHTAR}" in metinler[1]


def test_kol_duz_anahtar_degeri_bicim_hatasi_yazdirilmaz(ortam, kok, capsys):
    deneme(kok, ["a: env KOL=a", f"b: env KOL=b ANTHROPIC_API_KEY={GIZLI}"])
    k = GKos({"a": (0.1, 0.1), "b": (0.1, 0.1)})
    assert main(["dene", "d"], env=ortam, kos=k, gonder=SJev()) == 1
    assert k.cagri == [] and GIZLI not in capsys.readouterr().out


def test_eski_ab_eslesmeli_esit_sayida(ortam, kok):
    """## Kollar yoksa A düz · B talimat; ikisi de 2 kez, karışık sırayla."""
    d = kok / "docs" / "denemeler"
    (d / "gorevler").mkdir(parents=True)
    (d / "e.md").write_text("# Deneme: e\n\n## Başarı eşiği\nçıktı −%30\n\n## Talimat\ndocs/denemeler/t.md\n", encoding="utf-8")
    (d / "t.md").write_text("KISA YAZ", encoding="utf-8")
    (d / "gorevler" / "1-g.md").write_text("Görev 1: açıkla.\n", encoding="utf-8")
    k = KKos()
    assert main(["dene", "e"], env=ortam, kos=k, gonder=SJev()) == 0
    assert ["--append-system-prompt" in c for c in k.claude()] == [False, True, False, True]


# --- okuma görev seti: beklenen kontroller doğru/yanlış örnekte ---

DOGRU = {"1-basarisiz-test": "test_indirim_sinir_esik\ntests/test_fiyat.py:88\nneden: indirim uygulanmadı, 100 == 90 beklenirken 100 döndü (tutar > ESIK, 500 dahil değil)",
         "2-json-alan": "eposta: ayse.kaya@ornek.test\ntakip: TK771204993\ndurum: iade",
         "3-hatali-diff": "src/sepet_41.py\nsiparis_iptal\nneden: `and` yerine `or` — yetkili olan herkes başkasının siparişini iptal edebilir",
         "4-log-zincir": "kök neden: db.havuz bağlantı havuzu tükendi (istek=7f3a91)\nsiparis.kaydet: SiparisKaydedilemedi\nPOST /api/siparis 500"}
YANLIS = {"1-basarisiz-test": "test_kargo_014_durum_bos\ntests/test_kargo.py:12\nneden: zaman aşımı",
          "2-json-alan": "eposta: musteri1187@ornek.test\ntakip: TK771204993\ndurum: iade",
          "3-hatali-diff": "src/fiyat_40.py\nhesapla_40\nneden: yeniden adlandırma",
          "4-log-zincir": "kök neden: SMTP zaman aşımı (istek=c21d07)\nPOST /api/bildirim 502\nhavuz yok\n500 yok"}


@pytest.mark.parametrize("ad", sorted(DOGRU))
def test_okuma_gorevi_dogru_yanlis(ad):
    g = OKUMA / f"{ad}.md"
    assert kur.desen_denetle(g) is None
    assert kur.basari(g, DOGRU[ad], None)[0] is True
    assert kur.basari(g, YANLIS[ad], None)[0] is False


def test_okuma_fixture_buyuk_ve_istemde_gomulu_degil():
    gorevler = sorted(OKUMA.glob("*.md"))
    assert len(gorevler) == 4
    for g in gorevler:
        oku = next(s[4:].strip() for s in g.read_text(encoding="utf-8").splitlines() if s.startswith("oku:"))
        assert (g.parent / oku).stat().st_size >= 20 * 1024
        ist = kur._istem(g)
        assert str((g.parent / oku).resolve()) in ist and len(ist) < 2000 and "beklenen" not in ist


def test_gorevler_okuma_secenegi(ortam, kok):
    deneme(kok, IKI)
    shutil.copytree(OKUMA, kok / "docs" / "denemeler" / "gorevler-okuma")
    k = GKos({"a": (0.1, 0.1), "b": (0.1, 0.1)})
    assert main(["dene", "d", "--gorevler", "okuma"], env=ortam, kos=k, gonder=SJev()) == 0
    assert len(k.claude()) == 4 * 2 * 2 and "Read,Grep,Glob" in k.claude()[0][0]


# --- compress: yalnız kopya ---

class KJev:
    """score: kural korunmuş 2."""

    def __init__(self):
        self.istek = []

    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        return 200, {}, json.dumps({"answers": {k: {"type": "score", "score": 2, "legend": {}, "confidence": 0.9} for k in g["questions"]}}).encode()


def test_compress_hedefe_yazmaz_yalniz_kopya(ortam, kok, tmp_path, capsys):
    hedef = tmp_path / "baska-repo" / "CLAUDE.md"
    hedef.parent.mkdir()
    once = "# Kurallar\n\n- her değişiklikten önce test yaz ve kırmızıyı gör\n- sırları asla yazdırma\n- commit mesajı Türkçe olsun\n"
    hedef.write_bytes(once.encode("utf-8"))

    def sikistir(args):  # sahte caveman compress: verilen dosyayı kısaltır
        Path(args[-1]).write_text("- test önce, kırmızı gör\n- sır yazdırma\n- commit Türkçe\n", encoding="utf-8")

    d = kok / "docs" / "denemeler"
    d.mkdir(parents=True)
    (d / "c.md").write_text(f"# Deneme: c\n\n## Başarı eşiği\ntoken −%30 ve korunmayan kural 0\n\n## Kaynak\n{hedef.as_posix()}\n\n## Komut\nsikistir {{kopya}}\n",
                            encoding="utf-8")
    k, j = GKos({}, yaz=sikistir), KJev()
    assert main(["dene", "c", "--istek-tavan", "10"], env=ortam, kos=k, gonder=j) == 0
    assert hedef.read_bytes() == once.encode("utf-8")
    assert k.claude() == [] and len(k.cagri) == 1
    kopya = Path(k.cagri[0][-1])
    assert kopya.is_file() and kopya.resolve() != hedef.resolve() and (d / ".kos" / "c") in kopya.parents
    s = (d / "c-sonuc.md").read_text(encoding="utf-8")
    assert "korunmayan kural 0/3" in s and "token" in s and "KUR" in s.split("## Karar")[1]
    assert len(j.istek) == 3


def test_compress_komut_hedefe_dokunursa_red(ortam, kok, tmp_path):
    hedef = tmp_path / "CLAUDE.md"
    hedef.write_text("- kural bir\n", encoding="utf-8")
    d = kok / "docs" / "denemeler"
    d.mkdir(parents=True)
    (d / "c.md").write_text(f"# Deneme: c\n\n## Kaynak\n{hedef.as_posix()}\n\n## Komut\nsikistir {{kopya}}\n", encoding="utf-8")
    k = GKos({}, yaz=lambda a: hedef.write_text("bozuldu", encoding="utf-8"))
    assert main(["dene", "c"], env=ortam, kos=k, gonder=KJev()) == 1


# --- caveman onay --kuru ---

def test_caveman_onay_kuru_hicbir_sey_kosmaz(ortam, kok, capsys):
    b = kok / "docs" / "kurulumlar" / "bekleyen"
    b.mkdir(parents=True)
    shutil.copy2(Path(__file__).parent / "fixture" / "caveman-bekleyen.md", b / "caveman.md")  # 20b: gerçek bekleyen kurulumla tüketildi
    k = KKos()
    assert main(["onay", "caveman", "--kuru"], env=ortam, kos=k) == 0
    out = capsys.readouterr().out
    assert k.cagri == [] and (b / "caveman.md").is_file()
    assert "KURU caveman" in out and "npm.cmd i -g @caveman-ai/cli" in out and "caveman telemetry off" in out and "npm.cmd rm -g @caveman-ai/cli" in out


class MKos(GKos):
    """20b-devam: claude -p yanıtı session_id taşır; KOL b'nin transkriptine `cagri` kadar mcp__caveman__ araç çağrısı yazılır."""

    def __init__(self, ev, cagri, **k):
        super().__init__({"a": (0.3, 0.02), "b": (0.3, 0.02)}, **k)
        self.ev, self.mcp, self.n = ev, cagri, 0

    def __call__(self, args, timeout=None, env=None):
        rc, out, err = super().__call__(args, timeout, env)
        if out and "-p" in [str(a) for a in args]:
            self.n += 1
            j = {**json.loads(out), "session_id": f"s{self.n}"}
            t = self.ev / ".claude" / "projects" / "C--p" / f"s{self.n}.jsonl"
            t.parent.mkdir(parents=True, exist_ok=True)
            adlar = ["Read"] + (["mcp__caveman__retrieve"] * self.mcp if env["KOL"] == "b" else []) + ["mcp__headroom__headroom_retrieve"]
            t.write_text("\n".join(json.dumps({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": a}]}}) for a in adlar) + "\n", encoding="utf-8")
            out = json.dumps(j).encode()
        return rc, out, err


def _mcp_deneme(kok):
    (kok / "cm.json").write_text(json.dumps({"mcpServers": {"caveman": {"command": "caveman-mcp"}}}), encoding="utf-8")
    deneme(kok, ["a: temel · env KOL=a", "b: env KOL=b · mcp cm.json"], esik="girdi token −%20")


def test_mcp_kolu_config_ve_arac_izni_yalniz_o_kolda(ortam, kok, tmp_path):
    _mcp_deneme(kok)
    k = MKos(tmp_path / "ev", 2)
    assert main(["dene", "d"], env={**ortam, "VIDEO_EV": str(tmp_path / "ev")}, kos=k, gonder=SJev()) == 0
    for a, e in k.claude():
        if e["KOL"] == "b":
            assert a[a.index("--mcp-config") + 1] == str(kok / "cm.json")
            assert a[a.index("--allowedTools") + 1] == "Read,Grep,mcp__caveman"
        else:
            assert "--mcp-config" not in a and a[a.index("--allowedTools") + 1] == "Read,Grep"
    s = (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")
    assert "mcp çağrı: a 0 · b 8" in s  # 2 görev × 2 koşu × 2 çağrı; başka sunucunun çağrısı sayılmaz
    assert "devreye girmedi" not in s


def test_mcp_cagrisi_0_ise_karar_yok(ortam, kok, tmp_path):
    _mcp_deneme(kok)
    k = MKos(tmp_path / "ev", 0)
    assert main(["dene", "d"], env={**ortam, "VIDEO_EV": str(tmp_path / "ev")}, kos=k, gonder=SJev()) == 0
    s = (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")
    assert "b: KARAR YOK: sıkıştırma devreye girmedi (mcp çağrısı 0)" in s
    assert kayit(kok)[-1]["karar"].startswith("KARAR YOK")


def test_mcp_cagri_sayisi_onbellekten_de_gelir(ortam, kok, tmp_path):
    _mcp_deneme(kok)
    env = {**ortam, "VIDEO_EV": str(tmp_path / "ev")}
    assert main(["dene", "d"], env=env, kos=MKos(tmp_path / "ev", 1), gonder=SJev()) == 0
    shutil.rmtree(tmp_path / "ev")
    k = MKos(tmp_path / "ev2", 0)
    assert main(["dene", "d"], env=env, kos=k, gonder=SJev()) == 0 and not k.claude()
    assert "mcp çağrı: a 0 · b 4" in (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")
