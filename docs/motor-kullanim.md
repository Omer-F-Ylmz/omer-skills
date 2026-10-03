# Motor kullanımı (video kuyruğu, Opus'suz)

## Üç komut
```powershell
video parti kuyruk --short --en-fazla 8 --usd-tavan 1.0   # öneri → tarama → akil → panel; panelde durur
video panel uygula docs/kurulumlar/parti/<pid>/panel.md   # Ömer sütunu → karar + kayıt
video parti kapat <pid>                                    # rapor-denetle → gitleaks → commit + kuyruk --isle + push
```
`kuyruk` son satırda panel yolunu ve defter özetini (çağrı sayısı, $) yazar. Kuyruk dosyası varsayılan olarak `docs/video-tarama/kuyruk.md`; başka bir dosya için yolu ilk argüman olarak verin. `--short`/`--uzun` verilmezse kuyruktaki sıradaki parti alınır.

## Panel nasıl doldurulur
Her aday satırında "Ömer" sütununa tek kelime yazılır. Boş bırakılan satıra dokunulmaz. Desktop panelde öneri yazabilir, kararı Ömer onaylar.
- **AL**: kur/uygula · **RED**: alma, gerekçe kayda geçer · **ERTELE**: yalnız kayıt satırı düşer
- **DENE**: önce ölç/dene · **ÖĞREN**: bilgi olarak al, kurulum yok · **UYARLA**: kendi aracımıza uyarla
- **ZATEN VAR**: kurulu ya da bizde karşılığı var

## Kesinti sonrası devam
```powershell
video parti devam <pid>                       # tamamlanan çağrı tekrarlanmaz
video parti devam <pid> --form-red-yeniden    # form_red videolara yeni deneme hakkı
video parti devam <pid> --yeniden-tara        # bitmiş videoları düzeltilmiş girdiyle baştan tara
video parti akil <pid>                        # yalnız aday işi + panel
```

## Durum ve tavan
```powershell
video parti durum <pid>                       # video başına paket/tarama durumu + defter
video parti devam <pid> --cagri-ek 2 --usd-ek 0.3
```
Çağrı ve $ tavanı parti başında sabitlenir (`--cagri-tavan`, `--usd-tavan`). Tavan aşılırsa motor durur (çıkış 3, durum `tavan`). Tavanı yalnız `--cagri-ek`/`--usd-ek` açıkça yükseltir. Ek, mevcut tavana eklenir; harcanan tutara değil.

## İkinci göz (M5)
Sonnet formu geçen her video aynı paketle luna'ya (OpenRouter, `openai/gpt-6-luna-pro`) da taratılır. Luna'nın yalnız kendisinde olan kalemi (anahtar kesişimi yok) doğrulanırsa rapora ` (ikinci göz)` etiketiyle eklenir: metin kalemi URL'si paket.md'de ya da Jev "kaynak destekliyor" (segmentler ±60 sn + açıklamanın tamamı); kare kalemi görsel yargıç (hafif Sonnet, en yakın ≤8 kare, video başına tek çağrı). Doğrulanamayan kalem raporun `## Doğrulanamadı (ikinci göz)` ekinde görünür, panele girmez.
- Bayrak: `--ikinci-goz luna|yok` (varsayılan luna). `OPENROUTER_API_KEY` yoksa ya da `yok` seçildiyse rapor ve `parti durum` "ikinci göz KAPALI: <sebep>" yazar.
- Tavan (parti başına, Sonnet tavanından ayrı): OpenRouter $0,10 · Jev 150 durum · yargıç 8 çağrı; video başına luna ≤2, yargıç ≤1. Defterde `ikinci_goz_luna/_jev/_yargic` satırları; `parti durum` ikinci göz satırı (eklenen · doğrulanamadı · $ · Jev · yargıç).
- Luna hatası/429/geçersiz JSON: video Sonnet sonucuyla `tamam` kalır, rapora not düşülür.

## Hata durumları
- **hata**: taşıyıcı ya da çağrı kesildi. `devam` yalnız o grubu yeniden çağırır.
- **form_red**: form şemayı ya da kuralları geçmedi (eksik alan, açıklama bağlantısına karar yok, kare kaynaklı iddiada `karede_gorulen` boş, zamansız kanıt). Hata listesi `durum`'da görünür. `--form-red-yeniden` ile tekrar denenir.

## Desktop'tan izleme (köprü)
`cc-kopru komut "video parti durum <pid>"`: salt okunur, çağrı yapmaz. Panel dosyası `docs/kurulumlar/parti/<pid>/panel.md`.

## Dayanıklılık (M2e)

- **Kısmi kabul:** iki yeniden istekten sonra form hâlâ geçmiyorsa video kaybolmaz; son formun geçerli kısmıyla rapor yazılır, geçmeyen alan raporda `EKSİK: <alan> (<sebep>)`, durum `tamam_eksik`, panelde `## Eksik alanlar` (video · aday · alan). `rapor-denetle` EKSİK satırını geçerli-ama-uyarılı sayar. Son form `.kos/<parti>/form/<id>.json`'da; `video parti devam <parti> --kismi-kabul` form_red videoları bu dosyadan çağrısız `tamam_eksik` yapar (M2e öncesi partilerde dosya yok → form_red kalır, `--form-red-yeniden` gerekir). Kanıt zamanı yalnız kaynak altyazı/kare kaleminde aranır; açıklama kaynaklı kalemde beklenmez.
- **Kare sayısı:** short 3; uzun süre/2.5 dk (en az 4, en fazla 8); kuyruk notu ya da başlıkta site/UI · landing · prompt anatomisi geçerse en fazla 12. Paket adımı `paket <id>: kare N (neden)` yazar. Uzun videonun çağrı girdisi 40k jetonu aşarsa kare düşürülür, rapor künyesine not düşer.
- **panel uygula:** sütun sayısı başlıkla (8) uyuşmayan satır varsa satır numarasıyla uyarır, hiçbir karar işlenmez (rc 2). Sonda `işlenen N · boş M · hatalı K`; tanınmayan Ömer değeri hatalı sayılır (rc≠0).
- **Sınıflandırma:** ipucu/kural/teknik/prompt/iş akışı adayları kurulu/eşdeğer eşleşmesine girmez (yalnız T0 ve prompt yolları). Alt tür tek değer: kurulu > kendi aracımız > araç > servis > ürün; çelişkide gerekçede "alt tür çakışması".
- **Köprü:** Desktop'ta `video parti durum <parti>` ve `video kuyruk` (öneri) izinli; yazan alt komutlar (`parti baslat/kuyruk/devam/akil/kapat`, `kuyruk --isle`, `panel uygula`) izinsiz. İzin değişikliğinden sonra Desktop yeniden başlatılır.

- Panel ön-doldurma (M11): Ömer sütunu yalnız deterministik kurallarla önerilir — (a) kayıtta aynı adın en son Ömer kararı (RED hariç) · (b) ZATEN VAR · (c) tür prompt/teknik → ÖĞREN · (d) T0 → ÖĞREN; araştırılmış araç, SOR/RED, -gelistirme ve OLASI satırları boş kalır.
- Ön-doldurulan hücre yalnız öneridir: Ömer değiştirebilir, `panel uygula` Ömer sütununda ne yazıyorsa onu işler; dolu hücre (akil --yeniden dahil) asla ezilmez.
- Panelde `## Ön-doldurulan` bölümü (aday · karar · kural a/b/c/d) ve üstte "karar bekleyen N · ön-doldurulan M" özeti; aynı özet `video parti akil` çıktısında.

## Kanal keşfi (KANAL-1)
1. `video kanal liste` → `docs/video-tarama/kanallar.md`: kanal · işlenen (n) · değerli · son tarih · öneri (takip: değerli ≥2 ve oran ≥0.5 · atla: değerli 0 ve n ≥3 · bir-kez: diğer).
2. Ömer sütununa takip / bir-kez / atla yaz; `video kanal onay docs/video-tarama/kanallar.md` → `kanallar.json` (boş satır işlenmez).
3. `video kanal envanter [--kanal <channel_id>]`: yalnız onaylı kanallar, yt-dlp flat (videos + shorts, indirme yok), istekler arası 2 sn, 429/403'te 2 yeniden deneme → yarım; önbellek `.kos/kanal/<id>.json`. Kimliksiz kanal "kimlik yok" atlanır.
4. `video kanal etiket` → `docs/olcumler/kanal-etiket.json` (değerli = ≥1 AL/UYARLA/DENE; iptal parti hariç).
KANAL-2: kimlik çözme · Jev ön eleme → luna altyazı okuma → Sonnet tam tarama kademeleri bu etiketlerle ayarlanır.
