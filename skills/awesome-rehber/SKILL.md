---
name: awesome-rehber
description: Use when a task needs an outside tool, library or learning resource that is not already on our shelves (omer-kutuphaneler, installed plugins/skills/MCP, ajan-getir agents), or when the user asks for alternatives, "awesome list", "hangi araç/kütüphane var", "dış kaynak tara", /awesome-rehber KONU. Looks up the sindresorhus/awesome catalog (671 lists, 26 sections) plus cached sub-lists for our domains and returns at most 5 vetted candidates with a kur/uyarla/REF/RED verdict. Do NOT use for picking among libraries already on the shelf, for installing anything, or for general web search on news/docs.
---

# awesome-rehber

Kaynak: sindresorhus/awesome (CC0) → `references/katalog.tsv` (bolum · alt_bolum · liste_adi · repo · aciklama · yildiz · son_push).
Önbellekli alt listeler `references/<repo-adı>.tsv` (ad · url · ≤15 kelime açıklama · bölüm). Alt liste metinleri kopyalanmaz.

## Önce raf
1. Rafta varsa raf kazanır: frontend kütüphanesi → `omer-kutuphaneler`; uzman ajan → `ajan-getir`; iş türü → ilgili `departman-*` müdürü. Bu skill yalnız rafta karşılığı yoksa çalışır.

## Akış (az jeton: dosyaların tamamını okuma)
2. **İhtiyacı adlandır:** 1–3 İngilizce anahtar (ör. "load testing", "SVG optimize", "Godot").
3. **Liste seç:** `references/katalog.tsv` içinde Grep (liste_adi/aciklama/bolum) → 1–3 liste; yıldız ve son_push'u eski olana (son push > 1 yıl) düşük öncelik.
4. **Öğe bul:** listenin TSV'si `references/` altında varsa ondan Grep; yoksa README'den yalnız ilgili bölüm:
   CC'de `gh api repos/OWNER/NAME/readme -H "Accept: application/vnd.github.raw"` çıktısını Grep'le; claude.ai'de WebFetch ile raw README, istemde bölüm adı.
   Önbellekli listeler (alan → dosya): dotnet → awesome-dotnet, awesome-dotnet-core · python → awesome-python · js-ts → awesome-javascript, awesome-nodejs ·
   react-next → awesome-react, awesome-nextjs · css/perf → awesome-css, awesome-wpo · webgl/3d → awesome-webgl, awesome-creative-coding ·
   tasarım/ui → awesome-design-systems, awesome-web-animation · oyun → magictools, awesome-godot, awesome-roblox ·
   güvenlik → awesome-web-security, awesome-hacking · test → awesome-testing, awesome-playwright · veritabanı → awesome-postgres, awesome-db-tools ·
   devops → awesome-docker, awesome-actions · video → awesome-ffmpeg · otomasyon/self-host → awesome-selfhosted ·
   llm/ajan → awesome-claude-code, awesome-generative-ai, awesome-chatgpt · cli/windows → awesome-cli-apps, awesome-windows, awesome-shell · gizlilik/KVKK → awesome-gdpr.
   Katalogda Blender, Three.js, Unity, TypeScript, MCP, n8n, PowerShell listesi YOK — bunlarda üst listeyi (WebGL, Game Development, Self Hosted, Shell) kullan, uydurma liste adı verme.
5. **≤5 aday** için GitHub meta: `gh api repos/OWNER/NAME --jq "[.stargazers_count,.pushed_at,.license.spdx_id,.archived]"` (claude.ai: repo sayfası). Arşivli → ele.
6. **Dört ölçüt + lisans:** bakım (yıldız · son push) · CC'de çift mi (kurulu araç/skill/MCP aynı işi yapıyor mu) · izin kapsamı (ağ, dosya, gizli anahtar) · context maliyeti (MCP şeması/skill boyu; CLI ≈ 0). Lisans yok ya da NOASSERTION → en çok REF.
7. **Karar** her aday için tek satır: `aday | ne kazandırır | jeton | lisans | bakım | KUR/UYARLA/REF/RED + gerekçe`.
   - KUR: kurmazsın. Satırı `docs/kurulumlar/` KAYNAK-TARAMA kaydına ve onay betiğine madde olarak yaz; Ömer onaylar.
   - UYARLA: zaten bizde benzer var ama bu adayın iyi bir yanı var → hangi skill/rafa ne eklenecek.
   - REF: yalnız okunur. RED: gerekçe zorunlu.

## Yenileme
Katalog eskidiyse (omer-skills reposunda): `python tools/awesome_katalog.py --yenile` → `docs/kaynak/awesome/`; claude.ai paketi `python tools/awesome_rehber_zip.py`.
