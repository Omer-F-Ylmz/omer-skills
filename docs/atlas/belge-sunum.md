# Oyun kitabı — belge + sunum (docx/pptx/xlsx/pdf, Artifact; ATLAS-2 K3)

Karar kaynağı: `docs/atlas/kart.jsonl` (`karar` · `kosul`); aynı karar `docs/katalog/yetenek.jsonl` satırında. Departman sırası: `departman-belge`.
Ölçüm yok (claude -p bütçesi K1/K2'de bitti) → kabul değil, iş akışı belgesi.

## 0. Ayrım (önce hangi çıktı?)
- Kullanıcı dosya istiyor (.docx/.pptx/.xlsx/.pdf) → biçim skill'i (A2). Ekranda görüp paylaşacak → claude.ai'de Artifact (C), CC'de HTML/markdown.
- Belgeyi OKUMAK (PDF/docx/xlsx → metin) → `markitdown <dosya>` (CLI kurulu); üretim skill'i açılmaz.
- Rapor/özet içeriği önce markdown taslak; biçime en son çevrilir (biçim döngüsü ucuz, içerik döngüsü pahalı).

## A. VARSAYILAN (bu sırayla)
| Adım | Araç | Not |
|---|---|---|
| A1 Tür | `document-generate` (proje dokümanı) · `agent-skills:documentation-and-adrs` (ADR) · `example-skills:doc-coauthoring` (ortak yazım) | Belge koddan türetilir; kodla çelişen iddia yok |
| A2 Biçim | `make-pdf` (md → PDF) · `example-skills:docx` · `example-skills:pptx` · `example-skills:xlsx` · `example-skills:pdf` (oku/birleştir/form) | claude.ai'de aynı dördü yerleşik Anthropic skill'i |
| A2 Sunum | `claude-mem:wowerpoint` (HTML slayt) | .pptx dosyası şartsa `example-skills:pptx` |
| A2 Diyagram | `diagram` | mmdc kurulu değil → SVG/HTML çıktı |
| A3 Dil | `humanizer` → `writing-guidelines` | Talimat metni STE: cümle ≤20 kelime, adım başına tek eylem |
| A4 Yayın | `document-release` | Sürümden sonra README/CHANGELOG eşitle |
| Okuma | `markitdown` | pandoc/libreoffice kurulu değil; dönüşümde ona dayanma |

## B. GEREKİNCE (koşul)
- `example-skills:web-artifacts-builder` — çok bileşenli claude.ai artifact (state/routing/shadcn); tek dosya HTML/JSX'te değil.
- `example-skills:theme-factory` — belge/slayt/artifact'a hazır tema giydirilecekse.
- `ecc:frontend-slides` — animasyonlu HTML slayt, wowerpoint yetmezse. `baoyu-slide-deck` — makaleden görsel deste.
- `excalidraw-diagram` — el çizimi görünüm istenirse.
- `dok-markitdown-donusum` — çok dosyalı toplu dönüşüm alt ajana verilecekse; tek dosyada CLI.
- `dok-rapor-uretici` · `dok-pdf-uretici` · `dok-docx-uretici` · `dok-pptx-sunum` · `dok-xlsx-tablo` — iş ana bağlamı şişirecek kadar büyükse (çok kaynaklı rapor); küçük işte ana oturum skill'i.
- `pln-prd-yazar` (tek PRD) · `phoenix-prd-pipeline:*` (çok aşamalı PRD hattı).
- `adobe-for-creativity:*` — Adobe bağlantısı açık ve Adobe çıktısı istenirse.
- `stop-slop` — humanizer sonrası ikinci süzgeç. `-paket` öğeleri — asıl skill yetmezse tarif kaynağı.

## C. Artifact türleri (claude.ai)
- Markdown belge: rapor/kılavuz, kopyala-yapıştır metin. Kod: tek dosya betik.
- HTML: tek sayfa, slayt, etkileşimli demo (dış kaynak yalnız cdnjs). SVG: logo/şema. Mermaid: akış/sıra diyagramı.
- React: durumlu araç/pano (Tailwind çekirdek sınıfları; localStorage yok). Çok bileşenli → web-artifacts-builder.
- Mobil kontrol: is_mobile ~980px yakınlaştırır (playwright-csp-artifact-mobil notu); 390 genişlikte ayrıca bak.

## D. KULLANMA
- `gstack-make-pdf` · `gstack-document-generate` · `gstack-document-release` · `gstack-diagram` — kısa adlı kopyaları var; ikisini birden açma.
- `claude-ads:ads-report` — reklam denetim raporu; ad eşleşmesiyle kümeye girdi.

## İş sırası
1. Ayrım (0) → 2. markdown taslak (A1) → 3. dil (A3) → 4. biçim/sunum/diyagram (A2) → 5. dosyayı aç-doğrula (docx/pptx: markitdown ile geri oku; PDF: sayfa sayısı + görsel kontrol) → 6. yayın (A4).

## Token ipucu
- Kaynak belgeyi Read ile değil `markitdown` ile metne çevir, sonra dar aralık oku (PDF/docx Read'de ham bayt ya da görsel olur).
- Biçim skill'ini içerik bitince bir kez aç; her düzeltmede yeniden üretme, markdown'u düzelt.
- Büyük xlsx'te tümünü okuma; sayfa/sütun özeti için pandas betiği, yalnız sonucu yaz.
