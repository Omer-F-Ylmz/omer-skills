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


def _env(ad):
    """os.environ boşsa kullanıcı ortamından (HKCU\\Environment) oku; değer asla yazdırılmaz."""
    v = os.environ.get(ad)
    if v or sys.platform != "win32":
        return v
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ad)[0] or None
    except OSError:
        return None


TOK, CHAT = _env("TELEGRAM_BOT_TOKEN"), _env("TELEGRAM_CHAT_ID")


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


def ozet():
    """'durum' cevabı: saf Python, MODEL ÇAĞRISI YOK (yalnız arka_sira/_oto.json/psutil/nvidia-smi okuma + metin biçimleme)."""
    import psutil
    sys.path.insert(0, str(KOK / "tools"))
    import arka_sira, arka_oto
    d = arka_oto._durum()
    s = ["DURUM " + time.strftime("%d %b %H:%M"),
         "Koşan: " + (", ".join(sorted(arka_sira.canli_isler())) or "yok"),
         f"Kuyruk ({len(arka_sira.kuyruk())}): " + (", ".join(arka_sira.kuyruk()[:5]) or "boş"),
         f"RAM %{psutil.virtual_memory().percent:.0f} · GPU %{arka_sira.gpu():.0f}",
         "Karar bekleyen: " + (", ".join(f"{a}:{n}" for a, n in d["karar"].items()) or "yok"),
         "Son bitişler:"]
    s += ["- " + o for o in [o for o in d["olaylar"] if "BITTI" in o.upper() or "bitti" in o][-3:]] or ["- yok"]
    return "\n".join(s)[:3500]


def cevapla():
    """Yeni mesajları oku; 'durum' / '/durum' ise özet gönder. Başka metin yalnız gelen.jsonl'de kalır; komut ÇALIŞTIRILMAZ."""
    n0 = GELEN.read_text("utf-8").count("\n") if GELEN.exists() else 0
    oku()
    yeni = (GELEN.read_text("utf-8").splitlines() if GELEN.exists() else [])[n0:]
    cevap = 0
    for s in yeni:
        j = json.loads(s)
        if not j["kimden"] and j["metin"].strip().lstrip("/").lower() == "durum":
            api("sendMessage", chat_id=CHAT, text=ozet())
            cevap += 1
    return len(yeni), cevap


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
    elif k == "cevapla":
        print("yeni, cevap =", cevapla())
    elif k == "son":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        for s in (GELEN.read_text("utf-8").splitlines() if GELEN.exists() else [])[-n:]:
            print(s)
    elif k == "rehber":
        rehber(); print("channel_directory yazildi")
    elif k == "gonder":
        print(api("sendMessage", chat_id=CHAT, text=sys.argv[2][:3500])["ok"])
