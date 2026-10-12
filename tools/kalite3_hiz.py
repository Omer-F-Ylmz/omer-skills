"""KALİTE-3-HIZ: iki aşamalı ajan ölçümü + otomatik onarım. Karar d13 ile AYNI (skill/.kalite3/ajan_jev.karar: Jev ≥ ana VE
regex ≥ ana VE $ ≤ ana × 1.1); değişen yalnız ölçüm sırası/hızı ve ajan onarımı.
Aşama 1 = ajan kolu (+ Jev). ERKEN RET (kalibre: eski veride yanlış ret 0) ise ana kolu koşulmaz → onarım kuyruğu; aksi halde
aşama 2 = ana kolu (ajan tanımına bağlı değil: aynı model için önceki ana satırı yeniden kullanılır → onarım ölçümü tek çağrı).
Onarım: düşen ajan için ölçüm gerekçesi → claude -p tek hedefli düzeltme (açıklama/talimat/model; iş ve ad aynı) → aşama 1'den
yeniden; en fazla 2 tur; onarılan tanım yalnız geçerse ajanlar/kalite3/<aile>/<ad>.md yerine yazılır.
Eşzamanlılık RAM'e göre (< %85 artır, ≥ %92 azalt, tavan 6); `tools:` alanında mcp__ yoksa boş MCP (--strict-mcp-config).
  python tools/kalite3_hiz.py kalibre | parite | durum | kos
Bütçe: claude -p ≤ CAGRI_TAVAN (cagri.log satırları, yeniden başlatmada sürer)."""
import csv, json, re, shutil, subprocess, sys, threading, time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import model_olc as mo  # noqa: E402
from olcum import kosucu  # noqa: E402

SKILL = Path("C:/Projeler/omer-skills-wt/skill")  # d13'ün canlı verisi (salt okuma; kabul listesi d13'ün)
sys.path.insert(0, str(SKILL / ".kalite3"))
from ajan_jev import SORU, karar, ortam, Tasiyici  # noqa: E402

KOPRU = Path("C:/Projeler/omer-skills/.kos/kopru")
SIRA_MD = KOPRU / "gorev/SIRA.md"
DUR = KOPRU / "olcum.dur"
ESKI = SKILL / "docs/kutuphane/olcum/kalite3-ajan-pilot-jev.tsv"
ESKI_YANIT = SKILL / ".kalite3/ajan-yanit"
TSV = KOK / "docs/kutuphane/olcum/kalite3-ajan-hiz.tsv"
KABUL_EK = KOK / "docs/kutuphane/kalite3-ajan-kabul-ek.txt"
IS = KOK / ".kalite3/hiz"
CAGRI_TAVAN, ES_TAVAN, TUR_TAVAN, ARDISIK_TAVAN = 1700, 12, 2, 3  # d15 (13 Eki): +800 çağrı (d15 135 + ruflo ≤15 ajan), es x2
STRICT = ["--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']
ALAN = ["aile", "ajan", "kol", "tur", "model", "puan", "usd", "jeton", "alt_model", "sure", "alt_usd", "jev", "strict"]
R_ESIK, J_ESIK, U_PAY = 0.6, 5.0, 1.25  # kalibre(): geçenlerin min r 0.8, min Jev 5.7; $ tavanı = 1.25 × geçenlerin max $'ı
D13_P2 = time.mktime(time.strptime("2026-10-12 09:22:09", "%Y-%m-%d %H:%M:%S"))
EK = [KOK / "ajanlar/kalite3-d15", KOK / "ajanlar/kalite3-ruflo"]  # yeni aday kökleri (gorevler.json + <aile>/<ad>.md), d13 dilimine girmez
kilit = threading.Lock()
gorev = {g["ajan"]: g for k in [mo.AJAN, *EK] if (k / "gorevler.json").exists()
         for g in json.loads((k / "gorevler.json").read_text(encoding="utf-8"))}


class Gecici(Exception):
    """API/Jev hatası: ölçüm sayılmaz, öğe kuyruğa döner."""


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def api_hatasi(o):
    if o["metin"].lstrip().startswith("API Error"):
        raise Gecici(o["metin"].strip()[:120])
    return o


def oku(yol):
    return list(csv.DictReader(yol.open(encoding="utf-8"), delimiter="\t", restval="")) if yol.exists() else []


def usd(a):
    return float(a["alt_usd"]) if a.get("alt_usd") and a["alt_model"] == "claude-haiku-5-5" else float(a["usd"])


def rmax(ad):
    return sum(r["puan"] for r in gorev[ad]["rubrik"])


def u_tavan(eski):
    k, kol = karar(eski), {(s["ajan"], s["kol"]): s for s in eski}
    m = {}
    for ad, ok in k.items():
        if ok:
            md = gorev[ad]["model"]
            m[md] = max(m.get(md, 0), usd(kol[(ad, "ajan")]))
    return {md: U_PAY * v for md, v in m.items()}


def erken_ret(a, model, ut):
    """Aşama 1 gerekçesi (boş = 2. aşamaya geçer)."""
    n = []
    if float(a["puan"]) / rmax(a["ajan"]) < R_ESIK:
        n.append(f"regex {a['puan']}/{rmax(a['ajan'])} < %{R_ESIK * 100:.0f}")
    if float(a["jev"]) < J_ESIK:
        n.append(f"Jev {a['jev']} < {J_ESIK}")
    if model in ut and usd(a) > ut[model]:
        n.append(f"$ {usd(a):.3f} > {ut[model]:.3f} ({model} geçenlerin max'ı × {U_PAY})")
    return "; ".join(n)


def kalibre():
    """Geriye dönük kanıt: eski karar verisinde erken ret kuralı hiçbir GEÇEN'i düşürmüyor mu?"""
    eski = oku(ESKI)
    k, kol, ut = karar(eski), {(s["ajan"], s["kol"]): s for s in eski}, u_tavan(eski)
    yanlis = [ad for ad, ok in k.items() if ok and erken_ret(kol[(ad, "ajan")], gorev[ad]["model"], ut)]
    erken = [ad for ad, ok in k.items() if not ok and erken_ret(kol[(ad, "ajan")], gorev[ad]["model"], ut)]
    print(f"karar {sum(k.values())}/{len(k)} geçti · yanlış ret {len(yanlis)} {yanlis} · erken ret {len(erken)}/{len(k) - sum(k.values())} "
          f"düşen (ana kolu atlanır) · $ tavanı {({m: round(v, 3) for m, v in ut.items()})}")
    return len(yanlis)


class Cagri:
    def __init__(self):
        IS.mkdir(parents=True, exist_ok=True)
        self.yol = IS / "cagri.log"
        self.n = len(self.yol.read_text(encoding="utf-8").splitlines()) if self.yol.exists() else 0

    def kos(self, etiket, *a, **k):
        with kilit:
            self.n += 1
            with self.yol.open("a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%H:%M:%S')} {etiket}\n")
        return kosucu.kos(*a, **k)

    def dene(self, etiket, *a, **k):
        o = self.kos(etiket, *a, **k)
        return o if o["metin"].strip() else self.kos(etiket + " (yeniden)", *a, **k)


cagri = Cagri()


def jev(ad, metin):
    g = gorev[ad]
    kabul = "Yanıt şunları kapsamalı: " + "; ".join(f"{re.sub(r'^[(][?]i[)]', '', r['regex'])} ({r['puan']} puan)" for r in g["rubrik"])
    c = Tasiyici(env=ortam(), en_fazla=2, istek_tavan=12).yargila([{"gorev": g["istem"], "kabul": kabul, "yanit": metin}], SORU)[0]
    return round(c["kalite"]["score"] * 2, 1) if c else ""


def strict_mi(yol):
    return "mcp__" not in next((s for s in yol.read_text(encoding="utf-8").split("---", 2)[1].splitlines() if s.startswith("tools:")), "")


def olc(ad, kol, tur, yol, model, aile):
    g, s = gorev[ad], strict_mi(yol)
    ek = STRICT if s else []
    if kol == "ajan":
        _, t = mo.tanim(yol, model)
        istem = f"Delegate this task to the {ad} subagent with the Agent tool, then return its answer verbatim.\n\n{g['istem']}"
        o = api_hatasi(cagri.dene(f"{ad} ajan t{tur}", istem, mo.ek(ad, t, model) + ek, model=mo.ana_model(model), butce=1.5))
    else:
        o = api_hatasi(cagri.dene(f"{ad} ana t{tur}", g["istem"], ek, model=model, butce=1.5))
    mu, ana_m = o.get("model") or {}, mo.ana_model(model)
    am = mo.alt(mu, ana_m)[0] if kol == "ajan" else (",".join(sorted(mu)) or "-")
    (IS / "yanit").mkdir(exist_ok=True)
    (IS / "yanit" / f"{ad}-{kol}-t{tur}.md").write_text(o["metin"], encoding="utf-8", newline="\n")
    p = mo.puan(o, g["rubrik"])
    try:
        j = jev(ad, o["metin"]) if p != "hata" else ""
    except Exception as e:  # noqa: BLE001
        raise Gecici(f"Jev {e!r}"[:120]) from e
    a = dict(zip(ALAN, [aile, ad, kol, tur, model, p, round(o["usd"], 4), mo.jeton(mu), am, o["sure"],
                        mo.alt_usd(mu, ana_m) if kol == "ajan" else "", j, int(s)]))
    with kilit:
        yeni = not TSV.exists()
        with TSV.open("a", encoding="utf-8", newline="\n") as f:
            w = csv.DictWriter(f, fieldnames=ALAN, delimiter="\t", lineterminator="\n")
            if yeni:
                w.writeheader()
            w.writerow(a)
    return a, o["metin"]


ONAR = """You repair ONE Claude Code subagent definition that failed a measurement against doing the same task without the agent.
Pass rule (unchanged): agent answer quality (LLM judge) >= baseline, acceptance-term score >= baseline, cost <= baseline x 1.1.
Keep the agent's `name`, its job and scope identical. Make ONE targeted, GENERAL fix (no facts specific to this one task) in only:
the `description` (when to use), the instruction body, or the `model:` field (haiku|sonnet|opus). Keep the `tools:` line as is.
Cost failure → shorter instructions; tell it to answer directly and use tools/file exploration only when the request needs them;
a cheaper model only if quality allows. Quality failure → instructions that make it cover what such requests need, concretely.
Failure: {neden}
Acceptance terms its answer missed: {eksik}
Its answer (truncated):
{yanit}
Current definition:
{md}
Return ONLY the complete new definition file between a line <<<AJAN and a line AJAN>>>."""


def onar(ad, tur, yol, neden, yanit):
    """Yeni tanım yolu ya da None (biçim bozuksa onarım düşer)."""
    eksik = [re.sub(r"^[(][?]i[)]", "", r["regex"]) for r in gorev[ad]["rubrik"] if not re.search(r["regex"], yanit)]
    istem = ONAR.format(neden=neden, eksik="; ".join(eksik) or "-", yanit=yanit[:3000], md=yol.read_text(encoding="utf-8"))
    o = api_hatasi(cagri.kos(f"{ad} onar t{tur}", istem, STRICT, model="sonnet", butce=1.0))
    m = re.search(r"<<<AJAN\s*\n(.*?)\n\s*AJAN>>>", o["metin"], re.S)
    if not m:
        istem += f"\n\nYour previous reply had no <<<AJAN ... AJAN>>> block. Reply with nothing but:\n<<<AJAN\n---\nname: {ad}\n...\nAJAN>>>"
        o = api_hatasi(cagri.kos(f"{ad} onar t{tur} (biçim)", istem, STRICT, model="sonnet", butce=1.0))
        m = re.search(r"<<<AJAN\s*\n(.*?)\n\s*AJAN>>>", o["metin"], re.S)
    yeni = IS / "onarim" / f"{ad}.t{tur}.md"
    yeni.parent.mkdir(exist_ok=True)
    try:
        assert m, "biçim: <<<AJAN bloğu yok (2 deneme)"
        yeni.write_text(m.group(1).strip() + "\n", encoding="utf-8", newline="\n")
        assert mo.tanim(yeni, "x")[0] == ad
        return yeni
    except Exception as e:  # noqa: BLE001
        log("ONARIM BİÇİM", ad, f"t{tur}", repr(e)[:120])
        return None


def fm_model(yol, varsayilan):
    m = re.search(r"^model:\s*(haiku|sonnet|opus)\s*$", yol.read_text(encoding="utf-8").split("---", 2)[1], re.M)
    return m.group(1) if m else varsayilan


def neden(a, n):
    k = []
    if float(a["jev"]) < float(n["jev"]):
        k.append(f"judge {a['jev']} < baseline {n['jev']}")
    if float(a["puan"]) < float(n["puan"]):
        k.append(f"terms {a['puan']} < baseline {n['puan']}")
    if usd(a) > float(n["usd"]) * 1.1:
        k.append(f"cost ${usd(a):.3f} > baseline ${float(n['usd']):.3f} x 1.1")
    return "; ".join(k)


def sira(kokler=None):
    aileler = {a: [y.stem for y in sorted(a.glob("*.md")) if y.stem in gorev] for k in (kokler or [mo.AJAN]) if k.exists()
               for a in sorted(p for p in k.iterdir() if p.is_dir())}
    return [(a, ads[i]) for i in range(max(map(len, aileler.values()), default=0)) for a, ads in aileler.items() if i < len(ads)]


def es_ayarla(es, r):
    return min(ES_TAVAN, es + 1) if r <= 90 else max(1, es - 1) if r >= 92 else es


class Kosu:
    def __init__(self):
        self.q, self.calisan, self.gecen = deque(), 0, []
        self.ana = {}  # (ajan, model) → ana satırı (eski + yeni)
        self.ut = u_tavan(oku(ESKI))
        self.d12 = set((SKILL / ".kalite3/d12-ajanlar.txt").read_text(encoding="utf-8").split())
        self.p2_bitti, self.ardisik = False, 0
        self.ele_alinan = {s["ajan"] for s in oku(TSV)}
        for s in oku(ESKI) + oku(TSV):
            if s["kol"] == "ana" and s["puan"] != "hata" and s["jev"] != "":
                self.ana[(s["ajan"], s.get("model") or gorev[s["ajan"]]["model"])] = s
        self.gecen = KABUL_EK.read_text(encoding="utf-8").split() if KABUL_EK.exists() else []

    def p2_p3(self):
        """d13 parti 2 = 09:22'de tamamlanmamış ilk 63 ajan (sıra düzeni); parti 3 = kalanı → bu koşu."""
        tam = {}
        for s in oku(SKILL / "docs/kutuphane/olcum/kalite3-ajan-pilot.tsv"):
            y = ESKI_YANIT / f"{s['ajan']}-{s['kol']}.md"
            if y.exists() and y.stat().st_mtime < D13_P2:
                tam.setdefault(s["ajan"], set()).add(s["kol"])
        kalan = [(a, ad) for a, ad in sira() if ad not in self.d12 and tam.get(ad) != {"ajan", "ana"}]
        return kalan[:63], kalan[63:]

    def onarim_tohumu(self):
        """Eski karar verisinde düşen (ve bu koşuda ele alınmamış) ajanlar → onarım t1."""
        eski = oku(ESKI)
        kol = {(s["ajan"], s["kol"]): s for s in eski}
        aile = {ad: a for a, ad in sira()}
        n = 0
        for ad, ok in sorted(karar(eski).items()):
            if ok or ad in self.ele_alinan or ad not in aile:
                continue
            self.ele_alinan.add(ad)
            yanit = (ESKI_YANIT / f"{ad}-ajan.md").read_text(encoding="utf-8", errors="replace")
            self.q.append((ad, 1, aile[ad] / f"{ad}.md", gorev[ad]["model"], aile[ad], (neden(kol[(ad, "ajan")], kol[(ad, "ana")]), yanit)))
            n += 1
        log("onarım kuyruğuna", n, "eski düşen")

    def ek_aday(self):
        """EK köklerindeki (d15, ruflo) henüz ele alınmamış ajanlar → aşama 1 (t0). Kuyruk boşalınca yeniden çağrılır (koşu sırasında
        eklenen kök/gorevler.json yeniden başlatmasız alınır)."""
        for k in EK:
            if (k / "gorevler.json").exists():
                gorev.update((g["ajan"], g) for g in json.loads((k / "gorevler.json").read_text(encoding="utf-8")))
        n = 0
        for a, ad in sira(EK):
            if ad not in self.ele_alinan:
                self.ele_alinan.add(ad)
                self.q.append((ad, 0, a / f"{ad}.md", gorev[ad]["model"], a, None))
                n += 1
        log("yeni aday kuyruğuna", n)

    def gozcu(self):
        """d13 parti 2 bitince zinciri durdur (parti 3 bu koşuda paralel) ve parti 2'nin düşenlerini onarıma al."""
        while not self.p2_bitti:
            sira_md = SIRA_MD.read_text(encoding="utf-8")
            if "d13 zinciri parti 2/3 BİTTİ" in sira_md:
                r = subprocess.run(["powershell", "-NoProfile", "-Command",
                                    "(Get-CimInstance Win32_Process | ? { $_.CommandLine -like '*d13_zincir.py*' -and $_.Name -like 'python*' }).ProcessId"],
                                   capture_output=True, text=True, creationflags=kosucu.PENCERESIZ)
                for pid in r.stdout.split():
                    subprocess.run(["taskkill", "/T", "/F", "/PID", pid], capture_output=True, creationflags=kosucu.PENCERESIZ)
                    log("d13 zinciri durduruldu pid", pid)
                time.sleep(5)
                with kilit:
                    for s in oku(ESKI):
                        if s["kol"] == "ana" and s["puan"] != "hata" and s["jev"] != "":
                            self.ana.setdefault((s["ajan"], gorev[s["ajan"]]["model"]), s)
                    self.onarim_tohumu()
                    self.p2_bitti = True
                if "parti 2/3 sonrası durduruldu" in sira_md:  # yeniden başlatma: satır zaten yazıldı
                    continue
                with SIRA_MD.open("a", encoding="utf-8", newline="\n") as f:
                    f.write(f"- 12 Eki {time.strftime('%H:%M')} KALİTE-3-HIZ: d13 zinciri parti 2/3 sonrası durduruldu; "
                            f"parti 3 + onarım kalite3c paralel kuyruğunda (tools/kalite3_hiz.py)\n")
            time.sleep(20)

    def kabul(self, ad, tur, yol, aile):
        with kilit:
            if tur:
                shutil.copyfile(yol, aile / f"{ad}.md")
            if ad in self.gecen:
                return
            self.gecen.append(ad)
            KABUL_EK.write_text("\n".join(self.gecen) + "\n", encoding="utf-8", newline="\n")
            if len(self.gecen) % 25 == 0:
                tum = KOK / "docs/kutuphane/kalite3-ajan-kabul.txt"
                es = (SKILL / "docs/kutuphane/kalite3-ajan-kabul.txt").read_text(encoding="utf-8").split()
                tum.write_text("\n".join(dict.fromkeys(es + self.gecen)) + "\n", encoding="utf-8", newline="\n")
                with SIRA_MD.open("a", encoding="utf-8", newline="\n") as f:
                    f.write(f"- 12 Eki {time.strftime('%H:%M')} KALİTE-3-HIZ: {len(self.gecen)} GEÇTİ (son 25: {', '.join(self.gecen[-25:])}) → "
                            f"wt kalite3c docs/kutuphane/kalite3-ajan-kabul-ek.txt (+ birleşik kalite3-ajan-kabul.txt, onarılan tanımlar "
                            f"ajanlar/kalite3'te) — Desktop: kalite3c'de kalite_3_uygula --kuru → uygula\n")

    def geri(self, is_, e):
        """API/Jev hatası: öğe kuyruğun başına; art arda ARDISIK_TAVAN hatada olcum.dur yazılır (döngü yeni öğe başlatmaz)."""
        with kilit:
            self.q.appendleft(is_)
            self.ardisik += 1
            log("GERİ", is_[0], f"t{is_[1]}", f"ardışık {self.ardisik}", str(e))
            if self.ardisik >= ARDISIK_TAVAN and not DUR.exists():
                DUR.write_text(f"DURAKLAT (kalite3_hiz {time.strftime('%d.%m %H:%M')}): art arda {self.ardisik} API/Jev hatası, "
                               f"son: {e}\nKaldırma: ağ/OpenRouter düzeldiği doğrulanınca bu dosya silinir.\n", encoding="utf-8")
                log("DURAKLATILDI", DUR)

    def devam(self):
        """Yeniden başlatma: TSV'de son ajan turu düşmüş ama sonraki turu yazılmamış ajanlar (kesilen/İSTİSNA/API hatalı) → sonraki tur.
        TSV'de hiç satırı olmayanları p3/onarim_tohumu zaten kuyruğa alır."""
        aile, son = {ad: a for a, ad in sira([mo.AJAN, *EK])}, {}
        for s in oku(TSV):
            if s["kol"] == "ajan" and s["puan"] != "hata" and s["jev"] != "" and int(s["tur"]) >= int(son.get(s["ajan"], {"tur": -1})["tur"]):
                son[s["ajan"]] = s
        n = 0
        for ad, a in sorted(son.items()):
            t = int(a["tur"])
            if ad in self.gecen or ad not in aile:
                continue
            yol = IS / "onarim" / f"{ad}.t{t}.md" if t else aile[ad] / f"{ad}.md"
            ana = self.ana.get((ad, a["model"]))
            gerekce = neden(a, ana) if ana else erken_ret(a, a["model"], self.ut)
            if ana and karar([a, ana]).get(ad):
                continue
            if not ana and not gerekce:  # ana kolu yazılmamış → aynı tur yeniden
                self.q.append((ad, t, yol, a["model"], aile[ad], None))
            elif t < TUR_TAVAN:
                metin = (IS / "yanit" / f"{ad}-ajan-t{t}.md").read_text(encoding="utf-8", errors="replace")
                self.q.append((ad, t + 1, yol, a["model"], aile[ad], (gerekce, metin)))
            else:
                continue
            n += 1
        log("devam kuyruğuna", n, "yarım ajan")

    def isle(self, ad, tur, yol, model, aile, onceki):
        is_ = (ad, tur, yol, model, aile, onceki)
        try:
            if onceki:
                yol = onar(ad, tur, yol, *onceki)
                if yol is None:
                    return
                model = fm_model(yol, model)
                is_ = (ad, tur, yol, model, aile, None)  # onarılan tanım hazır → geri dönerse yeniden onarılmaz
            a, metin = olc(ad, "ajan", tur, yol, model, aile)
            if a["puan"] == "hata" or a["jev"] == "":
                log("HATA", ad, f"t{tur}", "ajan kolu boş/Jev yok")
                return
            n = self.ana.get((ad, model))
            gerekce = "" if n else erken_ret(a, model, self.ut)
            if not n and not gerekce:
                n, _ = olc(ad, "ana", tur, yol, model, aile)
                if n["puan"] == "hata" or n["jev"] == "":
                    log("HATA", ad, f"t{tur}", "ana kolu")
                    return
                with kilit:
                    self.ana[(ad, model)] = n
            with kilit:
                self.ardisik = 0
            ok = not gerekce and karar([a, n]).get(ad, False)
            gerekce = gerekce or neden(a, n)
            log("GECTI" if ok else ("ERKEN RET" if not n else "DÜŞTÜ"), ad, f"t{tur}", model, gerekce)
            if ok:
                self.kabul(ad, tur, yol, aile)
            elif tur < TUR_TAVAN:
                with kilit:
                    self.q.append((ad, tur + 1, yol, model, aile, (gerekce, metin)))
        except Gecici as e:
            self.geri(is_, e)
        except Exception as e:  # noqa: BLE001
            log("İSTİSNA", ad, f"t{tur}", repr(e)[:300])
        finally:
            with kilit:
                self.calisan -= 1

    def kos(self):
        sys.stdout.reconfigure(encoding="utf-8")
        p2, p3 = self.p2_p3()
        for a, ad in p3:
            if ad not in self.ele_alinan:
                self.ele_alinan.add(ad)
                self.q.append((ad, 0, a / f"{ad}.md", gorev[ad]["model"], a, None))
        log(f"parti 3 (bu koşu) {len(p3)} ajan · d13 parti 2 {len(p2)} · çağrı {cagri.n}/{CAGRI_TAVAN}")
        self.onarim_tohumu()
        self.devam()
        self.ek_aday()
        threading.Thread(target=self.gozcu, daemon=True).start()
        es, ayar = 4, 0
        with ThreadPoolExecutor(ES_TAVAN) as havuz:
            while True:
                with kilit:
                    bos, cal = not self.q, self.calisan
                if bos and cal == 0 and self.p2_bitti:
                    with kilit:
                        self.ek_aday()
                    if not self.q:
                        break
                r = mo.ram()
                if time.time() - ayar > 45:
                    es = es_ayarla(es, r)
                    ayar = time.time()
                if not bos and cal < es and r < 92 and not DUR.exists() and cagri.n < CAGRI_TAVAN - 3 * ES_TAVAN:
                    with kilit:
                        is_ = self.q.popleft()
                        self.calisan += 1
                    havuz.submit(self.isle, *is_)
                    log(f"başlat {is_[0]} t{is_[1]} · es {es} çalışan {cal + 1} RAM %{r} kuyruk {len(self.q)} çağrı {cagri.n}")
                    continue
                time.sleep(3)
        log(f"BİTTİ · geçen {len(self.gecen)} · çağrı {cagri.n}")


def parite(n=6):
    """Boş MCP kalite eşitliği: eski karar verisinden n geçen + n düşen ajan, iki kol boş MCP ile yeniden → eski ile kıyas.
    Ölçüt (önceden): karar uyuşması ≥ 10/12 VE ortalama Jev farkı |Δ| ≤ 0.5."""
    global TSV
    TSV = KOK / "docs/kutuphane/olcum/kalite3-ajan-hiz-parite.tsv"
    eski = oku(ESKI)
    k, kol, aile = karar(eski), {(s["ajan"], s["kol"]): s for s in eski}, {ad: a for a, ad in sira()}
    sec = [ad for ok in (True, False) for ad in sorted(a for a, v in k.items() if v == ok and a in aile)[::3][:n]]
    yap = {s["ajan"] + s["kol"] for s in oku(TSV)}
    with ThreadPoolExecutor(4) as h:
        for ad in sec:
            for kl in ("ajan", "ana"):
                if ad + kl not in yap:
                    h.submit(olc, ad, kl, "p", aile[ad] / f"{ad}.md", gorev[ad]["model"], aile[ad])
    yeni = oku(TSV)
    ky = karar(yeni)
    uy = sum(ky.get(ad) == k[ad] for ad in sec)
    dj = [float(s["jev"]) - float(kol[(s["ajan"], s["kol"])]["jev"]) for s in yeni if s["jev"] != ""]
    dp = [float(s["puan"]) - float(kol[(s["ajan"], s["kol"])]["puan"]) for s in yeni if s["puan"] != "hata"]
    ort = sum(dj) / max(1, len(dj))
    print(f"parite: karar uyuşması {uy}/{len(sec)} · ort ΔJev {ort:+.2f} · ort Δregex {sum(dp) / max(1, len(dp)):+.2f} · "
          f"boş MCP {sum(s['strict'] == '1' for s in yeni)}/{len(yeni)} satır · {'EŞİT' if uy >= 10 and abs(ort) <= 0.5 else 'EŞİT DEĞİL'}")
    for ad in sec:
        print(" ", ad, "eski", k[ad], "yeni", ky.get(ad))


def durum():
    s = oku(TSV)
    gec = KABUL_EK.read_text(encoding="utf-8").split() if KABUL_EK.exists() else []
    tur = {}
    for x in s:
        if x["kol"] == "ajan":
            tur[x["tur"]] = tur.get(x["tur"], 0) + 1
    print(f"geçen (kabul-ek) {len(gec)} · ajan kolu ölçümü tur başına {tur} · ana {sum(x['kol'] == 'ana' for x in s)} · çağrı {Cagri().n}/{CAGRI_TAVAN}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = sys.argv[1] if len(sys.argv) > 1 else "durum"
    if k == "kalibre":
        sys.exit(kalibre())
    elif k == "parite":
        parite()
    elif k == "kos":
        Kosu().kos()
    else:
        durum()
