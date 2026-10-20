---
name: beyin
description: "İkinci beyin: geçmiş karar, eşik, yasak, komut, ders ya da proje durumu gerekince dosya okumadan önce `beyin ara` ile birebir parça + kaynak satırı al."
---

# beyin — önce sor, sonra (gerekirse) aç

Kasa: Obsidian `C:\Users\pc\Desktop\Obsidian` (00-cekirdek · 10-kararlar · 20-ogren · 30-video · 40-projeler · 50-dersler · 90-log · index.md). Kaynak dosyaların bölüm bölüm birebir kopyası; her not frontmatter'ında `kaynak` + `satir`.

1. Bilgi gerekince: `python tools/beyin.py ara "<soru>" --k 5` (CLI kuruluysa `beyin ara`). Çıktı: `## <kaynak>:<satır>` + birebir satırlar; özet yok.
2. Sorgu anahtar kelimeyle: görev adı, araç adı, eşik/kural kelimesi ("ÖĞREN-0b kapı", "headroom PID"). Boşsa eşanlamlıyla bir kez daha dene.
3. Kaynak dosyayı yalnız kanıt satırı için aç: Read `offset=<satır>-2, limit≈10`. Tüm dosyayı okuma.
4. Çelişen iki parça: tarihi yeni olan (★ satırında saat/gün) geçerli; eskisini cevapta "geçersiz" diye an.
5. Geniş/özet soru ("X konusunda neler yaptık?", birden çok kaynağın sentezi): NotebookLM katmanı `python .kos/kopru/nblm.py ask_question.py --question "<soru>"` (defter "Ömer İkinci Beyin", günde ~50 soru, yanıt özettir). Birebir kural/eşik/kapı için yalnız `beyin ara` kanıt sayılır.
6. Kasa bayatsa (kaynak sonradan değişti): `python tools/beyin_al.py` (değişmeyen kaynak atlanır), denetim: `python tools/beyin_bakim.py` → 90-log.
