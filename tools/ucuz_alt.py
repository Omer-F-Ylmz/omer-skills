"""TOKEN-2 K8 + OMNİ-AYIR: ucuz alt adım — küçük yan işi (özet · lisans · etiket · görsel) YALNIZ ücretsiz modele yaptırır.
Claude oturumu ham metni okumaz: bağlam dosyaları burada birleşir, yanıt dosyaya yazılır, stdout'a yalnız yol + model + jeton.
Zincir: tür başı ölçülmüş :free sırası → combo cc-ucuz-free. Her yanıt doğrulanır (JSON şema · bağlamdan birebir alıntı ·
boş/"belirsiz" ret); geçmezse sonraki model, hepsi geçmezse çıkış 5 (bekle ve yeniden dene; Claude'a düşülmez). Ücretli modele ASLA yükselmez:
model adı :free / ollama yerel değilse çağrı reddedilir, yanıttaki model de denetlenir. Limit yedeği cc-yedek-dis (omniroute.mjs) ayrı.
Anahtar OMNIROUTE_KEY (env ya da HKCU) hiçbir çıktıya yazılmaz.
  python tools/ucuz_alt.py [--tur ozet|lisans|etiket|gorsel] [--secenek a,b,c] <istem.md|istem metni> <cikti.md> [bağlam...]
Kesik (finish=length) / 429 / zaman aşımı → sonraki model (429 alan model soguma.json ile paralel süreçlerce de atlanır).
Çıkış: 0 doğrulandı · 1 hata · 3 taslak (çıktı yazıldı, doğrulama çağıranda) · 4 ücretli model reddi · 5 hiçbir ücretsiz yol yanıtlamadı (bekle)."""
import base64
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

import psutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nihai_ozet

URL = "http://127.0.0.1:20128/v1/chat/completions"
OLLAMA = "http://127.0.0.1:11434/api/chat"
COMBO = "cc-ucuz-free"  # yalnız :free üyeler; güçlü limit yedeği cc-yedek-dis'e (cc-kopru/omniroute.mjs) dokunulmaz
SURUM = "v3"  # istem/şema değişince artır: hem yerel hem OmniRoute önbelleği eski yanıtı döndürmez
TAVAN = 400_000  # bağlam karakteri; combo'daki en küçük pencereye sığsın
DB = os.path.expanduser("~/.omniroute/storage.sqlite")
DIZIN = Path(__file__).resolve().parents[1] / ".kos/kopru/ucuz-onbellek"
# OMNİ-AYIR ölçümü (docs/ogren/token.md "Ücretsiz yol"); Groq gpt-oss üç ailede red (OMNIROUTE-2) → zincirde yok
# UCRETSIZ-HAVUZ-1: ("havuz", tür) = tools/ucretsiz_havuz (tüm sağlayıcılar, yük dağıtımlı); art arda üç halka = ret'te başka sağlayıcıya geçiş
HAVUZ = [("havuz", "ozet"), ("havuz", "hakem"), ("havuz", "yazim"), ("omni", COMBO), ("ollama", "qwen3.5:9b")]  # son halka yerel (RAM ≥%80 atlar)
ZINCIR = {"ozet": HAVUZ, "lisans": HAVUZ, "etiket": HAVUZ,
          "gorsel": [("omni", "openrouter/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free")]}
TASLAK = {"etiket", "gorsel", "ozet"}  # kapı ≥%98'e ulaşmayan türler: çıktı yazılır ama çıkış 3 (Claude doğrular); ozet kör hakem 78/84
SEMA = {"ozet": '{"ozet": "<istenen özet>", "alinti": ["özeti destekleyen, bağlamdan BİREBİR 1-3 alıntı, her biri ≤200 karakter"]}',
        "lisans": '{"lisans": "SPDX kimliği (MIT, Apache-2.0, GPL-3.0 …) ya da yok", "alinti": "lisansı gösteren BİREBİR alıntı ≤200 karakter"}',
        "etiket": '{"etiket": "<seçeneklerden biri>", "alinti": "etiketi destekleyen BİREBİR alıntı ≤200 karakter"}',
        "gorsel": '{"metin": "görseldeki metin (yoksa boş)", "hukum": "<istenen yargı>"}'}


def anahtar():
    if os.environ.get("OMNIROUTE_KEY"):
        return os.environ["OMNIROUTE_KEY"]
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        return winreg.QueryValueEx(k, "OMNIROUTE_KEY")[0]


def combo_uyeleri():
    try:
        c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
        r = c.execute("select data from combos where name=?", (COMBO,)).fetchone()
        return [m["model"] if isinstance(m, dict) else m for m in json.loads(r[0])["models"]] if r else []
    except (sqlite3.Error, KeyError, ValueError):
        return []


def ucretsiz(kol, model):
    """izin listesi: ollama yerel ya da :free; combo yalnız bütün üyeleri :free ise (katalog değişse bile ücretliye düşemez)"""
    if kol in ("ollama", "havuz"):
        return True
    if model == COMBO:
        u = combo_uyeleri()
        return bool(u) and all(m.endswith(":free") for m in u)
    return model.endswith(":free")


def govde(istem, dosyalar, model=COMBO):
    ek = "".join(f'\n\n<dosya yol="{Path(d).as_posix()}">\n{Path(d).read_text(encoding="utf-8", errors="ignore")}\n</dosya>'
                 for d in dosyalar)
    if len(istem) + len(ek) > TAVAN:
        raise ValueError(f"bağlam {len(istem) + len(ek)} karakter > {TAVAN}; dosyaları böl")
    # düşünme en az: "none" combo'da 400 (TOKEN-2 d3); düşünme jetonu çıktıyı yemesin diye 8000 (rtk-desktop kesiği, ÖĞREN-1 d4)
    return {"model": model, "messages": [{"role": "user", "content": istem + ek}], "max_tokens": 8000,
            "reasoning_effort": "low", "temperature": 0}


def iste(g, zaman=300):
    if g["model"] == COMBO and not ucretsiz("omni", COMBO):
        raise PermissionError(f"{COMBO} üyelerinde :free olmayan model")
    q = urllib.request.Request(URL, method="POST", data=json.dumps(g).encode(), headers={
        "content-type": "application/json", "authorization": f"Bearer {anahtar()}",
        "user-agent": "omer-skills-ucuz-alt/1"})  # Python-urllib UA'sı Groq'ta 403
    return json.load(urllib.request.urlopen(q, timeout=zaman))


def sor(kol, model, g):
    """(içerik, bitiş, yanıt modeli, usage); ollama /api/chat think:false (ÖĞREN-1 d6: /v1 düşünmeyle 4096'yı yiyordu)"""
    if kol == "havuz":
        sys.path.insert(0, str(Path(__file__).parent)); import ucretsiz_havuz
        y, k, log = ucretsiz_havuz.cagir(model, g["messages"][0]["content"], max_tokens=min(g["max_tokens"], 4000))
        if y is None:
            raise RuntimeError("havuz boş " + ",".join(log)[:120])
        return y, "stop", k, {}
    if kol == "omni":
        j = iste({**g, "model": model})
        c = j["choices"][0]
        return c["message"].get("content") or "", c.get("finish_reason"), j.get("model") or "", j.get("usage") or {}
    if (Path(__file__).resolve().parents[1] / ".kos" / "yerel-model.kapali").exists():  # HAVUZ-GENIS-2: yerel KAPALI bayrağı
        raise RuntimeError("atlandi-yerel-kapali")
    if psutil.virtual_memory().percent >= 80:  # ÖĞREN-1 ★ 05:48: RAM ≥%80 → ollama yok, sonraki kol
        raise RuntimeError("atlandi-ram")
    q = urllib.request.Request(OLLAMA, method="POST", headers={"content-type": "application/json"}, data=json.dumps(
        {"model": model, "think": False, "stream": False, "keep_alive": 0, "options": {"num_ctx": 8192, "temperature": 0},
         "messages": g["messages"]}).encode())
    j = json.load(urllib.request.urlopen(q, timeout=300))
    return j["message"].get("content") or "", j.get("done_reason"), model, {
        "prompt_tokens": j.get("prompt_eval_count"), "completion_tokens": j.get("eval_count")}


def n(s):
    return " ".join(re.sub(r"[\"'`*_‘’“”]", "", str(s)).split()).lower()


def bos(v):
    return not str(v).strip() or n(v).startswith("belirsiz")


def json_al(y):
    i, j = y.find("{"), y.rfind("}")
    try:
        return json.loads(y[i:j + 1]) if 0 <= i < j else None  # "substring not found" yerine None → ret
    except ValueError:  # parantezli ama bozuk JSON da ret → sonraki model (O12)
        return None


def dogrula(tur, o, baglam, secenek):
    """ret nedeni ya da None. Alıntı normalize edilmiş bağlamın alt dizesi olmalı (uydurma kilidi)."""
    if not isinstance(o, dict):
        return "JSON yok"
    nb = n(baglam)
    alinti = o.get("alinti")
    alintilar = alinti if isinstance(alinti, list) else [alinti] if isinstance(alinti, str) else []
    if tur == "gorsel":
        return "hüküm boş" if bos(o.get("hukum", "")) else None
    alan = {"ozet": "ozet", "lisans": "lisans", "etiket": "etiket"}[tur]
    if bos(o.get(alan, "")):
        return f"{alan} boş/belirsiz"
    if tur == "lisans" and n(o["lisans"]) in ("yok", "none"):
        return "lisans yok dedi ama bağlamda lisans geçiyor" if re.search(r"licen[cs]e|lisans", nb) else None
    if tur == "etiket" and secenek and n(o["etiket"]) not in {n(s) for s in secenek}:
        return "etiket seçeneklerde yok"
    if not alintilar or any(len(n(a)) < 10 or n(a) not in nb for a in alintilar):
        return "alıntı bağlamda birebir yok"
    if tur == "lisans" and not any(t in n(" ".join(alintilar)) for t in re.findall(r"[a-z]{3,}", n(o["lisans"]))):
        return "lisans adı alıntıda geçmiyor"
    return None


def soguma(model, sure=None):
    """429 alan modeli paralel süreçler de atlar. shortcut: dosya yarışı son yazanı tutar, sık paralelde kilit gerekir"""
    f = DIZIN / "soguma.json"
    d = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
    if sure is None:
        return d.get(model, 0) > time.time()
    d[model] = time.time() + sure
    f.write_text(json.dumps(d), encoding="utf-8")


def anahtar_ozet(tur, secenek, g):
    return hashlib.sha256(json.dumps([SURUM, tur, list(secenek), g["messages"], g["max_tokens"], g["reasoning_effort"], ZINCIR[tur]],
                                     ensure_ascii=False).encode()).hexdigest()[:24]


def coz(tur, istem, dosyalar, secenek=(), gorsel=None):
    """(sonuç dict | None, model, deneme sayısı, usage, ücretli_red). Önbellek: tür+istem+bağlam+zincir özeti."""
    baglam = istem + "".join(Path(d).read_text(encoding="utf-8", errors="ignore") for d in dosyalar)
    tam = f"{istem}\n\nYALNIZ şu JSON nesnesini döndür (Türkçe, uydurma yok):\n{SEMA[tur]}"
    if secenek:
        tam += f"\nSeçenekler: {' | '.join(secenek)}"
    g = govde(tam, dosyalar)
    # OmniRoute yanıt önbelleği max_tokens/reasoning'i anahtara katmaz: ayar değişince eski (kesik) yanıt dönmesin diye istemde etiket
    g["messages"][0]["content"] = f"[ucuz_alt {SURUM} mt{g['max_tokens']} {g['reasoning_effort']}]\n" + nihai_ozet.OZET + g["messages"][0]["content"]  # NİHAİ-KAPI-1
    if gorsel:
        g["messages"][0]["content"] = [{"type": "text", "text": g["messages"][0]["content"]}, {"type": "image_url", "image_url": {
            "url": "data:image/png;base64," + base64.b64encode(Path(gorsel).read_bytes()).decode()}}]
    DIZIN.mkdir(parents=True, exist_ok=True)
    onb = DIZIN / f"{anahtar_ozet(tur, secenek, g)}.json"
    if onb.is_file():
        k = json.loads(onb.read_text(encoding="utf-8"))
        return k["sonuc"], k["model"] + " (önbellek)", 0, {}, False
    deneme, red = 0, False
    for kol, model in ZINCIR[tur]:
        if not ucretsiz(kol, model):
            red = True
            continue
        if soguma(model):
            continue
        deneme += 1
        try:
            y, bitis, ymodel, u = sor(kol, model, g)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                soguma(model, min(int(e.headers.get("retry-after") or 60), 600))
            print(f"  {model} HTTP {e.code}", file=sys.stderr)
            continue
        except (OSError, ValueError, KeyError) as e:  # zaman aşımı, bağlantı, bozuk gövde → sonraki model
            print(f"  {model} {type(e).__name__}", file=sys.stderr)
            continue
        except RuntimeError as e:  # atlandi-ram → sonraki model
            print(f"  {model} {e}", file=sys.stderr)
            continue
        # OpenRouter yanıt modelinde :free son eki düşebilir; ad istenen/combo :free üyesiyle eşleşmeli
        if kol == "omni" and ymodel.split("/")[-1].removesuffix(":free") not in {
                m.split("/")[-1].removesuffix(":free") for m in combo_uyeleri() + [model] if m.endswith(":free")}:
            red = True  # yanıt ücretli modelden geldi: çıktı kullanılmaz
            print(f"  {model} → {ymodel} ÜCRETLİ RED", file=sys.stderr)
            continue
        if bitis == "length":
            print(f"  {model} kesik", file=sys.stderr)
            continue
        o = json_al(y)
        neden = dogrula(tur, o, baglam, secenek)
        if neden:
            print(f"  {model} RET {neden}", file=sys.stderr)
            continue
        onb.write_text(json.dumps({"sonuc": o, "model": ymodel}, ensure_ascii=False), encoding="utf-8")
        return o, ymodel, deneme, u, red
    return None, None, deneme, {}, red


def main(argv):
    tur, secenek, gorsel = "ozet", (), None
    while argv and argv[0].startswith("--"):
        bayrak, deger, *argv = argv
        if bayrak == "--tur":
            tur = deger
        elif bayrak == "--secenek":
            secenek = tuple(s.strip() for s in deger.split(",") if s.strip())
        elif bayrak == "--gorsel":
            tur, gorsel = "gorsel", deger
    istem, cikti, *dosyalar = argv
    istem = Path(istem).read_text(encoding="utf-8") if Path(istem).is_file() else istem  # kisa.py istemi metin verir
    t = time.time()
    try:
        o, model, deneme, u, red = coz(tur, istem, dosyalar, secenek, gorsel)
    except Exception as e:  # anahtar hata metnine girmez (yalnız tür + HTTP kodu)
        print(f"HATA {type(e).__name__} {getattr(e, 'code', '')}".strip())
        return 1
    if o is None:
        print(f"ÇEKİŞMELİ {tur} · {deneme} deneme · BEKLE (ücretsiz → yerel doldu; yeniden dene){' · ÜCRETLİ RED' if red else ''} · {time.time() - t:.0f} sn")
        return 4 if red and not deneme else 5
    Path(cikti).write_text(str(o["ozet"]) if tur == "ozet" else json.dumps(o, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{cikti} · {tur} · model {model} · deneme {deneme} · girdi {u.get('prompt_tokens')} çıktı {u.get('completion_tokens')} · "
          f"{time.time() - t:.0f} sn{' · TASLAK: Claude doğrular' if tur in TASLAK else ''}")
    return 3 if tur in TASLAK else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
