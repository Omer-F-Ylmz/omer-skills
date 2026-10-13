# DeYvLuYsdHv · shorzy.md · reel · https://www.instagram.com/reel/DeYvLuYsdHv/

## Özet
REA ("Reverse Engineer Anything") tanıtılıyor: 4 günde ~106k yıldız, `npx rea-agents@latest setup` ile Claude Code/Codex/Cursor/Gemini CLI'ya bağlanıyor.
Yerel ikililer için Ghidra/Hopper/IDA gerekiyor. Yalnız sahibi olunan ya da izinli yazılımda kullanılmalı, öncesinde 3 kontrol öneriliyor.

## Kalemler
| ad | tür | link | karar | ölçütler (bakım · çift · izin · context) | gerekçe |
|---|---|---|---|---|---|
| REA (rea-agents) | CLI/skill | https://github.com/morluto/rea | ÖĞREN | ★168331 push:2026-10-13 arşiv:h · önceki-karar:igkur/karar.tsv:REF · dosya yazma, shell · ~2k | Önceki REF kararıyla tutarlı: tersine mühendislik bizim kullanım alanımızda yok. Ders: Electron/JS uygulamalarında motor gerekmiyor, yerel exe için Ghidra şart |
| Ghidra | CLI | https://github.com/NationalSecurityAgency/ghidra | ÖĞREN | ★85450 push:2026-10-09 arşiv:h · yok · dosya yazma, shell · - | REA'nın yerel ikili analiz motoru, tek başına bizim için anlamsız. Ders: Hopper ve IDA ücretli, Ghidra ise açık kaynak alternatif |
| tersine mühendislik öncesi 3 kontrol | teknik | - | ÖĞREN | - · yok · - · - | Ders: ajanı bir uygulamaya yöneltmeden önce izin, EULA ve motor kontrolü yapılmalı; ticari lisansların çoğu tersine mühendisliği yasaklıyor |
