# ONAY kural prompt-teknoloji-dosya
ad: prompt-teknoloji-dosya
madde: Site/arayüz yaptırırken prompt'ta kullanılacak kütüphaneleri ve dosya yapısını (hangi dosya neyi taşır) açıkça yaz.
kaynak: video JfmAm3sxCSc, 15b
gerekce: Yeniden yapılandırma turu azalır (video: ilk prompt tek seferde çalışan site, ölçüm yok).
çift/çelişki: yok

Onay: `video kural-onay prompt-teknoloji-dosya` · ret: dosyayı sil.

# prompt-teknoloji-dosya
ad: prompt-teknoloji-dosya
tur: ipucu
video: JfmAm3sxCSc
karar: KUR
kural: Site/arayüz yaptırırken prompt'ta kullanılacak kütüphaneleri ve dosya yapısını (hangi dosya neyi taşır) açıkça yaz.
## Ne
Yapım prompt'unda teknoloji listesi (Three.js, GSAP, Lenis, Vite) ve JS/CSS dosya ayrımı açıkça verilir; çıktı istenen mimaride gelir.
## Kanıt
JfmAm3sxCSc 2:01 teknolojileri ve dosyaları prompt'ta sayıyor (docs/video-tarama/2026-09-24-JfmAm3sxCSc.md).
## Bizde durum
kısmen: skills/departman-frontend + omer-kutuphaneler kütüphane seçtiriyor; prompt'a dosya yapısı yazma kuralı yok.
## Beklenen fayda
Yeniden yapılandırma turu azalır (video: ilk prompt tek seferde çalışan site, ölçüm yok).
## Maliyet/risk
Kural dosyasına 1 satır; risk düşük.
## Karar
KUR (T0 kural, ONAY bekler).
## Sonraki adım
bekleyen/kural-*.md → Ömer `ONAY kural`.
## Geri alma
omer-kurallar.md eklenen satırı sil
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Prompt ne kadar detaylı olursa çıktı o kadar iyi olur (2:01) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | doğru | Be clear and direct: "being specific about your desired output" sonucu iyileştirir | - |
