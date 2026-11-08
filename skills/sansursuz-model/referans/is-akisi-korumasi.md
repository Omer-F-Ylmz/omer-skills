# İş akışı koruması

Amaç: skill çalışırken Ömer'in düzeni bozulmasın.

## Dokunma
- Yazma alanı: `skills/sansursuz-model/**`, `tmp/ss4/**`, `.kos/kopru/arka/sansursuz-*.md`, `rapor/sansursuz-*.md`, `dist/`.
- Bu alan dışına yazacaksan önce sor değil — yaz, sonra tek satırda bildir.
- Var olan dosyanın üstüne yazarken `.bak` bırak. Silme yok. `git push` yok.
- NİHAİ 1–43 geçerli.

## Onay sorma
"Devam edeyim mi", "ister misin", "hangi seçenek" yasak. Seç, yap, tek satırda gerekçe.

## Adım
Tek komut = tek adım. Aynı mesajda 3'ten fazla komut yığma. Uzun işi arka plana al, ilerleme yaz.

## İlerleme
10 dakikada bir `.kos/kopru/arka/sansursuz-<n>-ilerleme.md`'ye tek satır: ne yapıldı, ne kaldı, engel.

## Rapor
≤15 satır. İlk satır `BITTI` ya da `DUR`. `DUR` ise tek satır neden + denenen yedekler.

## Kaynak
RAM %95, VRAM %95, disk 40 GB altına inerse küçült. Küçültme yetmiyorsa bulut.

## İndirme
İndirilenleri sonda listele. Büyük indirmeyi arka planda bırak, önünü kapatma.

## Bozulursa
Mevcut akış bozulduysa önce onu geri al (`.bak`'tan), skill'i sonra sürdür. Bozuk hâlde ilerlemek yasak.
