"""TOKEN-8 f2b iş 2 kalite kapısı (2 claude -p, opus): 10 gerçek geçmiş Agent isteği için ajan seçimi.
A = tam ~/.claude/agents; B = cekirdek.txt + ajan-getir katalogu yeniden üretilmiş (tüm kullanıcı ajanları).
Çıktı: kapi2_A.json / kapi2_B.json (ham yanıt) — kör yargı ayrı."""
import json, os, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "C:/Projeler/omer-skills-wt/token8/tools")
import ajan_katalog
from ajan_olc import EV, WT, kur, sok  # import ölçüm döngüsünü koşmasın diye ajan_olc __main__ korumalı
import tempfile

GOREV = [
    "A React list re-renders on every keystroke. List the likely causes.",
    "How do you spot SQL injection in code review and fix it?",
    "What API security checks do you run on a user profile endpoint?",
    "Write unit test cases for a function that validates a password.",
    "omer-skills 7 suite'i koş (taban 1758). Suite başına sayı + kırmızı test adları dön.",
    "Research task (web, read-only): for a Windows user building product 3D (Turkish coffee machine exploded-view for a three.js website) with Blender + Claude, compare AI 3D generation platforms and asset APIs.",
    "Stress-test a design for a geometry pipeline (Genshin 3DMigoto body mod, pure numpy, no scipy/trimesh). Do NOT write files; return weaknesses and a revised step list.",
    "Read-only investigation on Windows (Git Bash): why does temp_git churn so much in ~/.claude? Do not modify ~/.claude, do not run claude.",
    "d15-spec.md şartnamesine göre d15-secim.tsv satır 81–100'deki ajan adaylarını Claude Code alt ajan tanımına (.md, frontmatter) dönüştür.",
    "Classify 20 gitleaks findings as REAL secret or FALSE alarm; never print the secret values.",
]
ISTEM = ("Aşağıdaki 10 görevin HİÇBİRİNİ yapma. Yalnız şunu yanıtla: her görev için bu oturumda hangi alt ajanı kullanırdın? "
         "Kurulu herhangi bir ajan olabilir (Agent listesinde görünmeyen kurulu ajanlar dahil; bulmak için Grep/Read serbest). "
         "Uygun uzman yoksa general-purpose. Yanıt yalnız JSON dizi: "
         '[{"no":1,"ajan":"<ad>","nasil":"Agent|ajan-getir","gerekce":"<12 kelime"}]\n\n'
         + "\n".join(f"{i}. {g}" for i, g in enumerate(GOREV, 1)))
TABAN = ["-p", "--output-format", "json", "--model", "opus", "--max-turns", "12",
         "--settings", json.dumps({"promptCacheTtl": "5m"})]


def b_skill(kok):
    """B: skills gerçek dizin; her skill junction, ajan-getir kopya + tam katalog."""
    os.rmdir(kok / "skills")
    (kok / "skills").mkdir()
    for p in (EV / "skills").iterdir():
        if p.name == "ajan-getir":
            shutil.copytree(p, kok / "skills" / p.name)
        elif p.is_dir():
            subprocess.run(["cmd", "/c", "mklink", "/J", str(kok / "skills" / p.name), str(p)], capture_output=True, check=True)
    satirlar, _ = ajan_katalog.uret(EV)
    (kok / "skills/ajan-getir/katalog.tsv").write_text("ad\tmodel\ttek_satir\tyol\n" + "".join("\t".join(s) + "\n" for s in satirlar),
                                                       encoding="utf-8", newline="\n")
    return len(satirlar)


tmp = Path(tempfile.mkdtemp(prefix="t8kapi_"))
try:
    kur(tmp / "A", True); kur(tmp / "B", False)
    print("B katalog satır", b_skill(tmp / "B"), flush=True)
    for kol in ("A", "B"):
        env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}  # api-kredi.kapali
        env["CLAUDE_CONFIG_DIR"] = str(tmp / kol)
        r = subprocess.run(["claude", *TABAN], input=ISTEM, capture_output=True, text=True, encoding="utf8",
                           cwd=WT, env=env, timeout=900, creationflags=0x08000000)
        (Path(__file__).parent / f"kapi2_{kol}.json").write_text(r.stdout or r.stderr, encoding="utf8")
        try:
            j = json.loads(r.stdout); print(kol, "tur", j.get("num_turns"), "sonuc", (j.get("result") or "")[:80].replace("\n", " "), flush=True)
        except ValueError:
            print(kol, "rc", r.returncode, r.stderr[:200], flush=True)
finally:
    bs = tmp / "B" / "skills"
    if bs.exists() and not bs.is_junction():
        for p in bs.iterdir():
            if p.is_junction():
                os.rmdir(p)
    for k in ("A", "B"):
        if (tmp / k).exists():
            sok(tmp / k)
    shutil.rmtree(tmp, ignore_errors=True)
