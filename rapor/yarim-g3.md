# YARIM-G3 raporu (24.10)

Yöntem: 3 salt-okuma alt ajan, 29 işi görev dosyası + ajan-sira sonucu + git log + dar testle denetledi. Kod değişikliği yok. Bütçe $4 tavanına dayandığı için kalan işler devam dosyasına yazıldı. Tam suit ve CI koşulmadı.

| iş | durum | kanıt / kalan |
|---|---|---|
| ajan-akis-1 | DEVAM + ÖMER | af55760a, test_akis_damit 8 yeşil; kabul tutmadı (ücretsiz 57→40/55/58, giriş jetonu +%4/+%8,5). Kalan: akis_olc.py madde-çıkarma ablation. ÖMER: dist/opus-akis.zip + fable-dusunme.zip yükle |
| arac-bul-2 | ZATEN BİTMİŞ | 2797cd03+86683386; rapor/arac-bul-2.tsv 221 satır, bilinmiyor %1,8 |
| arac-zorunlu-4 | DEVAM | bdab1c58, 39 yeşil; --oran 20 → arac_eksik %90 (hedef ≤%10) tutmadı; tools/cekirdek-genis.json yok |
| autoharness-kur | ZATEN BİTMİŞ + ÖMER | ed4fdb44; ÖMER: dist/autoharness/autoharness-learn.zip yükle, kayba hangi repoda koşsun söyle |
| fable-ajan | ÖMER | df76ac8d, 09b86cb6; `onay/fable_ajan_uygula.py --kuru` 117 ajan gösteriyor (canlıda uygulanmamış). Sıra: kalite_3 → fable_1 → fable_ajan; sonra ajan_getir_zip.py, dist/fable-ajan/calisma-protokolu.zip yükle |
| fable-video | ZATEN BİTMİŞ | bf3310f2, bb8b1b1b; test_m2a 11 yeşil |
| guvenlik-yama-1 | DEVAM | commit/rapor yok; kalan: node/PHP/Java resmi sürüm eşleşmesi, SHA256, ZAP-Java17, npm audit, ≤15 satır rapor |
| jev-1 | ÖMER | 7a1823b6, db82fd45; `.kos/kopru/onay/jev_1d4_uygula.py --kuru` sonra uygula. Açık sapma: J02/J04 rubrik 0 |
| jev-2 | ÖMER | 6d47de70, test_jev_yargic 97 yeşil, ρ 0.43→0.62; ÖMER: JEV_SKILL_HOOK=0 ya da skill sayısını ~400'e indir kararı; dist/jev-2/jev.zip yükle |
| kopru-effort-1 | ZATEN BİTMİŞ + ÖMER | 8d2e3c49, ajan-argv 12/12; ÖMER: köprü/Desktop yeniden başlat |
| mcp-ac-2 | DEVAM | 6e792097; "ek maliyet ≤%1" tutmadı (render +%19,5, blender süzülmüyor). Kalan: tools/mcp_profil.py render süzgeci + ≤6 `claude -p` yeniden ölçüm. on-soz.md satırı sorusu Ömer'de |
| mcp-ac-2-a | DEVAM (mcp-ac-2 ile aynı) | sonuç json 0 bayt, ek ölçüt yok |
| mcp-hafif-2 | ÖMER | 12 commit, RAM 3184→907 MB, 24/24 eşit; ÖMER: `onay/mcp_hafif_2_uygula.py` (kuru→uygula). Canlı durum doğrulanamadı |
| model-politikasi | ZATEN BİTMİŞ | politika belgesi, uygulayan kod tools/yonlendir.py main'de |
| ollama-kim-1 | ÖMER | boşaltma kodu 88b2b901 (7 yeşil); çağıran süreç bulunamadı; ÖMER: OLLAMA_KEEP_ALIVE=30s ile Ollama'yı yeniden başlat |
| ollama-kim-1-a2 | ÖMER | aynı; ayrıca test_mem_bekci_saglik::test_aktif_oturumda_eski_gozlem KIRMIZI (ayrı iş) |
| omni-ayir | DEVAM + ÖMER | ffc48253..9b78a7c9, 12 yeşil; kalan: departman-verimlilik claude.ai zip + zip_denetle, etiket/görsel ölçümü (RAM >%70 engeli), O12. ÖMER: zip yükle |
| plan-kur-2 | ZATEN BİTMİŞ (RET kararı) | 5b867612, 3e37c8d1, 9503d6e5; test_plan_kur 15 yeşil; kol/plankur2 main'in 2 commit önünde (6256d056, 454732d8) alınmamış |
| skill-butce-1 | ÖMER | 7a4926e4, f25b0ad4, acc3de81; ÖMER: `skill_butce_1_uygula.py --kuru 1b` sonra `1b` |
| skill-paket-2 | DEVAM (Ömer kararı) | 12 Eki'de Ömer ertelemiş ("video işi mükemmel olunca"); hiç başlanmamış, büyük iş |
| skill-yukle-1 | ÖMER | 5dfdc0d0; 302 aile zip dist/claude-ai/yukle-23eki; ÖMER: YUKLE.md sırasıyla Desktop'ta yükle |
| skill-yukle-1-a | ÖMER (+küçük) | zip_denetle son turda yeniden koşulmadı; ecc-agentshield kurulu değil |
| stalemap-kur-2-a | ZATEN BİTMİŞ (küçük açık) | 89848a97, test_mcp_profil_stalemap 3 yeşil; `claude -p` açılış yükü ayrı işte (903831f6) |
| ucretsiz-havuz | BİTTİ (test) | 17bef40d; kırmızı test kök neden: AJAN-AKIS-1 çekirdek öneki istemi şişiriyordu, kova hesabı bozuluyordu → testte önek kapatıldı (kod değişmedi); test_ucretsiz_havuz 16 yeşil |
| ucretsiz-havuz-2 | DEVAM | b1713d7b; en büyük sağlayıcı payı %57,5 (hedef ≤%50); 263158b4 sonrası ≤%40 ama yeniden ölçülmedi: `kapi_tekrar.py --simdi --tavan=150` (arka.py ile; dış çağrı tavanı gerekebilir) |
| wt-arsiv-1 | ZATEN BİTMİŞ | 7 worktree arşivlendi, test_wt_arsiv 4 yeşil |
| zorunlu-arac-2 | ZATEN BİTMİŞ | 6280c324, test_zorunlu_arac 39 yeşil |
| zorunlu-arac-2-a | ZATEN BİTMİŞ | aynı kod; sonuç json 0 bayt |
| zorunlu-kullanim-1 | ZATEN BİTMİŞ | 71eab7d3, kapı testleri yeşil; DEVİR_MADDE kapandı |

Sayım: ZATEN BİTMİŞ 11 · ÖMER adımı bekleyen 9 · DEVAM 9 (bazıları çift). BEKLEMEDE işlerine (TELVE, logo, NEFFEX, Mai, REA uyarısı, 10 karar) bu grupta rastlanmadı.

Sapma: bütçe ($4) ölçüme gitti; kalan işler uygulanmadı. Yönetici/canlı ayara (~/.claude) dokunulmadı.
