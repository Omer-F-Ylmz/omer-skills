"""AJAN-AKIS-1 2. beyin döngüsü: biten Opus kuyruk işinin transkriptinden iş-akışı kalıbı damıtır.
iz(jsonl) → numaralı satırlar (L<n> ARAC|HATA|KULLANICI|SON); cikar(iz, cagir) → kalıp listesi, alıntısı o satırda birebir yoksa atılır;
ekle → .kos/kopru/akis/kaliplar.jsonl; oneri → ≥2 farklı oturumda görülen kalıplar (çekirdeğe otomatik girmez, kapıdan geçince).
kanca(oturum_id, durum, model): yalnız durum=tamam + model=opus'ta bir ücretsiz çağrı yapar; hata kuyruğu bozmaz."""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
DIZIN = KOK / ".kos/kopru/akis"
ISTEM = ("Aşağıdaki numaralı iş izinden bu ajanın TEKRAR EDİLEBİLİR çalışma kalıplarını çıkar (başlama, plan, hazır kaynak arama, küçük doğrulanabilir adım, "
         "kanıt, öz-denetim, hata sonrası, DUR koşulu, araç seçimi). En çok 6 madde. Yalnız JSON dizi ver: "
         '[{"kalip": "<tek cümle kural>", "satir": <L numarası>, "alinti": "<o satırdan BİREBİR ≤60 karakter>"}]. Satırda olmayan alıntı = madde atılır.\n\n')


def _kisa(x, n=160):
    return re.sub(r"\s+", " ", x if isinstance(x, str) else json.dumps(x, ensure_ascii=False))[:n]


def iz(yol):
    """Transkript → ['L1 KULLANICI: …', 'L2 ARAC Bash: …', 'L3 HATA: …', 'L4 SON: …']; ham araç çıktısı alınmaz (yalnız hata başı)."""
    out, son = [], None
    for ham in Path(yol).read_text(encoding="utf-8").splitlines():
        try:
            o = json.loads(ham)
        except ValueError:
            continue
        m = o.get("message") or {}
        c = m.get("content")
        if o.get("type") == "user" and isinstance(c, str):
            out.append(("KULLANICI", _kisa(c, 200)))
        for b in c if isinstance(c, list) else []:
            if b.get("type") == "tool_use":
                girdi = b.get("input", {})
                out.append((f"ARAC {b.get('name')}", _kisa(girdi.get("command") or girdi.get("file_path") or girdi.get("pattern") or girdi)))
            elif b.get("type") == "tool_result" and b.get("is_error"):
                out.append(("HATA", _kisa(b.get("content", ""))))
            elif b.get("type") == "text" and o.get("type") == "assistant":
                son = _kisa(b.get("text", ""), 300)
    if son:
        out.append(("SON", son))
    return [f"L{i} {k}: {v}" for i, (k, v) in enumerate(out, 1)]


def dogrula(k, satirlar):
    try:
        n = int(k["satir"])
        return bool(k["kalip"]) and bool(k["alinti"]) and 1 <= n <= len(satirlar) and k["alinti"] in satirlar[n - 1]
    except (KeyError, TypeError, ValueError):
        return False


def secki(satirlar, n=220):
    """İstem boyu için alt küme (L numaraları korunur): ilk 3, her HATA + sonraki 2 satır, son 12, kalan boşluk eşit aralıkla."""
    if len(satirlar) <= n:
        return satirlar
    sec = set(range(3)) | set(range(len(satirlar) - 12, len(satirlar)))
    hata = [i for i, s in enumerate(satirlar) if " HATA:" in s][:30]
    for i in hata:
        sec |= {i, i + 1, i + 2}
    adim = max(1, len(satirlar) // max(1, n - len(sec)))
    sec |= set(range(0, len(satirlar), adim))
    return [satirlar[i] for i in sorted(x for x in sec if x < len(satirlar))]


def cikar(satirlar, cagir):
    metin = cagir(ISTEM + "\n".join(secki(satirlar)))
    m = re.search(r"\[.*\]", metin or "", re.S)
    try:
        adaylar = json.loads(m.group(0)) if m else []
    except ValueError:
        return []
    return [k for k in adaylar if isinstance(k, dict) and dogrula(k, satirlar)]


def ekle(k, dizin=DIZIN):
    dizin = Path(dizin)
    dizin.mkdir(parents=True, exist_ok=True)
    dosya = dizin / "kaliplar.jsonl"
    var = [json.loads(x) for x in dosya.read_text(encoding="utf-8").splitlines() if x.strip()] if dosya.exists() else []
    if any(v["kalip"] == k["kalip"] and v.get("oturum") == k.get("oturum") for v in var):
        return False
    with dosya.open("a", encoding="utf-8") as f:
        f.write(json.dumps(k, ensure_ascii=False) + "\n")
    return True


def oneri(dizin=DIZIN):
    """Haftalık çekirdek yenileme önerisi: ≥2 farklı oturumda görülen kalıplar. Çekirdeği DEĞİŞTİRMEZ."""
    dizin = Path(dizin)
    dosya = dizin / "kaliplar.jsonl"
    say = {}
    for x in dosya.read_text(encoding="utf-8").splitlines() if dosya.exists() else []:
        k = json.loads(x)
        say.setdefault(k["kalip"], set()).add(k.get("oturum"))
    adaylar = sorted(((len(v), t) for t, v in say.items() if len(v) >= 2), reverse=True)
    cikti = dizin / "oneri.md"
    cikti.write_text("# Çekirdek yenileme önerisi (otomatik uygulanmaz; Ömer/kapı onayı)\n" + "".join(f"- [{n} oturum] {t}\n" for n, t in adaylar), encoding="utf-8")
    return cikti


def oturum_bul(sid):
    for p in (Path.home() / ".claude/projects").glob(f"*/{sid}.jsonl"):
        return p
    return None


def model_cagir(istem):
    sys.path.insert(0, str(KOK / "tools"))
    import ucretsiz_havuz as H
    return H.cagir("ozet", istem, max_tokens=1500, zaman=90)[0]


def kanca(sid, durum, model, dizin=DIZIN):
    """Biten kuyruk işi: tamam + opus → kalıp damıt, beyne yaz. Başka her durumda None (çağrı yok)."""
    if durum != "tamam" or model != "opus":
        return None
    try:
        yol = oturum_bul(sid)
        if not yol:
            return None
        satirlar = iz(yol)
        return sum(ekle(dict(k, oturum=sid), dizin) for k in cikar(satirlar, model_cagir))
    except Exception:  # noqa: BLE001 — damıtma kuyruğu asla bozmaz
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "oneri":
        print(oneri())
    elif len(sys.argv) > 2:
        print(kanca(sys.argv[1], "tamam", sys.argv[2]))
