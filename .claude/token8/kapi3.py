"""TOKEN-8 f2c iş 2 v2. Kollar: A = tam ~/.claude/agents; V1 = cekirdek_v1.txt + ajan-getir tam katalog;
V2 = V1 + ajan-getir açıklamasına departman → önek eşlemesi. Plugin ajanları her kolda olduğu gibi kalır.
  python kapi3.py onek V1        → A ve V1 birer "tamam" (2 claude -p, sonnet): girdi jetonu farkı
  python kapi3.py kapi V1 [A]    → 20 görev ajan seçimi (kol başına 1 claude -p, opus) → kapi3_<kol>.json
Canlı ~/.claude'a yazılmaz (geçici CLAUDE_CONFIG_DIR; dizinler junction)."""
import ast, json, os, random, shutil, subprocess, sys, tempfile
from pathlib import Path

BURA = Path(__file__).parent
sys.path.insert(0, str(BURA))
sys.path.insert(0, "C:/Projeler/omer-skills-wt/token8/tools")
import ajan_katalog
import ajan_olc
from ajan_olc import EV, WT, kur, sok

ajan_olc.CEKIRDEK = [s.strip() for s in (BURA / "cekirdek_v1.txt").read_text(encoding="utf8").split() if s.strip()]
# kapi2.py korumasız (import edince koşar) → GOREV listesini kaynaktan oku
GOREV = next(ast.literal_eval(d.value) for d in ast.parse((BURA / "kapi2.py").read_text(encoding="utf8")).body
             if isinstance(d, ast.Assign) and getattr(d.targets[0], "id", "") == "GOREV")
GOREV += [g["g"] for g in json.loads((BURA / "gorev_v2.json").read_text(encoding="utf8"))]
ISTEM = (f"Aşağıdaki {len(GOREV)} görevin HİÇBİRİNİ yapma. Yalnız şunu yanıtla: her görev için bu oturumda hangi alt ajanı kullanırdın? "
         "Kurulu herhangi bir ajan olabilir (Agent listesinde görünmeyen kurulu ajanlar dahil; bulmak için Grep/Read serbest). "
         "Uygun uzman yoksa general-purpose. Yanıt yalnız JSON dizi: "
         '[{"no":1,"ajan":"<ad>","nasil":"Agent|ajan-getir","gerekce":"<12 kelime"}]\n\n'
         + "\n".join(f"{i}. {g}" for i, g in enumerate(GOREV, 1)))
ESLEME = ("Hidden specialist prefixes (search katalog.tsv by prefix before picking a generic plugin agent): "
          "fe- frontend/React/CSS; sec- security (injection, API, secrets); qa- tests; db- databases/SQL; dn- .NET/EF Core; "
          "be- backend design; dil- languages (Go, Node, Python); ops- infra/nginx/k8s; git- git/CI; dok- docs/reports; "
          "ml- ML/data; mob- mobile; vid- video/ffmpeg; bl- Blender; oyn- games/mods; pln- planning/specs; inc- code review/debug; "
          "ara- research/licenses; ajn- agents/skills/hooks/MCP; vrm- context/cost/worktrees; otm- automation/scripts; urn- product/marketing.")


def b_skill(kok, v2):
    """skills gerçek dizin; her skill junction, ajan-getir kopya + tam katalog (+ V2 eşleme)."""
    os.rmdir(kok / "skills")
    (kok / "skills").mkdir()
    for p in (EV / "skills").iterdir():
        if p.name == "ajan-getir":
            shutil.copytree(p, kok / "skills" / p.name)
        elif p.is_dir():
            subprocess.run(["cmd", "/c", "mklink", "/J", str(kok / "skills" / p.name), str(p)], capture_output=True, check=True)
    satirlar, _ = ajan_katalog.uret(EV)
    ag = kok / "skills/ajan-getir"
    (ag / "katalog.tsv").write_text("ad\tmodel\ttek_satir\tyol\n" + "".join("\t".join(s) + "\n" for s in satirlar), encoding="utf-8", newline="\n")
    if v2:
        s = (ag / "SKILL.md").read_text(encoding="utf-8")
        son = s.index("\n", s.index("description: "))
        (ag / "SKILL.md").write_text(s[:son] + " " + ESLEME + s[son:], encoding="utf-8", newline="\n")
    return len(satirlar)


def kos(kok, istem, taban):
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
    env["CLAUDE_CONFIG_DIR"] = str(kok)
    r = subprocess.run(["claude", *taban], input=istem, capture_output=True, text=True, encoding="utf8",
                       cwd=WT, env=env, timeout=1500, creationflags=0x08000000)
    return r


def temizle(tmp):
    for k in tmp.iterdir():
        bs = k / "skills"
        if bs.exists() and not bs.is_junction():
            for p in bs.iterdir():
                if p.is_junction():
                    os.rmdir(p)
        sok(k)
    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    is_ = sys.argv[1]
    kollar = ["A", sys.argv[2]] if is_ == "onek" else sys.argv[2:]
    tmp = Path(tempfile.mkdtemp(prefix="t8kapi3_"))
    try:
        for k in kollar:
            kur(tmp / k, k == "A")
            if k != "A":
                print(k, "katalog satır", b_skill(tmp / k, k == "V2"), "çekirdek", len(ajan_olc.CEKIRDEK), flush=True)
        for k in kollar:
            if is_ == "onek":
                r = kos(tmp / k, "tamam", ajan_olc.TABAN)
                j = json.loads(r.stdout); u = j.get("usage", {})
                print(json.dumps({"kol": k, "girdi": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                                  + u.get("cache_read_input_tokens", 0), "ekler": ajan_olc.ekler(j.get("session_id"))}, ensure_ascii=False), flush=True)
            else:
                taban = ["-p", "--output-format", "json", "--model", "opus", "--max-turns", "20", "--settings", json.dumps({"promptCacheTtl": "5m"})]
                r = kos(tmp / k, ISTEM, taban)
                (BURA / f"kapi3_{k}.json").write_text(r.stdout or r.stderr, encoding="utf8")
                try:
                    j = json.loads(r.stdout); print(k, "tur", j.get("num_turns"), "hata", j.get("is_error"), (j.get("result") or "")[:80].replace("\n", " "), flush=True)
                except ValueError:
                    print(k, "rc", r.returncode, r.stderr[:200], flush=True)
    finally:
        temizle(tmp)
