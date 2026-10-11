# TUR-6d rapor — e partisi KAÇAN? adayları (2026-10-11)

Kaynak: docs/kurulumlar/kacan-adaylar.md "Tur 6d — e partisi" (864 yeni aday, k8_aday.py üretimi). Karar dosyası: .claude/t6d/karar.tsv (157 kalem).

## Elenen gürültü (RED, karar.tsv dışında)
- Triyajda gürültü işaretli 128 (iş ilanı/genel site vb.).
- Site bölüm2 332: e-ticaret/kurumsal 80 · model/lab adı 38 · sponsor/affiliate 34 · haber/blog 32 · kişisel portföy 31 · framework dokümanı/CDN 18 · OCR kırığı 18 · diğer.
- GitHub gürültüsü 225: dosya/klasör yolu 47 · OCR parçası 29 · URL parçası 28 · CSS/TS ayar adı 22 · git dal adı 18 · model adı 13 · diğer.
- Kalan fark: OCR varyantları tek kaleme birleştirildi (ör. n8n-io/m8n,nbn,nm → n8n-io/n8n).

## Gerçek kalemler: tür × karar (157)
| tür | kur | zaten kurulu | hesap gerekli | araştır | RED |
|---|---|---|---|---|---|
| skill | 8 | 5 | 1 | 2 | 1 |
| plugin | 6 (1 kurulur + 5 hook'lu karar listesi) | 9 | 1 | 2 | 0 |
| MCP | 3 (çift satır birleşti) | 9 | 20 | 3 | 3 |
| CLI | 6 | 3 | 5 | 4 | 4 |
| kütüphane | 0 | 0 | 0 | 2 | 13 |
| site | 0 | 0 | 2 | 6 | 38 |
Ajan sayımından düzeltme: mukul975/Anthropic-Cybersecurity-Skills ve lackeyjb/playwright-skill → zaten kurulu (yukle-13 aileleri); K-Dense scientific 177 alt skill'in 101'i yukle-13'te (davila7-scientific) → yalnız 76 yeni paketlendi.

RED gerekçe sınıfları: kütüphane 13 = proje bağımlılığı (global kurulmaz) · site 38 = CC dışı ürün/IDE/sunucu uygulaması (kiro.dev, uptime-kuma, warp vb.) · MCP 3 = arşivli repo (browserbase, langsmith — resmi uzak MCP'leri yaşıyor olabilir, araştır'a çekilebilir) + OpenViking AGPL · CLI 4 = arşivli/eşleşme yok · skill 1 = eşleşme yok. Ayrıntı karar.tsv "gerekce" sütununda.

## Kurulacaklar (tur_6d_kur.py)
- Aile paketleri 9 zip (dist/yukle-14/_paket, claude.ai ile aynı zip): kdense-scientific-1/2 (76), ootto-content (53), loopy (2), diagram-design, superdesign, interfaces-better, resemble-detect, frontend-slides (1'er).
- Plugin (hook'suz): claude-hud@claude-hud. Statusline'ı kendisi değiştirmez; /claude-hud:setup ile Ömer açar.
- MCP stdio (deferred): codegraph 1.6.2 MIT · excalidraw (yctimlin mcp-excalidraw-server 2.1.2 MIT; npm "mcp-excalidraw" başka repo, al1y — kullanılmadı) · serena v1.7.0 uvx (**GPL-3.0**, SolidLSP MIT; yerel kullanım serbest, dağıtılırsa kaynak açma yükümlülüğü). Durumsuz MCP yok → 47800 proxy'ye ekleme yok.

## Karar listesi (kurulmadı, Ömer karar verir)
- Hook'lu plugin (enable EDİLMEZ): oh-my-claudecode, fast-claude-compaction (tamaratran), agentmemory (claude-mem ile çakışır), caveman (Ömer'de ponytail hook'u var), Understand-Anything.
- CLI 6 (betikte yok, bağlam maliyeti 0): `npm i -g @apify/mcpc@0.7.0 @musistudio/claude-code-router@3.1.3 repomix@1.18.1 vibe-kanban@0.1.44` + beads (gastownhall/beads, bd) + worktrunk (MIT/Apache çift, `cargo install worktrunk`). claude-code-router API anahtarlarını yönlendirir: güvenlik gözden geçirmesi önce.
- Lisans: trailofbits/skills CC-BY-SA-4.0, OpenMontage AGPL → araştır. Sentry MCP/sentry-cli FSL → hesap gerekli.
- Hesap gerekli 29: hesap-gereken.md'ye eklenecek (bu turda eklenmedi).

## Kuru kanıtı (--kuru, geçici dizin + settings/claude.json kopyası, port 47899)
```
kalemler: aile 9 · plugin 1 · MCP paylaşımlı 0 · MCP stdio 3
OK  codegraph  araç=1 · OK  excalidraw  araç=26 · OK  serena  araç=29
skill duman: OK (9 kopyalandı) · MCP duman 3/3
settings AYNI 2a5320ca891d5412 · mcpServers AYNI 2288e5246852913d · skills AYNI 0e275e17ba8d4256 · mcp_adlar AYNI · mcp_var_mi AYNI
KURU: canlı AYNI (yazım yok)
```
Not: MCP_PAY boş olduğu için 47899 proxy kuruda başlatılmadı (paylaşımlı kalem yok). codegraph'ın 1 araç vermesi şüpheli (tek giriş noktası mı, eksik mi): canlıdan sonra bakılmalı. Test: test_tur_6d_kur.py self-check OK.

## Tahmini ilk istem payı (ölçülmedi)
9 aile × (ad + ≤70 kr açıklama) ≈ 0.3k + claude-hud komut adları ≈ 0.1k + 3 MCP deferred (56 araç adı) ≈ 0.6k → **≈ 1k jeton**.

## Ömer'in koşacağı tek satır
```
python C:\Projeler\omer-skills\.kos\kopru\onay\tur_6d_kur.py
```
Geri: aynı komut `--geri` (plugin kaldırmaz; claude-hud için `claude plugin uninstall claude-hud`).
