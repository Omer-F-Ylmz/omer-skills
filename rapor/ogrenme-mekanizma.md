# Öğrenme mekanizmaları, envanter ve eksikler (ÖĞRENME-2, 23 Eki)

Doğrulama: ✔ = bu oturumda dosyası/kodu okundu; ~ = ad/açıklamadan (derin okuma yapılmadı, sonra doğrulanır).

| Mekanizma | Ne öğreniyor | Saklama | Geri verme | Doğrulama | Maliyet |
|---|---|---|---|---|---|
| beyin (beyin_dusun/kayit) ✔ | araç olayları, hata, maliyet → öneri | beyin-olay.jsonl, öneriler (durum makinesi taslak→kural/elendi) | SessionStart ≤20 satır özet | destek ≥3 + çelişki testi (Jaccard ≥0.4) + etki defteri | $0 (ücretsiz havuz/ollama) |
| MAKARA (makara_gece) ✔ | skill/kural önerisi, gece şeritleri | kum havuzu .kos/makara/kum | onay betiğiyle gerçek dosyaya | held-out + 2 farklı aile hakem | $0, günde 1 gece |
| skillopt-sleep ✔(SKILL.md) | geçmiş oturumlardan yinelenen görevler | CLAUDE.md/SKILL.md "learned" bloğu | yama olarak benimseme | held-out kapı; sınırlı add/delete/replace | backend'e bağlı |
| ruflo pattern-store/feedback ~ | desen + güven | agentdb | pattern-search (iş başı) | confidence alanı | $0 |
| claude-mem ~ | oturum gözlemleri | yerel DB | mem-search / mem2 | yok (kayıt) | kuyruk $ riski (park notu) |
| agentmemory ~ | gözlem, recall/handoff | yerel | recall, handoff, recap | yok | $0 |
| task-observer ~ | beceri iyileştirme fırsatları | gözlem günlüğü | haftalık gözden geçirme → skill güncelleme | insan | düşük |
| continuous-learning / learn ~ | oturumdan kalıp | learned skill | skill olarak | yok | düşük |
| context-engineering ~ | öğrenme değil, bağlam yöntemi | skill | yükleme |, |, |
| ders-bankası (tools/ogrenme/ders.py) ~ | ders havuzu | dosya | ön söz enjeksiyonu (onsoz.py) | ab_olc.py A/B | $0 |
| Laya + jev ~ | puanlama/yargıç |, | puan | ücretsiz yargıç kurulu | $0 |
| Threesided Agent-Memory, Skillopt (Microsoft) ~ |, |, |, |, | derin okunmadı |

## Bizde eksik olanlar (seçilen)
1. **Uyku-zamanı yansıtma → yama önerisi**: MAKARA kural üretiyor ama "günün olayları → ne iyi/pahalı/işe yarayan ders" günlük notu yok. skillopt-sleep'in held-out kapısı bizde MAKARA'da var; eksik olan günlük yansıtma ve SKILL.md yama dosyası.
2. **Sınav (dersli/derssiz tekrar senaryosu)**: ab_olc.py A/B altyapısı var; 20 senaryoluk haftalık sınav seti yok.
3. **Canlı gösterge**: yoktu → bu oturumda eklendi (`tools/beyin_dusun.py gosterge`, beyin-ozet.md son satır).
4. **Kaynak/tarif kartı enjeksiyonu**: kaynak-tam-1/USTALIK-1 kartları beyne bağlı değil.
5. **Çapraz öğrenme (claude.ai zip)**: haftalık ders özeti zip'e girmiyor.

## Taban (7 gün, 23 Eki)
iş başı ort. $0.82 (önceki 7 gün $2.75) · tekrar eden hata %11 (36 hata) · kurala dönen 0 · geri çekilen 0 · bugün 384 olay, 27 yeni ders.

## Yapılan / yapılmayan
- Yapıldı: madde 5 (gösterge) + test; madde 1 envanter tablosu.
- Yapılmadı: madde 2 (yansıtma betiği), 3 (sınav), 4, 6, sıradaki oturum; neden: kapsam büyük, settings/skills dizinleri kurulum-dalgasi-2'ye ait (yazma yasağı), SKILL.md yamaları yalnız öneri dosyasına yazılır.
- Sıradaki: `tools/ogrenme/yansit.py` (olay → ücretsiz model → Obsidian günlük + `.kos/kopru/yama-oneri.md`), sonra `sinav.py` (ab_olc.py üstüne).
