"""BEYIN-1/2 içe alma: kaynak md'leri + akışları Obsidian kasasına bölüm notları olarak yazar (model yok).

Kaynaklar silinmez/taşınmaz; kaynak sha'sı (ve bağ kümesi) değişmediyse not yeniden yazılmaz.
Her not: frontmatter (kaynak, satir, guncellenme, tur, guven, etiket[, aliases]) + birebir gövde
+ "Bağlar:" (ad eşleşmeli [[wikilink]]) + [[önceki · sonraki · klasör MOC]] satırı.
Akışlar (BEYIN-2): ajan-sira sonuçları, alt ajan özetleri, yönlendirici kaydı, ÖĞREN kartları,
claude-mem gözlemleri (worker yoksa atlanır), SIRA karar satırları.
Kullanım: python tools/beyin_al.py [--kasa YOL] [--qmd-yok] [--zorla]
"""
import argparse
import datetime
import glob
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
BELLEK = Path.home() / ".claude/projects/C--Projeler-omer-skills/memory"
ALT = Path.home() / ".claude/projects/C--Projeler-omer-skills"
MEM = "http://127.0.0.1:37777/api/observations?limit=500"
# (klasör, önek, tür, glob)
KAYNAKLAR = [
    ("10-kararlar", "gorev", "gorev", str(KOK / ".kos/kopru/gorev/*.md")),
    ("10-kararlar", "gecmis", "gorev", str(KOK / ".kos/kopru/gorev-gecmis/*.md")),
    ("10-kararlar", "kural", "kural", r"C:\Projeler\omer-kurallar.md"),
    ("10-kararlar", "global", "kural", str(Path.home() / ".claude/CLAUDE.md")),  # yalnız okunur
    ("10-kararlar", "global", "kural", str(Path.home() / ".claude/RTK.md")),
    ("20-ogren", "ogren", "ogren", str(KOK / "docs/ogren/*.md")),
    ("20-ogren", "kogren", "ogren", str(KOK / ".kos/kopru/ogren/*.md")),
    ("30-video", "kurulum", "kurulum", str(KOK / "docs/kurulumlar/*.md")),
    ("40-projeler", "devir", "devir", str(KOK / ".kos/kopru/devir/*.md")),
    ("50-dersler", "ders", "ders", str(BELLEK / "*.md")),
]
PARCA_TAVAN = 150  # satır; bundan uzun bölüm sonraki boş satırda (en geç +30'da) kesilir; arama bölüm içinde satır penceresi + başlık verir
TAKMA_TUR = {"gorev", "kurulum", "ders", "ogren", "ajan"}  # dosya kökü bağ hedefi olan türler
BAG_TAVAN = 5
GIZLI = re.compile(r"sk-[\w-]{20,}|gh[ps]_\w{20,}|github_pat_\w{20,}|AIza[\w-]{30,}|xox[abp]-[\w-]{10,}"
                   r"|Bearer\s+[\w.-]{20,}|(?i:(?:api[_-]?key|secret|password|parola)\s*[=:]\s*)[^\s\"',]{8,}")
SABLON = """---
tur: gunluk
guncellenme: {{date:YYYY-MM-DD}}
etiket: [gunluk]
---
# {{date:YYYY-MM-DD}}
## Kararlar (★)
## Öğrenilen
## Akış (beyin_al)
"""


def bol(satirlar):
    """[(baslangic_satir_1tabanli, [satirlar])] — başlıkta ya da PARCA_TAVAN'da böler."""
    parcalar, bas, cur = [], 1, []
    for i, s in enumerate(satirlar, 1):
        # bölüm başlığında bölünür; yalnız çok uzun bölüm tavanda, tercihen boş satırda (paragraf ortasında değil) kesilir
        if cur and (s.startswith("#") or (len(cur) >= PARCA_TAVAN and (not s.strip() or len(cur) >= PARCA_TAVAN + 30))):
            parcalar.append((bas, cur))
            bas, cur = i, []
        cur.append(s)
    if cur:
        parcalar.append((bas, cur))
    return [(b, p) for b, p in parcalar if any(x.strip() for x in p)]


def ad_yap(onek, yol):
    return f"{onek}-" + re.sub(r"[^\w.-]+", "-", Path(yol).stem).strip("-")


def kelimeler(metin):
    return set(re.findall(r"[\w-]+", metin.lower()))


def takma_adlar(girdiler):
    """takma ad (kaynak dosya kökü) -> not adı; kısa ya da kaynakların >%5'inde geçen (genel) adlar elenir."""
    aday = {}
    for g in girdiler:
        t = Path(g[2]).stem.lower()
        if g[3] in TAKMA_TUR and len(t) >= 5:
            aday.setdefault(t, g[1])
    kumeler = [kelimeler(g[4].decode("utf-8", "replace")) for g in girdiler]
    tavan = max(3, len(kumeler) // 20)
    return {t: ad for t, ad in aday.items() if sum(t in k for k in kumeler) <= tavan}


def baglar_hesapla(govde, tadlar, kendi):
    """[(not adı, takma ad)] — gövdede birebir geçen takma adlar, uzun olan önce, en fazla BAG_TAVAN."""
    es = {}
    for t in sorted(kelimeler("\n".join(govde)) & tadlar.keys(), key=lambda t: (-len(t), t)):
        if tadlar[t] != kendi:
            es.setdefault(tadlar[t], t)
    return list(es.items())[:BAG_TAVAN]


def not_metni(kaynak, bas, govde, tarih, tur, etiket, onceki, sonraki,
              guven="kaynak-birebir", baglar=(), takma=None, moc="index"):
    kar = any("★" in s for s in govde)
    etiketler = [etiket, tur] + (["karar"] if kar else [])
    fm = ["---", f"kaynak: {kaynak}", f"satir: {bas}", f"guncellenme: {tarih}", f"tur: {tur}",
          f"guven: {guven}", f"etiket: [{', '.join(etiketler)}]"]
    fm += [f"aliases: [{json.dumps(takma, ensure_ascii=False)}]"] if takma else []
    alt = ["Bağlar: " + " · ".join(f"[[{a}--1|{t}]]" for a, t in baglar)] if baglar else []
    alt.append(" · ".join(f"[[{x}]]" for x in (onceki, sonraki, moc) if x))
    return "\n".join(fm + ["---"] + govde + [""] + alt) + "\n"


def yaz(yol, metin):
    yol.parent.mkdir(parents=True, exist_ok=True)
    with open(yol, "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)


def kaynak_al(kasa, klasor, ad, kaynak, metin, tarih, tur, eski_sayi, guven="kaynak-birebir", tadlar=None):
    if tur == "ders":  # bellek notları [[slug]] ile bağlanır; kasada not adı ders-<slug>--1
        metin = re.sub(r"\[\[([^\]|#]+)\]\]", r"[[ders-\1--1|\1]]", metin)
    satirlar = metin.replace("\r\n", "\n").split("\n")
    parcalar = bol(satirlar)
    adlar = [f"{ad}--{i}" for i in range(1, len(parcalar) + 1)]
    tadlar = tadlar or {}
    takma = next((t for t, a in tadlar.items() if a == ad), None)
    for i, (bas, govde) in enumerate(parcalar):
        onceki = adlar[i - 1] if i else None
        sonraki = adlar[i + 1] if i + 1 < len(adlar) else None
        yaz(kasa / klasor / f"{adlar[i]}.md",
            not_metni(kaynak, bas, govde, tarih, tur, ad, onceki, sonraki, guven,
                      baglar_hesapla(govde, tadlar, ad), takma if i == 0 else None, f"index-{klasor}"))
    # kısalan kaynağın artık parçaları silinmez, geçersiz işaretlenir (beyin ara atlar)
    for i in range(len(parcalar) + 1, eski_sayi + 1):
        yaz(kasa / klasor / f"{ad}--{i}.md", f"---\nkaynak: {kaynak}\ngecersiz: true\n---\n")
    return len(parcalar)


def gun(p):
    return datetime.date.fromtimestamp(Path(p).stat().st_mtime).isoformat()


def jsonl(p):
    for s in Path(p).read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            yield json.loads(s)
        except ValueError:
            continue


def ajan_sira():
    out = []
    for p in sorted((KOK / ".kos/kopru/ajan-sira").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except ValueError:  # boş ya da yazılıyor
            continue
        mod = "; ".join(
            f"{m} girdi {u.get('inputTokens', 0) + u.get('cacheReadInputTokens', 0) + u.get('cacheCreationInputTokens', 0)}"
            f" (önbellek okuma {u.get('cacheReadInputTokens', 0)}) çıktı {u.get('outputTokens', 0)}"
            for m, u in (d.get("modelUsage") or {}).items())
        metin = (f"# ajan-sira {p.stem}\n- durum: {'HATA' if d.get('is_error') else 'tamam'} · tur {d.get('num_turns')}"
                 f" · maliyet ${d.get('total_cost_usd') or 0:.2f} · süre {(d.get('duration_ms') or 0) // 60000} dk\n"
                 f"- modeller: {mod}\n\n## sonuç\n{d.get('result') or ''}")
        out.append(("60-ajanlar", f"ajan-{p.stem}", str(p), "ajan", metin.encode(), gun(p), "kaynak-birebir"))
    return out


def alt_ozet(f):
    """Alt ajan transkripti → tek satır: tarih · tip/model · token · görev · sonuç · ders (model yok)."""
    gorev = sonuc = model = ilk = ""
    tok = 0
    for j in jsonl(f):
        m = j.get("message") or {}
        ilk = ilk or str(j.get("timestamp", ""))[:16]
        c = m.get("content")
        metin = c if isinstance(c, str) else " ".join(
            x.get("text", "") for x in c or [] if isinstance(x, dict) and x.get("type") == "text")
        if m.get("role") == "user" and not gorev:
            gorev = metin
        if m.get("role") == "assistant":
            u = m.get("usage") or {}
            tok += sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens",
                                                "cache_creation_input_tokens", "output_tokens"))
            model = m.get("model", model)
            sonuc = metin if metin.strip() else sonuc
    meta = f.with_suffix(".meta.json")
    tip = json.loads(meta.read_text(encoding="utf-8")).get("agentType", "") if meta.exists() else ""
    ders = next((x for x in sonuc.split("\n") if re.search(r"(?i)\bders|öğren|kök neden|root cause|lesson", x)), "")

    def tek(x, n):
        return " ".join(x.split())[:n]
    return (f"- {ilk} · {tip or '-'} · {model} · {tok} tok · görev: {tek(gorev, 200)} · sonuç: {tek(sonuc, 400)}"
            + (f" · ders: {tek(ders, 200)}" if ders else ""))


def alt_ajanlar(onbellek):
    gruplar = {}
    for f in sorted(ALT.glob("*/subagents/*.jsonl")):
        k, mt = str(f), f.stat().st_mtime
        if onbellek.get(k, [None])[0] != mt:
            onbellek[k] = [mt, alt_ozet(f)]
        gruplar.setdefault(f.parent.parent, []).append(onbellek[k][1])
    return [("60-ajanlar", f"alt-{d.name[:8]}", str(d / "subagents"), "alt",
             (f"# alt ajanlar · oturum {d.name}\n" + "\n".join(sorted(s))).encode(), gun(d / "subagents"),
             "betik-ozet") for d, s in gruplar.items()]


def yonlendir():
    p = KOK / ".kos/kopru/yonlendir-kayit.jsonl"
    if not p.exists():
        return []
    sat = ["# yönlendirici kaydı (ROUTER-1)"] + ["- " + " · ".join(f"{k}={v}" for k, v in j.items()) for j in jsonl(p)]
    return [("60-ajanlar", "yonlendir-kayit", str(p), "ajan", "\n".join(sat).encode(), gun(p), "kaynak-birebir")]


def kartlar():
    p = KOK / "docs/atlas/kart.jsonl"
    gr = {}
    for j in jsonl(p):
        gr.setdefault(re.sub(r"[^\w.-]+", "-", str(j.get("asama") or "diger")), []).append(
            f"- **{j.get('ad')}** — " + " · ".join(f"{k}: {v}" for k, v in j.items() if k not in ("ad", "asama")))
    return [("20-ogren", f"kart-{a}", f"{p}#{a}", "kart", (f"# ÖĞREN kartları: {a}\n" + "\n".join(v)).encode(),
             gun(p), "kaynak-birebir") for a, v in gr.items()]


def gozlemler():
    try:
        with urllib.request.urlopen(MEM, timeout=5) as r:
            items = json.load(r).get("items", [])
    except (OSError, ValueError):  # worker yok/kapalı → akış atlanır
        return []
    gunler = {}
    for it in items:
        if it.get("project") not in (None, "omer-skills"):
            continue
        e = it.get("created_at_epoch")
        g = (datetime.date.fromtimestamp(e / 1000 if e > 1e11 else e).isoformat() if e
             else str(it.get("created_at", ""))[:10])
        gunler.setdefault(g, []).append(f"- #{it.get('id')} {it.get('type')} — {it.get('title')}: "
                                        + " ".join(str(it.get("subtitle") or it.get("narrative") or "").split())[:300])
    if len(items) >= 500 and gunler:  # pencerenin en eski günü yarım olabilir; yazılmış notu kısaltmasın
        gunler.pop(min(gunler))
    return [("50-dersler", f"mem-{g}", f"claude-mem:{g}", "gozlem",
             (f"# claude-mem gözlemleri {g}\n" + "\n".join(sorted(v))).encode(), g, "model-ozet")
            for g, v in gunler.items()]


def sira_kararlar():
    p = KOK / ".kos/kopru/gorev/SIRA.md"
    sat = [f"SIRA.md:{i}: {s}" for i, s in enumerate(p.read_text(encoding="utf-8").splitlines(), 1)
           if re.search(r"BİTTİ|KARAR|[Kk]ararı|★|GEÇMEDİ|\bARA\b", s)]
    return [("10-kararlar", "sira-kararlar", f"{p}#karar", "karar",
             ("# SIRA karar satırları\n" + "\n".join(sat)).encode(), gun(p), "kaynak-birebir")]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kasa", default=str(KASA))
    ap.add_argument("--qmd-yok", action="store_true")
    ap.add_argument("--zorla", action="store_true", help="sha aynı olsa da yeniden yaz")
    a = ap.parse_args(argv)
    kasa = Path(a.kasa)
    durum_yol, alt_yol = kasa / ".beyin/durum.json", kasa / ".beyin/alt.json"
    durum = json.loads(durum_yol.read_text(encoding="utf-8")) if durum_yol.exists() else {}
    onbellek = json.loads(alt_yol.read_text(encoding="utf-8")) if alt_yol.exists() else {}
    yazilan = atlanan = 0
    harita = {}  # klasör -> [(ad, kaynak, parça)]
    girdiler = []
    for klasor, onek, tur, desen in KAYNAKLAR:
        for yol in sorted(glob.glob(desen)):
            p = Path(yol)
            girdiler.append((klasor, ad_yap(onek, p), str(p), tur, p.read_bytes(), gun(p), "kaynak-birebir"))
    proj = subprocess.run(["video", "projeler"], capture_output=True)
    if proj.returncode == 0 and proj.stdout.strip():
        girdiler.append(("40-projeler", "proje-ozetleri", "video projeler", "proje", proj.stdout,
                         datetime.date.today().isoformat(), "kaynak-birebir"))
    girdiler += ajan_sira() + alt_ajanlar(onbellek) + yonlendir() + kartlar() + gozlemler() + sira_kararlar()
    tadlar = takma_adlar(girdiler)
    for klasor, ad, kaynak, tur, ham, tarih, guven in girdiler:
        metin = GIZLI.sub("[GİZLİ]", ham.decode("utf-8", "replace"))
        bag = sorted((t, tadlar[t]) for t in kelimeler(metin) & tadlar.keys())
        sha = hashlib.sha256((metin + json.dumps(bag)).encode()).hexdigest()[:16]
        eski = durum.get(kaynak, {})
        if not a.zorla and eski.get("sha") == sha and (kasa / klasor / f"{ad}--1.md").exists():
            atlanan += 1
            sayi = eski["parca"]
        else:
            sayi = kaynak_al(kasa, klasor, ad, kaynak, metin, tarih, tur, eski.get("parca", 0), guven, tadlar)
            durum[kaynak] = {"sha": sha, "parca": sayi, "klasor": klasor, "ad": ad}
            yazilan += 1
        harita.setdefault(klasor, []).append((ad, kaynak, sayi))
    # kaynağı silinmiş notlar: bakım tespit eder, burada dokunulmaz
    bugun = datetime.date.today().isoformat()
    endeks = ["---", "tur: moc", f"guncellenme: {bugun}", "etiket: [moc]", "---", "# Beyin haritası", "",
              "Arama: `python tools/beyin.py ara \"<soru>\" --k 5`", ""]
    for klasor in sorted(harita):
        endeks.append(f"- [[index-{klasor}]] — {len(harita[klasor])} kaynak")
        yaz(kasa / klasor / f"index-{klasor}.md", "\n".join(
            ["---", "tur: moc", f"guncellenme: {bugun}", f"etiket: [moc, {klasor}]", "---", f"# {klasor}", ""]
            + [f"- [[{ad}--1]] — `{k}` ({n} parça)" for ad, k, n in harita[klasor]] + ["", "[[index]]"]) + "\n")
    yaz(kasa / "index.md", "\n".join(endeks) + "\n")
    for k in ("00-cekirdek", "90-log"):
        (kasa / k).mkdir(exist_ok=True)
    # günlük not şablonu (Obsidian çekirdek Daily notes + Templates); varsa dokunulmaz
    for yol, icerik in ((kasa / "_sablon/gunluk.md", SABLON),
                        (kasa / ".obsidian/daily-notes.json",
                         '{"folder": "90-log", "format": "YYYY-MM-DD", "template": "_sablon/gunluk"}'),
                        (kasa / ".obsidian/templates.json", '{"folder": "_sablon"}')):
        if not yol.exists():
            yaz(yol, icerik)
    simdi = datetime.datetime.now()
    gunluk = kasa / "90-log" / f"{simdi.date()}.md"
    if not gunluk.exists():
        yaz(gunluk, SABLON.replace("{{date:YYYY-MM-DD}}", bugun))
    with open(gunluk, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- {simdi:%H:%M} beyin_al: {yazilan} yazıldı, {atlanan} değişmedi\n")
    yaz(durum_yol, json.dumps(durum, ensure_ascii=False, indent=1))
    yaz(alt_yol, json.dumps(onbellek, ensure_ascii=False))
    print(f"beyin_al: {yazilan} kaynak yazıldı, {atlanan} değişmedi, {len(tadlar)} takma ad, kasa {kasa}")
    if not a.qmd_yok:
        qmd = shutil.which("qmd")  # Windows'ta qmd.cmd; düz "qmd" bulunmaz
        cols = subprocess.run([qmd, "collection", "list"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stdout
        if "qmd://beyin/" not in cols:
            subprocess.run([qmd, "collection", "add", str(kasa), "--name", "beyin",
                            "--mask", "**/*.md"], check=True, capture_output=True)
        subprocess.run([qmd, "update"], check=True, capture_output=True)
        print("qmd: beyin koleksiyonu güncel")


if __name__ == "__main__":
    sys.exit(main())
