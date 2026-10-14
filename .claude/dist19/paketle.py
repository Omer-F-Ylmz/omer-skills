"""DIST-19: claude.ai zip'leri fa2750d commit içeriğinden (git archive; çalışma ağacındaki commitsiz değişiklik girmez).
13 departman-* (dizin_uret.dosyalar süzgeci: ajanlar/ yalnız KALITE3) + yetenek-getir (ARA SÜRÜM). plan-kur hariç (kapı RET).
  python .claude/dist19/paketle.py   → dist/claude-ai-19/<skill>.zip + LISTE.md (CC kuru bölümü elle eklenir)"""
import io, json, re, subprocess, sys, tarfile, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "skill-paket"), str(KOK / "tools" / "secim")]
import zip_denetle, dizin_uret  # noqa: E402

REV, ESKI = "fa2750d", "6acd6bd"
DIST = KOK / "dist" / "claude-ai-19"
ID = {"departman-arastirma-ogrenme": "01CZAK3UC5fg1HqwizEh4okW", "departman-backend-dotnet": "01Psv9rXkPXbBJ8kapxJEB2J",
      "departman-belge": "01SrhWAeW8Lu5th8mHnmu94d", "departman-guvenlik": "01JK2Lu5hfQpz5LiALKgpGBS",
      "departman-surec-ajan-arac": "01AF1LNfpQdrjfGHj74bHVQ7", "departman-surec-git-yayin": "01H7z8utXE1GMfeCZiNooyjb",
      "departman-surec-inceleme": "011gD4KdpyVKRDJkbwCaqnxt", "departman-surec-plan": "01HB9k9eaPDHk4gU7vFsfzsk",
      "departman-test-qa": "011YWGaXHF3BMtAFg16A6cY2", "departman-veri-db": "012npkZd1AbuwbrcxkahhqpM",
      "departman-verimlilik": "018Kpf8nP4rjacdZjDhH28WV", "departman-frontend": "skill_01CHBvYpGKTyed5UPh3usNUp",
      "departman-diger": "skill_01VFvgDetg9eeeWf7UHKqoak", "yetenek-getir": "bilinmiyor (verilmedi) → claude.ai'de yoksa YENİ YÜKLEME"}
KATALOG = "SKILL.md +1 koşullu katalog satırı (KATALOG-KANCA-1)"


def git(*a):
    return subprocess.run(["git", "-C", str(KOK), *a], capture_output=True, check=True).stdout


def degisen(ad):
    return [s for s in git("diff", "--name-only", ESKI, REV, "--", f"skills/{ad}").decode().split() if s]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    DIST.mkdir(parents=True, exist_ok=True)
    satir, sorunlar = [], []
    with tempfile.TemporaryDirectory() as t:
        tarfile.open(fileobj=io.BytesIO(git("archive", REV, "skills"))).extractall(t, filter="data")
        for ad in ID:
            d = Path(t) / "skills" / ad
            dosya = dizin_uret.dosyalar(d) if ad.startswith("departman-") else sorted(p for p in d.rglob("*") if p.is_file())
            zp = DIST / f"{ad}.zip"
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                for f in dosya:  # archive yalnız dosya listesi için; core.autocrlf=true .py/.jsonl'yi CRLF yapar → blob baytı
                    rel = f"{ad}/{f.relative_to(d).as_posix()}"
                    z.writestr(rel, git("show", f"{REV}:skills/{rel}"))
            on = zip_denetle._on_bilgi((d / "SKILL.md").read_text(encoding="utf-8"))
            s = zip_denetle.denetle(zp)
            if on.get("name") != ad or len(ad) > 64 or not re.fullmatch(r"[a-z0-9-]+", ad):
                s.append(f"{ad}: name '{on.get('name')}' klasör adıyla/claude.ai biçimiyle uyuşmuyor")
            sorunlar += s
            dg = degisen(ad)
            if ad == "yetenek-getir":
                ozet = (f"ARA SÜRÜM (ENVANTER-4 tarif/kılavuz ekleyecek) — yeni skill: katalog_ara + yetenek.jsonl/tsv"
                        f" + ogrenim.jsonl (öğrenim kataloğu); docs/katalog/ek.jsonl adayları yetenek.jsonl içinde ({ek_kapsama()})")
            else:
                ajan = [a.split("/")[-1] for a in dg if "/ajanlar/" in a]
                girdi = [a for a in ajan if (d / "ajanlar" / a) in dosya]
                ozet = KATALOG + (f"; TOKEN-12 ajan açıklama onarımı {len(ajan)} ({', '.join(a[:-3] for a in ajan)};"
                                  f" zip'e giren {len(girdi)})" if ajan else "")
            satir.append(f"- **{ad}** · ID {ID[ad]} · {ozet} · {len(dosya)} dosya, {zp.stat().st_size / 1024:.1f} KB"
                         f" · description {len(on.get('description', ''))} kr · {'TEMİZ' if not s else 'SORUN'}")
    bas = [f"# DIST-19 claude.ai zip'leri ({REV} commit içeriği, git archive; değişiklik tabanı {ESKI})", "",
           "Yükleme: claude.ai → Settings → Capabilities → Skills → aynı adlı skill'in yerine yükle (yetenek-getir yeni).",
           "plan-kur HARİÇ (ENVANTER-3 kör kapı 2× RET). CC'deki departman-* claude.ai senkron kopyasından gelir → bu yükleme CC'yi de günceller.",
           f"zip_denetle: {'TEMİZ ' + str(len(ID)) + ' zip' if not sorunlar else '; '.join(sorunlar)}", ""]
    (DIST / "LISTE.md").write_text("\n".join(bas + satir) + "\n", encoding="utf-8")
    print("\n".join(sorunlar) or f"TEMİZ {len(ID)} zip → {DIST}")
    return 1 if sorunlar else 0


def ek_kapsama():
    ek = [json.loads(s) for s in git("show", f"{REV}:docs/katalog/ek.jsonl").decode("utf-8").splitlines() if s.strip()]
    anahtar = next(k for k in ("ad", "name", "id") if k in ek[0])
    var = {json.loads(s).get(anahtar) for s in git("show", f"{REV}:skills/yetenek-getir/yetenek.jsonl").decode("utf-8").splitlines() if s.strip()}
    return f"{sum(e[anahtar] in var for e in ek)}/{len(ek)}"


if __name__ == "__main__":
    sys.exit(main())
