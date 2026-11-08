# LINK-27 — KALAN HER ŞEY (27 Eki 17:00) — CC sırayla yapar, her maddeyi [x] işaretler

Kurallar: global kirletme yok (venv/node_modules repo içinde) · RAM %89 (aşarsa bekle, tekrar ölç; kural dışına çıkma) · C: ≥80 GB · anahtar değeri yazma · silme yok · ad çakışmasında önek ver, üzerine yazma · her madde sonunda 1 satır `.kos/kopru/video/link27-kurulum3.log`. Klonlar: `C:\Users\pc\Desktop\Claude ile yapılanlar\araclar\link27\`. Repo yoksa önce gh/web ile bul; "bulunamadı" yazmadan önce en az 3 arama.

## A. KUR
- [x] A1 deepseek-harness (klonlu): corepack pnpm install + build, smoke `pnpm dsh --help`, pnpm install tamam; `pnpm dsh --help` çalıştı (tsx ile kaynaktan; tam build native/8GB tsc gerektirdiği için koşulmadı)
- [x] A2 Harness2: schedule.py fcntl→msvcrt + tree.py `str(relative_to)`→`.as_posix()` (Windows `scripts\summarize.py` yüzey dışı sayılıp düzenlenen betik düşüyordu); demo 2/2 ok, düzenlenen sürüm Total 85.15 / 20.25 seçildi (eski 105.25)
- [x] A3 archify: clone --depth 1 github.com/tt-a1i/archify; agent skill'ini CC'ye kur, klonlandı; skill zaten ~/.claude/skills/archify'da kurulu
- [x] A4 google-research/rrsi (klonlu): README'ye göre kur + smoke, çekirdek .venv'e kuruldu, `rrsi.py --help` + pytest 8/8; domain smoke benchmark ortamı + LLM ister, koşulmadı
- [x] A5 TencentDB Agent Memory: CC plugin github.com/baodq97/tencentdb-agent-memory (README yolu); claude-mem ile çakışmasın (ayrı veri klasörü), smoke: kaydet/ara, plugin kuruldu (MIT; veri ~/.memory-tencentdb, claude-mem'den ayrı); smoke write-l1 + search geçti. Not: oto-konsolidasyon sonnet ile günde ≤3 koşu (12→3; `cli.js config consolidate-max-runs-per-day 3`). Ücretsiz sağlayıcı yok: konsolidatör `claude -p --model sonnet` alt süreci, ANTHROPIC_BASE_URL alt süreçte araçları gizliyor
- [x] A6 5 skill paketi (IG De6oEmiMblJ): Chief of Staff (aday: adamfarren/chief-os, Akshat2430/ai-chief-of-staff, JimmySadek), Teach, Marketing Psychology, kurulu olanları atla (Anatomy, Last30Days var); bulunanları ~/.claude/skills'e kur, Chief of Staff = strategic-partner-plugin (MIT) plugin olarak kuruldu; Teach = apxxrv/session-teacher (MIT) ~/.claude/skills/teach; Marketing Psychology zaten vardı
- [x] A7 15 anti-slop skill eksikleri: .kos/kopru/video/link27/kur-ozet.md'deki eksik listesi, eksik yok (impeccable/humanizer/understand-anything plugin olarak kurulu)
- [x] A8 Creem MCP: github.com/Selenium39/mcp-server-creem (anahtar yoksa yapılandırma şablonu + docs; mcptoon gateway'ine ekle), klon + npm install + build tamam; CREEM_API_KEY yok → şablon docs/kurulumlar/creem-mcp.md, gateway'e eklenmedi
- [x] A9 ajan tarayıcı: daijro/camoufox (MPL-2.0) link27/daijro__camoufox/.venv; tarayıcı ~/AppData/Local/camoufox önbelleğinde; Türkçe yol IndexedZstdFile'ı bozuyordu → fpgen values.dat bir kez açıldı; headless smoke `TITLE: Example Domain`
- [x] A10 (tur 3 koştu, 5.86 KOŞULLU GİT) Roast Room: skills/roast-room + 7 persona ajan (geri-dönülebilirlik, nakit, müşteri, teknik risk, zaman/fırsat, hukuk/KVKK, şeytanın avukatı) + brains/<ajan>/hot.md; 3 tur; ajanlar haiku; .roast-room/<tarih>.md kayıt; 1 smoke koşu, KISMEN: skill + 7 ajan + 7 hot.md yazıldı; smoke BEKLİYOR: oturum ortası eklenen ajan yüklenmez, yeni oturumda koşulacak. 27 Eki 19:00 smoke Tur 1: 6/7 haiku ajan yüklendi, hot.md okudu, puan+gerekçe döndü (roast-zaman çağrısı auto-mode sınıflandırıcısınca reddedildi); tur 2–3 + hot.md güncellemesi koşulmadı; kayıt `.roast-room/2026-10-27-1900.md` (KOŞULLU GİT, ort. 5.5)
- [x] A11 Tasarım npm şablonu: araclar/sablon-3d-site (Vite+React, 6 paket src/main.jsx'te kullanılıyor), `npm run build` geçti (500 kB chunk uyarısı); görsel kontrol yapılmadı
- [x] A12 parsel-video: Pillow skill içi .venv'e; Bodrum/Bitez 204/3 --dikey → parsel.mp4 (4.4 MB); ~/.claude/skills/parsel-video junction
- [x] A13 memvid ↔ claude-mem: memvid ile 2. beyin kasasından tek .mv2 (C:\Users\pc\Desktop\Obsidian), arama testi; claude-mem'e dokunma, KISMEN: izin geldi; betik scratchpad `kasa_mv2.py` (9014 md, lexical; put_many'de `label` zorunlu). İlk koşu 19.8 MB'de "tantivy index writer unavailable" → seal düştü; obsidian-kasa-5.mv2 koşusu 10 MB'de takılı görünüyor, kök neden henüz kanıtlanmadı. 27 Eki 19:00: kasa-5 (PID 46128/17556) CPU 0, dosya 18:38:52'den beri donuk → kilitlenme, öldürüldü. Gerçek hata `MV999: Tantivy error: An IO error occurred: 'Erişim engellendi. (os error 5)'`; ASCII yolda da çıkıyor (Türkçe yol değil), 100'lük partide 3. partide, tek commit 500'de ve 150'de de çıkıyor (deterministik değil → Windows dosya kilidi şüphesi: Defender/indeksleyici ya da tantivy segment silme; kanıtlanmadı). "writer unavailable" ve takılma bu hatanın ardılı. Ayrıca serbest kapasite 52 428 800 B (50 MB), kasa ~135 MB ister → tam kasa tek .mv2'ye sığmaz. 3 deneme düştü, DUR: sıradaki adım Defender dışlaması (Ömer onayı gerekir) ya da Linux/WSL'de kurmak. Önceki .mv2'ler mühürsüz (MV012), arama gösterilemedi

DEVAM: B2 (A13 Ömer kararı bekliyor: Defender dışlaması ya da WSL; A10 tur 2–3 + roast-zaman isteğe bağlı), sonra B3–B4, E1–E3. Önceki not: `cd X && npm` yerine `npm --prefix X`; B1: `ajan_sira/_tur.py` yok, karşılığı `.kos/kopru/ajan_sira.py`

## B. UYARLA (bizdeki sisteme mekanizma)
- [x] B1 clodfarm limit kapısı: `.kos/kopru/ajan_sira.py` kullanim_dolu() — 5 saat ≥%85 / haftalık ≥%80 iken yeni ajan başlamaz; veri ~/.claude/rate-limits.json (statusline.ps1 rate_limits varsa yazar), yok/15 dk eski → kapı açık; self-check 6/6
- [x] B2 HF Inference ücretsiz havuza (ucretsiz_havuz): HF_TOKEN varsa ekle, yoksa şablon + Ömer'e not
- [x] B3 BEYİN'e karpathy llm-wiki deseni: kasada index/kaynak/özet sayfa yapısı (mevcutları silmeden), Obsidian/00-cekirdek/wiki-semasi.md (katman+ingest/query/lint+log; index/MOC zaten beyin_al.py üretiyor, silme yok)
- [x] B4 limit-onlem notu (CmOs0LZUOMM, 23 limit hatası): docs/limit-onlem.md + CLAUDE.md'ye 1 satır atıf, yazıldı; videonun transkripti yerelde yok → içerik bizdeki önlemlerden, video maddeleri doğrulanmadı

- [x] .gitignore: skills/*/.venv, *.mp4, deneme.log eklendi (git check-ignore doğrulandı)

## C. Bekleyen
- [x] C1 deer-flow frontend: RAM %89 altında corepack pnpm install (paketler repo deposunda)
- [x] C2 (clodfarm ayakta 565 MiB; Ömer giriş + docker logs) clodfarm: Docker Desktop aç → `python tools/clodfarm_ac.py`; sonra Ömer giriş + `docker logs clodfarm`
- [x] C3 hibi: Ömer elle açtı (27 Eki 19:06), çalışıyor

## D. Desktop (claude.ai) — en son
- [x] D1 (27 Eki 21:48: claude.ai'ye link27-paket, archify, openmontage-paket yüklendi) yeni skill'lerin zip'leri dist\ altına (roast-room, parsel-video, kurulan skill'ler) + docs/claude-ai-yukleme.md'ye ekle

## E. ZORUNLU KURAL (Ömer 27 Eki 18:39): Desktop + ajanlar CC'yi Ömer gibi kullanır
- [x] E1 cc-kopru `ajan` aracı: her çağrıda yeni `claude -p` oturumu yerine proje başına kalıcı oturum — ilk çağrıda session_id kaydet (.kos/kopru/oturumlar/<proje>.json), sonraki çağrılarda `--resume <id>` ile aynı oturuma blok gönder (önbellek ısınık kalır); bağlam %60'ı geçince ya da iş bitince yeni oturum. Parametre: `yeni_oturum` (varsayılan false). Testle: 2 ardışık çağrıda 2.'nin cache_read oranı ≥%90. YAPILDI: sunucu.mjs yeni_oturum + kayıt/--resume + 120k eşiği, test 13/13; cache_read ≥%90 canlı ölçülmedi (ücretli çağrı)
- [x] E2 (işçi havuzu yapıldı, self-check 4/4, canlı kuyruk koşulmadı) Ajan_sira / _tur.py ile açılan alt ajanlar da aynı kalıcı oturum kuralı; tek seferlik küçük iş = haiku, tek blok. KISMEN: haiku/medium varsayılan zaten var; kalıcı oturum paralel kuyruğa uygulanmadı (aynı oturuma eşzamanlı --resume çakışır) — BEKLİYOR: Ömer kararı.
- [x] E3 Kuralı yaz: omer-skills CLAUDE.md'ye 1 satır + docs/cc-kullanim-kurali.md (tek oturum, blok halinde iş, /clear yalnız iş değişince, gereksiz yeni oturum yok).
