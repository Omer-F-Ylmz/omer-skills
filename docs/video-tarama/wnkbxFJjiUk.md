# Claude Code Kullanıyorsanız Bu 5 Repo'yu Mutlaka Kurun! (2026)
kanal: Burhan KOCABIYIK · süre: 5 dk · altyazı: otomatik tr
ana iddia: Claude Code kullanan herkes Anthropic'in skill/plugin reposu, Excalidraw, Paperclip, Dify ve Everything Claude Code repolarını kurmalı; kurulum repo URL'sini Claude Code'a verip "kur" demek kadar basit.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| Excalidraw MCP? (excalidraw/excalidraw-mcp?) | YENİ | ELENDİ | istemle canvas diyagram/sunum; repo kimliği videoda doğrulanamadı, 6 aydır push yok, yerleşik artifact-diagramming ile kısmen çift |
| paperclipai/paperclip | YENİ | ELENDİ | ajan orkestrasyonu (siz şef, ajanlar çalışan); video kendisi "overrated, herkes için değil" diyor; ayrı sunucu+arayüz yükü |
| affaan-m/ECC (Everything Claude Code) | YENİ | ELENDİ | skill, memory, güvenlik, research, kurallar+hooks paketi; superpowers + claude-md-management + CLAUDE.md ile çift, context yükü yüksek |
| lisans kontrolü (dış repo üzerine geliştirmeden önce) | YENİ | BİLGİ | video: Dify MIT değil, üzerine ürün geliştirmede kısıt var; global CLAUDE.md'de lisans kuralı yok |
| diğer: anthropics/skills?, frontend-design, Claude Code VS Code eklentisi | ÇİFT / ZATEN VAR | ELENDİ | skills reposunun öne çıkan frontend-design ve skill-creator'ı claude-plugins-official'dan kurulu; VS Code eklentisi yerleşik |
| diğer: langgenius/dify, GOAT (sunucunun kendi sistemi), Google Antigravity, n8n, Instantly, repo URL'si verip "bunu kur" demek | YENİ | ELENDİ | dify Claude Code aracı değil (self-host platform, lisans kısıtlı); GOAT yayınlanmamış; Antigravity IDE; n8n/Instantly açıklamada ortaklık linki; URL ile kurdurma denetimsiz kurulum |
## ölçütler (YENİ)
- Excalidraw MCP?: bakım=push 2026-03-24 (~6 ay), 5.3k★, arşiv değil, lisans alanı boş · çift=kısmi: yerleşik artifact-diagramming skill'i / Mermaid · izin=MCP sunucusu (türü doğrulanmadı) · context=MCP tool şemaları her oturum (sayı bilinmiyor) · kurulum: —
- paperclipai/paperclip: bakım=push 2026-09-15, 80.7k★, MIT, arşiv değil · çift=kısmi: superpowers subagent-driven-development / dispatching-parallel-agents · izin=ayrı sunucu+arayüz, arka planda MCP kurulumu (video) · context=Claude Code'a kalıcı yük yok, MCP eklenirse tool şeması · kurulum: —
- affaan-m/ECC: bakım=push 2026-09-15, 258.9k★, MIT, arşiv değil (repo adı everything-claude-code'dan ECC'ye taşınmış) · çift=superpowers (skill/iş akışı), claude-md-management (memory/kurallar), global CLAUDE.md · izin=hooks (video: "kurallar ve hooks") · context=yüksek: çok sayıda skill açıklaması her oturum (sayı doğrulanmadı) · kurulum: —
- lisans kontrolü: bakım=uygulanmaz · çift=örtüşme yok · izin=yok · context=CLAUDE.md'de tek satır, her oturum · kurulum: —
- diğer: bakım=dify push 2026-09-15, 155.8k★, lisans NOASSERTION; GOAT yayınlanmamış; kalanlar uygulanmaz · çift=örtüşme yok · izin=dify/n8n self-host, Antigravity ayrı IDE, URL ile kurdurma README komutlarını denetimsiz çalıştırır · context=Claude Code'a kalıcı yük yok · kurulum: —
## hedefler (BİLGİ)
- dış repo kodunu/kuralını projeye almadan ya da üzerine geliştirmeden önce lisansı oku (MIT değilse koşulları kontrol et) → CLAUDE.md (dış kaynak benimseme)
---
## ek: somut
- ayar: Claude Code'u VS Code (ya da Antigravity) içinde klasör açıp Terminal > Yeni Terminal'den ya da sol panel / Extensions üzerinden eklenti olarak çalıştırma
- komut: terminalde claude; Claude Code'a repo URL'sini verip "bunu kur" istemi
- dosya: demo çalışma klasörü "YouTube Codex"
- sayı: 5 repo her gün kullanılıyor — yalnız iddia
- sayı: Dify dışındaki repoların hepsi MIT lisanslı — yalnız iddia (gh: paperclip ve ECC MIT, anthropics/skills ve excalidraw-mcp lisans alanı boş, dify NOASSERTION)
- sayı: "tüm kaynaklar %100 ücretsiz" (açıklama, skool linki) — yalnız iddia
- sayı: açıklamadaki diğer videolar Claude Code Full Kurs 2 saat; Yapay Zeka Ajanları 3 saat; n8n & Claude Code Masterclass 8 saat — bilgi, kanıt gerekmez
