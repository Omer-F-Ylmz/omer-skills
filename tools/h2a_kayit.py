"""TOKEN-H2a: Headroom /transformations/feed yoklayıcı — istek başına mesaj sha8 dizisi, gövde yazmaz.
Proxy `--log-messages` ile son 100 isteği bellekte tutar (request_logger.py:150); feed loopback-only (server.py:5018).
Feed'de system/tools yok (server.py:5047-5069) → yalnız messages hash'lenir. PC yeniden başlayınca durur.
Çalıştır: python tools/h2a_kayit.py   ·   Çıktı: ~/.headroom/h2a_kayit.jsonl"""
import hashlib
import json
import time
import urllib.request
from pathlib import Path

FEED = "http://127.0.0.1:6768/transformations/feed?limit={}"
CIKTI = Path.home() / ".headroom" / "h2a_kayit.jsonl"
ARALIK = 60
ALANLAR = ("request_id", "model", "turn_id", "input_tokens_original", "input_tokens_optimized",
           "tokens_saved", "transforms_applied", "uncached_input_tokens", "cache_write_tokens",
           "cache_read_tokens")


def sha8(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:8]


def satir(t):
    s = {"ts": t.get("timestamp"), **{a: t.get(a) for a in ALANLAR}}
    for ad in ("request_messages", "compressed_messages"):
        s[ad] = [[m.get("role"), sha8(m.get("content"))] for m in t.get(ad) or []]
    return s


def cek(limit):
    with urllib.request.urlopen(FEED.format(limit), timeout=30) as r:
        return json.load(r)["transformations"]


def yokla(cek, gorulen, yaz):
    feed = cek(10)
    ortusur = lambda f: any(t["request_id"] in gorulen for t in f)  # noqa: E731
    if gorulen and feed and not ortusur(feed):
        feed = cek(100)
        if not ortusur(feed):
            yaz({"bosluk": time.strftime("%Y-%m-%dT%H:%M:%S")})
    for t in feed:
        if t["request_id"] not in gorulen:
            gorulen.add(t["request_id"])  # ponytail: set sınırsız büyür (~4k/gün), günlerce koşacaksa son N'e kırp
            yaz(satir(t))


def main():
    gorulen = set()  # ponytail: yeniden başlatmada son 10 tekrar yazılır; okuyan request_id ile tekilleştirir
    with CIKTI.open("a", encoding="utf-8") as f:
        def yaz(s):
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            f.flush()
        while True:
            try:
                yokla(cek, gorulen, yaz)
            except (OSError, ValueError, KeyError) as e:
                yaz({"hata": repr(e)[:200], "ts": time.strftime("%Y-%m-%dT%H:%M:%S")})
            time.sleep(ARALIK)


if __name__ == "__main__":
    main()
