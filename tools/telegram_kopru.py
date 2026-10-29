"""TELEGRAM-KOPRU: tek okuyucu. Bota gelen mesajları gelen.jsonl'e yazar (yalnız okuma, komut ÇALIŞTIRMAZ),
hermes channel_directory.json'a telegram hedefini yazar. Token/chat id yazdırılmaz.
Kullanım: telegram_kopru.py durum | oku | son [N] | rehber | gonder "metin"
"""
import json, os, sys, time, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DIZ = KOK / ".kos/kopru/telegram"
GELEN, OFFSET = DIZ / "gelen.jsonl", DIZ / "offset.txt"
HOME = KOK / "araclar/hermes-home"
TOK, CHAT = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")


def api(yontem, **veri):
    r = urllib.request.Request(f"https://api.telegram.org/bot{TOK}/{yontem}", data=json.dumps(veri).encode(),
                               headers={"Content-Type": "application/json", "User-Agent": "omer-arka/1"})
    return json.load(urllib.request.urlopen(r, timeout=20))


def oku():
    """getUpdates + kalıcı offset; yalnız Ömer'in chat id'sinden gelenler kaydedilir."""
    DIZ.mkdir(parents=True, exist_ok=True)
    off = int(OFFSET.read_text()) if OFFSET.exists() else 0
    s = api("getUpdates", offset=off, timeout=0, allowed_updates=["message"])["result"]
    yeni = 0
    with GELEN.open("a", encoding="utf-8") as f:
        for u in s:
            m = u.get("message") or {}
            if str((m.get("chat") or {}).get("id")) == CHAT:
                f.write(json.dumps({"id": u["update_id"], "t": m.get("date"), "kimden": (m.get("from") or {}).get("is_bot"),
                                    "metin": m.get("text", "")}, ensure_ascii=False) + "\n")
                yeni += 1
            off = max(off, u["update_id"] + 1)
    OFFSET.write_text(str(off))
    return len(s), yeni


def rehber():
    p = HOME / "channel_directory.json"
    d = json.loads(p.read_text("utf-8")) if p.exists() else {"platforms": {}}
    d["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    d.setdefault("platforms", {})["telegram"] = [{"id": CHAT, "name": "Omer (arka-oto botu)", "type": "dm"}]
    p.write_text(json.dumps(d, indent=2), "utf-8")


if __name__ == "__main__":
    if not (TOK and CHAT):
        sys.exit("TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID yok")
    k = sys.argv[1] if len(sys.argv) > 1 else "durum"
    if k == "durum":
        w = api("getWebhookInfo")["result"]
        print("webhook_url_var:", bool(w.get("url")), "bekleyen:", w.get("pending_update_count"))
    elif k == "oku":
        print("alinan, kaydedilen =", oku())
    elif k == "son":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        for s in (GELEN.read_text("utf-8").splitlines() if GELEN.exists() else [])[-n:]:
            print(s)
    elif k == "rehber":
        rehber(); print("channel_directory yazildi")
    elif k == "gonder":
        print(api("sendMessage", chat_id=CHAT, text=sys.argv[2][:3500])["ok"])
