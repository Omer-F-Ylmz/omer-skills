"""RUFLO-1 d10: günlük öğrenme kancasının uçtan uca kanıtı — gerçek `claude -p` oturumu, kancalar `--settings` ile (canlı ~/.claude'a
dokunulmaz). Kod ailesi 5 görev (ab_olc.kur/yargic); ana oturum görevi `kodcu` alt ajanına verir (--agents).
Kol dersli: SubagentStart/SubagentStop kancası + oturum sonunda kanca.isle (gerçek Jev + karma; damıtma haiku). Kol derssiz: OGRENME_KANCA=0.
SessionEnd kancası burada yok: isle sürücüden eşzamanlı çağrılır (canlıda SessionEnd → arka.py; birim testte sınanır).
Tavan: ≤10 oturum + ≤5 damıtma, Σ$ ≤ 6. TSV: docs/kutuphane/olcum/ruflo-1-kanca-e2e.tsv"""
import json
import os
import sys
import tempfile
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "olcum"), str(KOK / "tools" / "ogrenme")]
import ab_olc  # noqa: E402
import ders  # noqa: E402
import kanca  # noqa: E402

TSV = KOK / "docs" / "kutuphane" / "olcum" / "ruflo-1-kanca-e2e.tsv"
USD_TAVAN = 6.0
AJAN = {"kodcu": {"description": "Görev klasöründe Python kodunu düzelten alt ajan.", "model": "sonnet",
                  "tools": ["Read", "Edit", "Write", "Glob", "Grep", "Bash"],
                  "prompt": "Görev klasöründeki Python kodunu istenen şekilde düzelt ve testlerle doğrula. Bitince ne yaptığını 2 satırda yaz."}}
ISTEM = ("Bu görevi Agent aracıyla `kodcu` alt ajanına ver (görev metnini aynen aktar). Kendin dosya okuma/düzenleme yapma; "
         "alt ajan bitince tek satır özet yaz.\n\nGörev:\n%s")


def ayarlar(d):
    kom = {"type": "command", "command": f'"{sys.executable}" "{Path(kanca.__file__).as_posix()}"', "timeout": 5}
    p = Path(d) / "kanca-ayar.json"
    p.write_text(json.dumps({"hooks": {o: [{"hooks": [kom]}] for o in ("SubagentStart", "SubagentStop")}}), encoding="utf-8")
    return str(p)


def damit(istem, say):
    import kosucu
    o = kosucu.kos(istem, ek=["--strict-mcp-config", "--max-turns", "1"], model="haiku", butce=0.2, timeout=180)
    say.append(o["usd"])
    return o["metin"]


def main():
    import kosucu
    # kanca transkriptten okur; ölçüm rotasının --no-session-persistence'ı onu diske yazdırmaz (günlük kullanımda kalıcılık açık)
    kosucu.ROTA = [x for x in kosucu.ROTA if x != "--no-session-persistence"]
    banka = KOK / ".kos" / "ogrenme-ab" / ("kanca-e2e-" + time.strftime("%Y%m%d-%H%M%S"))
    os.environ["OGRENME_DIZIN"] = str(banka)
    ayar = ayarlar(ders.dizin())
    usd, yeni = 0.0, not TSV.exists()
    with open(TSV, "a", encoding="utf-8", newline="\n") as out:
        if yeni:
            out.write("zaman\tsira\tkol\tpuan\tgizli\ttur\tinput\tcache_creation\tcache_read\toutput\tusd\tsure_sn\tders_ids\tkarma\tyeni_ders\trc\n")
        for i in range(5):
            for kol in ("dersli", "derssiz"):
                if usd >= USD_TAVAN or kosucu.bos_ram_gb() < 1.6:
                    print(time.strftime("%H:%M:%S"), f"TAVAN: ${usd:.2f} boş RAM {kosucu.bos_ram_gb():.1f} GB — durdu", flush=True)
                    return
                os.environ["OGRENME_KANCA"] = "1" if kol == "dersli" else "0"
                d = tempfile.mkdtemp(prefix=f"ruflo-kanca-{i}-")
                o = kosucu.kos(ISTEM % ab_olc.kur("kod", i, d), cwd=d, model="sonnet", butce=0.8,
                               ek=["--permission-mode", "acceptEdits", "--allowedTools", "Read,Edit,Write,Glob,Grep,Bash(python:*),Agent,Task",
                                   "--strict-mcp-config", "--max-turns", "20", "--agents", json.dumps(AJAN), "--settings", ayar])
                usd += o["usd"]
                puan, gizli, _ = ab_olc.yargic("kod", i, d)
                ids, karma, onceki, dmu = [], [], len(ders.oku()), []
                for q in (banka / "kuyruk").glob("*.jsonl") if kol == "dersli" else ():
                    kayit = list(kanca._satirlar(q))
                    ids += [x for k in kayit if k["tip"] == "getir" for x in k["ids"]]
                    jv = []
                    kanca.isle(q.stem, yargic=lambda s: jv.append(kanca._jev(s)) or jv[-1], damit=lambda m: damit(m, dmu))
                    karma += jv[-1] if jv else ["atlandi"]  # ham Jev 0-10 (karma = Jev − hata oranı)
                usd += sum(dmu)
                out.write("\t".join(map(str, [time.strftime("%H:%M:%S"), i + 1, kol, puan, gizli, o["tur"], *kosucu.jeton(o["usage"]),
                                              round(o["usd"] + sum(dmu), 4), o["sure"], ",".join(ids), karma, len(ders.oku()) - onceki, o["rc"]])) + "\n")
                out.flush()
                print(time.strftime("%H:%M:%S"), i + 1, kol, "puan", puan, "tur", o["tur"], f"${o['usd']:.3f}", "ders", ids, "karma", karma,
                      f"Σ${usd:.2f}", flush=True)
    print(time.strftime("%H:%M:%S"), f"BİTTİ: ${usd:.2f} · banka {banka}", flush=True)


if __name__ == "__main__":
    main()
