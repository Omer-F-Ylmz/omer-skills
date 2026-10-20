"""SLASH-ÖĞREN d2 kapı: daraltılmış köprü oturumu (--setting-sources "" + --plugin-dir) → gerçek girdi token'ı + held-out 10 görevde doğru skill seçimi. 1 `claude -p`."""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import slash_dar  # noqa: E402
import slash_olc  # noqa: E402
from slash_kapi import GOREV  # noqa: E402

KOK = slash_olc.KOK

if __name__ == "__main__":
    ek = ["--setting-sources", "", "--plugin-dir", str(slash_dar.kur()), *slash_olc.argv(True)]
    istem = ("Skill aracının listesine bak. Aşağıdaki her görev için, çağıracağın TEK skill/komut adını seç (yalnız ad; `:` önekini ve `/`'ı at). "
             "HİÇBİRİNİ ÇAĞIRMA, araç kullanma. Yanıt yalnız JSON dizisi: [\"ad1\", ... 10 öğe].\n" + "\n".join(f"{i + 1}. {g}" for i, (g, _) in enumerate(GOREV)))
    p = subprocess.run([shutil.which("claude"), "-p", "--output-format", "json", "--model", "sonnet", "--max-turns", "3", *ek],
                       input=istem, capture_output=True, text=True, encoding="utf-8", cwd=str(KOK), timeout=300)
    j = json.loads(p.stdout)
    u = j["usage"]
    toplam = u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
    secim = json.loads(re.search(r"\[.*\]", j["result"], re.S).group(0))
    dogru = sum(1 for s, (_, b) in zip(secim, GOREV) if s.split(":")[-1].strip("/ ") == b)
    print(f"girdi toplam {toplam} · seçim {dogru}/{len(GOREV)}", secim, "tur", j.get("num_turns"))
