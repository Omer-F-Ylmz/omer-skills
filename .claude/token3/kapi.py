"""TOKEN-3 d4 kalite kapıları: ajan_sira ile AYNI argv (ajan profili + efor) → .claude/token3/kapi-<ad>.json.
  python .claude/token3/kapi.py k11 k12   (claude -p: ad başına 1)"""
import json, subprocess, sys, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
sys.path.insert(0, str(KOK / ".kos/kopru"))
from ajan_sira import baslat_argv  # noqa: E402

D = Path(__file__).parent
ISTEM = {
    "k11": ("medium", "Mekanik iş, yorum yok. 1) `python -m pytest tests/test_ajan_sira.py tests/test_cc_profil.py -q` koş. "
            "2) .kos/kopru/ajan-sira.tsv boş olmayan satır sayısını say. Yanıt tam 2 satır: `pytest: <passed sayısı> passed, <failed> failed` ve `tsv: <n>`."),
    "k12": ("high", "Agent aracıyla AYNI ANDA (tek mesajda) iki alt ajan aç: subagent_type=okuyucu ve subagent_type=general-purpose; ikisine "
            "harfiyen şu istemi ver:\n---\nBu repoda (C:\\Projeler\\omer-skills) cc_profil'in \"ajan\" profilini araştır (tools/cc_profil.py, "
            "tools/cc-kopru/sunucu.mjs, profiller/ altı, ilgili testler). Cevapla: (a) profil hangi CC ayarlarını/bayraklarını uygular "
            "(ttl, includeGitInstructions, env), (b) ajan deny listesi hangi kaynaklardan üretilir ve ad biçimi ne, (c) hangi ajanlar "
            "deny'dan muaf tutulur ve nerede tanımlı, (d) CC_PROFIL_ZORLA ne yapar, (e) hangi test dosyaları bunu sınıyor. "
            "Dosya yazma. ≤12 satır, her iddiaya dosya:satır.\n---\nİki yanıt gelince her birini HARFİYEN dosyaya yaz: okuyucu → "
            ".claude/token3/k12-okuyucu.md, general-purpose → .claude/token3/k12-gp.md. Sonra yalnız `bitti` yaz."),
}

for ad in sys.argv[1:]:
    efor, istem = ISTEM[ad]
    argv, env = baslat_argv(efor)
    t = time.time()
    p = subprocess.run(argv, input=istem, capture_output=True, text=True, encoding="utf-8", cwd=KOK, env=env, timeout=1800)
    (D / f"kapi-{ad}.json").write_text(p.stdout or p.stderr, encoding="utf-8")
    print(ad, "rc", p.returncode, f"{time.time() - t:.0f}s", flush=True)
print("BITTI", flush=True)
