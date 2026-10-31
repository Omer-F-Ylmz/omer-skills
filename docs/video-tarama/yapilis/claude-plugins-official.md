# claude-plugins-official

- tür: arac · durum: KURULU-KANITSIZ · videolar: DYY6WpNDP7k,Dcl0nk9ibZE,DdO1UioAHAS,DdmQWJzqP8H,DeEiGKKIKqB,DeEzggoDMYU,DeUbXXoo2mi,DeddnBCCSv4,DeloFdYmRuI,DenGFZkDj0h,DepR08lCqU8,Dex8vyLHNeh
- bizde: ~/.claude/plugins/cache; claude-code-setup@claude-plugins-official:docs\katalog\yetenek.tsv; kaynak-kutuphane/envanter:docs/envanter/envanter.tsv; baglayici:.kos\kopru\kaynak-dizin\dizin.tsv; plugin-pazar:~\.claude\plugins\marketplaces/claude-plugins-official

## Özellikler
- Claude Code'a Telegram ve Discord kanalları eklenerek telefondan görev verilebilir (videoda: hata düzeltme, refaktör, dağıtım)
- Yalnızca izin listesindeki (allowlist) kullanıcı ID'leri bota mesaj atabilir
- Telefondan tam dosya sistemi, git ve MCP erişimi sağlandığı belirtiliyor
- macOS'ta iMessage kanalı da geçiyor (sıfır yapılandırma olarak anılıyor)

## Videoda yapılış
1) Telegram'da @BotFather'a /newbot yazılır. 2) /plugin install telegram@claude-plugins-official. 3) /telegram:configure YOUR_BOT_TOKEN. 4) claude --channels plugin:telegram ile başlatılır. 5) Bota DM atılıp /telegram:access pair CODE_FROM_BOT ile hesap eşleştirilir. Discord için 'telegram' yerine 'discord' yazılır.

## Bizdeki karşılık ve fark
Kurulu görünen kayıtlar: ~/.claude/plugins/cache, claude-code-setup@claude-plugins-official (yetenek.tsv), marketplace dizini ~/.claude/plugins/marketplaces/claude-plugins-official. Telegram/Discord kanal eklentisi BIZDE alanında listelenmiyor; fark bu.

## Al
Kanal eklentisinin izin listesi (allowlist) ile sınırlanması; kurulumun kısa adımlarla yapılması

## At
Telefondan tam dosya sistemi, git ve MCP erişimi geniş bir yetki yüzeyi oluşturur; bot token'ının saklanması ve eşleştirme kodunun güvenliği gerekir
