"""TOKEN-DENEME-2a: K0 takas okuma · video tara --kol biçimi · openrouter kolunda yalnız paket/altyazı (anahtar/yerel yol yok)."""
import base64
import json

from video.cli import main

from test_girdi import GKos, IKI, deneme
from test_kur import SJev
from test_uygula import kok  # noqa: F401 (kok fixture)
from test_video import ortam  # noqa: F401 (ortam fixture)

ANAHTAR = "sk-or-v1-GIZLIANAHTAR0123456789"
KARE = b"\xff\xd8JPEGVERI"


def sonuc(kok):
    return (kok / "docs" / "denemeler" / "d-sonuc.md").read_text(encoding="utf-8")


def test_k0_eski_esik_uyarir_karar_takas_tablosundan(ortam, kok, capsys):
    deneme(kok, IKI, "girdi −%0 · maliyet −%5")  # eski tek eşik: sıcak −%10 bunu geçerdi → AL
    assert main(["dene", "d"], env=ortam, kos=GKos({"a": (0.3, 0.02), "b": (0.3, 0.018)}), gonder=SJev()) == 0
    assert "uyarı: eski '## Başarı eşiği'" in capsys.readouterr().out
    assert "b: RED(token)" in sonuc(kok)  # takas: düşüş 0, tasarruf %10 < %25


def test_k0_karar_olcutu_takas_tablosu_uyarisiz(ortam, kok, capsys):
    deneme(kok, IKI, "x")
    d = kok / "docs" / "denemeler" / "d.md"
    d.write_text(d.read_text(encoding="utf-8").replace("## Başarı eşiği\nx", "## Karar ölçütü\ntakas tablosu (omer-kurallar 21)"), encoding="utf-8")
    assert main(["dene", "d"], env=ortam, kos=GKos({"a": (0.3, 0.02), "b": (0.3, 0.01)}), gonder=SJev()) == 0
    assert "uyarı" not in capsys.readouterr().out
    assert "b: AL" in sonuc(kok)


def paket(ortam, kok, tmp_path, kare=2):
    (vc := tmp_path / "vc" / "abc").mkdir(parents=True)
    kareler = []
    for i in range(kare):
        (p := vc / f"k_{i}.jpg").write_bytes(KARE)
        kareler.append(p)
    (vc / "paket.md").write_text("# Paket: abc\n\nALTYAZI: Claude Code ile ucuz model\n" + "".join(f"kare: {p} · 0:0{i}\n" for i, p in enumerate(kareler))
                                 + f"not: {ANAHTAR}\n", encoding="utf-8")
    (a := kok / ".claude" / "agents").mkdir(parents=True, exist_ok=True)
    (a / "video-tarayici.md").write_text("---\nname: video-tarayici\nmodel: sonnet\n---\nTALIMAT: rapor yaz. Önbellek C:\\Projeler\\.video-cache ve /c/Users/pc/x\n",
                                         encoding="utf-8")
    return {**ortam, "VIDEO_CACHE": str(tmp_path / "vc"), "OPENROUTER_API_KEY": ANAHTAR}


def test_tara_sonnet_haiku_ajan_satiri(ortam, kok, tmp_path, capsys):
    env = paket(ortam, kok, tmp_path)
    assert main(["tara", "abc", "--kol", "sonnet", "--tarih", "2026-09-29"], env=env) == 0
    out = capsys.readouterr().out
    assert out.startswith("ajan: video-tarayici · id: abc · paket: ") and "k_0.jpg" in out and "rapor: docs/video-tarama/2026-09-29-abc.md" in out
    assert main(["tara", "abc", "--kol", "haiku"], env=env) == 0
    out = capsys.readouterr().out
    assert out.startswith("ajan: video-tarayici-haiku · id: abc · ") and "rapor: docs/denemeler/ucuz-tarayici/haiku/abc.md" in out
    assert main(["tara", "abc", "--kol", "opus"], env=env) != 0
    assert main(["tara", "yok", "--kol", "sonnet"], env=env) != 0  # paket yoksa önce video paket


class ORSahte:
    def __init__(self):
        self.cagri = []

    def __call__(self, url, basliklar, govde):
        self.cagri.append((url, basliklar, govde))
        return 200, {}, json.dumps({"choices": [{"message": {"content": "# Rapor: abc\n\n## Adaylar\n"}}],
                                    "usage": {"prompt_tokens": 1200, "completion_tokens": 300, "cost": 0.0021}}).encode()


def test_tara_openrouter_yalniz_paket_gider_anahtar_yol_yok(ortam, kok, tmp_path, capsys):
    env, g = paket(ortam, kok, tmp_path), ORSahte()
    assert main(["tara", "abc", "--kol", "openrouter:x/y:free", "--kare", "1"], env=env, gonder=g) == 0
    (url, _, govde), = g.cagri
    metin = govde.decode()
    assert url == "https://openrouter.ai/api/v1/chat/completions"
    assert "GIZLIANAHTAR" not in metin
    assert "C:\\\\" not in metin and ".video-cache" not in metin and "/c/Users" not in metin and "AppData" not in metin
    assert "ALTYAZI: Claude Code ile ucuz model" in metin and "TALIMAT: rapor yaz" in metin
    istek = json.loads(metin)
    assert istek["model"] == "x/y:free"
    resim = [p for m in istek["messages"] if isinstance(m["content"], list) for p in m["content"] if p.get("type") == "image_url"]
    assert [p["image_url"]["url"] for p in resim] == ["data:image/jpeg;base64," + base64.b64encode(KARE).decode()]  # --kare 1: 2 kareden 1'i
    rapor = kok / "docs" / "denemeler" / "ucuz-tarayici" / "openrouter-x-y-free" / "abc.md"
    assert rapor.read_text(encoding="utf-8").startswith("# Rapor: abc")
    assert ("tara: docs/denemeler/ucuz-tarayici/openrouter-x-y-free/abc.md · kol: openrouter:x/y:free · token: 1200+300 · $0.0021 · istek: 1 · kare: 1 · denetim: "
            in capsys.readouterr().out)


def test_tara_openrouter_kare_ust_siniri_6(ortam, kok, tmp_path):
    env, g = paket(ortam, kok, tmp_path, kare=8), ORSahte()
    assert main(["tara", "abc", "--kol", "openrouter:x/y", "--kare", "9"], env=env, gonder=g) == 0
    assert g.cagri[0][2].decode().count('"type": "image_url"') == 6
