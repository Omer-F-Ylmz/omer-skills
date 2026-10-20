# MEM-FIX-4 — KISMİ (DUR: gözlem sayısı artmadı, üç halka da kotada)
1. Neden: gemini cooldown'daydı ve yedek `mem-yedek` combo'su Gemini'siz kuruluydu (nemotron :free → gemma → super → groq); OpenRouter :free halkaları "All credentials cooling down" (429), Groq TPD 197595/200000 → observer fiilen Groq'a düşüyordu; Groq 200+gövde-429'u claude-mem "quota exhausted (status 200)" diye 30 dk cooldown'a çevirdi (observer-health.json, worker log 16:48).
2. Düzeltme: combo = gemini/gemini-3.1-flash-lite → OpenRouter :free ×3 → Groq (tools/mem_fix_omni.py ZINCIR, yeniden kuruldu); settings: CLAUDE_MEM_PROVIDER=openai-compatible (mem-yedek), QUOTA_FALLBACK boş — claude-mem'in Gemini cooldown'unu bypass eder; cooldown dosyası sıfırlandı, worker yeniden başladı.
3. Bekçi: tools/mem_bekci.py uyarı satırı artık "gozlem sayisi 30 dk sabit (son gozlem N dk)".
4. Doğrulama ✗: gözlem 29449 (maks id 29458) 16:35→17:00 sabit. Yoklama: Gemini 504 (OmniRoute yerel hız sınırı süresi), OR :free hepsi cooling down, Groq TPD ~9 dk; claude-mem Groq cooldown'u ~17:20'ye kadar. Kota açılınca (Groq gece/TPD) kendiliğinden akar; sınama aracı tools/mem_zincir_yokla.py.
5. Ücretli çağrı 0, yerel model yok, Claude yok. Commit yalnız 3 yol, push yok.
SIRA: MEM-FIX-4 KISMİ
