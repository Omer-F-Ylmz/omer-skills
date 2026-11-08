"""ARKA-OTO-1: arka iş sonuçlarını Claude'suz ($0) değerlendirir; arka_sira.tur() her turda çağırır.
  python tools/arka_oto.py          tek tur   |   --desktop  _desktop.md'yi yeniden yazar
İş json'u: 'kapi' {"tur": "hakem >= %87"}, 'sonraki' [yön, ...] (Desktop'un önceden yazdığı sıradaki TUR yönleri).
Karar: regex + ücretsiz havuz AYNI sonucu vermeli (KABUL/DUR); çakışma ya da havuz yok → 'karar-bekliyor' (tahmin yok)."""
import json
import os
import re
import sys
import time
import urllib.request

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARKA = os.path.join(KOK, ".kos", "kopru", "arka")
TAKILDI_SN = 30 * 60
RAM_BILDIR = 89.0
SIZINTI = []  # test: gönderilecek bildirimler (ARKA_OTO_TEST=1 iken ağa çıkılmaz)


def _p(ad):
    return os.path.join(ARKA, ad)


def _durum():
    try:
        return json.load(open(_p("_oto.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return {"islenen": {}, "bildirilen": [], "olaylar": [], "karar": {}, "yeniden": {}}


def _yaz(d):
    d["olaylar"] = d["olaylar"][-200:]
    json.dump(d, open(_p("_oto.json"), "w", encoding="utf-8"), ensure_ascii=False)


def olay(d, ad, metin, bildir=False):
    d["olaylar"].append(time.strftime("%d %H:%M ") + ad + " " + metin)
    if bildir:
        bildirim(d, f"{ad}|{metin}", f"[{ad}] {metin}")


def bildirim(d, anahtar, metin):
    """Aynı olay iki kez gitmez. Anahtar/token yazdırılmaz; chat id yoksa 'telegram-kurulum-eksik' olayı bir kez."""
    if anahtar in d["bildirilen"]:
        return
    d["bildirilen"].append(anahtar)
    d["bildirilen"] = d["bildirilen"][-500:]
    if os.environ.get("ARKA_OTO_TEST"):
        SIZINTI.append(metin)
        return
    tok, chat = os.environ.get("TELEGRAM_BOT_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if not tok:
        return
    try:
        if not chat:  # getUpdates'ten son sohbet; yoksa Ömer'in bota bir mesaj yazması gerekir
            r = json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{tok}/getUpdates", headers={"User-Agent": "omer-arka/1"}), timeout=15))
            ids = [u["message"]["chat"]["id"] for u in r.get("result", []) if "message" in u]
            if not ids:
                d["olaylar"].append(time.strftime("%d %H:%M ") + "telegram chat id yok: Omer'in bota bir mesaj yazmasi gerek")
                return
            chat = str(ids[-1])
        req = urllib.request.Request(f"https://api.telegram.org/bot{tok}/sendMessage", data=json.dumps({"chat_id": chat, "text": metin[:3500]}).encode(),
                                     headers={"Content-Type": "application/json", "User-Agent": "omer-arka/1"})
        urllib.request.urlopen(req, timeout=15).read()
    except Exception as e:  # ağ hatası bildirimi bir sonraki tura bırakmaz ama turu da düşürmez
        d["olaylar"].append(time.strftime("%d %H:%M ") + "telegram hata " + type(e).__name__)


def sonuc_oku(ad):
    """(metin | None, maliyet | None). Log'da result yoksa (None, None)."""
    try:
        t = open(_p(ad + ".log"), encoding="utf-8", errors="replace").read()
    except OSError:
        return None, None
    i = t.rfind('"result":"')
    if i < 0:
        return None, None
    try:
        metin, _ = json.JSONDecoder().raw_decode(t, i + 9)
    except ValueError:
        return None, None
    m = re.search(r'"total_cost_usd":\s*([0-9.]+)', t[i:]) or re.search(r'"total_cost_usd":\s*([0-9.]+)', t)
    return metin, (m.group(1) if m else None)


def cikar(metin):
    c = re.findall(r"\b[0-9a-f]{7,8}\b", metin)
    c = [x for x in c if re.search(r"[a-f]", x) and re.search(r"\d", x)]
    return c[0] if c else "-"


def regex_karar(kapi, metin):
    """KABUL/DUR/None. Kapı 'etiket >= %N' biçimi: sonuçta etiketten sonraki ilk %sayı (ya da sayı/100) eşikle karşılaştırılır."""
    m = re.match(r"\s*(.+?)\s*>=?\s*%?\s*(\d+(?:[.,]\d+)?)", kapi or "")
    if not m:
        return None
    etiket, esik = m.group(1), float(m.group(2).replace(",", "."))
    degerler = []
    for e in re.finditer(re.escape(etiket) + r"[^\n]{0,60}?(?:%\s*(\d+(?:[.,]\d+)?)|(\d+(?:[.,]\d+)?)\s*(?:/\s*100|%))", metin, re.I):
        degerler.append(float((e.group(1) or e.group(2)).replace(",", ".")))
    if not degerler:
        return None
    return "KABUL" if degerler[-1] >= esik else "DUR"


def havuz_karar(kapi, metin):
    """Ücretsiz modelden KABUL/DUR; havuz yoksa ya da cevap anlaşılmazsa None. Claude'a çağrı yok (haiku_tavan=0)."""
    try:
        sys.path.insert(0, os.path.join(KOK, "tools"))
        import ucretsiz_havuz
        istem = ("Bir arka plan işinin sonuç metni ve kabul kapısı verilir. Sonuç kapıyı sağlıyorsa yalnız KABUL, sağlamıyorsa yalnız DUR, "
                 "sayı bulunamıyorsa yalnız BELIRSIZ yaz (tek kelime).\nKAPI: " + kapi + "\nSONUÇ:\n" + metin[-2500:])
        y, _, _ = ucretsiz_havuz.cagir("kolay", istem, max_tokens=20, zaman=60, haiku_tavan=0, etiket="arka-oto")
    except Exception:
        return None
    if not y:
        return None
    w = re.search(r"\b(KABUL|DUR|BELIRSIZ)\b", y.upper())
    return w.group(1) if w and w.group(1) != "BELIRSIZ" else None


def degerlendir(d, ad):
    j = json.load(open(_p(ad + ".json"), encoding="utf-8"))
    metin, maliyet = sonuc_oku(ad)
    if metin is None:
        return olu(d, ad, j, "bitti ama sonuc yok")
    commit, kapi = cikar(metin), (j.get("kapi") or {}).get("tur")
    mal = f"${float(maliyet):.2f}" if maliyet else "$?"
    if not kapi:
        karar, neden = "BITTI", "kapi yok"
    else:
        rg, hv = regex_karar(kapi, metin), havuz_karar(kapi, metin)
        if rg and rg == hv:
            karar, neden = rg, "regex+havuz"
        else:
            karar, neden = "BELIRSIZ", f"regex={rg} havuz={hv}"
    satir = f"{time.strftime('%H:%M')} | {ad} | {karar} | {mal} | {commit}"
    open(_p("gece-ozeti.md"), "a", encoding="utf-8").write(satir + "\n")
    if karar == "KABUL":
        sonraki = list(j.get("sonraki") or [])
        if sonraki:
            j["devam_notu"] = sonraki.pop(0)
            j["sonraki"] = sonraki
            j["yeni_oturum"] = False
            json.dump(j, open(_p(ad + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
            import arka_sira
            k = arka_sira.kuyruk()
            if ad not in k:
                arka_sira.yaz_kuyruk(k + [ad])
            olay(d, ad, f"KABUL {mal} {commit}; sonraki yon kuyrukta ({len(sonraki)} kaldi)", bildir=True)
        else:
            olay(d, ad, f"KABUL {mal} {commit}; sonraki yon yok", bildir=True)
    elif karar == "BITTI":
        olay(d, ad, f"bitti {mal} {commit}", bildir=True)
    else:
        d["karar"][ad] = f"{karar} ({neden}) {mal} {commit}"
        olay(d, ad, f"karar-bekliyor: {karar} ({neden})", bildir=True)


def olu(d, ad, j, neden):
    if d["yeniden"].get(ad, 0) < 1:
        d["yeniden"][ad] = d["yeniden"].get(ad, 0) + 1
        import arka_sira
        k = arka_sira.kuyruk()
        if ad not in k:
            arka_sira.yaz_kuyruk(k + [ad])
        olay(d, ad, f"OLDU/TAKILDI ({neden}); bir kez yeniden kuyruga alindi", bildir=True)
    else:
        d["karar"][ad] = f"oldu ({neden}); yeniden denendi, kuyruga alinmadi"
        olay(d, ad, f"OLDU ({neden}); ikinci kez kuyruga alinmadi", bildir=True)
    open(_p("gece-ozeti.md"), "a", encoding="utf-8").write(f"{time.strftime('%H:%M')} | {ad} | OLDU | $? | -\n")


def son_etkinlik(ad):
    """İşin gerçek etkinlik zamanı: .log yalnız başta/sonda yazılır; asıl iz CC oturum transkripti (~/.claude/projects/*/<oturum>.jsonl).
    Oturum bilinmiyorsa None → takıldı kararı VERİLMEZ (tahmin yok)."""
    try:
        sid = open(_p(ad + ".oturum"), encoding="utf-8").read().strip()
    except OSError:
        return None
    if not sid:
        return None
    kok = os.path.join(os.path.expanduser("~"), ".claude", "projects")
    en = None
    try:
        for kl in os.listdir(kok):
            p = os.path.join(kok, kl, sid + ".jsonl")
            if os.path.exists(p):
                t = os.path.getmtime(p)
                en = t if en is None or t > en else en
                alt = os.path.join(kok, kl, sid)
                if os.path.isdir(alt):
                    for r, _, fs in os.walk(alt):
                        for f in fs:
                            en = max(en, os.path.getmtime(os.path.join(r, f)))
    except OSError:
        return None
    return en


def tara(canli=None):
    import arka_sira
    ilk = not os.path.exists(_p("_oto.json"))  # ilk koşu: eski loglar taban çizgisi, bildirim/yeniden kuyruk yok
    d = _durum()
    canli = arka_sira.canli_isler() if canli is None else canli
    simdi = time.time()
    for f in sorted(os.listdir(ARKA)):
        if not f.endswith(".json") or f.startswith("_") or f.endswith((".mcp.json", ".eklenti.json")):
            continue
        ad = f[:-5]
        lg = _p(ad + ".log")
        if not os.path.exists(lg):
            continue
        t = open(lg, encoding="utf-8", errors="replace").read()
        m = list(re.finditer(r"^BITTI (\S+) kod (\S+)", t, re.M))
        if m and ad not in canli:
            anahtar = f"{ad}@{m[-1].group(0)}@{int(os.path.getmtime(lg))}"
            if d["islenen"].get(ad) != anahtar:
                d["islenen"][ad] = anahtar
                if ilk:
                    continue
                try:
                    degerlendir(d, ad)
                except Exception as e:
                    olay(d, ad, f"degerlendirme hatasi {type(e).__name__}", bildir=True)
        elif ad in canli and (son_etkinlik(ad) is not None) and simdi - max(os.path.getmtime(lg), son_etkinlik(ad)) > TAKILDI_SN:
            anahtar = f"takildi:{ad}@{int(son_etkinlik(ad))}"
            if d["islenen"].get(ad + "#t") != anahtar:
                d["islenen"][ad + "#t"] = anahtar
                try:
                    arka_sira.durdur(ad)
                except Exception:
                    pass
                olu(d, ad, {}, "oturum transkripti 30 dk hareketsiz")
        elif not m and ad not in canli and os.path.exists(_p(ad + ".kilit")) and '"result":"' not in t:
            anahtar = f"olu:{ad}@{int(os.path.getmtime(lg))}"
            if d["islenen"].get(ad + "#o") != anahtar:
                d["islenen"][ad + "#o"] = anahtar
                if ilk:
                    continue
                olu(d, ad, {}, "claude/ajan oldu, sonuc yok")
    import psutil
    ram = psutil.virtual_memory().percent
    if ram >= RAM_BILDIR:
        bildirim(d, "ram-" + time.strftime("%Y%m%d%H"), f"RAM %{ram:.0f} (>= {RAM_BILDIR:.0f})")
        olay(d, "RAM", f"%{ram:.0f}")
    _yaz(d)
    desktop(d)
    if not os.environ.get("ARKA_OTO_TEST"):
        try:
            import telegram_kopru
            if telegram_kopru.TOK and telegram_kopru.CHAT:
                y, c = telegram_kopru.cevapla()
                if y:
                    open(_p("_tg.log"), "a", encoding="utf-8").write(time.strftime("%d %H:%M ") + f"yeni={y} cevap={c}\n")
            else:
                open(_p("_tg.log"), "a", encoding="utf-8").write(time.strftime("%d %H:%M ") + "TOK/CHAT yok\n")
        except Exception as e:
            open(_p("_tg.log"), "a", encoding="utf-8").write(time.strftime("%d %H:%M ") + f"hata {type(e).__name__}: {str(e)[:150]}\n")


def desktop(d=None):
    d = d or _durum()
    s = ["# ARKA DURUM (otomatik, arka_oto.py) " + time.strftime("%d %b %H:%M"), "", "## Karar bekleyenler"]
    s += [f"- {a}: {n}" for a, n in d["karar"].items()] or ["- yok"]
    s += ["", "## Son 20 olay"] + ["- " + o for o in d["olaylar"][-20:]]
    open(_p("_desktop.md"), "w", encoding="utf-8").write("\n".join(s[:40]) + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--desktop":
        desktop()
    else:
        tara()
