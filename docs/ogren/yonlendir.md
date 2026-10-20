# ROUTER-1 (20 Eki) — görev başı kademe yönlendirici: ölçüm ve karar

Yönlendirici `tools/yonlendir.py` + `tools/yonlendir-kurallar.json` (20 tür, T0–T4), kayıt `.kos/kopru/yonlendir-kayit.jsonl`,
kart `skills/is-akisi/references/calisma-karti.md` (FABLE-1 protokolü + Opus/Fable tarzı), ölçüm `tools/olcum/yonlendir_olc.py`,
ham çıktı `docs/ogren/yonlendir-olcum/`. Önceki iş: ROUTER-1 d3 (12 Eki) `model_sec` (yalın oturum + effort sınıfı) — bayraklar ondan.

## Ölçüm (12 görev: 3 T0 · 3 kolay · 3 orta · 3 zor; kabul yerel ve mekanik)
| | başarı | jeton (girdi+önbellek+çıktı) | USD eşdeğeri | claude -p |
|---|---|---|---|---|
| A: hepsi Sonnet high, tek toplu çağrı | 12/12 | 17 748 (girdi 10 606 · çıktı 7 142) | 0.1138 | 1 |
| B: T0 betik · T1 ücretsiz · T2/T3 ayrı toplu | 12/12 (yükseltme 0) | 21 368 (Sonnet 19 555 + ücretsiz 1 813) | 0.1008 | 2 |
| fark | = | **+%20 (kapı ≥−%30)** | −%11 | |

Koşu 2 (yalnız T0+T1; Sonnet kısmı claude -p ≤4 tavanına sığmadı): G05 (MIT lisansı) kaldı — nemotron "JSON yok", ollama ve
gemma 429, combo "JSON yok". Gerçek akışta T2'ye yükselirdi; kararlılık ölçütü yine de tutmadı.
Sınıflayıcı yan ölçüsü (tür etiketsiz, tek ücretsiz çağrı): 3/12 doğru, jeton 0 → gemma 429; sınıflayıcı **ölçülemedi**.

## Neden kapı tutmadı (çağrı dökümünden)
- Çıktı jetonu B'de −%22 (5 546 ↔ 7 142): T0/T1 görevlerini Sonnet'ten almak gerçekten kazandırıyor.
- Girdi B'de +%32 (14 007 ↔ 10 606): iki ayrı çağrı = sabit yük iki kez (önbellekli sistem 1 370/çağrı) + kart ~700/çağrı.
- Toplu tasarım A'yı kayırıyor: A tek çağrıda sabit yükü bir kez öder. Görev başı gerçek kullanımda (her görev ayrı çağrı) A 12×,
  B 6× sabit yük öder — bu ölçülmedi (12+6 claude -p tavanı aşar).
- Görev kütlesi zor kod işlerinde (G10–G12); onlar iki kolda da Sonnet high. Kazanç payı küçük görevlerle sınırlı.

## Karar
**KAPI GEÇMEDİ** (başarı eşit, jeton +%20, kararlılık tutmadı). Yönlendirici + kayıt + yükseltme mekanizması hazır ve testli
(tests/test_yonlendir.py 6/6); ÖĞREN-2+/video hattına bağlanmadı. Sonraki ölçüm için: görev başı ayrı çağrı (her iki kol),
kart yalnız T2/T3'te ve kısaltılmış, T1 zincirinde lisans için ücretsiz kota boşken koşu.

## Alt ajan model/effort (keşif)
- code.claude.com/docs/en/sub-agents: frontmatter `model:` ve `effort:` destekli; Agent aracı çağrıda `effort` alır.
- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` kullanıcı settings.json'unda AÇIK, `CLAUDE_CODE_SUBAGENT_MODEL` yok. Belge: FORCE açıkken
  "Claude Code ignores the `model` field in subagent definitions" → alt ajanlarda kademe tablosu işlemez (model yerine hangi
  modelin geldiği ölçülmedi). Onay: `python onay/router_1b_force.py --kuru|uygula|--geri` (Ömer koşar).
