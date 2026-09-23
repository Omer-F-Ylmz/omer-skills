"""15 öğrenme: durum.md · karar kümesi · kural/olgu · bilgi kartı · çelişki · sponsor."""
import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from jev import cekirdek as c

from . import metin as m
from . import tarama as tr

KOK = Path(__file__).resolve().parents[3]
ELLE = "<!-- elle -->"
ELLE_ISKELET = "\n## Öncelikler\n- \n\n## Açık sorunlar\n- \n"
TAVAN = 3000
KARAR = ("KUR", "DENE", "ÖĞREN", "ZATEN VAR", "ALTERNATİF", "RED")
ARACLAR = (("RTK", "komut çıktısını hook ile sıkıştırır (git/npm/dotnet/pytest)"),
           ("headroom", "girdi context'ini sıkıştıran yerel vekil + MCP (compress/retrieve)"),
           ("graphify", "kod/doküman bilgi grafiği; query/path/explain ile dar bağlam"),
           ("jev", "TypeSafe tipli yargı: log · ilgili · kanit · triage · tarama · skill"),
           ("video", "YouTube kademeli izleme, tarama, katman, durum, bilgi kartları"))
OLCUM = ("docs/*-notlari*.md", "docs/video-tarama/olcum-*.md")
GUVEN = ("yüksek", "orta", "düşük")
FM = ("iddia", "kaynak", "guven", "dogrulama", "tarih", "bayatlama", "etiketler")
ALAN = re.compile(r"^(\w+):\s*(.*?)\s*$")
TUR_SORU = "Videodaki ipucu (state) Ömer'in iş akışına dair bir davranış kuralı mı, yoksa model/araç/ortam hakkında bir olgu mu?"
TUR_OLCUT = {"kural": "Ömer'in çalışma biçimine dair uygulanabilir davranış kuralı (ne yapılır, ne yapılmaz).",
             "olgu": "Bir model, araç ya da ortamın nasıl davrandığına dair bilgi; Ömer'in iş akışı kuralı değil."}
KART_A1 = "Yeni olgu (state) aşağıdaki bilgi kartlarından hangisiyle aynı iddiayı taşıyor? Hiçbiriyse 'hiçbiri'."
KART_A2 = "Yeni olgu (state) şu kartla aynı iddia mı? Kart: {k}"
CEL_A1 = "Yeni kural/olgu (state) aşağıdakilerden hangisine en yakın konuda? Hiçbiri ilgili değilse 'hiçbiri'."
CEL_A2 = "Yeni kural/olgu (state) şu maddeyle çelişiyor mu (ikisi birlikte uygulanamaz mı)? Madde: {k}"
SPONSOR_Q = "Bu video kesiti (state) bir sponsor/reklam tanıtımı mı?"
# 15b K2: belirli model/araç adı geçen ipucu olgudur (Jev'e sorulmaz)
# ponytail: sabit ad listesi; yeni model/araç çıktıkça eklenir, plugin adları gerekirse tr.sozluk_kur'dan beslenir
ADLI = re.compile(r"\b(fable|opus|sonnet|haiku|gpt-?\d[\w.]*|gemini|codex|llama|mistral|deepseek|qwen|rtk|headroom|graphify|gitleaks|semgrep"
                  r"|skillspector|yt-dlp|ffmpeg)\b", re.I)
SPONSOR = re.compile(r"sponsor|brought to you|promo code|discount code|affiliate|indirim kodu|reklam", re.I)


def yargi_oku(k):
    """Kayıt satırının K1 kararı; eski satırlar işaret/katmandan eşlenir, UYGULA/BEKLE → None (değerlendirmeye girer)."""
    if k.get("yargi"):
        return k["yargi"]
    e = k.get("etiket") or k.get("isaret") or ""
    if e.startswith(("ÇİFT", "ÖNCEDEN")) or "ÇİFT" in (k.get("karar") or ""):
        return "ZATEN VAR"
    if e:
        return None
    return {"T0": "KUR", "T1": "KUR", "T2": "KUR", "RED": "RED"}.get(k.get("katman"))


# --- K4 bilgi kartları ---

def kart_metni(a, bugun):
    dog = a.get("dogrulama") or "doğrulanamadı"
    g = a.get("guven") if a.get("guven") in GUVEN else "orta"
    if g == "yüksek" and not dog.startswith("http"):  # doğrulanmamış iddia yüksek güvenle yazılmaz
        g = "orta"
    iddia = a.get("iddia") or a.get("kural") or a["ad"]
    fm = {"iddia": iddia, "kaynak": kaynak(a), "guven": g, "dogrulama": dog, "tarih": bugun.isoformat(),
          "bayatlama": (bugun + timedelta(days=90)).isoformat(), "etiketler": a.get("etiketler") or "-"}
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in fm.items()) + "---\n" + (a.get("govde") or iddia) + "\n"


def kaynak(a):
    return " ".join(x for x in (a.get("video"), a.get("zaman")) if x) or a.get("url") or "?"


def kart_oku(metin):
    p = metin.split("---\n", 2)
    if len(p) < 3 or p[0].strip():
        return {}, metin.splitlines()
    return {x[1]: x[2] for s in p[1].splitlines() if (x := ALAN.match(s))}, p[2].splitlines()


def kart_denetle(metin):
    fm, gov = kart_oku(metin)
    h = [f"alan eksik: {k}" for k in FM if not fm.get(k)]
    if fm.get("guven") and fm["guven"] not in GUVEN:
        h.append(f"guven geçersiz: {fm['guven']} ({'/'.join(GUVEN)})")
    if fm.get("guven") == "yüksek" and not fm.get("dogrulama", "").startswith("http"):
        h.append("guven yüksek ama dogrulama linki yok")
    for k in ("tarih", "bayatlama"):
        try:
            date.fromisoformat(fm.get(k, ""))
        except ValueError:
            h.append(f"{k} tarih değil: {fm.get(k)}")
    if (n := sum(1 for s in gov if s.strip())) > 8:
        h.append(f"gövde {n} satır > 8")
    return h


def kartlar(kok):
    return [(y.stem, kart_oku(y.read_text(encoding="utf-8"))[0], y) for y in sorted((Path(kok) / "bilgi").glob("*.md"))]


def celiski(tk, state, kl, ks):
    """K5: en yakın kural/kart (aşama 1) → çelişiyor mu (aşama 2, p≥0.5). Etiket ya da None; eşleşen asla otomatik çözülmez."""
    return tr.kural_esle(tk, state, list(kl) + [(f"bilgi:{s}", fm.get("iddia", "")) for s, fm, _ in ks], CEL_A1, CEL_A2)


def ogren(tk, kok, a, ad, bugun, kl):
    """(karar, çelişki etiketi|None). Çift kart → yeni kaynak mevcut karta eklenir; çelişkide kart yazılmaz."""
    ks, d = kartlar(kok), Path(kok) / "bilgi"
    state = f"OLGU: {ad}\n{a.get('iddia') or a.get('kural') or ad}"
    if ks and (es := tr.kural_esle(tk, state, [(f"bilgi:{s}", fm.get("iddia", "")) for s, fm, _ in ks], KART_A1, KART_A2)):
        y, yeni = d / f"{es.split(':', 1)[1]}.md", kaynak(a)
        y.write_text(re.sub(r"^kaynak: (.*)$", lambda x: x[0] if yeni in x[1] else f"kaynak: {x[1]}, {yeni}",
                            y.read_text(encoding="utf-8"), count=1, flags=re.M), encoding="utf-8")
        return f"kart birleşti: bilgi/{y.name} (+{yeni})", None
    if cel := celiski(tk, state, kl, ks):
        return f"eklenmedi: ÇELİŞKİ ({cel})", cel
    d.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"\W+", "-", ad.casefold()).strip("-") or "kart"
    y = d / f"{slug}.md"
    i = 2
    while y.exists():
        y, i = d / f"{slug}-{i}.md", i + 1
    y.write_text(kart_metni({**a, "ad": ad}, bugun), encoding="utf-8")
    return f"kart yazıldı: bilgi/{y.name}", None


def bilgi(ns, ctx):
    kok, bugun = Path(ctx["env"].get("VIDEO_UYGULA_KOK") or KOK), date.today().isoformat()
    n = 0
    for s, fm, _ in kartlar(kok):
        bayat = fm.get("bayatlama", "") < bugun
        if ns.bayat and not bayat:
            continue
        n += 1
        print(f"{s} · {fm.get('guven', '?')} · {fm.get('bayatlama', '?')}" + (" · yeniden doğrula" if bayat else "") + f" · {fm.get('iddia', '')[:100]}")
    print(f"{n} kart{' (bayat)' if ns.bayat else ''} · {kok / 'bilgi'}")
    return 0


# --- K3 · K2 · K6 ---

def olgu_mu(tk, ad, a):
    if ADLI.search(f"{ad} {a.get('iddia') or ''} {a.get('kural') or ''}"):
        return True
    q = {"tur": {"type": "choice", "instructions": TUR_SORU, "criteria": TUR_OLCUT}}
    p = (((tk.yargila([f"İPUCU: {ad}\nİddia: {a.get('iddia') or '-'}\nKural önerisi: {a.get('kural') or ad}"], q)[0] or {}).get("tur") or {}).get("probabilities") or {})
    return p.get("olgu", 0) > p.get("kural", 0)


def deneme_yaz(kok, a, ad, metin):
    y = Path(kok) / "docs" / "denemeler" / f"{ad}.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    alan = (("Hipotez", "hipotez"), ("Metrik", "metrik"), ("Bütçe", "butce"), ("Geri alma", "geri_alma"), ("Başarı eşiği", "esik"))
    ilk = lambda b: next((s.strip() for s in tr.bolum(metin, b).splitlines() if s.strip()), "")
    y.write_text(f"# Deneme: {ad}\n\nvideo {a.get('video', '?')} · 15 · bu dalgada koşulmaz (14b)\n\n"
                 + "".join(f"## {b}\n{a.get(k) or ilk(b) or '?'}\n\n" for b, k in alan), encoding="utf-8")
    return f"deneme: docs/denemeler/{ad}.md"


def meta(ctx, v):
    try:
        return json.loads((ctx["kok"] / str(v) / "meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def sponsor_mu(ctx, me, a, jev):
    """Adayın anındaki chapter başlığı + segment metninde sponsor sinyali varsa Jev noul teyidi (1 istek)."""
    if not a.get("zaman") or not me:
        return False
    t = m.sn(a["zaman"])
    parca = [ch.get("title", "") for ch in me.get("chapters") or [] if ch.get("start_time", 0) <= t < ch.get("end_time", float("inf"))]
    try:
        seg = (ctx["kok"] / str(a.get("video")) / "segmentler.jsonl").read_text(encoding="utf-8").splitlines()
        parca += [s["metin"] for x in seg if x.strip() and (s := json.loads(x))["bas"] <= t < s["son"]]
    except OSError:
        pass
    metin = "\n".join(parca)
    if not SPONSOR.search(metin):
        return False
    y = (jev().yargila([metin[:4000]], {"s": {"type": "noul", "instructions": SPONSOR_Q}})[0] or {}).get("s")
    return bool(y and y["noul"] >= 0.5)


# --- K0 durum.md ---

def _olcum(y):
    sat = y.read_text(encoding="utf-8").splitlines()
    out = [f"- {y.name}: {next((s[2:] for s in sat if s.startswith('# ')), y.stem)}"]
    bas = None
    for s in sat:
        if s.startswith("## "):
            bas = s[3:].strip()
        elif bas and s.startswith("- "):
            out.append(f"  - {bas}: {s[2:].strip()[:140]}")
            bas = None
    return out


def durum(ns, ctx):
    env = ctx["env"]
    kok = Path(env.get("VIDEO_UYGULA_KOK") or KOK)
    hedef = kok / "docs" / "durum.md"
    ku, vt = kok / "docs" / "kurulumlar" / "kayit.jsonl", kok / "docs" / "video-tarama" / "kayit.jsonl"
    olcum = sorted(p for g in OLCUM for p in kok.glob(g))
    eski = hedef.read_text(encoding="utf-8") if hedef.is_file() else ""
    if eski and all(not y.is_file() or y.stat().st_mtime <= hedef.stat().st_mtime for y in (ku, vt, *olcum)):
        print(f"güncel: {hedef} · ~{c.token(eski)} token")
        return 0
    elle = eski.split(ELLE, 1)[1] if ELLE in eski else ELLE_ISKELET
    say = Counter(k for _, k in tr.sozluk_kur(Path(env.get("VIDEO_EV") or Path.home()), []))
    kay, tar = tr.kayit_oku(ku), tr.kayit_oku(vt)
    kanal = {}
    for k in kay:
        x = kanal.setdefault(k.get("kanal") or "?", [0, 0])
        x[0] += 1
        x[1] += yargi_oku(k) in ("KUR", "ÖĞREN")
    ele = [f"- {a} (video {k['id']})" for k in tar for a in k.get("ele") or []]
    karar = [f"- {k['ad']} → {yargi_oku(k) or '?'}: {str(k.get('karar', ''))[:90]}" + (" (sponsor)" if k.get("sponsor") else "") for k in kay]
    bas = ["# Durum envanteri", "", "`video durum` üretir (mtime'la yenilenir); OTOMATİK bölüm her yenilemede yeniden yazılır, "
           "sondaki elle işaretinin altı korunur.", "", "## Köprü katalogu",
           f"- skill {say['skill']} · plugin {say['plugin']} · MCP {say['mcp']}"] + [f"- {a}: {d}" for a, d in ARACLAR]
    son = (["", "## Kanal güvenilirliği (aday · KUR/ÖĞREN oranı)"] + [f"- {k}: {n} aday · {i / n:.0%}" for k, (n, i) in kanal.items()]
           + ["", "## Son taramalar"] + [f"- {k['id']} {k.get('tarih', '')}: {len(k.get('adaylar') or [])} aday" for k in tar[-10:]]
           + ["", "## Ölçüm bulguları"] + [s for y in olcum for s in _olcum(y)[:4]]
           + ["", "## ELE (son 20)"] + ele[-20:] + ([f"- … +{len(ele) - 20} (docs/video-tarama/kayit.jsonl)"] if len(ele) > 20 else []) + ["", ELLE])
    i = 0
    while True:  # 3k aşılırsa en eski kararlar tek satır sayıma katlanır
        ozet = Counter(yargi_oku(k) or "?" for k in kay[:i])
        md = "\n".join(bas + ["", "## Son kararlar"] + ([f"- eski {i} karar: " + " · ".join(f"{a} {n}" for a, n in ozet.most_common())] if i else [])
                       + karar[i:] + son) + elle
        if c.token(md) <= TAVAN or i >= len(karar):
            break
        i = min(len(karar), i + max(1, len(karar) // 20))
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(md, encoding="utf-8")
    print(f"durum.md ~{c.token(md)} token · karar {len(karar)}" + (f" (eski {i} özetlendi)" if i else "") + f" · {hedef}")
    return 0
