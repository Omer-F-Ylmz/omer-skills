"""EGITIM-1 arac kapisi: Claude disi (ucretsiz havuz) modelin OpenAI-uyumlu tool calling ile bizim aracları — kombin_sec · katalog_ara · dosya_oku · ara —
kullanmasi. Hepsi SALT OKUNUR: yazma/ag/kabuk yok; yol KOK icinde, gizli dosya adlari reddedilir, cikti kirpilir.
python tools/ogret/arac_kapi.py "<gorev>"  → son yanit + hangi araclar cagrildi.   import: arac_kapi.kos(gorev) -> (metin, model, cagrilar)"""
import json, re, subprocess, sys, urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ucretsiz_havuz as H  # noqa: E402

TOOLS_PROV = ("gemini", "groq", "mistral", "openrouter")  # tool calling bilen uclar
GIZLI = re.compile(r"(?i)\.env|secret|credential|\.pem|\.key$|id_rsa|token|\.git[/\\]")
KIRP = 3000


def _p(**ozellik):
    return {"type": "object", "properties": {k: {"type": v} for k, v in ozellik.items()}, "required": list(ozellik)}


ARACLAR = [{"type": "function", "function": {"name": n, "description": d, "parameters": p}} for n, d, p in [
    ("kombin_sec", "Görev tarifine uyan en iyi 1-3 araç kombinini (adım adım) döner.", _p(gorev="string")),
    ("katalog_ara", "Yetenek/araç kataloğunda görev tarifine göre arama yapar.", _p(is_tarifi="string")),
    ("dosya_oku", "Proje içinden bir dosyanın satır aralığını okur (en çok 60 satır).", _p(yol="string", bas="integer", adet="integer")),
    ("ara", "Proje dizininde dosya adı desenine (regex) uyan yolları listeler (en çok 20).", _p(desen="string", dizin="string"))]]


def _kok_ici(yol):
    p = (KOK / yol).resolve()
    if KOK not in p.parents and p != KOK:
        raise ValueError("kök dışı yol")
    if GIZLI.search(str(p.relative_to(KOK))):
        raise ValueError("gizli dosya adı")
    return p


def _calistir(ad, a):
    if ad in ("kombin_sec", "katalog_ara"):
        komut = [sys.executable, "-I", "tools/kombin_sec.py", "sec", str(a["gorev"])] if ad == "kombin_sec" else [sys.executable, "-I", "tools/katalog_ara.py", str(a["is_tarifi"])]
        p = subprocess.run(komut, cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=40, creationflags=H.NW)
        return (p.stdout or p.stderr)[:KIRP]
    if ad == "dosya_oku":
        p = _kok_ici(str(a["yol"]))
        satir = p.read_text(encoding="utf-8", errors="replace").splitlines()
        b, n = max(int(a.get("bas", 1)), 1), min(int(a.get("adet", 40)), 60)
        return "\n".join(f"{b + i}\t{s}" for i, s in enumerate(satir[b - 1:b - 1 + n]))[:KIRP]
    if ad == "ara":
        kok, r = _kok_ici(str(a.get("dizin") or ".")), re.compile(str(a["desen"]))
        return "\n".join([str(x.relative_to(KOK)) for x in kok.rglob("*") if x.is_file() and r.search(x.name) and not GIZLI.search(str(x.relative_to(KOK)))][:20]) or "(yok)"
    raise ValueError("bilinmeyen araç")


def _istek(e, mesajlar, zaman=60):
    g = {"model": e.model, "messages": mesajlar, "tools": ARACLAR, "max_tokens": 2000}
    if e.prov in H.DUSUNME and "gemma" not in e.model:
        g["reasoning_effort"] = "low"
    q = urllib.request.Request(H._url(e.prov), json.dumps(g).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8", "Authorization": "Bearer " + H._anahtar(H.SAG[e.prov][1])})
    try:
        with urllib.request.urlopen(q, timeout=zaman) as f:
            j = json.load(f)
    except urllib.error.HTTPError as x:
        raise H.Hata(x.code, H._gizle(x.read()[:200].decode("utf-8", "replace")))
    try:
        return j["choices"][0]["message"]
    except (KeyError, IndexError, TypeError):
        raise H.Hata(502, "choices yok")


def kos(gorev, tur=6):
    """(metin | None, model, cagrilar). Model tool_calls dönmezse düz yanıt; model hata verirse havuzdaki sıradaki halka."""
    denenen, tahmin = set(), len(gorev) // 3 + 2000
    while (e := H._sec("yazim", tahmin, None, None, denenen)):
        denenen.add(H.ad(e))
        if e.prov not in TOOLS_PROV:
            continue
        mesaj, cagrilar = [{"role": "system", "content": "Araçları gerektiğinde çağır; araç çıktısına dayanarak kısa yanıt ver."}, {"role": "user", "content": gorev}], []
        try:
            for _ in range(tur):
                m = _istek(e, mesaj)
                tc = m.get("tool_calls")
                if not tc:
                    if (m.get("content") or "").strip():
                        H._basari(e); H._oran(e, False)
                        return m["content"].strip(), H.ad(e), cagrilar
                    raise H.Hata(0, "boş yanıt")
                mesaj.append({"role": "assistant", "content": m.get("content") or "", "tool_calls": tc})
                for c in tc:
                    ad = c["function"]["name"]
                    try:
                        cikti = _calistir(ad, json.loads(c["function"]["arguments"] or "{}"))
                    except (ValueError, KeyError, OSError, subprocess.SubprocessError) as x:
                        cikti = f"HATA: {type(x).__name__}: {x}"[:300]
                    cagrilar.append(ad)
                    mesaj.append({"role": "tool", "tool_call_id": c.get("id", ad), "content": cikti})
            return None, H.ad(e), cagrilar  # tur sınırı
        except (H.Hata, OSError, ValueError) as x:
            H._dus(e, x if isinstance(x, H.Hata) else H.Hata(599, type(x).__name__)); H._oran(e, True)
    return None, None, []


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    y, model, cagrilar = kos(" ".join(sys.argv[1:]) or "Bir 3D landing sitesi için hangi araç kombini?")
    print(model, cagrilar); print(y)
