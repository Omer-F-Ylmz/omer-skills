# Blender üretim skill'i (BLENDER-SKILL · 1 Eki 2026)

KARAR: skills/blender-uretim orkestra (akış, sıra, kalite kapısı); blender-oturum oturum ve araç skill'i; çift yönlü atıf, içerik tekrarı yok. Tablolarda kaynak sütunu (#no · video id · öneri).

## Dört ölçüt
- **blender-uretim** bakım: repo içi, testli (tests/test_blender_uretim_skill.py: bpy_kontrol + gerçek Blender 5.2.1 boş sahne) · çift: hayır (oturum/araç blender-oturum'da) · izin: md + iki bpy betiği (dosya/ağ/süreç yok) · context: description 171 karakter; SKILL kısa, references yalnız gerekince.
- **ra100/blender-claude-plugin** bakım: ★17, son commit 2026-04-29 · çift: kısmen (search_api_docs / get_python_api_docs aynı bilgiyi canlı verir) · izin: yalnız md (8 SKILL, script/hook/MCP yok), MIT · context: SKILL.md 13.4k kelime, toplam md 45k (yalnız tetiklenince) · SkillSpector --no-llm: 0 bulgu ama 13 statik analizör "degraded" → kurmadan önce LLM'li tarama. Kurulum Ömer'de, oturum başında: `/plugin marketplace add ra100/blender-claude-plugin` → `/plugin install blender-skills@blender-claude-marketplace`.
- **emalorenzo/three-agent-skills**: LICENSE dosyası yok (GitHub lisans alanı boş) → web-sahne-desenleri'ne eklenmedi.

## Araç düzeltmesi
blender_pisir: `--png16` (16 bit PNG) + 8 bit PNG'de lightMapIntensity > 2 → SONUC `uyari` (öneri --hdr / --png16).

## Tetikleyici tablosu (20 gerçek claude -p, --max-turns 1)
- Olumlu 10/10 tetikledi (çoğunda blender-oturum da yüklendi).
- Olumsuz 10/10 Skill çağrısı yok; komşu 4: mod-atolyesi ×2, threejs-bloom, gorsel-uret seçildi. 1 satır ölçer artefaktı (Bash komut metninde dosya yolu).
- skill-creator run_eval Windows'ta çalışmıyor (select() pipe, WinError 10038) → tek seferlik betik.
- Ölçüm uzun description ile yapıldı; skill_denetim 200 karakter sınırı için kısaltıldı, çağrı tavanı yüzünden yeniden ölçülmedi.

## Ölçüm (BLENDER-OLCUM · 2 Eki 2026)
A/B fincan (skill kapalı/açık): B tekrar teslim + kapı geçti ama kör puan 3.4 = A (ölçüt ≥ 3.9) ve $12.26 = 2.5 × A (ölçüt ≤ $6); maliyetin %60'ı teslimden sonraki render/sahne turlarında → "kısa rehber" moduna geçiş (ayrı dalga). Ayrıntı: docs/denemeler/blender-uretim-olcum.md.

## 5.2 API notları (canlı sorgu)
Doku çıkışı ve ColorRamp girişi `Factor` (eski `Fac`) · compositor'da Mix = ShaderNodeMix (A/B/Result) · `scene.compositing_node_group` · ışık `use_temperature` · `visible_camera` · light linking `receiver_collection`.
