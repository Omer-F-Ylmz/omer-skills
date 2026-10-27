"""KONSOL-GECIS-2: biten ajan raporunu okuyup KABUL/DUR ön-değerlendirmesi yapar (≤5 satır).
Önce ücretsiz havuz; yalnız başarısız/boş/biçimsiz ise Console kredisi (haiku, ANTHROPIC_API_KEY_AJAN). Anahtar hiçbir yere yazılmaz.
Kullanım: python -I tools/kontrol_onoku.py <iş-adı> [görev.md]"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
K = KOK / ".kos/kopru"
sys.path[:0] = [str(KOK / "tools"), str(K)]
import maliyet_defter  # noqa: E402
import ucretsiz_havuz  # noqa: E402

MODEL = "claude-haiku-5-5"
FIYAT = (1.0, 5.0)  # shortcut: haiku $/Mtok girdi/çıktı varsayımı (cache okuma 0.1x yok sayılır → ihtiyatlı); fiyat değişirse güncelle
CAGRI_TAVAN, GUN_TAVAN, MAX_CIKTI = 0.01, 1.0, 300
LOG = K / "kontrol_onoku.log"
SISTEM = ("Sen bir kontrol ajanısın. Verilen KABUL ölçütüne göre ajan raporunu değerlendir. En fazla 5 satır yaz: "
          "ilk satır yalnız KABUL ya da DUR, sonrasında kısa gerekçe (kanıt eksikse DUR).")


def log(*a):
    s = time.strftime("%Y-%m-%d %H:%M:%S ") + " ".join(map(str, a))
    print(s, flush=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(s + "\n")


def sonuc_metni(ad):
    """sonuc json'unun (son satır) result alanı, ≤1400 karakter."""
    satirlar = (K / "ajan-sira" / f"{ad}.json").read_text(encoding="utf-8").strip().splitlines()
    return (json.loads(satirlar[-1]).get("result") or "")[:1400]


def kabul_satiri(gorev):
    m = re.search(r"^KABUL.*$", Path(gorev).read_text(encoding="utf-8"), re.M)
    return m.group(0)[:600] if m else ""


def dogrula(m):
    return None if re.match(r"\s*(KABUL|DUR)\b", m, re.I) else "biçim"


def anahtar():
    """ANTHROPIC_API_KEY_AJAN: ortam, yoksa HKCU. Değer hiçbir çıktıya yazılmaz."""
    if os.environ.get("ANTHROPIC_API_KEY_AJAN"):
        return os.environ["ANTHROPIC_API_KEY_AJAN"]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, "ANTHROPIC_API_KEY_AJAN")[0]
    except (ImportError, OSError):
        return None


def konsol(ad, istem):
    """Console çağrısı (tek mesaj). Çağrı başı ≤$0.01, günlük ≤$1; aşılırsa/anahtar yoksa None."""
    k = anahtar()
    if not k:
        log("KONSOL-YOK", ad, "anahtar yok → kredi kullanılmadı")
        return None
    tahmin = len(istem) / 3 * FIYAT[0] / 1e6 + MAX_CIKTI * FIYAT[1] / 1e6
    bugun = maliyet_defter.konsol_harcama(maliyet_defter.oku(), time.strftime("%Y-%m-%d"), model="haiku-kontrol")  # iş ajanı satırları kontrol tavanına sayılmaz
    if tahmin > CAGRI_TAVAN or bugun + tahmin > GUN_TAVAN:
        log("KONSOL-TAVAN", ad, f"tahmin ${tahmin:.4f} · bugün ${bugun:.2f} → çağrı yapılmadı")
        return None
    govde = {"model": MODEL, "max_tokens": MAX_CIKTI, "system": [{"type": "text", "text": SISTEM, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": istem}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(govde).encode(), method="POST",
                                 headers={"x-api-key": k, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            j = json.load(r)
    except (urllib.error.URLError, OSError, ValueError) as e:
        log("KONSOL-HATA", ad, getattr(e, "code", type(e).__name__))  # gövde/başlık yazılmaz
        return None
    u = j.get("usage") or {}
    girdi = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    usd = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)) * FIYAT[0] / 1e6 + u.get("cache_read_input_tokens", 0) * FIYAT[0] * 0.1 / 1e6 \
        + u.get("output_tokens", 0) * FIYAT[1] / 1e6
    maliyet_defter.yaz(ad, "haiku-kontrol", usd, True, kaynak="konsol", cache=u.get("cache_read_input_tokens", 0) / girdi if girdi else 0)
    log(f"KONSOL ${usd:.4f}", ad)
    return "".join(b.get("text", "") for b in j.get("content", [])).strip()


def kontrol(ad, gorev):
    """(karar metni | None, kaynak). Ücretsiz yol önce; boş/biçimsiz/başarısız → Console."""
    istem = f"KABUL ölçütü: {kabul_satiri(gorev)}\n\nAjan raporu ({ad}):\n{sonuc_metni(ad)}"
    try:
        m, kaynak, hlog = ucretsiz_havuz.cagir("ozet", SISTEM + "\n\n" + istem, max_tokens=MAX_CIKTI, dogrula=dogrula, etiket="kontrol")
    except Exception as e:  # havuz kurulu/ulaşılır değilse de kredi yolu denenir
        m, kaynak, hlog = None, None, [type(e).__name__]
    if m and not dogrula(m):
        log("ÜCRETSİZ", ad, kaynak)
        return "\n".join(m.strip().splitlines()[:5]), f"ucretsiz/{kaynak}"
    log("ÜCRETSİZ-BAŞARISIZ", ad, ";".join(map(str, hlog))[:200], "→ krediye düşülüyor")
    m = konsol(ad, istem)
    return ("\n".join(m.splitlines()[:5]), "konsol") if m and not dogrula(m) else (None, None)


if __name__ == "__main__":
    ad = sys.argv[1]
    karar, kaynak = kontrol(ad, sys.argv[2] if len(sys.argv) > 2 else K / f"gorev-{ad}.md")
    print(f"[{kaynak}] {karar}" if karar else "KONTROL-BOŞ")
