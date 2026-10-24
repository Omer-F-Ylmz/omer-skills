"""VERİM-HEDEF-1 pano: saatlik Claude jetonu/$, ücretsiz payı, RAM, kalite kapısı + merdiven.
  python tools/verim_pano.py [GUN=bugün]            # saatlik pano + özet
  python tools/verim_pano.py kalite <adim_turu> ok|red [kaynak]   # kalite kapısı kaydı (hakem/test/Desktop)
  python tools/verim_pano.py merdiven               # adım türü başına geçerli basamak
Salt okur (usage.db, ucretsiz/durum.json, ram-buyume.json); yazdığı tek dosya kalite.jsonl."""
import collections, datetime, json, sqlite3, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
DB = Path.home() / ".claude" / "usage.db"
HAVUZ = KOK / ".kos/kopru/ucretsiz/durum.json"
RAM = KOK / ".kos/kopru/ram-buyume.json"
KALITE = KOK / ".kos/kopru/verim/kalite.jsonl"
SIRA = KOK / ".kos/kopru/ajan-sira"
MERDIVEN = ["ucretsiz", "haiku", "sonnet", "opus"]
PENCERE, RED_ESIK = 5, 0.4  # son 5 kayıttan ≥%40 RED → bir basamak yukarı
# $/M jeton: (girdi, çıktı); önbellek okuma 0.1x, yazma 1.25x girdi
FIYAT = {"sonnet": (3, 15), "opus": (5, 25), "haiku": (1, 5)}


def _dolar(model, i, o, cr, cc):
    f = next((v for k, v in FIYAT.items() if k in (model or "")), FIYAT["sonnet"])
    return (i * f[0] + o * f[1] + cr * f[0] * 0.1 + cc * f[0] * 1.25) / 1e6


def claude(gun):
    c = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    yerel = datetime.datetime.now().astimezone().tzinfo
    saat = collections.defaultdict(lambda: [0, 0, 0.0])  # tur, jeton, $
    for ts, m, i, o, cr, cc in c.execute(
            "select timestamp,model,input_tokens,output_tokens,cache_read_tokens,cache_creation_tokens from turns"):
        t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(yerel)
        if t.strftime("%Y-%m-%d") != gun:
            continue
        s = saat[t.hour]
        s[0] += 1; s[1] += i + o; s[2] += _dolar(m, i, o, cr, cc)
    return saat


def haftalik():
    c = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    gun = collections.defaultdict(float)
    for ts, m, i, o, cr, cc in c.execute(
            "select timestamp,model,input_tokens,output_tokens,cache_read_tokens,cache_creation_tokens from turns"
            " where substr(timestamp,1,10) >= date('now','-6 day')"):
        gun[ts[:10]] += _dolar(m, i, o, cr, cc)
    return gun


def ucretsiz(gun):
    try:
        say = json.loads(HAVUZ.read_text(encoding="utf-8")).get("say", {})
    except (OSError, ValueError):
        return 0
    return sum(v[1] for k, v in say.items() if k.startswith("p:") and v[0] == gun)


def ram():
    try:
        d = json.loads(RAM.read_text(encoding="utf-8"))
        return sum(d["mb"].values())
    except (OSError, ValueError, KeyError):
        return None


def kayit():
    try:
        return [json.loads(l) for l in KALITE.read_text(encoding="utf-8").splitlines() if l.strip()]
    except OSError:
        return []


def eksik_tur():
    """(devam turu $, devam turu adedi, son 7 gün en sık eksik araçlar). Devam turu = ajan-sira/*-a.json, *-a2.json."""
    sinir = datetime.datetime.now().timestamp() - 7 * 86400
    dolar = adet = 0
    sik = collections.Counter()
    for p in SIRA.glob("*.json"):
        if p.stat().st_mtime < sinir:
            continue
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if p.name.endswith(".denetim.json"):
            if "eksik" in d.get("durum", ""):
                sik.update(d.get("eksik", []))
        elif p.stem.endswith(("-a", "-a2")) and ".zorunlu" not in p.name:
            dolar += d.get("total_cost_usd", 0) or 0; adet += 1
    return round(dolar, 2), adet, sik.most_common(5)


def merdiven():
    """Adım türü → basamak. Başlangıç ücretsiz; pencere RED oranı eşiği aşarsa bir yukarı (her aşım +1)."""
    tur = collections.defaultdict(list)
    for r in kayit():
        tur[r["tur"]].append(r["sonuc"])
    out = {}
    for t, l in tur.items():
        b = 0
        for k in range(len(l)):  # kayıtları sırayla oynat: pencere dolunca eşik aşılırsa yüksel, pencereyi sıfırla
            w = l[max(0, k - PENCERE + 1):k + 1]
            if len(w) >= 3 and w.count("red") / len(w) >= RED_ESIK and b < len(MERDIVEN) - 1:
                b += 1
                l[:k + 1] = ["ok"] * (k + 1)
        out[t] = MERDIVEN[b]
    return out


def pano(gun):
    s = claude(gun)
    print(f"VERİM PANO {gun}")
    print("saat  tur  jeton(K)   $")
    for h in sorted(s):
        print(f"{h:02d}    {s[h][0]:4d} {s[h][1]/1e3:9.0f} {s[h][2]:7.2f}")
    tur = sum(v[0] for v in s.values()); dol = sum(v[2] for v in s.values())
    u = ucretsiz(gun)
    pay = 100 * u / (u + tur) if u + tur else 0
    hf = haftalik(); r = ram()
    print(f"toplam: Claude tur={tur} ${dol:.2f} | ücretsiz çağrı={u} pay=%{pay:.1f}")
    print(f"7 gün Claude ≈ ${sum(hf.values()):.0f} ({', '.join(f'{k[5:]}=${v:.0f}' for k, v in sorted(hf.items()))})")
    print(f"RAM (son ram-buyume örneği): {r} MB" if r is not None else "RAM: ölçüm yok")
    k = kayit()
    ok = sum(1 for x in k if x["sonuc"] == "ok")
    print(f"KALİTE kapısı: {ok}/{len(k)} ok" if k else "KALİTE kapısı: kayıt yok (kalite ... ile besle)")
    d, a, sik = eksik_tur()
    print(f"EKSİK-TUR (7 gün): {a} devam turu ${d:.2f} | en sık eksik: {', '.join(f'{k}×{v}' for k, v in sik) or 'yok'} → kombinler.json önerisi: bunları ilk tura al")
    print("limit %: claude-usage CLI yalnız $/jeton verir, haftalık limit yüzdesi sunmaz → $ vekil")
    print("merdiven:", merdiven() or "kayıt yok")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["kalite"] and len(a) >= 3 and a[2] in ("ok", "red"):
        KALITE.parent.mkdir(parents=True, exist_ok=True)
        with KALITE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"), "tur": a[1],
                                "sonuc": a[2], "kaynak": a[3] if len(a) > 3 else ""}, ensure_ascii=False) + "\n")
    elif a[:1] == ["merdiven"]:
        print(json.dumps(merdiven(), ensure_ascii=False))
    else:
        pano(a[0] if a else datetime.date.today().isoformat())
