"""telegram_kopru.cevapla birim testi: sahte getUpdates; model/ağ çağrısı yok. Çalıştır: python tools/test_telegram_kopru.py"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import telegram_kopru as t

t.CHAT = "42"
t.DIZ = Path(tempfile.mkdtemp())
t.GELEN, t.OFFSET = t.DIZ / "gelen.jsonl", t.DIZ / "offset.txt"
gonderilen = []


def sahte(yontem, **v):
    if yontem == "getUpdates":
        m = lambda i, c, x: {"update_id": i, "message": {"chat": {"id": c}, "date": 1, "from": {"is_bot": False}, "text": x}}
        return {"result": [m(1, 42, "Durum"), m(2, 42, "/durum"), m(3, 42, "rm -rf"), m(4, 99, "durum")]}
    gonderilen.append(v["text"])
    return {"ok": True}


t.api = sahte
t.ozet = lambda: "OZET"
yeni, cevap = t.cevapla()
assert (yeni, cevap) == (3, 2), (yeni, cevap)  # yabancı chat elendi, 'rm -rf' cevapsız/çalıştırılmadı
assert gonderilen == ["OZET", "OZET"]
assert t.OFFSET.read_text() == "5"
print("TAMAM")
