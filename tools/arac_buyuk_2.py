"""ARAC-BUL-2 adım 3: arac-indir-2.tsv 'buyuk-ertelendi' repoları sırayla clone --depth 1 (arka plan, tek tek).
Her indirmeden önce boş alan ölçülür; indirme sonrası boş alan 30 GB altına inecekse BAŞLATILMAZ (sırada kalır). Kaldığı yerden devam eder.
Çıktı: .kos/kopru/rapor/arac-buyuk-2.tsv (ad, durum, boyut, tarama). Kullanım: python tools/arac_buyuk_2.py"""
import csv, os, shutil, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import arac_indir_1 as ai  # noqa: E402

GIRDI = os.path.join(ai.RAPOR, "arac-indir-2.tsv")
CIKTI = os.path.join(ai.RAPOR, "arac-buyuk-2.tsv")
TABAN_GB = 30


def _yaz_sil(fn, yol, _):  # Windows: git nesneleri salt-okunur, ignore_errors .part'ı bırakıyor → sonraki clone "dizin var" ile düşüyordu (23 Eki kök neden)
    if os.path.lexists(yol):
        os.chmod(yol, 0o700)
        fn(yol)


def bos_gb():
    return shutil.disk_usage("C:\\").free / 2**30


def main():
    with open(GIRDI, encoding="utf-8") as f:
        liste = [r for r in csv.DictReader(f, delimiter="\t") if r["durum"] == "buyuk-ertelendi"]
    with open(os.path.join(ai.RAPOR, "arac-bul-2.tsv"), encoding="utf-8") as f:  # arac_bul_2d'nin ertelediği >500MB repolar da sıraya girer
        gorulen = {r["ad"] for r in liste}
        for r in csv.DictReader(f, delimiter="\t"):
            if r["durum"] == "buyuk-ertelendi" and r["aday"] not in gorulen:
                gorulen.add(r["aday"])
                liste.append({"ad": r["aday"], "boyut": r["boyut"]})
    biten = {}
    if os.path.isfile(CIKTI):
        with open(CIKTI, encoding="utf-8") as f:
            biten = {r["ad"]: r for r in csv.DictReader(f, delimiter="\t") if r["durum"] == "indirildi"}
    sat = list(biten.values())
    for r in sorted(liste, key=lambda r: int(r["boyut"].rstrip("MB"))):
        ad, mb = r["ad"], int(r["boyut"].rstrip("MB"))
        if ad in biten:
            continue
        yol = os.path.join(ai.HEDEF, ad.replace("/", "__"))
        bos = bos_gb()
        if bos - mb / 1024 < TABAN_GB:
            sat.append({"ad": ad, "durum": "sirada-yer-yok", "boyut": r["boyut"], "tarama": f"bos={bos:.0f}GB"})
            print(ad, "YER YOK", f"{bos:.0f}GB", flush=True)
            continue
        if not os.path.isdir(yol):
            part = yol + ".part"
            shutil.rmtree(part, onerror=_yaz_sil)
            for _ in range(2):  # ilk koşuda boş çıktıyla HATA verenler (stdout-only) için: longpaths + stderr + bir yeniden deneme
                rc, o = ai.calis(["git", "clone", "--depth", "1", "--no-tags", "-c", "core.symlinks=false", "-c", "core.longpaths=true", f"https://github.com/{ad}.git", part], 3600)
                if rc == 0:
                    break
                shutil.rmtree(part, onerror=_yaz_sil)
            if rc != 0:
                sat.append({"ad": ad, "durum": "indirilemedi", "boyut": r["boyut"], "tarama": o.strip()[-80:]})
                print(ad, "HATA", o.strip()[-80:], flush=True)
                shutil.rmtree(part, onerror=_yaz_sil)
                continue
            os.rename(part, yol)
        sat.append({"ad": ad, "durum": "indirildi", "boyut": r["boyut"], "tarama": ai.tara(yol)})
        print(ad, "indirildi", sat[-1]["tarama"], f"bos={bos_gb():.0f}GB", flush=True)
        with open(CIKTI, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, ["ad", "durum", "boyut", "tarama"], delimiter="\t")
            w.writeheader(); w.writerows(sat)
    with open(CIKTI, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["ad", "durum", "boyut", "tarama"], delimiter="\t")
        w.writeheader(); w.writerows(sat)
    print("BITTI", len(sat), time.strftime("%H:%M"), flush=True)


if __name__ == "__main__":
    main()
