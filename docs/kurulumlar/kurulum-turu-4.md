# Kurulum turu 4 (2026-10-10)

Kaynak: `kacan-adaylar.md` "Tur 4 adayları" (34 aday). Ayrıntı: `tur4-sonuc.tsv`. Betik: `tools/kurulum-turu-4.sh` (`--kuru` 0 hata, sonra gerçek koşu; log `.kos/kurulum-4/kurulum-turu-4.log`, geri-al `.kos/kurulum-4/geri-al.sh`, tam SHA `.kos/kurulum-4/kurtarma.json`).

## Sayılar
KUR 1 · KUR-duzeltmeli 2 · HESAP 1 · ÖNERİLMEZ 1 · AYRI-UYGULAMA 13 (i web 7 · ii masaüstü/model 3 · iii sunucu/GPU 3) · RED 16 (bulunamadı 6 · gürültü 9 · lisans 1) · ZATEN 0. Toplam 34.

## Kurulanlar
| ad | tür | pin | içerik |
|---|---|---|---|
| Dammyjay93/interface-design | plugin (user) | 2f9be3206855 | MIT ★5785, 1 plugin |
| wshobson/agents → mobile-android-design | skill kopyası | 46891e7e60da | MIT ★40315, yalnız 1 skill (94 plugin'lik marketplace eklenmedi) |
| JimLiu/baoyu-skills | skill kopyası | 1567581c26ec | MIT ★26512, 14 skill; 6 atlandı (danger-* ×2, post-to-* ×3, electron-extract); baoyu-wechat-summary (sohbet verisi) yanlışlıkla kopyalandı, silme hook tarafından engellendi → Ömer silsin |

## AYRI-UYGULAMA
| aday | alt | not |
|---|---|---|
| dev.epicgames.com · actorcore/magazine/discussions/tips.reallusion.com · filesync.app (flesync/fllesync OCR) | i web | yalnız tarayıcı |
| soupday/cc_blender_tools 2.4.4 · soupday/CCiC-Blender-Pipeline-Plugin 2.4.4 | ii Blender eklentisi | GPL-3.0, release dosyası yok (kaynak zip), Blender + Character Creator gerekir; winget yok |
| Qwen/Qwen3-4B-Instruct-2507 | ii model | apache-2.0, ~8GB; LM Studio/Ollama |
| SkyworkAI/SkyReels-V2 (3 OCR satırı) | iii GPU | özel lisans, 14B ≈ 14GB+ |

## HESAP / ÖNERİLMEZ
| aday | sınıf | neden |
|---|---|---|
| coderabbit → coderabbitai/skills (resmi marketplace `coderabbit`, MIT, pin 928c3b61f71b) | HESAP | CLI girişi şart; hesaplar.md + tetikleyici.md |
| vercel-labs/skills (npm `skills` 1.7.2) | ÖNERİLMEZ | telemetri, pin/lisans kapısını delen `npx skills add` yolu |

## RED
Bulunamadı (GitHub 404): a8aj-1/det, ssal-1/der, aoe2/genie, bodies/constraints, huibui-ai/aemma, ibtests/palmierprofests. Gürültü: aw.githubusercontent.com, ocalhost:4000, copy/run-py, copy/run-pyr, deploy/docker-compose ×3, chaosclothsharedsimconfig/gam, glow/self-llumination. Lisans: PanicPetal/ALS-Community (NOASSERTION, 2024).

## Doğrulama
16 skill klasörü (14 baoyu + mobile-android-design + wechat-summary) hepsinde SKILL.md var, ad çakışması 0. `claude plugin list`: interface-design@interface-design enabled.
