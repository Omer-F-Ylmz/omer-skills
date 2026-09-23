"""12c video-optimize: paket (alt ajan girdisi tek dosya), yalnız-ekran süzgeci, izle (Desktop tek çağrı), dar alt ajan tanımı. Ağsız."""
import json
import re
from pathlib import Path

from video import metin as m
from video.cli import main

from test_tarama import dizin, rapor  # noqa: F401  (dizin fixture)
from test_video import VID, Jev, Kos, ag, ayri, kare_kur, onbellek, ortam, segmentler  # noqa: F401  (ortam fixture)

KOK = Path(__file__).resolve().parents[3]
SEG = re.compile(r"^\[(?:\d+:)?\d+:\d\d\] \S")
KARE = re.compile(r"^\S+\.jpg · (?:\d+:)?\d+:\d\d$")


# --- sadeleştirme ---

def test_sadelestir_dolgu_ve_tekrar():
    assert m.sadelestir("um so so we we install it uh [Music] install it now") == "so we install it now"
    assert m.sadelestir("ııı bu bu araç eee çok iyi") == "bu araç çok iyi"
    assert m.sadelestir("The the tool, a b a b c") == "The tool, a b c"
    assert m.sadelestir("[Müzik]") == ""


def test_sadelestir_tekrarsiz_metne_dokunmaz():
    x = "Claude Code ile graphify kurulur ve e peki denir"
    assert m.sadelestir(x) == x


# --- paket ---

def paket_md(ortam):
    return (Path(ortam["VIDEO_CACHE"]) / VID / "paket.md").read_text(encoding="utf-8")


def bolumler(md):
    out, cur = {}, None
    for s in md.splitlines():
        if s.startswith("## "):
            cur = out.setdefault(s[3:].strip(), [])
        elif cur is not None and s.strip():
            cur.append(s)
    return out


def test_paket_bolumleri_ve_satir_bicimi(ortam, capsys):
    onbellek(ortam, ["um ARAC EKRAN graphify graphify kurulur", "BOS sohbet", "uh ARAC komut komut yazılır"])
    jev = Jev()
    assert main(["paket", VID], env=ortam, kos=Kos(ham=ayri), gonder=jev) == 0
    md = paket_md(ortam)
    assert md.splitlines()[0].startswith(f"# {VID} · Deneme videosu · Kanal · süre 5:00")
    b = bolumler(md)
    assert list(b) == ["Chapter", "Linkler", "Segmentler", "Kareler"]
    assert b["Chapter"] == ["0:00 Giriş", "1:40 Asıl"] and b["Linkler"] == ["https://a.com/x", "https://b.io/y"]
    assert len(b["Segmentler"]) == 3 and all(SEG.match(s) for s in b["Segmentler"])
    assert b["Segmentler"][0] == "[0:00] ARAC EKRAN graphify kurulur"
    assert b["Kareler"] and all(KARE.match(s) and Path(s.split(" · ")[0]).is_file() for s in b["Kareler"])
    out = capsys.readouterr().out
    assert "graphify" not in out and len(out.strip().splitlines()) == 1  # segment metni ana ajana gitmez
    assert out.startswith("paket: ") and "token" in out


def test_paket_kare_tavani(ortam):
    kare_kur(ortam, [0.9] * 8)
    assert main(["paket", VID], env=ortam, kos=Kos(ham=ayri), gonder=Jev()) == 0
    assert len(bolumler(paket_md(ortam))["Kareler"]) == 6
    assert main(["paket", VID, "--kare", "3"], env=ortam, kos=Kos(ham=ayri), gonder=Jev()) == 0
    k = bolumler(paket_md(ortam))["Kareler"]
    assert len(k) == 3 and all("_0.jpg" in s for s in k)  # pencere 0: zaman başına tek tam-t karesi


def test_paket_onbellekte_p_varsa_istek_yok(ortam):
    kare_kur(ortam, [0.9, 0.2, 0.8])
    jev = Jev()
    assert main(["paket", VID], env=ortam, kos=Kos(ham=ayri), gonder=jev) == 0
    assert jev.istek == []


# --- suz yalnız ekran ---

def test_suz_yalniz_ekran_sorusu(ortam):
    d = onbellek(ortam, ["ARAC EKRAN", "BOS", "x"])
    jev = Jev()
    assert main(["suz", VID, "--sorular", "ekran"], env=ortam, gonder=jev) == 0
    assert len(jev.istek) == 3 and all(list(g["questions"]) == ["ekran"] for g in jev.istek)
    seg = segmentler(d)
    assert seg[0]["p_ekran"] == 0.9 and not any("p_arac" in s or "atla" in s for s in seg)
    assert main(["suz", VID, "--sorular", "ekran"], env=ortam, gonder=jev) == 0
    assert len(jev.istek) == 3
    assert main(["suz", VID], env=ortam, gonder=jev) == 0  # p_ekran var, p_arac eksik → yalnız arac sorulur
    assert all(list(g["questions"]) == ["arac"] for g in jev.istek[3:]) and len(jev.istek) == 6


# --- izle ---

def test_izle_act_tek_kare(ortam, capsys):
    onbellek(ortam, [f"segment {i} kelime" for i in range(6)])
    kos, jev = Kos(ham=ayri), Jev(goruntu=0.97)
    assert main(["izle", f"https://youtu.be/{VID}", "hangi araç?"], env=ortam, kos=kos, gonder=jev) == 0
    out = capsys.readouterr().out
    assert len(jev.istek) <= 2 and not any({"arac", "ekran"} & set(g["questions"]) for g in jev.istek)
    kare = [s for s in out.splitlines() if ".jpg" in s]
    assert len(kare) == 1 and "2:30" in kare[0] and len(ag(kos)) == 1  # en iyi segment s2 (2:00-3:00) ortası
    assert "Deneme videosu" in out and "[2:00-3:00]" in out


def test_izle_act_degilse_kare_yok(ortam, capsys):
    onbellek(ortam, [f"segment {i} kelime" for i in range(6)])
    kos, jev = Kos(ham=ayri), Jev(goruntu=0.1)
    assert main(["izle", VID, "hangi araç?"], env=ortam, kos=kos, gonder=jev) == 0
    assert ".jpg" not in capsys.readouterr().out and kos.cagri == [] and len(jev.istek) <= 2


# --- rapor-denetle sözlük sütunu ---

def test_rapor_denetle_soru_isaretli_sozlugu_doldurur(ortam, dizin, tmp_path, capsys):
    ortam["VIDEO_EV"] = str(dizin / "ev")
    onbellek(ortam, ["a"])
    y = tmp_path / f"2026-09-23-{VID}.md"
    y.write_text(rapor().replace("| graphify | graphify 1.00 |", "| Claude Code | ? |"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    assert "| Claude Code | Claude Code (yerlesik, 1.00) |" in y.read_text(encoding="utf-8")
    y.write_text(rapor().replace("| graphify 1.00 |", "| ? |"), encoding="utf-8")
    assert main(["rapor-denetle", str(y)], env=ortam) == 0
    assert "| graphify | yok |" in y.read_text(encoding="utf-8")


# --- dar alt ajan ---

def test_alt_ajan_yalniz_bash_read_write():
    on = (KOK / ".claude" / "agents" / "video-tarayici.md").read_text(encoding="utf-8").split("---")[1]
    alan = dict(x.split(":", 1) for x in on.strip().splitlines())
    assert {t.strip() for t in alan["tools"].split(",")} == {"Bash", "Read", "Write"}
    assert alan["model"].strip() == "sonnet"


# --- 12d: sabit görev metni alt ajan tanımında (paralel ajanlar arası önbellek) ---

def test_alt_ajan_govdesi_sabit_gorev_metnini_tasir():
    govde = (KOK / ".claude" / "agents" / "video-tarayici.md").read_text(encoding="utf-8").split("---", 2)[2]
    for parca in ("## Künye", "## Adaylar", "## Kareden okunanlar", "Tur 1:", "Tur 2:", "rapor: <yol> · aday: <n>", "ipucu"):
        assert parca in govde, parca
    assert "AYNI mesajda" in govde


def test_skill_md_gorev_metnini_kopyalamaz():
    s = (KOK / "skills" / "video-tarama" / "SKILL.md").read_text(encoding="utf-8")
    for parca in ("## Künye", "Tur 1:", "Alt ajan görevi"):
        assert parca not in s, parca
    assert "alt ajan tanımında" in s


# --- toplu Jev tavanı (canlı ölçüm ≤40 istek) ---

def test_toplu_istek_tavani(ortam, dizin):
    from test_tarama import TaramaJev
    r1, r2 = dizin / f"2026-09-23-{VID}.md", dizin / "2026-09-23-abcdefghijk.md"
    r1.write_text(rapor(), encoding="utf-8")
    r2.write_text(rapor().replace("| graphify | graphify 1.00", "| Meta Ads MCP | yok").replace(VID, "abcdefghijk"), encoding="utf-8")
    ortam["VIDEO_EV"] = str(dizin / "ev")
    jev = TaramaJev()
    assert main(["toplu", str(r1), str(r2), "--istek-tavan", "1"], env=ortam, kos=Kos(), gonder=jev) == 1
    assert len(jev.istek) <= 1
