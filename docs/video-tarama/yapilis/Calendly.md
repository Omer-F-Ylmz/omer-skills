# Calendly

- tür: arac · durum: KURULU-KANITSIZ · videolar: DZZr2P_k1TY,DbsSDgAm5JX,De4rkL4MSDz,DeB6QU6N4Ec,DeWPBbShCBu,De_0D2tEa9y,De_iYRotE4D,DedbF9YDjmR,DeekQtwk30w,DelEX-8t6as,Der3v24JiU9,DezCrecDDSm,DfFWZz-gOjz
- bizde: docs/envanter/envanter.tsv; plugin sales@knowledge-work-plugins:docs\katalog\yetenek.tsv; ~/.claude/skills:docs\katalog\yetenek.tsv; kurulu-skill:~/.claude/skills/calendly

## Özellikler
- Tarih/saat seçim popup'ı içeren 30 dakikalık görüşme zamanlama butonu
- Calendly kullanıcı adıyla URL ayarı
- Popup yerine doğrudan link yedeği
- react-calendly kendi tip tanımlarını taşıyor (ayrı @types paketi gerekmeyebilir)
- Cal.com: ücretsiz, sınırsız etkinlik türü; Calendly ücretsiz planında 1 etkinlik türü

## Videoda yapılış
Video, AI asistanın ürettiği kodu VS Code'da projeye yapıştırmayı ve Calendly URL'sini ayarlamayı gösteriyor; popup engellenirse doğrudan link kullanılıyor. Ayrıca 15 aracın ücretli katman karşılıkları listesinde 'Calendly $16 → Cal.com' geçiyor.

## Bizdeki karşılık ve fark
Kurulu skill ~/.claude/skills/calendly (KURULU-KANITSIZ); envanter: docs/envanter/envanter.tsv; katalog: docs\katalog\yetenek.tsv. FARK: videoda React bileşeniyle gömülü takvim butonu var; bizdeki karşılık bir Calendly skill'i, gömme değil.

## Al
Popup yerine doğrudan link yedeği; Cal.com ile ücretsiz ve sınırsız etkinlik türü.

## At
Mobil tarayıcıda popup engeli; Calendly URL ayarlanmazsa çalışmaz; Calendly ücretsiz planı tek etkinlik türüyle sınırlı.
