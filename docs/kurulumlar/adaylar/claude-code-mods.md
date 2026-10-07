# claude-code-mods
ad: claude-code-mods
tur: teknik
video: _0NSNY7n5lE
etiket: teknik
karar: ÖĞREN (CC yerleşik plugin-authoring skill'i karşılar; mod yazımı ihtiyacı yok → kullanım kartı)
kural: Claude Code mod'u oturum içinde koşan, oturumu izleyip davranışı değiştiren JS/TS dosyasıdır (pane · band · status line · toast · hook)
zaman: 1:39
teknik: Claude Code Mods (You Should Know eklentisinin altındaki mimari)
## Ne
Claude Code oturumu içinde çalışan, olayları izleyip davranışı değiştirebilen JavaScript/TypeScript dosyaları; You Should Know eklentisi bu mimariyle yazılmış.
## Kanıt
_0NSNY7n5lE 1:39 (docs/video-tarama/2026-10-07-_0NSNY7n5lE.md): "A mod is a JavaScript TypeScript file that runs inside Claude Code session. It can watch what's happening." (karede: Getting started with Claude Code mods, Addy Osmani)
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Mod, oturum içinde koşan ve oturumu izleyebilen JS/TS dosyasıdır (1:39) | CC yerleşik `plugin-authoring` skill tanımı ("Make a mod: a live pane, band, status line, toast or hook … plugin of function hooks that hot-reloads") | doğru (yerleşik skill tanımı) | resmi doküman sayfası açılmadı | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): yok
- toplu eşleşmesi `Claude Code: /model (ele, 0.90)` yanlış eşleşme: /model ile mod mimarisi ilgisiz → ÖNCEDEN-GÖRÜLDÜ son karar sayılmadı
- var (kısmen): CC yerleşik `plugin-authoring` skill'i mod yazımını kapsar; repoda mod yok, hook'lar settings.json + hookify ile
