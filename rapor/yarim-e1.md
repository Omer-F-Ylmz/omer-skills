# YARIM-E1 raporu (24.10 16:40)

- token-rea d20: DEVAM. Mod uygulanmış (CLAUDE_MEM_MODE=code--anahtar, 21.10 19:23; 2149 işaretli omer-skills kaydı, işaret `subtitle` alanında). Kapı `.kos/kopru/token-rea/mem_anahtar_isaretli.py` ile ölçüldü (tohum 24101, n=40, mem2.ara top-5): anahtar 0.961 ≥0.93 ✓, süre 0.05–0.08 sn ✓; paraphrase TR→EN 0.35 (d19: 0.025), EN→TR 0.325 (<0.5 ✗). Aynı tohumda yeniden koşu 0.225/0.425: LLM-soru üretimi gürültülü, n=40 yetersiz. subtitle ağırlığı 6/10 denemesi sonuçsuz (soru havuzu düştü, n=0). Mod KAPATILMADI, mem2 AGIRLIK değişmedi.
- atlas-2-d1d: ZATEN BİTMİŞ (d576a614, zip_denetle TEMİZ 4 zip). 4 zip dist/claude-ai/yukle-24eki/ altına kopyalandı (+LISTE.md).
- ters-1: KISMEN. `tersine.zip` yukle-24eki'de (departman bağı + SIRA satırı zaten vardı). Kapı hâlâ geçmedi (0.534/0.527 <0.92, ters-2 d10 "kötü değil" geçti); parcacik-three 404 + Haiku tavanı yüzünden ATLANDI. Zip "kapı geçti" iddiası olmadan teslim.
- skill-yukle-1b: ZATEN BİTMİŞ. 625 zip dist/claude-ai/yukle-23eki/grup-01..17 (YUKLE.md); klasör adı 24eki'ye taşınmadı. Karantina 17 + kisisel-24 yüklenmeyecek; seo-cockpit paketsiz (2c işi).
- rea-agir-1/2: BİTTİ (teslim). `reverse-engineer-anything-agir.zip` (12 dosya) yeniden üretildi: heavy-targets.md + scripts/{rea_parcali,rea_parcali_kapi,rea_oto}.py, yerel yollar çıkarıldı (NODE_EXE ortam değişkeni, `python scripts/…`). Açık kalan (e2): react.dev OOM ölçümü, excalidraw %100, MCP içi otomatik düşüş.
- ÖMER: dist/claude-ai/yukle-24eki/ (6 zip) + yukle-23eki gruplarını Desktop claude.ai'ye yüklesin; yükleme kanıtı yok.
- Bütçe: ~$2.4 (hedef $0.50 aşıldı: 10 dk'lık okuyucu alt ajan keşfi $1.1, 3 ölçüm koşusu).
- Commit: YARIM-E1 (repo içi dosyalar; zipler dist/ gitignore'lu). Test: yeni kod yok (ölçüm betiği), paketle/zip_denetle TEMİZ: 6 zip.
