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
K15 = ("Kural dosyası: {} — Read ile oku, gösterdiği dosya varsa onu da. Sonra şu hayali görev için köprü oturumu d1 planını yaz "
       "(dosya yazma ve komut çalıştırma YOK; yalnız Read). Görev OLCUM-Z: secim_olc.py ile zor seti tekrar 2 ölç (~25 dk sürer), "
       "sonuca göre tools/ altında küçük bir betik düzeltmesi yap, düzeltilen skill'i claude.ai'ye de teslim et. Yanıt: (1) sırayla ilk 6 adım, "
       "her biri komut/dosya yoluyla (2) ölçüm sürerken RAM %89'a çıkarsa ne yaparsın (3) 40. dakikada ne yaparsın (4) devir notu taslağı "
       "(5) iş bitince son adımlar. ≤40 satır.")
ISTEM["k15a"] = ("high", K15.format("C:/Projeler/omer-skills/skills/is-akisi/arsiv.md"))
ISTEM["k15b"] = ("high", K15.format("C:/Projeler/omer-skills/.kos/kopru/gorev/DEVAM-KURALI.md"))

for ad in sys.argv[1:]:
    efor, istem = ISTEM[ad]
    argv, env = baslat_argv(efor)
    t = time.time()
    p = subprocess.run(argv, input=istem, capture_output=True, text=True, encoding="utf-8", cwd=KOK, env=env, timeout=1800)
    (D / f"kapi-{ad}.json").write_text(p.stdout or p.stderr, encoding="utf-8")
    print(ad, "rc", p.returncode, f"{time.time() - t:.0f}s", flush=True)
print("BITTI", flush=True)
