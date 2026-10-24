---
type: rapor
status: tamam
tags: [ustalik-1, kapi]
relatedTo: [ustalik-1]
---
# USTALIK-1-KAPI

**Sonuç:** parça 1 kapısı %74 → %100 (97/97 koştu-geçti; 3 kart muaf, kapı hesabı dışı). Komut: `python -X utf8 tools/ustalik.py kart 1`.

## Kök nedenler
- **"Bulunamayan" 10 (KALDI):** kurulum eksik değildi, ad eşlemesi yanlıştı. netlify-cli→`netlify`, open-code-review→`ocr`, testsprite-cli→`testsprite`, ecc-agentshield→`agentshield`, puppeteer-mcp-server→`mcp-server-puppeteer`, ui-to-vue-converter→`ui-to-vue`; hepsi npm -g kurulu. Yeni kurulum gerekmedi (gitleaks/semgrep/agentshield kapısı çalıştırılmadı: kod indirilmedi). `ALIAS` tablosu eklendi.
- **headroom-compress, claude-mem, nano-banana-2:** eklenti `.mcp.json`'undan stdio başlatılıp gerçek `initialize + tools/list` koşuldu (`eklenti_mcp` + `mcp_tools`).
- **"Yanıt vermeyen" 16:** (a) `beyin.CMD` bozuktu: `\t` `\b` kaçışı yolu `tools\x08eyin.py` yapıyordu → `~/.local/bin/beyin.CMD` ileri eğik çizgiyle yeniden yazıldı; (b) summarize/skillspector/codeburn `--version` 30-40 sn sürüyordu, zaman aşımı 8→45 sn (yalnız `--version`; diğer bayraklar 12 sn); (c) bayrak listesi `--version, -V, version, --help, -h, help`; (d) uv tool kurulumlarında komut adı paket adından farklıydı (headroom-ai→headroom, jev-cli→jev, video-cli→video, graphifyy→graphify, mimic-client→mimic, strix-agent→strix).

## Muaf (ÖMER:)
- **skill-ui:** npm'den kaldırılmış (2023-04-28), global dizin boş, kaynak bilinmiyor.
- **open-design:** `od` masaüstü uygulamasıyla gelir; uygulama yok, daemon 127.0.0.1:7456 gerekir.
- **whisper-cli:** whisper.cpp ikilisi yok; çalışan yol `tools/asr_hat.py`.

## Sapma
- Kartlar `kartlar/arac/` + Obsidian `30-araclar/` betikle yeniden yazıldı (status: dogrulandi / muaf).
- Kapı yalnız komutun çalıştığını ölçer; MCP'lerde tools/list yanıtı, uzak (http) MCP'lerde yalnız yapılandırma kontrolü.
- Tek seferlik OSError(22) `mcp-remote.md` yazımında görüldü, yeniden koşuda tekrarlanmadı (kök neden kanıtlanamadı).
- Maliyet hedefi ($0,50) aşıldı: probe betikleri + yavaş `--version` bekleme.
