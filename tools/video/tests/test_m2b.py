"""MOTOR-M2b: K0 artıkları · aday birleştirme · araçlı araştırma (izinli liste) · destek · panel + uygula · kapat gitleaks kapısı."""
import json
from types import SimpleNamespace

from test_m2a import V, Sahte, _ctx, _durum, _form, _kurulum, _ns, _pid

from video import akil, hafif
from video import parti as pt
from video import tarama as tr


def _pk(tmp_path, kareler="yok", sure=100, short=None):
    y = tmp_path / "paket.md"
    y.write_text(f"# {V[0]} · Başlık · Kanal · süre 1:40 · sure_sn {sure}" + (f" · short: {short}" if short else "") + " · dil tr\n"
                 f"## Açıklama bağlantıları\nyok\n## Segmentler\n[0:00] merhaba\n[0:05] araç\n## Kareler\n{kareler}\n", encoding="utf-8")
    return pt.paket_oku(y)


# K0 (a) short tek tanım (<120 sn) + gruplama kuyruk sırasından bağımsız
def test_short_120_ve_sira_bagimsiz_gruplama(tmp_path):
    assert _pk(tmp_path, sure=100)["short"] is True
    assert tr.short_mu(119) and not tr.short_mu(120) and not tr.short_mu(0)
    pk = {v: {"short": s, "metin": "a", "kareler": []} for v, s in (("s1", True), ("u1", False), ("s2", True), ("u2", False), ("s3", True))}
    assert pt.gruplar(pk) == [["s1", "s2", "s3"], ["u1"], ["u2"]]


# K0 (b) kare gönderildiyse Site/UI ve kare kaynaklı bulguda "karede görülen" zorunlu
def test_karede_gorulen_zorunlu(tmp_path):
    f = _form(V[0])
    f["site_ui"] = [{"teknik": "Kart ızgarası", "ne": "Üç sütunlu kartlar", "kanit_zamani": "0:05", "kaynak": "kare"}]
    kareli = _pk(tmp_path, kareler="c/k1.jpg · 0:05")
    h = pt.dogrula({"videolar": [f]}, {V[0]: kareli}, [V[0]])
    assert any("karede_gorulen" in x for x in h.get(V[0], []))
    f["site_ui"][0]["karede_gorulen"] = "   "
    assert any("karede_gorulen" in x for x in pt.dogrula({"videolar": [f]}, {V[0]: kareli}, [V[0]]).get(V[0], []))
    f["site_ui"][0]["karede_gorulen"] = "Üç sütun, mor başlık"
    assert not any("karede_gorulen" in x for x in pt.dogrula({"videolar": [f]}, {V[0]: kareli}, [V[0]]).get(V[0], []))
    del f["site_ui"][0]["karede_gorulen"]  # kare yoksa alan aranmaz
    assert not any("karede_gorulen" in x for x in pt.dogrula({"videolar": [f]}, {V[0]: _pk(tmp_path)}, [V[0]]).get(V[0], []))


class Kopuk(Sahte):
    """kes. çağrıda taşıyıcı istisna atar (KeyboardInterrupt değil: süreç hatası)."""

    def __call__(self, sistem, metin, sema, **k):
        if len(self.cagrilar) + 1 == self.kes:
            self.cagrilar.append((sema["properties"]["videolar"]["items"]["properties"]["id"]["enum"], metin))
            raise RuntimeError("taşıyıcı koptu")
        return super().__call__(sistem, metin, sema, **k)


# K0 (c) çağrı ortası kesinti → durum hata; devamda yalnız o çağrı tekrar
def test_cagri_ortasi_hata_yalniz_o_cagri_tekrar(tmp_path):
    kok = _kurulum(tmp_path, V[:2], sure=300)
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Kopuk(kes=2)))
    d = _durum(kok)
    assert d["videolar"][V[0]]["tarama"]["durum"] == "tamam"
    assert d["videolar"][V[1]]["tarama"]["durum"] == "hata" and "koptu" in d["videolar"][V[1]]["tarama"]["hata"]
    s = Sahte()
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    assert [c[0] for c in s.cagrilar] == [[V[1]]]


def _rapor(v, adaylar, iddia=None):
    f = _form(v)
    f["adaylar"] = [{"ad": a, "tur": t, "ne": "İşi hızlandıran komut satırı aracı", "kanit_zamani": "0:05", "kaynak": "altyazı",
                     "kanit": "Anlatıcı aracı çalıştırıyor.", "repo_url": r} for a, t, r in adaylar]
    if iddia:
        f["iddialar"] = [{"iddia": iddia, "kanit_zamani": "0:05", "kaynak": "altyazı", "tur": "özellik", "aday_adi": adaylar[0][0]}]
    pk = {"id": v, "baslik": f"Başlık {v}", "kanal": "Kanal", "sure": 30, "dil": "tr", "metin": "## Segmentler\n[0:00] a\n", "kareler": []}
    return pt.rapor_md(f, pk, [])


def _parti(kok, pid, raporlar):
    """Tarama bitmiş parti: raporlar docs/video-tarama'da, durum.json tamam."""
    td = kok / "docs" / "video-tarama"
    td.mkdir(parents=True, exist_ok=True)
    (kok / "kuyruk.md").write_text("### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n"
                                   + "".join(f"| {v} | 0.5 | t | - | bekliyor |\n" for v in raporlar), encoding="utf-8")
    vid = {}
    for v, md in raporlar.items():
        (r := td / f"2026-09-29-{v}.md").write_text(md, encoding="utf-8")
        vid[v] = {"paket": {"durum": "tamam", "deneme": 1}, "tarama": {"durum": "tamam", "deneme": 1, "cikti": r.as_posix()}}
    (p := kok / ".kos" / pid).mkdir(parents=True)
    (p / "durum.json").write_text(json.dumps({"parti": pid, "tur": "short", "tarih": "2026-09-29", "model": hafif.MODEL, "butce": 0.5,
                                              "kuyruk": (kok / "kuyruk.md").as_posix(), "tavan": {"cagri": 12, "usd": 1.0},
                                              "durum": "tamam", "videolar": vid}), encoding="utf-8")
    (e := kok / "docs" / "departmanlar" / "envanter.json").parent.mkdir(parents=True, exist_ok=True)
    e.write_text(json.dumps([{"ad": "graphify", "tur": "skill"}]), encoding="utf-8")
    return p


def _arastirma(ad):
    return {"ad": ad, "tur": "CLI", "repo_url": None, "lisans": "MIT", "yildiz": None, "son_commit": "2026-09-01", "ne": "Komut satırı hızlandırıcı",
            "mekanizma": "Sık komutların çıktısını önbellekten verir", "kurulum": ["uv tool install hizli"], "telemetri": "yok", "tasarruf": None,
            "fayda": "Tekrarlanan komutlar hızlanır", "risk": "düşük", "iddia_sinama": [],
            "ozellikler": [{"ozellik": "önbellek", "kaynak_url": "https://example.com/hizli"}],
            "uretilebilir": {"hedef_tur": "yok", "tarif": None}, "skillspector": None}


class Arastirici:
    """Sahte araçlı hafif taşıyıcı: çağrıları (tür, araclar) kaydeder."""

    def __init__(self):
        self.cagrilar = []

    def __call__(self, sistem, metin, sema, **k):
        ozellik = "ozellik" in sema.get("required", [])
        self.cagrilar.append(("ozellik" if ozellik else "arastirma", tuple(k.get("araclar") or ())))
        form = {"ozellik": "paralel indirme", "arastirma": "README paralel indirmeyi anlatıyor", "kaynak_url": "https://example.com/p",
                "sonuc": "doğrulandı"} if ozellik else _arastirma("Hızlı Araç")
        return {"form": form, "usage": {"input_tokens": 5, "output_tokens": 5}, "usd": 0.02, "sure": 0.1, "hata": None}


def _actx(kok, cagir, alt=None):
    return {**_ctx(kok, cagir), "alt": alt or (lambda a: None)}


def _aday_md(kok, slug):
    return (kok / "docs" / "kurulumlar" / "adaylar" / f"{slug}.md").read_text(encoding="utf-8")


# K1 aynı repo iki ad → tek aday; kurulu → araştırma yok
def test_birlestirme_ayni_repo_tek_aday_kurulu_arastirilmaz(tmp_path):
    ad, belirsiz = akil.birlestir([
        (V[0], _rapor(V[0], [("Hızlı Araç", "CLI", "https://github.com/Ornek/hizli")])),
        (V[1], _rapor(V[1], [("hizli-cli", "CLI", "github.com/ornek/hizli.git"), ("graphify", "skill", None)])),
    ], tmp_path / "yok-envanter")
    h = [x for x in ad.values() if x["repo"] == "ornek/hizli"]
    assert len(h) == 1 and sorted(h[0]["videolar"]) == [V[0], V[1]]
    assert len(ad) == 2 and not belirsiz

    kok = tmp_path / "k"
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("graphify", "skill", None)])})
    a = Arastirici()
    pt.parti(_ns("akil", p.name), _actx(kok, a))
    d = json.loads((p / "durum.json").read_text(encoding="utf-8"))
    assert d["adaylar"]["graphify"]["kurulu"] and a.cagrilar == []


# K2 araştırma çağrısı yalnız izinli araçlarla
def test_arastirma_cagrisi_yalniz_izinli_araclar(tmp_path):
    assert akil.ARASTIRMA_ARAC == ("WebSearch", "Bash(video getir:*)", "Bash(video repo:*)")
    yak = []

    def kos(args, girdi, env, timeout):
        yak.append(args)
        return SimpleNamespace(stdout='{"type":"result","structured_output":{},"usage":{},"total_cost_usd":0}\n', stderr="", returncode=0)

    hafif.cagir("s", "m", {"type": "object"}, araclar=akil.ARASTIRMA_ARAC, kos=kos, env={})
    hafif.cagir("s", "m", {"type": "object"}, kos=kos, env={})
    a, b = yak
    assert a[a.index("--tools") + 1] == "WebSearch,Bash"
    i = a.index("--allowedTools")
    assert a[i + 1:i + 4] == list(akil.ARASTIRMA_ARAC) and (i + 4 == len(a) or a[i + 4].startswith("--"))
    assert a.count("--tools") == 1 and b[b.index("--tools") + 1] == "" and "--allowedTools" not in b

    kok = tmp_path / "k"
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    ar = Arastirici()
    pt.parti(_ns("akil", p.name), _actx(kok, ar))
    assert ar.cagrilar == [("arastirma", akil.ARASTIRMA_ARAC)]
    md = _aday_md(kok, "hizli-arac")
    assert "arastirma: tam" in md and "lisans: MIT" in md and "## Destek" in md


# K3 ikinci video yalnız destek ekler (araştırma tekrarlanmaz, idempotent) · özellik araştırması
def test_ikinci_video_yalniz_destek(tmp_path):
    kok = tmp_path
    p1 = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    a1 = Arastirici()
    pt.parti(_ns("akil", p1.name), _actx(kok, a1))
    assert [c[0] for c in a1.cagrilar] == ["arastirma"]
    p2 = kok / ".kos" / "2026-09-30-short"
    p2.mkdir(parents=True)
    r2 = kok / "docs" / "video-tarama" / f"2026-09-30-{V[1]}.md"
    r2.write_text(_rapor(V[1], [("Hızlı Araç", "CLI", None)], iddia="Hızlı Araç paralel indirme yapıyor"), encoding="utf-8")
    d = json.loads((p1 / "durum.json").read_text(encoding="utf-8"))
    d.update(parti=p2.name, videolar={V[1]: {"paket": {"durum": "tamam"}, "tarama": {"durum": "tamam", "cikti": r2.as_posix()}}})
    d.pop("adaylar", None)
    (p2 / "durum.json").write_text(json.dumps(d), encoding="utf-8")
    a2 = Arastirici()
    for _ in range(2):
        pt.parti(_ns("akil", p2.name), _actx(kok, a2))
    assert [c[0] for c in a2.cagrilar] == ["ozellik"]  # araştırma yok; yalnız videoya özgü özellik bir kez
    md = _aday_md(kok, "hizli-arac")
    destek = tr.bolum(md, "Destek")
    assert destek.count(V[0]) == 1 and destek.count(V[1]) == 1
    assert "paralel indirme" in tr.bolum(md, "Özellikler")


# K4 panel üretimi + panel uygula (boş satır dokunulmaz)
def test_panel_ve_uygula(tmp_path):
    kok = tmp_path
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None), ("graphify", "skill", None)])})
    pt.parti(_ns("akil", p.name), _actx(kok, Arastirici()))
    y = kok / "docs" / "kurulumlar" / "parti" / p.name / "panel.md"
    L = y.read_text(encoding="utf-8").splitlines()
    assert any(s.startswith("| aday |") and s.rstrip().endswith("| Ömer |") for s in L)
    for b in ("form_red", "Belirsiz birleşmeler", "ÜRETİLEBİLİR", "Kural önerileri", "OLASI TEKRAR"):
        assert any(s.startswith("## ") and b in s for s in L), b
    satir = [s for s in L if s.startswith(("| hizli-arac |", "| graphify |"))]
    assert len(satir) == 2 and all(s.endswith("| |") for s in satir)
    assert "ZATEN VAR" in next(s for s in satir if s.startswith("| graphify |"))
    y.write_text("\n".join(s[:-3] + "| AL |" if s.startswith("| hizli-arac |") else s for s in L) + "\n", encoding="utf-8")
    yak = []
    rc = akil.panel_uygula(SimpleNamespace(panel=str(y)), {**_actx(kok, None), "karar": lambda ns, ctx: yak.append((ns.ad, ns.secim)) or 0})
    assert rc == 0 and yak == [("hizli-arac", "AL")]


def _kos_sahte(sizinti):
    cagri = []

    def kos(args, timeout=None, env=None):
        cagri.append(args)
        if args[0] == "git" and "status" in args:
            return 0, b" M docs/video-tarama/2026-09-29-aaaaaaaaaa1.md\n", b""
        if "gitleaks" in args[0]:
            return (1, b"leaks found: 1", b"") if sizinti else (0, b"no leaks found", b"")
        return 0, b"abc1234\n", b""
    return kos, cagri


# K5 kapat: sızıntıda commit yok; temizse commit + kuyruk --isle + push
def test_kapat_sizintida_commit_yok(tmp_path):
    kok = tmp_path
    p = _parti(kok, "2026-09-29-short", {V[0]: _rapor(V[0], [("Hızlı Araç", "CLI", None)])})
    kos, cagri = _kos_sahte(True)
    assert pt.parti(_ns("kapat", p.name), {**_actx(kok, None), "kos": kos}) != 0
    assert any("gitleaks" in a[0] for a in cagri) and not any("commit" in a or "push" in a for a in cagri)
    kos, cagri = _kos_sahte(False)
    assert pt.parti(_ns("kapat", p.name), {**_actx(kok, None), "kos": kos}) == 0
    assert sum("commit" in a for a in cagri) >= 1 and any("push" in a for a in cagri)
    assert "abc1234" in (kok / "kuyruk.md").read_text(encoding="utf-8")
