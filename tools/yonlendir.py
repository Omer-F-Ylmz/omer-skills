"""ROUTER-1 (20 Eki, "goat"): görev başı kademe + effort + doğrulama; başarısızlıkta bir kademe yukarı, her koşu kayda.
Kademeler (yonlendir-kurallar.json): T0 betik · T1 ücretsiz (ucuz_alt) · T2 Sonnet medium · T3 Sonnet high · T4 Opus medium.
Tür tabloda yoksa tek ücretsiz çağrıyla sınıflanır (≤300 jeton, birebir alıntı denetimi); o da olmazsa T3 (çoğu kod/yargı).
claude -p bayrakları model_sec'in yalın oturumundan (CLAUDE.md/skill/hook/MCP yükü yok).
  python tools/yonlendir.py sec <tur> [--boyut kucuk|orta|buyuk] [--risk a,b]   → karar (JSON)
  python tools/yonlendir.py sinifla "<görev tanımı>"                            → karar (JSON)
  python tools/yonlendir.py ozet [--gun 7] [--yaz]                              → tür başı başarı/yükseltme + kural önerisi"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model_sec  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
KURAL = Path(__file__).with_name("yonlendir-kurallar.json")
KAYIT = KOK / ".kos/kopru/yonlendir-kayit.jsonl"
SIRA = KOK / ".kos/kopru/gorev/SIRA.md"
SIRALI = ["T0", "T1", "T2", "T3", "T4"]
YUKSELTME = 2  # en fazla 2 kez +1, sonra Desktop'a SIRA satırı
# BULUT-1: yerel model yok (RAM 0). Gemini → OpenRouter :free → Groq EN SON (TPM küçük; OmniRoute UA'yı iletir, ucuz_alt.iste urllib dışı UA yollar)
T1_ZINCIR = [("omni", "gemini/gemini-3.1-flash-lite"), ("omni", "openrouter/nvidia/nemotron-3-super-120b-a12b:free"),
             ("omni", "groq/openai/gpt-oss-120b")]
HAIKU = "claude-haiku-5-5"


def kurallar():
    return json.loads(KURAL.read_text(encoding="utf-8"))


def karar(kademe, dogrulama, tur, kaynak, k=None):
    k = k or kurallar()
    return {"tur": tur, "kademe": kademe, **k["kademe"][kademe], "dogrulama": dogrulama, "kaynak": kaynak,
            "ucuz_tur": k["tur"].get(tur, {}).get("ucuz_tur")}


def sec(tur, boyut="kucuk", risk=(), k=None):
    """Tablodaki tür → kademe; büyük boyut ve riskli etiket +1 (T0 betik kalır), herhangi bir risk → full doğrulama."""
    k = k or kurallar()
    if tur not in k["tur"]:
        return None
    t = k["tur"][tur]
    i = SIRALI.index(t["kademe"])
    if i > 0:
        i = min(i + k["boyut"].get(boyut, 0) + sum(k["risk"].get(r, 0) for r in risk), len(SIRALI) - 1)
    return karar(SIRALI[i], "full" if risk else t["dogrulama"], tur, "kural", k)


def _haiku(istem, max_tokens=None):
    """Zincirin son çaresi: Haiku 5.5 yalın claude -p (OmniRoute değil). (yanıt, bitiş, model, usage, usd)"""
    import subprocess
    r = subprocess.run(["claude", "-p", "--output-format", "json", "--model", HAIKU, *model_sec.YALIN, "--safe-mode", "--tools", ""],
                       input=istem, capture_output=True, text=True, encoding="utf-8", timeout=600, creationflags=0x08000000)
    d = json.loads(r.stdout)
    u = d.get("usage", {})
    giris = sum(u.get(x) or 0 for x in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return d.get("result", ""), "stop", HAIKU, {"prompt_tokens": giris, "completion_tokens": u.get("output_tokens") or 0}, \
        d.get("total_cost_usd") or 0


def t1(istem, max_tokens=2000, sor=None, haiku=_haiku):
    """T1 zinciri: Gemini → nemotron :free → Groq → Haiku 5.5. Kota/hata/kesik → sıradaki; görev düşmez.
    Döner {yanit, model, usage{giris,cikis}, usd, sebep[], kota}; haiku=None → son çare yok (yanit None)."""
    import urllib.error
    import ucuz_alt
    g = {**ucuz_alt.govde(istem, []), "max_tokens": max_tokens}
    sebep = []
    for kol, model in T1_ZINCIR + ([("haiku", HAIKU)] if haiku else []):
        try:
            y, bitis, m, u, *usd = haiku(istem, max_tokens) if kol == "haiku" else (sor or ucuz_alt.sor)(kol, model, g)
        except urllib.error.HTTPError as e:
            sebep.append(f"{model}:{'kota' if e.code == 429 else e.code}")
            continue
        except Exception as e:  # ağ, RAM ≥%80 (atlandi-ram), bozuk yanıt
            sebep.append(f"{model}:{type(e).__name__}")
            continue
        if not y.strip() or bitis == "length":
            sebep.append(f"{model}:{'kesik' if bitis == 'length' else 'bos'}")
            continue
        return {"yanit": y, "model": m or model, "usd": usd[0] if usd else 0, "sebep": sebep,
                "kota": any(s.endswith(":kota") for s in sebep),
                "usage": {"giris": u.get("prompt_tokens") or 0, "cikis": u.get("completion_tokens") or 0}}
    return {"yanit": None, "model": None, "usd": 0, "sebep": sebep, "kota": any(s.endswith(":kota") for s in sebep),
            "usage": {"giris": 0, "cikis": 0}}


def sinifla(tanim, sor=None, k=None, haiku=_haiku):
    """Tek T1 zincir çağrısı (≤300 jeton): tür etiketi + tanımdan birebir alıntı (ucuz_alt.dogrula). Olmazsa T3/full."""
    import ucuz_alt
    k = k or kurallar()
    secenek = list(k["tur"])
    istem = (f"Görev tanımı:\n{tanim}\n\nBu görevin iş türünü seçeneklerden seç. YALNIZ JSON:\n{ucuz_alt.SEMA['etiket']}"
             f"\nSeçenekler: {' | '.join(secenek)}")
    r = t1(istem, 300, sor, haiku)
    o = ucuz_alt.json_al(r["yanit"]) if r["yanit"] else None
    neden = ucuz_alt.dogrula("etiket", o, tanim, secenek) if o else f"yanit yok ({', '.join(r['sebep'])})"
    if neden:
        return {**karar("T3", "full", None, f"varsayilan ({neden})", k), "usage": r["usage"], "t1": r}
    return {**sec(o["etiket"], k=k), "kaynak": "t1-sinif", "usage": r["usage"], "t1": r}


def yukselt(kd):
    i = SIRALI.index(kd["kademe"])
    if i + 1 >= len(SIRALI):
        return None
    return {**kd, **kurallar()["kademe"][SIRALI[i + 1]], "kademe": SIRALI[i + 1]}


def argv(kd, arac=()):
    """claude -p bayrakları (T2-T4); araçsız yalın oturum model_sec ile aynı."""
    b = ["--model", kd["model"], "--effort", kd["effort"], *model_sec.YALIN]
    if not arac:
        return b + ["--safe-mode", "--tools", ""]
    return b + ["--setting-sources", "", "--tools", ",".join(a.split("(")[0] for a in arac), "--allowedTools", *arac]


def kaydet(kd, sonuc, usage, yukseltme, ek=None):
    KAYIT.parent.mkdir(parents=True, exist_ok=True)
    s = {"tarih": time.strftime("%Y-%m-%dT%H:%M:%S"), "tur": kd["tur"], "kademe": kd["kademe"], "model": kd["model"],
         "effort": kd["effort"], "giris": usage.get("giris", 0), "cikis": usage.get("cikis", 0), "sonuc": sonuc,
         "dogrulama": kd["dogrulama"], "yukseltme": yukseltme, **(ek or {})}
    with KAYIT.open("ab") as f:  # bayt: Windows'ta CRLF'ye dönmez
        f.write((json.dumps(s, ensure_ascii=False) + "\n").encode("utf-8"))
    return s


def kos(kd, calistir, denetle, ad=""):
    """calistir(kd) → (çıktı, usage{giris,cikis}); denetle(çıktı, kd) → bool (light: mekanik; full: bir üst kademe denetçi
    — çağıran yonlendir.yukselt(kd) ile kurar). Başarısız → +1 kademe (≤2), tükenirse SIRA satırı. Döner (çıktı|None, son kd)."""
    for n in range(YUKSELTME + 1):
        cikti, u = calistir(kd)
        ok = bool(denetle(cikti, kd))
        kaydet(kd, "gecti" if ok else "kaldi", u, n, {"ad": ad} if ad else None)
        if ok:
            return cikti, kd
        if n == YUKSELTME or not (kd := yukselt(kd)):
            break
    with SIRA.open("ab") as f:
        f.write(f"- {time.strftime('%H:%M')} ROUTER-1 YÜKSELTME TÜKENDİ: {ad or kd['tur']} · son {kd['kademe']} · Desktop bakmalı\n"
                .encode("utf-8"))
    return None, kd


def satirlar():
    return [json.loads(s) for s in KAYIT.read_text(encoding="utf-8").splitlines() if s.strip()] if KAYIT.is_file() else []


def ozet(gun=7, yaz=False):
    """Haftalık: tür başı koşu/başarı/ortalama yükseltme. ≥3 koşuda yükseltme oranı ≥%50 → başlangıç +1 (--yaz uygular);
    ≥5 koşu sıfır yükseltme → '-1 ölç' önerisi (yalnız rapor; aşağı inmek ölçümle)."""
    sinir = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - gun * 86400))
    satir = [json.loads(s) for s in KAYIT.read_text(encoding="utf-8").splitlines() if s.strip()] if KAYIT.is_file() else []
    tur = {}
    for s in satir:
        if s["tarih"] >= sinir and s.get("tur") and s["yukseltme"] == 0:  # ilk deneme = görev başı bir sayım
            tur.setdefault(s["tur"], []).append(s)
    son = {(s.get("ad"), s["tur"], s["tarih"][:13]): s for s in satir if s["tarih"] >= sinir}  # görev başı son durum
    k = kurallar()
    oneri = {}
    for t, ilk in tur.items():
        kalan = sum(1 for s in ilk if s["sonuc"] == "kaldi")
        if t in k["tur"] and len(ilk) >= 3 and kalan / len(ilk) >= 0.5:
            i = SIRALI.index(k["tur"][t]["kademe"])
            if i + 1 < len(SIRALI):
                oneri[t] = SIRALI[i + 1]
        elif t in k["tur"] and len(ilk) >= 5 and kalan == 0 and k["tur"][t]["kademe"] not in ("T0", "T1"):
            oneri[t] = "-1 ölç"
    if yaz and any(v in SIRALI for v in oneri.values()):
        for t, v in oneri.items():
            if v in SIRALI:
                k["tur"][t]["kademe"] = v
        KURAL.write_bytes((json.dumps(k, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return {"tur": {t: {"kosu": len(v), "ilk_kalan": sum(1 for s in v if s["sonuc"] == "kaldi")} for t, v in tur.items()},
            "gorev_son": len(son), "oneri": oneri, "yazildi": yaz}


if __name__ == "__main__":
    a = sys.argv[1:]
    al = lambda b, v: a[a.index(b) + 1] if b in a else v
    if a[0] == "sec":
        print(json.dumps(sec(a[1], al("--boyut", "kucuk"), [r for r in al("--risk", "").split(",") if r]), ensure_ascii=False))
    elif a[0] == "sinifla":
        print(json.dumps(sinifla(a[1]), ensure_ascii=False))
    elif a[0] == "ozet":
        print(json.dumps(ozet(int(al("--gun", "7")), "--yaz" in a), ensure_ascii=False, indent=1))
