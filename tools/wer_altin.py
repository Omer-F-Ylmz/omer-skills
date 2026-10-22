"""Altın WER referansı: aynı TR reel sesleri için Groq large-v3 + Gemini + Mistral voxtral dökümü, kelime hizalı çoğunluk oyu.

Kullanım: python tools/wer_altin.py            (döküm + oy; belirsizler wer-altin/belirsiz.json)
Çıktı: .kos/kopru/wer-altin/<id>.{groq,gemini,mistral}.txt, <id>.altin.txt, ozet.json
"""
import base64
import difflib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
TMP = KOK / ".kos/kopru/wer-tmp"
ALTIN = KOK / ".kos/kopru/wer-altin"
UA = {"User-Agent": "curl/8.5.0"}
BIRLER = "sıfır bir iki üç dört beş altı yedi sekiz dokuz".split()
ONLAR = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def yazi(n):
    """0-99 → Türkçe yazı (büyük sayılar değiştirilmez; iki taraf da aynı kuralla dönüşür)."""
    if n < 10:
        return BIRLER[n]
    return (ONLAR[n // 10] + " " + (BIRLER[n % 10] if n % 10 else "")).strip()


def norm(m):
    """Küçük harf (Türkçe İ/ı doğru), noktalama atılır, 0-99 sayı → yazı."""
    m = m.replace("İ", "i").replace("I", "ı").lower().replace("i̇", "i")
    m = re.sub(r"[^\w\s]", " ", m)
    m = re.sub(r"\b\d{1,2}\b", lambda x: " " + yazi(int(x.group())) + " ", m)
    return re.sub(r"\s+", " ", m).strip()


def multipart(alanlar, dosya, ad):
    sn = "wa" + str(os.getpid())
    g = b"".join(f'--{sn}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in alanlar.items())
    g += f'--{sn}\r\nContent-Disposition: form-data; name="{ad}"; filename="a.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()
    return g + dosya + f"\r\n--{sn}--\r\n".encode(), f"multipart/form-data; boundary={sn}"


def groq(wav):
    g, ct = multipart({"model": "whisper-large-v3", "temperature": "0", "language": "tr"}, wav.read_bytes(), "file")
    r = urllib.request.Request("https://api.groq.com/openai/v1/audio/transcriptions", g,
                               {"Authorization": "Bearer " + os.environ["GROQ_API_KEY"], "Content-Type": ct, **UA})
    return json.load(urllib.request.urlopen(r, timeout=120))["text"]


def mistral(wav):
    g, ct = multipart({"model": "voxtral-mini-latest"}, wav.read_bytes(), "file")
    r = urllib.request.Request("https://api.mistral.ai/v1/audio/transcriptions", g,
                               {"Authorization": "Bearer " + os.environ["MISTRAL_API_KEY"], "Content-Type": ct, **UA})
    return json.load(urllib.request.urlopen(r, timeout=120))["text"]


GEMINI_MODELLER = ["gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-flash-latest"]


def gemini(wav):
    istek = {"contents": [{"parts": [
        {"text": "Bu Türkçe konuşmanın birebir dökümünü yaz. Yalnız söylenenleri yaz, yorum ekleme, özetleme. Sayıları söylendiği gibi yaz."},
        {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(wav.read_bytes()).decode()}}]}],
        "generationConfig": {"temperature": 0}}
    for model in GEMINI_MODELLER:  # günlük kota (429) bitince sıradaki model
        r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                   json.dumps(istek).encode(), {"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json", **UA})
        try:
            return json.load(urllib.request.urlopen(r, timeout=180))["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503) or model == GEMINI_MODELLER[-1]:
                raise


KAYNAK = {"groq": groq, "gemini": gemini, "mistral": mistral}


def span_haritasi(ref, diger):
    """groq (ref) kelime aralığı → diğer kaynağın karşılığı; yalnız farklı aralıklar."""
    return {(i1, i2): tuple(diger[j1:j2]) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ref, diger, autojunk=False).get_opcodes() if op != "equal"}


def oy(kodlar):
    ozet, belirsiz = {}, []
    hakem = ALTIN / "hakem.json"
    HAKEM = json.loads(hakem.read_text(encoding="utf-8")) if hakem.exists() else {}
    for kod in kodlar:
        t = {k: norm((ALTIN / f"{kod}.{k}.txt").read_text(encoding="utf-8")).split() for k in KAYNAK}
        ref = t["groq"]
        harita = {k: span_haritasi(ref, t[k]) for k in ("gemini", "mistral")}
        tum = sorted(set(harita["gemini"]) | set(harita["mistral"]))
        karar = {}
        for sp in tum:
            g, m = harita["gemini"].get(sp), harita["mistral"].get(sp)
            yer = tuple(ref[sp[0]:sp[1]])
            if g is not None and g == m:
                karar[sp] = g  # 2 oy (gemini+mistral) groq'a karşı
            elif g is None and m is not None or m is None and g is not None:
                karar[sp] = yer  # groq + biri aynı fikirde: groq kalır
            else:
                birlesik = {"".join(c): c for c in (yer, g or (), m or ()) if c}  # yalnız boşluk farkı: bitişik (az kelimeli) yazım
                if len(birlesik) < len({yer, g, m} - {()}):
                    karar[sp] = min(birlesik.values(), key=len)
                    continue
                if f"{kod}:{sp[0]}-{sp[1]}" in HAKEM:  # bağlamla elle/hakemle karara bağlanmış
                    karar[sp] = tuple(norm(HAKEM[f"{kod}:{sp[0]}-{sp[1]}"]).split())
                    continue
                belirsiz.append({"id": kod, "span": list(sp), "baglam": " ".join(ref[max(0, sp[0] - 6):sp[1] + 6]),
                                 "groq": " ".join(yer), "gemini": " ".join(g), "mistral": " ".join(m)})
                karar[sp] = g or yer  # üç yönlü ayrışma: Groq kelime keser, Gemini bağlamı en iyi tutar → Gemini
        (ALTIN / f"{kod}.karar.json").write_text(json.dumps({f"{a}-{b}": list(v) for (a, b), v in karar.items()}, ensure_ascii=False), encoding="utf-8")
        ozet[kod] = {"kelime": len(ref), "oylanan": len(tum), "belirsiz": sum(1 for b in belirsiz if b["id"] == kod)}
        cikti, i = [], 0
        for sp in sorted(karar):
            if sp[0] < i:
                continue
            cikti += ref[i:sp[0]] + list(karar[sp])
            i = sp[1]
        (ALTIN / f"{kod}.altin.txt").write_text(" ".join(cikti + ref[i:]), encoding="utf-8")
    return ozet, belirsiz


def main():
    ALTIN.mkdir(parents=True, exist_ok=True)
    kodlar = sorted(p.stem[:-2] for p in TMP.glob("*_0.dil") if p.read_text().lower() == "turkish")
    for kod in kodlar:
        for k, f in KAYNAK.items():
            yol = ALTIN / f"{kod}.{k}.txt"
            if not yol.exists():
                try:
                    yol.write_text(f(TMP / f"{kod}_0.wav"), encoding="utf-8")
                except urllib.error.HTTPError as e:
                    sys.exit(f"{kod} {k} HTTP {e.code}: {e.read()[:300]}")
                print(kod, k, "ok", flush=True)
    ozet, belirsiz = oy(kodlar)
    (ALTIN / "belirsiz.json").write_text(json.dumps(belirsiz, ensure_ascii=False, indent=1), encoding="utf-8")
    top = sum(o["kelime"] for o in ozet.values())
    print(json.dumps({"klip": len(ozet), "kelime": top, "belirsiz": len(belirsiz), "oran": round(len(belirsiz) / top, 4)}))


if __name__ == "__main__":
    sys.exit(main())
