"""DERİNLİK-MASTER C2: kare seçimi sabit aralık değil — sahne değişimi (ffmpeg scene) + metin yoğunluğu + altyazı işaret anları; dHash ile aynı ekran bir kez."""
import json
import random
from pathlib import Path

from video import cli
from video import metin as m
from video.cli import main
from test_video import VID, Kos, jpeg, onbellek, ortam  # noqa: F401 (ortam fixture)

SAHNE = (b"frame:0    pts:100000  pts_time:100\nlavfi.scene_score=0.900000\n"
         b"frame:1    pts:300000  pts_time:300\nlavfi.scene_score=0.500000\n"
         b"frame:2    pts:500000  pts_time:500.5\nlavfi.scene_score=0.400000\n")
DOLGU = {300: 900, 500: 800, 150: 100, 450: 50}  # bayt/piksel: metin yoğunluğu vekili
AYNI = {"k00500": "k00300"}  # 8:20 ekranı 5:00 ile aynı


class SahneKos(Kos):
    def __init__(self, sahne=SAHNE, rc=0, **k):
        super().__init__(ham=lambda yol: random.Random(AYNI.get(Path(yol).name[:6], Path(yol).name[:6])).randbytes(72), **k)
        self.sahne, self.rc = sahne, rc

    def __call__(self, args, timeout=None):
        if args[0] == "ffmpeg" and "metadata=print" in args[args.index("-vf") + 1]:
            self.cagri.append(list(args))
            return self.rc, self.sahne if self.rc == 0 else b"", f"[https @ 0x1] {self.url}: 403 Forbidden".encode()
        if args[0] == "powershell":  # C3: yoğunluk artık OCR karakter sayısı; kod satırı → kare modele gider (sıra testi değişmez)
            self.cagri.append(list(args))
            n = lambda a: DOLGU.get(int(Path(a).name[1:6]), 0)  # noqa: E731
            return 0, json.dumps({Path(a).name: {"tr": [["x=1;" * (n(a) // 4), 0, 0, 9, 9]] if n(a) else [], "en": []}
                                  for a in args[args.index("-File") + 2:]}).encode(), b""
        r = super().__call__(args, timeout)
        if args[0] == "ffmpeg" and str(args[-1]).endswith(".jpg"):
            yol = Path(args[-1])
            yol.write_bytes(jpeg()[:-2] + b"\0" * DOLGU.get(int(yol.name[1:6]), 0) + b"\xff\xd9")
        return r


def tara(kos):
    return [a for a in kos.cagri if a[0] == "ffmpeg" and "metadata=print" in a[a.index("-vf") + 1]]


def kareler(ortam):
    md = (Path(ortam["VIDEO_CACHE"]) / VID / "paket.md").read_text(encoding="utf-8")
    return [s.split(" · ")[1] for s in md.split("## Kareler\n")[1].splitlines() if ".jpg" in s]


def test_dhash_ayni_ekran_yakin_farkli_uzak():
    taban = bytes(random.Random(1).randbytes(72))
    gurultu = bytes(min(255, b + 1) if i % 17 == 0 else b for i, b in enumerate(taban))
    fark = lambda a, b: bin(m.dhash(a) ^ m.dhash(b)).count("1")
    assert m.dhash(bytes(72)) == 0 and fark(taban, gurultu) <= 5
    assert fark(taban, bytes(random.Random(2).randbytes(72))) > 5
    assert m.dhash(bytes(range(9)) * 8) == 0 and m.dhash(bytes(range(9, 0, -1)) * 8) == 2 ** 64 - 1  # 9×8: satır başına 8 bit


def test_sahne_ve_yogunluk_sabit_araligi_gecer_tekrar_ekran_secilmez(ortam):
    onbellek(ortam, [], duration=600)
    kos = SahneKos()
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    (a,) = tara(kos)
    assert a.index("-skip_frame") < a.index("-i") and a[a.index("-skip_frame") + 1] == "nokey"  # yalnız anahtar kareler çözülür
    assert "gt(scene," in a[a.index("-vf") + 1] and not str(a[-1]).endswith((".mp4", ".jpg"))  # video yazılmaz
    assert kareler(ortam) == ["2:30", "5:00"]  # 5:00 en yoğun · 8:20 aynı ekran → atlanır · 2:30 sıradaki · 7:30/1:40 seyrek
    d = Path(ortam["VIDEO_CACHE"]) / VID
    assert json.loads((d / "sahne.json").read_text(encoding="utf-8"))["sahneler"][0] == [100.0, 0.9]
    ikinci = SahneKos()
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=ikinci, uyku=lambda s: None) == 0
    assert not tara(ikinci)  # sahne.json önbellekten


def test_altyazi_isaret_anlari_once_gelir(ortam, monkeypatch):
    onbellek(ortam, ["sohbet", "şu repoya bak github", "ayarlar ekranında config", "devam", "son"], duration=600)
    gor = []
    monkeypatch.setattr(cli, "_kareler", lambda ctx, d, z, *a: gor.append((z, a)) or [])
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0"], env=ortam, kos=Kos(), uyku=lambda s: None) == 0
    (z, a), = gor
    assert z[:2] == [90.0, 150.0] and a[2] == 2 and a[3] is True and list(a[4]) == [90.0, 150.0]


def test_isaret_kare_yogunluktan_once(ortam):
    onbellek(ortam, ["sohbet", "komut şu terminalde"] + ["x"] * 8, duration=600)
    assert main(["paket", VID, "--kare", "1", "--istek-tavan", "0"], env=ortam, kos=SahneKos(), uyku=lambda s: None) == 0
    assert kareler(ortam) == ["1:30"]  # 5:00 daha yoğun ama işaret anı önce


def test_sahne_alinamazsa_paket_surer_sebep_kayitli(ortam):
    onbellek(ortam, [], duration=600)
    kos = SahneKos(rc=1)
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    j = json.loads((Path(ortam["VIDEO_CACHE"]) / VID / "sahne.json").read_text(encoding="utf-8"))
    assert j["durum"].startswith("sahne alınamadı") and "googlevideo" not in j["durum"] and j["sahneler"] == []
    assert kareler(ortam) == ["2:30", "7:30"]
    k2 = SahneKos()
    assert main(["paket", VID, "--kare", "2", "--istek-tavan", "0", "--kare-yalniz"], env=ortam, kos=k2, uyku=lambda s: None) == 0
    assert len(tara(k2)) == 1  # hata durumu önbellek sayılmaz, yeniden denenir


def test_kare_komutu_tum_videoyu_taramaz(ortam):
    onbellek(ortam, ["a", "b"], duration=600)
    kos = SahneKos()
    assert main(["kare", VID, "--t", "1:00"], env=ortam, kos=kos) == 0
    assert not tara(kos)
