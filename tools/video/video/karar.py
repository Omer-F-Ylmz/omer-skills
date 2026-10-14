"""VİDEO-KISA-TOKEN-2 M1–M4/M6: kısa + uzun hat ortak karar adımı.

Araç/link listesi deterministiktir (Gemini + paket kanıtı); Claude yalnız bilinmeyen/farklı araç satırına KUR|DENE|ATLA ekler, listeyi yazmaz.
Önbellek (karar.tsv): aynı ad + aynı kanıt (repo) yeniden sorulmaz. Satırı olmayan video Claude'a hiç gitmez.
"""
import os
import re
from pathlib import Path

from . import hafif
from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
ONBELLEK = KOK / ".kos" / "kopru" / "video" / "kisa" / "karar.tsv"
PARTI = 120  # satır/çağrı (M3)
KARARLAR = ("KUR", "DENE", "ATLA")
# sabit önek bayt-bayt aynı kalır (M3 önek önbelleği); değiştirirsen karar.tsv'yi de sıfırla
SISTEM = ("Ömer'in Claude Code (Windows) kurulumu için araç kararı verirsin. Her girdi satırı: "
          "ad<TAB>videodaki kanıt<TAB>araştırma özü<TAB>lisans<TAB>yıldız·son push. "
          "Her satır için TEK çıktı satırı yaz: ad<TAB>KUR|DENE|ATLA<TAB>≤12 kelime Türkçe gerekçe. "
          "KUR: açık lisans (MIT/Apache/BSD), bakımlı, bizde doğrudan işe yarar (skill, MCP, CLI, ajan aracı). "
          "DENE: işe yarayabilir ama belirsiz (lisans yok, az yıldız, hesap/anahtar şartı, kanıt zayıf). "
          "ATLA: araç değil (genel kelime, kişi, arayüz yazısı), kapalı/ücretli, ilgisiz ya da eşdeğeri bizde var. "
          "Ad aynen kopyalanır; satır silme, ekleme, açıklama yok. Çıktı JSON alanı tsv.\n"
          "Örnek girdi:\nRepomix\trepoyu tek dosyaya paketler\tLLM için repo paketleyici CLI\tMIT\t21000·2026-10-01\n"
          "Tamam butonu\tekranda düğme yazısı\t\t\t\n"
          "Örnek çıktı:\nRepomix\tKUR\tMIT, bakımlı; repoyu Claude bağlamına tek dosyada verir\n"
          "Tamam butonu\tATLA\tarayüz yazısı, araç değil")
SEMA = {"type": "object", "required": ["tsv"], "properties": {"tsv": {"type": "string"}}}
SURUM = re.compile(r"\b(v\d+(\.\d+)*|\d+\.\d+(\.\d+)?)\b|\byeni (sürüm|özellik)\b", re.I)  # bilinen araçta "fark var" işareti


def _kisa(s, n):
    return " ".join(str(s or "").split()[:n])


def satir(a, kunye=None):
    """Gemini aracı + araştırma künyesi → tek TSV girdi satırı (kanıt ≤20, özet ≤40 kelime)."""
    k = kunye or {}
    ozet = _kisa(f"{k.get('aciklama', '')} {k.get('readme', '')}", 40)
    return "\t".join([a["ad"].replace("\t", " "), _kisa(a.get("ne_dedi"), 20), ozet, k.get("lisans", ""),
                      f"{k['yildiz']}·{k.get('push', '')}" if k.get("yildiz") is not None else ""])


def sorulacak(a, kat):
    """Bilinmeyen araç ya da katalogda olup videoda sürüm/yeni özellik iddiası taşıyan araç."""
    return not kat or bool(SURUM.search(a.get("ne_dedi") or ""))


def _kanit_anahtar(k):
    return (k or {}).get("repo", "")


def onbellek(yol=ONBELLEK):
    """{normal(ad): (karar, gerekçe, kanıt)}"""
    if not yol.is_file():
        return {}
    out = {}
    for s in yol.read_text(encoding="utf-8").splitlines()[1:]:
        p = s.split("\t")
        if len(p) == 5:
            out[tr.normal(p[0])] = (p[1], p[2], p[4])
    return out


def ayristir(tsv, adlar):
    """Claude TSV → {ad: (karar, gerekçe)}; yalnız sorulan adlar, geçerli karar."""
    n = {tr.normal(a): a for a in adlar}
    out = {}
    for s in (tsv or "").splitlines():
        p = [x.strip() for x in s.split("\t")]
        if len(p) >= 2 and tr.normal(p[0]) in n and p[1].upper() in KARARLAR:
            out[n[tr.normal(p[0])]] = (p[1].upper(), _kisa(p[2] if len(p) > 2 else "", 12))
    return out


def ver(istek, env=None, efor="low", cagir=hafif.cagir, yol=ONBELLEK, tarih=""):
    """istek: {ad: (girdi satırı, künye)} → ({ad: (karar, gerekçe)}, [çağrı sonuçları]). Önbellekteki aynı kanıt sorulmaz."""
    eski, out, cagrilar = onbellek(yol), {}, []
    sor = {}
    for ad, (s, k) in istek.items():
        e = eski.get(tr.normal(ad))
        if e and e[2] == _kanit_anahtar(k):
            out[ad] = e[:2]
        else:
            sor[ad] = (s, k)
    env = {**(os.environ if env is None else env), "VIDEO_FABLE_PROTOKOL": "0"}  # önek ≤1k jeton (M3); FABLE öneki karar için gereksiz
    adlar = list(sor)
    for i in range(0, len(adlar), PARTI):
        p = adlar[i:i + PARTI]
        y = cagir(SISTEM, "\n".join(sor[a][0] for a in p), SEMA, efor=efor, env=env, butce=1.0)
        cagrilar.append(y)
        yeni = ayristir((y.get("form") or {}).get("tsv"), p)
        out.update(yeni)
        if yeni:
            yol.parent.mkdir(parents=True, exist_ok=True)
            bas = "" if yol.is_file() else "ad\tkarar\tgerekce\ttarih\tkanit\n"
            with yol.open("a", encoding="utf-8") as f:
                f.write(bas + "".join(f"{a}\t{kr}\t{g}\t{tarih}\t{_kanit_anahtar(sor[a][1])}\n" for a, (kr, g) in yeni.items()))
    return out, cagrilar
