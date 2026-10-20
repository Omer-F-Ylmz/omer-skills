"""TOKEN-REA d12 CANLI erken devir A/B: eşli görev, A = tek oturum, B = yarıda devir notu (dosya) + taze oturum.
Görev betikle üretilir (tohum → rastgele repo .py dosyaları, anahtar = regex sayımı); geliştirici içeriği okumaz. Kalite = anahtara tam uyan satır oranı.
Bağlam eşiği `claude -p` içinde ölçülemediği için eşik = dosya sayısının yarısı (vekil); sim (devir_sim.py) 120k eşikle −%68 verir.
En fazla CAGRI_TAVAN `claude -p` (3 görev x (1 + 2) = 9).
Kullanım: python -I devir_ab.py [tohum]   → devir_ab_<tohum>.json"""
import json, random, re, subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
NOT_DIZIN = Path(__file__).with_name("devir_notlar")
CAGRI_TAVAN, GOREV, DOSYA_N, MAKS_TUR = 10, 3, 14, "40"
IZIN = ["--permission-mode", "acceptEdits", "--allowedTools", "Read", "Write", "Glob"]  # Bash/Grep kapalı: sayım yalnız Read ile
GOREV_METNI = ("GÖREV: Aşağıdaki dosyaları SIRAYLA, her birini Read aracıyla baştan sona oku (Grep/Bash kullanma, alt ajan çağırma). "
               "Her dosya için: satır başında (girintili olabilir) `def` ya da `async def` ile başlayan satır sayısı ve dosyadaki SON bu tür tanımın adı. "
               "Son yanıtın SON bölümü tam olarak şu biçimde olsun: her dosya için `DOSYA|<yol>|<sayı>|<son ad>` satırı (dosya sırasıyla), en sonda `TOPLAM=<sayıların toplamı>`.\n"
               "Dosyalar:\n{liste}\n")
DEVIR_METNI = ("\nÖNEMLİ: yalnız İLK {k} dosyayı işle, sonra DUR. Bağlam dolmak üzere: {yol} dosyasına Write ile devir notu yaz — yeni, taze bir oturum "
               "YALNIZ bu notla işi bitirecek (görev tanımı, çıktı biçimi, TÜM dosya listesi, şu ana kadarki dosya başına değerler, sıradaki adım). "
               "Yanıtının son satırı tam olarak DEVIR-HAZIR olsun.")
DEVAM_METNI = "Devam: {yol} devir notunu oku ve notta anlatılan işi kaldığın yerden bitir; nottaki biçimle son yanıtı ver."


def gorevler(tohum):
    adaylar = []
    for y in subprocess.run(["git", "ls-files", "*.py"], cwd=KOK, capture_output=True, text=True, encoding="utf-8").stdout.split():
        try:
            m = (KOK / y).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if 120 <= len(m.splitlines()) <= 290 and "devir_ab" not in y:  # >300 satır ilk Read kancada reddedilir
            adaylar.append((y, m))
    rnd = random.Random(tohum)
    sec = rnd.sample(adaylar, GOREV * DOSYA_N)
    out = []
    for i in range(GOREV):
        L = sec[i * DOSYA_N:(i + 1) * DOSYA_N]
        anahtar = []
        for y, m in L:
            d = re.findall(r"(?m)^\s*(?:async\s+)?def\s+(\w+)", m)
            anahtar.append((y, len(d), d[-1] if d else "-"))
        out.append((f"g{i + 1}", anahtar))
    return out


def istem_liste(anahtar):
    return "\n".join(f"{i + 1}. {y}" for i, (y, _, _) in enumerate(anahtar))


def kalite(yanit, anahtar):
    dogru = 0
    for y, n, son in anahtar:
        dogru += bool(re.search(rf"DOSYA\|{re.escape(y)}\|{n}\|{re.escape(son)}\b", yanit))
    dogru += bool(re.search(rf"TOPLAM={sum(n for _, n, _ in anahtar)}\b", yanit))
    return round(dogru / (len(anahtar) + 1), 3)


sayac = 0


def kos(istem):
    global sayac
    sayac += 1
    assert sayac <= CAGRI_TAVAN, "claude -p tavanı"
    t = time.time()
    p = subprocess.run(["claude", "-p", "--output-format", "json", "--model", "sonnet", "--max-turns", MAKS_TUR, "--disable-slash-commands",
                        "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', *IZIN], input=istem, capture_output=True, text=True,
                       encoding="utf-8", cwd=KOK, timeout=1200, creationflags=0x08000000)
    j = json.loads(p.stdout)
    mu = j.get("modelUsage", {}).values()
    return {"girdi": sum(m.get("inputTokens", 0) + m.get("cacheReadInputTokens", 0) + m.get("cacheCreationInputTokens", 0) for m in mu),
            "agirlikli": round(sum(m.get("inputTokens", 0) + .1 * m.get("cacheReadInputTokens", 0) + 1.25 * m.get("cacheCreationInputTokens", 0) + 5 * m.get("outputTokens", 0) for m in mu)),
            "tur": j.get("num_turns") or 0, "sn": round(time.time() - t), "usd": j.get("total_cost_usd") or 0, "yanit": j.get("result") or ""}


def topla(rs):
    return {k: sum(r[k] for r in rs) for k in ("girdi", "agirlikli", "tur", "sn", "usd")}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tohum = sys.argv[1] if len(sys.argv) > 1 else "20102101"
    cikti = Path(__file__).with_name(f"devir_ab_{tohum}.json")
    NOT_DIZIN.mkdir(exist_ok=True)
    sonuc = []
    for ad, anahtar in gorevler(tohum):
        temel = GOREV_METNI.format(liste=istem_liste(anahtar))
        a = kos(temel)
        yol = (NOT_DIZIN / f"{tohum}-{ad}.md").relative_to(KOK).as_posix()
        (KOK / yol).unlink(missing_ok=True)
        b1 = kos(temel + DEVIR_METNI.format(k=DOSYA_N // 2, yol=yol))
        not_var = (KOK / yol).exists() and "DEVIR-HAZIR" in b1["yanit"]
        b2 = kos(DEVAM_METNI.format(yol=yol)) if not_var else None
        b = topla([b1, b2] if b2 else [b1])
        r = dict(gorev=ad, A=dict(topla([a]), kalite=kalite(a["yanit"], anahtar)),
                 B=dict(b, kalite=kalite(b2["yanit"], anahtar) if b2 else 0.0, not_var=not_var, cagri=2 if b2 else 1), A_yanit=a["yanit"][-600:], B_yanit=(b2 or b1)["yanit"][-600:])
        sonuc.append(r)
        cikti.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(ad, "A", r["A"], "B", r["B"], flush=True)
    for k in "AB":
        print(k, {x: round(sum(r[k][x] for r in sonuc), 2) for x in ("girdi", "agirlikli", "tur", "sn", "usd")}, "kalite", round(sum(r[k]["kalite"] for r in sonuc) / len(sonuc), 3))
