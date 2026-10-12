# P3 UYARLA listesi (12 satır → 6 hedef)

| sira | kaynak | hedef | nasıl |
|---|---|---|---|
| 270, 274, 275, 281, 342 | Dd1zrTggHCW reel skill seti (repo yok, ücretli) | yeni skill `reel-plan` (p3/skill/reel-plan/SKILL.md) | kurulu reel-taste'te olmayan üç parça: aykırı gönderiden hook madenciliği · tutma merdiveni denetimi · haftalık plan. 269/271/272/277–280 reel-taste+motion-studio karşılıyor (KURULU), 273/276 animasyon devri. claude.ai: dist/ig-40-p3/kendi/reel-plan.zip |
| 293 | danyuchn/asd-ste100-skill (MIT) | ~/.claude/CLAUDE.md "Closing report" kuralı (Ömer onayıyla) | tek satır: "tek anlamlı kelime, ≤20 kelimelik cümle, etken çatı". Skill kurulmaz: raporlar Türkçe |
| 295 | Shubhamsaboo/awesome-llm-apps (Apache-2.0) | docs/kaynak/awesome kaynak listesi | awesome-rehber taramasına kaynak satırı; kod kurulmaz |
| 296 | microsoft/SkillOpt (MIT) | tools/ogrenme/ders.py + skill-creator eval | iz-güdümlü düzenleme: başarısız iz → skill metnine tek düzenleme önerisi → doğrulama kümesinde geçmezse geri al (doğrulama kapısı). pip paketi LLM anahtarı ister; kurulmaz |
| 335 | Boss Loop prompt (IG) | departman-surec-plan kalite kapısı | işçi alt ajan çıktısı, görev başında verilen "çıta örneği"ne göre katı denetçi ajanca puanlanır; çıta altı → gerekçeyle işçiye geri, en çok 3 tur |
| 390–392 | skill yazım ipuçları | tests/test_claudeai_paket.py (yeni test) + skill-creator notu | (a) her SKILL.md ≤500 satır testi (bugün yok); (b) skill yazmadan önce skill'siz baseline koşusu — superpowers writing-skills RED aşamasıyla aynı, not düşülür |

Uygulama sırası: reel-plan zip'i onay betiğiyle CC'ye kopyalanır (skills/), claude.ai zip'ini Ömer yükler; 293/296/335/390–392 metin değişiklikleri ayrı dalga (canlı ~/.claude ve skill metni dokunuşu → onay).
