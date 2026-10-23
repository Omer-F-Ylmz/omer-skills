KAYNAK-TAM-FIX-1 ilerleme (23 Eki)
- Kök neden: ücretsiz havuz 429 (gemini/mistral/omniroute) + ministral JSON dışı yanıt; eski kod 3 deneme/15-45 sn sonra "hata" yazıyordu.
- Düzeltme e456dc7f: hata ayrıntısı loga, soğuma bitimini bekleyerek 10 deneme, günlük kota (>900 sn) -> "kota" ile dur.
- 20'lik deneme x2: 19/20 ok her seferde (%5 hata, hedef %2 tutmadı); hata işleri önbelleksiz, sonraki koşuda yeniden denenir.
- Devam: python -I .kos/kopru/arka.py --bagimsiz .claude/kaynak_tam_llm.log tools/kaynak_tam.py llm --is 4
