---
name: is-akisi
description: Ömer'in her işte bağlayıcı tek çalışma biçimi — iş başı sırası, katalog/hazır/referans/varlık, süreç ve kaynak kuralları (RAM, fatura, vekil, claude -p), token kuralları, kalite kapısı, ara kayıt/devir/bölünme/bitiş. Köprü oturumunda (DEVAM-KURALI.md bunu gösterir) ve her omer-skills işinin başında oku.
---

# İş akışı (bağlayıcı)
`Lnn` = arsiv.md satırı (gerekçe/tarihçe orada). Öncelik: VEKİL ve JETON en üst; çelişkide tarihi yeni kazanır. Görev dosyasındaki kurallar aynen geçerli.

## 0. Yasaklar
- ~/.claude/settings.json ve kullanıcı ortamında ANTHROPIC_BASE_URL'ye DOKUNMA; test vekili yalnız süreç başına env, ona HEADROOM_CC_SWITCH_* kopyalanmaz; Headroom testinden sonra `python .kos/kopru/vekil_dene.py` 401 vermeli (502 = bozuk → `.kos/kopru/onay/headroom_ccswitch_onar.py`, --geri var). L2 L16
- Güvenlik ayarları, Ömer'in commitsiz dosyaları korunur; push yok; kurulu hiçbir şey kaldırılmaz; anahtar değeri yazdırılmaz; arka plan pencere açmaz; canlı ~/.claude yalnız onay betiğiyle. L37
- Junction'lı worktree'yi çıplak `git worktree remove`/`--force` ile silme: önce her junction `rmdir`, ya da işin --sil komutu; kurduğun junction'ları devire yaz. L40
- `KOPRU_OMNIROUTE=1` iken onay `uygula`, kabul/kalite kararı, ölçüm tabanı yazımı YOK — yalnız araştırma/indirme/etiketleme/taslak. L10
- Fatura: `.kos/kopru/api-kredi.ac` varsa alt süreç ANTHROPIC_API_KEY'i devralabilir; yoksa (api-kredi.kapali) hiçbir alt sürece verme ('Credit balance is too low'). Aç/kapa yalnız Ömer. L8 L9

## 1. İş başı (sırayla)
**Raporun ilk satırı her işte (rutin dahil): `Katalog: kullanılan [araç/betik adları] · atlanan [..] (neden)` — kullanılanlar boş bırakılmaz.** L3
**Her ayrı `claude -p`: `--strict-mcp-config --mcp-config "{\"mcpServers\":{}}" --disable-slash-commands`, olcum_sira ile, aynı anda ≤1.** L23
1. Kilit `.kos/kopru/gorev/<görev>-dN.kilit`; varsa ÇIK. L31
2. Durum TEK komut: `python C:/Projeler/omer-skills/.kos/kopru/durum_ozet.py <görev> [wt]` (git/son commit/devir/rapor/SIRA/kilit/durma); ek okuma yalnız eksik için; Desktop devir özetini gömdüyse yalnız `git log -3`. Yapılanı tekrarlama, yarımı tamamla. L32 L15
3. Katalog: rutin tek alanlı işte ÇAĞIRMA. Zor işte (≥2 alan, alan dışı, araç adı bilinmiyor) TEK çağrı/tek Bash: departman-* müdür dizini + plan-kur + katalog_ara (≤3 sorgu, ≤40 satır; yetenek-getir yoksa `python C:/Projeler/omer-skills-wt/envanter2/tools/katalog_ara.py "<iş>" --tam`) + docs/atlas oyun kitabı; ek sorgu yok; `<katalog>` eki geldiyse yalnız ondan seç. İlgili her kayıt (skill · plugin · MCP · CLI · kütüphane · betik) planda adımıyla; gerekçesiz dışarıda kalan yok. L3 L20 L21
4. HAZIR-ÖNCE: hazır kod/varlık/şablonu al, değiştirip premium yap; sıfırdan yalnız hazır yoksa ya da ölçülerek kötüyse. L3
5. Araştırma üç kol (uygun olanlar): alanın en iyi örnekleri · açık kaynak repo/kod · yapılış anlatan yazı/video (docs/video-tarama/ dahil, salt okuma). Mekanizma alınır, birebir klon yok; lisansı uygun hazır alınıp geliştirilebilir. L22
6. Site/UI REFERANS-ÖNCE: Playwright ile referans ekran görüntüsü + DOM/CSS/hareket (design-extractor/design-dna, image-to-code; sayı önce: renk, font, ızgara, boşluk, geçiş, kütüphane) → mekanizma tablosu → 2–3 referansın iyisini birleştirip özgün premium. Başkasının görseli/metni/logosu yok; görüntü yalnız gerekli karede. L4
7. 3D/VARLIK: sıfırdan modelleme yok. Merdiven: (1) yerel (2) Objaverse (HF, hesapsız; Sketchfab uid; lisans+yazar annotations) (3) Poly Haven API / ambientCG (CC0) (4) Sketchfab API yalnız Ömer'in token'ı ortamdaysa (5) ücretsiz görüntü→3D (HF Spaces Hunyuan3D/TRELLIS, kalite kapılı) (6) en son sade bpy. Blender yalnız küçük düzenleme (ölçek/yön, decimate, malzeme, UV, GLB) `-b` + betik + kompakt JSON. Hesap/anahtar yok; CC-BY → kolofonda atıf. L5
8. SAĞLAM PLAN içerir: (1) katalog araçları + öğrenimler (docs/video-tarama/*, .kos/kopru/rapor/ig-*.md, ~/.claude/ig41-kur-eklenen.json, kaynak-tarama, omer-kurallar.md — salt okuma) (2) iş türü kapıları: test, güvenlik (semgrep · gitleaks · strix · ZAP · OWASP skill'leri), a11y/SEO, KVKK, kapanış listesi 6 madde (3) değişiklik inceleme ajanları (kod/güvenlik/tasarım) (4) kritik/belirsiz kararda tartışma konseyi (octo:skill-debate · octo:skill-council · ecc:council-multi-model; Claude personaları, harici model yalnız ücretsiz) (5) faz başına jeton bütçesi. Kullanılmayan ilgili araca tek satır gerekçe. L26

## 2. Süreç ve kaynak
- Uzun iş (ölçüm, toplu üretim, indirme, kurulum testi, büyük tarama) arka plana: ölçüm `olcum_sira.py`, diğeri `arka.py`; günlük `.kos/kopru/<görev>-*.log`; bitince yapılacak devire. L33
- Ayrı claude -p yalnız gerekirse, bayraklar §1 başındaki gibi (düz claude -p ~4 GB). L23
- RAM asla %90'ı geçmez: olcum_sira ilk yuva <%88, ek yuva <%86; kendi koşucuların kapısı %86, paralel ≤4; >1 GB yükleyen iş (OCR, torch) aynı anda 1. RAM ≥%88: yeni süreç açma, bekle. L7
- Bekleme: oturum 3 sa / 60 tur, 40. dakikada bırakma. Arka plan ölçümünü bekliyor ve paralel iş yoksa ~5 dk aralıkla tek kısa komut (`python .kos/kopru/bekle.py <günlük> "BITTI|Traceback" 540`); bitince karar + onay betiği aynı oturumda. RAM ≥%90 ve yalnız bekliyorsan (kalan >15 dk): devire `BEKLE: <günlük> BITTI olunca → <adımlar>`, SIRA satırı, ÇIK. L7 L12 L13
- graphify update yalnız `python .kos/kopru/graphify_hafif.py [kök]` ile (artımlı ~4 sn/332 MB; çıplak `graphify update .` değil): oturum sonunda arka planda BAŞLATMA; yalnız iş başında, başka graphify/ağır python yokken; RAM kapısı artımlı <%85, tam (--tam ya da ilk kurulum, ~1.5 GB) <%75. Keşif önce cc-kopru oku (iskelet/sembol). L1 L42
- Test/inceleme tarayıcısı Chrome (Playwright Chrome kanalı ya da Claude in Chrome), Opera değil; pencere öne çıkmaz. L25

## 3. Token (kalite düşmeden)
- Effort varsayılan HIGH; xhigh yalnız Desktop görev metninde yazarsa. Mekanik adım (test koşma, taşıma, paketleme, rapor, ölçüm) claude -p'de `--effort medium` (ajan-sira.tsv 4. sütun `efor=medium`); karar/tasarım/kod yazma HIGH. MAX_THINKING_TOKENS ekleme (Opus 5.5'te etkisiz). L6 L16
- Alt ajan varsayılan 0; zorunluysa tek, kısa çıktılı, ≤150k. Araştırma/okuma gerekiyorsa büyük partiyle, ana oturuma damıtılmış özet. L6 L23
- claude -p ölçümü görev başına ≤6; yeniden ölçüm turu yalnız Desktop izniyle. Yöntem: tam kollu yeniden oynatma yok; taban tarihsel dökümden (k0_olc.py), B yalnız gerçek işte; A/B yalnız şüpheli tek mekanizmada, 1 adımlık görevle, ≤2 claude -p. L6 L17
- Okuma: graphify/oku sembol-aralık, dosyayı bütün açma; Write yerine Edit; aynı dosyayı iki kez okuma; skill gerekiyorsa yalnız ilgili SKILL.md bölümü Read ile. L6 L3
- Ölçüm/analiz birden çok küçük komut yerine tek betik; çıktı sayıya/özete iner, ham döküm bağlama girmez. L15
- Token ve kalite birlikte ölçülür: kalite düşüren tasarruf kabul edilmez (onar, yeniden ölç); token'ı gereksiz artıran kalite artışının ucuz yolu aranır. Faz/iş başına jeton kaydı rapora (ajan_sira işleri is-kaydi.tsv'ye kendiliğinden yazılır). L27 L23
- Büyük çıktı ham dosyada kalır, bağlama yalnız öz: test koşusu `rtk pytest`/`rtk dotnet test` (`jev log` anahtarsız ortamda boş döner), tarama JSON `jev triage`, diğer >20 kB günlük `python tools/ucuz_alt.py <istem.md> <öz.md> <günlük>` (Claude-dışı). TOKEN-3 K16: 3 örnekte özden karar = hamdan karar.
- Rapor/devir kısa; övgü/tekrar yok. L6

### Token araç sırası
Ölçüm: `python .claude/token4/a0.py` → docs/kutuphane/olcum/token-4-arac.tsv (14 Eki). Keşif sırası (GRAPHIFY-ULTRA-1): graphify-out/GRAPH_REPORT.md başlıkları (harita) → `graphify query`/cc-kopru `oku` iskelet-sembol → dosya yalnız kanıt satırı için Read offset/limit (~20 satır); >300 satırlık dosyanın aralıksız Read'i köprü ajanlarında `tools/oku_yonlendir.py` ile iskelete döner.
- Konum: sembol/ilişki → graphify query/oku; içerik konumu → Grep (files_with_matches/-n). `rtk grep` en kalabalık, en düşük oranlı kalem (8372 komut, %25.6).
- `rtk discover` kaçakları transkriptten sayar; kanca yeniden yazımı transkripte düşmez → çoğu yanlış pozitif (14 Eki: rtk 4764 komut koştu, transkriptte `rtk` önekli 2651). Gerçek kaçak ölçümü: rtk history.db `hook_decisions`.
- YASAK: `git show <ref>:<yol>` ile dosya dökmek (rtk passthrough, 14 Eki tek günde 1.56M token, %0 tasarruf) → `git diff <ref> -- <yol>` ya da geçici dosya + dar Read. `git status --short` de passthrough (ort. 780 token) → yol ver: `git status --short -- <yollar>`. L44
- YASAK: ev dizini, AppData ve `..` üstünde `ls` (-la/-t/-A): komut başı 28–114 sn, girdi 0.9–2.8M token (rtk süzmese bağlamı doldurur). Dar Glob deseni kullan. L41

## 4. Kalite kapısı
- Sayı önce (kapi.mjs/JSON); kare/görüntü yalnız eşik aşılınca, adım başı ≤2 görüntü. L6
- Plandaki iş türü kapıları + inceleme ajanları + kritik kararda konsey (§1.8). L26

## 5. Kayıt, devir, bölünme, bitiş
- İlk 15 dk: rapor/<görev>.md'ye ilk bulgular, devir/<görev>-devam.md'ye plan; sonra ~15 dk'da bir güncelle + wt'de commit. Araştırma ve alt ajan sonuçları bağlamda değil dosyada. L35
- Ara kayıt (en geç 150. dk ya da 55. tur): (a) rapor sonuna "Ara rapor N" ≤12 satır (yapılan · ölçüm · kalan · onay komutu) (b) devir üzerine yaz (c) SIRA.md satırı (d) testler yeşilse kol dalında commit (Ömer'in commitsiz dosyaları hariç). Tek tur: rapor + devir Write, sonra TEK Bash (SIRA + git add + commit). L34 L12 L15
- Devir şeması (≤15 satır): `KALAN:` sıralı adımlar · `ARKA PLAN:` günlük + bitince yapılacak · `SON COMMIT:` hash · `AÇIK KARAR:` Desktop/Ömer'e soru (yoksa 'yok'). L15
- Durma: her ara kayıtta durum_ozet son satırı `-- durma: … (%X)`; %X ≥30 → ara kayıt + DUR (Desktop yeni oturum açar). /compact yok; köprü ayarı değişmez. L39
- Bölünme (M5, sabit 45 değil): yeni oturum ~100–155k tek sefer, sürdürmek adım başı ~0.1·C → C ≥200k ve ≥8 adım kaldıysa (C=150k'da ≥13) ara kayıt + DUR. L39 L6
- Hat çıkarımı: iş sonunda tekrar kullanılabilir öğrenim (mekanizma, araç sırası, kalıp) ilgili/yeni skill'e — CC + claude.ai zip birlikte. L24
- Bitti: son rapor + SIRA'ya `<GÖREV> BİTTİ` + devire `BİTTİ`. L36
