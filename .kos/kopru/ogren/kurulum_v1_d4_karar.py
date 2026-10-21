"""KURULUM-V1 d4: sonuc2.tsv'de biten adayların kararını plan.tsv'ye yazar (karar=13., komut=14. sütun).
Kullanım: python kurulum_v1_d4_karar.py <ad>|<karar>|<komut>  [...]   (karar boşsa satır atlanır; CRLF'siz bayt yazımı)"""
import sys

P = r"C:\Projeler\omer-skills\.kos\kopru\ogren\kurulum-v1-plan.tsv"
yeni = {}
for a in sys.argv[1:]:
    ad, karar, komut = a.split("|")
    yeni[ad] = (karar, komut or "-")
satir = open(P, encoding="utf-8", newline="").read().split("\n")
for i, l in enumerate(satir):
    c = l.rstrip("\r").split("\t")
    if c[0] in yeni and len(c) == 14:
        c[12], c[13] = yeni.pop(c[0])
        satir[i] = "\t".join(c)
if yeni:
    sys.exit(f"plan'da yok/sütun sayısı 14 değil: {list(yeni)}")
open(P, "w", encoding="utf-8", newline="").write("\n".join(satir))
print("yazıldı")
