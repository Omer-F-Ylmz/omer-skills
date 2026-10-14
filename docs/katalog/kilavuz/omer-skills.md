# omer-skills — 37 benzersiz kayıt

**Amaç:** Ömer'in kendi skill'leri: departman-* müdürleri (iş türüne göre araç sırası), Blender ve frontend-craft eklentileri, Desktop köprü sarmalayıcıları, video izleme/uygulama, ajan/tasarım katalogları.

**İç yapı:** İki [plugin] (blender, frontend-craft) ve alt skill'leri; departman-* yönlendiriciler; *-desktop sarmalayıcıları (cc-kopru ile CLI); video-* üçlüsü; katalog skill'leri (ajan-getir, awesome-rehber, tasarim-katalog).

## En güçlü parçalar
- `calisma-protokolu` — Her kodlama, plan, değerlendirme, hata ayıklama, araştırma işinde temel protokol.
- `frontend-craft:frontend-craft` — Landing/vitrin/panelde marka kararı, referans eşleme, 3 genişlikte screenshot döngüsü.
- `blender:blender-oturum` — 3B işte önce yüklenir; Blender oturumunu (aç, MCP, kaydet, kapat) CC yönetir.
- `departman-surec-plan` — Yeni iş/dalga başında koda dokunmadan niyet, spec, PRD, plan sırası.
- `departman-surec-inceleme` — Yapım bitince, commit/PR öncesi review, sadeleştirme, doğrulama sırası.
- `ajan-getir` — Agent aracı listesinde olmayan uzman ajan gerektiğinde (284 kurulu ajan).
- `video-izle` — YouTube'u altyazı özeti → Jev süzme → yalnız gereken kare ile kademeli izler.
- `gorsel-uret` — Görsel üretme/düzenleme/büyütme/arka plan silmede yerel ComfyUI oturumu.
- `departman-guvenlik` — Sır taraması, SAST, pentest, KVKK sırası; yayın öncesi güvenlik.
- `awesome-rehber` — Raflarda olmayan dış araç, kütüphane, eklenti ya da öğrenme kaynağı arayışı.

## Birlikte kullanım
- departman-surec-plan → (departman-frontend/backend-dotnet) → departman-surec-inceleme → departman-surec-git-yayin.
- video-tarama → video-izle → video-uygula: toplu tarama, izleme, riskli uygulamada onay.
- frontend-craft:frontend-craft + tasarim-katalog + omer-kutuphaneler + web-sahne-desenleri.
- blender:blender-oturum → blender:blender-uretim + omer-araclar blender_dogrula.

## Tuzaklar
- *-desktop skill'leri yalnız Desktop'ta cc-kopru ile koşar; claude.ai sandbox'ında koşmaz.
- video-uygula çalıştırılabilir her şeyi onaya bağlar; otomatik değil.
- departman-* yönlendiricileri hangi işte hangisinin açılacağı ayrımına dayanır; yanlış müdür yanlış araç sırası verir.
- frontend-craft eklentisi ile frontend-craft:frontend-craft skill'i aynı içeriğin iki girişi.

## Üyeler
- plugin (2): blender, frontend-craft
- skill (35): agent-reach-desktop, ajan-getir, animasyon-atolyesi, awesome-rehber, blender:blender-oturum, blender:blender-uretim, calisma-protokolu, departman-arastirma-ogrenme, departman-backend-dotnet, departman-belge, departman-frontend, departman-guvenlik, departman-surec-ajan-arac, departman-surec-git-yayin, departman-surec-inceleme, departman-surec-plan, departman-test-qa, departman-veri-db, departman-verimlilik, frontend-craft:frontend-craft, gitleaks-desktop, gorsel-uret, graphify-desktop, jev, model-sec, omer-kutuphaneler, playwright-cli-desktop, rtk-desktop, semgrep-desktop, skill-ui-desktop, tasarim-katalog, video-izle, video-tarama, video-uygula, web-sahne-desenleri
