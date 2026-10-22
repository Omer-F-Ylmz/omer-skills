# opus-akis kaynakları (AJAN-AKIS-1, 22 Eki 2026)

Mekanizma alındı, kod kopyası yok. İndirme: .kos/kopru/indir/opus-akis/ (gitignore).

| Kaynak | Lisans | Ne yapıyor | fable-dusunme ile fark → karar |
|---|---|---|---|
| disler/fixing-smartass-opus-5 | MIT | Tek sistem istemi Opus 5'in "yük taşıyan bilmiş" üslubunu kısa, kanıtlı, kapsam aşmayan mühendis ortağa çevirir (sonuç başta, olgu bir kez, kanıtsız tamamlandı yok, yanlış varsayımı reddet) | fable-dusunme düşünme sırası verir, üslup/kapsam disiplini yoktu → ÖĞREN: "kapsamı aşma, sonucu başa koy, yanlış varsayımı gerekçeyle düzelt" çekirdeğe girdi |
| DannyMac180/fable-advisor | MIT | Orkestrasyon: şartname (arayüz, kısıt, doğrulama komutu), adım başı model/efor etiketi, uygulama sonrası diff + komut yeniden, boş diff başarı değil, teslimden önce danışman incelemesi, 2 başarısız denemede danış | fable-dusunme'de bağımsız doğrulama yoktu → UYARLA: "teslimden önce diff + doğrulama komutunu yeniden koş", "2 başarısız denemede yöntem değiştir" |
| mrtooher/fable-mode | lisans YOK (GitHub licenseInfo=null) | Fable tarzı çok aşamalı plan + alt ajan devri + öz-doğrulama | Lisans kapısı: içeriği okunmadı, mekanizma alınmadı → ATLANDI (lisans eklenirse yeniden değerlendir) |
| MoreThought/Fable-5.1-Max-Reasoning-* | GitHub'da yok; HF veri kümesi (10k ajan izi, ~500M jeton) | Eğitim verisi, skill değil | Çekirdek için fazla büyük, lisansı HF kartında doğrulanmadı → ATLANDI |
| ahmdd4vd/Fable5res | "Other" (belirsiz) | 4665 CoT izinden damıtılmış düşünme skill'i | Lisans MIT/Apache değil → ATLANDI |

Kendi kaynağımız (asıl veri): 3 başarılı Opus kuyruk oturumu (telve-v2-faz1b-b, neffex-klon-4-b, bhs5-d0) → tools/akis_damit.py ile 17 kalıp damıtıldı, hepsi transkript satırı + birebir alıntıyla doğrulandı (references/kalip-kanitlari.md). Önceki egitim-1 analizi (160 Opus oturumu: %91 doğrulama komutu koşar) çekirdeğin 2. adımını destekler.

## AJAN-AKIS-2 (22 Eki 2026): tüm benzer kaynaklar

Tarama: awesome/*.tsv · yetenek.tsv · kurulumlar · video-tarama (624 rapor) · devir notları → 88 repo, ~25 ilgili. Kurulu = ~/.claude/plugins. Karar: KUR (yeni kurulum) · UYARLA (mekanizma çekirdeğe) · ÖĞREN (references/) · RED.

| Aday | Lisans | Kurulu | Karar → neden |
|---|---|---|---|
| obra/superpowers | MIT | evet | UYARLA: Ruling, "sanırım" yasağı, ajan raporuna güvenme; model-açık-yaz → references |
| juliusbrussee/caveman | Apache-2.0 | hayır | UYARLA: kuralı-bozma listesi, bounded status, verify-and-stop; ses modu KURULMADI (CLAUDE.md ile örtüşür, ölçülmedi) |
| dietrichgebert/ponytail | MIT | evet | ÖĞREN: atlananı bildir, asla-kesme listesi |
| mattpocock/skills | MIT | evet | UYARLA: hipotez-önce, kırmızı/yeşil döngü, DEBUG etiketi |
| frankbria/ralph-claude-code | MIT | hayır | ÖĞREN: ilerlemesiz-N-tur eşiği, yalnız-test≠ilerleme; bash döngüsü RED |
| anthropics ralph-wiggum (claude-code/plugins) | © Anthropic, MIT/Apache DEĞİL | evet | ÖĞREN: yalnız fikir (Stop kancası + tavan); kod alınmaz |
| mikeyobrien/ralph-orchestrator, claytonfarr/ralph-playbook, vkuprin/ralph-harness, muratcankoylan/ralph-wiggum-marketer, snwfdhmp/awesome-ralph | MIT ×4 / listede yok | hayır | RED: ralph ailesi, frankbria ile aynı fikir; marketer alan dışı |
| nousresearch/hermes-agent | MIT | hayır | UYARLA→references: düzeltme sinyali, yazmadan-önce-oku, kural+NEDEN, arşivle-silme; arka plan fork KURULMADI (ekran/maliyet kuralı) |
| asgeirtj/system_prompts_leaks | CC0 | hayır | UYARLA: vaat-sonu→işi yap, kapsam daraltma bildirimi, belirsizlikte ilerle |
| x1xhlol/system-prompts-and-models-of-ai-tools | GPL-3.0 | hayır | RED: GPL, kopya alınmaz |
| yeekal/leaked-system-prompts | yok | hayır | RED: lisanssız |
| karpathy/llm-council | yok | hayır | ÖĞREN: anonim etiketli sıralama (yalnız zor, tek yargıç) |
| karpathy/autoresearch | yok | hayır | ÖĞREN: değerlendirmeyi değiştirme, kötüyse geri al; "asla durma" alınmaz |
| multica-ai/andrej-karpathy-skills | YOK (kurulu!) | evet | ÖĞREN: 4 ilke zaten ~/.claude/CLAUDE.md; lisans kapısı ihlali raporlandı, Ömer kararı: kalsın mı |
| karanb192/cache-tax | MIT | hayır | ÖĞREN: soğuk-yazma tahmini; ping KURULMADI |
| fable-advisor (DannyMac180) | MIT | evet | ajan-akis-1'de alındı |
| jakubantalik/thinking-orbs | MIT | evet | RED (çekirdek için): arayüz bileşeni, düşünme tarzı değil |
| kumamaki/claude-code-personalities | WTFPL | hayır | RED: statusline süsü |
| grooverlab/fable | MIT | hayır | RED: transkript hafızası, claude-mem var |
| mem0ai/mem0, sapientinc/hrm, michaelshimeles/skills(yok), anthropics/skills(repo lisansı yok), vostride/agent-qa(NOASSERTION) | karışık | kısmen | RED: kapsam dışı ya da lisans kapısı |
| Cloudflare avcı+çürütücü (reel) | repo yok | — | UYARLA: çekirdek "çürütmeye çalış", zor "çürütücü" |
| Orchestrator Beyin/Scout/Implementer/Verifier (reel) | istem | — | ÖĞREN: omer-notlar rol dağılımıyla örtüşür |
| /check farklı model incelemesi, claudex-loop, Advisor Tool (beta) | — | — | ÖĞREN: yazan≠inceleyen → zor/references; Codex bağımlı, beta ücretli |
| MAX_THINKING_TOKENS=10000, effort kalibrasyonu | resmî ayar | — | ÖĞREN: kalite etkisi ölçülmeden ayar değişmez |
| Sequential Thinking MCP | muhtemelen MIT, doğrulanmadı | hayır | RED: fable-dusunme aynı işi bağlam yükü olmadan yapar |
| mrtooher/fable-mode, MoreThought Fable-5.1-*, ahmdd4vd/Fable5res | yok / HF / Other | hayır | ajan-akis-1'de ATLANDI (lisans kapısı) |

Sayım: KUR 0 · UYARLA 6 · ÖĞREN 11 · RED 8 (+3 ajan-akis-1 ATLANDI). Çekirdeğe ≤120 kelime girdi; ayrıntı skills/opus-akis/references/ajan-akis-2-kaynaklar.md.
