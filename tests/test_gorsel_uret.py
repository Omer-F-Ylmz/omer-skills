"""KURULUM-GÖRSEL K5: tools/gorsel_uret.py — netstat/tasklist/Popen taklitli, ComfyUI yerine sahte HTTP sunucu."""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import gorsel_uret as gu  # noqa: E402

PID = 5151
PNG = b"\x89PNG\r\n\x1a\nsahte"


def dinleme(adres, pid=PID):
    return f"  TCP    {adres}         0.0.0.0:0              LISTENING       {pid}\n"


class Sahte:
    """netstat/tasklist/taskkill ve ComfyUI Popen taklidi."""

    def __init__(self, netstat="", sonra_netstat=None, canli=True):
        self.komutlar, self.popen = [], []
        self.netstat = netstat
        self.sonra_netstat = dinleme(f"127.0.0.1:{gu.PORT}") if sonra_netstat is None else sonra_netstat
        self.canli = canli

    def run(self, cmd, **_):
        self.komutlar.append(cmd)
        ad = Path(cmd[0]).name.lower()
        cikti = ""
        if ad == "netstat":
            cikti = self.netstat
        elif ad == "tasklist" and self.canli:
            cikti = f"python.exe                   {PID} Console    1    900.000 K\n"
        elif ad.startswith("rembg"):
            Path(cmd[-1]).write_bytes(PNG)
        return type("R", (), {"stdout": cikti, "returncode": 0})()

    def Popen(self, cmd, **_):
        self.popen.append(cmd)
        self.netstat = self.sonra_netstat
        return type("P", (), {"pid": PID})()

    def oldurmeler(self):
        return [c for c in self.komutlar if c[0].lower() == "taskkill"]


class Comfy(BaseHTTPRequestHandler):
    istekler = []

    def log_message(self, *_):
        pass

    def _yanit(self, govde, tur="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", tur)
        self.end_headers()
        self.wfile.write(govde)

    def do_POST(self):
        Comfy.istekler.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
        self._yanit(json.dumps({"prompt_id": f"p{len(Comfy.istekler)}"}).encode())

    def do_GET(self):
        if self.path.startswith("/history/"):
            pid = self.path.rsplit("/", 1)[1]
            cikti = {"9": {"images": [{"filename": f"{pid}.png", "subfolder": "", "type": "output"}]}}
            self._yanit(json.dumps({pid: {"outputs": cikti}}).encode())
        else:
            self._yanit(PNG, "image/png")


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    masa = tmp_path / "Desktop"
    proje = masa / "Telve"
    proje.mkdir(parents=True)
    comfy = tmp_path / "ComfyUI"
    for alt in {d.split("/")[0] for m in gu.MODELLER.values() for d in m["dosyalar"]}:
        (comfy / "models" / alt).mkdir(parents=True, exist_ok=True)
    for ad in ("zimage", "klein"):
        for d in gu.MODELLER[ad]["dosyalar"]:
            (comfy / "models" / d).write_bytes(b"x")
    (comfy / "models" / "upscale_models").mkdir(exist_ok=True)
    (comfy / "models" / "upscale_models" / "RealESRGAN_x4plus.safetensors").write_bytes(b"x")
    (comfy / "input").mkdir()
    monkeypatch.setattr(gu, "MASAUSTU", masa)
    monkeypatch.setattr(gu, "COMFY", comfy)
    monkeypatch.setattr(gu, "DURUM", tmp_path / "gorsel-oturum.json")
    monkeypatch.setattr(gu.time, "sleep", lambda _: None)
    sunucu = ThreadingHTTPServer(("127.0.0.1", 0), Comfy)
    threading.Thread(target=sunucu.serve_forever, daemon=True).start()
    monkeypatch.setattr(gu, "SUNUCU", f"http://127.0.0.1:{sunucu.server_address[1]}")
    Comfy.istekler = []
    yield proje
    sunucu.shutdown()


def kur(monkeypatch, sahte):
    monkeypatch.setattr(gu.subprocess, "run", sahte.run)
    monkeypatch.setattr(gu.subprocess, "Popen", sahte.Popen)
    return sahte


def acik(sahte):
    gu.DURUM.write_text(json.dumps({"pid": PID, "baslangic": 0}), encoding="utf-8")
    sahte.netstat = dinleme(f"127.0.0.1:{gu.PORT}")
    return sahte


def uret(proje, *ek):
    return gu.main(["uret", "--is", "foto", "--prompt", "fincan", "--cikti", str(proje), *ek])


def test_yol_siniri_disi_2(ortam, monkeypatch, tmp_path):
    s = acik(kur(monkeypatch, Sahte()))
    assert gu.main(["uret", "--is", "foto", "--prompt", "x", "--cikti", str(tmp_path / "dis")]) == 2
    assert gu.main(["uret", "--is", "foto", "--prompt", "x", "--cikti", str(gu.MASAUSTU)]) == 2
    assert Comfy.istekler == [] and s.popen == []


def test_yol_buyuk_kucuk_harf_duyarsiz(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    assert uret(Path(str(ortam).upper())) == 0


@pytest.mark.parametrize("komut", ["ac", "uret", "buyut"])
def test_9876_doluysa_2(ortam, monkeypatch, komut):
    s = acik(kur(monkeypatch, Sahte()))
    s.netstat += dinleme("127.0.0.1:9876", 777)
    (ortam / "a.png").write_bytes(PNG)
    argv = {"ac": ["ac"], "uret": ["uret", "--is", "foto", "--prompt", "x", "--cikti", str(ortam)],
            "buyut": ["buyut", str(ortam / "a.png"), "--kat", "2"]}[komut]
    assert gu.main(argv) == 2
    assert s.popen == [] and Comfy.istekler == []


def test_adet_5_reddedilir(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    assert uret(ortam, "--adet", "5") == 2
    assert Comfy.istekler == []


def test_referans_yalniz_duzenle(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    ref = ortam / "ref.png"
    ref.write_bytes(PNG)
    assert uret(ortam, "--referans", str(ref)) == 2
    assert gu.main(["uret", "--is", "duzenle", "--prompt", "x", "--cikti", str(ortam)]) == 2
    assert Comfy.istekler == []


def test_127_disi_dinleme_1_ve_pid_ile_kapatma(ortam, monkeypatch):
    s = kur(monkeypatch, Sahte(sonra_netstat=dinleme(f"0.0.0.0:{gu.PORT}")))
    assert gu.main(["ac"]) == 1
    assert s.oldurmeler() == [["taskkill", "/PID", str(PID), "/T", "/F"]]
    assert "--listen" in s.popen[0] and s.popen[0][s.popen[0].index("--listen") + 1] == "127.0.0.1"


def test_ac_basarili_durum_dosyasi(ortam, monkeypatch):
    kur(monkeypatch, Sahte())
    assert gu.main(["ac"]) == 0
    assert json.loads(gu.DURUM.read_text(encoding="utf-8"))["pid"] == PID


def test_kapatma_yalniz_durum_pid(ortam, monkeypatch):
    s = kur(monkeypatch, Sahte(netstat=dinleme(f"127.0.0.1:{gu.PORT}", 999)))
    assert gu.main(["kapat"]) == 0  # durum dosyası yok: yabancı 8188 dinleyicisine dokunulmaz
    assert s.oldurmeler() == []
    acik(s)
    assert gu.main(["kapat"]) == 0
    assert s.oldurmeler() == [["taskkill", "/PID", str(PID), "/T", "/F"]]
    assert all("/IM" not in c for c in s.komutlar)
    assert not gu.DURUM.exists()


def test_meta_json_alanlari(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    assert uret(ortam, "--tohum", "42", "--boyut", "768x512", "--adet", "2") == 0
    pngler = sorted(ortam.glob("*.png"))
    assert len(pngler) == 2 and pngler[0].read_bytes() == PNG
    meta = json.loads(pngler[0].with_suffix(".json").read_text(encoding="utf-8"))
    assert {"model", "lisans", "prompt", "tohum", "boyut", "sure"} <= set(meta)
    assert meta["prompt"] == "fincan" and meta["boyut"] == "768x512" and meta["tohum"] in (42, 43)
    assert "Apache" in meta["lisans"]


@pytest.mark.parametrize("is_", ["foto", "urun", "doku", "metinli"])
def test_is_model_yonlendirmesi(ortam, monkeypatch, is_):
    acik(kur(monkeypatch, Sahte()))
    assert gu.main(["uret", "--is", is_, "--prompt", "x", "--cikti", str(ortam)]) == 0
    beklenen = gu.MODELLER[gu.YONLENDIRME[is_]]["dosyalar"][0].split("/")[1]
    unet = [n for n in Comfy.istekler[0]["prompt"].values() if n["class_type"] == "UNETLoader"]
    assert unet[0]["inputs"]["unet_name"] == beklenen


def test_duzenle_klein_ve_referans(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    refler = [ortam / "r1.png", ortam / "r2.png"]
    for r in refler:
        r.write_bytes(PNG)
    argv = ["uret", "--is", "duzenle", "--prompt", "koyu fon", "--cikti", str(ortam), "--referans", *map(str, refler)]
    assert gu.main(argv) == 0
    dugum = Comfy.istekler[0]["prompt"].values()
    assert sum(n["class_type"] == "ReferenceLatent" for n in dugum) == 4
    assert {n["inputs"]["image"] for n in dugum if n["class_type"] == "LoadImage"} == {"r1.png", "r2.png"}


def test_kurulmamis_model_2(ortam, monkeypatch):
    acik(kur(monkeypatch, Sahte()))
    assert uret(ortam, "--model", "qwen-image") == 2
    monkeypatch.setitem(gu.YONLENDIRME, "metinli", "qwen-image")
    assert gu.main(["uret", "--is", "metinli", "--prompt", "x", "--cikti", str(ortam)]) == 2
    assert gu.main(["uret", "--is", "duzenle", "--model", "zimage", "--prompt", "x", "--cikti", str(ortam),
                    "--referans", str(ortam / "r.png")]) == 2
    assert Comfy.istekler == []


def test_kapaliyken_uret_2(ortam, monkeypatch):
    kur(monkeypatch, Sahte())
    assert uret(ortam) == 2


def test_buyut_ve_arkaplan(ortam, monkeypatch):
    s = acik(kur(monkeypatch, Sahte()))
    girdi = ortam / "fincan.png"
    girdi.write_bytes(PNG)
    assert gu.main(["buyut", str(girdi), "--kat", "2"]) == 0
    olcek = [n for n in Comfy.istekler[0]["prompt"].values() if n["class_type"] == "ImageScaleBy"]
    assert olcek[0]["inputs"]["scale_by"] == 0.5
    assert json.loads((ortam / "fincan-x2.json").read_text(encoding="utf-8"))["lisans"].startswith("BSD")
    assert gu.main(["arkaplan", str(girdi)]) == 0
    rembg = [c for c in s.komutlar if Path(c[0]).name.lower().startswith("rembg")][0]
    assert rembg[rembg.index("-m") + 1] == "birefnet-general"
    assert (ortam / "fincan-arkaplansiz.png").exists() and (ortam / "fincan-arkaplansiz.json").exists()
    assert gu.main(["arkaplan", str(gu.MASAUSTU.parent / "x.png")]) == 2
