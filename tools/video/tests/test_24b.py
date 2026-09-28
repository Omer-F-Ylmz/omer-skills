"""KURULUM-24b hat-düzeltme-2: güvenlik ön taraması on.md'de · kanıt tüm parçalar + lisans normalizasyonu · günlük çıktı ezilmez ·
departman güven eşiği · T0 dört tür. Ağsız; Jev sahte `gonder`, komutlar sahte `kos`."""
import json
from pathlib import Path

from video import departman as dp
from video import tarama as tr
from video import uygula as uy
from video.cli import main

from test_ogren import OJev
from test_uygula import UKos, aday, calis, kayit, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

KOK = Path(__file__).resolve().parents[3]


# K1 güvenlik ön taraması: `video on` klonlar + SkillSpector koşar; araştırıcı klon/tarama yapmaz
def test_on_guvenlik_on_taramasi_ve_onbellek(ortam, tmp_path):
    cagri = []

    def kos(args, timeout=None):
        args = [str(a) for a in args]
        cagri.append(args)
        if args[:2] == ["git", "clone"]:
            Path(args[-1]).mkdir(parents=True)
            (Path(args[-1]) / "SKILL.md").write_text("# x\n", encoding="utf-8")
        elif args[0] == "skillspector":
            Path(args[args.index("--output") + 1]).write_text(json.dumps({"issues": [{"severity": "HIGH"}, {"severity": "LOW"}]}), encoding="utf-8")
            return 1, b"", b""
        return 0, b"", b""
    env = {**ortam, "VIDEO_UYGULA_KOK": str(tmp_path / "k")}
    for _ in range(2):
        assert main(["on", VID, "cm", "--repo", "o/cm"], env=env, kos=kos) == 0
    m = (tmp_path / "k" / ".kos" / VID / "cm" / "on.md").read_text(encoding="utf-8")
    assert "## Güvenlik ön taraması" in m and "HIGH/CRITICAL 1" in m and "kaynak:" in m
    assert sum(a[:2] == ["git", "clone"] for a in cagri) == 1  # ikinci koşu önbellekten
    assert any(a[0] == "skillspector" and "--no-llm" in a for a in cagri)


def test_arastirici_klonlamaz_taramaz():
    m = (KOK / ".claude" / "agents" / "aday-arastirici.md").read_text(encoding="utf-8")
    assert "git clone" not in m and "skillspector scan" not in m and "Güvenlik ön taraması" in m


# K2 kanıt: tüm `anahtar: değer` parçaları; lisans normalleştirilir (claude-mm, Parti B'de elle düzeltildi)
def test_kanit_tum_parcalar_claude_mm():
    o = {"ozellik": "minimax-m3-backend-degisimi", "etiket": "token", "karar": "RED",
         "gerekce": "güvenlik: --bare OAuth bypass + veri 3. taraf (MiniMax) sunucusuna gidiyor, API anahtarı düz metin · "
                    "lisans: yok (aday dosyasındaki bulgu, license-gate kuralı)"}
    assert uy.ozellik_karar(o, {"lisans": "yok"}, "", Path("."), {})[0] == "RED"


def test_lisans_normallestirme():
    assert [uy.lisans_norm(x) for x in ("MIT License", "Apache 2.0", "BSL 1.1", "lisans yok", "", "yok (LICENSE dosyası yok)")] == \
        ["MIT", "Apache-2.0", "BUSL-1.1", "yok", "yok", "yok"]
    o = {"etiket": "token", "karar": "RED", "gerekce": "ölçüm: yok · lisans: GPL 3.0"}
    assert uy.kanit(o, {"lisans": "GPL-3.0"}, "", Path("."), {}) is True  # yazım farkı (GPL 3.0 / GPL-3.0) kanıtı düşürmez
    assert uy.kanit({**o, "gerekce": "lisans: MIT License"}, {"lisans": "MIT"}, "", Path("."), {}) is False  # izinli lisans kanıt değil


# K3 günlük çıktı ezilmez
def test_toplu_ikinci_kosu_ezmez(ortam, tmp_path):
    t = tmp_path / "tarama"
    t.mkdir()
    r = t / f"2026-09-28-{VID}.md"
    r.write_text("# boş rapor\n", encoding="utf-8")
    env = {**ortam, "VIDEO_TARAMA_DIZIN": str(t), "VIDEO_EV": str(tmp_path / "ev")}
    assert main(["toplu", str(r)], env=env) == 0
    ilk = sorted(t.glob("*-toplu*.md"))
    assert len(ilk) == 1
    ilk[0].write_text("ELLE NOT\n", encoding="utf-8")
    assert main(["toplu", str(r)], env=env) == 0
    assert ilk[0].read_text(encoding="utf-8") == "ELLE NOT\n"
    assert {y.name for y in t.glob("*-toplu*.md")} == {ilk[0].name, ilk[0].name.replace("-toplu.md", "-toplu-2.md")}


def test_bos_yol(tmp_path):
    y = tmp_path / "a.md"
    assert tr.bos_yol(y) == y
    y.write_text("1", encoding="utf-8")
    (tmp_path / "a-2.md").write_text("2", encoding="utf-8")
    assert tr.bos_yol(y) == tmp_path / "a-3.md"


# K4 departman güven eşiği
class DepJev:
    def yargila(self, states, sorular):
        return [{"departman": {"probabilities": {"surec-ajan-arac": 0.49, "frontend": 0.3}}}]


def test_dusuk_guven_site_videosunda_frontend(tmp_path):
    assert dp.sinifla(tmp_path, DepJev, "4ce9-yat-sitesi-promptu", "prompt", "yat sitesi kurar", site=True)[:2] == ("frontend", 0.49)
    dep, p, n = dp.sinifla(tmp_path, DepJev, "4ce9-yat-sitesi-promptu", "prompt", "yat sitesi kurar")
    assert (dep, p) == ("surec-ajan-arac", 0.49) and "departman: belirsiz (p=0.49)" in n


def test_site_mi_tarama_raporundan(tmp_path):
    t = tmp_path / "tarama"
    t.mkdir()
    (t / "r.md").write_text("# Yat\n## Künye\nkanal: x\n## Özet\nlanding sayfası, gsap scroll animasyonu\n## Adaylar\n", encoding="utf-8")
    (t / "kayit.jsonl").write_text(json.dumps({"id": VID, "tarih": "2026-09-28", "rapor": "r.md", "adaylar": [], "ele": []}) + "\n", encoding="utf-8")
    assert uy.site_mi({"VIDEO_TARAMA_DIZIN": str(t)}, VID) is True
    assert uy.site_mi({"VIDEO_TARAMA_DIZIN": str(t)}, "baskavideo") is False


# K5 T0 dört tür: yalnız "kural" bekleyen/kural-*.md üretir (Parti A-B örnekleri)
def _t0(ortam, kok, ad, tur, **alan):
    y = aday(kok, ad, tur="ipucu", repo="yok", lisans="yok", son_commit="yok", **alan)
    assert calis(ortam, [y], UKos(), OJev(tur="kural", secim=[("dört tür", tur)])) == 0
    return kayit(kok)[-1]


def test_t0_dort_tur(ortam, kok):
    bk = kok / "docs" / "kurulumlar" / "bekleyen"
    k = _t0(ortam, kok, "god-file-esigi", "kural", kural="Büyüyen tek dosyada parçalama önerilir")
    assert k["katman"] == "T0" and (bk / "kural-god-file-esigi.md").is_file()
    k = _t0(ortam, kok, "3d-perspektif", "prompt", kural="3D perspektif detayını promptta açıkça yaz", zaman="4:10", teknik="CSS perspective")
    assert k["yargi"] == "UYARLA" and not (bk / "kural-3d-perspektif.md").exists()
    assert "3D perspektif detayını promptta açıkça yaz" in (kok / "docs" / "departmanlar" / "frontend-promptlar.md").read_text(encoding="utf-8")
    k = _t0(ortam, kok, "edit-regenerate", "ipucu", kural="Düzeltme yazmak yerine mesajı düzenleyip yeniden üret")
    assert k["yargi"] == "ÖĞREN" and not (bk / "kural-edit-regenerate.md").exists()
    assert any("kullanım" in y.read_text(encoding="utf-8") for y in (kok / "bilgi").glob("*.md"))
    aday(kok, "claude-mm", tur="CLI")
    k = _t0(ortam, kok, "minimax-anahtari", "araca-özel", kural="MiniMax API anahtarını oluştur, bakiye yükle", arac="claude-mm")
    assert k["yargi"] == "ARACA ÖZEL" and not (bk / "kural-minimax-anahtari.md").exists()
    assert "## Araca özel prosedür" in (kok / "docs" / "kurulumlar" / "adaylar" / "claude-mm.md").read_text(encoding="utf-8")
    assert sorted(y.name for y in bk.glob("kural-*.md")) == ["kural-god-file-esigi.md"]
