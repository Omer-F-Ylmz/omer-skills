# zsh

- tür: arac · durum: KURULMADI-SIRADA · videolar: DXezZ_KjHTm,DaLGdlHuOKh,DbUg-kOFC-C,DcbxXZnFYRh,Ddq_d1bDV_Z,DeHET6Djdww,DebzkIqE9g7,DejcAcwz89b,Dertf_QNKyu,Det4Eo5RgSk,DetAb-6FN_P,DfD4q2sDyNN
- bizde: yok

## Özellikler
- Claude Code'un native kurulumu: ~/.local/bin/claude konumuna kurulur (Version 2.1.89 gösterilmiş)
- PATH uyarısı: ~/.local/bin PATH'te değilse kurulum notu çıkıyor
- Skill kurulumu: npm install -g re-walkthrough-pro, ardından re-walkthrough-pro install; ~/.claude/skills/re-walkthrough-pro/ altına kurulur

## Videoda yapılış
Kurulum: curl -fsSL https://claude.ai/install.sh | bash. PATH için: echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc (metinde 'SHOME' olarak OCR'lı; $HOME kabul edildi). Güncelleme: npm view re-walkthrough-pro version; npx re-walkthrough-pro@latest update.

## Bizdeki karşılık ve fark
BIZDE: yok. Durum: KURULMADI-SIRADA.

## Al
PATH'i ~/.zshrc'ye kalıcı ekleyip source ile hemen yükleme

## At
-
