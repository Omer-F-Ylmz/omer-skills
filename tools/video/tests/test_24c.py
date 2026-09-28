"""KURULUM-24c hat-düzeltme-3: hat iskeleti · T0 örnekleri · brief Site/UI + prompt anatomisi · prompt/kural ZATEN VAR ·
büyük repo · CRLF yol + toplu ÇİFT. Ağsız; Jev sahte `gonder`, komutlar sahte `kos`."""
import json
from pathlib import Path

from jev import cekirdek as c
from video import uygula as uy
from video.cli import main

from test_ogren import OJev
from test_uygula import UKos, aday, calis, kayit, kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)

KOK = Path(__file__).resolve().parents[3]
FIX = json.loads((Path(__file__).parent / "fixture" / "t0-tur.json").read_text(encoding="utf-8"))


def _kos(kb=1000):
    def kos(args, timeout=None):
        args = [str(a) for a in args]
        kos.cagri.append(args)
        if args[:2] == ["gh", "api"] and ".size" in args:
            return 0, str(kb).encode(), b""
        if args[:2] == ["git", "clone"]:
            Path(args[-1]).mkdir(parents=True)
        return 0, b"", b""
    kos.cagri = []
    return kos


# K1 hat iskeleti: araştırıcı hiç yazmasa da aday.md geçerli, yarım işaretli; ikinci koşu ezmez
def test_k1_hat_iskeleti_arastirici_yazmasa_da_gecerli(ortam, kok, capsys):
    assert main(["on", VID, "cm", "--repo", "o/cm", "--tur", "plugin"], env=ortam, kos=_kos()) == 0
    y = kok / "docs" / "kurulumlar" / "adaylar" / "cm.md"
    m = y.read_text(encoding="utf-8")
    assert "arastirma: yarım" in m and "repo: o/cm" in m and "## Önerilen katman" in m and "on.md" in m
    capsys.readouterr()
    assert main(["rapor-denetle", str(y)], env=ortam) == 0 and "yarım" in capsys.readouterr().out
    y.write_text(m + "not: araştırıcı yazdı\n", encoding="utf-8")
    assert main(["on", VID, "cm", "--repo", "o/cm", "--tur", "plugin"], env=ortam, kos=_kos()) == 0
    assert "not: araştırıcı yazdı" in y.read_text(encoding="utf-8")
    assert calis(ortam, [y], UKos(), OJev()) == 0 and kayit(kok)[-1]["yargi"] == "ÖĞREN"  # yarım: lisans kapısına düşmez


def test_k1_prompt_iskeleti_ve_arastirici_yalniz_edit(ortam, kok, capsys):
    assert main(["on", VID, "pp", "--tur", "prompt"], env=ortam, kos=_kos()) == 0
    y = kok / "docs" / "kurulumlar" / "adaylar" / "pp.md"
    assert "## Prompt anatomisi" in y.read_text(encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    m = (KOK / ".claude" / "agents" / "aday-arastirici.md").read_text(encoding="utf-8")
    assert "tools: Bash, Read, Edit, WebSearch" in m


# K2 T0: tür tanımları + 8 hatalı örnek soruda; araç/servis adı geçen öneri de sorulur (MiniMax → araca-özel)
def test_k2_t0_ornekleri_ve_arac_adi():
    assert len(FIX["t0"]) == 8
    j = OJev(tur="olgu", secim=[("dört tür", "araca-özel")])
    t = c.Tasiyici(env={"TYPESAFE_API_KEY": "sahte"}, en_fazla=2, gonder=j, istek_tavan=2)
    assert uy.t0_tur(t, "minimax-api-anahtari", {"kural": "MiniMax API anahtarı oluştur, bakiye yükle"}) == "araca-özel"
    ins = next(q["instructions"] for q in j.istek[0]["questions"].values() if "dört tür" in q["instructions"])
    assert "Ömer'in eylemi" in ins and all(f"{x['ad']} → {x['tur']}" in ins for x in FIX["t0"])


# K3 brief (uygula raporu): son koşunun videolarından Site/UI teknikleri + prompt anatomisi
def test_k3_brief_site_ui_ve_prompt_anatomisi(ortam, kok, capsys):
    (kok / "docs" / "kurulumlar" / "kayit.jsonl").write_text(json.dumps({"ad": "pp/x", "aday": "pp", "yargi": "ZATEN VAR", "video": VID}) + "\n", encoding="utf-8")
    (kok / "docs" / "departmanlar").mkdir(parents=True)
    (kok / "docs" / "departmanlar" / "frontend.md").write_text(f"# frontend\n## Teknikler\n- sahne geçişi · UYARLA · video {VID} · 0:51 anlatım\n- başka · UYARLA · video xxxxxxxxxxx · 1:00\n", encoding="utf-8")
    aday(kok, "pp", tur="prompt")
    y = kok / "docs" / "kurulumlar" / "adaylar" / "pp.md"
    y.write_text(y.read_text(encoding="utf-8") + "## Prompt anatomisi\n### Kalıplar\n- Stack'i adıyla yaz · 5:04 · teknik: R3F · şablon: teknoloji\n", encoding="utf-8")
    r = kok / "r.md"
    r.write_text("# rapor\n## Koşu 1 — 10:00\n## ÖZELLİK KARARLARI\n- pp/x → ZATEN VAR — şablon\n## DEPARTMAN\n- pp → frontend\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["brief", str(r)], env=ortam) == 0
    out = capsys.readouterr().out
    assert "sahne geçişi" in out.split("## Site/UI teknikleri", 1)[1] and "başka" not in out
    assert "Stack'i adıyla yaz" in out.split("## Prompt anatomisi", 1)[1]


# K4 prompt/kural ZATEN VAR: şablon · kütüphane · omer-kurallar 25-26 · DESIGN.md; "?" zaman → ÖĞREN (eksik kaynak)
def _zaten_kok(kok, tmp_path):
    fc = kok / "plugins" / "frontend-craft" / "skills" / "frontend-craft"
    fc.mkdir(parents=True)
    (fc / "SKILL.md").write_text("# fc\n- DESIGN.md tam olarak 6 başlık: renk · tipografi (font ailesi, boyut px) · boşluk\n", encoding="utf-8")
    with open(tmp_path / "kaynak" / "omer-kurallar.md", "a", encoding="utf-8") as f:
        f.write("\n25. site/UI yapım promptlarında: kütüphaneleri ve dosya yapısını açıkça yaz.\n")


def test_k4_prompt_zaten_var_design_md(ortam, kok, tmp_path):
    _zaten_kok(kok, tmp_path)
    ids = [i for i, _ in uy.zaten_liste(kok, ortam)]
    assert any(i.startswith("DESIGN.md") for i in ids) and "omer-kurallar:25" in ids
    did = next(i for i in ids if i.startswith("DESIGN.md"))
    y = aday(kok, "font-stili", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural=FIX["zaten"][0]["kalip"], zaman="5:04", teknik="tipografi")
    assert calis(ortam, [y], UKos(), OJev(secim=[("dört tür", "prompt"), (uy.ZATEN_SORU[:30], did)])) == 0
    k = kayit(kok)[-1]
    assert k["yargi"] == "ZATEN VAR" and "DESIGN.md" in k["karar"]


def test_k4_kural_zaten_var_ve_eksik_kaynak(ortam, kok, tmp_path):
    _zaten_kok(kok, tmp_path)
    y = aday(kok, "teknik-prompt", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural=FIX["zaten"][1]["kalip"], zaman="5:04", teknik="stack")
    assert calis(ortam, [y], UKos(), OJev(secim=[("dört tür", "prompt"), (uy.ZATEN_SORU[:30], "omer-kurallar:25")])) == 0
    assert kayit(kok)[-1]["yargi"] == "ZATEN VAR" and "omer-kurallar:25" in kayit(kok)[-1]["karar"]
    y = aday(kok, "sis", tur="ipucu", repo="yok", lisans="yok", son_commit="yok", kural="Sahneye sis ekle", zaman="?")
    assert calis(ortam, [y], UKos(), OJev(secim=[("dört tür", "prompt")])) == 0
    k = kayit(kok)[-1]
    assert k["yargi"] == "ÖĞREN" and "eksik kaynak" in k["karar"]
    assert not list((kok / "docs" / "kurulumlar" / "bekleyen").glob("prompt-*.md"))


# K5 büyük repo: gh api boyutu >100 MB → klon/tarama yok; zaman aşımı 300
def test_k5_buyuk_repo_klonlanmaz(ortam, kok):
    kos = _kos(kb=200000)
    assert main(["on", VID, "lh", "--repo", "o/lh"], env=ortam, kos=kos) == 0
    m = (kok / ".kos" / VID / "lh" / "on.md").read_text(encoding="utf-8")
    assert "atlandı (repo 195 MB)" in m and not any(a[:2] == ["git", "clone"] or a[0] == "skillspector" for a in kos.cagri)
    assert uy._kos.__defaults__ == (300,)


# K6 CRLF yol listesi + toplu ÇİFT katmanda devralınır (log-dosyası, Parti C)
def test_k6_crlf_yol_ve_toplu_cift(ortam, kok, tmp_path):
    t = tmp_path / "tarama"
    t.mkdir()
    (t / "2026-09-28-toplu-2.md").write_text(
        "# toplu\n\n| aday | işaret | sözlük eşleşmesi | çift p | izin riski (0-3) | tür | videolar |\n|---|---|---|---|---|---|---|\n"
        f"| Log dosyası üzerinden hata çözme iş akışı | ÇİFT (kural: CLAUDE:15) | yok | - | - | iş akışı | {VID} |\n", encoding="utf-8")
    ortam["VIDEO_TARAMA_DIZIN"] = str(t)
    y = aday(kok, "log-dosyası-üzerinden-hata-çözme-iş-akış", tur="iş akışı", repo="yok", lisans="yok", son_commit="yok", kural="Log dosyasından hata çöz")
    assert calis(ortam, [f"{y}\r"], UKos(), OJev(secim=[("dört tür", "ipucu")])) == 0
    k = kayit(kok)[-1]
    assert k["yargi"] == "ZATEN VAR" and "CLAUDE:15" in k["karar"]
