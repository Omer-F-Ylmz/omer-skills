# TUR-5b-1 raporu
Sınıf (185): KUR 4 satır (=1 plugin) · ZATEN 9 · HESAP 27 · AYRI-UYGULAMA 68 · RED 77 (gürültü 56, kapsam 17, bulunamadı 2, lisans 2).
Kurulan: expo@expo-plugins · plugin · pin d4f484024fec15196bfd3c272e953e3f983972cf (v1.13.9, MIT) · 24 skill · ~/.claude/plugins/cache/expo-plugins/expo/1.13.9/skills (marketplace ~/.claude/plugins/marketplaces/expo-plugins). `claude plugin list` ✔ enabled; çakışma 0.
Kurulmayan: Mobbin (resmi skill+MCP var, Pro plan/giriş ister → HESAP), Lovable (resmi skill yok → HESAP), Higgsfield/prova/Anima vb. HESAP; motion.dev (yalnız kütüphane; repo skill'leri bakım içi); oh-my-claudecode/learn-claude-code/gsd (harness, mevcutla çakışır); multica (lisans belirsiz); expo deprecated+experiments plugin'leri.
Yeni skill klasörü: yok (~/.claude/skills değişmedi). Yeni plugin: expo (24 skill: expo-router, expo-ui, expo-upgrade, expo-animation, eas-* …).
Paketleme önerisi: expo → yeni küçük paket "expo-mobil" ya da android-paket'in yanına "mobil-expo"; mevcut animate-expo ile birlikte animasyon-scroll'a değil mobil gruba.
Çıktılar: docs/kurulumlar/tur5b-1-sonuc.tsv, kurulum-turu-5b-1.md, tools/kurulum-turu-5b-1.sh, .kos/kurulum-5b-1/{geri-al.sh,kurtarma.json}.
Sapma: install betiği tur-4'ten farklı olarak marketplace'in tüm plugin'leri yerine yalnız listelenen plugin'i kurar (deprecated kopyaları engellemek için). Bütçe: ~14 tur.
