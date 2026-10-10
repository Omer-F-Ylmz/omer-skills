---
name: markitdown
description: "PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, EPUB, ZIP ve görselleri LLM'e uygun Markdown'a çevirir (microsoft/markitdown, MIT). Belgeyi okumadan önce metne dökmek, tabloyu korumak ya da token'ı azaltmak gerektiğinde kullan."
---

# markitdown — belgeyi Markdown'a çevir, sonra oku

Neden: ham PDF/DOCX/PPTX okumak yerine Markdown'a çevirmek başlık, liste ve tabloları korur, metin dışı gürültüyü atar.
Büyük belgede önce çevir, sonra yalnız gereken bölümü oku (grep/aralık) — tamamını bağlama alma.

## Ortama göre

| Ortam | Komut |
|---|---|
| claude.ai sandbox | `pip install 'markitdown[pdf,docx,pptx,xlsx]' --break-system-packages -q` → `markitdown girdi.pdf -o cikti.md` |
| Claude Code (Ömer'in makinesi) | CLI kurulu (`~/.local/bin/markitdown`, uv tool 0.1.8): `markitdown girdi.docx -o cikti.md`; MCP `markitdown` → `convert_to_markdown(uri)` (`file:///C:/...` ya da `https://...`) |
| Desktop sohbeti | markitdown köprü allowlist'inde yok → cc-kopru `ajan` ile Claude Code'a çevirt, `.md`'yi filesystem ile oku |

Python API (sandbox/CC):

```python
from markitdown import MarkItDown
md = MarkItDown().convert("girdi.xlsx").text_content
```

## Kurallar

- Çıktıyı dosyaya yaz (`-o`), sohbete basma; sonra `grep -n`/aralıkla gereken kısmı aç.
- Taranmış (görüntü) PDF'te metin boş gelir → OCR gerekir (pdf/pdf-reading skill'i); markitdown OCR yapmaz.
- Excel/CSV girdide tablo Markdown tabloya çevrilir; PDF tablosu için pdfplumber (pdf skill'i) daha isabetli.
- `markitdown-mcp` alfa sürüm (0.0.1a7): MCP hata verirse CLI'ya dön.
- Oturum/çerez gerektiren sayfalar URL'den çevrilmez.
