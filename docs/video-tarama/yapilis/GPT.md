# GPT

- tür: arac · durum: KURULMADI-SIRADA · videolar: 2n84xa99FRY,5LLLxHxkCnI,DWY3Mphimwg,DY_SoPGKv2A,DZ-DVAxMkn9,DZI1ok5Ss4b,Dar76wns2Iv,Db6urS4sQZR,Db_GVNhOnQF,Dc5mDOmgB0w,DcIccFMjPTs,DcJQd0TRewZ,DcQwBpXDSXs,Dd0nXg2Mabb,Dd56RIYHZ5_,DdHSX-Dib0O,DdKfJBHSlWN,DdVWXArCa_T,DdbljkbH5b2,DdeLN4ujZGN,DdlyT_dIiT7,DdnzgroER7E,DdqG1fjiiQm,Ddqym0VAqzU,DdrHoHXMhQU,De68AiWSiMp,De7ueOMSVHF,De82MvBGH8X,DeChE4DChaA,DeHdXeWsgph,DeNA3LtjDzc,DePTgfoGbn6,DePWmOHCPX1,DeZJ
- bizde: yok

## Özellikler
- Video, GPT modellerinin talimat takibini (instruction following) güçlü buluyor ve detaylı görevlerde kaliteli çıktı verdiğini söylüyor
- Aynı görev iki kez test edildi: 56 satırlık ağır prompt ve 5 satırlık kısa brif; Claude Opus 5.5 ve GPT-6 Astra ile altı test yapılmış
- Kısa brif neredeyse her testte daha iyi sonuç vermiş
- Ağır promptla verilen faturada model 7 gizli sorunun hiçbirini bildirmemiş; kısa brifle iki denemede de yedisini bulmuş

## Videoda yapılış
Codebase'in ekran görüntüleri alınıp Claude, Codex, GPT veya Gemini'ye sorulmuş. Subagent'lar Opus ile çalıştırılıp Fable limitinden düşmemesi planlanmış. Skill'ler uzun promptlar yerine kısa brifle yeniden yazılmış. Alıntı bozuk olduğu için tam adımlar ve komutlar çıkarılamıyor.

## Bizdeki karşılık ve fark
Kayıtlarda GPT için karşılık yok (BIZDE: yok) ve durum KURULMADI-SIRADA. Ayrıca bizim skill'ler uzun promptla yazılmış görünüyor; videonun önerdiği kısa brif yaklaşımı henüz denenmemiş.

## Al
Görevleri kısa ve net brifle vermek; uzun, şişmiş promptların yerine kısa talimat kullanmak; subagent'ları daha ucuz modelle çalıştırıp ana modeli rezerve etmek.

## At
Test küçük ve tek senaryolu (altı test); sonuçlar tek bir video anlatımına dayanıyor. 'GPT-6 Astra' gibi model adları doğrulanmadan kullanılmamalı.
