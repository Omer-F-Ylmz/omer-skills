"""TASARIM-1 (4) kanıt: aynı brief'le taban (main frontend-craft) vs yeni (kol/tasarim frontend-craft) tek sayfa üretimi.
    python tools/tasarim/kanit.py <cikti_dizini> [--kuru]
2 brief × 2 kol × 2 tekrar = 8 claude -p; `--kol ciplak` skill'siz 4 çağrı daha (dedektör gerçek AI çıktısını ayırıyor mu; 12 ≤16).
Her çağrı --max-budget-usd 1; ana koşu toplam $7'yi geçerse durur, çıplak koşu en çok $4 (gerçekleşen Σ < $8).
Puan: slop.mjs bayrak sayısı (aynı denetçi iki kola) + audit.mjs sonucu + sayfa baytı + usd/tur/jeton → <cikti>/kanit.tsv.
"""
import json
import os
import pathlib
import subprocess
import sys
import time

WT = pathlib.Path(__file__).resolve().parents[2]
KOLLAR = {"taban": pathlib.Path(r"C:\Projeler\omer-skills\plugins\frontend-craft\skills\frontend-craft"),
          "yeni": WT / "plugins/frontend-craft/skills/frontend-craft"}
BRIEF = {"landing": "El yapımı kahve öğütücü markası 'Telve Atölye' için ürün landing sayfası: hero, 3 özellik, fiyat, SSS, footer.",
         "portfolyo": "Bağımsız mimar 'Deniz Kaya' için portfolyo sayfası: 6 proje, hakkında, iletişim."}
TAVAN = 7.0
PORT = 3918 if "ciplak" in sys.argv else 3917  # iki koşu olcum_sira'da paralel düşebilir


def sistem(kol):
    if kol == "ciplak":
        return (f"Etkileşimsiz koşu. Çalışma dizininde index.html yaz (CSS/JS satır içi, harici görsel yok); sayfa http://localhost:{PORT}/ "
                "adresinde sunuluyor. Son mesajın tek satır özet.")
    d = KOLLAR[kol]
    skill = (d / "SKILL.md").read_text(encoding="utf-8").replace("${CLAUDE_SKILL_DIR}", d.as_posix())
    return ("frontend-craft skill'ini uygularsın; içeriği aşağıda. Etkileşimsiz koşu: DUR adımlarında kendin seç ve sürdür, "
            "yön keşfinde tek yön yeter, screenshot döngüsü en çok 2 tur, node_modules kurulu (Adım 0 atla). "
            f"Sayfa http://localhost:{PORT}/ adresinde zaten sunuluyor (serve.mjs başlatma). Çıktı: çalışma dizininde index.html "
            "(CSS/JS satır içi, harici görsel yok) + DESIGN.md. Son mesajın tek satır özet.\n\n" + skill)


def kos(kol, brief, tekrar, kok):
    dizin = kok / f"{brief}-{kol}-{tekrar}"
    dizin.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}  # headroom vekili araçları gizliyor; anahtar varsa plan yerine API kredisi (d3: 401)
    sunucu = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=dizin, creationflags=0x08000000,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        r = subprocess.run(["claude", "-p", BRIEF[brief], "--model", "sonnet", "--output-format", "json", "--max-budget-usd", "1",
                            "--setting-sources", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
                            "--disable-slash-commands", "--tools", "Read,Write,Edit,Bash", "--allowedTools", "Read", "Write", "Edit",
                            "Bash", "--system-prompt", sistem(kol)], cwd=dizin, env=env, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1500, creationflags=0x08000000)
        (dizin / "claude.json").write_text(r.stdout + r.stderr[-2000:], encoding="utf-8")  # hata nedeni (d2: 7 koşu tur 1/$0)
        j = json.loads(r.stdout or "{}")
        if not (dizin / "index.html").exists():  # yoksa http.server dizin listesini sunar, slop onu "0 bayrak" sayıp geçmişe yazar
            return [kol, brief, tekrar, 1, "ÜRETİLMEDİ", "-", 0, j.get("total_cost_usd") or 0, j.get("num_turns"), 0, 0]
        url, yeni = f"http://localhost:{PORT}/", KOLLAR["yeni"] / "scripts"
        s = subprocess.run(["node", str(yeni / "slop.mjs"), url, "--json", str(dizin / "slop.json")], cwd=dizin, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=180, creationflags=0x08000000)
        a = subprocess.run(["node", str(yeni / "audit.mjs"), url, "dev"], capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=180, cwd=KOLLAR["yeni"], creationflags=0x08000000)
    finally:
        sunucu.kill()
    sj = json.loads((dizin / "slop.json").read_text(encoding="utf-8")) if (dizin / "slop.json").exists() else {"bayrak": ["ÖLÇÜLEMEDİ"]}
    u = j.get("usage") or {}
    satir = [kol, brief, tekrar, len(sj["bayrak"]), " | ".join(sj["bayrak"]), (a.stdout.strip().splitlines() or ["-"])[0][:60],
             (dizin / "index.html").stat().st_size if (dizin / "index.html").exists() else 0, j.get("total_cost_usd") or 0,
             j.get("num_turns"), u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
             u.get("output_tokens", 0)]
    return satir


def main(argv):
    kok = pathlib.Path(argv[0]).resolve()
    kollar = ["ciplak"] if "ciplak" in argv else list(KOLLAR)
    plan = [(k, b, t) for t in (1, 2) for b in BRIEF for k in kollar]
    if "--kuru" in argv:
        print(len(plan), "çağrı:", plan, "\nsistem uzunluğu:", {k: len(sistem(k)) for k in kollar})
        return 0
    kok.mkdir(parents=True, exist_ok=True)
    tsv, toplam = kok / "kanit.tsv", 0.0
    if not tsv.exists():
        tsv.write_text("kol\tbrief\ttekrar\tbayrak_n\tbayraklar\taudit\tbayt\tusd\ttur\tgirdi\tcikti\n", encoding="utf-8")
    for k, b, t in plan:
        if toplam >= TAVAN:
            print("TAVAN", toplam, flush=True)
            break
        t0 = time.time()
        satir = kos(k, b, t, kok)
        toplam += float(satir[7])
        with tsv.open("a", encoding="utf-8") as f:
            f.write("\t".join(map(str, satir)) + "\n")
        print(k, b, t, "bayrak", satir[3], "usd", satir[7], f"{time.time() - t0:.0f}s", flush=True)
    print("BITTI toplam_usd", round(toplam, 2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
