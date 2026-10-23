# web-kod (DYSM2zSsbmk)

**Amaç:** Tek komutla profesyonel görünen ve çalışan bir web sitesi oluşturmak.
**Araçlar:** Claude Code (npm kurulumu), Framer Motion (animasyon kütüphanesi), UI/UX Pro Max (tasarım entegrasyonu), 21st.dev (MCP sunucusu)

**Adımlar**
1. [0:00-0:05] Claude Code'u npm üzerinden global olarak kurun. Örnek komut: `curl -fsSL https://claude.ai/install.sh` (macOS/Linux) veya `irm https://claude.ai/install.ps1` (Windows PowerShell).
2. [0:08-0:10] Projenize Framer Motion'u ekleyin. Örnek: `npm install framer-motion`.
3. [0:10-0:13] UI/UX Pro Max yeteneğini Claude Code'a entegre edin. Örnek: `claude skill add ui-ux-pro-max`.
4. [0:13-0:16] 21st.dev'i MCP sunucusu olarak bağlayın ve tek bir komutla web sitesi oluşturun. Örnek: `claude deploy --provider 21st.dev`.

**Prompt/kod/ayar:** npm install -g claude-code; npm install framer-motion; claude skill add ui-ux-pro-max; claude deploy --provider 21st.dev
**Sonuç:** Tek komutla profesyonel web sitesi oluşturulur (temiz tasarım, akıcı animasyonlar).
**Bizde (öneri, modelden):** Kurulu araçlarla (npm, Claude Code CLI, Framer Motion) benzer bir entegrasyon yapmak için: `npm install -g claude-code; npm install framer-motion; claude skill add [uygun-tasarım-skill]; claude deploy --provider [alternatif-sunucu]`.
**Daha iyi (öneri):** Önceden hazırlanmış UI/UX skill'leri ve sunucu entegrasyonlarını destekleyen bir kodlama ortamı kurmak.
