"""OMNIROUTE-2 pilot: herkese açık IG transkript özeti — Claude tabanı (plan, claude -p) vs OmniRoute combo cc-yedek-dis (d4: Ömer istemi; 'ucretsiz' etiketi bu yolu anar, ilk adımı OpenRouter ücretli).
  python .claude/omniroute1/pilot.py [--kuru]
Tavan: en fazla 20 ücretsiz HTTP + 20 Claude + 4 Opus yargı çağrısı + 1 Jev batch (en_fazla=2). Ara sonuç önbellekte; yeniden koşu ödenmiş çağrıyı tekrarlamaz.
Kayıt: docs/kutuphane/olcum/omniroute-2-ig-ozet.tsv. Anahtar değerleri basılmaz; claude çocuğuna ANTHROPIC_API_KEY verilmez (kredi kapalı)."""
import ctypes, json, math, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "jev"), str(KOK / "tools" / "olcum")]
CACHE = Path("C:/Projeler/.video-cache")
OB = Path(__file__).with_name("pilot-ob.jsonl")
COMBO = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--combo=")), "cc-yedek-dis")  # d2: --combo=ucretsiz-ozet
EFOR = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--efor=")), "none")  # d3: düşünme bütçesi
YOL, EK = ("ucretsiz", "") if COMBO == "cc-yedek-dis" else (COMBO + ("" if EFOR == "none" else "-" + EFOR),) * 2  # varsayılan = d4 önbellek anahtarları
EK = EK and ":" + EK
TSV = KOK / f"docs/kutuphane/olcum/omniroute-2-ig-ozet{EK.replace(':', '-')}.tsv"
CLAUDE = "C:/Users/pc/.local/bin/claude.exe"
N, OPUS_TAVAN = 20, 4
ISTEM = ("Aşağıda herkese açık bir Instagram videosunun konuşma transkripti var. Türkçe, 3-5 maddelik kısa bir özet yaz: "
         "videonun ana iddiası/konusu, verilen somut araç-yöntem-sayılar, varsa çağrı. Uydurma ekleme; yalnız özet maddelerini yaz.\n\n")
KABUL = "3-5 madde, Türkçe; transkriptteki ana konu ve somut öğeleri doğru verir; transkriptte olmayan bilgi eklemez."


def ram():
    class M(ctypes.Structure):
        _fields_ = [("l", ctypes.c_ulong), ("yuk", ctypes.c_ulong)] + [(f"x{i}", ctypes.c_ulonglong) for i in range(7)]
    m = M(); m.l = ctypes.sizeof(M); ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.yuk


def ram_bekle():  # DEVAM-KURALI: ≥%88 yeni süreç açma
    while ram() >= 88:
        print("RAM", ram(), "bekle", flush=True); time.sleep(60)


def ornekler():
    aday = []
    for d in sorted(CACHE.glob("ig-*")):
        g = d / "groq.txt"
        if g.exists():
            metin = " ".join(s.split("\t", 1)[-1].strip() for s in g.read_text(encoding="utf-8").splitlines() if s.strip())
            if 50 <= len(metin.split()) <= 300:
                aday.append((d.name, metin))
    adim = len(aday) / N  # deterministik, eşit aralıklı
    return [aday[int(i * adim)] for i in range(N)]


def env_oku(ad):
    if os.environ.get(ad):
        return os.environ[ad]
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, ad)[0]
    except OSError:
        return None


def ucretsiz(istem):
    q = urllib.request.Request("http://127.0.0.1:20128/v1/chat/completions", method="POST",
                               # d3: 600 jetonun ~570'i düşünmeye gidiyordu (finish_reason=length) → düşünme kapalı + pay
                               data=json.dumps({"model": COMBO, "messages": [{"role": "user", "content": istem}], "max_tokens": 2000,
                                                "reasoning_effort": EFOR}).encode(),
                               headers={"content-type": "application/json", "authorization": f"Bearer {env_oku('OMNIROUTE_KEY')}"})
    t = time.time()
    try:
        j = json.load(urllib.request.urlopen(q, timeout=120))
        return {"yanit": j["choices"][0]["message"]["content"] or "", "model": j.get("model", "?"), "ms": int((time.time() - t) * 1000),
                "bitis": j["choices"][0].get("finish_reason"), "usage": j.get("usage")}
    except Exception as e:  # anahtar hata metnine girmez (yalnız tür + HTTP kodu)
        return {"yanit": "", "model": "-", "ms": int((time.time() - t) * 1000), "hata": f"{type(e).__name__} {getattr(e, 'code', '')}".strip()}


def claude(istem, model):
    ram_bekle()
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY" and not re.match(r"CLAUDECODE|CLAUDE_CODE_(CHILD|MESSAGING|SESSION|ENTRYPOINT|EXECPATH)|CLAUDE_PID", k)}
    t = time.time()
    p = subprocess.run([CLAUDE, "-p", "--output-format", "json", "--model", model, "--disable-slash-commands", "--strict-mcp-config",
                        "--mcp-config", '{"mcpServers":{}}'], input=istem, env=env, capture_output=True, text=True, encoding="utf-8",
                       timeout=300, creationflags=0x08000000)
    try:
        j = json.loads(p.stdout)
    except ValueError:
        return {"yanit": "", "model": model, "ms": int((time.time() - t) * 1000), "hata": "json-degil " + (p.stdout + p.stderr)[:120].replace("\n", " ")}
    r = {"yanit": "" if j.get("is_error") else str(j.get("result", "")), "model": ",".join(j.get("modelUsage", {})) or model, "ms": j.get("duration_ms", 0)}
    if j.get("is_error") or re.search(r"usage limit|limit reached|resets? at", r["yanit"], re.I):  # plan limiti düz metin gelir
        r.update(yanit="", hata="limit/hata " + str(j.get("result", ""))[:120])
    return r


def basari(y):
    maddeler = [s for s in y.splitlines() if re.match(r"\s*([-*•]|\d+[.)])\s+\S", s)]
    return int(3 <= len(maddeler) <= 6)


def opus_yargila(parca):
    metin = "Her öğe için özeti, kabul ölçütüne göre 0-10 puanla. Yalnız satır başına `<id> <puan>` yaz.\nKabul: " + KABUL + "\n\n"
    metin += "\n\n".join(f"### id={i}\nTRANSKRİPT: {s['gorev'][len(ISTEM):]}\nÖZET:\n{s['yanit']}" for i, s in parca)
    r = claude(metin, "opus")
    return {int(a): float(b) for a, b in re.findall(r"^\s*(\d+)\s+(\d+(?:\.\d+)?)", r["yanit"], re.M)}, r.get("hata")


def main(kuru=False):
    ob = {json.loads(s)["anahtar"]: json.loads(s) for s in OB.read_text(encoding="utf-8").splitlines()} if OB.exists() else {}
    def kayit(a, v):
        ob[a] = {"anahtar": a, **v}
        with OB.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ob[a], ensure_ascii=False) + "\n")
    orn = ornekler()
    print(len(orn), "örnek", [len(m.split()) for _, m in orn], flush=True)
    if kuru:
        return
    satir = []
    for ad, metin in orn:
        for yol, f in ((YOL, lambda i: ucretsiz(i)), ("claude", lambda i: claude(i, "sonnet"))):
            a = f"{yol}:{ad}"
            if a not in ob or ob[a].get("hata"):
                kayit(a, f(ISTEM + metin))
                print(a, ob[a]["model"], ob[a]["ms"], ob[a].get("bitis", ""), ob[a].get("hata", ""), flush=True)
            if yol == "claude" and ob[a].get("hata", "").startswith("limit"):
                sys.exit("plan limiti — dur; önbellek korunur")
            satir.append({"ad": ad, "kelime": len(metin.split()), "yol": yol, "gorev": ISTEM + metin, **ob[a]})
    # Ölçümde düşüş yok: ücretsiz hata = boş yanıt (düşük puan + hata sütunu); canlı mekanizmada hata → Claude'a düşer.
    for s in satir:
        s["basari"] = basari(s["yanit"])
    if "jev" + EK not in ob:
        from jev.cekirdek import Tasiyici
        from jev_yargic import SORU, yargila
        t = Tasiyici(en_fazla=2, istek_tavan=60)
        c = yargila([{"gorev": s["gorev"], "kabul": KABUL, "yanit": s["yanit"] or "(boş)"} for s in satir], SORU, t)
        kayit("jev" + EK, {"puan": [None if x is None else round(x["kalite"]["score"] * 2, 1) for x in c],
                      "usd": sum(u.get("cost") or 0 for u in t.kullanim), "cagri": t.cagri})
    from jev_yargic import belirsiz
    jev = ob["jev" + EK]["puan"]
    sec = belirsiz(jev)[:2 * OPUS_TAVAN]
    if "opus" + EK not in ob:
        puan, hatalar = {}, []
        for k in range(0, len(sec), 2):
            p, h = opus_yargila([(i, satir[i]) for i in sec[k:k + 2]])
            puan.update(p); hatalar.append(h)
        kayit("opus" + EK, {"puan": {str(k): v for k, v in puan.items()}, "hata": [h for h in hatalar if h]})
    opus = {int(k): v for k, v in ob["opus" + EK]["puan"].items()}
    TSV.parent.mkdir(parents=True, exist_ok=True)
    with TSV.open("w", encoding="utf-8", newline="") as f:
        f.write("ornek\tkelime\tyol\tmodel\tsure_ms\tbasari\tjev\topus\tkarma\thata\tbitis\n")
        for i, s in enumerate(satir):
            s["karma"] = opus.get(i, jev[i])
            f.write(f"{s['ad']}\t{s['kelime']}\t{s['yol']}\t{s['model']}\t{s['ms']}\t{s['basari']}\t{jev[i]}\t{opus.get(i, '')}\t{s['karma']}\t{s.get('hata', '')}\t{s.get('bitis', '')}\n")
    for yol in ("claude", YOL):
        k = [s for s in satir if s["yol"] == yol]
        km = [s["karma"] for s in k if s["karma"] is not None]
        print(f"{yol}: karma ort {sum(km) / max(len(km), 1):.2f} (n={len(km)}) · başarı {sum(s['basari'] for s in k)}/{len(k)} · "
              f"hata {sum(1 for s in k if s.get('hata'))} · medyan ms {sorted(s['ms'] for s in k)[len(k) // 2]}")
    print("jev usd", ob["jev" + EK]["usd"], "· opus yargılanan", len(opus), "· opus hata", ob["opus" + EK]["hata"])
    print("sunan model:", dict(__import__("collections").Counter(s["model"] for s in satir if s["yol"] == YOL)))


if __name__ == "__main__":
    main("--kuru" in sys.argv)
