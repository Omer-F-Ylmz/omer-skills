r"""TELVE-TOKEN-1 d3 onay betiği: DEVAM-KURALI.md'ye önbellek durması + M5 bölünme kuralı (son paragraf olarak) eklenir.

Kullanım: python C:\Projeler\omer-skills\.kos\kopru\onay\token1_durma_kural.py          # yedek + uygula
          python C:\Projeler\omer-skills\.kos\kopru\onay\token1_durma_kural.py --kuru   # canlıya DOKUNMAZ: geçici kopyaya yazar
Yalnız sona ekler; mevcut satırlar aynen. İkinci kez çalışırsa ekleme yapmaz.
"""
import hashlib, shutil, sys, tempfile, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
D = Path(r"C:\Projeler\omer-skills\.kos\kopru\gorev\DEVAM-KURALI.md")
KURAL = ("\nDESKTOP 14 Eki (TELVE-TOKEN-1 d3) ÖNBELLEK DURMASI: `python C:/Projeler/omer-skills/.kos/kopru/durum_ozet.py <görev> <wt>`"
         " son satırı `-- durma: … son N adımda D (%X)` verir (durma = cache yazma 0 ve önbelleksiz girdi ≥3k; kök neden CC istemcisi/Opus"
         " ≥2.1.288, TTL değil). Her 15 dk ara kayıtta bu satıra bak; %X ≥30 ise: ara kayıt (madde 4 a–d) + DUR → Desktop yeni oturum açar."
         " /compact KULLANMA (kırılma zaten tam yazma; -p oturumunda yok). Köprü ayarı değişmez."
         " BÖLÜNME (M5, ölçülen): yeni oturum ~100–155k tek sefer, sürdürmek adım başı ~0.1·C (C = bağlam) → C ≥200k ve ≥8 adım"
         " kaldıysa (C=150k'da ≥13) aynı biçimde ara kayıt + DUR.\n")


def calis(kuru):
    metin, once = D.read_text(encoding="utf-8"), hashlib.sha256(D.read_bytes()).hexdigest()
    if "TELVE-TOKEN-1 d3) ÖNBELLEK DURMASI" in metin:
        return print("ZATEN VAR: değişiklik yok")
    if kuru:
        hedef = Path(tempfile.mkdtemp(prefix="t1-durma-kuru-")) / D.name
    else:
        shutil.copy2(D, D.with_name(D.name + time.strftime(".bak-t1d-%Y%m%d%H%M%S")))
        hedef = D
    hedef.write_text(metin.rstrip("\n") + "\n" + KURAL, encoding="utf-8")
    yeni = hedef.read_text(encoding="utf-8")
    assert yeni.startswith(metin.rstrip("\n")) and yeni.count("ÖNBELLEK DURMASI") == 1
    print(f"{'KURU' if kuru else 'UYGULANDI'}: {hedef} · +{len(yeni.splitlines()) - len(metin.splitlines())} satır (yalnız sona)"
          f" · canlı sha256 {'aynı' if hashlib.sha256(D.read_bytes()).hexdigest() == once else 'DEĞİŞTİ'}")


if __name__ == "__main__":
    calis("--kuru" in sys.argv)
