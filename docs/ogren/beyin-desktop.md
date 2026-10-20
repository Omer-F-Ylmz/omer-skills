# beyin — Desktop / claude.ai kullanım protokolü (BEYIN-2)

Kasa tek kaynak: Obsidian `C:\Users\pc\Desktop\Obsidian`. Desktop kasayı iki yoldan okur, tek yoldan yazar.

## Sorma (okuma)
1. Önce arama, köprüden: cc-kopru komut aracıyla `python tools/beyin.py ara "<soru>" --k 5` (cwd `C:\Projeler\omer-skills`; allowlist'te `python` dosyaGerek açık, `-c` yasak).
   Çıktı `## <kaynak>:<satır>` + birebir satırlar + en fazla 3 `Bağlar:` komşusu. Özet yok; cevap bu satırlardan kurulur.
2. Kanıt gerekirse yalnız o satır: obsidian MCP `view` ile notu ya da köprüden Read `offset=<satır>-2, limit≈10`. Tüm dosyayı açma.
3. Sorgu kelimesi: görev adı (BEYIN-2, ÖĞREN-0b), araç adı, eşik/kural kelimesi. Boşsa eşanlamlıyla bir kez daha.
4. Gezinme (insan gibi): `index.md` → `index-<klasör>` MOC → not → `Bağlar:` satırı. Bu yol arama değil, bağ kontrolü içindir.
5. Geniş sentez sorusu: NotebookLM katmanı (kanıt sayılmaz; birebir eşik/kural yalnız `beyin ara`).

## Yazma (karar ve ★ satırları)
- Günlük not `90-log/<YYYY-MM-DD>.md` (şablon `_sablon/gunluk.md`): obsidian MCP `insert` ile `## Kararlar (★)` başlığının altına
  `- HH:MM ★ <karar> — kaynak: <görev/SIRA satırı>` yaz. Yoksa `create` ile şablon başlıklarını koy.
- Kalıcı karar ayrıca görev dosyasına/SIRA'ya yazılır (asıl kaynak orası); kasa notu `beyin_al` ile yeniden üretilir.
  10-kararlar/20-ogren/30-video/60-ajanlar notlarını elle düzenleme: sonraki `beyin_al` üzerine yazar.
- Elle not: `40-projeler/` ya da `50-dersler/` altına frontmatter'lı (`tur · etiket · kaynak · guncellenme · guven: elle`) yeni not.
- Silme yok: `_arsiv/` klasörüne taşı. Gizli değer/anahtar kasaya yazılmaz.

## Tazeleme
- `python tools/beyin_al.py` (köprüden; değişmeyen kaynak atlanır, ~100 sn ilk koşu, qmd güncellenir).
- Bağ/çift/bayat denetimi: `python tools/beyin_bakim.py` → 90-log.

## Ölçüm (20 Eki, BEYIN-2 d1)
- `beyin ara` 1 sn; 1943 not, 545'inde `Bağlar:`; 315 takma ad (kaynak dosya kökü, kaynakların >%5'inde geçen elenir).
- Kapı sonucu: `.kos/kopru/rapor/beyin-2-d1.md`.
