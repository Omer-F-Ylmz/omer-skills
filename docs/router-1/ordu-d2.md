# ORDU-1 d2 kapı (21 Eki)
20 held-out iş (6 kolay·6 orta·6 zor·2 imkansiz), mekanik kabul; A = 3 toplu Sonnet high, B = merdiven (ücretsiz → Haiku medium → Sonnet medium → Opus medium).
Sonuç: kalite 1.0=1.0, başarısızlık 0=0, Claude token B/A = 0.805 (17156/21308) → KAPI GEÇMEDİ (hedef ≤0.50); USD −%35 (0.059/0.091). Bayrak kapalı kaldı.
Neden: ölçüm 3 toplu çağrı; çağrı başı sabit yük (~4.7k) iki kolda aynı, zor+imkansiz çağrıları B de Claude ile yapıyor; tasarruf yalnız kolay+orta toplusundan (10/12 ücretsiz geçti, O3/O4 Haiku medium). Ücretsiz zincir: 36 çağrı (Gemini 404, nemotron kota, Groq taşıdı).
Yinelemek: python tools/olcum/ordu_olc.py <dizin> (ham yanıt önbelleği → yeniden koşu ücretsiz).
