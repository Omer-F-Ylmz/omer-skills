"""TOKEN-10 iş 3–4: A = canlı ~/.claude/agents, B = aynı dosyalar, kendi ajanlarımızın description'ı esleme.tsv'den.
  python kapi10.py onek        → A/B birer "tamam" (2 claude -p sonnet): girdi jetonu + ajan listesi kr
  python kapi10.py kapi [A B]  → 30 görev ajan seçimi (kol başına 1 claude -p opus) → docs/token-10/kapi_<kol>.json
  python kapi10.py kor         → kor.md (X/Y karışık) + anahtar.json + genel ajan sayısı
  python kapi10.py sonuc       → puan.json (okuyucu, görev başına 0–2) + anahtar → kapı kararı
Canlı ~/.claude'a yazılmaz (geçici CLAUDE_CONFIG_DIR; dizinler junction, agents B'de kopya)."""
import ast, json, os, random, re, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf8")
T8 = Path("C:/Projeler/omer-skills/.claude/token8")
sys.path.insert(0, str(T8))
import ajan_olc
from ajan_olc import EV, kur, sok
sys.path.insert(0, str(Path(__file__).parent))
from ajan_aciklama import aciklama_degistir

WT = Path(__file__).resolve().parents[2]
CIK = WT / "docs/token-10"
GOREV = next(ast.literal_eval(d.value) for d in ast.parse((T8 / "kapi2.py").read_text(encoding="utf8")).body
             if isinstance(d, ast.Assign) and getattr(d.targets[0], "id", "") == "GOREV")
GOREV += [g["g"] for g in json.loads((T8 / "gorev_v2.json").read_text(encoding="utf8"))]
GOREV += [  # TOKEN-10 ek 10: f2b/f2c'nin az kapsadığı aileler, kardeş ajanı olan görevler
    "Our Postgres orders table keeps growing on disk although the row count is flat and autovacuum looks behind. Diagnose and fix.",
    "Design an idempotent money transfer between user wallets so balances never drift; include reconciliation.",
    "A Go service leaks goroutines under load; review the worker pool and channel shutdown logic.",
    "Pods get OOMKilled and drop requests during each rollout; tune the Kubernetes deployment manifest.",
    "The spec only says 'the app must be fast and secure'. Turn that into measurable targets with verification.",
    "Users don't understand our API error messages; rewrite them so they say what happened and what to do next.",
    "Our fraud model shows 99% accuracy but catches almost no fraud; fix the evaluation and decision threshold.",
    "iOS universal links from marketing emails open Safari instead of our app. Find why and fix the setup.",
    "A CSV export opens garbled in Turkish-locale Excel with shifted columns. Fix the export.",
    "Write a Claude Code PreToolUse hook that blocks rm -rf outside the repository.",
]
ISTEM = (f"Aşağıdaki {len(GOREV)} görevin HİÇBİRİNİ yapma. Yalnız şunu yanıtla: her görev için bu oturumda hangi alt ajanı kullanırdın? "
         "Agent listesindeki herhangi bir ajan olabilir. Uygun uzman yoksa general-purpose. Yanıt yalnız JSON dizi: "
         '[{"no":1,"ajan":"<ad>","gerekce":"<12 kelime"}]\n\n' + "\n".join(f"{i}. {g}" for i, g in enumerate(GOREV, 1)))
GENEL = {"general-purpose", "Explore", "Plan", "claude"}


def b_ajanlar(kok):
    """B: agents junction'ı kaldır, kopyala, kendi ajanlarda yalnız description satırını değiştir."""
    os.rmdir(kok / "agents")
    shutil.copytree(EV / "agents", kok / "agents")
    yeni = {s.split("\t")[0]: s.split("\t")[2] for s in (CIK / "esleme.tsv").read_text(encoding="utf8").splitlines()[1:]}
    n = 0
    for ad, d in yeni.items():
        p = kok / "agents" / f"{ad}.md"
        metin = p.read_text(encoding="utf8")
        y = aciklama_degistir(metin, d)
        if y != metin:
            p.write_text(y, encoding="utf8", newline="")
            n += 1
    return n


def kos(kok, istem, taban):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
    env["CLAUDE_CONFIG_DIR"] = str(kok)
    return subprocess.run(["claude", *taban], input=istem, capture_output=True, text=True, encoding="utf8",
                          cwd=WT, env=env, timeout=1500, creationflags=0x08000000)


def secimler(k):
    j = json.loads((CIK / f"kapi_{k}.json").read_text(encoding="utf8"))
    return {d["no"]: d["ajan"] for d in json.loads(re.search(r"\[.*\]", j["result"], re.S).group(0))}, j.get("num_turns")


if __name__ == "__main__":
    is_ = sys.argv[1]
    if is_ in ("onek", "kapi"):
        kollar = sys.argv[2:] or ["A", "B"]
        tmp = Path(tempfile.mkdtemp(prefix="t10_"))
        try:
            for k in kollar:
                kur(tmp / k, True)
                if k == "B":
                    print("B değişen ajan", b_ajanlar(tmp / k), flush=True)
            for k in kollar:
                if is_ == "onek":
                    j = json.loads(kos(tmp / k, "tamam", ajan_olc.TABAN).stdout); u = j.get("usage", {})
                    print(json.dumps({"kol": k, "girdi": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                                      + u.get("cache_read_input_tokens", 0), "ekler": ajan_olc.ekler(j.get("session_id"))}, ensure_ascii=False), flush=True)
                else:
                    taban = ["-p", "--output-format", "json", "--model", "opus", "--max-turns", "20", "--settings", json.dumps({"promptCacheTtl": "5m"})]
                    r = kos(tmp / k, ISTEM, taban)
                    (CIK / f"kapi_{k}.json").write_text(r.stdout or r.stderr, encoding="utf8")
                    print(k, "rc", r.returncode, (r.stdout or r.stderr)[:120].replace("\n", " "), flush=True)
        finally:
            for k in kollar:
                if (tmp / k).exists():
                    sok(tmp / k)
            shutil.rmtree(tmp, ignore_errors=True)
    elif is_ == "kor":
        (sa, ta), (sb, tb) = secimler("A"), secimler("B")
        rnd, anahtar, md = random.Random(1013), {}, []
        for i, g in enumerate(GOREV, 1):
            x, y = ("A", "B") if rnd.random() < 0.5 else ("B", "A")
            anahtar[i] = {"X": x, "Y": y}
            sec = {"A": sa.get(i, "-"), "B": sb.get(i, "-")}
            md.append(f"## {i}. {g}\n- X: {sec[x]}\n- Y: {sec[y]}\n")
        (CIK / "kor.md").write_text("\n".join(md), encoding="utf8")
        genel = {k: sum(v in GENEL for v in s.values()) for k, s in (("A", sa), ("B", sb))}
        (CIK / "anahtar.json").write_text(json.dumps({"anahtar": anahtar, "tur": {"A": ta, "B": tb}, "genel": genel}), encoding="utf8")
        print("seçim", len(sa), len(sb), "tur", ta, tb, "genel", genel, "farklı", [i for i in sa if sa[i] != sb.get(i)])
    else:
        a = json.loads((CIK / "anahtar.json").read_text(encoding="utf8"))
        p = json.loads((CIK / "puan.json").read_text(encoding="utf8"))
        top = {"A": 0, "B": 0}
        kayip = []
        for i, xy in a["anahtar"].items():
            pu = {xy["X"]: p[i]["X"], xy["Y"]: p[i]["Y"]}
            top["A"] += pu["A"]; top["B"] += pu["B"]
            if pu["B"] < pu["A"]:
                kayip.append(int(i))
        t, g = a["tur"], a["genel"]
        kabul = top["B"] >= top["A"] and t["B"] <= t["A"] and g["B"] <= g["A"]
        print(f"puan A {top['A']} B {top['B']} · tur A {t['A']} B {t['B']} · genel A {g['A']} B {g['B']} · B kayıp görev {kayip} · {'KABUL' if kabul else 'RET'}")
