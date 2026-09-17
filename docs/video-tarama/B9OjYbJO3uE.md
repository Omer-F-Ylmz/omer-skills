# Bilgisayarımı Claude'a verdim (computer & browser use)
kanal: Selma Kocabıyık · tarih: 2026-05-24 · süre: 7 dk 49 sn · altyazı: tr-orig
ana iddia: Anthropic'in Computer Use API'sini resmi best-practice'lere göre (çözünürlük 1280-1568 "sweet spot", context editing/screenshot prune, göreve göre model routing: rutin Sonnet, planlama Opus) düzeltip kendi PyAutoGUI+Pillow tabanlı Python ajan döngüsü demo reposunda gösteriyor.
- PyAutoGUI (asweigart/pyautogui) → ELE · bakım durgun (gh api: son push 2024-08-20, 12.7K★), Claude Code'a kurulan araç değil, ayrı özel Python ajan döngüsü bağımlılığı
- Pillow (python-pillow/Pillow) → ELE · bakım aktif (gh api: son push bugün) ama Claude Code'a bağlanmayan ayrı Python demo bağımlılığı
- Anthropic Computer Use API / context editing header → ELE · Claude yerleşik API özelliği, aday değil
not: sweet-spot çözünürlük 1280-1568 px (küçültülmeden gönderilen görüntüde yanlış koordinat riski); context %65-85 dolunca compact/prune, 20 adımlık sınırlı görevde ekstra temizleme gerekmiyor.
