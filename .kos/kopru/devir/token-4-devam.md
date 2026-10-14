# TOKEN-4 devam (d2 → d3) — 14 Eki ~23:15
Görev: .kos/kopru/gorev/token-4.md (VEKİL KAZASI geçerli). claude -p 3/6 harcandı. Ayrıntı: rapor/token-4.md d2.
SON COMMIT: d2 ara (hr_ab.py tek vekil + RAM bekçisi, mem_kiyas.py doğrudan Gemini + cc-yedek-dis yargıç).
KALAN (öncelik):
1. A2: hr_ab.py ISTEM'i ≥20 içerik bloklu mesaj üretecek şekilde değiştir (ör. 3 turda 8'er paralel Read) — d2'de iki kolda durma 0 çıktı, karşılaştırma boş. Koşu: `python .kos/kopru/arka.py .claude/token4/hr_ab3.log .claude/token4/hr_ab.py ABAB` (≤3 claude -p kaldı), RAM <%75. Bitince vekil_dene 401.
2. A3: Gemini API 429 (kota). Alternatif yalnız kota çakışmasız bir yol bulunursa (CLAUDE_MEM_OPENROUTER_BASE_URL → OmniRoute?) `python .claude/token4/mem_kiyas.py 20`; yoksa A3 kapalı.
3. A1 kaçak kaynağı: rtk rewrite çalışıyor, cc_profil kancaları koruyor → hangi oturum türü kancasız (Desktop? alt ajan?) belirle.
4. A4 öz hattı, A5 qmd, 4 iş kapısı, onay/token_4_uygula.py --kuru (yalnız geçen öneri), zip (paketle.py → dist/claude-ai-27 + zip_denetle).
5. Bitince gorev/SIRA.md "TOKEN-4 BİTTİ".
ARKA PLAN: yok.
