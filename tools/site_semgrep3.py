"""KAYNAK-SITE-3 adim 4: kurulum-ek-site.tsv'de semgrep_ERROR>0 repolari tek tek tara (--max-memory 1500), bulgulari sinifla:
zararli (kotu niyet kurallari / gizlenmis yurutme / uzaktan betik indir-calistir) | ornek-test (test/example/docs/fixture/vendor yolu) | yanlis-alarm (kalan, tipik zafiyet kurali = kodlama hatasi, kotu niyet degil).
Cikti: .kos/kopru/ara/semgrep3/<repo>.json, docs/site-inceleme/semgrep-sinif.tsv, guvenlik-ret.tsv (zararli). Yeniden baslatilabilir. RAM>=%75 ise bekler. Claude yok."""
import csv, json, os, re, subprocess, sys, time
from pathlib import Path
KOK = Path(__file__).resolve().parents[1]
TSV = KOK / "docs/site-inceleme/kurulum-ek-site.tsv"
CIK = KOK / ".kos/kopru/ara/semgrep3"
HEDEF = Path(r"C:\AI\indirilen")
YOL_ORNEK = re.compile(r"(^|[\\/])(tests?|__tests__|spec|specs|examples?|demos?|docs?|fixtures?|samples?|vendor|node_modules|third[_-]party|benchmarks?|e2e|mocks?|stories|playground|\.github)([\\/]|$)|\.(test|spec|stories)\.|\.md$|\.min\.js$", re.I)
KURAL_ZARARLI = re.compile(r"(backdoor|malware|malicious|exfil|reverse-shell|cryptominer|crypto-?min|obfuscat|eval-?base64|base64-?exec|curl.*(sh|bash)|wget.*(sh|bash)|keylog|stealer|webhook-?exfil|discord-?webhook|pastebin)", re.I)


def ram():
    r = subprocess.run(["powershell", "-NoProfile", "-c", "(Get-CimInstance Win32_OperatingSystem|%{[int](100-100*$_.FreePhysicalMemory/$_.TotalVisibleMemorySize)})"], capture_output=True, text=True)
    try:
        return int(r.stdout.strip())
    except ValueError:
        return 0


def tara(ad):
    yol = HEDEF / ad.replace("/", "__")
    cik = CIK / (ad.replace("/", "__") + ".json")
    if cik.exists():
        return json.loads(cik.read_text(encoding="utf-8"))
    while ram() >= 88:  # ASKI-1: eski esik 75 iken RAM %79'da sonsuz bekliyordu; proje tavani 90 (ram_bekci 88/86)
        print("  ram bekle", ad, flush=True)
        time.sleep(30)
    print("  basla", ad, flush=True)
    try:
        pr = subprocess.Popen(["semgrep", "--config", "auto", "--severity", "ERROR", "--json", "--quiet", "--max-memory", "1500", "--timeout", "20", str(yol)],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
        try:
            out, _ = pr.communicate(timeout=300)
        except subprocess.TimeoutExpired:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(pr.pid)], capture_output=True)  # semgrep-core yetim kalmasin
            raise
        res = json.loads(out)["results"]
    except Exception as e:
        res = None
        hata = type(e).__name__
    if res is None:
        d = {"repo": ad, "hata": hata}
    else:
        say = {"zararli": 0, "ornek-test": 0, "yanlis-alarm": 0}
        kural = {}
        for b in res:
            rid, p = b["check_id"], b["path"]
            s = "zararli" if KURAL_ZARARLI.search(rid) or KURAL_ZARARLI.search(b.get("extra", {}).get("message", "")[:200]) else "ornek-test" if YOL_ORNEK.search(os.path.relpath(p, yol) if os.path.isabs(p) else p) else "yanlis-alarm"
            say[s] += 1
            kural.setdefault(s, {}).setdefault(rid.split(".")[-1], 0)
            kural[s][rid.split(".")[-1]] += 1
        d = {"repo": ad, "say": say, "kural": {k: sorted(v.items(), key=lambda x: -x[1])[:3] for k, v in kural.items()}}
    cik.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return d


def main():
    CIK.mkdir(parents=True, exist_ok=True)
    hed = [r["ad"] for r in csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t") if r["durum"] == "indirildi" and re.search(r"semgrep_ERROR=([1-9]\d*)", r["tarama"])]
    if "--ters" in sys.argv:
        hed.reverse()
    print("hedef", len(hed), flush=True)
    son = []
    for i, ad in enumerate(hed):
        son.append(tara(ad))
        print(i + 1, ad, son[-1].get("say") or son[-1].get("hata"), flush=True)
    with open(KOK / "docs/site-inceleme/semgrep-sinif.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["repo", "zararli", "ornek-test", "yanlis-alarm", "ornek-kural", "hata"])
        for d in son:
            s = d.get("say", {})
            ork = ";".join(x[0] for v in d.get("kural", {}).values() for x in v[:1])
            w.writerow([d["repo"], s.get("zararli", ""), s.get("ornek-test", ""), s.get("yanlis-alarm", ""), ork, d.get("hata", "")])
    ret = [d for d in son if d.get("say", {}).get("zararli")]
    with open(KOK / "docs/site-inceleme/guvenlik-ret.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["repo", "zararli_bulgu", "kural"])
        for d in ret:
            w.writerow([d["repo"], d["say"]["zararli"], ";".join(x[0] for x in d["kural"].get("zararli", []))])
    print("zararli repo", len(ret))


main()
