"""15 öğrenme: durum.md · karar kümesi · kural/olgu · bilgi kartı · çelişki · sponsor · bizde durum. Ağsız; Jev sahte `gonder`."""
import json
import os
from datetime import date, timedelta
from pathlib import Path

import pytest

from jev import skill as sk
from video import ogren as og
from video import uygula as uy
from video.cli import main

from test_uygula import UKos, aday, calis, kayit, kok, kurallar  # noqa: F401 (kok fixture)
from test_video import VID, onbellek, ortam  # noqa: F401 (ortam fixture)


class OJev:
    """choice: TUR_SORU → self.tur; diğerleri `secim` [(yönerge parçası, ölçüt anahtarı | {anahtar: p})], yoksa hiçbiri.
    noul: `noul` [(yönerge parçası, p)], yoksa 0.99."""

    def __init__(self, tur="kural", secim=(), noul=()):
        self.tur, self.secim, self.noul, self.istek = tur, list(secim), list(noul), []

    def __call__(self, url, basliklar, veri):
        g = json.loads(veri)
        self.istek.append(g)
        cv = {}
        for k, q in g["questions"].items():
            ins = q.get("instructions", "")
            if q["type"] == "choice":
                if ins == og.TUR_SORU:
                    pr = {self.tur: 0.95}
                else:
                    hit = next((a for s, a in self.secim if s in ins and (isinstance(a, dict) or a in q["criteria"])), "hiçbiri")
                    pr = hit if isinstance(hit, dict) else {hit: 0.97}
                cv[k] = {"type": "choice", "choice": max(pr, key=pr.get), "probabilities": pr, "confidence": 0.95}
            else:
                cv[k] = {"type": "noul", "noul": next((p for s, p in self.noul if s in ins), 0.99)}
        return 200, {}, json.dumps({"answers": cv}).encode()


def ipucu(kok, ad, **alan):
    return aday(kok, ad, tur="ipucu", repo="yok", lisans="yok", son_commit="yok", **alan)


def kart(kok, slug, iddia, bayat=90, kaynak=f"{VID} 1:00"):
    d = kok / "bilgi"
    d.mkdir(exist_ok=True)
    y = d / f"{slug}.md"
    y.write_text(f"---\niddia: {iddia}\nkaynak: {kaynak}\nguven: orta\ndogrulama: doğrulanamadı\ntarih: {date.today()}\n"
                 f"bayatlama: {date.today() + timedelta(days=bayat)}\netiketler: model\n---\n{iddia}\n", encoding="utf-8")
    return y


# --- K0 durum.md ---

def durum_kur(kok, n=3):
    k = kok / "docs" / "kurulumlar" / "kayit.jsonl"
    k.write_text("".join(json.dumps({"ad": f"aday-{i}", "katman": "RED", "karar": "lisans yok " + "x" * 40, "tarih": "2026-09-01"}) + "\n"
                         for i in range(n)), encoding="utf-8")
    t = kok / "docs" / "video-tarama"
    t.mkdir(parents=True, exist_ok=True)
    (t / "kayit.jsonl").write_text(json.dumps({"id": VID, "tarih": "2026-09-20", "adaylar": ["a", "Eski araç"], "ele": ["Eski araç"]}) + "\n", encoding="utf-8")
    (kok / "docs" / "cikti-notlari.md").write_text("# Çıktı notları\n\n## Maliyet\n- Maliyet ≈ girdi context × tur; çıktı payı küçük.\n- ikinci\n", encoding="utf-8")
    return k


def test_durum_elle_bolumu_yenilemede_korunur(ortam, kok, capsys):
    k = durum_kur(kok)
    assert main(["durum"], env=ortam) == 0
    d = kok / "docs" / "durum.md"
    md = d.read_text(encoding="utf-8")
    assert og.ELLE in md and "RTK" in md and "Maliyet ≈ girdi context × tur" in md and "Eski araç" in md and "aday-2" in md
    assert "token" in capsys.readouterr().out
    d.write_text(md.split(og.ELLE)[0] + og.ELLE + "\n## Öncelikler\n- elle yazılmış öncelik\n", encoding="utf-8")
    k.write_text(k.read_text(encoding="utf-8") + json.dumps({"ad": "yeni-aday", "katman": "T0", "karar": "madde eklendi"}) + "\n", encoding="utf-8")
    ileri = d.stat().st_mtime + 10
    os.utime(k, (ileri, ileri))
    assert main(["durum"], env=ortam) == 0
    md = d.read_text(encoding="utf-8")
    assert "yeni-aday" in md and "- elle yazılmış öncelik" in md and md.count(og.ELLE) == 1


def test_durum_3k_asiminda_eski_kararlar_ozetlenir(ortam, kok, capsys):
    durum_kur(kok, n=400)
    assert main(["durum"], env=ortam) == 0
    md = (kok / "docs" / "durum.md").read_text(encoding="utf-8")
    from jev import cekirdek as c
    assert c.token(md) <= og.TAVAN and "aday-399" in md and "aday-0 " not in md and "eski " in md


# --- K1 eşleme ---

@pytest.mark.parametrize("k, beklenen", [
    ({"etiket": "ÇİFT (kural: omer-kurallar:4)"}, "ZATEN VAR"), ({"isaret": "ÖNCEDEN-GÖRÜLDÜ"}, "ZATEN VAR"),
    ({"isaret": "UYGULA"}, None), ({"isaret": "BEKLE"}, None),
    ({"katman": "T0", "karar": "eklenmez: ÇİFT (kural: omer-kurallar:4)"}, "ZATEN VAR"),
    ({"katman": "T0", "karar": "madde eklendi: 20. x"}, "KUR"), ({"katman": "T1"}, "KUR"), ({"katman": "T2"}, "KUR"),
    ({"katman": "RED"}, "RED"), ({"katman": "T0", "yargi": "ÖĞREN"}, "ÖĞREN")])
def test_eski_isaretler_eslenir(k, beklenen):
    assert og.yargi_oku(k) == beklenen


# --- K3 kural/olgu ---

def test_olgu_turu_t0a_girmez_ogren_ve_kart(ortam, kok, capsys):
    once = kurallar(ortam)
    y = ipucu(kok, "muhakeme", kural="Fable muhakemesini açıklatmak gereksiz", iddia="Fable 5 muhakemesini açıklatmak sonucu iyileştirmez",
              zaman="7:42", guven="orta", dogrulama="doğrulanamadı", etiketler="model,fable")
    jev = OJev(tur="olgu")
    assert calis(ortam, [y], UKos(), jev) == 0
    assert kurallar(ortam) == once
    k = kayit(kok)[-1]
    assert k["yargi"] == "ÖĞREN" and k["katman"] != "T0"
    kartlar = list((kok / "bilgi").glob("*.md"))
    assert len(kartlar) == 1 and og.kart_denetle(kartlar[0].read_text(encoding="utf-8")) == []
    assert "ÖĞRENİLENLER" in capsys.readouterr().out
    assert not any(q.get("instructions") == uy.tr.KURAL_ASAMA1 for g in jev.istek for q in g["questions"].values())


# --- K4 kart ---

def test_dogrulanmamis_yuksek_guven_ortaya_kirpilir_ve_denetim():
    m = og.kart_metni({"iddia": "X", "video": VID, "zaman": "1:00", "guven": "yüksek", "dogrulama": "doğrulanamadı"}, date(2026, 9, 23))
    assert "guven: orta" in m and "bayatlama: 2026-12-22" in m and og.kart_denetle(m) == []
    m2 = og.kart_metni({"iddia": "X", "video": VID, "guven": "yüksek", "dogrulama": "https://docs.example.com/a"}, date(2026, 9, 23))
    assert "guven: yüksek" in m2
    assert any("guven" in h for h in og.kart_denetle(m.replace("guven: orta", "guven: kesin")))
    assert any("8" in h for h in og.kart_denetle(m + "satır\n" * 9))
    assert any("iddia" in h for h in og.kart_denetle(m.replace("iddia: X\n", "")))


def test_cift_kart_birlesir(ortam, kok):
    eski = kart(kok, "fable-muhakeme", "Fable muhakemesi açıklatılmamalı")
    y = ipucu(kok, "muhakeme-2", iddia="Fable'a muhakemeyi yazdırma", video="yeniVIDEO01", zaman="2:00")
    assert calis(ortam, [y], UKos(), OJev(tur="olgu", secim=[("aynı iddia", "bilgi:fable-muhakeme")])) == 0
    assert list((kok / "bilgi").glob("*.md")) == [eski]
    assert "yeniVIDEO01 2:00" in eski.read_text(encoding="utf-8") and VID in eski.read_text(encoding="utf-8")


def test_bayat_kartlar_listelenir(ortam, kok, capsys):
    kart(kok, "eski-kart", "Eski iddia", bayat=-1)
    kart(kok, "taze-kart", "Taze iddia")
    assert main(["bilgi", "--bayat"], env=ortam) == 0
    out = capsys.readouterr().out
    assert "eski-kart" in out and "taze-kart" not in out and "yeniden doğrula" in out
    assert main(["bilgi"], env=ortam) == 0
    assert "taze-kart" in capsys.readouterr().out


# --- K5 çelişki ---

def test_celiski_actte_otomatik_eklenmez(ortam, kok, capsys):
    once = kurallar(ortam)
    y = ipucu(kok, "yavas-git", kural="Commit mesajlarını İngilizce yaz")
    jev = OJev(secim=[("en yakın", "omer-kurallar:4")], noul=[("çelişiyor", 0.95)])
    assert calis(ortam, [y], UKos(), jev) == 0
    assert kurallar(ortam) == once
    assert "ÇELİŞKİ" in kayit(kok)[-1]["karar"] and "ÇELİŞKİLER" in capsys.readouterr().out


# --- K6 sponsor ---

def test_sponsor_aday_dusuk_oncelik(ortam, kok, capsys):
    onbellek(ortam, ["giriş", "bu video X tarafından sponsorlu, indirim kodu", "asıl konu"],
             chapters=[{"start_time": 0, "end_time": 60, "title": "Giriş"}, {"start_time": 60, "end_time": 120, "title": "Sponsor"},
                       {"start_time": 120, "end_time": 300, "title": "Asıl"}])
    s = aday(kok, "sponsorlu-arac", tur="plugin", lisans="yok", zaman="1:30", karar="RED")
    n = aday(kok, "normal-arac", tur="plugin", lisans="yok", zaman="2:30", karar="RED")
    assert calis(ortam, [s, n], UKos(), OJev(noul=[("sponsor", 0.95)])) == 0
    kk = {k["ad"]: k for k in kayit(kok)}
    assert kk["sponsorlu-arac"]["sponsor"] is True and not kk["normal-arac"].get("sponsor")
    assert kk["sponsorlu-arac"]["kanal"] == "Kanal"
    out = capsys.readouterr().out
    assert out.index("normal-arac") < out.index("sponsorlu-arac") and "sponsor" in out


# --- K2 karar yolları + bizde durum ---

def test_dene_deneme_dosyasi_yazilir(ortam, kok):
    y = aday(kok, "caveman", tur="teknik", karar="DENE", hipotez="çıktı tokenı %30 azalır", metrik="çıktı token/tur")
    assert calis(ortam, [y], UKos(), OJev()) == 0
    d = (kok / "docs" / "denemeler" / "caveman.md").read_text(encoding="utf-8")
    assert all(b in d for b in ("Hipotez", "Metrik", "Bütçe", "Geri alma", "Başarı eşiği")) and "%30" in d
    assert kayit(kok)[-1]["yargi"] == "DENE" and not (kok / "docs" / "kurulumlar" / "bekleyen" / "caveman.md").exists()


def test_bizde_act_skill_girer_alti_girmez(ortam, kok, tmp_path):
    ev = Path(ortam["VIDEO_EV"])
    for ad in ("omni-compression", "alakasiz"):
        (ev / ".claude" / "skills" / ad).mkdir(parents=True)
        (ev / ".claude" / "skills" / ad / "SKILL.md").write_text(f"---\nname: {ad}\ndescription: {ad} açıklama\n---\n", encoding="utf-8")
    y = aday(kok, "caveman", tur="teknik")
    jev = OJev(secim=[(sk.ASAMA1[:30], {"omni-compression": 0.6, "alakasiz": 0.3})],
                noul=[("`omni-compression`", 0.99), ("`alakasiz`", 0.3)])
    assert main(["bizde", str(y)], env=ortam, gonder=jev) == 0
    bizde = uy.tr.bolum(y.read_text(encoding="utf-8"), "Bizde durum")
    assert "omni-compression" in bizde and "alakasiz" not in bizde and len(jev.istek) == 2


# --- K8 gerçek kayıt ---

def test_kayit_uyumu_k8():
    kk = {k["ad"]: k for k in uy.tr.kayit_oku(uy.KOK / "docs" / "kurulumlar" / "kayit.jsonl")}
    assert "birleşti → omer-kurallar:13 (Desktop)" in kk["efor-seviyeleri"]["karar"]
    assert og.yargi_oku(kk["muhakemeyi-aciklatmama"]) == "ÖĞREN"
    assert any("vcU85OrwuV0" in y.read_text(encoding="utf-8") for y in (uy.KOK / "bilgi").glob("*.md"))
