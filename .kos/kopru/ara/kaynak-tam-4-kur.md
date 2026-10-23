# KAYNAK-TAM-4 kurulum kuyruğu taslağı (öncelik ilk 10; kurulum Desktop onayıyla)
Kaynak: kartlar/tarif/*.md. Komut yalnız kartta birebir varsa yazıldı; yoksa "kart yok". Lisans her satırda kurulumdan önce okunur (MIT/Apache değilse koşul rapora).

| # | tarif | durum | kur/indir | komut/kaynak (kartta) | not |
|--|--|--|--|--|--|
| 1 | bug-bounty-otomasyon-DdA-QjwAMh_ | KUR-sonra | Pentest Agents (uv, Python 3.10+, MCP) | `uv run python3 tools/scaffold.py hackerone tesla` | repo adı kartta yok → video açıklamasından bul; gerçek hedefe (hackerone/tesla) tarama yetki kanıtı olmadan koşulmaz, yalnız kurulum |
| 2 | video-kurgu-Dery8BLNDJK | kurulu | HyperFrames skill | `npx skills add heygen-com/hyperframes` | hyperframes-paket zaten kurulu → yalnız sürüm karşılaştır |
| 3 | otomasyon-DcQwBpXDSXs | KUR | n8n + Self-hosted AI Starter Kit (Ollama, Qdrant, Postgres) | kartta "docker komutu" var, birebir komut yok | repo adı/komut videodan; Docker gerekir |
| 4 | video-kurgu-DeR11OUkobq | hesap | Higgsfield (Claude entegrasyonu) | kart yok | hesap/ücretli olabilir; kurulum değil |
| 5 | prompt-hilesi-DezC2eYkpAa | KUR-sonra | Kronos (K-line tokenizer modeli) | repo URL kartta yok | GPU/ağırlık boyutu belirsiz; önce repo+lisans bul |
| 6 | motion-capture-DeaOQ2bD9Zl | KUR | Motion2MixamoRig (CLI ya da Blender 4.2+ eklentisi) | URL kartta yok | Blender kurulu mu doğrula |
| 7 | video-kurgu-DcNOMyTCXmO | KUR | squall01337/mixamo-llm-mocap + GVHMR | repo: squall01337/mixamo-llm-mocap | Blender 5.1+, CUDA, ~8GB VRAM gerekir; donanım kontrolü önce |
| 8 | openship-kurulum-deploy-DbVGcvfgUsD | KUR | OpenShip | `npm install -g openship` | `curl ... \| sh` seçeneği KULLANILMAZ (doğrulanmamış betik); npm paketi gerçek mi önce `npm view openship` |
| 9 | 3d-modeling-Devb42_CIpc | KUR | CadQuery (+ SOMA CLI) | pip paketi cadquery; SOMA kartta yarım | SOMA kaynağı videodan |
| 10 | security-audit-DeJxR3-hR5b | KUR | cloudflare security-audit skill | `npx skills add https://github.com/cloudflare/ --skill security-audit` | URL repo kökü eksik gibi; skillspector + lisans sonra video-uygula |

Önerilen sıra (ucuz→pahalı): 8 → 10 → 9 → 2(sürüm) → 3 → 6 → 7 → 5 → 1; 4 atlanır (hesap).
