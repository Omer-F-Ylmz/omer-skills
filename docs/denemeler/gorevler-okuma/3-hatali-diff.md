Aşağıdaki büyük diff'te değişikliklerin çoğu davranışı koruyan yeniden adlandırma. Davranışı bozan tek değişikliği bul: dosya, fonksiyon ve neden. Yanıt en fazla 3 satır.
oku: fixture/degisiklik.diff
araclar: Read,Grep,Glob
beklenen:
- olgu: siparis_iptal
- olgu: src/\w+_41\.py
- olgu: (?i)\b(or|veya)\b
- satir-en-fazla: 3
