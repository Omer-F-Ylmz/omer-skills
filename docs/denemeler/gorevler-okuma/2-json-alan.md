Aşağıdaki JSON dosyasında id'si S-1187 olan siparişin müşteri e-postasını, kargo takip numarasını ve durumunu çıkar. Yanıt tam 3 satır, biçim `alan: değer` (eposta, takip, durum); başka bir şey yazma.
oku: fixture/siparisler.json
araclar: Read,Grep,Glob
beklenen:
- olgu: ayse\.kaya@ornek\.test
- olgu: TK771204993
- olgu: (?i)iade
- satir-en-az: 3
- satir-en-fazla: 3
