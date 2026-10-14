# TOKEN-3 devam (d1 → d2) — 14 Eki ~18:05
Görev: .kos/kopru/gorev/token-3.md (bütçe/kurallar orada; VEKİL KAZASI: ANTHROPIC_BASE_URL'ye dokunma). claude -p kalan: 4/6.
Yapılan (rapor/token-3.md d1): K10 blok farkı çıkarıldı; plugin ajan deny'ı cc_profil.py + sunucu.mjs'te (testler yeşil).

## d2 sırası
1. K10 gerçek ölçüm (≤2 claude -p): `.claude/token3/onek_kayit.py` üst portu (UST=6769) d1'de reddetti. Önce 6767/6768/6769'dan hangisi dinliyor bak (yalnız soket yoklama, env değeri basma); UST'yi düzelt; `python .claude/token3/onek_kayit.py b 2` → 1. istek cw/cr önce (d1 tabanı cw ~24k, cr 6.6k) / sonra; msg1 karakter boyu düşüşünü gövdeden doğrula (ajan listesi 16.6k→?).
   Kalite kapısı: 1 küçük köprü/ajan_sira işinin çıktısı değişmiyor mu (proje ajanları hâlâ çağrılabilir).
2. K10 öneri (global → yalnız onay betiği --kuru): git durumu sabitleme (`includeGitInstructions:false` / CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS — binary'de var, git status'u kaldırıp kaldırmadığı yakalanan gövdeyle 0 API sınanabilir: kayıt vekili üst yerine 500 dönsün), claude-mem damgasının dakikalık olması.
3. K11: ajan_sira.tsv 4. sütun efor=medium|high → ARGV'ye `--effort` (köprüde effort parametresi zaten var, KÖPRÜ-EFFORT-1). ajan_sira.py kuyruk() şu an 3. sütunu koşul diye okuyor; 4. sütunu ekle, test + 1 örnek kalite kapısı.
4. K12: token_dagilim.py alt ajan kırılımı (ana oturum → alt ajan türü/token) — yerel betik.
5. K13: ölçüm koşuları için aynı istem öneki + 5 dk pencere; seçim kıyası 196 görev maliyet tahmini.
