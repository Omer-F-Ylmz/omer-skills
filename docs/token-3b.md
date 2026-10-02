# TOKEN-3b — proje profilleri: skill-arac + mod-blender

## K1 mekanizma
- Proje `.claude/settings.json` içindeki skillOverrides okunuyor ve global ile birleşiyor.
- name-only skill listede yalnız adıyla görünür. Kullanıcı adını söyleyince Skill aracıyla çağrılır.
- off ya da kapalı plugin'de SKILL.md hâlâ Read ile açılır, references de okunur.
- enabledPlugins:false proje düzeyinde çalışıyor. Plugin skill anahtarı skillOverrides'ta 5 biçimde etkisiz kaldı, bu yüzden KARAR 2 uygulandı.
- Proje settings yalnız cwd'den okunur, üst klasörden miras alınmaz. blender-kum'da ölçüm: kökte 284 skill / 34 plugin / 60.0k, alt klasörde 393 / 51 / 92.4k, alt klasörde `--settings <kök settings>` ile 284 / 34 / 59.9k.

## Uygulanan profiller (`profiller/proje-profilleri.json`)
- omer-skills → skill-arac: 82 name-only, 7 off, 13 kapalı plugin.
- Kendi oyun modlarim → mod-blender: 82 name-only, 7 off, 17 kapalı plugin.
- blender-kum → mod-blender: aynı sayılar. Bu klasörde settings.json daha önce yoktu (`.yokT3b` işareti).
- mod-blender ölçüldü, RED (aşağıda Blender kapısı) ve iki klasörde `--geri` ile geri alındı. Profil tanımı duruyor, eşlemeden çıkarıldı. Kendi oyun modlarim `.bakT3b` ile bayt-eşit döndü. blender-kum'da settings.json önceden olmadığı için yine yok; profilli dosya `.geriT3b` olarak kenara alındı.

## Kapatılan plugin'ler
- Üç klasörde kapalı: design-mastery, discernment-nudge, dotnet-aspnetcore, dotnet-nuget, dotnet-test, phoenix-* (6), supabase, taste-skill.
- Yalnız mod-blender'da kapalı: agent-skills, claude-api, plugin-dev, typesafe.
- mod-blender geri alındığı için bu kapatmalar şu an yalnız omer-skills'te (skill-arac) uygulanıyor.
- Koruma kuralı (`tools/profil.py:9`): G/H hook'u sağlayan, 14 günde MCP'si ya da ajanı kullanılan plugin açık kalır. Açık kalanlar: G everything-claude-code, headroom, hookify, security-guidance · H claude-mem, claude-mem-cowork · E superpowers, ponytail, explanatory/learning-output-style · D impeccable, ralph-wiggum.

## Ölçülen taban (ilk ctx, "ok" istemi, `olcum/token-3b-ok.json`)
- skill-arac 73.5k · mod-blender (Kendi oyun modlarim) 65.2k · mod-blender (blender-kum) 61.7k. Ortalama 66.8k.
- Profilsiz 3a tabanı 101.0k (`docs/token-3a.md:35`).

## Tetik kapısı (`olcum/token-3b-tetik.json`)
- 16 istem: recall 0.857, precision 0.889. İkisi de 3a'nın aynı alt kümesine eşit. Negatif 2/2.

## Blender kapısı
- Koşu: fincan B (rehber), tam ve T3b (mod-blender) birer kez (n=1).
- İlk sonuçta T3b teslim False çıktı. Teşhis ölçüm hatasıydı: T3b GLB'yi `blender-kum\web\` altına yazmıştı, `kos.py` bu klasörü taramıyordu. `kos.py` tarama köklerine `web\` eklendi (repo dışı, yedek `kos.py.bakT3b2`). Yeniden hesapta iki koşu da teslim etti.
- Kör puan (2 okuyucu, eşleme puandan sonra açıldı): tam 3.9 → T3b 3.3, ışık 4 → 3. Düşüş %15.4.
- references okuması: tam 7 md + 2 py, T3b 2 md + 15 kısmi py. Işık ve malzeme rehber md'leri T3b'de açılmadı.
- Koşu başı maliyet: ağırlıklı token 3.168M → 2.673M (−%15.6), $ 9.59 → 9.20 (−%4.0), istek 83 → 69.
- Madde 21: düşüş %15.4 (kör puan; teslim düşüşü %0), bant %15–20, tasarruf <%50 → RED. SOR için bile ≥%25 tasarruf gerekirdi. mod-blender geri alındı.
- Ayrıştırma adayı: TOKEN-1'de de 3b'de de profil koşusunda rehber md okuması ve ışık puanı düştü. Önce blender-uretim'e ışık/malzeme rehberi için zorunlu okuma adımı eklenir (Blender açık skill işi), sonra mod-blender n≥2 ile yeniden ölçülür.
- Ders: oturum başı taban −%35 düşse de uzun Blender koşusunda kazanç ağırlıklı −%15.6, $ olarak −%4 kaldı. İstek sayısı 83'ten 69'a indi ama istek başı ağırlıklı maliyet +%1.5 arttı. Uzun koşuda maliyeti başlangıç ön eki değil biriken bağlam belirliyor. Kaldıraç TOKEN-4 ve L6 görsel bütçesi. 3c'de profil kapısı hem kısa hem uzun koşuyla ölçülür.

## Tasarruf
- Oturum başı: ilk ctx 101.0k'dan ortalama 66.8k'ya indi (−34.2k, −%34). 3a tabanı farklı bir global ayarla ölçüldü (aşağıdaki notlara bakın). Aynı koşulda ölçülen tek çift blender-kum: 92.4k → 60.0k (−32.4k, −%35).
- Tur başı: bu ön ek her turda önbellekten yeniden okunur, yani tur başına yaklaşık 32–34k token daha az okuma. Profilli "ok" çağrısının maliyeti $0.38–0.51.

## Geri alma
- `python tools/profil.py --geri <proje>`: settings dosyasını `.bakT3b` yedeğinden bayt-eşit geri yükler.

## Desktop zip
- `dist/token-3b/` altında 12 router zip var. claude.ai'ye Replace ile yüklenmeyi bekliyorlar (Ömer).
- `profil.py --kontrol` temiz çıktı veriyor, yani senkron CC kopyası henüz ezilmedi.

## Açık notlar
- "ok" isteminde skill-arac ve Kendi oyun modlarim koşuları tur tavanına dayandı (`error_max_turns`) → TOKEN-6.
- Global `~/.claude/settings.json` 22:25'te değişti: `env.ANTHROPIC_BASE_URL`, `env.ENABLE_TOOL_SEARCH` ve headroom SessionStart sarmalayıcısı eklendi. Bu yüzden mühürde settings FARK veriyor. Değişikliği hangi sürecin yazdığı kanıtlanmadı. TOKEN-3b bu dosyaya yazmadı ve değişiklik geri alınmadı.
- `kos.py` (repo dışı) koşuyu alt klasörde başlattığı için proje settings okunmuyordu. `KOS_PROJE_AYAR` env'i verildiğinde artık `--settings` ekliyor. Eski hâli `kos.py.bakT3b` yedeğinde.
