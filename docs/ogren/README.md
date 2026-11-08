---
type: index
status: active
tags: [ogren, karar-agaci, kombo]
relatedTo: [kombo-katalog, departman-diger, is-akisi]
---
# ÖĞREN dizini, kategori → karar ağacı dosyası (HIC-122, 28 Eki)

Kaynak: `.kos/kopru/gorev/ogren-ortak.md` (4 grup kararı, 20 Eki 11:27). ÖĞREN-5/7/8/9/10/11/12/13/14 ayrı oturum açmadı; kategorileri grup lideri dosyasında kapandı. Kartlar: `docs/atlas/kart.jsonl` (kategori_son alanı), kombolar: `docs/atlas/kombo.jsonl`.

| Kategori (görev) | Grup / karar ağacı dosyası | Kapanış kanıtı |
|---|---|---|
| frontend-tasarım · 3d/görsel (ogren-5) · oyun-mod (ogren-13) | G1 `frontend.md` | SIRA "ÖĞREN-2 BİTTİ" t11 %99 · t12 %99 |
| ajan-orkestrasyon · araştırma (ogren-11) · bilim/diğer (ogren-14) | G2 `ajan-orkestrasyon.md` | SIRA "ÖĞREN-3 BİTTİ" t23 %92.0 · t24 %95.0 |
| video-medya · belge (ogren-8) · pazarlama (ogren-12) | G3 `g3.md` | SIRA "ÖĞREN-4 d3 KAPI GEÇTİ" t41 %95 · t42 %99 |
| test-qa · güvenlik (ogren-7) · backend-dotnet (ogren-9) · veri-db (ogren-10) | G4 `test-qa.md` | SIRA "ÖĞREN-6 BİTTİ" t67 %95/96 · t68 %94/93 (borç `ogren-6-borc.tsv`) |
| token | `token.md` | ÖĞREN-1 d3 |
| yönlendirme | `yonlendir.md` | ROUTER-1 |
| ikinci beyin | `beyin.md`, `beyin-desktop.md` | BEYIN-1/2 |

## İş türü → hangi kategori, hangi sırayla (kategoriler arası kombolar)
Tam liste ve ölçüm koşulu: `kombo-katalog.md` § kategoriler-arasi. Hepsi `aday`; kabul için tek başına en iyi araca karşı kalite · token · süre · kullanışlılık dördünde üstünlük gerekir.

- **Değişiklik: bul → güvenlik → test** (x-kod-guvenlik-test): graphify query → semgrep → security-reviewer → writing-mstest-tests → run-tests.
- **Site yayın öncesi kapı** (x-tasarim-erisilebilirlik-sizinti): fe-referans-diff → fe-a11y-perf-kapisi → gitleaks.
- **Videodaki arayüzden sayfa** (x-video-site): /watch → DESIGN.md taslağı → fe-referans-diff → frontend-visual-qa.
- **Doküman araştırması → karar** (x-arastirma-ajan): context7 CLI → ordu.py sinif → okuyucu alt ajan → ana oturumda derleme.
- **Büyük log → kök neden** (x-token-ajan-log): jev log|triage → okuyucu alt ajan → headroom_retrieve → özet satırı.

## Bağlı müdür skill'leri
`docs/ogren` yolunu anan skill'ler: departman-belge, departman-diger, departman-surec-ajan-arac, departman-verimlilik, is-akisi, video-uygula.

## Bilinen eksikler
- Desktop (claude.ai) kombin denemeleri ve ÖĞREN-6 borcu açık.
- Kombolar ölçülmedi (`durum: aday`); bu README karar ağaçlarını dizinler, yeni ölçüm yapmaz.
