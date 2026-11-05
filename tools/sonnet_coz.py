"""SONNET-COZ (5 Kas, Ömer: "ücretsiz model yok, ya sen ya Sonnet — hata istemiyorum").
Kapsam: ana-liste'de arac+kutuphane+ui-kutuphane, durum KURULMADI-SIRADA/BULUNAMADI/KAYITSIZ/KURULU-KANITSIZ/KURULUM-HATA (KAPSAM=tam).
Her kalemin kurulum kaynağı video raporu + GitHub linkleriyle Claude Sonnet (claude -p, high) tarafından yeniden çözülür.
Çıktı: .kos/kopru/kurulum-coz.jsonl'a kaynak="sonnet" kayıtları (en_iyi sonnet'i önceler) + .kos/kopru/sonnet-coz.log
Sonra: indir -> kurulum_eksik -> kalem_denetim. Yeniden başlatılırsa kaldığı yerden devam eder.
"""
import json, os, re, subprocess, sys, time, threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
os.environ["KAPSAM"] = "tam"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "tools"))
import kurulum_coz2 as K  # noqa: E402

LOG = os.path.join(KOK, ".kos", "kopru", "sonnet-coz.log")
C = os.path.expanduser(r"~\.local\bin\claude.exe")
BOS = os.path.join(os.environ.get("TEMP", KOK), "sonnet_coz_cwd")
os.makedirs(BOS, exist_ok=True)
kilit = threading.RLock()
PARALEL = 12
VIDEO_BASI = 8

ISTEM = """You resolve install sources for tools/libraries mentioned in short videos. For EACH video below and EACH listed item,
return the real install source. Use the video report text and GitHub links shown; otherwise use your own knowledge of the real project.
Return ONLY one JSON object: {"<video_id>": {"<item exactly as written>": "<value>", ...}, ...}
value formats:
- "gh:owner/repo"  the item's real GitHub repository (exact owner and repo spelling; slash commands / sub-skills -> repo of the package they belong to)
- "npm:package" | "pypi:package"  when installed from a registry and you are not sure of the GitHub repo
- "site:domain"  hosted service / web app with no installable repo
- "cc:yerlesik"  Claude Code built-in command or feature (/clear /compact /effort /btw /add-dir /branch ...)
- "genel:category"  general concept or technology, not one installable thing (".NET", "GitHub", "Instagram", "Claude", "RAG", "API")
- "bilinmiyor:" + short reason   if you genuinely cannot identify it
Never invent a repository. If an item could be several projects, choose the one the report context points to; if still ambiguous use "bilinmiyor:belirsiz".

{bloklar}"""


def yaz(*a):
    s = time.strftime("%H:%M:%S ") + " ".join(str(x) for x in a)
    print(s, flush=True)
    with kilit:
        open(LOG, "a", encoding="utf-8").write(s + "\n")


def sonnet(istem, model="sonnet"):
    # Hızlı mod (5 Kas ölçüm: 67.7 sn -> 3.8 sn açılış): kullanıcı ayarı/hook/plugin/skill/MCP/araç yüklenmez, OAuth aynı.
    # NİHAİ 49: Sonnet 3 denemede çözemezse son BOSS Opus 5.5 medium.
    argv = [C, "-p", "--output-format", "text", "--model", model, "--effort", "high" if model == "sonnet" else "medium", "--strict-mcp-config",
            "--disable-slash-commands", "--no-session-persistence", "--setting-sources", "local", "--tools", ""]
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY") and k != "CLAUDE_CODE_EFFORT_LEVEL"}
    import tempfile
    for deneme in range(3):
        gir = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False, dir=BOS)
        gir.write(istem); gir.close()
        cik_yol = gir.name + ".out"
        try:
            with open(gir.name, encoding="utf-8") as fi, open(cik_yol, "w", encoding="utf-8") as fo:
                p = subprocess.Popen(argv, stdin=fi, stdout=fo, stderr=subprocess.STDOUT, cwd=BOS, env=env, creationflags=0x08000000)
                try:
                    p.wait(timeout=900)
                except subprocess.TimeoutExpired:
                    subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
                    yaz("zaman-asimi", deneme)
            out = open(cik_yol, encoding="utf-8", errors="replace").read()
            if len(out) < 300 and re.search(r"(?i)usage limit|limit reached|resets? (at|in)", out):
                yaz("plan-limiti", model, out[-150:].replace("\n", " "))
                time.sleep(600)
                continue
            m = re.search(r"\{.*\}", out, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception as e:
                    yaz("json-bozuk", deneme, str(e)[:80])
            else:
                yaz("cevap-json-yok", deneme, p.returncode, out[-200:].replace("\n", " "))
        except Exception as e:
            yaz("hata", deneme, str(e)[:150])
        finally:
            for f in (gir.name, cik_yol):
                try:
                    os.remove(f)
                except OSError:
                    pass
        time.sleep(15 * (deneme + 1))
    if model == "sonnet":
        yaz("boss: opus medium'a yukseltildi")
        return sonnet(istem, "opus")
    return None


def main():
    satir = K.bekleyen()
    grup = defaultdict(list)
    for s in satir:
        vids = [v for v in (s.get("kaynak_video_idleri") or "").split(",") if v]
        grup[vids[0] if vids else "_yok"].append(s["kalem"])
    bitti = set()
    for l in open(K.COZ, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(l)
        except Exception:
            continue
        if r.get("kaynak") == "sonnet":
            for kl in (r.get("eslesme") or {}):
                bitti.add((r["video"], kl))
    isler = [(v, [x for x in ks if (v, x) not in bitti]) for v, ks in grup.items()]
    isler = [x for x in isler if x[1]]
    idx = K.rapor_dizini()
    paket = [isler[i:i + VIDEO_BASI] for i in range(0, len(isler), VIDEO_BASI)]
    yaz("kapsam kalem", len(satir), "kalan video", len(isler), "kalan kalem", sum(len(x[1]) for x in isler), "cagri", len(paket))
    say = [0, 0]

    def f(pk):
        bloklar = []
        for v, ks in pk:
            metin = K.oku(idx.get(v, []), 5000) if v != "_yok" else ""
            gh = sorted({f"{a}/{b}" for a, b in K.GH.findall(metin)})
            bloklar.append(f"### VIDEO {v}\nITEMS:\n" + "\n".join("- " + x for x in ks) + ("\nGITHUB LINKS: " + ", ".join(gh) if gh else "") +
                           "\nREPORT:\n" + (metin or "(no report)"))
        sonuc = sonnet(ISTEM.replace("{bloklar}", "\n\n".join(bloklar))) or {}
        for v, ks in pk:
            es_m = sonuc.get(v) or {}
            metin = K.oku(idx.get(v, []), 9000).lower() if v != "_yok" else ""
            es, kanit = {}, {}
            for x in ks:
                d = es_m.get(x)
                if not isinstance(d, str):
                    continue
                es[x] = d
                if d.startswith("gh:"):
                    full = d[3:].strip().strip("/").lower()
                    kanit[x] = "raporda" if (full in metin or full.replace("/", " / ") in metin) else "sonnet-bilgisi"
            if es:
                with kilit:
                    open(K.COZ, "a", encoding="utf-8").write(json.dumps({"video": v, "kaynak": "sonnet", "rapor_var": bool(metin), "eslesme": es, "kanit": kanit}, ensure_ascii=False) + "\n")
            with kilit:
                say[1] += len(es)
        with kilit:
            say[0] += 1
            if say[0] % 3 == 0:
                yaz(say[0], "/", len(paket), "cagri; cozulen kalem", say[1])

    with ThreadPoolExecutor(PARALEL) as ex:
        list(ex.map(f, paket))
    yaz("BITTI-SONNET", say)


def adim(ad, args):
    yaz(ad, "başladı")
    with open(LOG, "a", encoding="utf-8") as fl:
        rc = subprocess.run([sys.executable, "-u"] + args, cwd=KOK, env=dict(os.environ, PYTHONIOENCODING="utf-8"), stdout=fl, stderr=subprocess.STDOUT,
                            creationflags=0x08000000, timeout=7200).returncode
    yaz(ad, "bitti rc", rc)
    if rc != 0:  # ECC H6: basarisiz adim sonrakini baslatmaz
        yaz("DUR", ad, "rc", rc)
        sys.exit(rc)


if __name__ == "__main__":
    main()
    if "--yalniz-coz" not in sys.argv:
        adim("INDIR", ["tools/kurulum_coz2.py", "indir"])
        adim("EKSIK", ["tools/kurulum_eksik.py"])
        adim("DENETIM", ["tools/kalem_denetim.py"])
        yaz("SONNET-HAT-BITTI")
