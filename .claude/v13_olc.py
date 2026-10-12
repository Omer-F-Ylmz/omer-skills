"""VİDEO-13-devam ölçümü, v10_olc.py kopyası — altın 4 video × kollar {taban (VIDEO_JETON verilmez = şu anki varsayılan) · K · C2K} × 3 tekrar.
Tekrar dışta, kol içte (erken durursa eşleştirilmiş kalır). Σ USD ≥ 19 → dur (API ≤ $20). Canlı runner'a dokunmaz: ayrı VIDEO_CACHE (kopya,
paket dahil → kollar aynı paketi görür), ayrı VIDEO_TARAMA_DIZIN + VIDEO_UYGULA_KOK. ASR_ONAR kolu yok: paket yeniden kurulumu gerekir (kanıt yok)."""
import json, os, re, shutil, subprocess, sys, time
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
ONB = Path(r"C:\Projeler\.video-cache")
CACHE = Path(r"C:\Projeler\.video-cache-v13")
PARTILER = {"short": ["FaChtkkG9X4", "aZe5ZTYcF1M"], "uzun": ["1nGx7WR8YLE", "HYMDaMcuSGQ"]}
TAVAN = {"short": "0.40", "uzun": "1.00"}
KOLLAR = sys.argv[1:] or ["taban", "K", "C2K"]
VIDEO = ["uv", "run", "--project", str(KOK / "tools" / "video"), "video"]
DIS = ("ikinci_goz", "tavan", "omniroute_baslat", "paket_yenilendi")  # parti._defter ile aynı süzgeç
TOPLAM = 0.0

for v in sum(PARTILER.values(), []):
    if not (CACHE / v).exists():
        shutil.copytree(ONB / v, CACHE / v)
for tk in (1, 2, 3):
    for kol in KOLLAR:
        for tur, vids in PARTILER.items():
            if TOPLAM >= 19:
                print(f"DUR Σ usd={TOPLAM:.3f}", flush=True)
                sys.exit(0)
            tdir = KOK / ".claude" / "v13" / f"{kol}-{tur}-{tk}"
            tdir.mkdir(parents=True, exist_ok=True)
            satir = [f"| {v} | {round((json.loads((CACHE / v / 'meta.json').read_text(encoding='utf-8')).get('duration') or 0) / 60, 1)} | altin | v13 | bekliyor |" for v in vids]
            (ky := tdir / "kuyruk.md").write_text("| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n" + "\n".join(satir) + "\n", encoding="utf-8")
            env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(tdir), "VIDEO_CACHE": str(CACHE), "VIDEO_UYGULA_KOK": str(tdir / "kok"), "VIDEO_PUSH_YOK": "1"}
            env.pop("VIDEO_JETON", None)
            if kol != "taban":
                env["VIDEO_JETON"] = kol
            print(f"== tekrar {tk} kol {kol} {tur}", flush=True)
            t0 = time.time()
            r = subprocess.run([*VIDEO, "parti", "baslat", str(ky), "--tarih", f"v13-{kol}-{tk}", "--ikinci-goz", "yok", "--en-fazla", "3",
                                "--cagri-tavan", "12", "--cagri-tavan-max", "12", "--usd-tavan", TAVAN[tur], "--usd-tavan-max", TAVAN[tur]],
                               env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
            sure = time.time() - t0
            print(f"rc={r.returncode}", r.stdout[-600:], r.stderr[-400:], sep="\n", flush=True)
            jt = usd = 0
            for df in (tdir / "kok").rglob("defter.jsonl"):
                for x in (json.loads(s) for s in df.read_text(encoding="utf-8").splitlines() if s.strip()):
                    if not x.get("adim", "").startswith(DIS):
                        jt += sum(x.get(a) or 0 for a in ("girdi", "onb_okuma", "onb_yazma", "cikti"))
                        usd += x.get("usd") or 0
            TOPLAM += usd
            print(f"OZET {tk} {kol} {tur} jeton={jt} usd={usd:.3f} sure={sure:.0f} Σusd={TOPLAM:.3f}", flush=True)
            subprocess.run([*VIDEO, "parti", "iptal", f"v13-{kol}-{tk}-{tur}", "--neden", "VİDEO-13 olcum partisi"], env=env, capture_output=True)
            for v in vids:
                if not (rap := sorted(tdir.glob(f"*-{v}.md"))):
                    print(f"PUAN {tk} {kol} {v} RAPOR YOK", flush=True)
                    continue
                a = KOK / "docs" / "video-tarama" / "altin" / f"{v}.json"
                p = subprocess.run([*VIDEO, "altin", "puan", str(rap[-1]), str(a)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace") if a.is_file() else None
                d = subprocess.run([*VIDEO, "rapor-denetle", str(rap[-1])], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
                y = re.search(r"adaylar: yakalama (\d+)/(\d+).*?ad yazım (\d+)/(\d+)", p.stdout) if p else None
                k = re.search(r"komutlar: yakalama (\d+)/(\d+)", p.stdout) if p else None
                u = re.search(r"urller: yakalama (\d+)/(\d+)", p.stdout) if p else None
                print(f"PUAN {tk} {kol} {v} aday/ad={' '.join(y.groups()) if y else '?'} komut={'/'.join(k.groups()) if k else '?'} "
                      f"url={'/'.join(u.groups()) if u else '?'} denetle_rc={d.returncode}", flush=True)
print(f"BITTI Σusd={TOPLAM:.3f}", flush=True)
