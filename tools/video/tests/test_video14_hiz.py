"""VİDEO-14 Faz 2: uzun video hızlandırma bayrakları (varsayılan kapalı; altın ölçümüyle açılır)."""
import sys
import types

from video import cli
from video import goz as gz


def test_uzun_hiz_esik(monkeypatch):
    """VIDEO_UZUN_HIZ=1 → 10-60 dk video da melez anahtar-kare yolu (+ es_kare OCR eşi, paralel dilim); bayraksız eşik ANAHTAR_SN."""
    monkeypatch.delenv("VIDEO_HIZ2", raising=False)
    monkeypatch.delenv("VIDEO_UZUN_HIZ", raising=False)
    assert cli._hiz2(880) == ""
    monkeypatch.setenv("VIDEO_UZUN_HIZ", "1")
    assert cli._hiz2(880) == "2" and cli._hiz2(599) == "" and cli._hiz2(6407) == "2"
    monkeypatch.setenv("VIDEO_HIZ2", "0")
    assert cli._hiz2(880) == ""


class _E:
    def __getattr__(self, a):
        return a


def _params(monkeypatch, tmp_path):
    for f in gz.MODEL_DOSYA.values():
        (tmp_path / f).write_bytes(b"")
    monkeypatch.setenv("VIDEO_OCR_MODEL", str(tmp_path))
    al = {}
    monkeypatch.setitem(sys.modules, "rapidocr", types.SimpleNamespace(
        LangCls=_E(), LangDet=_E(), LangRec=_E(), ModelType=_E(), OCRVersion=_E(), RapidOCR=lambda params: al.update(params)))
    gz.rapid_yukle("cpu")
    return al


def test_ocr_det_bayrak(monkeypatch, tmp_path):
    """VIDEO_OCR_DET=<px> → algılama girdisi uzun kenar ≤ px (Det.limit_type max); bayraksız RapidOCR varsayılanı, önbellek anahtarı ayrışır."""
    monkeypatch.delenv("VIDEO_OCR_DET", raising=False)
    assert "Det.limit_side_len" not in _params(monkeypatch, tmp_path) and gz.ocr_det() == 0
    monkeypatch.setenv("VIDEO_OCR_DET", "1280")
    p = _params(monkeypatch, tmp_path)
    assert p["Det.limit_type"] == "max" and p["Det.limit_side_len"] == 1280 and gz.ocr_det() == 1280


def test_ocr_cls_bayrak(monkeypatch, tmp_path):
    """VIDEO_OCR_CLS=0 → yön sınıflayıcı kapalı (ekran metni hep yatay; HYMD 60 kare −28% süre, cls 180° çevirip çöp okuyordu); bayraksız RapidOCR varsayılanı."""
    monkeypatch.delenv("VIDEO_OCR_CLS", raising=False)
    assert "Global.use_cls" not in _params(monkeypatch, tmp_path) and gz.ocr_cls0() is False
    monkeypatch.setenv("VIDEO_OCR_CLS", "0")
    assert _params(monkeypatch, tmp_path)["Global.use_cls"] is False and gz.ocr_cls0() is True


def test_ocr_esz(monkeypatch, tmp_path):
    """VİDEO-14-d4: rapid_yukle(esz=k) → CPU oturumu k iş parçacığı (havuz işçileri çekirdekleri bölüşür); verilmezse RapidOCR varsayılanı."""
    monkeypatch.delenv("VIDEO_OCR_CLS", raising=False)
    assert "EngineConfig.onnxruntime.intra_op_num_threads" not in _params(monkeypatch, tmp_path)
    al = _params(monkeypatch, tmp_path)
    gz.rapid_yukle("cpu", esz=3)
    assert al["EngineConfig.onnxruntime.intra_op_num_threads"] == 3


def test_havuz_sayi(monkeypatch):
    """VIDEO_OCR_HAVUZ=N → N CPU işçisi, boş RAM'e göre kısılır (iki RAM_ESIK_GB payı, işçi başı HAVUZ_GB); bayraksız 0."""
    monkeypatch.delenv("VIDEO_OCR_HAVUZ", raising=False)
    assert cli._havuz(100) == 0
    monkeypatch.setenv("VIDEO_OCR_HAVUZ", "6")
    assert cli._havuz(100) == 6 and cli._havuz(2 * cli.RAM_ESIK_GB + 2 * cli.HAVUZ_GB) == 2 and cli._havuz(1) == 0


def _havuz_kur(monkeypatch, cpu):
    import time
    from concurrent.futures import ThreadPoolExecutor
    monkeypatch.setattr(cli, "HAVUZ_EX", ThreadPoolExecutor)
    monkeypatch.setattr(cli, "_cpu_oku", cpu)

    def motor(y):
        time.sleep(0.005)
        return [("dml " + y.name, 0.9, 1)]
    monkeypatch.setattr(cli, "_MOTOR", [None])
    return {"rapid": lambda: motor}


def test_ocr_havuz_is_calma(monkeypatch, tmp_path):
    """DML 10'lu partiler + N CPU işçisi aynı kuyruktan çalar; her kare bir kez, sıra yollar sırası; güvenlik tavanı aşılınca kalan döner."""
    import time

    def cpu(y):
        time.sleep(0.005)
        return [["cpu " + y.rsplit("/", 1)[-1].rsplit("\\", 1)[-1], 0.9, 1]]
    ctx = _havuz_kur(monkeypatch, cpu)
    yollar = [(float(i), tmp_path / f"k{i:06d}.jpg") for i in range(40)]
    okunan, kalan = cli._ocr_havuz(ctx, yollar, 3, time.monotonic())
    assert [t for t, _ in okunan] == [t for t, _ in yollar] and kalan == []
    assert all(r[0][0].endswith(y.name) for (_, r), (_, y) in zip(okunan, yollar))
    assert {r[0][0].split()[0] for _, r in okunan} == {"dml", "cpu"}
    monkeypatch.setattr(gz, "OCR_GUVENLIK", -1)
    assert cli._ocr_havuz(ctx, yollar, 3, time.monotonic()) == ([], [t for t, _ in yollar])


def test_ocr_havuz_cpu_hata(monkeypatch, tmp_path):
    """CPU işçisi çökerse (model/bellek) kare kaybolmaz: kuyruğa geri döner, DML okur."""
    import time

    def cpu(y):
        raise MemoryError("cpu yok")
    ctx = _havuz_kur(monkeypatch, cpu)
    yollar = [(float(i), tmp_path / f"k{i:06d}.jpg") for i in range(25)]
    okunan, kalan = cli._ocr_havuz(ctx, yollar, 2, time.monotonic())
    assert len(okunan) == 25 and kalan == [] and all(r[0][0].startswith("dml") for _, r in okunan)
