"""SLASH-ÖĞREN d3 kapı: dar küme (--settings birleşik, ayarlar korunur) → girdi token'ı + hook + CLAUDE.md kanıtı. En fazla 3 `claude -p`.
Sonuç .kos/ogrenme/slash-d3.json. Kullanım: python tools/ogrenme/slash_d3.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / ".kos" / "kopru"))
import ajan_sira  # noqa: E402

HOOK = "Bash aracıyla tam şu komutu çalıştır: rm -rf C:/tmp/__d3_yok_dizin (yalnız bu yol, olmayan bir dizin; başka argüman yok). Sonra ne olduğunu tek cümleyle yaz (engellendi mi, hata metni ne)."
SKILL = "Skill aracının listesindeki skill sayısını ve 'graphify' ile 'watch' adlı skill'lerin listede olup olmadığını yaz (tam adlarıyla); başka bir şey yazma."
CLAUDEMD = "Yüklü CLAUDE.md talimatlarında 'sor2' sözcüğü geçiyor mu? Yalnız evet/hayır yaz."


def kos(istem):
    with tempfile.TemporaryDirectory() as t:
        ajan_sira.SLASH_DOSYA = Path(t) / "x.slash"
        ajan_sira.SLASH_DOSYA.write_text("dar=cekirdek", encoding="utf-8")
        argv, env = ajan_sira.baslat_argv("")
    argv = [a if a != "opus" else "sonnet" for a in argv] + ["--max-turns", "4"]
    p = subprocess.run(argv, input=istem, capture_output=True, text=True, encoding="utf-8", cwd=str(KOK), timeout=300, env=env)
    j = json.loads(p.stdout)
    u = j["usage"]
    return {"girdi": u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
            "yanit": j.get("result", "")[:900], "izin_ret": len(j.get("permission_denials", []))}


if __name__ == "__main__":
    sonuc = {ad: kos(i) for ad, i in ((a, {"claudemd": CLAUDEMD, "hook": HOOK, "skill": SKILL}[a]) for a in sys.argv[1:])}
    for ad, r in sonuc.items():
        print(ad, r, flush=True)
    (KOK / ".kos" / "ogrenme" / "slash-d3.json").write_text(json.dumps(sonuc, indent=1, ensure_ascii=False), encoding="utf-8")
