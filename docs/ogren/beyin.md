# BEYIN-1 — ikinci beyin

## Mimari
- Kasa: Obsidian `C:\Users\pc\Desktop\Obsidian` (ayrı git, push Ömer'in). 00-cekirdek (harfiyen kurallar, ~550 token) · 10-kararlar · 20-ogren · 30-video · 40-projeler · 50-dersler · 90-log · index.md. Her not: frontmatter `kaynak/satir/tarih/tur/guven/etiket` + birebir bölüm + `[[önceki · sonraki · index]]`.
- İçe alma: `python tools/beyin_al.py` (model yok; sha aynıysa atlar; kısalan kaynağın artık parçası `gecersiz: true`, silinmez). Kaynaklar: görev, gorev-gecmis, omer-kurallar, docs/ogren, .kos/kopru/ogren, docs/kurulumlar, devir, bellek, `video projeler`.
- Arama: `python tools/beyin.py ara "<soru>" --k 5` → `## kaynak:satır` + birebir satırlar. qmd FTS5 indeksini salt-okur; terimler OR + 5 harf önek (Türkçe ek), BM25. Vektör/rerank kapalı (RAM %83–84 ≥ %75). d2: 4 varyant (özgün · 4 harf kök · +TR→EN eş anlam · yalnız EN) sırayla birleşir; not başına en iyi pencere + ≤2 ek isabet satırı. Global CLAUDE.md + RTK.md de kaynak.
- d2 ölçümü (kapı değil): eski 40 soruda satır±2 14→20/40, dosya 24→23/40; kapı 2003/2004 koşulmadı → `.kos/kopru/ogren/beyin-borc.tsv`.
- Geniş katman: NotebookLM ("Ömer İkinci Beyin", `python .kos/kopru/nblm.py ask_question.py --question "…"`), sentez/özet soruları için; birebir kural/eşik kanıtı yalnız `beyin ara`.
- Çekirdek diyeti: `python tools/beyin_diyet.py <gorev.md> [--cikti Y] [--uygula]` geçmiş ★ satırlarını `.kos/kopru/gorev-gecmis/`'e ekler, görevde ilk ★ + GEÇERLİ + işaretçi kalır.
- Arşivci: `python tools/beyin_bakim.py` → çift/kırık/bayat raporu 90-log'a, ROUTER-1 sayımı 50-dersler'e (elle koşu; zamanlama SLEEP-2 ile).

## Ölçüm (d1b, 20 Eki)
| ölçüt | sonuç | hedef |
|---|---|---|
| doğruluk tohum 2001 (kör hakem) | 19/20 = %95 | ≥%92 ✓ |
| doğruluk tohum 2002 (kör hakem) | 15/20 = %75 | ≥%92 ✗ |
| girdi token, 20 soru (s2001) | B beyin ara 346 915 (9 tur) ↔ A dosya okuma 2 163 339 (41 tur) = %16 | ≤%40 ✓ |
| köprü ilk tur (ogren-1, diyet önce/sonra) | 118 253 → 114 913 (−%2.8) | — |
| NotebookLM 10 soru (s2001 ilk 10, oturum bakışı, kapı değil) | 1/10 kullanılır (#24); 9'u "Limitler 5 Saatte Bir Yenilenir" katmanı + önceki cevabın yeniden okunması | ≤10 soru ✓ |

Iska sınıfı (6): içe alma 2 (39 skill öncelik sırası, 40 cache TTL: global CLAUDE.md kaynak değil) · arama 4 (19 ozet-0b sayımı gelmedi, 24 zoetrope yalnız bir sorguda geldi, 12 yanlış ★ satırı seçildi, 29 aynı dosyada yanlış satır).
Çekirdek bulgusu: ilk turun ~108k'i sistem + araç tanımı; görev dosyası diyeti yalnız ~3.3k kazandırır. Asıl kazanç oturum içi okumada (A→B −%84).

## Kaynak inceleme (UYARLA, kod kopyalanmadı)
| kaynak | en iyi yaptığı | bizde |
|---|---|---|
| masterclass hafıza modu (selmakcby, video raporundan; repo okunmadı) | ham → wiki → index → log katmanı + arşivci ajan | klasör düzeni, 90-log, beyin_bakim |
| claude-mem (kurulu) | oturum gözlemini kendiliğinden yakalar | özet + model bağımlı (Gemini kotası durdurur) → kanıt değil |
| context-mode (kurulu) | araç çıktısını FTS5'te tutar, bağlama sokmaz | oturuma özel; kalıcı bilgi değil |
| Obsidian MCP | insan gezinmesi/düzenleme, bağlantı grafiği | dosyalar doğrudan yazılıyor; MCP gerekmedi |
| qmd (kurulu) | yerel BM25 + vektör + rerank | arama çekirdeği (yalnız BM25) |
| NotebookLM | çok kaynaklı sentez | geniş/özet katmanı |

## Kullanım
- CC: skill `beyin` (onay/beyin_1_uygula.py ile ~/.claude/skills'e) → "bilgi gerekince önce `beyin ara`, dosyayı yalnız kanıt satırı için aç".
- Desktop: cc-kopru allowlist'inde `python` (dosyaGerek, -c yasak) açık → aynı komut değişiksiz geçer.

## BEYIN-2 (20 Eki) — Obsidian merkezli
- Kasa yapısı: frontmatter `kaynak · satir · guncellenme · tur · guven (kaynak-birebir|betik-ozet|model-ozet) · etiket` + ilk parçada `aliases`; `Bağlar:` satırı = gövdede birebir geçen takma adlar (kaynak dosya kökü ≥5 harf, kaynakların >%5'inde geçen elenir; ≤5 bağ) → `[[ad--1|takma]]`; her klasörde MOC `index-<klasör>` (index.md bunlara bağlanır); günlük not şablonu `_sablon/gunluk.md` + çekirdek Daily notes/Templates ayarı (90-log, YYYY-MM-DD).
- Akışlar (`beyin_al`, model yok, sha+bağ kümesi idempotent): `60-ajanlar/ajan-*` (ajan-sira sonuç + maliyet + model dağılımı), `alt-<oturum>` (alt ajan transkriptinden görev · sonuç · ders · token; mtime önbelleği `.beyin/alt.json`), `yonlendir-kayit`; `20-ogren/kart-<aşama>` (kart.jsonl); `50-dersler/mem-<gün>` (claude-mem worker /api/observations, yoksa atlanır); `10-kararlar/sira-kararlar`. SLEEP export-obsidian çıktısı yok (d3 planı) → atlandı. Gizli desenler `[GİZLİ]`; gitleaks notlarda 0 (2 bulgu eklenti main.js'te).
- Arama: BM25 ilk k ≤5 + seçilen notların `Bağlar:` hedeflerinden soruyla ≥1 kavram eşleşen ≤3 komşu; 'ı'lı soruya katlanmamış varyant (FTS unicode61 'ı'yı katlamaz).
- Araçlar: qmd (arama çekirdeği, `qmd search … -c beyin` ✓) · Desktop obsidian MCP (eklenti claude-code-mcp kasada kurulu; uygulama kapalıydı, pencere kuralı gereği açılmadı → koşu yok) · obsidian-paket / obsidian-skills / obsidian-cli-skill (0b kataloğunda belge, CC'de kurulu değil; `obsidian` CLI PATH'te yok) · doğrudan dosya yazımı (beyin_al) asıl yol.
- Karşılaştırma: OpenViking (pypi 0.5.1, Apache 2.0 çekirdek; entegrasyonlar AGPLv3) `viking://` sanal dosya sistemi + L0 özet / L1 genel bakış / L2 tam içerik katmanı; L0/L1'i VLM + embedding modeli üretir → bizde model yok. Alınacak: klasör MOC'una kaynak başına 1 satır mekanik L0 (ilk başlık) → borç. Video 'Agent Memory' (DdD0FdkmTvh): repo adı belirsiz; "görevler arası kalıcı ajan belleği" = bizde 60-ajanlar akışı.

## d2 önerisi (BEYIN-1)
1. İçe alma: global + proje CLAUDE.md ve RTK.md kaynak olsun. 2. Arama: sorgu başına 2 varyant (önek 4/5) birleşik sıralama + başlık/★ satırına ağırlık; aynı dosyada terim yoğunluğu en yüksek 2 pencere. 3. Kapı yeniden: yeni tohumlar 2003/2004, aynı 40 soru setine 40 yeni soru eklenerek (ezber önleme). 4. Görev diyeti `--uygula` Desktop onayıyla.
