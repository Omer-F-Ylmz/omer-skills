"""TOKEN-12: kaynaksız 87 agency-agents ajanının description'ı sıkışır — TOKEN-10 araçları (ajan_sikistir, kapi10) docs/token-12 ile.
  python token12.py envanter               → docs/token-12/aciklama.tsv (ad, kr, yol) + orijinal.tsv (tam metin; geri alma + katalog)
  python token12.py uret [parti...]        → claude -p sonnet, parti başına 1 çağrı → uret_<n>.json
  python token12.py denetle                → uret_*.json + onar.json → esleme.tsv; kural ihlalleri
  python token12.py onek|kapi|kor|sonuc    → kapi10 akışı; 30 görev (17'si agency-agents alanı), tur payı +1
Canlı ~/.claude'a yazmaz; ANTHROPIC_API_KEY alt sürece verilmez."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
sys.path.insert(0, str(Path(__file__).parent))
import ajan_sikistir, kapi10  # noqa: E402
from ajan_aciklama import EV, aciklama, kaynaklar  # noqa: E402

WT = Path(__file__).resolve().parents[2]
CIK = WT / "docs/token-12"
GOREV = [  # agency-agents alanı (17)
    "Our AWS bill jumped 40% last quarter; set up cost allocation tags, find rightsizing wins and decide on savings plans.",
    "Add enterprise SSO with SAML and SCIM user provisioning to our multi-tenant SaaS.",
    "Integrate Stripe subscriptions with SCA/3DS and make webhook handling idempotent with daily reconciliation.",
    "Build a collaborative text editor where several users edit the same document offline and merge without conflicts.",
    "Our OpenSearch product search returns irrelevant results; tune analyzers and BM25, add hybrid vector retrieval, measure with nDCG.",
    "Compile our Rust image-processing library to WebAssembly and cut the JS boundary marshalling overhead.",
    "Set up fastlane to sign, build and ship our iOS and Android apps with phased store rollouts.",
    "Our Electron app needs code signing, macOS notarization and a safe auto-update pipeline.",
    "We have 20k field sensors; design device provisioning, MQTT telemetry and staged OTA firmware updates with rollback.",
    "Write SIEM detection rules mapped to MITRE ATT&CK for suspicious PowerShell activity and tune false positives.",
    "An API key was found in a public GitHub repo; handle the leak, rotate credentials and move secrets into a vault.",
    "Localize our React app into Arabic and Polish: ICU plural messages, RTL layout and pseudo-localization tests.",
    "Build an HLS/DASH adaptive bitrate ladder with ffmpeg and tune the player for low-latency live streams.",
    "Our RAG chatbot retrieves the wrong chunks; fix chunking, add re-ranking and build a retrieval eval set.",
    "Write FreeRTOS firmware for an STM32 sensor board with low-power sleep and a reliable UART protocol.",
    "Audit this Solidity lending contract for reentrancy and oracle manipulation before mainnet launch.",
    "Write AI image-generation prompts for a product photoshoot of a ceramic mug in natural window light.",
] + kapi10.GOREV[-13:]  # TOKEN-10 kapısından 13: kendi ajanlarımıza düşen işler kaymasın

ajan_sikistir.CIK = kapi10.CIK = CIK
ajan_sikistir.PARTI = [["design", "security"], ["engineering"]]
kapi10.GOREV, kapi10.ISTEM, kapi10.TUR_PAY = GOREV, kapi10.istem(GOREV), 1
ONARIM = {s.split("\t")[0]: s.split("\t")[2] for s in (CIK / "onarim.tsv").read_text(encoding="utf8").splitlines()[1:] if s.strip()}  # d4 (b): kendi ajanlarımız, iki kolda


def onar(kok):
    for ad, d in ONARIM.items():
        p = kok / "agents" / f"{ad}.md"
        p.write_text(kapi10.aciklama_degistir(p.read_text(encoding="utf8"), d), encoding="utf8", newline="")
    return len(ONARIM)


_kur, _b = kapi10.kur, kapi10.b_ajanlar


def kur(kok, *a):  # A: agents junction → kopya + onarım (B'de b_ajanlar kopyalar)
    _kur(kok, *a)
    if kok.name == "A" and ONARIM:
        kapi10.os.rmdir(kok / "agents")
        kapi10.shutil.copytree(kapi10.EV / "agents", kok / "agents")
        print("A onarım", onar(kok), flush=True)


kapi10.kur, kapi10.b_ajanlar = kur, lambda kok: _b(kok) + onar(kok)


def yabanci():
    kay = kaynaklar(WT)
    return {p.stem: p for p in sorted(EV.glob("*.md")) if p.stem not in kay}


if __name__ == "__main__":
    CIK.mkdir(parents=True, exist_ok=True)
    y = yabanci()
    eski = {k: aciklama(p.read_text(encoding="utf8")) or "" for k, p in y.items()}
    is_ = sys.argv[1]
    if is_ == "envanter":
        assert not any("\t" in v or "\n" in v for v in eski.values())
        (CIK / "aciklama.tsv").write_text("ad\tkr\tyol\n" + "".join(f"{k}\t{len(eski[k])}\t{p.as_posix()}\n" for k, p in y.items()), encoding="utf8")
        (CIK / "orijinal.tsv").write_text("ad\taciklama\n" + "".join(f"{k}\t{v}\n" for k, v in eski.items()), encoding="utf8")
        print("ajan", len(y), "· kr", sum(map(len, eski.values())), "· >120", sum(len(v) > 120 for v in eski.values()))
    elif is_ == "uret":
        for no in map(int, sys.argv[2:] or range(len(ajan_sikistir.PARTI))):
            ajan_sikistir.uret(no, eski)
    elif is_ == "denetle":
        sys.exit(1 if ajan_sikistir.denetle(eski) else 0)
    elif is_ == "karar":  # koşu: (A kapı, B kapı, ek) → anahtar<ek>.json + puan<ek>.json; d3 karar kuralı
        import json, re
        sik = {l.split("\t")[0] for l in (CIK / "esleme.tsv").read_text(encoding="utf8").splitlines()[1:] if l}
        ad = {m.group(1).strip(): k for k, p in y.items() if (m := re.search(r"^name:\s*(.+)$", p.read_text(encoding="utf8"), re.M))}
        top, genel = {"A": [], "B": []}, {"A": [], "B": []}
        sikkayip = []
        kosu = [tuple(sys.argv[i:i + 3]) for i in range(2, len(sys.argv), 3)] or [("A1", "B1", "1"), ("A1", "B2", "2"), ("A2", "B3", "3")]
        for ka, kb, ek in kosu:  # d4: onarım sonrası çift argümanla (karar A3 B4 4)
            a = json.loads((CIK / f"anahtar{ek}.json").read_text(encoding="utf8"))
            p = json.loads((CIK / f"puan{ek}.json").read_text(encoding="utf8"))
            sec = {"A": kapi10.secimler(ka)[0], "B": kapi10.secimler(kb)[0]}
            pu = {k: 0 for k in "AB"}
            kayip = []
            for i, xy in a["anahtar"].items():
                s = {xy["X"]: p[i]["X"], xy["Y"]: p[i]["Y"]}
                pu["A"] += s["A"]; pu["B"] += s["B"]
                if s["B"] < s["A"]:
                    secim = [sec[k].get(int(i), "-") for k in "AB"]
                    bagli = [n for n in secim if ad.get(n.strip(), "") in sik]
                    kayip.append((int(i), *secim, bagli))
                    sikkayip += bagli
            for k in "AB":
                top[k].append(pu[k]); genel[k].append(a["genel"][k])
            print(f"{ka}/{kb}: puan A {pu['A']} B {pu['B']} · genel A {a['genel']['A']} B {a['genel']['B']} · kayıp {kayip}")
        o = {k: (sum(top[k]) / len(kosu), sum(genel[k]) / len(kosu)) for k in "AB"}
        kabul = o["B"][0] >= o["A"][0] - 1 and not sikkayip and o["B"][1] <= o["A"][1] + 0.5
        print(f"ort puan A {o['A'][0]:.2f} B {o['B'][0]:.2f} · genel A {o['A'][1]:.2f} B {o['B'][1]:.2f} · sıkışık kayıp {sikkayip} · {'KABUL' if kabul else 'RET'}")
    else:
        kapi10.main(sys.argv[1:])
