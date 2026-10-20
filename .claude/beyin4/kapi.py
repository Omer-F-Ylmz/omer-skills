"""BEYIN-4 d2 kapı: tohum 2009+2010 (sayısal) + 2011 (sayısal olmayan, çok notlu; sorular-<tohum>.jsonl, betik üretimi), A = `beyin.py ara`, B = yalnız Read; düzenek beyin2/kapi.py.
Hakem: sayısalda BETİK (cevaptaki her sayı aday cevapta tam geçerse doğru); sayısal olmayanda iki ailenin ücretsiz bulut modeli (OmniRoute :free), iki ayrı doğruluk. Ölçü: doğruluk + API girdi token'ı A/B.
Kullanım: python .claude/beyin4/kapi.py [adım...]  (adım: A2009 B2009 A2010 B2010 A2011 B2011; varsayılan hepsi; kosu/<adım>.json varsa yeniden kullanılır)
Kabul: doğruluk ≥%92 ve token A ≤ B'nin %25."""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).parent
sys.path.insert(0, str(D.parent / "beyin2"))
import kapi  # noqa: E402

kapi.CIKTI = D / "kosu"
kapi.CIKTI.mkdir(exist_ok=True)
TOHUM = (2009, 2010, 2011, 2012, 2013, 2014, 2015)
SAYISAL = (2009, 2010, 2012, 2014)
sys.path.insert(0, str(D.parent.parent / ".kos/kopru"))
import video764_kos as V  # noqa: E402  (zincir: post/haiku/modeller yeniden kullanılır)
V.HAIKU_TAVAN = 40
# iki ayrı aile: OpenRouter :free (nvidia/google/minimax) | Groq gpt-oss (openai) → Haiku (anthropic); 429 → bekleme yok, sıradaki halka
AILE = ("openrouter", "groq-haiku")  # hakem kolları; halka seçimi _hakem_iste'de havuza bırakılır
# B kolu dizin düzenini bilsin (A arama ile bulur; Read dizin listeleyemez)
B_DUZEN = ("Dosya düzeni: ajan notları .kos/kopru/ajan-sira/<ad>.json (cevap 'result' alanında); SIRA: .kos/kopru/gorev/SIRA.md; "
           "diğer notlar .kos/kopru/{gorev,gorev-gecmis,devir}/<ad>.md, docs/ogren/<ad>.md, docs/kurulumlar/<ad>.md.\nSorular:\n")
CEVAP_B = kapi.CEVAP_B.replace("Sorular:\n", B_DUZEN)
HAKEM = ("Her satırda soru, referans (TEK doğru değer) ve aday cevap var; aday cevap birden çok parçalı olabilir ('(1) x (2) y' ya da düz metin): "
         "referans değeri adayın HERHANGİ bir yerinde doğru (ad/yol/kimlik/kelime) veriliyorsa d=1, yoksa ya da yanlışsa d=0 (yol biçimi farkı: \\ ile / aynıdır). "
         "Yalnız satır başına bir JSON yaz: {\"id\":N,\"d\":0|1}.\n")
# tek aramalı A: yeniden arama yönergesi yok; tur tavanı 12, arama bütçesi = soru sayısı
CEVAP_A = """Aşağıdaki soruları cevapla. Tek bilgi kaynağın ikinci beyin araması (Bash'te yalnız bu komut):
python tools/beyin.py ara "<soru>"
(birebir kaynak satırları + yol:satır döner; çok parçalı "(1)… (2)…" soru da TEK aramada). Soru başına TAM BİR arama, sorunun kendisiyle;
tüm aramaları İLK mesajda paralel Bash çağrılarıyla yap, sonuçlar gelince başka arama yapma, doğrudan cevapla. Başka komut (grep, cat, dosya okuma) çalıştırma.
Çıktı: YALNIZ JSONL, soru başına bir satır: {"id":…,"cevap":"kısa cevap","kaynak":"yol:satır"}
Sorular:
"""
TUR_A = "12"
S = {t: [json.loads(s) for s in (D / f"sorular-{t}.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()] for t in TOHUM}


def liste(t):
    return "\n".join(f'{q["id"]}. {q["soru"]}' for q in S[t])


def calis(ad, istem, arac=None, izin=None, tur=None):
    yol = kapi.CIKTI / f"{ad}.json"
    return json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else kapi.cagir(ad, istem, arac, izin, tur)


def dogru(q, cevap):
    return all(re.search(rf"(?<![\d.,]){re.escape(s)}(?!\d)", str(cevap)) for s in q["cevap"].split(";") if s.strip())


def llm_hakem(aile, t, cev):
    """{id: 0|1}; kosu/hakem-<aile>-<t>.json önbellek. Zincirde 429/hata/eksik yanıt → sıradaki halka (bekleme yok)."""
    yol = kapi.CIKTI / f"hakem2-{aile}-{t}.json"
    # normalize: çok parçalı referans parça parça sorulur (id*10+j); aday cevap "(1) x (2) y" biçiminde de olsa hakem tek değeri arar
    satir = [(q["id"] * 10 + j, q, p.strip()) for q in S[t] for j, p in enumerate(q["cevap"].split(";"), 1) if p.strip()]
    if yol.exists():
        d = {int(k): v for k, v in json.loads(yol.read_text(encoding="utf-8")).items()}
    else:
        istem = HAKEM + "\n".join(json.dumps({"id": i, "soru": q["soru"], "referans": p, "aday": str(cev.get(q["id"], ""))},
                                             ensure_ascii=False) for i, q, p in satir)
        d = _hakem_iste(aile, istem, {i for i, _, _ in satir})
        if d:
            yol.write_text(json.dumps(d), encoding="utf-8")
    return d and {"parca": d, "tam": {q["id"]: int(all(d.get(i, 0) for i, qq, _ in satir if qq is q)) for q in S[t]}}


def _hakem_iste(aile, istem, ids):
    tam = lambda y: None if set(int(a) for a, _ in re.findall(r'"id"\s*:\s*(\d+)\s*,\s*"d"\s*:\s*([01])', y)) >= ids else "eksik"  # noqa: E731
    y, kaynak, _ = V.HAVUZ.cagir("hakem", istem, max_tokens=2000, aile={"openrouter": "nvidia", "groq-haiku": "openai"}[aile], dogrula=tam)
    if y is None:
        return {}
    d = {int(a): int(b) for a, b in re.findall(r'"id"\s*:\s*(\d+)\s*,\s*"d"\s*:\s*([01])', y)}
    print(f"hakem {aile}: {kaynak}", file=sys.stderr)
    return d


def turlar(d):
    """Gerçek API turu: transkriptte num_turns paralel çağrıları ayrı mesaj sayar → ayrı requestId sayısı."""
    t = kapi.PROJ / f"{d.get('session_id')}.jsonl"
    return len({json.loads(x).get("requestId") for x in t.read_text(encoding="utf-8").splitlines()
                if (json.loads(x).get("message") or {}).get("role") == "assistant"}) if t.exists() else "?"


def main():
    isler = {}
    for t in TOHUM:
        isler[f"A{t}"] = (CEVAP_A + liste(t), "Bash", f"Bash({kapi.BEYIN_KOMUT}:*)", TUR_A)
        isler[f"B{t}"] = (CEVAP_B + liste(t), "Read", None, kapi.TUR)
    ad = sys.argv[1:] or list(isler)
    with ThreadPoolExecutor(6) as ex:
        sonuc = dict(zip(ad, ex.map(lambda k: calis(k, *isler[k]), ad)))
    rapor = []
    for t in TOHUM:
        for kol in "AB":
            if f"{kol}{t}" in sonuc:
                cev = {int(c.get("id")): c.get("cevap") for c in kapi.satirlar(sonuc[f"{kol}{t}"])}
                if t in SAYISAL:
                    ds = {"betik": {q["id"]: dogru(q, cev.get(q["id"], "")) for q in S[t]}}
                elif kol == "A":
                    ds = {a: llm_hakem(a, t, cev) for a in AILE}
                else:
                    continue
                for h, d in ds.items():
                    if not d:  # hakem hiç yanıt vermedi (429) → 0/20 doğruluk gibi görünmesin
                        rapor.append(f"tohum {t} {kol} hakem {h}: YOK (429)")
                        continue
                    p = d.get("parca")
                    d = d.get("tam", d)
                    rapor.append(f"tohum {t} {kol} hakem {h}: {sum(d.get(q['id'], 0) for q in S[t])}/{len(S[t])}"
                                 f" (çok {sum(d.get(q['id'], 0) for q in S[t] if q['cok'])}/{sum(q['cok'] for q in S[t])})"
                                 + (f" parça {sum(p.values())}/{len(p)}" if p else "")
                                 + f" yanlış {[q['id'] for q in S[t] if not d.get(q['id'])]}")
                if len(ds) == 2 and all(ds.values()):  # iki hakem aile uyumu (soru düzeyi)
                    x, y = (d["tam"] for d in ds.values())
                    rapor.append(f"tohum {t} {kol} hakem uyumu: {sum(x.get(q['id']) == y.get(q['id']) for q in S[t])}/{len(S[t])}")
        if f"A{t}" in sonuc and f"B{t}" in sonuc:
            a, b = sonuc[f"A{t}"], sonuc[f"B{t}"]
            rapor.append(f"tohum {t}: token A {kapi.girdi(a)} B {kapi.girdi(b)} = %{100 * kapi.girdi(a) / max(1, kapi.girdi(b)):.0f}"
                         f" tur A {a.get('num_turns')} B {b.get('num_turns')} (API turu A {turlar(a)} B {turlar(b)}) ihlal A {kapi.ihlal(a)}")
    (kapi.CIKTI / "sonuc.txt").write_text("\n".join(rapor), encoding="utf-8")
    print("\n".join(rapor))


if __name__ == "__main__":
    main()
