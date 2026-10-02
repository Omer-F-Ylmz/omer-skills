# TOKEN-2 — claude-mem observer önbelleği (L3)
TOKEN-2b tur: 17/20 — DUR (17. tur sınırı). Yama CANLI (13.25.2, --kontrol: yamalı).
Bitti: önce geçerli ($0.734) · yama+restart+health+gözlem 4744–4745 · sonra $0.672, kuyruk 0 (294 sn) · sonra compress 4 istek: 1h=0 ✓, 5m=0, okuma 54,556, ağırlıklı 66.6k, $0.067 · Ek3 ölçülemedi (vekil discovery_tokens ≈45.1M/12 gün, anlamı doğrulanmadı).
Kalan (TOKEN-2c):
1. kapi_analiz/kor_cift gözlem eşlemesi 0 döndü (content_session_id join tutmuyor) → t0–t2 penceresi + project ile eşle; önce/sonra gözlem sayısı ±%10.
2. "önce" penceresinde observer isteği 0, "sonra"da ana observer (diğer) 0 → transcript dizini/mtime filtresi doğrula.
3. DISABLE_PROMPT_CACHING altında compress cache_okuma 54.6k — neden, açıkla.
4. kor_cift.py → 10 çift, sonnet tanımlı ajanla kör puan (Agent aracında model parametresi yok; tanım üzerinden) → madde 21 kararı.
5. Kapanış: token_olc önce/sonra ($, ağırlıklı, çağrı başı, ×48/gün) · model sütunu sonnet · repo kodu değişmedi → suite yok · gitleaks → .claude/token2 commit · mühür · docs/token-2.md · arşiv · push. Önce geçerli ($0.73, kuyruk 0) · yama uygulandı + restart + health ok + gözlem 4744–4745 · kapi.py yoklaması 40 sn × ≤10'a çekildi · sonra koşusu arka planda.

KARAR: yol (c) hedefli yama. worker-service.cjs'te yalnız tek atımlık compress çağrısına (runStandaloneObserverPrompt, maxTurns:1) `DISABLE_PROMPT_CACHING:"1"` eklenir. (a) elenir: claude-mem ayarlarında TTL/önbellek anahtarı yok. (b) elenir: worker env'i kalıcı değil, ayrıca ana observer oturumunu da etkiler.
Teşhis: 46.2 M'in tamamı 678 tek atımlık compress isteğinden geliyor. Yükler benzersiz, sistem istemi boş, bu yüzden okuma olamaz. 1h, CLI'nin abonelik varsayılanı: settingSources:[] olduğu için settings.json:680 yüklenmiyor. Ana observer oturumu --no-session-persistence ile çalışıyor, transcript'i yok.

Kabul (değişmedi): K2 · Ek1 node --check + health + ≥1 gözlem, yoksa --geri ve DUR · Ek2 token_olc UYARI · Ek3 ana observer maliyeti ≤3 tur · K3 · K4.

Durum:
- K1 bitti (sonnet ajan).
- K2 bitti: kırmızı 32eef5e → yeşil 07dda53 (tests 28/28). Mutasyonlar: EK→1H kırmızı, UYARI kapalı kırmızı. Ek2 bu commit'e dahil.
- Canlı dosya henüz YAMASIZ (`python tools/cmem_yama.py --kontrol`); gerçek 13.25.2'de tek çapa doğrulandı.
- K3 önce koşusu arka planda sürüyor (.claude/token2/kapi.py once). Sonucu olcum/token-2-kapi-once.json'a yazacak, istem olcum/token-2-istem.txt.
- Başlangıç mühürü: .claude/token2/muhur-bas.json (settings 3c572ce1 · mcpServers 23452893 · hooks a0801fdf · plugin 47/53 · mcp 19 · skill 1054).
- .claude/token2/ gitignore'da DEĞİL (untracked). K4'te karar verilecek: commit'e girmez.

Kalan iş (sırayla):
1. olcum/token-2-kapi-once.json'u oku: session_id, cost, son_durum.queueDepth=0 mı?
2. `python tools/cmem_yama.py` (node --check otomatik) → `curl -s -X POST localhost:37777/api/admin/restart` → /api/health + /api/processing-status yanıtı → ≥1 yeni gözlem (claude-mem.db ro). Biri başarısızsa `python tools/cmem_yama.py --geri` ve DUR.
3. `python .claude/token2/kapi.py sonra` (2. ve son claude -p, ≤$1.5).
4. Kanıt: once/sonra pencerelerindeki (t0–t2) observer transcript'lerinde compress isteklerinin 1h yazması = 0 olmalı. Gözlem sayısı ±%10 (sorgu: observations JOIN sdk_sessions ON memory_session_id, content_session_id=session_id). 10 gözlem çifti kör puanlanır (K1 ajanına SendMessage). Karar: omer-kurallar 21.
5. Ek3: ana observer gerçek maliyeti (sırayla headroom kaydı → ~/.claude-mem/logs + db). ≤3 tur, bulunamazsa "ölçülemedi". Müdahale yok.
6. K4:
   - `python tools/token_olc.py olc --kok ~/.claude/projects/C--Users-pc--claude-mem-observer-sessions --gun 1`: çağrı başı ağırlıklı ve $, günlük tahmin (678/14 ≈ 48 çağrı/gün).
   - tests/ suite (pipefail).
   - `python .claude/token2/muhur.py .claude/token2/muhur-bas.json` → MÜHÜR EŞİT.
   - diff-filter=D boş · gitleaks.
   - docs/token-2.md: TOKEN-6 SessionStart uyarı notu + Ek3 sonucu + sıradaki kaldıraç adayı.
   - Arşiv: dalga.md → .claude/dalga-arsiv/TOKEN-2.md.
   - commit + push.
